from nicegui import ui, app
from datetime import date
from services.NegociacaoService import NegociacaoService
from services.AnuncioService import AnuncioService
from entities.StatusNegociacao import StatusNegociacao

class NegociacoesUi:
    """Interface para gerenciar negociações entre locatários e proprietários."""
    
    def __init__(self):
        self._negociacao_service = NegociacaoService()
        self._anuncio_service = AnuncioService()
    
    # ---------------- RENDER -----------------
    
    def render(self):
        if 'usuario_logado' not in app.storage.user:
            ui.navigate.to('/login')
            return
        
        usuario = app.storage.user['usuario_logado']
        email = usuario['email']
        tipo = usuario.get('tipo', 'locatario')
        
        ui.query('body').style('background-color: #ffffff')
        
        with ui.header().classes('items-center justify-between'):
            ui.label('AlugaFácil').classes('text-xl font-bold text-primary')
            with ui.row():
                ui.button('Dashboard', on_click=lambda: ui.navigate.to('/dashboard')).props('flat')
                ui.button('Anúncios', on_click=lambda: ui.navigate.to('/anuncios')).props('flat')
                if tipo == 'locatario':
                    ui.button('Visitas', on_click=lambda: ui.navigate.to('/visitas')).props('flat')
        
        with ui.column().classes('w-full p-6'):
            ui.label('Minhas Negociações').classes('text-3xl font-bold mb-4 text-primary')
            
            # Botão para criar nova negociação (apenas locatários) - mantido como alternativa
            if tipo == 'locatario':
                ui.button('Criar Nova Negociação (Manual)', 
                        on_click=lambda: self._abrir_dialogo_criar_negociacao(email)).props('color=primary outline').classes('mb-4')
                ui.label('Dica: Você pode fazer propostas diretamente pelos anúncios!').classes('text-sm text-gray-600 italic mb-4')
            
            # Lista negociações baseado no tipo de usuário
            if tipo == 'locatario':
                negociacoes = self._negociacao_service.listar_por_locatario(email)
            else:
                negociacoes = self._negociacao_service.listar_por_proprietario(email)
            
            if not negociacoes:
                if tipo == 'locatario':
                    ui.label('Nenhuma negociação encontrada. Visite a página de Anúncios para fazer propostas!').classes('text-gray-600 italic')
                else:
                    ui.label('Nenhuma negociação encontrada. Aguarde propostas dos locatários.').classes('text-gray-600 italic')
            else:
                for negociacao in negociacoes:
                    self._render_card_negociacao(negociacao, email, tipo)
            
            # Botão voltar
            ui.button('Voltar ao Dashboard', 
                    on_click=lambda: ui.navigate.to('/dashboard')).classes('mt-8').props('color=primary outline')
    
    # ---------------- PRIVADOS ---------------
    
    def _render_card_negociacao(self, negociacao, email_usuario, tipo_usuario):
        with ui.card().classes('w-full mb-4 p-4'):
            with ui.row().classes('w-full justify-between items-start'):
                with ui.column().classes('flex-grow'):
                    ui.label(f'Negociação #{negociacao.id}').classes('text-xl font-bold text-primary')
                    ui.label(f'Status: {negociacao.status.value}').classes('text-md font-medium')
                    ui.label(f'Data Início: {negociacao.data_inicio.strftime("%d/%m/%Y")}').classes('text-sm text-gray-600')
                    
                    if negociacao.data_fim:
                        ui.label(f'Data Fim: {negociacao.data_fim.strftime("%d/%m/%Y")}').classes('text-sm text-gray-600')
                    
                    ui.label(f'Valor Proposto: R$ {negociacao.valor_proposto:.2f}').classes('text-green-600 font-medium')
                    
                    if negociacao.valor_final > 0:
                        ui.label(f'Valor Final: R$ {negociacao.valor_final:.2f}').classes('text-green-700 font-bold')
                    
                    if negociacao.observacoes:
                        ui.label(f'Observações: {negociacao.observacoes}').classes('text-sm text-gray-700 mt-2')
                    
                    # Informações de contato
                    if tipo_usuario == 'locatario':
                        ui.label(f'Proprietário: {negociacao.proprietario_email}').classes('text-sm text-gray-600')
                    else:
                        ui.label(f'Locatário: {negociacao.locatario_email}').classes('text-sm text-gray-600')
                
                # Botões de ação
                with ui.column().classes('gap-2'):
                    if negociacao.status == StatusNegociacao.INICIADA and tipo_usuario == 'proprietario':
                        ui.button('Aprovar', 
                                on_click=lambda n=negociacao: self._abrir_dialogo_aprovar(n)).props('color=positive size=sm')
                        ui.button('Cancelar', 
                                on_click=lambda n=negociacao: self._cancelar_negociacao(n.id)).props('color=negative size=sm')
                    
                    elif negociacao.status == StatusNegociacao.APROVADA:
                        ui.button('Finalizar', 
                                on_click=lambda n=negociacao: self._finalizar_negociacao(n.id)).props('color=primary size=sm')
                        ui.button('Ver Visitas', 
                                on_click=lambda n=negociacao: ui.navigate.to(f'/visitas?negociacao_id={n.id}')).props('color=primary outline size=sm')
                    
                    elif negociacao.status == StatusNegociacao.CANCELADA:
                        ui.label('Cancelada').classes('text-red-600 font-bold')
                    
                    elif negociacao.status == StatusNegociacao.FINALIZADA:
                        ui.label('Finalizada').classes('text-blue-600 font-bold')
                        if tipo_usuario == 'proprietario' and negociacao.avaliacao_locatario == 0:
                            ui.button('Avaliar Locatário', 
                                    on_click=lambda n=negociacao: self._abrir_dialogo_avaliar_locatario(n)).props('color=warning size=sm')
                        if tipo_usuario == 'locatario' and negociacao.avaliacao_proprietario == 0:
                            ui.button('Avaliar Proprietário', 
                                    on_click=lambda n=negociacao: self._abrir_dialogo_avaliar_proprietario(n)).props('color=warning size=sm')
    
    def _abrir_dialogo_criar_negociacao(self, email_locatario):
        dialog = ui.dialog()
        with dialog:
            with ui.card().classes('p-6 w-full max-w-lg'):
                ui.label('Criar Nova Negociação').classes('text-2xl font-bold mb-4')
                
                anuncios = self._anuncio_service.listar()
                if not anuncios:
                    ui.label('Nenhum anúncio disponível').classes('text-gray-600')
                    ui.button('Fechar', on_click=dialog.close).props('flat')
                    dialog.open()
                    return
                
                anuncio_select = ui.select(
                    label='Selecione o Anúncio',
                    options={a.id: f'{a.titulo} - R$ {a.valor:.2f}' for a in anuncios},
                    with_input=True
                ).classes('w-full')
                
                proprietario_input = ui.input(
                    label='E-mail do Proprietário',
                    placeholder='proprietario@email.com'
                ).classes('w-full')
                
                valor_input = ui.number(
                    label='Valor Proposto (R$)',
                    min=0.01,
                    step=0.01,
                    format='%.2f'
                ).classes('w-full')
                
                obs_input = ui.textarea(
                    label='Observações (opcional)',
                    placeholder='Detalhes da proposta...'
                ).classes('w-full')
                
                with ui.row().classes('justify-end mt-4 gap-2'):
                    ui.button('Cancelar', on_click=dialog.close).props('flat')
                    ui.button('Criar Negociação', 
                            on_click=lambda: self._criar_negociacao(
                                dialog, email_locatario, proprietario_input, 
                                anuncio_select, valor_input, obs_input
                            )).props('color=primary')
        
        dialog.open()
    
    def _criar_negociacao(self, dialog, email_locatario, proprietario_input, anuncio_select, valor_input, obs_input):
        proprietario_email = proprietario_input.value
        anuncio_id = anuncio_select.value
        valor_proposto = valor_input.value or 0
        observacoes = obs_input.value or ""
        
        if not proprietario_email or not anuncio_id or valor_proposto <= 0:
            ui.notify('Preencha todos os campos obrigatórios', type='warning')
            return
        
        sucesso, negociacao, mensagem = self._negociacao_service.criar_negociacao(
            locatario_email=email_locatario,
            proprietario_email=proprietario_email,
            anuncio_id=anuncio_id,
            valor_proposto=valor_proposto,
            observacoes=observacoes
        )
        
        if sucesso:
            ui.notify(mensagem, type='positive')
            dialog.close()
            ui.navigate.reload()
        else:
            ui.notify(mensagem, type='negative')
    
    def _abrir_dialogo_aprovar(self, negociacao):
        dialog = ui.dialog()
        with dialog:
            with ui.card().classes('p-6 w-96'):
                ui.label('Aprovar Negociação').classes('text-xl font-bold mb-4')
                ui.label(f'Valor Proposto: R$ {negociacao.valor_proposto:.2f}').classes('mb-2')
                
                valor_input = ui.number(
                    label='Valor Final (R$)',
                    min=0.01,
                    step=0.01,
                    value=negociacao.valor_proposto,
                    format='%.2f'
                ).classes('w-full')
                
                with ui.row().classes('justify-end mt-4 gap-2'):
                    ui.button('Cancelar', on_click=dialog.close).props('flat')
                    ui.button('Aprovar', 
                            on_click=lambda: self._aprovar_negociacao(dialog, negociacao.id, valor_input)).props('color=positive')
        
        dialog.open()
    
    def _aprovar_negociacao(self, dialog, negociacao_id, valor_input):
        valor_final = valor_input.value or 0
        
        if valor_final <= 0:
            ui.notify('Valor final deve ser maior que zero', type='warning')
            return
        
        sucesso, mensagem = self._negociacao_service.aprovar_negociacao(negociacao_id, valor_final)
        
        if sucesso:
            ui.notify(mensagem, type='positive')
            dialog.close()
            ui.navigate.reload()
        else:
            ui.notify(mensagem, type='negative')
    
    def _cancelar_negociacao(self, negociacao_id):
        sucesso, mensagem = self._negociacao_service.cancelar_negociacao(negociacao_id)
        
        if sucesso:
            ui.notify(mensagem, type='positive')
            ui.navigate.reload()
        else:
            ui.notify(mensagem, type='negative')
    
    def _finalizar_negociacao(self, negociacao_id):
        sucesso, mensagem = self._negociacao_service.finalizar_negociacao(negociacao_id)
        
        if sucesso:
            ui.notify(mensagem, type='positive')
            ui.navigate.reload()
        else:
            ui.notify(mensagem, type='negative')
    
    def _abrir_dialogo_avaliar_locatario(self, negociacao):
        dialog = ui.dialog()
        with dialog:
            with ui.card().classes('p-6 w-96'):
                ui.label('Avaliar Locatário').classes('text-xl font-bold mb-4')
                
                nota_input = ui.number(
                    label='Nota (0-5)',
                    min=0,
                    max=5,
                    step=0.5,
                    value=0,
                    format='%.1f'
                ).classes('w-full')
                
                with ui.row().classes('justify-end mt-4 gap-2'):
                    ui.button('Cancelar', on_click=dialog.close).props('flat')
                    ui.button('Avaliar', 
                            on_click=lambda: self._avaliar_locatario(dialog, negociacao.id, nota_input)).props('color=primary')
        
        dialog.open()
    
    def _avaliar_locatario(self, dialog, negociacao_id, nota_input):
        nota = nota_input.value or 0
        sucesso, mensagem = self._negociacao_service.avaliar_locatario(negociacao_id, nota)
        
        if sucesso:
            ui.notify(mensagem, type='positive')
            dialog.close()
            ui.navigate.reload()
        else:
            ui.notify(mensagem, type='negative')
    
    def _abrir_dialogo_avaliar_proprietario(self, negociacao):
        dialog = ui.dialog()
        with dialog:
            with ui.card().classes('p-6 w-96'):
                ui.label('Avaliar Proprietário').classes('text-xl font-bold mb-4')
                
                nota_input = ui.number(
                    label='Nota (0-5)',
                    min=0,
                    max=5,
                    step=0.5,
                    value=0,
                    format='%.1f'
                ).classes('w-full')
                
                with ui.row().classes('justify-end mt-4 gap-2'):
                    ui.button('Cancelar', on_click=dialog.close).props('flat')
                    ui.button('Avaliar', 
                            on_click=lambda: self._avaliar_proprietario(dialog, negociacao.id, nota_input)).props('color=primary')
        
        dialog.open()
    
    def _avaliar_proprietario(self, dialog, negociacao_id, nota_input):
        nota = nota_input.value or 0
        sucesso, mensagem = self._negociacao_service.avaliar_proprietario(negociacao_id, nota)
        
        if sucesso:
            ui.notify(mensagem, type='positive')
            dialog.close()
            ui.navigate.reload()
        else:
            ui.notify(mensagem, type='negative')
