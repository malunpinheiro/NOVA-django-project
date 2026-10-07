from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("perfumes/", views.lista_perfumes, name="lista_perfumes"),
    path("perfumes/<int:pk>/", views.detalhe_perfume, name="detalhe_perfume"),
    path("misturas/", views.lista_misturas, name="lista_misturas"),
    path("misturas/nova/", views.criar_mistura, name="criar_mistura"),
    path("misturas/<int:pk>/", views.detalhe_mistura, name="detalhe_mistura"),
    path("misturas/<int:pk>/editar/", views.editar_mistura, name="editar_mistura"),
    path("misturas/<int:pk>/excluir/", views.excluir_mistura, name="excluir_mistura"),
    path("carrinho/", views.ver_carrinho, name="ver_carrinho"),
    path("carrinho/adicionar/<int:pk>/", views.adicionar_carrinho, name="adicionar_carrinho"),
    path("carrinho/diminuir/<int:pk>/", views.diminuir_carrinho, name="diminuir_carrinho"),
    path("carrinho/remover/<int:pk>/", views.remover_carrinho, name="remover_carrinho"),
    path("cadastro/", views.cadastro, name="cadastro"),
]