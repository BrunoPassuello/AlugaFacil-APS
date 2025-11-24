from typing import Optional, Dict, Any, Tuple
from datetime import datetime
from entities.Locatario import Locatario
from entities.Proprietario import Proprietario
from repository.CadastroRepositoryPickle import CadastroRepositoryPickle

class CadastroService:
    def __init__(self, repo: CadastroRepositoryPickle):
        self.repo = repo

    def cadastrar(self, tipo_usuario: str, cpf: str, data_nascimento: datetime, email: str, 
                nome: str, senha: str, telefone: str, telefone_verificado: bool = False, 
                  **outros_dados) -> Tuple[bool, Optional[Dict[str, Any]], str]:
        '''
        Cadastra um usuário como Locatário ou Proprietário, dependendo do tipo de usuário informado.
        
        tipo_usuario: "locatario" ou "proprietario"
        Outros parâmetros variam conforme o tipo de usuário.
        '''
        

        if not isinstance(cpf, str) or not isinstance(email, str) or not isinstance(senha, str) or not isinstance(nome, str) or not isinstance(telefone, str):
            return False, None, "Dados inválidos"
        

        email_norm = email.strip().lower()
        if self.repo.get_pessoa_email(email_norm) is not None:
            return False, None, "E-mail já cadastrado"
        

        if tipo_usuario == "locatario":

            estudante = outros_dados.get("estudante", False)
            fumante = outros_dados.get("fumante", False)
            instituicao_ensino_str = outros_dados.get("instituicao_ensino_str", "")
            observacoes_str = outros_dados.get("observacoes_str", "")
            possui_pet = outros_dados.get("possui_pet", False)
            profissao_str = outros_dados.get("profissao_str", "")
            tipo_pet_str = outros_dados.get("tipo_pet_str", "")
            

            novo_usuario = Locatario(cpf, data_nascimento, email_norm, nome, senha, telefone, 
                                    estudante, fumante, instituicao_ensino_str, observacoes_str,
                                    possui_pet, profissao_str, tipo_pet_str, telefone_verificado)
        
        elif tipo_usuario == "proprietario":

            aceita_apenas_tel_verf = outros_dados.get("aceita_apenas_tel_verf", False)
            anos_mercado = outros_dados.get("anos_mercado", 0)
            avaliacao_media = outros_dados.get("avaliacao_media", 0.0)
            horario_atendimento = outros_dados.get("horario_atendimento", datetime.now())
            quantidade_imoveis = outros_dados.get("quantidade_imoveis", 0)
            
            novo_usuario = Proprietario(cpf, data_nascimento, email_norm, nome, senha, telefone, 
                                        aceita_apenas_tel_verf, anos_mercado, avaliacao_media, 
                                        horario_atendimento, quantidade_imoveis, telefone_verificado)
        
        else:
            return False, None, "Tipo de usuário inválido"

        self.repo.adicionar_cadastro(novo_usuario)
        

        payload = {
            "email": novo_usuario.email,
            "nome": novo_usuario.nome,
            "cpf": novo_usuario.cpf,
            "tipo": novo_usuario.get_tipo_usuario(),
            "telefoneVerificado": novo_usuario.telefone_verificado,
        }
        return True, payload, "Cadastro realizado com sucesso"

    def get_all_cadastros(self):
        return self.repo.get_all()