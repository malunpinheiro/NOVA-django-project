from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("perfumes/", views.lista_perfumes, name="lista_perfumes"),

    path("misturas/", views.lista_misturas, name="lista_misturas"),
    path("misturas/nova/", views.criar_mistura, name="criar_mistura"),
    path("misturas/<int:pk>/", views.detalhe_mistura, name="detalhe_mistura"),
    path("misturas/<int:pk>/editar/", views.editar_mistura, name="editar_mistura"),
    path("misturas/<int:pk>/excluir/", views.excluir_mistura, name="excluir_mistura"),
]