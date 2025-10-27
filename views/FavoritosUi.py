from nicegui import ui, app

from services.FavoritoService import FavoritoService


class FavoritosUi:
    def __init__(self):
        self._favorito_service = FavoritoService()

    def render(self):
        if 'usuario_logado' not in app.storage.user:
            ui.navigate.to('/login')
            return

        usuario = app.storage.user['usuario_logado']
        email = usuario['email']

        with ui.header().classes('items-center justify-between'):
            ui.label('AlugaFácil').classes('text-xl font-bold text-primary')
            with ui.row():
                ui.button('Anúncios', on_click=lambda: ui.navigate.to(
                    '/anuncios')).props('flat')
                ui.button('Dashboard', on_click=lambda: ui.navigate.to(
                    '/dashboard')).props('flat')

        with ui.column().classes('w-full p-6'):
            ui.label('Favoritos').classes(
                'text-3xl font-bold mb-4 text-primary')
            favoritos = self._favorito_service.listar(email)
            if not favoritos:
                ui.label('Nenhum favorito adicionado ainda.').classes(
                    'text-gray-600')
            for fav in favoritos:
                self._render_fav_card(fav, email)

            ui.button('Voltar ao Dashboard', on_click=lambda: ui.navigate.to(
                '/dashboard')).classes('mt-8').props('color=primary outline')

    def _render_fav_card(self, fav_dict, email):
        anuncio = fav_dict['anuncio']
        anotacao = fav_dict.get('anotacao', '')
        with ui.card().classes('w-full mb-4 flex items-center p-0'):
            ui.image(anuncio.imagem_url).classes('w-40 h-32 object-cover')
            with ui.column().classes('p-4 w-full'):
                ui.label(anuncio.titulo).classes(
                    'text-lg font-bold text-primary')
                ui.label(
                    f'Adicionado em {fav_dict["data_favorito"].strftime("%d/%m/%Y")}').classes('text-sm text-gray-600')
                ui.label(f'Valor: R${anuncio.valor:.2f}').classes(
                    'text-green-600 font-medium')
                if anotacao:
                    ui.label(f'Anotação: {anotacao}').classes(
                        'text-sm text-gray-700')
                with ui.row().classes('mt-2'):
                    ui.button('Entrar em contato', on_click=lambda: ui.notify(
                        'Funcionalidade futura')).props('color=primary')
                    ui.button('Editar', on_click=lambda a_id=anuncio.id: self._editar_anotacao(
                        email, a_id, anotacao)).props('color=primary outline')
                    ui.button('Remover', on_click=lambda a_id=anuncio.id: self._remover(
                        email, a_id)).props('color=negative')

    def _editar_anotacao(self, email, anuncio_id, anotacao_atual):
        dialog = ui.dialog()
        with dialog:
            with ui.card().classes('p-4 w-96'):
                ui.label('Editar anotação').classes('text-lg font-bold mb-2')
                anot_input = ui.textarea(
                    value=anotacao_atual).classes('w-full')
                with ui.row().classes('justify-end mt-4'):
                    ui.button('Cancelar', on_click=dialog.close).props('flat')
                    ui.button('Salvar', on_click=lambda: self._salvar_edicao(
                        dialog, email, anuncio_id, anot_input)).props('color=primary')
        dialog.open()

    def _salvar_edicao(self, dialog, email, anuncio_id, input_widget):
        nova_anot = input_widget.value or ''
        self._favorito_service.atualizar_anotacao(email, anuncio_id, nova_anot)
        ui.notify('Anotação atualizada', type='positive')
        dialog.close()
        ui.navigate.refresh()

    def _remover(self, email, anuncio_id):
        self._favorito_service.remover(email, anuncio_id)
        ui.notify('Favorito removido', type='positive')
        ui.navigate.refresh()
