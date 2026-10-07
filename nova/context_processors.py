def carrinho(request):
    dados = request.session.get("carrinho", {})
    return {"carrinho_qtd": sum(dados.values())}

#deixa o número de itens disponível em todas as páginas, para o contador da navbar