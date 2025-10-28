import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nicegui import ui, app
from services.CadastroService import CadastroService
from repository.CadastroRepositoryPickle import CadastroRepositoryPickle
from entities.Locatario import Locatario
from entities.Proprietario import Proprietario
from datetime import datetime

class CadastroUI:
    def __init__(self):
        self.service_cadastro = CadastroService(CadastroRepositoryPickle())
        self.email = None
        self.nome = None
        self.cpf = None
        self.data_nascimento = None
        self.telefone = None
        self.senha = None
        self.instituicao_ensino = None
        self.possui_pet = None
        self.profissao = None
        self.tipo_pet = None
        self.fumante = None
        self.aceita_tel = None
        self.anos_mercado = None
        self.avaliacao_media = None
        self.horario_atendimento = None
        self.quantidade_imoveis = None
        self.tipo_cadastro = {'value': 'Locatário'}
        ui.select(
            ['Locatário', 'Proprietário'],
            value=self.tipo_cadastro['value'],
            on_change=self.tipo_cadastro_changed,
        ).classes('absolute-top-right mt-4 mr-4 w-60')

        # Container centralizado na página
        with ui.row().classes('w-full h-screen items-center justify-center'):
            self.container = ui.column().classes('items-center')
        self.render_inputs()

    def tipo_cadastro_changed(self, e):
        self.tipo_cadastro['value'] = e.value
        self.render_inputs()

    def render_inputs(self):
        self.container.clear()
        ui.query('body').style('background-color: #f5f5f5')

        if self.tipo_cadastro['value'] == "Locatário":
            with self.container:
                with ui.card().classes('w-96 p-8'):
                    ui.label('Cadastro - Locatário').classes('text-2xl font-bold mb-4 text-center')
                    self.nome = ui.input(
                        label='Nome Completo',
                        placeholder='Seu nome...'
                    ).classes('w-full').on('keydown.enter', self.fazer_cadastro)
                    self.cpf = ui.input(
                        label='CPF',
                        placeholder=''
                    ).classes('w-full').on('keydown.enter', self.fazer_cadastro)
                    self.data_nascimento = ui.input(
                        label='Data de nascimento',
                        placeholder='DD/MM/AAAA'
                    ).classes('w-full').on('keydown.enter', self.fazer_cadastro)
                    self.email = ui.input(
                        label='E-mail',
                        placeholder='seu.email@exemplo.com'
                    ).props('type=email').classes('w-full').on('keydown.enter', self.fazer_cadastro)
                    self.telefone = ui.input(
                        label='Número de telefone',
                        placeholder='(XX) X XXXX-XXXX'
                    ).classes('w-full').on('keydown.enter', self.fazer_cadastro)
                    self.senha = ui.input(
                        label='Senha',
                        password=True,
                        password_toggle_button=True
                    ).classes('w-full').on('keydown.enter', self.fazer_cadastro)
                    self.profissao = ui.input(
                        label='Profissão',
                        placeholder='Administrador'
                    ).classes('w-full').on('keydown.enter', self.fazer_cadastro)
                    self.fumante = ui.checkbox(
                       'Sou fumante',
                    ).classes('w-full').on('keydown.enter', self.fazer_cadastro)
                    self.estudante = ui.checkbox(
                       'Sou estudante',
                    ).classes('w-full').on('keydown.enter', self.fazer_cadastro)
                    self.ensino = ui.input(
                        label='Instituição de ensino',
                        placeholder='UFSC'
                    ).classes('w-full').on('keydown.enter', self.fazer_cadastro)
                    self.pet = ui.checkbox(
                       'Possuo pet',
                    ).classes('w-full').on('keydown.enter', self.fazer_cadastro)
                    self.tipo_pet = ui.input(
                        label='Tipo do pet',
                        placeholder='Cachorro'
                    ).classes('w-full').on('keydown.enter', self.fazer_cadastro)
                    ui.button(
                        'Cadastrar',
                        on_click=self.fazer_cadastro
                    ).classes('w-full mt-4').props('color=primary')
                    with ui.row().classes('w-full justify-center mt-4'):
                        ui.label('Já tem conta?').classes('text-sm')
                        ui.link('Login', '/login').classes('text-sm text-blue-600')

        elif self.tipo_cadastro['value'] == "Proprietário":
            with self.container:
                 with ui.card().classes('w-96 p-8'):
                    ui.label('Cadastro - Proprietário').classes('text-2xl font-bold mb-4 text-center')
                    self.nome = ui.input(
                        label='Nome Completo',
                        placeholder='Seu nome...'
                    ).classes('w-full').on('keydown.enter', self.fazer_cadastro)
                    self.cpf = ui.input(
                        label='CPF',
                        placeholder=''
                    ).classes('w-full').on('keydown.enter', self.fazer_cadastro)
                    self.data_nascimento = ui.input(
                        label='Data de nascimento',
                        placeholder='DD/MM/AAAA'
                    ).classes('w-full').on('keydown.enter', self.fazer_cadastro)
                    self.anos_mercado = ui.number(
                        label='Anos no mercado',
                        placeholder='5',
                        min=0
                    ).classes('w-full').on('keydown.enter', self.fazer_cadastro)
                    self.quantidade_imoveis = ui.number(
                        label='Quantidade de imóveis',
                        placeholder='2',
                        min=0
                    ).classes('w-full').on('keydown.enter', self.fazer_cadastro)
                    self.email = ui.input(
                        label='E-mail',
                        placeholder='seu.email@exemplo.com'
                    ).props('type=email').classes('w-full').on('keydown.enter', self.fazer_cadastro)
                    self.telefone = ui.input(
                        label='Número de telefone',
                        placeholder='(XX) X XXXX-XXXX'
                    ).classes('w-full').on('keydown.enter', self.fazer_cadastro)
                    self.senha = ui.input(
                        label='Senha',
                        password=True,
                        password_toggle_button=True
                    ).classes('w-full').on('keydown.enter', self.fazer_cadastro)
                    ui.button(
                        'Cadastrar',
                        on_click=self.fazer_cadastro
                    ).classes('w-full mt-4').props('color=primary')
                    with ui.row().classes('w-full justify-center mt-4'):
                        ui.label('Já tem conta?').classes('text-sm')
                        ui.link('Login', '/login').classes('text-sm text-blue-600')

    def fazer_cadastro(self):
        tipo_valor_ui = self.tipo_cadastro['value']  # "Locatário" | "Proprietário"
        tipo_usuario = 'locatario' if tipo_valor_ui == 'Locatário' else 'proprietario'

        # -------- Campos comuns --------
        nome = (self.nome.value or '').strip()
        email = (self.email.value or '').strip().lower()
        senha = (self.senha.value or '')
        cpf = (self.cpf.value or '').strip()
        data_nascimento_txt = (self.data_nascimento.value or '').strip()
        telefone = (self.telefone.value or '').strip()

        if not all([nome, email, senha, cpf, data_nascimento_txt, telefone]):
            ui.notify('Preencha todos os campos obrigatórios.', type='warning')
            return

        try:
            data_nascimento = datetime.strptime(data_nascimento_txt, '%d/%m/%Y')
        except ValueError:
            ui.notify('Data de nascimento inválida. Use o formato DD/MM/AAAA.', type='warning')
            return

        telefone_verificado = False

        outros = {}

        if tipo_usuario == 'locatario':
            estudante = bool(self.estudante.value)
            fumante = bool(self.fumante.value)
            instituicao_ensino_str = (self.ensino.value or '').strip() if estudante else ""
            observacoes_str = ""  # ajuste se tiver um campo de observações
            possui_pet = bool(self.pet.value)
            profissao_str = (self.profissao.value or '').strip()
            tipo_pet_str = (self.tipo_pet.value or '').strip() if possui_pet else ""

            outros = {
                'estudante': estudante,
                'fumante': fumante,
                'instituicao_ensino_str': instituicao_ensino_str,
                'observacoes_str': observacoes_str,
                'possui_pet': possui_pet,
                'profissao_str': profissao_str,
                'tipo_pet_str': tipo_pet_str,
            }

        elif tipo_usuario == 'proprietario':
            try:
                anos_mercado = int(self.anos_mercado.value or 0)
                quantidade_imoveis = int(self.quantidade_imoveis.value or 0)
            except ValueError:
                ui.notify('Anos no mercado e quantidade de imóveis devem ser números válidos.', type='warning')
                return

            aceita_apenas_tel_verf = False
            avaliacao_media = 0.0
            horario_atendimento = datetime.now()

            outros = {
                'aceita_apenas_tel_verf': aceita_apenas_tel_verf,
                'anos_mercado': anos_mercado,
                'avaliacao_media': avaliacao_media,
                'horario_atendimento': horario_atendimento,
                'quantidade_imoveis': quantidade_imoveis,
            }

        sucesso, pessoa, mensagem = self.service_cadastro.cadastrar(
            tipo_usuario,            # str: "locatario" | "proprietario"
            cpf,                     # str
            data_nascimento,         # datetime
            email,                   # str
            nome,                    # str
            senha,                   # str
            telefone,                # str
            telefone_verificado,     # bool (default False)
            **outros
        )

        if sucesso:
            ui.notify(mensagem or 'Cadastro realizado com sucesso!', type='positive')
            app.storage.user['usuario_logado'] = pessoa
            app.storage.user['email'] = email
            ui.navigate.to('/dashboard')
        else:
            ui.notify(mensagem or 'Não foi possível realizar o cadastro.', type='negative')
            self.senha.value = ''
