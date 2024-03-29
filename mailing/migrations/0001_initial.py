# Generated by Django 4.2 on 2024-03-01 14:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='контактный email')),
                ('full_name', models.CharField(max_length=100, verbose_name='ФИО')),
                ('comment', models.CharField(max_length=300, verbose_name='комментарий')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='владелец')),
            ],
            options={
                'verbose_name': 'Клиент сервиса',
                'verbose_name_plural': 'Клиенты сервиса',
            },
        ),
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateField(blank=True, null=True, verbose_name='начало рассылки')),
                ('end_time', models.DateField(blank=True, null=True, verbose_name='конец рассылки')),
                ('period', models.CharField(blank=True, choices=[('daily', 'Ежедневная'), ('weekly', 'Раз в неделю'), ('monthly', 'Раз в месяц')], max_length=20, null=True, verbose_name='периодичность')),
                ('status', models.CharField(choices=[('created', 'Создана'), ('started', 'Запущена'), ('done', 'Завершена')], max_length=20, verbose_name='статус рассылки')),
                ('title_message', models.CharField(max_length=100, verbose_name='тема письма')),
                ('body_message', models.TextField(blank=True, null=True, verbose_name='тело письма')),
                ('last_run', models.DateField(blank=True, null=True, verbose_name='дата последней отправки рассылки')),
                ('client', models.ManyToManyField(to='mailing.client', verbose_name='клиент')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='владелец')),
            ],
            options={
                'verbose_name': 'Рассылка (настройки)',
                'verbose_name_plural': 'Рассылки (настройки)',
            },
        ),
        migrations.CreateModel(
            name='Logs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_of_last_attempt', models.DateTimeField(verbose_name='дата и время последней попытки')),
                ('status', models.CharField(choices=[('ok', 'Успешно'), ('failed', 'Ошибка')], max_length=20, verbose_name='статус попытки')),
                ('error_msg', models.TextField(blank=True, null=True, verbose_name='error msg')),
                ('mailing', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mailing.mailing', verbose_name='рассылка')),
            ],
            options={
                'verbose_name': 'Лог рассылки',
                'verbose_name_plural': 'Логи рассылки',
            },
        ),
    ]
