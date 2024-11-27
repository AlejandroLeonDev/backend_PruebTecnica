from app import db

class Movement(db.Model):
    """Modelo para la tabla de movimientos"""
    __tablename__ = 'movements'

    id_movimiento = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(50), nullable=False)

    # Relacion con vuelos
    flights = db.relationship('Flight', backref='movement', lazy=True)

    def __repr__(self):
        return f'<Movement {self.descripcion}>'

    def to_dict(self):
        return {
            'id_movimiento': self.id_movimiento,
            'descripcion': self.descripcion
        }