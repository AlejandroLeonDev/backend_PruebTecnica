# app/services/stackoverflow_service.py

import requests
from datetime import datetime
from typing import Dict, Optional
from functools import wraps
import logging

class StackOverflowService:
    """
    Servicio para manejar las interacciones con la API de Stack Exchange.
    Proporciona métodos para obtener y analizar datos de Stack Overflow.
    """
    
    def __init__(self):
        """
        Inicializa el servicio con la configuración base.
        """
        self.base_url = "https://api.stackexchange.com/2.2"
        self.search_params = {
            'order': 'desc',
            'sort': 'activity',
            'intitle': 'perl',
            'site': 'stackoverflow'
        }

    def _get_data(self) -> Dict:
        """
        Método privado para obtener datos de la API.
        
        Returns:
            Dict: Datos obtenidos de la API o diccionario vacío en caso de error
        """
        try:
            response = requests.get(
                f"{self.base_url}/search",
                params=self.search_params
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error al obtener datos de Stack Exchange: {str(e)}")
            return {'items': []}

    def get_answer_statistics(self) -> Dict[str, int]:
        """
        Obtiene estadísticas sobre respuestas contestadas y no contestadas.
        
        Returns:
            Dict[str, int]: Diccionario con estadísticas de respuestas
        """
        data = self._get_data()
        items = data.get('items', [])
        
        total = len(items)
        answered = sum(1 for item in items if item.get('is_answered', False))
        
        return {
            'total_questions': total,
            'answered': answered,
            'unanswered': total - answered,
            'answer_rate': round((answered / total * 100), 2) if total > 0 else 0
        }

    def get_highest_reputation_answer(self) -> Optional[Dict]:
        """
        Obtiene la respuesta con mayor reputación.
        
        Returns:
            Optional[Dict]: Datos de la respuesta con mayor reputación o None
        """
        data = self._get_data()
        items = data.get('items', [])
        
        if not items:
            return None
            
        highest_rep = max(items, key=lambda x: x.get('owner', {}).get('reputation', 0))
        
        return {
            'title': highest_rep.get('title'),
            'author': highest_rep.get('owner', {}).get('display_name'),
            'reputation': highest_rep.get('owner', {}).get('reputation'),
            'score': highest_rep.get('score'),
            'link': highest_rep.get('link')
        }

    def get_least_viewed_answer(self) -> Optional[Dict]:
        """
        Obtiene la respuesta con menor número de vistas.
        
        Returns:
            Optional[Dict]: Datos de la respuesta menos vista o None
        """
        data = self._get_data()
        items = data.get('items', [])
        
        if not items:
            return None
            
        least_viewed = min(items, key=lambda x: x.get('view_count', float('inf')))
        
        return {
            'title': least_viewed.get('title'),
            'views': least_viewed.get('view_count'),
            'link': least_viewed.get('link'),
            'created_at': datetime.fromtimestamp(
                least_viewed.get('creation_date', 0)
            ).strftime('%Y-%m-%d %H:%M:%S')
        }

    def get_answer_timeline(self) -> Dict:
        """
        Obtiene las respuestas más antigua y más reciente.
        
        Returns:
            Dict: Diccionario con la respuesta más antigua y más reciente
        """
        data = self._get_data()
        items = data.get('items', [])
        
        if not items:
            return {'oldest': None, 'newest': None}
            
        oldest = min(items, key=lambda x: x.get('creation_date', float('inf')))
        newest = max(items, key=lambda x: x.get('creation_date', 0))
        
        def format_answer(answer: Dict) -> Dict:
            return {
                'title': answer.get('title'),
                'created_at': datetime.fromtimestamp(
                    answer.get('creation_date', 0)
                ).strftime('%Y-%m-%d %H:%M:%S'),
                'link': answer.get('link'),
                'score': answer.get('score')
            }
        
        return {
            'oldest': format_answer(oldest),
            'newest': format_answer(newest)
        }

    def print_analytics(self) -> None:
        """
        Imprime todos los análisis en la consola.
        """
        try:
            # Obtener datos
            stats = self.get_answer_statistics()
            high_rep = self.get_highest_reputation_answer()
            least_viewed = self.get_least_viewed_answer()
            timeline = self.get_answer_timeline()
            
            # Imprimir estadísticas
            print("\n=== Estadísticas de Stack Overflow ===")
            print(f"\nTotal de preguntas: {stats['total_questions']}")
            print(f"Contestadas: {stats['answered']}")
            print(f"Sin contestar: {stats['unanswered']}")
            print(f"Tasa de respuesta: {stats['answer_rate']}%")
            
            if high_rep:
                print("\nRespuesta con mayor reputación:")
                print(f"Título: {high_rep['title']}")
                print(f"Autor: {high_rep['author']}")
                print(f"Reputación: {high_rep['reputation']}")
                
            if least_viewed:
                print("\nRespuesta menos vista:")
                print(f"Título: {least_viewed['title']}")
                print(f"Vistas: {least_viewed['views']}")
                print(f"Creada: {least_viewed['created_at']}")
                
            if timeline['oldest'] and timeline['newest']:
                print("\nLínea de tiempo:")
                print(f"Más antigua: {timeline['oldest']['created_at']}")
                print(f"Más reciente: {timeline['newest']['created_at']}")
                
        except Exception as e:
            print(f"Error al imprimir analytics: {str(e)}")


    
    # Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def handle_api_errors(func):
    """Decorador para manejar errores de API de manera consistente"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.RequestException as e:
            logger.error(f"Error de API en {func.__name__}: {str(e)}")
            raise APIError(f"Error al comunicarse con Stack Exchange: {str(e)}")
        except ValueError as e:
            logger.error(f"Error de validación en {func.__name__}: {str(e)}")
            raise ValidationError(str(e))
        except Exception as e:
            logger.error(f"Error inesperado en {func.__name__}: {str(e)}")
            raise ServiceError(f"Error interno del servicio: {str(e)}")
    return wrapper

class APIError(Exception):
    """Error específico para problemas de API"""
    pass

class ValidationError(Exception):
    """Error específico para problemas de validación"""
    pass

class ServiceError(Exception):
    """Error específico para problemas internos del servicio"""
    pass

class StackOverflowService:
    def __init__(self):
        self.base_url = "https://api.stackexchange.com/2.2"
        self.search_params = {
            'order': 'desc',
            'sort': 'activity',
            'intitle': 'perl',
            'site': 'stackoverflow'
        }
        self.cache = {}
        self.cache_duration = 300  # 5 minutos en segundos

    def validate_response(self, data: Dict) -> None:
        """Valida la respuesta de la API"""
        if not isinstance(data, dict):
            raise ValidationError("Respuesta inválida de la API")
        if 'items' not in data:
            raise ValidationError("Formato de respuesta inválido")
        if not isinstance(data['items'], list):
            raise ValidationError("Datos de items inválidos")

    @handle_api_errors
    def _get_data(self) -> Dict:
        """Obtiene datos de la API con validación"""
        try:
            response = requests.get(
                f"{self.base_url}/search",
                params=self.search_params,
                timeout=10  # Timeout de 10 segundos
            )
            response.raise_for_status()
            data = response.json()
            self.validate_response(data)
            return data
        except requests.Timeout:
            raise APIError("Timeout al conectar con Stack Exchange")
        except requests.RequestException as e:
            raise APIError(f"Error de conexión: {str(e)}")

    def validate_statistics(self, stats: Dict) -> None:
        """Valida las estadísticas calculadas"""
        required_fields = ['total_questions', 'answered', 'unanswered', 'answer_rate']
        for field in required_fields:
            if field not in stats:
                raise ValidationError(f"Campo requerido faltante: {field}")
        
        if stats['answered'] + stats['unanswered'] != stats['total_questions']:
            raise ValidationError("Inconsistencia en las estadísticas")

    @handle_api_errors
    def get_answer_statistics(self) -> Dict[str, int]:
        """Obtiene estadísticas con validación"""
        data = self._get_data()
        items = data.get('items', [])
        
        if not items:
            return {
                'total_questions': 0,
                'answered': 0,
                'unanswered': 0,
                'answer_rate': 0
            }
        
        total = len(items)
        answered = sum(1 for item in items if item.get('is_answered', False))
        
        stats = {
            'total_questions': total,
            'answered': answered,
            'unanswered': total - answered,
            'answer_rate': round((answered / total * 100), 2) if total > 0 else 0
        }
        
        self.validate_statistics(stats)
        return stats

    def validate_answer(self, answer: Dict) -> None:
        """Valida los datos de una respuesta"""
        required_fields = ['title', 'link']
        for field in required_fields:
            if not answer.get(field):
                raise ValidationError(f"Campo requerido faltante en respuesta: {field}")

    @handle_api_errors
    def get_highest_reputation_answer(self) -> Optional[Dict]:
        """Obtiene respuesta con mayor reputación con validación"""
        data = self._get_data()
        items = data.get('items', [])
        
        if not items:
            return None
            
        highest_rep = max(items, key=lambda x: x.get('owner', {}).get('reputation', 0))
        
        answer = {
            'title': highest_rep.get('title'),
            'author': highest_rep.get('owner', {}).get('display_name'),
            'reputation': highest_rep.get('owner', {}).get('reputation'),
            'score': highest_rep.get('score'),
            'link': highest_rep.get('link')
        }
        
        self.validate_answer(answer)
        return answer

    def log_api_call(self, method_name: str, response: Dict) -> None:
        """Registra las llamadas a la API"""
        logger.info(f"API Call - Method: {method_name}")
        logger.info(f"Response Status: success")
        logger.info(f"Response Data Size: {len(str(response))} bytes")