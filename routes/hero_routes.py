from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models import HeroBase, Ficha, Campanha
import json

hero_bp = Blueprint('hero', __name__)

@hero_bp.route('/selecionar_heroi/<int:campanha_id>', methods=['GET', 'POST'])
@login_required
def selecionar_heroi(campanha_id):
    campanha = Campanha.query.get_or_404(campanha_id)
    if request.method == 'POST':
        # Obtém o ID do herói selecionado
        heroi_id = request.form.get('heroi_id')
        if not heroi_id:
            flash('Selecione um herói.')
            return redirect(url_for('hero.selecionar_heroi', campanha_id=campanha_id))
        heroi = HeroBase.query.get_or_404(heroi_id)
        # Cria uma nova ficha para o jogador usando os dados do herói escolhido
        nova_ficha = Ficha(
            nome_personagem=heroi.nome,
            classe=heroi.nome,
            nivel=1,
            raca="Desconhecida",  # Esses dados podem ser adaptados conforme necessário
            alinhamento="Neutro",
            forca=heroi.atributos_iniciais.get("FOR", 10),
            destreza=heroi.atributos_iniciais.get("DES", 10),
            constituicao=heroi.atributos_iniciais.get("CON", 10),
            inteligencia=heroi.atributos_iniciais.get("INT", 10),
            sabedoria=heroi.atributos_iniciais.get("SAB", 10),
            carisma=heroi.atributos_iniciais.get("CAR", 10),
            vida_maxima=10,  # Ou calcular com base em pv_pm do herói
            mana_maxima=10,  # Ou calcular com base em pv_pm do herói
            experiencia=0,
            jogador_id=current_user.id,
            campanha_id=campanha_id
        )
        db.session.add(nova_ficha)
        db.session.commit()
        flash('Herói selecionado e ficha criada com sucesso!')
        return redirect(url_for('main.ver_ficha', ficha_id=nova_ficha.id))
    # GET: exibe os heróis disponíveis
    herois = HeroBase.query.all()
    return render_template('selecionar_heroi.html', herois=herois, campanha=campanha)
