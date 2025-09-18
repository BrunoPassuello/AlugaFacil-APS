# auth.py
from typing import Optional, Tuple, Dict, Any
from RepositorioUsuarios import RepositorioUsuarios

class LoginService:
    def __init__(self, repo: RepositorioUsuarios):
        self.repo = repo

    def login(self, email: str, senha: str) -> Tuple[bool, Optional[Dict[str, Any]], str]:
        '''
        Retorno de login(): {
        True (login correto) OU False (login errado) ;
        Json com informações do usuário (Só retorna se login correto) ;
        Motivo do erro OU Sucesso
        }
        '''
        
        #Verifica se email e senha são strings válidas
        if not isinstance(email, str) or not isinstance(senha, str):
            return False, None, "Credenciais inválidas"

        #Verifica se email possui "@"
        email_norm = email.strip().lower()
        if "@" not in email_norm or len(senha) < 1:
            return False, None, "E-mail ou senha inválidos"

        #Verifica se há um usuário com aquele email -> retorno de Usuário
        pessoa = self.repo.obter_por_email(email_norm)
        
        if pessoa is None:

            #Não diz se o e-mail não existe -> SEGURANÇA
            return False, None, "Credenciais inválidas"

        #Verificação de senha criptografada
        if not pessoa.verificar_senha(senha):
            return False, None, "Credenciais inválidas"

        #Sucesso -> retorno de informações do usuárip
        payload = {
            "email": pessoa.email,
            "nome": pessoa.nome,
            "tipo": pessoa.get_tipo_usuario(),  # "locatario" ou "proprietario"
            "telefoneVerificado": pessoa.telefone_verificado,
            "avaliacao": pessoa.avaliacao,
        }
        return True, payload, "Autenticado"