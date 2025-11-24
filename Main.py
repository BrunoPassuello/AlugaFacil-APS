from nicegui import ui

from views.LoginUi import LoginUI
from views.DashboardUi import DashboardUi
from views.AnunciosUi import AnunciosUi
from views.FavoritosUi import FavoritosUi
from views.CadastroUi import CadastroUI
from views.NegociacoesUi import NegociacoesUi
from views.VisitasUi import VisitasUi

from views.MeusImoveisUi import MeusImoveisUi
from views.MeusAnunciosUi import MeusAnunciosUi

@ui.page('/login')
def login():
    LoginUI().render()

@ui.page('/cadastro')
def cadastro():
    CadastroUI()

@ui.page('/dashboard')
def dashboard():
    DashboardUi().render()

@ui.page('/anuncios')
def anuncios():
    AnunciosUi().render()

@ui.page('/favoritos')
def favoritos():
    FavoritosUi().render()

@ui.page('/negociacoes')
def negociacoes():
    NegociacoesUi().render()

@ui.page('/visitas')
def visitas():
    VisitasUi().render()

@ui.page('/meus-imoveis')
def meus_imoveis():
    MeusImoveisUi().render()

@ui.page('/meus-anuncios')
def meus_anuncios():
    MeusAnunciosUi().render()

@ui.page('/')
def index():
    ui.navigate.to('/login')

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        port=8080,
        reload=True,
        title='AlugaFacil - Sistema de Aluguel',
        storage_secret='ALUGA FACIL MELHOR QUE OLX'
    )
