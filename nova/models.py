import unicodedata
from django.db import models
from django.contrib.auth.models import User


class Perfume(models.Model):
    FAMILIAS = [
        ("FRU", "Frutal"),
        ("FLO", "Floral"),
        ("GOU", "Gourmand"),
        ("CIT", "Cítrica"),
        ("AQU", "Aquática"),
        ("SOL", "Solar"),
    ]

    nome = models.CharField(max_length=120)
    descricao = models.CharField(max_length=300)
    notas = models.CharField(max_length=200, help_text="Ex: coco, maracujá, baunilha")
    familia = models.CharField(max_length=3, choices=FAMILIAS, default="FRU")
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    imagem_url = models.URLField(blank=True)
    destaque = models.BooleanField(default=False, help_text="Aparece na Home")

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Mistura(models.Model):
    nome = models.CharField(max_length=120)
    descricao = models.CharField(max_length=300, blank=True)
    perfumes = models.ManyToManyField(Perfume, related_name="misturas")
    criador = models.ForeignKey(User, on_delete=models.CASCADE, related_name="misturas")
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-criado_em"]
        verbose_name_plural = "misturas"

    def __str__(self):
        return f"{self.nome} ({self.criador.username})"