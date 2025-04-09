# Estrutura de Diretórios e Arquivos - Projeto Flask: Eryndor Fichas Interativas

# Estrutura Geral
eryndor_rpg/
|
|│-- app.py                       # Inicializa a aplicação Flask, SocketIO e registra as rotas
|│-- config.py                    # Configuração da aplicação (segurança, DB, etc.)
|│-- models.py                    # Modelos SQLAlchemy (Usuário, Ficha, Campanha)
|│-- routes/
|   |│-- auth_routes.py             # Login, logout, registro
|   |│-- main_routes.py             # Dashboard, campanhas, fichas
|   |│-- mestre_routes.py           # Painel e ferramentas do mestre
|│-- utils/
|   |│-- dice.py                   # Lógica de rolagem de dados (ex: "2d6+3")
|   |│-- decorators.py             # Decoradores personalizados (login_required, mestre_required)
|│-- templates/
|   |│-- base.html                 # Layout base com cabeçalho, navbar, etc.
|   |│-- login.html                # Tela de login
|   |│-- register.html             # Tela de cadastro
|   |│-- dashboard.html            # Tela principal após login
|   |│-- campanha.html            # Detalhes da campanha (info + fichas vinculadas)
|   |│-- ficha.html                # Tela de edição e visualização da ficha do jogador
|   |│-- mestre.html               # Tela do mestre com ferramentas específicas
|│-- static/
|   |│-- css/
|   |   └-- style.css               # Estilização principal
|   |│-- js/
|   |   ├-- ficha.js                # Lógica interativa da ficha
|   |   ├-- socket.js               # Comunicação com servidor via SocketIO
|   |   └-- dados.js                # Interface de rolagem de dados e botões
|│-- database/
|   |│-- db.sqlite3                # Arquivo de banco de dados SQLite
|│-- requirements.txt             # Dependências do projeto
|│-- README.md                    # Instruções de instalação e uso

# Conteúdo Esperado em Cada Parte

## app.py
- Inicializa Flask, SQLAlchemy, Flask-Login, SocketIO
- Registra rotas a partir da pasta "routes"
- Configura eventos do SocketIO (rolagem de dados, sincronização de fichas)

## config.py
- Chave secreta, configuração de SQLite, timeout de sessão, entre outros

## models.py
- Modelos: Usuário, Ficha (Personagem), Campanha, MoralityLog, Histórico de Rolação

## utils/dice.py
- Função principal: roll_dice(expression)
- Valida rolagens, interpreta expressões e retorna estrutura com resultados

## templates
- Sistema baseado em `base.html`
- Cada template representa uma página funcional completa

## static/js
- `socket.js` para lidar com a troca em tempo real (dados, fichas, rolagens)
- `ficha.js` para operações de interface do jogador
- `dados.js` para ativar botoes de rolagem e mostrar resultados

## requirements.txt
```txt
Flask
Flask-SQLAlchemy
Flask-Login
Flask-SocketIO
python-dotenv
```

## README.md
- Explica como instalar, rodar e usar o sistema
- Explica comandos de terminal, inicialização do banco, e cadastro inicial de campanha

---