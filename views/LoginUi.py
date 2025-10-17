import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nicegui import ui, app
from services.LoginService import LoginService
from repository.CadastroRepositoryPickle import CadastroRepositoryPickle
from entities.Locatario import Locatario
from entities.Proprietario import Proprietario

from datetime import datetime

class LoginUI:
    def __init__(self):
        self.service_login = LoginService(CadastroRepositoryPickle())
        self.email = None
        self.senha = None
    
    def render(self):
        ui.query('body').style('background-color: #f5f5f5')
        
        with ui.column().classes('absolute-center items-center'):
            with ui.card().classes('w-96 p-8'):
                ui.label('Login - AlugaFacil').classes('text-2xl font-bold mb-4 text-center')
                
                self.email = ui.input(
                    label='E-mail',
                    placeholder='seu.email@exemplo.com'
                ).props('type=email').classes('w-full').on('keydown.enter', self.fazer_login)
                
                self.senha = ui.input(
                    label='Senha',
                    password=True,
                    password_toggle_button=True
                ).classes('w-full').on('keydown.enter', self.fazer_login)
                
                ui.button(
                    'Entrar',
                    on_click=self.fazer_login
                ).classes('w-full mt-4').props('color=primary')
                
                with ui.row().classes('w-full justify-center mt-4'):
                    ui.label('Não tem conta?').classes('text-sm')
                    ui.link('Cadastre-se', '/cadastro').classes('text-sm text-blue-600')
    
    def fazer_login(self):
        email_valor = self.email.value.strip()
        senha_valor = self.senha.value
        
        if not email_valor or not senha_valor:
            ui.notify('Preencha todos os campos', type='warning')
            return
        
        sucesso, pessoa, mensagem = self.service_login.login(email_valor, senha_valor)
        
        #Se sucesso, "entra" pro site, na tela do Dashboard
        if sucesso:
            ui.notify(mensagem, type='positive')
            app.storage.user['usuario_logado'] = pessoa
            app.storage.user['email'] = email_valor
            ui.navigate.to('/dashboard')
        #Se não, reseta a senha e continua na tela de login notificando erro no login
        else:
            ui.notify(mensagem, type='negative')
            self.senha.value = ''
