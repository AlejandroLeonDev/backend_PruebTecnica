from flask import Flask
from flask_migrate import Migrate
from app import create_app
from app import db
from app.models import Airline, Airport, Movement, Flight

app = create_app()
migrate = Migrate(app, db)


@app.route('/')
def home():
    return "¡Bienvenido al backend del Proyecto Técnico!"


if __name__ == '__main__':
    app.run(debug=True)