from datetime import datetime
from LoginService import LoginService
from RepositorioUsuarios import RepositorioUsuarios
from Locatario import Locatario
from Proprietario import Proprietario

repo = RepositorioUsuarios()
auth_service = LoginService(repo)

locatario_teste = Locatario(
    cpf="11122233344",
    data_nascimento=datetime(2005, 8, 2),
    email="brunão@email.com",
    nome="Bruno Passuello",
    senha="INTERNACIONAL",
    telefone="48999898765",
    estudante=False,
    fumante=False,
    instituicao_ensino_str="",
    observacoes_str="Busco apto perto do centro.",
    possui_pet=True,
    profissao_str="Desenvolvedor",
    tipo_pet_str="Cachorro",
)

proprietario_teste = Proprietario(
    cpf="555.666.777-88",
    data_nascimento=datetime(1999, 7, 18),
    email="mariana@email.com",
    nome="Mariana Passuello",
    senha="mariana_senha_segura",
    telefone="48988776655",
    aceita_apenas_tel_verf=False,
    anos_mercado=5,
    avaliacao_media=4.8,
    horario_atendimento="09:00-18:00",
    quantidade_imoveis=3,
    telefone_verificado=False
)

#simulacao de mudança de telefone
locatario_teste.telefone_verificado = True

#simulaçao do calculo de avaliacao
proprietario_teste.avaliacao = 4.6

#adiciona os objetos testes no repositorio de usuarios 
repo.adicionar(locatario_teste)
repo.adicionar(proprietario_teste)


print("--- Usuários de teste carregados no repositório em memória. ---")

def tentar_login(email, senha):
    print(f"\nTentando login com E-mail: {email} | Senha: {senha}")
    sucesso, payload, mensagem = auth_service.login(email, senha)
    
    if sucesso:
        print(f"  -> Resultado: Sucesso! ({mensagem})")
        print(f"     Payload da sessão: {payload}")
    else:
        print(f"  -> Resultado: Falha! ({mensagem})")

#Login bem-sucedido de um locatário
tentar_login("brunão@email.com", "INTERNACIONAL")

#Login bem-sucedido de um proprietário
tentar_login("mariana@email.com", "mariana_senha_segura")

#Tentativa de login com senha errada
tentar_login("brunão@email.com", "senha_errada")

#Tentativa de login com um email inexistente
tentar_login("usuario.inexistente@email.com", "qualquer_senha")
