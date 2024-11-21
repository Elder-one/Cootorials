from django.db import models
from user_auth.models import UserExtended

# Create your models here.


class RecipeCategory(models.Model):
    name = models.CharField(max_length=30, null=False, unique=True)


class Recipe(models.Model):
    author = models.ForeignKey(UserExtended, on_delete=models.CASCADE, related_name='recipies')
    title = models.CharField(max_length=150, null=False)
    category = models.ForeignKey(RecipeCategory, related_name='recipies', on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to="/home/Elder9one/Cootorials/images/", null=False)
    short_description = models.CharField(max_length=250, null=False)
    tutorial = models.TextField(null=False, default='')
    uploaded_on = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(UserExtended, related_name='liked_recipies')
    likes_count = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'{self.author} {self.title}'
