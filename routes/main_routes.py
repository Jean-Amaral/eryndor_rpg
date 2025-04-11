from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from extensions import db
from models import Campanha, Ficha, HistoricoRolagem

main_bp = Blueprint('main', __name__)

# Rota raiz - redireciona para o dashboard
@main_bp.route('/')
@login_required
def index():
    return redirect(url_for('main.dashboard'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    # Campanhas onde o usuário é mestre
    campanhas_mestre = Campanha.query.filter_by(mestre_id=current_user.id).all()
    
    # Campanhas onde o usuário participa como jogador (tem ficha)
    campanhas_jogador_query = Ficha.query.filter_by(jogador_id=current_user.id).with_entities(Ficha.campanha_id).distinct().all()
    campanhas_jogador_ids = [campanha_id for (campanha_id,) in campanhas_jogador_query]
    campanhas_jogador = Campanha.query.filter(Campanha.id.in_(campanhas_jogador_ids)).all()
    
    return render_template('dashboard.html', campanhas_mestre=campanhas_mestre, campanhas_jogador=campanhas_jogador)

@main_bp.route('/criar_campanha', methods=['POST'])
@login_required
def criar_campanha():
    titulo = request.form['titulo']
    descricao = request.form['descricao']

    campanha = Campanha(titulo=titulo, descricao=descricao, mestre_id=current_user.id)
    db.session.add(campanha)
    db.session.commit()
    flash('Campanha criada com sucesso.')
    return redirect(url_for('main.dashboard'))

@main_bp.route('/entrar_campanha/<int:campanha_id>')
@login_required
def entrar_campanha(campanha_id):
    campanha = Campanha.query.get_or_404(campanha_id)
    if campanha.mestre_id == current_user.id:
        # Se o usuário é o mestre, direciona para o painel do mestre
        return redirect(url_for('mestre.painel_mestre', campanha_id=campanha.id))
    else:
        # Se jogador: se já tiver ficha, continua; se não, encaminha para seleção de herói.
        ficha = Ficha.query.filter_by(jogador_id=current_user.id, campanha_id=campanha.id).first()
        if ficha:
            return redirect(url_for('main.ver_campanha', campanha_id=campanha.id))
        else:
            return redirect(url_for('hero.selecionar_heroi', campanha_id=campanha.id))

@main_bp.route('/campanha/<int:campanha_id>')
@login_required
def ver_campanha(campanha_id):
    campanha = Campanha.query.get_or_404(campanha_id)
    if campanha.mestre_id != current_user.id:
        ficha = Ficha.query.filter_by(jogador_id=current_user.id, campanha_id=campanha.id).first()
        if not ficha:
            flash('Acesso negado.')
            return redirect(url_for('main.dashboard'))
    return render_template('campanha.html', campanha=campanha)

# Nova rota para visualizar a ficha, para quando o jogador quiser ver os detalhes da sua ficha
@main_bp.route('/ficha/<int:ficha_id>')
@login_required
def ver_ficha(ficha_id):
    ficha = Ficha.query.get_or_404(ficha_id)
    # Verifica se o usuário tem acesso à ficha (é o dono ou o mestre da campanha)
    if ficha.jogador_id != current_user.id and ficha.campanha.mestre_id != current_user.id:
        flash('Acesso negado.')
        return redirect(url_for('main.dashboard'))
    # Carrega o histórico de rolagens (battle log) para essa ficha
    logs = HistoricoRolagem.query.order_by(HistoricoRolagem.data.desc()).all()
    return render_template('ficha.html', ficha=ficha, logs=logs)
