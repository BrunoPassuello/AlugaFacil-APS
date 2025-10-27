"""Teste simples em linha de comando para verificar UC03 – Gerenciar Favoritos.
Execute: python test_favoritos.py
"""

from datetime import datetime

from repository.CadastroRepositoryPickle import CadastroRepositoryPickle
from services.AnuncioService import AnuncioService
from services.FavoritoService import FavoritoService
from services.CadastroService import CadastroService

# --------------------------------------------------
# Setup
# --------------------------------------------------
repo = CadastroRepositoryPickle()
fav_service = FavoritoService(repo)
anuncio_service = AnuncioService()

locatario_email = "teste.locatario@exemplo.com"

# Se locatário não existir, cria rapidamente
if repo.get_pessoa_email(locatario_email) is None:
    print("Locatário de teste não encontrado, criando...")
    cadastro_srv = CadastroService(repo)
    cadastro_srv.cadastrar(
        tipo_usuario="locatario",
        cpf="999.999.999-99",
        data_nascimento=datetime(1999, 1, 1),
        email=locatario_email,
        nome="Locatário Teste",
        senha="123",
        telefone="(48) 90000-0000",
        telefone_verificado=True,
        estudante=False,
        fumante=False,
        instituicao_ensino_str="",
        observacoes_str="",
        possui_pet=False,
        profissao_str="QA",
        tipo_pet_str="",
    )

# --------------------------------------------------
# Operações de Favorito
# --------------------------------------------------
print("\n--- Listando anúncios disponíveis ---")
for a in anuncio_service.listar():
    print(f"{a.id} - {a.titulo} - R${a.valor}")

primeiro_anuncio = anuncio_service.get_por_id(1)
print("\nAdicionando favorito #1 com anotação ...")
fav_service.adicionar(locatario_email, primeiro_anuncio, "Ótima localização!")

print("\nFavoritos atuais:")
for f in fav_service.listar(locatario_email):
    print(f"{f['anuncio'].id} | {f['anuncio'].titulo} | Anotação: {f['anotacao']}")

print("\nAtualizando anotação do favorito...")
fav_service.atualizar_anotacao(locatario_email, 1, "Verificar vaga de garagem")

print("\nFavoritos após edição:")
for f in fav_service.listar(locatario_email):
    print(f"{f['anuncio'].id} | {f['anuncio'].titulo} | Anotação: {f['anotacao']}")

print("\nRemovendo favorito...")
fav_service.remover(locatario_email, 1)

print("\nFavoritos finais:")
print(fav_service.listar(locatario_email))

print("Teste concluído com sucesso.")
