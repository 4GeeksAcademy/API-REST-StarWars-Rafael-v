import os
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import db, User, Personas, Vehiculos, Planetas, Favoritos 

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(ModelView(User, db.session, name='Usuarios', endpoint='admin_usuarios')) 

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))

    admin.add_view(ModelView(Personas, db.session, name='Personas', endpoint='admin_personas'))
    admin.add_view(ModelView(Vehiculos, db.session, name='Vehiculos', endpoint='admin_vehiculos'))
    admin.add_view(ModelView(Planetas, db.session, name='Planetas', endpoint='admin_planetas'))
    admin.add_view(ModelView(Favoritos, db.session, name='Favoritos', endpoint='admin_favoritos'))