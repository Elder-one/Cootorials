import logging

from django.shortcuts import render, redirect
from .models import Recipe, RecipeCategory
from .forms import NewRecipeForm
from django.contrib.auth.models import User
import random as rnd


# Create your views here.
logger = logging.getLogger('django')


def main_page(request, category='None'):
    categ_names = [cat.name for cat in RecipeCategory.objects.all()]

    if request.user.is_authenticated:
        liked_recipies = request.user.extended_user.liked_recipies.all()
    else:
        liked_recipies = []

    if category != 'None' and (category not in categ_names):
        logger.info('category is does not match, page not found')
        return render(request, '404.html')
    if category == 'None':
        logger.debug('random-5 recipies selection ...')
        count = Recipe.objects.all().count()
        r_ids = [i for i in range(count)]
        if count >= 5:
            r_ids = rnd.sample(range(count), 5)

        recipies = [Recipe.objects.all()[i] for i in r_ids]
        logger.debug('random-5 recipies selection finished')
    else:
        logger.debug('choosing recipies from selected category')
        recipies = Recipe.objects.filter(category__name=category).all()

    logger.debug('recipies have been chosen')

    if request.method == 'POST':
        logger.info('process POST-request ...')
        if 'like-button' in request.POST:
            logger.debug('like-button has been triggered')
            pk, category = request.POST['like-button'].split(',')
            pk = int(pk)
            selected = Recipe.objects.filter(pk=pk).first()
            selected.likes.add(request.user.extended_user)
            selected.likes_count += 1
            selected.save()
            logger.debug(f'request user has been added to {pk} Recipe likes')
            logger.info('redirecting to home page')
            return redirect('home-page', category)

        if 'unlike-button' in request.POST:
            logger.debug('unlike-button has been triggered')
            pk, category = request.POST['unlike-button'].split(',')
            pk = int(pk)
            selected = Recipe.objects.filter(pk=pk).first()
            selected.likes.remove(request.user.extended_user)
            if selected.likes_count > 0:
                selected.likes_count -= 1
            selected.save()
            logger.debug(f'request user has been removed from {pk} Recipe likes')
            logger.info('redirecting to home page')
            return redirect('home-page', category)

        for name in categ_names:
            if name in request.POST:
                logger.debug('category button has been triggered')
                logger.debug('redirecting to selected category')
                return redirect('home-page', name)

    else:
        context = {
            'liked_recipies': liked_recipies,
            'recipies': recipies,
            'categ_names': categ_names,
            'category': category,
        }
        logger.debug('context for page is completed. rendering homepage ...')
        return render(request, 'main_app/home_page.html', context=context)


def profile_page(request, uid):

    if request.method == 'POST':
        logger.info('process POST request ...')

        if 'like-button' in request.POST:
            logger.debug('like-button has been triggered')
            pk = int(request.POST['like-button'])
            selected = Recipe.objects.filter(pk=pk).first()
            selected.likes.add(request.user.extended_user)
            selected.likes_count += 1
            selected.save()
            logger.debug(f'request user has been added to {pk} Recipe likes')
            logger.info('redirecting to profile page')
            return redirect('profile-page', uid)

        if 'unlike-button' in request.POST:
            logger.debug('unlike-button has been triggered')
            pk = int(request.POST['unlike-button'])
            selected = Recipe.objects.filter(pk=pk).first()
            selected.likes.remove(request.user.extended_user)
            if selected.likes_count > 0:
                selected.likes_count -= 1
            selected.save()
            logger.debug(f'request user has been deleted from {pk} Recipe likes')
            logger.info('redirecting to profile page')
            return redirect('profile-page', uid)

        if 'own-recipies' in request.POST:
            logger.debug('own recipies filter selected')
            liked_recipies = request.user.extended_user.liked_recipies.all()
            recipies = Recipe.objects.filter(author_id=uid)
            context = {
                'liked_recipies': liked_recipies,
                'recipies': recipies,
                'liked': False,
            }
            logger.debug('context for own page is completed. rendering ...')
            return render(request, 'main_app/own_profile.html', context=context)

        if 'liked-recipies' in request.POST:
            logger.debug('liked recipies filter has been selected')
            liked_recipies = request.user.extended_user.liked_recipies.all()
            context = {
                'liked_recipies': liked_recipies,
                'recipies': liked_recipies,
                'liked': True,
            }
            logger.debug('context for own page is completed. rendering ...')
            return render(request, 'main_app/own_profile.html', context=context)

    else:

        try:
            test = User.objects.get(pk=uid)
        except User.DoesNotExist:
            logger.info('invalid uid. page not found')
            return render(request, '404.html')
        del test

        if request.user.is_authenticated:
            liked_recipies = request.user.extended_user.liked_recipies.all()
        else:
            liked_recipies = []

        if request.user.is_authenticated and request.user.id == uid:
            logger.debug('request user is selected one')
            recipies = Recipe.objects.filter(author_id=uid)
            context = {
                'liked_recipies': liked_recipies,
                'recipies': recipies,
                'liked': False,
            }
            logger.debug('context for own page is complete. rendering ...')
            return render(request, 'main_app/own_profile.html', context=context)
        else:
            logger.debug('selected user is not the request one')
            selected_user = User.objects.filter(pk=uid).first()
            recipies = Recipe.objects.filter(author_id=uid)
            context = {
                'liked_recipies': liked_recipies,
                'selected_user': selected_user,
                'recipies': recipies,
            }
            logger.debug('context for other user page is complete. rendering ...')
            return render(request, 'main_app/other_profile.html', context=context)


def new_recipe(request):
    if request.method == "POST":
        logger.info('processing POST request ...')
        form = NewRecipeForm(request.POST, request.FILES)
        if form.is_valid():
            logger.debug('form is valid. processing info ...')
            title = form.cleaned_data.get('title')
            description = form.cleaned_data.get('description')
            tutorial = form.cleaned_data.get('tutorial')
            image = form.cleaned_data.get('image')
            category = form.cleaned_data.get('category')

            category = RecipeCategory.objects.filter(name=category).first()

            recipe = Recipe.objects.create(title=title,
                                           short_description=description,
                                           tutorial=tutorial,
                                           image=image,
                                           author=request.user.extended_user,
                                           category=category)
            recipe.save()
            logger.debug('new recipe is in the DB. redirecting to profile page ...')
            return redirect('profile-page', request.user.id)

        else:
            logger.debug('form is not valid. rendering form-page with warnings ...')
            return render(request,
                          'main_app/new_recipe.html',
                          {'form': form,
                           })
    else:
        logger.info('GET request processing ...')
        if request.user.is_authenticated:
            logger.debug('User is authenticated. rendering form-page ...')
            return render(request,
                          'main_app/new_recipe.html',
                          {'form': NewRecipeForm(),
                           })
        else:
            logger.debug('User is NOT authenticated. rendering warning page ...')
            return render(request,
                          'main_app/not_logged_in.html')


def full_recipe(request, rid):

    if request.method == 'POST':
        logger.info('processing POST request ...')
        if 'like-button' in request.POST:
            logger.debug('like-button has been triggered')
            pk = int(request.POST['like-button'])
            selected = Recipe.objects.filter(pk=pk).first()
            selected.likes.add(request.user.extended_user)
            selected.likes_count += 1
            selected.save()
            logger.debug(f'request user has been added to {pk} Recipe likes')
            logger.info('redirecting to full recipe page')
            return redirect('full-recipe', rid)

        if 'unlike-button' in request.POST:
            logger.debug('unlike-button has been triggered')
            pk = int(request.POST['unlike-button'])
            selected = Recipe.objects.filter(pk=pk).first()
            selected.likes.remove(request.user.extended_user)
            if selected.likes_count > 0:
                selected.likes_count -= 1
            selected.save()
            logger.debug(f'request user has been deleted from {pk} Recipe likes')
            logger.info('redirecting to full recipe page')
            return redirect('full-recipe', rid)

        if 'edit' in request.POST:
            logger.info('edit button has been triggered. redirecting to editing page ...')
            return redirect('edit-recipe', rid)

        if 'delete' in request.POST:
            logger.info('delete button has been triggered. redirecting to deleting page ...')
            return redirect('delete-recipe', rid)

    else:
        logger.info('GET request processing ...')
        try:
            recipe = Recipe.objects.get(pk=rid)
        except Recipe.DoesNotExist:
            logger.info('rid is invalid. page not found')
            return render(request, '404.html')

        own = False

        if request.user.is_authenticated and recipe in request.user.extended_user.recipies.all():
            own = True

        if request.user.is_authenticated:
            liked_recipies = request.user.extended_user.liked_recipies.all()
        else:
            liked_recipies = []

        context = {
            'liked_recipies': liked_recipies,
            'rid': rid,
            'recipe': recipe,
            'own': own,
        }
        logger.debug('context for full recipe page is complete. rendering ...')
        return render(request, 'main_app/full_recipe.html', context=context)


def edit_recipe(request, rid):

    if request.method == "POST":
        logger.info('POST request processing ...')
        form = NewRecipeForm(request.POST, request.FILES)

        if form.is_valid():
            logger.debug('form is valid. processing info ...')
            title = form.cleaned_data.get('title')
            description = form.cleaned_data.get('description')
            tutorial = form.cleaned_data.get('tutorial')
            image = form.cleaned_data.get('image')
            category = form.cleaned_data.get('category')

            category = RecipeCategory.objects.filter(name=category).first()

            recipe = Recipe.objects.filter(pk=rid).first()
            recipe.title = title
            recipe.short_description = description
            recipe.tutorial = tutorial
            recipe.image = image
            recipe.category = category
            recipe.save()
            logger.debug('recipe has been updated. redirecting to own profile page ...')
            return redirect('profile-page', request.user.id)

    else:
        logger.info('GET request processing ...')
        if not request.user.is_authenticated:
            logger.debug('request user is not authenticated. rendering warning page ...')
            return render(request, 'main_app/not_logged_in.html')

        try:
            recipe = Recipe.objects.get(pk=rid)
        except Recipe.DoesNotExist:
            logger.debug('recipe does not exist. page not found')
            return render(request, '404.html')

        if recipe not in request.user.extended_user.recipies.all():
            logger.debug('recipe does not belong to request user. access denied')
            return render(request, 'main_app/access_denied.html')

        form = NewRecipeForm({'title': recipe.title,
                              'description': recipe.short_description,
                              'tutorial': recipe.tutorial,
                              'image': recipe.image,
                              'category': recipe.category.name,
                              })
        logger.info('context for editing page is complete. rendering ...')
        return render(request, 'main_app/edit_recipe.html',
                      context={
                          'form': form,
                      })


def delete_recipe(request, rid):
    if request.method == 'POST':
        logger.info('POST request processing ...')
        if 'delete-recipe' in request.POST:
            logger.debug('deletion button has been triggered')
            recipe = Recipe.objects.filter(pk=rid).first()
            recipe.delete()
            logger.debug(f'Recipe[rid={rid}] has been deleted from DB')
            logger.info('redirecting to own profile page ...')
            return redirect('profile-page', request.user.id)

    else:
        logger.info('GET request processing ...')
        if not request.user.is_authenticated:
            logger.debug('request user is not authenticated. rendering warning page ...')
            return render(request, 'main_app/not_logged_in.html')

        try:
            recipe = Recipe.objects.get(pk=rid)
        except Recipe.DoesNotExist:
            logger.debug('recipe does not exist. page not found')
            return render(request, '404.html')

        if recipe not in request.user.extended_user.recipies.all():
            logger.debug('recipe does not belong to request user. access denied')
            return render(request, 'main_app/access_denied.html')
        logger.info('rendering deletion page ...')
        return render(request, 'main_app/delete_confirm.html',
                      {'rid': rid,
                       })
