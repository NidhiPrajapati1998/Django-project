from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': ''}))
    middle_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': ''}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': ''}))
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': ''}))
    pine_code = models.IntegerField()
    gender = forms.ChoiceField(choices=[('Female', 'Female'), ('Male', 'Male')])

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ("first_name", "middle_name", "last_name", "address", "pine_code", "gender", "mobile_no", "email",)


class CustomUserChangeForm(UserChangeForm):
    first_name = forms.CharField()
    middle_name = forms.CharField()
    last_name = forms.CharField()
    address = forms.CharField()
    pine_code = models.IntegerField()
    gender = forms.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female')])

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ("first_name", "middle_name", "last_name", "address", "pine_code", "gender", "mobile_no",)


class ContactForm(forms.ModelForm):
    full_name = forms.CharField(max_length=50, min_length=4,
                                widget=forms.TextInput(attrs={"placeholder": "First Name  Last Name"}))

    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Your Email"}))
    message = forms.CharField(max_length=150, min_length=4,
                              widget=forms.Textarea(attrs={"placeholder": "Your Message"}))

    class Meta:
        model = Contact
        fields = ("full_name", "email", "message", )


class FeedbackForm(forms.ModelForm):
    full_name = forms.CharField(max_length=50, min_length=4,
                                widget=forms.TextInput(attrs={"placeholder": "Enter Your Name"}))
    message = forms.CharField(max_length=150, min_length=4,
                              widget=forms.Textarea(attrs={"placeholder": "Your Feedback"}))

    class Meta:
        model = Feedback
        fields = ("full_name", "message", )