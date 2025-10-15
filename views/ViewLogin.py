import sys
import os
# Subir 2 níveis: repository/ -> AlugaFacil-APS/
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.LoginService import LoginService
from repository.CadastroRepositoryPickle import CadastroRepositoryPickle
from entities.Locatario import Locatario
from entities.Proprietario import Proprietario

from datetime import datetime

serviceLogin = LoginService(CadastroRepositoryPickle())

# Locatário 1 - Estudante universitário
sucesso1, pessoa1, mensagem1 = serviceLogin.login(
    email="joao.silva@estudante.ufsc.br",
    senha="senha123",
)
print(f"Cadastro 1: {mensagem1}")

sucesso2, pessoa2, mensagem2 = serviceLogin.login(
    email="maria.santos@gmail.com",
    senha="segura456",
)
print(f"Cadastro 2: {mensagem2}")

# Locatário 3 - Fumante sem pet
sucesso3, pessoa3, mensagem3 = serviceLogin.login(
    email="carlos.oliveira@hotmail.com",
    senha="carlos789",
)
print(f"Cadastro 3: {mensagem3}")

# Proprietário 1 - Experiente no mercado
sucesso4, pessoa4, mensagem4 = serviceLogin.login(
    email="EMAILERRADO@gmail.com",
    senha="propsegura123",
)
print(f"Cadastro 4: {mensagem4}")

# Proprietário 2 - Iniciante no mercado
sucesso5, pessoa5, mensagem5 = serviceLogin.login(
    email="pedro.imoveis@outlook.com",
    senha="SENHA ERRADA",
)
print(f"Cadastro 5: {mensagem5}")