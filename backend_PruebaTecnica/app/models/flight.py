from app import db
from datetime import datetime

class Flight(db.Model):
    """Modelo para la tabla de vuelos"""
    __tablename__ = 'flights'

    id = db.Column(db.Integer, primary_key=True)
    id_aerolinea = db.Column(db.Integer, db.ForeignKey('airlines.id_aerolinea'), nullable=False)
    id_aeropuerto = db.Column(db.Integer, db.ForeignKey('airports.id_aeropuerto'), nullable=False)
    id_movimiento = db.Column(db.Integer, db.ForeignKey('movements.id_movimiento'), nullable=False)
    dia = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f'<Flight {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'id_aerolinea': self.id_aerolinea,
            'id_aeropuerto': self.id_aeropuerto,
            'id_movimiento': self.id_movimiento,
            'dia': self.dia.strftime('%Y-%m-%d')
        }