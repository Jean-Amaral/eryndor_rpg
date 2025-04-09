from functools import wraps
from flask import flash, redirect, url_for, request
from flask_login import current_user
from models import Campanha

def mestre_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        campanha_id = kwargs.get('campanha_id')
        campanha = Campanha.query.get(campanha_id)

        if not campanha or campanha.mestre_id != current_user.id:
            flash('Apenas o mestre da campanha pode acessar esta página.')
            return redirect(url_for('main.dashboard'))

        return f(*args, **kwargs)
    return decorated_function
