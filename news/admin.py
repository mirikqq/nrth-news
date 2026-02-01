from django.contrib import admin
from .models import News, Visitor


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'pub_date', 'created_at', 'has_photo']
    list_filter = ['pub_date', 'created_at']
    search_fields = ['title', 'short_description']
    ordering = ['-pub_date']
    date_hierarchy = 'pub_date'

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'photo')
        }),
        ('Описание', {
            'fields': ('short_description', 'full_description')
        }),
        ('Публикация', {
            'fields': ('pub_date',)
        }),
    )

    def has_photo(self, obj):
        return bool(obj.photo)
    has_photo.boolean = True
    has_photo.short_description = 'Есть фото'


@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ['ip_address', 'city', 'region', 'country', 'latitude', 'longitude', 'visited_at']
    list_filter = ['country', 'visited_at']
    search_fields = ['ip_address', 'city', 'country']
    ordering = ['-visited_at']
    readonly_fields = ['ip_address', 'city', 'region', 'country', 'country_code',
                       'latitude', 'longitude', 'visited_at', 'user_agent']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
