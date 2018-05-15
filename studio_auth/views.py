from django.contrib.auth import authenticate, login, logout
from django import forms
from django.core.validators import MinValueValidator
from django.shortcuts import render, redirect, HttpResponse

from shop.models import Order
from studio_auth.models import User
from django.db.utils import IntegrityError


def login_on_website(request):
    if request.method == 'GET':
        return render(request, 'studio_auth/login.html')
    else:
        user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            if user.is_staff or user.is_superuser:
                return redirect('/admin')
            else:
                return redirect('shop:index')
        else:
            return redirect('studio_auth.login')


validate_size = MinValueValidator(0, message='Should be greater than zero')


class SignupForm(forms.ModelForm):
    password = forms.CharField(min_length=6, widget=forms.PasswordInput(), validators=[])
    repeat_password = forms.CharField(min_length=6, widget=forms.PasswordInput())

    # def clean_lenght_of_arms(self):
    #     validate_size(self.cleaned_data['lenght_of_arms'])

    def clean(self):
        cleaned_data = super(SignupForm, self).clean()
        if cleaned_data.get('password') != cleaned_data.get('repeat_password'):
            raise forms.ValidationError('Password does not match')

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'length_of_arms',
                  'length_of_legs', 'length_of_waist_girth', 'length_of_head')


def signup(request):
    if request.method == "GET":
        return render(request, 'studio_auth/signup.html', {'form': SignupForm()})
    else:
        form = SignupForm(request.POST)
        if form.is_valid():
            try:
                data = form.cleaned_data
                user = User.objects.create_user(username=data['username'], password=data['password'],
                                                length_of_arms=data['length_of_arms'],
                                                lenghth_of_legs=data['length_of_legs'],
                                                length_of_waist_girth=data['length_of_waist_girth'],
                                                length_of_head=data['length_of_head']

                                                )
                user.save()
                return redirect('studio_auth.login')
            except IntegrityError:
                return HttpResponse('Error')
        else:
            return render(request, 'studio_auth/signup.html', {'form': form})


def signout(request):
    logout(request)
    return redirect('studio_auth.login')
