from app import db

class Airport(db.Model):
    """Modelo para la tabla de aeropuertos"""
    __tablename__ = 'airports'

    id_aeropuerto = db.Column(db.Integer, primary_key=True)
    nombre_aeropuerto = db.Column(db.String(100), nullable=False)

    # Relacion con vuelos
    flights = db.relationship('Flight', backref='airport', lazy=True)

    def __repr__(self):
        return f'<Airport {self.nombre_aeropuerto}>'

    def to_dict(self):
        return {
            'id_aeropuerto': self.id_aeropuerto,
            'nombre_aeropuerto': self.nombre_aeropuerto
        }