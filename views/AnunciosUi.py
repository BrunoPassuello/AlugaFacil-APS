# AnunciosUi.py
from nicegui import ui, app
from services.AnuncioService import AnuncioService
from services.FavoritoService import FavoritoService
from services.NegociacaoService import NegociacaoService
from typing import List

class AnunciosUi:

    def __init__(self):
        self._anuncio_service = AnuncioService()
        self._favorito_service = FavoritoService()
        self._negociacao_service = NegociacaoService()
        
        self.input_cidade = None
        self.input_valor_min = None
        self.input_valor_max = None
        self.select_quartos = None
        self.select_banheiros = None
        self.checkbox_garagem = None
        self.select_tipo_imovel = None
        self.container_anuncios = None

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
            
            self._render_filtros()
            
            self.container_anuncios = ui.column().classes('w-full mt-6')
            
            self._exibir_anuncios(usuario['email'], tipo)

            ui.button('Voltar ao Dashboard',
                      on_click=lambda: ui.navigate.to('/dashboard')).classes('mt-8').props('color=primary outline')

    def _render_filtros(self):
        with ui.expansion('Filtros de Busca', icon='filter_alt').classes('w-full mb-4').props('dense'):
            with ui.card().classes('w-full p-4'):
                with ui.grid(columns=3).classes('w-full gap-4'):
                    with ui.column():
                        ui.label('Cidade:').classes('text-sm font-semibold')
                        self.input_cidade = ui.input(
                            placeholder='Ex: Florianópolis'
                        ).classes('w-full')
                    
                    with ui.column():
                        ui.label('Tipo de Imóvel:').classes('text-sm font-semibold')
                        self.select_tipo_imovel = ui.select(
                            options=['Todos', 'apartamento', 'casa'],
                            value='Todos'
                        ).classes('w-full')
                    
                    with ui.column():
                        ui.label('Quartos:').classes('text-sm font-semibold')
                        self.select_quartos = ui.select(
                            options=['Todos', '1+', '2+', '3+', '4+'],
                            value='Todos'
                        ).classes('w-full')
                
                with ui.grid(columns=3).classes('w-full gap-4 mt-3'):
                    with ui.column():
                        ui.label('Banheiros:').classes('text-sm font-semibold')
                        self.select_banheiros = ui.select(
                            options=['Todos', '1+', '2+', '3+'],
                            value='Todos'
                        ).classes('w-full')
                    
                    with ui.column():
                        ui.label('Valor Mínimo (R$):').classes('text-sm font-semibold')
                        self.input_valor_min = ui.number(
                            placeholder='0.00',
                            format='%.2f',
                            min=0
                        ).classes('w-full')
                    
                    with ui.column():
                        ui.label('Valor Máximo (R$):').classes('text-sm font-semibold')
                        self.input_valor_max = ui.number(
                            placeholder='10000.00',
                            format='%.2f',
                            min=0
                        ).classes('w-full')
                
                with ui.row().classes('mt-3'):
                    self.checkbox_garagem = ui.checkbox('Apenas imóveis com garagem')
                
                with ui.row().classes('mt-4 gap-2'):
                    ui.button('Buscar', on_click=self._aplicar_busca).props('color=primary icon=search')
                    ui.button('Limpar Filtros', on_click=self._limpar_filtros).props('outline icon=clear')

    def _aplicar_busca(self):
        usuario = app.storage.user['usuario_logado']
        tipo = usuario.get('tipo', 'locatario')
        self._exibir_anuncios(usuario['email'], tipo)

    def _limpar_filtros(self):
        if self.input_cidade:
            self.input_cidade.value = ''
        if self.input_valor_min:
            self.input_valor_min.value = None
        if self.input_valor_max:
            self.input_valor_max.value = None
        if self.select_quartos:
            self.select_quartos.value = 'Todos'
        if self.select_banheiros:
            self.select_banheiros.value = 'Todos'
        if self.checkbox_garagem:
            self.checkbox_garagem.value = False
        if self.select_tipo_imovel:
            self.select_tipo_imovel.value = 'Todos'
        
        usuario = app.storage.user['usuario_logado']
        tipo = usuario.get('tipo', 'locatario')
        self._exibir_anuncios(usuario['email'], tipo)

    def _exibir_anuncios(self, email_usuario, tipo_usuario):
        todos_anuncios = self._anuncio_service.listar()
        
        anuncios_filtrados = self._aplicar_filtros(todos_anuncios)
        
        self.container_anuncios.clear()
        
        with self.container_anuncios:
            ui.label(f'{len(anuncios_filtrados)} anúncio(s) encontrado(s)').classes(
                'text-lg font-semibold mb-4 text-gray-700'
            )
            
            if not anuncios_filtrados:
                ui.label('Nenhum anúncio encontrado com os filtros selecionados.').classes(
                    'text-gray-600 italic'
                )
            else:
                for anuncio in anuncios_filtrados:
                    self._render_card(anuncio, email_usuario, tipo_usuario)

    def _aplicar_filtros(self, anuncios: List) -> List:
        filtrados = anuncios
        
        if self.input_cidade and self.input_cidade.value:
            cidade_busca = self.input_cidade.value.lower().strip()
            filtrados = [
                a for a in filtrados 
                if cidade_busca in a.cidade.lower()
            ]
        
        if self.select_tipo_imovel and self.select_tipo_imovel.value != 'Todos':
            tipo_selecionado = self.select_tipo_imovel.value
            filtrados = [
                a for a in filtrados 
                if a.imovel and a.imovel.tipo_imovel() == tipo_selecionado
            ]
        
        if self.input_valor_min and self.input_valor_min.value is not None:
            valor_min = float(self.input_valor_min.value)
            filtrados = [a for a in filtrados if a.valor >= valor_min]
        
        if self.input_valor_max and self.input_valor_max.value is not None:
            valor_max = float(self.input_valor_max.value)
            filtrados = [a for a in filtrados if a.valor <= valor_max]
        
        if self.select_quartos and self.select_quartos.value != 'Todos':
            quartos_min = int(self.select_quartos.value.replace('+', ''))
            filtrados = [
                a for a in filtrados 
                if a.imovel and a.imovel.quartos >= quartos_min
            ]
        
        if self.select_banheiros and self.select_banheiros.value != 'Todos':
            banheiros_min = int(self.select_banheiros.value.replace('+', ''))
            filtrados = [
                a for a in filtrados 
                if a.imovel and a.imovel.banheiros >= banheiros_min
            ]
        
        if self.checkbox_garagem and self.checkbox_garagem.value:
            filtrados = [
                a for a in filtrados 
                if a.imovel and a.imovel.possui_garagem
            ]
        
        return filtrados

    def _render_card(self, anuncio, email_usuario, tipo_usuario):
        with ui.card().classes('w-full mb-4 flex items-center p-0 hover:shadow-lg transition-shadow'):
            ui.image(anuncio.imagem_url).classes('w-64 h-48 object-cover rounded mx-auto')

            with ui.column().classes('p-4 w-full'):
                ui.label(anuncio.titulo).classes('text-lg font-bold text-primary')
                ui.label(f'Adicionado em {anuncio.data_postagem.strftime("%d/%m/%Y")}').classes('text-sm text-gray-600')
                
                if anuncio.imovel:
                    with ui.row().classes('gap-4 mt-2'):
                        with ui.row().classes('items-center gap-1'):
                            ui.icon('location_on', size='sm').classes('text-gray-600')
                            ui.label(f'{anuncio.cidade}').classes('text-sm')
                        
                        with ui.row().classes('items-center gap-1'):
                            ui.icon('bed', size='sm').classes('text-gray-600')
                            ui.label(f'{anuncio.imovel.quartos} quartos').classes('text-sm')
                        
                        with ui.row().classes('items-center gap-1'):
                            ui.icon('bathtub', size='sm').classes('text-gray-600')
                            ui.label(f'{anuncio.imovel.banheiros} banheiros').classes('text-sm')
                        
                        if anuncio.imovel.possui_garagem:
                            with ui.row().classes('items-center gap-1'):
                                ui.icon('garage', size='sm').classes('text-gray-600')
                                ui.label('Garagem').classes('text-sm')
                    
                    with ui.row().classes('mt-2 gap-2'):
                        ui.badge(anuncio.imovel.tipo_imovel().capitalize()).classes('bg-blue-500')
                        ui.label(f'{anuncio.imovel.metragem}m²').classes('text-sm text-gray-600')
                
                ui.label(f'Valor: R${anuncio.valor:.2f}').classes('text-green-600 font-medium text-xl mt-2')

                with ui.row().classes('mt-2 gap-2'):
                    if tipo_usuario == 'locatario':
                        ui.button('FAZER PROPOSTA',
                                  on_click=lambda a=anuncio: self._abrir_dialogo_fazer_proposta(email_usuario, a)).props('color=primary')
                        ui.button('FAVORITAR',
                                  on_click=lambda a=anuncio: self._abrir_dialogo_favoritar(email_usuario, a)).props('outline')
                    else:
                        ui.label('(Proprietário - visualização apenas)').classes('text-gray-500 italic')

    def _abrir_dialogo_fazer_proposta(self, email_locatario, anuncio):
        dialog = ui.dialog()
        with dialog:
            with ui.card().classes('p-6 w-full max-w-lg'):
                ui.label('Fazer Proposta de Aluguel').classes('text-2xl font-bold mb-4')

                with ui.card().classes('w-full p-4 bg-gray-100 mb-4'):
                    ui.label(f'Anúncio: {anuncio.titulo}').classes('font-bold')
                    ui.label(f'Endereço: {anuncio.endereco}').classes('text-sm')
                    ui.label(f'Cidade: {anuncio.cidade}').classes('text-sm')
                    ui.label(f'Valor Anunciado: R$ {anuncio.valor:.2f}').classes('text-green-600 font-medium')
                    ui.label(f'Proprietário: {anuncio.proprietario_email}').classes('text-sm text-gray-600')

                valor_input = ui.number(
                    label='Valor da Proposta (R$)',
                    min=0.01,
                    step=0.01,
                    value=anuncio.valor,  
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
        valor_proposto = valor_input.value or 0
        observacoes = obs_input.value or ""

        if valor_proposto <= 0:
            ui.notify('O valor da proposta deve ser maior que zero', type='warning')
            return

        sucesso, negociacao, mensagem = self._negociacao_service.criar_negociacao(
            locatario_email=email_locatario,
            proprietario_email=anuncio.proprietario_email,  
            anuncio_id=anuncio.id,
            valor_proposto=valor_proposto,
            observacoes=observacoes
        )

        if sucesso:
            ui.notify(mensagem, type='positive')
            dialog.close()
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
