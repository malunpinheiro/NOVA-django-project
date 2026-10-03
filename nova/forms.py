from django import forms
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