"""Конфигурация приложения foodgram_api проекта foodgram."""

from django.apps import AppConfig


class FoodgramApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'foodgram_api'
