from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from extensions import db, login_manager

# Modelo de Usuário
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    campanhas = db.relationship('Campanha', backref='criador', lazy=True)
    fichas = db.relationship('Ficha', backref='jogador', lazy=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Modelo de Campanha
class Campanha(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    mestre_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    fichas = db.relationship('Ficha', backref='campanha', lazy=True)
    moralidade = db.relationship('MoralityLog', backref='campanha', lazy=True)

# Modelo de Ficha (Personagem)
class Ficha(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_personagem = db.Column(db.String(100), nullable=False)
    classe = db.Column(db.String(50))
    nivel = db.Column(db.Integer, default=1)
    raca = db.Column(db.String(50))
    alinhamento = db.Column(db.String(20))
    forca = db.Column(db.Integer, default=10)
    destreza = db.Column(db.Integer, default=10)
    constituicao = db.Column(db.Integer, default=10)
    inteligencia = db.Column(db.Integer, default=10)
    sabedoria = db.Column(db.Integer, default=10)
    carisma = db.Column(db.Integer, default=10)
    vida_maxima = db.Column(db.Integer, default=10)
    mana_maxima = db.Column(db.Integer, default=10)
    experiencia = db.Column(db.Integer, default=0)
    jogador_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    campanha_id = db.Column(db.Integer, db.ForeignKey('campanha.id'), nullable=False)

# Modelo de Log de Moralidade
class MoralityLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ponto = db.Column(db.String(10), nullable=False)
    campanha_id = db.Column(db.Integer, db.ForeignKey('campanha.id'), nullable=False)
    jogador_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    data = db.Column(db.DateTime, default=datetime.utcnow)

# Modelo de Histórico de Rolagens (Battle Log)
class HistoricoRolagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jogador = db.Column(db.String(100))
    pericia = db.Column(db.String(50))
    expressao = db.Column(db.String(50))
    total = db.Column(db.Integer)
    detalhes = db.Column(db.String(100))
    data = db.Column(db.DateTime, default=datetime.utcnow)

# Novo Modelo: Base dos Heróis (informações padrão das 15 Classes Puras de Eryndor)
class HeroBase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    aparencia = db.Column(db.Text)
    personalidade = db.Column(db.Text)
    motivacao = db.Column(db.Text)
    lore = db.Column(db.Text)
    # Armazenados em formato JSON para facilitar a manipulação
    atributos_iniciais = db.Column(db.JSON)
    pv_pm = db.Column(db.JSON)
    proficiencias = db.Column(db.JSON)
    armas = db.Column(db.JSON)
    habilidades_normais = db.Column(db.JSON)     # Lista de habilidades normais
    habilidade_ultimate = db.Column(db.JSON)
    talentos_exemplo_nivel_3 = db.Column(db.JSON)
    evolucoes_exemplo = db.Column(db.JSON)
