from nicegui import ui, app

from services.AnuncioService import AnuncioService
from services.FavoritoService import FavoritoService


class AnunciosUi:
    """Renderiza a listagem de anúncios com opção de favoritá-los, seguindo protótipo."""

    def __init__(self):
        self._anuncio_service = AnuncioService()
        self._favorito_service = FavoritoService()

    # ---------------- RENDER -----------------

    def render(self):
        if 'usuario_logado' not in app.storage.user:
            ui.navigate.to('/login')
            return

        usuario = app.storage.user['usuario_logado']

        ui.query('body').style('background-color: #ffffff')

        with ui.header().classes('items-center justify-between'):
            ui.label('AlugaFácil').classes('text-xl font-bold text-primary')
            with ui.row():
                ui.button('Dashboard', on_click=lambda: ui.navigate.to(
                    '/dashboard')).props('flat')
                ui.button('Favoritos', on_click=lambda: ui.navigate.to(
                    '/favoritos')).props('flat')

        with ui.column().classes('w-full p-6'):
            ui.label('Anúncios').classes(
                'text-3xl font-bold mb-4 text-primary')
            anuncios = self._anuncio_service.listar()
            for anuncio in anuncios:
                self._render_card(anuncio, usuario['email'])

            # Botão voltar
            ui.button('Voltar ao Dashboard', on_click=lambda: ui.navigate.to(
                '/dashboard')).classes('mt-8').props('color=primary outline')

    # ---------------- PRIVADOS ---------------

    def _render_card(self, anuncio, email_usuario):
        with ui.card().classes('w-full mb-4 flex items-center p-0'):
            # Imagem
            ui.image(anuncio.imagem_url).classes('w-40 h-32 object-cover')
            with ui.column().classes('p-4 w-full'):
                ui.label(anuncio.titulo).classes(
                    'text-lg font-bold text-primary')
                ui.label(
                    f'Adicionado em {anuncio.data_postagem.strftime("%d/%m/%Y")}').classes('text-sm text-gray-600')
                ui.label(f'Valor: R${anuncio.valor:.2f}').classes(
                    'text-green-600 font-medium')
                with ui.row().classes('mt-2'):
                    ui.button('Entrar em contato', on_click=lambda: ui.notify(
                        'Funcionalidade futura')).props('color=primary')
                    ui.button('Favoritar', on_click=lambda a=anuncio: self._abrir_dialogo_favoritar(
                        email_usuario, a)).props('color=primary outline')

    def _abrir_dialogo_favoritar(self, email, anuncio):
        dialog = ui.dialog()
        with dialog:
            with ui.card().classes('p-4 w-96'):
                ui.label('Adicionar anotação (opcional)').classes(
                    'text-lg font-bold mb-2')
                anot_input = ui.textarea(
                    placeholder='Insira sua anotação aqui...').classes('w-full')
                with ui.row().classes('justify-end mt-4'):
                    ui.button('Cancelar', on_click=dialog.close).props('flat')
                    ui.button('Salvar', on_click=lambda: self._salvar_favorito(
                        dialog, email, anuncio, anot_input)).props('color=primary')
        dialog.open()

    def _salvar_favorito(self, dialog, email, anuncio, input_widget):
        anot = input_widget.value or ""
        if self._favorito_service.adicionar(email, anuncio, anot):
            ui.notify('Favorito adicionado', type='positive')
        else:
            ui.notify('Anúncio já está nos favoritos', type='warning')
        dialog.close()
