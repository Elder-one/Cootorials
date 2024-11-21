from django.core.management.base import BaseCommand
from main_app.models import RecipeCategory


class Command(BaseCommand):
    def handle(self, *args, **options):
        list_ = ['Первые блюда', 'Вторые блюда', 'Напитки', 'Десерты']
        for el in list_:
            obj_ = RecipeCategory(name=el)
            obj_.save()
            