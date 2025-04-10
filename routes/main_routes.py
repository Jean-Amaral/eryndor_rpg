from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from extensions import db
from models import Campanha, Ficha, HistoricoRolagem

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required
def dashboard():
    campanhas = Campanha.query.filter_by(mestre_id=current_user.id).all()
    fichas = Ficha.query.filter_by(jogador_id=current_user.id).all()
    return render_template('dashboard.html', campanhas=campanhas, fichas=fichas)

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

@main_bp.route('/campanha/<int:campanha_id>')
@login_required
def ver_campanha(campanha_id):
    campanha = Campanha.query.get_or_404(campanha_id)
    if campanha.mestre_id != current_user.id and current_user not in [f.jogador for f in campanha.fichas]:
        flash('Acesso negado.')
        return redirect(url_for('main.dashboard'))

    return render_template('campanha.html', campanha=campanha)

@main_bp.route('/ficha/<int:ficha_id>')
@login_required
def ver_ficha(ficha_id):
    ficha = Ficha.query.get_or_404(ficha_id)
    # Verifica acesso: se o usuário não é o dono da ficha nem o mestre da campanha, bloqueia o acesso
    if ficha.jogador_id != current_user.id and ficha.campanha.mestre_id != current_user.id:
        flash('Acesso negado.')
        return redirect(url_for('main.dashboard'))
    # Carrega o histórico de rolagens, ordenado por data decrescente
    logs = HistoricoRolagem.query.order_by(HistoricoRolagem.data.desc()).all()
    return render_template('ficha.html', ficha=ficha, logs=logs)
