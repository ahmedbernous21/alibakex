from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['LinkFb', 'phone', 'name', 'Card']
        exclude = ['user']


class OfferForm(ModelForm):
    class Meta:
        model = offers
        fields = ['price', 'devise', 'lowest', 'payment', 'status', 'description', 'quantity']


class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

        customer, created = Customer.objects.get_or_create(user=user, defaults={'email': user.email})

        if not created:
            # If a Customer object already exists for this user, update its email field
            customer.email = user.email
            customer.save()

        return user

class CaptureFaceForm(forms.Form):
    face_picture = forms.ImageField(widget=forms.HiddenInput())
