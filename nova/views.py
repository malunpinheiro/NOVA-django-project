from django.contrib.auth import login
from .forms import CadastroForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from decimal import Decimal
from django.views.decorators.http import require_POST
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import MisturaForm
from .models import Perfume, Mistura


def home(request):
    destaques = Perfume.objects.filter(destaque=True)[:4]
    return render(request, "home.html", {"destaques": destaques})


def lista_perfumes(request):
    perfumes = Perfume.objects.all()

    familia = request.GET.get("familia", "")
    if familia:
        perfumes = perfumes.filter(familia=familia)

    context = {
        "perfumes": perfumes,
        "familias": Perfume.FAMILIAS,
        "familia_ativa": familia,
    }
    return render(request, "lista_perfumes.html", context)


# ---------- LABORATÓRIO (CRUD de Mistura) ----------

def lista_misturas(request):  # READ (lista)
    misturas = Mistura.objects.select_related("criador").prefetch_related("perfumes")
    return render(request, "lista_misturas.html", {"misturas": misturas})


def detalhe_mistura(request, pk):  # READ (detalhe)
    mistura = get_object_or_404(Mistura, pk=pk)
    return render(request, "detalhe_mistura.html", {"mistura": mistura})


@login_required
def criar_mistura(request):  # CREATE
    if request.method == "POST":
        form = MisturaForm(request.POST)
        if form.is_valid():
            mistura = form.save(commit=False)
            mistura.criador = request.user
            mistura.save()
            form.save_m2m()  # salva os perfumes escolhidos
            messages.success(request, "Mistura criada com sucesso!")
            return redirect("detalhe_mistura", pk=mistura.pk)
    else:
        form = MisturaForm()
    return render(request, "form_mistura.html", {"form": form, "titulo": "Criar minha mistura"})


@login_required
def editar_mistura(request, pk):  # UPDATE
    mistura = get_object_or_404(Mistura, pk=pk, criador=request.user)
    if request.method == "POST":
        form = MisturaForm(request.POST, instance=mistura)
        if form.is_valid():
            form.save()
            messages.success(request, "Mistura atualizada!")
            return redirect("detalhe_mistura", pk=mistura.pk)
    else:
        form = MisturaForm(instance=mistura)
    return render(request, "form_mistura.html", {"form": form, "titulo": "Editar mistura"})


@login_required
def excluir_mistura(request, pk):  # DELETE
    mistura = get_object_or_404(Mistura, pk=pk, criador=request.user)
    if request.method == "POST":
        mistura.delete()
        messages.success(request, "Mistura excluída.")
        return redirect("lista_misturas")
    return render(request, "confirmar_exclusao.html", {"mistura": mistura})

def detalhe_perfume(request, pk):
    perfume = get_object_or_404(Perfume, pk=pk)
    return render(request, "detalhe_perfume.html", {"perfume": perfume})

# ---------- CARRINHO ----------

def _voltar(request, padrao="ver_carrinho"):
    destino = request.POST.get("next", "")
    if destino and url_has_allowed_host_and_scheme(destino, allowed_hosts={request.get_host()}):
        return redirect(destino)
    return redirect(padrao)


def ver_carrinho(request):
    dados = request.session.get("carrinho", {})
    itens = []
    total = Decimal("0")
    for perfume in Perfume.objects.filter(pk__in=dados.keys()):
        quantidade = dados[str(perfume.pk)]
        subtotal = perfume.preco * quantidade
        total += subtotal
        itens.append({"perfume": perfume, "quantidade": quantidade, "subtotal": subtotal})
    return render(request, "carrinho.html", {"itens": itens, "total": total})


@require_POST
def adicionar_carrinho(request, pk):
    perfume = get_object_or_404(Perfume, pk=pk)
    carrinho = request.session.get("carrinho", {})
    atual = carrinho.get(str(pk), 0)
    if atual + 1 > perfume.estoque:
        messages.warning(request, f"Só temos {perfume.estoque} unidade(s) de {perfume.nome}.")
    else:
        carrinho[str(pk)] = atual + 1
        request.session["carrinho"] = carrinho
        messages.success(request, f"{perfume.nome} adicionado ao carrinho.")
    return _voltar(request)


@require_POST
def diminuir_carrinho(request, pk):
    carrinho = request.session.get("carrinho", {})
    atual = carrinho.get(str(pk), 0)
    if atual <= 1:
        carrinho.pop(str(pk), None)
    else:
        carrinho[str(pk)] = atual - 1
    request.session["carrinho"] = carrinho
    return redirect("ver_carrinho")


@require_POST
def remover_carrinho(request, pk):
    carrinho = request.session.get("carrinho", {})
    carrinho.pop(str(pk), None)
    request.session["carrinho"] = carrinho
    messages.success(request, "Item removido do carrinho.")
    return redirect("ver_carrinho")

#As ações de alterar o carrinho só aceitam POST, o mesmo cuidado da exclusão de misturas

def cadastro(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = CadastroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            messages.success(request, f"Conta criada! Bem-vinda, {usuario.username}.")
            return redirect("home")
    else:
        form = CadastroForm()

    return render(request, "registration/cadastro.html", {"form": form})