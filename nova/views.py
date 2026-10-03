from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import MisturaForm
from .models import Perfume, Mistura


def home(request):
    destaques = Perfume.objects.filter(destaque=True)[:3]
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