
from django.urls import path, include
from .views import main_page, profile_page, new_recipe, full_recipe, edit_recipe, delete_recipe

urlpatterns = [
    path('home-page/', main_page, name='home-page'),
    path('home-page/<str:category>/', main_page, name='home-page'),
    path('profile-page/<int:uid>/', profile_page, name='profile-page'),
    path('new-recipe/', new_recipe, name='add-recipe'),
    path('full-recipe/<int:rid>/', full_recipe, name='full-recipe'),
    path('edit-recipe/<int:rid>/', edit_recipe, name='edit-recipe'),
    path('delete-recipe/<int:rid>/', delete_recipe, name='delete-recipe'),
]