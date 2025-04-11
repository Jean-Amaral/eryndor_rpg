import json
import os
from datetime import datetime
from extensions import db
from models import HeroBase
from app import app

def importar_classes(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    classes = data.get("classes", [])
    for classe in classes:
        # Verifica se já existe uma classe com o mesmo nome (para evitar duplicatas)
        existing = HeroBase.query.filter_by(nome=classe.get("nome")).first()
        if existing:
            print(f"Classe {classe.get('nome')} já existe. Ignorando.")
            continue
        
        nova_classe = HeroBase(
            nome=classe.get("nome"),
            descricao=classe.get("descricao"),
            aparencia=classe.get("aparencia"),
            personalidade=classe.get("personalidade"),
            motivacao=classe.get("motivacao"),
            lore=classe.get("lore"),
            atributos_iniciais=classe.get("atributos_iniciais"),
            pv_pm=classe.get("pv_pm"),
            proficiencias=classe.get("proficiencias"),
            armas=classe.get("armas"),
            habilidades_normais=classe.get("habilidades_normais"),
            habilidade_ultimate=classe.get("habilidade_ultimate"),
            talentos_exemplo_nivel_3=classe.get("talentos_exemplo_nivel_3"),
            evolucoes_exemplo=classe.get("evolucoes_exemplo")
        )
        db.session.add(nova_classe)
    
    try:
        db.session.commit()
        print("Importação concluída com sucesso!")
    except Exception as e:
        db.session.rollback()
        print("Erro na importação:", e)

if __name__ == '__main__':
    # Caminho do arquivo JSON (ajuste conforme necessário)
    json_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'database', 'classes.json')
    with app.app_context():
        db.create_all()  # Certifica que as tabelas existem
        importar_classes(json_file)
