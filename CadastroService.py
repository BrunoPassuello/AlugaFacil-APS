from typing import Optional, Dict, Any, Tuple
from datetime import datetime
from Pessoa import Pessoa
from RepositorioUsuarios import RepositorioUsuarios

class CadastroService:
    def __init__(self, repo: RepositorioUsuarios):
        self.repo = repo

    def cadastrar(self, cpf: str, data_nascimento: datetime, email: str, nome: str, senha: str, telefone: str, telefone_verificado: bool = False) -> Tuple[bool, Optional[Dict[str, Any]], str]:
        '''
        Retorno de cadastrar():
        True (cadastro realizado) OU False (cadastro falhou) ;
        Json com informações do usuário (Só retorna se cadastro for realizado) ;
        Motivo do erro OU Sucesso
        '''
        
        # Verifica se todos os campos são válidos
        if not isinstance(cpf, str) or not isinstance(email, str) or not isinstance(senha, str) or not isinstance(nome, str) or not isinstance(telefone, str):
            return False, None, "Dados inválidos"

        # Verifica se o email é único
        email_norm = email.strip().lower()
        if self.repo.obter_por_email(email_norm) is not None:
            return False, None, "E-mail já cadastrado"

        # Cria uma nova instância de Pessoa
        nova_pessoa = Pessoa(
            cpf=cpf,
            data_nascimento=data_nascimento,
            email=email_norm,
            nome=nome,
            senha=senha,
            telefone=telefone,
            telefone_verificado=telefone_verificado
        )

        # Adiciona a pessoa ao repositório
        self.repo.adicionar(nova_pessoa)

        # Retorna os dados do usuário em formato JSON
        payload = {
            "email": nova_pessoa.email,
            "nome": nova_pessoa.nome,
            "cpf": nova_pessoa.cpf,
            "telefoneVerificado": nova_pessoa.telefone_verificado,
        }
        return True, payload, "Cadastro realizado com sucesso"
