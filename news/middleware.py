import logging
from .models import Visitor
from .services import get_client_ip, geolocate_ip

logger = logging.getLogger(__name__)


class GeoTrackingMiddleware:
    """
    Middleware для отслеживания посетителей.
    При каждом запросе:
    1. Извлекаем IP адрес
    2. Определяем геолокацию через внешний API
    3. Сохраняем запись в базу данных
    """

    # Пути, которые не нужно отслеживать
    EXCLUDED_PATHS = [
        '/admin/',
        '/static/',
        '/media/',
        '/visitors/api/',  # API для фронтенда не должен создавать рекурсию
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Пропускаем admin, static и api запросы
        if any(request.path.startswith(p) for p in self.EXCLUDED_PATHS):
            return self.get_response(request)

        # Обрабатываем только GET запросы (не POST forms и т.д.)
        if request.method == 'GET':
            self._track_visitor(request)

        return self.get_response(request)

    def _track_visitor(self, request):
        try:
            ip = get_client_ip(request)
            if not ip:
                return

            user_agent = request.META.get('HTTP_USER_AGENT', '')

            # Геолокация
            geo_data = geolocate_ip(ip)

            # Создаём запись посетителя
            visitor_data = {
                'ip_address': ip,
                'user_agent': user_agent,
            }

            if geo_data:
                visitor_data.update(geo_data)

            Visitor.objects.create(**visitor_data)

        except Exception as e:
            # Никогда не ломаем сайт из-за ошибки трекинга
            logger.error(f'GeoTrackingMiddleware error: {e}')
