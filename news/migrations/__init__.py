from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='news_photos/', verbose_name='Фотография')),
                ('title', models.CharField(max_length=250, verbose_name='Название новости')),
                ('short_description', models.TextField(verbose_name='Краткое описание')),
                ('full_description', models.TextField(verbose_name='Полное описание')),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата публикации')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Новость',
                'verbose_name_plural': 'Новости',
                'ordering': ['-pub_date'],
            },
        ),
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField(verbose_name='IP адрес')),
                ('city', models.CharField(blank=True, default='', max_length=100, verbose_name='Город')),
                ('region', models.CharField(blank=True, default='', max_length=100, verbose_name='Регион')),
                ('country', models.CharField(blank=True, default='', max_length=100, verbose_name='Страна')),
                ('country_code', models.CharField(blank=True, default='', max_length=10, verbose_name='Код страны')),
                ('latitude', models.FloatField(blank=True, null=True, verbose_name='Широта')),
                ('longitude', models.FloatField(blank=True, null=True, verbose_name='Долгота')),
                ('visited_at', models.DateTimeField(auto_now_add=True, verbose_name='Время визита')),
                ('user_agent', models.TextField(blank=True, default='', verbose_name='User Agent')),
            ],
            options={
                'verbose_name': 'Посетитель',
                'verbose_name_plural': 'Посетители',
                'ordering': ['-visited_at'],
            },
        ),
    ]
