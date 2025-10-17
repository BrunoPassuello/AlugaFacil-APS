from nicegui import ui
from views.LoginUi import LoginUI
from views.DashboardUi import DashboardUi

@ui.page('/login')
def login():
    LoginUI().render()

@ui.page('/dashboard')
def dashboard():
    DashboardUi().render()

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

