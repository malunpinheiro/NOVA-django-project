# NOVA ✦ Perfumaria de Nicho

Vitrine de perfumes tropicais de nicho com um **Laboratório de Misturas**: o usuário logado cria a própria fragrância combinando 2 ou 3 perfumes do catálogo. Projeto da Aula 12 de Back-end com Python (Django).

## O que o projeto faz

- **Home** com os perfumes em destaque e **vitrine** com filtro por família olfativa
- **Laboratório**: listagem, detalhes, criação, edição e exclusão de misturas (CRUD completo)
- **Login** nativo do Django; criar, editar e excluir exigem login (`@login_required`)
- Só o criador de uma mistura pode editá-la ou excluí-la
- Exclusão por POST, com página de confirmação
- Templates com herança (`base.html`) e Bootstrap 5

## Como rodar

1. Clone o repositório e entre na pasta:
```bash
   git clone https://github.com/malunpinheiro/NOVA-django-project.git
   cd NOVA-django-project
```
2. Crie e ative o ambiente virtual:
```bash
   python -m venv venv
   venv\Scripts\activate        # Windows
   # source venv/bin/activate   # Linux/Mac
```
3. Instale as dependências:
```bash
   pip install -r requirements.txt
```
4. Crie o banco e carregue os perfumes:
```bash
   python manage.py migrate
   python manage.py loaddata perfumes
```
5. Crie um superusuário:
```bash
   python manage.py createsuperuser
```
6. Rode o servidor e acesse http://127.0.0.1:8000/:
```bash
   python manage.py runserver
```

## Tecnologias

Python • Django • Bootstrap 5 • SQLite