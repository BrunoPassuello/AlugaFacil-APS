from nicegui import ui, app
from datetime import date, time, datetime
from services.VisitaService import VisitaService
from services.NegociacaoService import NegociacaoService
from services.AnuncioService import AnuncioService
from entities.StatusVisita import StatusVisita
from entities.StatusNegociacao import StatusNegociacao

class VisitasUi:
    
    def __init__(self):
        self._visita_service = VisitaService()
        self._negociacao_service = NegociacaoService()
        self._anuncio_service = AnuncioService()
        
    def render(self):
        if 'usuario_logado' not in app.storage.user:
            ui.navigate.to('/login')
            return
        
        usuario = app.storage.user['usuario_logado']
        email = usuario['email']
        tipo = usuario.get('tipo', 'locatario')
        
        negociacao_id = app.storage.browser.get('negociacao_id')
        
        ui.query('body').style('background-color: #ffffff')
        
        with ui.header().classes('items-center justify-between'):
            ui.label('AlugaFácil').classes('text-xl font-bold text-primary')
            with ui.row():
                ui.button('Dashboard', on_click=lambda: ui.navigate.to('/dashboard')).props('flat')
                ui.button('Negociações', on_click=lambda: ui.navigate.to('/negociacoes')).props('flat')
                if tipo == 'locatario':
                    ui.button('Anúncios', on_click=lambda: ui.navigate.to('/anuncios')).props('flat')
        
        with ui.column().classes('w-full p-6'):
            ui.label('Minhas Visitas').classes('text-3xl font-bold mb-4 text-primary')
            
            if tipo == 'locatario':
                ui.label('Visitas que você agendou').classes('text-md text-gray-600 mb-4')
            else:
                ui.label('Visitas agendadas nos seus imóveis').classes('text-md text-gray-600 mb-4')
            
            if tipo == 'locatario':
                ui.button('Agendar Nova Visita', 
                         on_click=lambda: self._abrir_dialogo_agendar_visita(email, tipo)).props('color=primary').classes('mb-4')
            
            visitas = self._obter_visitas_usuario(email, tipo, negociacao_id)
            
            if not visitas:
                if tipo == 'locatario':
                    ui.label('Nenhuma visita agendada. Crie negociações e agende visitas!').classes('text-gray-600 italic')
                else:
                    ui.label('Nenhuma visita agendada nos seus imóveis.').classes('text-gray-600 italic')
            else:
                for visita in visitas:
                    self._render_card_visita(visita, tipo)
            
            if negociacao_id:
                ui.button('Voltar para Negociações', 
                         on_click=lambda: ui.navigate.to('/negociacoes')).classes('mt-8').props('color=primary outline')
            else:
                ui.button('Voltar ao Dashboard', 
                         on_click=lambda: ui.navigate.to('/dashboard')).classes('mt-8').props('color=primary outline')
    
    
    def _obter_visitas_usuario(self, email, tipo, negociacao_id=None):
        if negociacao_id:
            return self._visita_service.listar_por_negociacao(int(negociacao_id))
        
        if tipo == 'locatario':
            negociacoes = self._negociacao_service.listar_por_locatario(email)
        else:
            negociacoes = self._negociacao_service.listar_por_proprietario(email)
        
        visitas = []
        for negociacao in negociacoes:
            visitas.extend(self._visita_service.listar_por_negociacao(negociacao.id))
        
        return visitas
    
    def _render_card_visita(self, visita, tipo_usuario):
        negociacao = self._negociacao_service.get_por_id(visita.negociacao_id)
        
        anuncio = None
        if negociacao:
            anuncio = self._anuncio_service.get_por_id(negociacao.anuncio_id)
        
        with ui.card().classes('w-full mb-4 p-4'):
            with ui.row().classes('w-full justify-between items-start gap-4'):
                if anuncio and anuncio.imagem_url:
                    with ui.column().classes('flex-shrink-0'):
                        ui.image(anuncio.imagem_url).classes('w-40 h-32 object-cover rounded')
                
                with ui.column().classes('flex-grow'):
                    ui.label(f'Visita #{visita.id}').classes('text-xl font-bold text-primary')
                    ui.label(f'Status: {visita.status.value}').classes('text-md font-medium')
                    
                    ui.separator().classes('my-2')
                    
                    if anuncio:
                        with ui.card().classes('w-full p-3 bg-blue-50'):
                            ui.label('Informações do Imóvel').classes('text-sm font-bold text-blue-900 mb-2')
                            
                            ui.label(anuncio.titulo).classes('text-base font-semibold')
                            
                            with ui.row().classes('gap-4 mt-1'):
                                with ui.row().classes('items-center gap-1'):
                                    ui.icon('location_on', size='sm').classes('text-blue-600')
                                    ui.label(f'{anuncio.cidade} - {anuncio.endereco}').classes('text-sm')
                            
                            if anuncio.imovel:
                                with ui.row().classes('gap-4 mt-2'):
                                    with ui.row().classes('items-center gap-1'):
                                        ui.icon('bed', size='sm').classes('text-gray-600')
                                        ui.label(f'{anuncio.imovel.quartos} quartos').classes('text-xs')
                                    
                                    with ui.row().classes('items-center gap-1'):
                                        ui.icon('bathtub', size='sm').classes('text-gray-600')
                                        ui.label(f'{anuncio.imovel.banheiros} banheiros').classes('text-xs')
                                    
                                    with ui.row().classes('items-center gap-1'):
                                        ui.icon('straighten', size='sm').classes('text-gray-600')
                                        ui.label(f'{anuncio.imovel.metragem}m²').classes('text-xs')
                                    
                                    if anuncio.imovel.possui_garagem:
                                        with ui.row().classes('items-center gap-1'):
                                            ui.icon('garage', size='sm').classes('text-gray-600')
                                            ui.label('Garagem').classes('text-xs')
                                
                                # Badge do tipo de imóvel
                                with ui.row().classes('mt-2'):
                                    ui.badge(anuncio.imovel.tipo_imovel().capitalize()).classes('bg-blue-600')
                            
                            ui.label(f'Valor: R$ {anuncio.valor:.2f}/mês').classes('text-green-600 font-bold text-base mt-2')
                    else:
                        ui.label('Anúncio não encontrado').classes('text-orange-600 text-sm italic')
                    
                    ui.separator().classes('my-2')
                    
                    with ui.row().classes('gap-4'):
                        with ui.row().classes('items-center gap-1'):
                            ui.icon('event', size='sm').classes('text-gray-600')
                            ui.label(f'{visita.data_agendada.strftime("%d/%m/%Y")}').classes('text-sm font-medium')
                        
                        with ui.row().classes('items-center gap-1'):
                            ui.icon('schedule', size='sm').classes('text-gray-600')
                            ui.label(f'{visita.hora_agendada.strftime("%H:%M")}').classes('text-sm font-medium')
                    
                    if negociacao:
                        ui.label(f'Negociação: #{negociacao.id} ({negociacao.status.value})').classes('text-sm text-gray-600 mt-1')
                        
                        if tipo_usuario == 'locatario':
                            ui.label(f'Proprietário: {negociacao.proprietario_email}').classes('text-sm text-gray-600')
                        else:
                            ui.label(f'Locatário Interessado: {negociacao.locatario_email}').classes('text-sm text-gray-600')
                    
                    if visita.observacoes:
                        with ui.card().classes('w-full p-2 bg-yellow-50 mt-2'):
                            ui.label(f'📝 Observações: {visita.observacoes}').classes('text-xs text-gray-700')

                with ui.column().classes('gap-2 flex-shrink-0'):
                    if visita.status == StatusVisita.AGENDADA:
                        if tipo_usuario == 'locatario':
                            ui.button('Reagendar',
                                    on_click=lambda v=visita: self._abrir_dialogo_reagendar(v)).props('color=primary size=sm icon=edit_calendar')
                            ui.button('Cancelar',
                                    on_click=lambda v=visita: self._cancelar_visita(v.id)).props('color=negative size=sm icon=cancel')
                        
                        if tipo_usuario == 'proprietario':
                            ui.button('Realizada',
                                    on_click=lambda v=visita: self._realizar_visita(v.id)).props('color=positive size=sm icon=check_circle')
                            ui.button('Não Compareceu',
                                    on_click=lambda v=visita: self._registrar_nao_comparecimento(v.id)).props('color=warning size=sm icon=event_busy')
                    
                    elif visita.status == StatusVisita.REALIZADA:
                        with ui.card().classes('p-2 bg-green-100'):
                            ui.icon('check_circle', size='md').classes('text-green-600')
                            ui.label('Realizada').classes('text-green-700 font-bold text-sm')
                    
                    elif visita.status == StatusVisita.CANCELADA:
                        with ui.card().classes('p-2 bg-red-100'):
                            ui.icon('cancel', size='md').classes('text-red-600')
                            ui.label('Cancelada').classes('text-red-700 font-bold text-sm')
                    
                    elif visita.status == StatusVisita.NAO_COMPARECEU:
                        with ui.card().classes('p-2 bg-orange-100'):
                            ui.icon('event_busy', size='md').classes('text-orange-600')
                            ui.label('Não Compareceu').classes('text-orange-700 font-bold text-sm')

    
    def _abrir_dialogo_agendar_visita(self, email, tipo):
        if tipo != 'locatario':
            ui.notify('Apenas locatários podem agendar visitas', type='warning')
            return
        
        negociacoes = self._negociacao_service.listar_por_locatario(email)
        
        negociacoes_disponiveis = [
            n for n in negociacoes 
            if n.status in [StatusNegociacao.INICIADA, StatusNegociacao.APROVADA]
        ]
        
        if not negociacoes_disponiveis:
            ui.notify('Você não possui negociações ativas para agendar visitas', type='warning')
            return
        
        dialog = ui.dialog()
        with dialog:
            with ui.card().classes('p-6 w-full max-w-lg'):
                ui.label('Agendar Nova Visita').classes('text-2xl font-bold mb-4')
                
                options_dict = {}
                for n in negociacoes_disponiveis:
                    valor_display = n.valor_final if n.status == StatusNegociacao.APROVADA else n.valor_proposto
                    status_text = n.status.value
                    options_dict[n.id] = f'Negociação #{n.id} ({status_text}) - R$ {valor_display:.2f}'
                
                negociacao_select = ui.select(
                    label='Selecione a Negociação',
                    options=options_dict,
                    with_input=True
                ).classes('w-full')
                
                ui.label('Você pode agendar visitas mesmo antes da aprovação do proprietário').classes('text-xs text-gray-500 italic mb-2')
                
                with ui.input('Data da Visita').props('type=date') as data_input:
                    data_input.value = date.today().isoformat()
                data_input.classes('w-full')
                
                with ui.input('Horário').props('type=time') as hora_input:
                    hora_input.value = '10:00'
                hora_input.classes('w-full')
                
                obs_input = ui.textarea(
                    label='Observações (opcional)',
                    placeholder='Informações adicionais sobre a visita...'
                ).classes('w-full')
                
                with ui.row().classes('justify-end mt-4 gap-2'):
                    ui.button('Cancelar', on_click=dialog.close).props('flat')
                    ui.button('Agendar Visita', 
                            on_click=lambda: self._agendar_visita(
                                dialog, negociacao_select, data_input, 
                                hora_input, obs_input
                            )).props('color=primary')
        
        dialog.open()
    
    def _agendar_visita(self, dialog, negociacao_select, data_input, hora_input, obs_input):
        negociacao_id = negociacao_select.value
        data_str = data_input.value
        hora_str = hora_input.value
        observacoes = obs_input.value or ""
        
        if not negociacao_id or not data_str or not hora_str:
            ui.notify('Preencha todos os campos obrigatórios', type='warning')
            return
        
        data_agendada = datetime.strptime(data_str, '%Y-%m-%d').date()
        hora_agendada = datetime.strptime(hora_str, '%H:%M').time()
        
        sucesso, visita, mensagem = self._visita_service.agendar_visita(
            negociacao_id=negociacao_id,
            data_agendada=data_agendada,
            hora_agendada=hora_agendada,
            observacoes=observacoes
        )
        
        if sucesso:
            ui.notify(mensagem, type='positive')
            dialog.close()
            ui.navigate.reload()
        else:
            ui.notify(mensagem, type='negative')
    
    def _abrir_dialogo_reagendar(self, visita):
        dialog = ui.dialog()
        with dialog:
            with ui.card().classes('p-6 w-full max-w-lg'):
                ui.label('Reagendar Visita').classes('text-2xl font-bold mb-4')
                ui.label(f'Visita #{visita.id}').classes('mb-2')
                
                with ui.input('Nova Data').props('type=date') as data_input:
                    data_input.value = visita.data_agendada.isoformat()
                data_input.classes('w-full')
                
                with ui.input('Novo Horário').props('type=time') as hora_input:
                    hora_input.value = visita.hora_agendada.strftime('%H:%M')
                hora_input.classes('w-full')
                
                with ui.row().classes('justify-end mt-4 gap-2'):
                    ui.button('Cancelar', on_click=dialog.close).props('flat')
                    ui.button('Reagendar', 
                            on_click=lambda: self._reagendar_visita(
                                dialog, visita.id, data_input, hora_input
                            )).props('color=primary')
        
        dialog.open()
    
    def _reagendar_visita(self, dialog, visita_id, data_input, hora_input):
        data_str = data_input.value
        hora_str = hora_input.value
        
        if not data_str or not hora_str:
            ui.notify('Preencha todos os campos', type='warning')
            return
        
        nova_data = datetime.strptime(data_str, '%Y-%m-%d').date()
        nova_hora = datetime.strptime(hora_str, '%H:%M').time()
        
        sucesso, mensagem = self._visita_service.reagendar_visita(visita_id, nova_data, nova_hora)
        
        if sucesso:
            ui.notify(mensagem, type='positive')
            dialog.close()
            ui.navigate.reload()
        else:
            ui.notify(mensagem, type='negative')
    
    def _cancelar_visita(self, visita_id):
        sucesso, mensagem = self._visita_service.cancelar_visita(visita_id)
        
        if sucesso:
            ui.notify(mensagem, type='positive')
            ui.navigate.reload()
        else:
            ui.notify(mensagem, type='negative')
    
    def _realizar_visita(self, visita_id):
        sucesso, mensagem = self._visita_service.realizar_visita(visita_id)
        
        if sucesso:
            ui.notify(mensagem, type='positive')
            ui.navigate.reload()
        else:
            ui.notify(mensagem, type='negative')
    
    def _registrar_nao_comparecimento(self, visita_id):
        sucesso, mensagem = self._visita_service.registrar_nao_comparecimento(visita_id)
        
        if sucesso:
            ui.notify(mensagem, type='positive')
            ui.navigate.reload()
        else:
            ui.notify(mensagem, type='negative')
