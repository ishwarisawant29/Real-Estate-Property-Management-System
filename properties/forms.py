from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Property, PropertyImage
from .models import Inquiry, Visit, Review


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={'placeholder': 'Choose a username'})
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'placeholder': 'you@example.com'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = 'Password'
        self.fields['password2'].label = 'Confirm password'
        self.fields['password1'].help_text = 'Use at least 8 characters.'
        self.fields['password2'].help_text = ''
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')


class InquiryForm(forms.ModelForm):

    class Meta:
        model = Inquiry
        fields = ['message']

        widgets = {
            'message': forms.Textarea(
                attrs={
                    'rows': 5,
                    'placeholder': 'Enter your inquiry...'
                }
            )
        }


class VisitForm(forms.ModelForm):

    class Meta:
        model = Visit
        fields = ['visit_date']

        widgets = {
            'visit_date': forms.DateInput(
                attrs={
                    'type': 'date'
                }
            )
        }


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = [
            'rating',
            'comment'
        ]

        widgets = {
            'rating': forms.NumberInput(
                attrs={
                    'min': 1,
                    'max': 5
                }
            ),
            'comment': forms.Textarea(
                attrs={
                    'rows': 4
                }
            )
        }



class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'title',
            'description',
            'price',
            'area',
            'address',
            'city',
            'category',
            'status',
        ]


class PropertyImageForm(forms.ModelForm):
    class Meta:
        model = PropertyImage
        fields = ['image']