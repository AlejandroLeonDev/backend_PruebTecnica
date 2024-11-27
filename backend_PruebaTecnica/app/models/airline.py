from app import db

class Airline(db.Model):
    """Modelo para la tabla de aerolineas"""
    __tablename__ = 'airlines'

    id_aerolinea = db.Column(db.Integer, primary_key=True)
    nombre_aerolinea = db.Column(db.String(100), nullable=False)

    # Relacion con vuelos
    flights = db.relationship('Flight', backref='airline', lazy=True)

    def __repr__(self):
        return f'<Airline {self.nombre_aerolinea}>'

    def to_dict(self):
        return {
            'id_aerolinea': self.id_aerolinea,
            'nombre_aerolinea': self.nombre_aerolinea
        }