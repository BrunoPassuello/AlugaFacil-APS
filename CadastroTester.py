from datetime import datetime
from CadastroService import CadastroService
from RepositorioUsuarios import RepositorioUsuarios
from Locatario import Locatario
from Proprietario import Proprietario

repo = RepositorioUsuarios()
cadastro_service = CadastroService(repo)

def testar_cadastro_locatario():
    print("\n--- Teste de Cadastro para Locatário ---")

    resultado, dados, mensagem = cadastro_service.cadastrar(
        tipo_usuario="locatario", 
        cpf="11122233344", 
        data_nascimento=datetime(2005, 8, 2), 
        email="locatario@email.com", 
        nome="Bruno Passuello", 
        senha="senha_locatario", 
        telefone="48999898765", 
        estudante=False, 
        fumante=False, 
        instituicao_ensino_str="Universidade XYZ", 
        observacoes_str="Procurando apto perto do centro.",
        possui_pet=True, 
        profissao_str="Desenvolvedor", 
        tipo_pet_str="Cachorro"
    )

    print(f"Resultado: {mensagem}")
    print(f"Dados cadastrados: {dados}")
    
def testar_cadastro_proprietario():
    print("\n--- Teste de Cadastro para Proprietário ---")

    resultado, dados, mensagem = cadastro_service.cadastrar(
        tipo_usuario="proprietario", 
        cpf="55566677788", 
        data_nascimento=datetime(1980, 6, 15), 
        email="proprietario@email.com", 
        nome="Mariana Oliveira", 
        senha="senha_proprietario", 
        telefone="48988776655", 
        aceita_apenas_tel_verf=False, 
        anos_mercado=10, 
        avaliacao_media=4.9, 
        horario_atendimento=datetime(2023, 7, 1, 9, 0), 
        quantidade_imoveis=5
    )

    print(f"Resultado: {mensagem}")
    print(f"Dados cadastrados: {dados}")

def testar_cadastro_email_existente():
    print("\n--- Teste de Cadastro com E-mail já Existente ---")

    cadastro_service.cadastrar(
        tipo_usuario="locatario", 
        cpf="12345678900", 
        data_nascimento=datetime(2000, 1, 1), 
        email="locatario@email.com", 
        nome="João Silva", 
        senha="senha_nova", 
        telefone="48999988877", 
        estudante=True, 
        fumante=False, 
        instituicao_ensino_str="Universidade ABC", 
        observacoes_str="Quero alugar um apartamento", 
        possui_pet=False, 
        profissao_str="Estudante", 
        tipo_pet_str=""
    )

def testar_cadastro_tipo_usuario_invalido():
    print("\n--- Teste de Cadastro com Tipo de Usuário Inválido ---")

    resultado, dados, mensagem = cadastro_service.cadastrar(
        tipo_usuario="visitante",  
        cpf="77788899900", 
        data_nascimento=datetime(1992, 4, 10), 
        email="visitante@email.com", 
        nome="Carlos Silva", 
        senha="senha_visitante", 
        telefone="48987654321"
    )

    print(f"Resultado: {mensagem}")
    print(f"Dados: {dados}")

# Executando os testes
testar_cadastro_locatario()
testar_cadastro_proprietario()
testar_cadastro_email_existente()
testar_cadastro_tipo_usuario_invalido()

