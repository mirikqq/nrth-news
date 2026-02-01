import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Count
from .models import News, Visitor


def news_list(request):
    """Главная страница — список всех новостей"""
    news = News.objects.all().order_by('-pub_date')
    return render(request, 'news/news_list.html', {'news_list': news})


def news_detail(request, pk):
    """Страница отдельной новости"""
    news = get_object_or_404(News, pk=pk)
    return render(request, 'news/news_detail.html', {'news': news})


def visitors_map(request):
    """Страница карты посетителей"""
    # Общее количество визитов
    total_visits = Visitor.objects.count()

    # Уникальные посетители по IP
    unique_visitors = Visitor.objects.values('ip_address').distinct().count()

    # Статистика по странам
    country_stats = (
        Visitor.objects
        .exclude(country='')
        .values('country')
        .annotate(count=Count('id'))
        .order_by('-count')[:10]
    )

    return render(request, 'news/visitors_map.html', {
        'total_visits': total_visits,
        'unique_visitors': unique_visitors,
        'country_stats': country_stats,
    })


def visitors_api(request):
    """JSON API — возвращает список посетителей для карты"""
    visitors = (
        Visitor.objects
        .exclude(latitude__isnull=True)
        .exclude(longitude__isnull=True)
        .values('ip_address', 'city', 'region', 'country', 'latitude', 'longitude', 'visited_at')
        .order_by('-visited_at')[:500]  # Последние 500 для производительности
    )

    data = []
    for v in visitors:
        data.append({
            'ip': v['ip_address'],
            'city': v['city'],
            'region': v['region'],
            'country': v['country'],
            'lat': v['latitude'],
            'lon': v['longitude'],
            'visited_at': v['visited_at'].strftime('%d.%m.%Y %H:%M'),
        })

    return JsonResponse({'visitors': data, 'count': len(data)})
