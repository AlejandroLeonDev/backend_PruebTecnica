from flask import Blueprint, jsonify
from app.models import Airline, Airport, Movement, Flight
from ..services.stackoverflow_service import (
    StackOverflowService, 
    APIError, 
    ValidationError, 
    ServiceError
)

from app import db
from sqlalchemy import func

api = Blueprint('api', __name__)
stack_service = StackOverflowService()

# Rutas básicas
@api.route('/airlines', methods=['GET'])
def get_airlines():
    airlines = Airline.query.all()
    result = [{
        'id_aerolinea': airline.id_aerolinea,
        'nombre_aerolinea': airline.nombre_aerolinea
    } for airline in airlines]
    return jsonify(result)

@api.route('/airports', methods=['GET'])
def get_airports():
    airports = Airport.query.all()
    result = [{
        'id_aeropuerto': airport.id_aeropuerto,
        'nombre_aeropuerto': airport.nombre_aeropuerto
    } for airport in airports]
    return jsonify(result)

@api.route('/movements', methods=['GET'])
def get_movements():
    movements = Movement.query.all()
    result = [{
        'id_movimiento': movement.id_movimiento,
        'descripcion': movement.descripcion
    } for movement in movements]
    return jsonify(result)

# Rutas analíticas
@api.route('/analytics/busiest-airport', methods=['GET'])
def get_busiest_airport():
    """Aeropuerto que ha tenido mayor movimiento durante el año"""
    result = db.session.query(
        Airport.nombre_aeropuerto,
        db.func.count(Flight.id).label('total_movements')
    ).join(Flight).group_by(Airport.id_aeropuerto, Airport.nombre_aeropuerto)\
    .order_by(db.func.count(Flight.id).desc()).first()
    
    return jsonify({
        'airport': result[0] if result else None,
        'total_movements': result[1] if result else 0
    })

@api.route('/analytics/most-active-airline', methods=['GET'])
def get_most_active_airline():
    """Aerolínea con mayor número de vuelos"""
    result = db.session.query(
        Airline.nombre_aerolinea,
        db.func.count(Flight.id).label('total_flights')
    ).join(Flight).group_by(Airline.id_aerolinea, Airline.nombre_aerolinea)\
    .order_by(db.func.count(Flight.id).desc()).first()
    
    return jsonify({
        'airline': result[0] if result else None,
        'total_flights': result[1] if result else 0
    })

@api.route('/analytics/busiest-day', methods=['GET'])
def get_busiest_day():
    """Día con mayor número de vuelos"""
    result = db.session.query(
        Flight.dia,
        db.func.count(Flight.id).label('total_flights')
    ).group_by(Flight.dia)\
    .order_by(db.func.count(Flight.id).desc()).first()
    
    return jsonify({
        'date': result[0].strftime('%Y-%m-%d') if result else None,
        'total_flights': result[1] if result else 0
    })

@api.route('/analytics/airlines-multiple-daily', methods=['GET'])
def get_airlines_multiple_daily():
    """Aerolíneas con más de 2 vuelos por día"""
    result = db.session.query(
        Airline.nombre_aerolinea,
        Flight.dia,
        db.func.count(Flight.id).label('flights_per_day')
    ).join(Airline)\
    .group_by(Airline.nombre_aerolinea, Flight.dia)\
    .having(db.func.count(Flight.id) > 2).all()
    
    return jsonify([{
        'airline': r[0],
        'date': r[1].strftime('%Y-%m-%d'),
        'flights': r[2]
    } for r in result])

# Nuevas rutas para Stack Exchange
@api.route('/stack/statistics', methods=['GET'])
def get_stack_statistics():
    """Obtener estadísticas de respuestas"""
    try:
        stats = stack_service.get_answer_statistics()
        return jsonify({
            'status': 'success',
            'data': stats
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@api.route('/stack/highest-reputation', methods=['GET'])
def get_highest_reputation():
    """Obtener respuesta con mayor reputación"""
    try:
        answer = stack_service.get_highest_reputation_answer()
        if not answer:
            return jsonify({
                'status': 'error',
                'message': 'No answers found'
            }), 404
        return jsonify({
            'status': 'success',
            'data': answer
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@api.route('/stack/least-viewed', methods=['GET'])
def get_least_viewed():
    """Obtener respuesta menos vista"""
    try:
        answer = stack_service.get_least_viewed_answer()
        if not answer:
            return jsonify({
                'status': 'error',
                'message': 'No answers found'
            }), 404
        return jsonify({
            'status': 'success',
            'data': answer
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@api.route('/stack/timeline', methods=['GET'])
def get_timeline():
    """Obtener línea de tiempo de respuestas"""
    try:
        timeline = stack_service.get_answer_timeline()
        if not timeline['oldest'] or not timeline['newest']:
            return jsonify({
                'status': 'error',
                'message': 'No answers found'
            }), 404
        return jsonify({
            'status': 'success',
            'data': timeline
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@api.route('/stack/analytics', methods=['GET'])
def print_stack_analytics():
    """Imprimir y devolver analytics completos"""
    try:
        # Imprimir en consola
        stack_service.print_analytics()
        
        # Recopilar todos los datos
        data = {
            'statistics': stack_service.get_answer_statistics(),
            'highest_reputation': stack_service.get_highest_reputation_answer(),
            'least_viewed': stack_service.get_least_viewed_answer(),
            'timeline': stack_service.get_answer_timeline()
        }
        
        return jsonify({
            'status': 'success',
            'data': data
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500