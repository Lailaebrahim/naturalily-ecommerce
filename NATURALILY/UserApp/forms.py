from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from .models import ShopUser
from re import match
from django.core.exceptions import ValidationError
import re


class SignUpForm(UserCreationForm):
    image = forms.ImageField(required=False)
    phone = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username',
                  'email', 'image',  'phone', 'password1', 'password2']

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone.isnumeric():
            raise forms.ValidationError('Phone number must be numeric')
        elif not match(r'^01[0-9]', phone):
            raise forms.ValidationError(
                'Egyptian Phone Number are only allowed')
        return phone

    def save(self):
        user = super(SignUpForm, self).save()
        if self.cleaned_data.get('image'):
            image = self.cleaned_data['image']
        else:
            image = ShopUser._meta.get_field('img').get_default()
            
        shopUser = ShopUser.objects.create(
            user=user, img=image, phone=self.cleaned_data['phone'])
        return user


class UpdateForm(UserChangeForm):
    image = forms.ImageField(required=False, widget=forms.FileInput)
    phone = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'username', 'email', 'image', 'phone']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, 'shopUser'):
            self.fields['phone'].initial = self.instance.shopUser.phone

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone:
            if not phone.isnumeric():
                raise ValidationError('Phone number must be numeric')
            elif not re.match(r'^01[0-9]', phone):
                raise ValidationError('Egyptian Phone Number are only allowed')
        return phone

    def save(self, commit=True):
        user = super().save(commit=False)
        shopuser, created = ShopUser.objects.get_or_create(user=user)

        if self.cleaned_data.get('phone'):
            shopuser.phone = self.cleaned_data['phone']

        if self.cleaned_data.get('image'):
            shopuser.img = self.cleaned_data['image']

        if commit:
            user.save()
            shopuser.save()

        return user
