from nicegui import ui, app
from services.AnuncioService import AnuncioService
from services.FavoritoService import FavoritoService
from services.NegociacaoService import NegociacaoService

class AnunciosUi:
    """Renderiza a listagem de anúncios com opção de favoritá-los e fazer propostas."""
    
    def __init__(self):
        self._anuncio_service = AnuncioService()
        self._favorito_service = FavoritoService()
        self._negociacao_service = NegociacaoService()
    
    # ---------------- RENDER -----------------
    
    def render(self):
        if 'usuario_logado' not in app.storage.user:
            ui.navigate.to('/login')
            return
        
        usuario = app.storage.user['usuario_logado']
        tipo = usuario.get('tipo', 'locatario')
        
        ui.query('body').style('background-color: #ffffff')
        
        with ui.header().classes('items-center justify-between'):
            ui.label('AlugaFácil').classes('text-xl font-bold text-primary')
            with ui.row():
                ui.button('Dashboard', on_click=lambda: ui.navigate.to('/dashboard')).props('flat')
                ui.button('Favoritos', on_click=lambda: ui.navigate.to('/favoritos')).props('flat')
                if tipo == 'locatario':
                    ui.button('Negociações', on_click=lambda: ui.navigate.to('/negociacoes')).props('flat')
                    ui.button('Visitas', on_click=lambda: ui.navigate.to('/visitas')).props('flat')
        
        with ui.column().classes('w-full p-6'):
            ui.label('Anúncios').classes('text-3xl font-bold mb-4 text-primary')
            
            anuncios = self._anuncio_service.listar()
            
            if not anuncios:
                ui.label('Nenhum anúncio disponível no momento.').classes('text-gray-600 italic')
            else:
                for anuncio in anuncios:
                    self._render_card(anuncio, usuario['email'], tipo)
            
            # Botão voltar
            ui.button('Voltar ao Dashboard', 
                     on_click=lambda: ui.navigate.to('/dashboard')).classes('mt-8').props('color=primary outline')
    
    # ---------------- PRIVADOS ---------------
    
    def _render_card(self, anuncio, email_usuario, tipo_usuario):
        with ui.card().classes('w-full mb-4 flex items-center p-0'):
            # Imagem
            ui.image(anuncio.imagem_url).classes('w-40 h-32 object-cover')
            
            with ui.column().classes('p-4 w-full'):
                ui.label(anuncio.titulo).classes('text-lg font-bold text-primary')
                ui.label(f'Adicionado em {anuncio.data_postagem.strftime("%d/%m/%Y")}').classes('text-sm text-gray-600')
                ui.label(f'Valor: R${anuncio.valor:.2f}').classes('text-green-600 font-medium')
                
                with ui.row().classes('mt-2 gap-2'):
                    # Botões disponíveis apenas para locatários
                    if tipo_usuario == 'locatario':
                        ui.button('FAZER PROPOSTA', 
                                 on_click=lambda a=anuncio: self._abrir_dialogo_fazer_proposta(email_usuario, a)).props('color=primary')
                        ui.button('FAVORITAR', 
                                 on_click=lambda a=anuncio: self._abrir_dialogo_favoritar(email_usuario, a)).props('outline')
                    else:
                        ui.label('(Proprietário - visualização apenas)').classes('text-gray-500 italic')
    
    def _abrir_dialogo_fazer_proposta(self, email_locatario, anuncio):
        """Abre diálogo para fazer proposta, com informações do anúncio pré-preenchidas."""
        dialog = ui.dialog()
        with dialog:
            with ui.card().classes('p-6 w-full max-w-lg'):
                ui.label('Fazer Proposta de Aluguel').classes('text-2xl font-bold mb-4')
                
                # Informações do anúncio (apenas visualização)
                with ui.card().classes('w-full p-4 bg-gray-100 mb-4'):
                    ui.label(f'Anúncio: {anuncio.titulo}').classes('font-bold')
                    ui.label(f'Endereço: {anuncio.endereco}').classes('text-sm')
                    ui.label(f'Cidade: {anuncio.cidade}').classes('text-sm')
                    ui.label(f'Valor Anunciado: R$ {anuncio.valor:.2f}').classes('text-green-600 font-medium')
                    ui.label(f'Proprietário: {anuncio.proprietario_email}').classes('text-sm text-gray-600')
                
                # Campos editáveis
                valor_input = ui.number(
                    label='Valor da Proposta (R$)',
                    min=0.01,
                    step=0.01,
                    value=anuncio.valor,  # Pré-preenche com o valor do anúncio
                    format='%.2f'
                ).classes('w-full')
                
                obs_input = ui.textarea(
                    label='Observações (opcional)',
                    placeholder='Adicione detalhes da sua proposta, condições, data desejada, etc...'
                ).classes('w-full')
                
                with ui.row().classes('justify-end mt-4 gap-2'):
                    ui.button('Cancelar', on_click=dialog.close).props('flat')
                    ui.button('Enviar Proposta', 
                             on_click=lambda: self._criar_negociacao_do_anuncio(
                                 dialog, email_locatario, anuncio, valor_input, obs_input
                             )).props('color=primary')
        
        dialog.open()
    
    def _criar_negociacao_do_anuncio(self, dialog, email_locatario, anuncio, valor_input, obs_input):
        """Cria a negociação usando as informações do anúncio."""
        valor_proposto = valor_input.value or 0
        observacoes = obs_input.value or ""
        
        if valor_proposto <= 0:
            ui.notify('O valor da proposta deve ser maior que zero', type='warning')
            return
        
        sucesso, negociacao, mensagem = self._negociacao_service.criar_negociacao(
            locatario_email=email_locatario,
            proprietario_email=anuncio.proprietario_email,  # Obtido automaticamente do anúncio
            anuncio_id=anuncio.id,
            valor_proposto=valor_proposto,
            observacoes=observacoes
        )
        
        if sucesso:
            ui.notify(mensagem, type='positive')
            dialog.close()
            # Redireciona para a página de negociações
            ui.navigate.to('/negociacoes')
        else:
            ui.notify(mensagem, type='negative')
    
    def _abrir_dialogo_favoritar(self, email, anuncio):
        dialog = ui.dialog()
        with dialog:
            with ui.card().classes('p-4 w-96'):
                ui.label('Adicionar anotação (opcional)').classes('text-lg font-bold mb-2')
                anot_input = ui.textarea(placeholder='Insira sua anotação aqui...').classes('w-full')
                
                with ui.row().classes('justify-end mt-4'):
                    ui.button('Cancelar', on_click=dialog.close).props('flat')
                    ui.button('Salvar', 
                             on_click=lambda: self._salvar_favorito(dialog, email, anuncio, anot_input)).props('color=primary')
        
        dialog.open()
    
    def _salvar_favorito(self, dialog, email, anuncio, input_widget):
        anot = input_widget.value or ""
        if self._favorito_service.adicionar(email, anuncio, anot):
            ui.notify('Favorito adicionado', type='positive')
        else:
            ui.notify('Anúncio já está nos favoritos', type='warning')
        dialog.close()
