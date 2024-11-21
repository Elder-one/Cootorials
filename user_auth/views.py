from django.shortcuts import render, HttpResponse, redirect
from .forms import UserSignUp
from .models import UserExtended
from django.contrib.auth.models import User


# Create your views here.


def sign_up(request):
    if request.method == 'POST':
        form = UserSignUp(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            f_name = form.cleaned_data.get('f_name')
            s_name = form.cleaned_data.get('s_name')

            user_total = User.objects.count()
            User.objects.create_user(username=f'User{user_total + 1}',
                                     password=password,
                                     email=email,
                                     first_name=f_name,
                                     last_name=s_name)
            user = User.objects.filter(email=email).first()
            user_ext = UserExtended(base_user=user)
            user_ext.save()

            return render(request,
                          'user_auth/sign_up_complete.html')
        else:
            return render(request,
                          'user_auth/sign_up.html',
                          {'form': form})

    else:
        form = UserSignUp()
        return render(request,
                      'user_auth/sign_up.html',
                      {'form': form})
