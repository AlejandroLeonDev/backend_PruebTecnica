from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from .config import config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    # Registrar blueprints
    from app.api import api as api_blueprint  # Importar el blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    @app.cli.command("seed-db")
    def seed_db():
        """Cargar datos iniciales"""
        from app.data.seed import seed_data
        seed_data()
        print("Datos cargados exitosamente!")

    return app