# test_integration.py
import requests
import json
from datetime import datetime
from colorama import init, Fore, Style

init()  # Inicializar colorama

class IntegrationTester:
    def __init__(self, base_url="http://127.0.0.1:5000"):
        self.base_url = base_url
        self.success_count = 0
        self.fail_count = 0
        self.total_tests = 0

    def print_header(self, message):
        print(f"\n{Fore.CYAN}{'='*20} {message} {'='*20}{Style.RESET_ALL}")

    def print_result(self, test_name, success, response=None, error=None):
        self.total_tests += 1
        if success:
            self.success_count += 1
            print(f"{Fore.GREEN}✓ {test_name} - PASÓ{Style.RESET_ALL}")
            if response:
                print(f"{Fore.WHITE}Respuesta:{Style.RESET_ALL}")
                print(json.dumps(response, indent=2))
        else:
            self.fail_count += 1
            print(f"{Fore.RED}✗ {test_name} - FALLÓ{Style.RESET_ALL}")
            if error:
                print(f"{Fore.RED}Error: {error}{Style.RESET_ALL}")

    def validate_stack_response(self, response):
        """Valida la estructura básica de respuesta"""
        if not isinstance(response, dict):
            raise ValueError("La respuesta no es un diccionario")
        if 'status' not in response:
            raise ValueError("Falta el campo 'status' en la respuesta")
        if response['status'] not in ['success', 'error']:
            raise ValueError("Estado de respuesta inválido")
        if 'data' not in response and response['status'] == 'success':
            raise ValueError("Falta el campo 'data' en una respuesta exitosa")

    def test_endpoint(self, endpoint, test_name, validations=None):
        """Prueba un endpoint específico con validaciones opcionales"""
        try:
            response = requests.get(f"{self.base_url}{endpoint}")
            response_data = response.json()
            
            # Validar estructura básica
            self.validate_stack_response(response_data)
            
            # Ejecutar validaciones específicas si existen
            if validations and response_data['status'] == 'success':
                validations(response_data['data'])
            
            self.print_result(test_name, True, response_data)
            return True
        except Exception as e:
            self.print_result(test_name, False, error=str(e))
            return False

    def validate_statistics(self, data):
        """Valida los datos de estadísticas"""
        required_fields = ['total_questions', 'answered', 'unanswered', 'answer_rate']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Campo faltante en estadísticas: {field}")
        if data['answered'] + data['unanswered'] != data['total_questions']:
            raise ValueError("Inconsistencia en las estadísticas")

    def validate_timeline(self, data):
        """Valida los datos de timeline"""
        if 'oldest' not in data or 'newest' not in data:
            raise ValueError("Faltan campos en timeline")
        for entry in [data['oldest'], data['newest']]:
            if entry and 'created_at' not in entry:
                raise ValueError("Falta fecha de creación en timeline")

    def run_all_tests(self):
        """Ejecuta todas las pruebas de integración"""
        self.print_header("INICIANDO PRUEBAS DE INTEGRACIÓN")

        # Probar endpoint de estadísticas
        self.test_endpoint(
            '/api/stack/statistics',
            'Test de Estadísticas',
            self.validate_statistics
        )

        # Probar endpoint de respuesta con mayor reputación
        self.test_endpoint(
            '/api/stack/highest-reputation',
            'Test de Mayor Reputación'
        )

        # Probar endpoint de respuesta menos vista
        self.test_endpoint(
            '/api/stack/least-viewed',
            'Test de Menos Vistas'
        )

        # Probar endpoint de timeline
        self.test_endpoint(
            '/api/stack/timeline',
            'Test de Timeline',
            self.validate_timeline
        )

        # Probar endpoint de analytics
        self.test_endpoint(
            '/api/stack/analytics',
            'Test de Analytics Completo'
        )

        # Mostrar resumen
        self.print_header("RESUMEN DE PRUEBAS")
        print(f"\nTotal de pruebas: {self.total_tests}")
        print(f"{Fore.GREEN}Pruebas exitosas: {self.success_count}{Style.RESET_ALL}")
        print(f"{Fore.RED}Pruebas fallidas: {self.fail_count}{Style.RESET_ALL}")
        success_rate = (self.success_count / self.total_tests) * 100 if self.total_tests > 0 else 0
        print(f"Tasa de éxito: {success_rate:.2f}%")

if __name__ == "__main__":
    tester = IntegrationTester()
    tester.run_all_tests()