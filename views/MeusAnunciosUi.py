from nicegui import ui, app
from services.AnuncioService import AnuncioService
from services.ImovelService import ImovelService

class MeusAnunciosUi:
    
    def __init__(self):
        self._anuncio_service = AnuncioService()
        self._imovel_service = ImovelService()
    
    def render(self):
        if 'usuario_logado' not in app.storage.user:
            ui.navigate.to('/login')
            return
        
        usuario = app.storage.user['usuario_logado']
        email = usuario['email']
        tipo = usuario.get('tipo', 'locatario')
        
        if tipo != 'proprietario':
            ui.label('Acesso negado. Apenas proprietários podem acessar esta página.').classes('text-red-600')
            ui.button('Voltar', on_click=lambda: ui.navigate.to('/dashboard')).props('color=primary')
            return
        
        ui.query('body').style('background-color: #ffffff')
        
        with ui.header().classes('items-center justify-between'):
            ui.label('AlugaFácil').classes('text-xl font-bold text-primary')
            with ui.row():
                ui.button('Dashboard', on_click=lambda: ui.navigate.to('/dashboard')).props('flat')
                ui.button('Meus Imóveis', on_click=lambda: ui.navigate.to('/meus-imoveis')).props('flat')
        
        with ui.column().classes('w-full p-6'):
            ui.label('Meus Anúncios').classes('text-3xl font-bold mb-4 text-primary')
            
            ui.button('Criar Novo Anúncio', 
                     on_click=lambda: self._abrir_dialogo_criar_anuncio(email)).props('color=primary').classes('mb-4')
            
            anuncios = self._anuncio_service.listar_por_proprietario(email)
            
            if not anuncios:
                ui.label('Você ainda não criou nenhum anúncio.').classes('text-gray-600 italic')
                ui.label('Cadastre um imóvel primeiro em "Meus Imóveis" antes de criar um anúncio.').classes('text-sm text-gray-500 italic')
            else:
                for anuncio in anuncios:
                    self._render_card_anuncio(anuncio, email)
            
            ui.button('Voltar ao Dashboard', 
                     on_click=lambda: ui.navigate.to('/dashboard')).classes('mt-8').props('color=primary outline')
    
    def _render_card_anuncio(self, anuncio, email_proprietario):
        with ui.card().classes('w-full mb-4 flex items-center p-0'):
            ui.image(anuncio.imagem_url).classes('w-64 h-48 object-cover rounded mx-auto')
            
            with ui.column().classes('p-4 w-full'):
                ui.label(anuncio.titulo).classes('text-lg font-bold text-primary')
                ui.label(f'Postado em {anuncio.data_postagem.strftime("%d/%m/%Y")}').classes('text-sm text-gray-600')
                ui.label(f'Valor: R$ {anuncio.valor:.2f}/mês').classes('text-green-600 font-medium')
                ui.label(f'Endereço: {anuncio.endereco}').classes('text-sm text-gray-700')
                ui.label(f'Cidade: {anuncio.cidade}').classes('text-sm text-gray-700')
                
                if anuncio.imovel:
                    ui.label(f'Tipo: {anuncio.imovel.tipo_imovel().capitalize()}').classes('text-sm text-gray-600')
                
                with ui.row().classes('mt-2 gap-2'):
                    ui.button('Editar Anúncio', 
                            on_click=lambda a=anuncio: self._abrir_dialogo_editar_anuncio(a, email_proprietario)).props('color=primary size=sm')
                    ui.button('Remover Anúncio', 
                            on_click=lambda a=anuncio: self._remover_anuncio(a.id, email_proprietario)).props('color=negative size=sm')

    def _abrir_dialogo_editar_anuncio(self, anuncio, email_proprietario):
        dialog = ui.dialog()
        with dialog:
            with ui.card().classes('p-6 w-full max-w-lg'):
                ui.label('Editar Anúncio').classes('text-2xl font-bold mb-4')
                
                titulo_input = ui.input(
                    label='Título do Anúncio',
                    value=anuncio.titulo,
                    placeholder='Ex: Apartamento 2 quartos no Centro'
                ).classes('w-full')
                
                valor_input = ui.number(
                    label='Valor do Aluguel (R$/mês)',
                    value=anuncio.valor,
                    min=0.01,
                    step=0.01,
                    format='%.2f'
                ).classes('w-full')
                
                imagem_input = ui.input(
                    label='URL da Imagem',
                    value=anuncio.imagem_url,
                    placeholder='https://...'
                ).classes('w-full')
                
                with ui.row().classes('justify-end mt-4 gap-2'):
                    ui.button('Cancelar', on_click=dialog.close).props('flat')
                    ui.button('Salvar Alterações', 
                            on_click=lambda: self._editar_anuncio(
                                dialog, anuncio.id, email_proprietario, titulo_input, valor_input, imagem_input
                            )).props('color=primary')
        
        dialog.open()

    def _editar_anuncio(self, dialog, anuncio_id, email, titulo_input, valor_input, imagem_input):
        titulo = titulo_input.value
        valor = valor_input.value or 0
        imagem_url = imagem_input.value or "https://i.ibb.co/9q0N4pG/door-key.jpg"
        
        if not titulo or valor <= 0:
            ui.notify('Preencha todos os campos obrigatórios', type='warning')
            return
        
        sucesso, mensagem = self._anuncio_service.atualizar_anuncio(
            anuncio_id=anuncio_id,
            proprietario_email=email,
            titulo=titulo,
            valor=valor,
            imagem_url=imagem_url
        )
        
        if sucesso:
            ui.notify(mensagem, type='positive')
            dialog.close()
            ui.navigate.reload()
        else:
            ui.notify(mensagem, type='negative')

    
    def _abrir_dialogo_criar_anuncio(self, email_proprietario):
        imoveis = self._imovel_service.listar_por_proprietario(email_proprietario)
        
        if not imoveis:
            ui.notify('Você precisa cadastrar um imóvel antes de criar um anúncio', type='warning')
            return
        
        dialog = ui.dialog()
        with dialog:
            with ui.card().classes('p-6 w-full max-w-lg'):
                ui.label('Criar Novo Anúncio').classes('text-2xl font-bold mb-4')
                
                imovel_select = ui.select(
                    label='Selecione o Imóvel',
                    options={i.id: f'{i.tipo_imovel().capitalize()} - {i.endereco}' for i in imoveis},
                    with_input=True
                ).classes('w-full')
                
                titulo_input = ui.input(
                    label='Título do Anúncio',
                    placeholder='Ex: Apartamento 2 quartos no Centro'
                ).classes('w-full')
                
                valor_input = ui.number(
                    label='Valor do Aluguel (R$/mês)',
                    min=0.01,
                    step=0.01,
                    format='%.2f'
                ).classes('w-full')
                
                imagem_input = ui.input(
                    label='URL da Imagem (opcional)',
                    placeholder='https://...',
                    value='https://i.ibb.co/9q0N4pG/door-key.jpg'
                ).classes('w-full')
                
                with ui.row().classes('justify-end mt-4 gap-2'):
                    ui.button('Cancelar', on_click=dialog.close).props('flat')
                    ui.button('Criar Anúncio', 
                             on_click=lambda: self._criar_anuncio(
                                 dialog, email_proprietario, imovel_select, titulo_input, valor_input, imagem_input
                             )).props('color=primary')
        
        dialog.open()
    
    def _criar_anuncio(self, dialog, email, imovel_select, titulo_input, valor_input, imagem_input):
        imovel_id = imovel_select.value
        titulo = titulo_input.value
        valor = valor_input.value or 0
        imagem_url = imagem_input.value or "https://i.ibb.co/9q0N4pG/door-key.jpg"
        
        if not imovel_id or not titulo or valor <= 0:
            ui.notify('Preencha todos os campos obrigatórios', type='warning')
            return
        
        sucesso, anuncio, mensagem = self._anuncio_service.criar_anuncio(
            proprietario_email=email,
            imovel_id=imovel_id,
            titulo=titulo,
            valor=valor,
            imagem_url=imagem_url
        )
        
        if sucesso:
            ui.notify(mensagem, type='positive')
            dialog.close()
            ui.navigate.reload()
        else:
            ui.notify(mensagem, type='negative')
    
    def _remover_anuncio(self, anuncio_id, email_proprietario):
        sucesso, mensagem = self._anuncio_service.remover(anuncio_id, email_proprietario)
        
        if sucesso:
            ui.notify(mensagem, type='positive')
            ui.navigate.reload()
        else:
            ui.notify(mensagem, type='negative')
