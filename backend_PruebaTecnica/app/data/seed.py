from app import db
from app.models import Airline, Airport, Movement, Flight
from datetime import datetime

def seed_data():
    # Crear aerolíneas
    airlines = [
        Airline(nombre_aerolinea='Volaris'),
        Airline(nombre_aerolinea='Aeromar'),
        Airline(nombre_aerolinea='Interjet'),
        Airline(nombre_aerolinea='Aeromexico')
    ]

    # Crear aeropuertos
    airports = [
        Airport(nombre_aeropuerto='Benito Juarez'),
        Airport(nombre_aeropuerto='Guanajuato'),
        Airport(nombre_aeropuerto='La paz'),
        Airport(nombre_aeropuerto='Oaxaca')
    ]

    # Crear movimientos
    movements = [
        Movement(descripcion='Salida'),
        Movement(descripcion='Llegada')
    ]

    # Agregar a la base de datos
    db.session.add_all(airlines)
    db.session.add_all(airports)
    db.session.add_all(movements)

    
    flights = [
        Flight(id_aerolinea=1, id_aeropuerto=1, id_movimiento=1, dia=datetime(2021, 5, 2)),
        Flight(id_aerolinea=2, id_aeropuerto=1, id_movimiento=1, dia=datetime(2021, 5, 2)),
        Flight(id_aerolinea=3, id_aeropuerto=2, id_movimiento=2, dia=datetime(2021, 5, 2)),
        Flight(id_aerolinea=4, id_aeropuerto=3, id_movimiento=2, dia=datetime(2021, 5, 2)),
        Flight(id_aerolinea=1, id_aeropuerto=3, id_movimiento=2, dia=datetime(2021, 5, 2)),
        Flight(id_aerolinea=2, id_aeropuerto=1, id_movimiento=1, dia=datetime(2021, 5, 2)),
        Flight(id_aerolinea=2, id_aeropuerto=3, id_movimiento=1, dia=datetime(2021, 5, 4)),
        Flight(id_aerolinea=3, id_aeropuerto=4, id_movimiento=1, dia=datetime(2021, 5, 4)),
        Flight(id_aerolinea=3, id_aeropuerto=4, id_movimiento=1, dia=datetime(2021, 5, 4))
    ]


    # Agregar vuelos a la base de datos
    db.session.add_all(flights)
    

    # Guardar cambios
    db.session.commit()