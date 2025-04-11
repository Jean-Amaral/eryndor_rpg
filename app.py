from flask import Flask, request
from config import Config
from extensions import db, login_manager, socketio
from datetime import datetime

# Inicializa a aplicação Flask
app = Flask(__name__)
app.config.from_object(Config)

# Inicializa as extensões
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
socketio.init_app(app, manage_session=False)

# Importa os modelos
from models import User, Campanha, Ficha, MoralityLog, HistoricoRolagem

# Importa e registra os blueprints
from routes.auth_routes import auth_bp
from routes.main_routes import main_bp
from routes.mestre_routes import mestre_bp
from routes.hero_routes import hero_bp  # Para seleção de herói

app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.register_blueprint(mestre_bp)
app.register_blueprint(hero_bp)

# Injeta a variável global 'now' para uso nos templates
@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

# --- SOCKET.IO: Eventos ---
from flask_socketio import emit, join_room, leave_room
from utils.dice import roll_dice

# Dicionário para rastrear usuários conectados (SID -> {user_id, nome})
online_users = {}  # Exemplo: { "AbCdEf123": {"user_id": "1", "nome": "Jean"} }

@socketio.on('connect')
def handle_connect():
    print(f"[SocketIO] Conectado: {request.sid}")

@socketio.on('usuario_logado')
def handle_usuario_logado(data):
    sid = request.sid
    user_id = data.get('user_id')
    nome = data.get('nome')
    if user_id is None or nome is None:
        print("[SocketIO] Erro: dados do usuário ausentes ao emitir usuario_logado.")
        return
    # Converte user_id para string para consistência com join_room
    user_id = str(user_id)
    online_users[sid] = {'user_id': user_id, 'nome': nome}
    join_room(user_id)
    print(f"[SocketIO] {nome} entrou online com user_id {user_id} e SID {sid}.")
    # Envia confirmação para o próprio usuário
    emit('usuario_logado_confirmado', {'status': 'ok', 'room': user_id}, to=user_id)
    # Atualiza a lista de usuários online para todos
    emit('usuarios_online', list(online_users.values()), broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    user = online_users.pop(sid, None)
    if user:
        leave_room(str(user['user_id']))
        print(f"[SocketIO] {user['nome']} desconectado (SID {sid}).")
        emit('usuarios_online', list(online_users.values()), broadcast=True)

@socketio.on('roll')
def handle_roll(data):
    result = roll_dice(data['expression'])
    result['jogador'] = data.get('user', 'Desconhecido')
    result['pericia'] = data.get('pericia', 'Livre')
    emit('nova_rolagem', result, broadcast=True)
    # Salva o histórico de rolagens (battle log)
    try:
        new_log = HistoricoRolagem(
            jogador=result['jogador'],
            pericia=result['pericia'],
            expressao=result.get('expressao', data['expression']),
            total=result.get('total', 0),
            detalhes=", ".join(map(str, result.get('rolagens', []))),
            data=datetime.utcnow()
        )
        db.session.add(new_log)
        db.session.commit()
        print(f"[SocketIO] Histórico salvo: {new_log.expressao} = {new_log.total}")
    except Exception as e:
        db.session.rollback()
        print(f"[SocketIO] Erro ao salvar histórico: {e}")

@socketio.on('convidar_para_campanha')
def handle_convite(data):
    campanha_id = data.get('campanha_id')
    destino_id = data.get('user_id')
    if not campanha_id or not destino_id:
        print("[SocketIO] Dados incompletos para convite.")
        return
    destino_id = str(destino_id)
    print(f"[SocketIO] Tentando convidar jogador com user_id {destino_id} para campanha #{campanha_id}")
    emit('convite_recebido', {
        'campanha_id': campanha_id,
        'mensagem': f"Voc\u00ea foi convidado para a campanha #{campanha_id}!"
    }, to=destino_id)
    print(f"[SocketIO] Convite emitido para sala {destino_id}.")

@socketio.on('aceitar_convite')
def handle_aceitar_convite(data):
    campanha_id = data.get('campanha_id')
    user_id = data.get('user_id')
    if not campanha_id or not user_id:
        print("[SocketIO] Dados incompletos para aceitar convite.")
        return
    user_id = str(user_id)
    print(f"[SocketIO] Usuário {user_id} aceitou convite para campanha #{campanha_id}.")
    from models import Ficha
    ficha_existente = Ficha.query.filter_by(jogador_id=user_id, campanha_id=campanha_id).first()
    if ficha_existente:
        print(f"[SocketIO] Usuário {user_id} já possui ficha na campanha {campanha_id}.")
        emit('convite_aceito', {'campanha_id': campanha_id, 'rota': 'ver_campanha'}, to=user_id)
    else:
        print(f"[SocketIO] Nenhuma ficha encontrada para usuário {user_id} na campanha {campanha_id}. Encaminhando para seleção de herói.")
        emit('convite_aceito', {'campanha_id': campanha_id, 'rota': 'selecionar_heroi'}, to=user_id)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
