import urllib.request
import json
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


def get_client_ip(request):
    """Извлекаем реальный IP адрес клиента из заголовков"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def is_private_ip(ip):
    """Проверяем, является ли IP адрес приватным (localhost и т.д.)"""
    private_ranges = [
        '127.0.0.0/8',
        '10.0.0.0/8',
        '172.16.0.0/12',
        '192.168.0.0/16',
        '::1',
        'fd00::/8',
    ]
    import ipaddress
    try:
        addr = ipaddress.ip_address(ip)
        return addr.is_private or addr.is_loopback or addr.is_reserved
    except ValueError:
        return True


def geolocate_ip_api(ip):
    """
    Геолокация через ip-api.com
    - Бесплатно, без ключа API
    - Лимит: 45 запросов/минуту для бесплатного тира
    - Возвращает: город, регион, страна, координаты
    """
    url = f'http://ip-api.com/json/{ip}?fields=status,city,regionName,country,countryCode,lat,lon,message'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
            if data.get('status') == 'success':
                return {
                    'city': data.get('city', ''),
                    'region': data.get('regionName', ''),
                    'country': data.get('country', ''),
                    'country_code': data.get('countryCode', ''),
                    'latitude': data.get('lat'),
                    'longitude': data.get('lon'),
                }
            else:
                logger.warning(f'ip-api.com failed for {ip}: {data.get("message", "unknown error")}')
                return None
    except Exception as e:
        logger.error(f'ip-api.com request failed for {ip}: {e}')
        return None


def geolocate_ipstack(ip):
    """
    Геолокация через ipstack.com (резервный вариант)
    - Бесплатный план: 1000 запросов/месяц
    - Требует API ключ (GEOIP_API_KEY в settings)
    - Более детализированные данные
    """
    api_key = settings.GEOIP_API_KEY
    if not api_key:
        logger.warning('ipstack API key is not configured')
        return None

    url = f'http://api.ipstack.com/{ip}?access_key={api_key}'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
            if 'error' not in data:
                return {
                    'city': data.get('city', '') or '',
                    'region': data.get('region_name', '') or '',
                    'country': data.get('country_name', '') or '',
                    'country_code': data.get('country_code', '') or '',
                    'latitude': data.get('latitude'),
                    'longitude': data.get('longitude'),
                }
            else:
                logger.warning(f'ipstack failed for {ip}: {data["error"]}')
                return None
    except Exception as e:
        logger.error(f'ipstack request failed for {ip}: {e}')
        return None


def geolocate_ip(ip):
    """
    Основной метод геолокации.
    Пробует провайдер из настроек, затем резервный.

    Доступные провайдеры:
    1. ip-api.com      — бесплатно, без ключа, 45 запросов/мин
    2. ipstack.com     — бесплатный план 1000 запросов/мес, нужен ключ
    3. ipgeolocation.io— бесплатный план 1000 запросов/мес, нужен ключ
    """
    if is_private_ip(ip):
        logger.info(f'Skipping geolocation for private IP: {ip}')
        return None

    provider = getattr(settings, 'GEO_API_PROVIDER', 'ip-api')

    providers = {
        'ip-api': geolocate_ip_api,
        'ipstack': geolocate_ipstack,
    }

    # Пробуем основной провайдер
    primary = providers.get(provider, geolocate_ip_api)
    result = primary(ip)
    if result:
        return result

    # Если не удалось — пробуем резервный
    for name, func in providers.items():
        if name != provider:
            result = func(ip)
            if result:
                return result

    return None
