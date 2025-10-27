from nicegui import ui
from views.LoginUi import LoginUI
from views.DashboardUi import DashboardUi
# Novas UIs
from views.AnunciosUi import AnunciosUi
from views.FavoritosUi import FavoritosUi
from views.CadastroUi import CadastroUI


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


@ui.page('/')
def index():
    ui.navigate.to('/login')


if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        port=8080,
        reload=True,
        title='AlugaFacil - Sistema de Login',
        storage_secret='ALUGA FACIL MELHOR QUE OLX'
    )
