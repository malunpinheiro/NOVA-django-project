from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Mistura, Perfume


class MisturaForm(forms.ModelForm):
    perfumes = forms.ModelMultipleChoiceField(
        queryset=Perfume.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Escolha de 2 a 3 perfumes",
    )

    class Meta:
        model = Mistura
        fields = ["nome", "descricao", "perfumes"]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex: Pôr do sol em Ipanema"}),
            "descricao": forms.TextInput(attrs={"class": "form-control", "placeholder": "Conte a história da sua mistura"}),
        }

    def clean_perfumes(self):
        perfumes = self.cleaned_data["perfumes"]
        if perfumes.count() < 2 or perfumes.count() > 3:
            raise forms.ValidationError("Escolha de 2 a 3 perfumes para criar sua mistura.")
        return perfumes


class CadastroForm(UserCreationForm):
    email = forms.EmailField(required=True, label="E-mail")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Já existe uma conta com este e-mail.")
        return email