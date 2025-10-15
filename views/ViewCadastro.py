import sys
import os
# Subir 2 níveis: repository/ -> AlugaFacil-APS/
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.CadastroService import CadastroService
from repository.CadastroRepositoryPickle import CadastroRepositoryPickle
from entities.Locatario import Locatario
from entities.Proprietario import Proprietario

from datetime import datetime

serviceCadastro = CadastroService(CadastroRepositoryPickle())

# Locatário 1 - Estudante universitário
sucesso1, pessoa1, mensagem1 = serviceCadastro.cadastrar(
    tipo_usuario="locatario",
    cpf="123.456.789-00",
    data_nascimento=datetime(2000, 5, 15),
    email="joao.silva@estudante.ufsc.br",
    nome="João Silva",
    senha="senha123",
    telefone="(48) 99999-1111",
    telefone_verificado=True,
    # Dados específicos de Locatário via **outros_dados
    estudante=True,
    fumante=False,
    instituicao_ensino_str="UFSC",
    observacoes_str="Procuro república próxima ao campus",
    possui_pet=False,
    profissao_str="Estudante de Sistemas de Informação",
    tipo_pet_str=""
)
print(f"Cadastro 1: {mensagem1}")

sucesso2, pessoa2, mensagem2 = serviceCadastro.cadastrar(
    tipo_usuario="locatario",
    cpf="987.654.321-00",
    data_nascimento=datetime(1995, 8, 22),
    email="maria.santos@gmail.com",
    nome="Maria Santos",
    senha="segura456",
    telefone="(48) 98888-2222",
    telefone_verificado=True,
    estudante=False,
    fumante=False,
    instituicao_ensino_str="",
    observacoes_str="Tenho um cachorro de pequeno porte bem educado",
    possui_pet=True,
    profissao_str="Desenvolvedora de Software",
    tipo_pet_str="Cachorro pequeno porte"
)
print(f"Cadastro 2: {mensagem2}")

# Locatário 3 - Fumante sem pet
sucesso3, pessoa3, mensagem3 = serviceCadastro.cadastrar(
    tipo_usuario="locatario",
    cpf="456.789.123-00",
    data_nascimento=datetime(1992, 3, 10),
    email="carlos.oliveira@hotmail.com",
    nome="Carlos Oliveira",
    senha="carlos789",
    telefone="(48) 97777-3333",
    telefone_verificado=False,
    estudante=False,
    fumante=True,
    instituicao_ensino_str="",
    observacoes_str="Aceito fumódromo no imóvel",
    possui_pet=False,
    profissao_str="Engenheiro Civil",
    tipo_pet_str=""
)
print(f"Cadastro 3: {mensagem3}")

# Proprietário 1 - Experiente no mercado
sucesso4, pessoa4, mensagem4 = serviceCadastro.cadastrar(
    tipo_usuario="proprietario",
    cpf="111.222.333-44",
    data_nascimento=datetime(1975, 12, 5),
    email="ana.proprietaria@gmail.com",
    nome="Ana Proprietária",
    senha="propsegura123",
    telefone="(48) 96666-4444",
    telefone_verificado=True,
    # Dados específicos de Proprietário via **outros_dados
    aceita_apenas_tel_verf=True,
    anos_mercado=10,
    avaliacao_media=4.8,
    horario_atendimento=datetime.strptime("09:00", "%H:%M"),
    quantidade_imoveis=5
)
print(f"Cadastro 4: {mensagem4}")

# Proprietário 2 - Iniciante no mercado
sucesso5, pessoa5, mensagem5 = serviceCadastro.cadastrar(
    tipo_usuario="proprietario",
    cpf="555.666.777-88",
    data_nascimento=datetime(1988, 6, 18),
    email="pedro.imoveis@outlook.com",
    nome="Pedro Imóveis",
    senha="pedro456",
    telefone="(48) 95555-5555",
    telefone_verificado=True,
    aceita_apenas_tel_verf=False,
    anos_mercado=2,
    avaliacao_media=4.2,
    horario_atendimento=datetime.strptime("14:00", "%H:%M"),
    quantidade_imoveis=2
)
print(f"Cadastro 5: {mensagem5}")


dicionario_cadastros = serviceCadastro.get_all_cadastros()
print("Começando prints: ")
for pessoa in dicionario_cadastros.values():
    print(f"nome: {pessoa.nome}")
    print(f"cpf: {pessoa.cpf}")
    print(f"email: {pessoa.email}")