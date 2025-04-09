from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from extensions import db
from models import Campanha, Ficha, MoralityLog
from utils.decorators import mestre_required

mestre_bp = Blueprint('mestre', __name__)

@mestre_bp.route('/mestre/campanha/<int:campanha_id>')
@login_required
@mestre_required
def painel_mestre(campanha_id):
    campanha = Campanha.query.get_or_404(campanha_id)
    fichas = Ficha.query.filter_by(campanha_id=campanha_id).all()
    moralidades = MoralityLog.query.filter_by(campanha_id=campanha_id).order_by(MoralityLog.data.desc()).all()
    return render_template('mestre.html', campanha=campanha, fichas=fichas, moralidades=moralidades)

@mestre_bp.route('/mestre/campanha/<int:campanha_id>/moralidade', methods=['POST'])
@login_required
@mestre_required
def registrar_moralidade(campanha_id):
    ponto = request.form['ponto']  # luz / sombra / cinzas
    log = MoralityLog(ponto=ponto, campanha_id=campanha_id, jogador_id=current_user.id)
    db.session.add(log)
    db.session.commit()
    flash(f'Ponto de moralidade "{ponto}" registrado.')
    return redirect(url_for('mestre.painel_mestre', campanha_id=campanha_id))
