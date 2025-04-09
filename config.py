import os

class Config:
    # Chave secreta para sessões e CSRF (pode ser gerada com os.urandom(24))
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sua-chave-secreta-aqui'

    # Caminho do banco de dados SQLite
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'database', 'db.sqlite3')

    # Evita warning do SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # SocketIO config (se necessário adicionar, aqui é o lugar)
    # SOCKETIO_MESSAGE_QUEUE = None (opcional para escalar com Redis/Fila)
