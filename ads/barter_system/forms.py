# from django import forms

# from .models import ExchangeProposal
# from .models import Ad
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User


# class SignUpForm(UserCreationForm):
#     email = forms.EmailField(
#         required=True,
#         help_text="Обязательное поле.",
#     )

#     class Meta:
#         model = User
#         fields = (
#             "username",
#             "email",
#             "password1",
#             "password2",
#         )


# class AdForm(forms.ModelForm):
#     class Meta:
#         model = Ad
#         fields = [
#             "title",
#             "description",
#             "image_url",
#             "Category",
#             "Condition",
#         ]


# class ExchangeProposalForm(forms.ModelForm):
#     class Meta:
#         model = ExchangeProposal
#         fields = [
#             "ad_sender",
#             "ad_receiver",
#             "comment",
#             "status",
#         ]
