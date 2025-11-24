# NegociacoesUi.py - VERSÃO MELHORADA COM VISUAL DE VISITAS
from nicegui import ui, app
from datetime import date
from services.NegociacaoService import NegociacaoService
from services.AnuncioService import AnuncioService
from repository.CadastroRepositoryPickle import CadastroRepositoryPickle
from entities.StatusNegociacao import StatusNegociacao

class NegociacoesUi:

    def __init__(self):
        self._negociacao_service = NegociacaoService()
        self._anuncio_service = AnuncioService()
        self._cadastro_repo = CadastroRepositoryPickle()

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

            if tipo == 'locatario':
                ui.button('Criar Nova Negociação (Manual)',
                          on_click=lambda: self._abrir_dialogo_criar_negociacao(email)).props('color=primary outline').classes('mb-4')
                ui.label('Dica: Você pode fazer propostas diretamente pelos anúncios!').classes('text-sm text-gray-600 italic mb-4')

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

            ui.button('Voltar ao Dashboard',
                      on_click=lambda: ui.navigate.to('/dashboard')).classes('mt-8').props('color=primary outline')

    def _render_card_negociacao(self, negociacao, email_usuario, tipo_usuario):
        anuncio = self._anuncio_service.get_por_id(negociacao.anuncio_id)
        
        with ui.card().classes('w-full mb-4 p-4'):
            with ui.row().classes('w-full justify-between items-start gap-4'):
                if anuncio and anuncio.imagem_url:
                    with ui.column().classes('flex-shrink-0'):
                        ui.image(anuncio.imagem_url).classes('w-48 h-40 object-cover rounded')
                
                with ui.column().classes('flex-grow'):
                    ui.label(f'Negociação #{negociacao.id}').classes('text-xl font-bold text-primary')
                    
                    status_color = {
                        StatusNegociacao.INICIADA: 'bg-blue-500',
                        StatusNegociacao.APROVADA: 'bg-green-500',
                        StatusNegociacao.CANCELADA: 'bg-red-500',
                        StatusNegociacao.FINALIZADA: 'bg-gray-500'
                    }
                    ui.badge(negociacao.status.value.upper()).classes(f'{status_color.get(negociacao.status, "bg-gray-500")} text-white')
                    
                    ui.separator().classes('my-2')
                    
                    if anuncio:
                        with ui.card().classes('w-full p-3 bg-blue-50'):
                            ui.label('🏠 Informações do Imóvel').classes('text-sm font-bold text-blue-900 mb-2')
                            
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
                                
                                with ui.row().classes('mt-2'):
                                    ui.badge(anuncio.imovel.tipo_imovel().capitalize()).classes('bg-blue-600')
                            
                            ui.label(f'Valor Anúncio: R$ {anuncio.valor:.2f}/mês').classes('text-green-600 font-bold text-sm mt-2')
                    else:
                        ui.label('Anúncio não encontrado').classes('text-orange-600 text-sm italic')
                    
                    ui.separator().classes('my-2')
                    
                    # Informações da Negociação
                    with ui.row().classes('gap-4'):
                        with ui.row().classes('items-center gap-1'):
                            ui.icon('event', size='sm').classes('text-gray-600')
                            ui.label(f'Início: {negociacao.data_inicio.strftime("%d/%m/%Y")}').classes('text-sm')
                        
                        if negociacao.data_fim:
                            with ui.row().classes('items-center gap-1'):
                                ui.icon('event_available', size='sm').classes('text-gray-600')
                                ui.label(f'Fim: {negociacao.data_fim.strftime("%d/%m/%Y")}').classes('text-sm')
                    
                    # Valores
                    with ui.row().classes('gap-4 mt-2'):
                        ui.label(f'Valor Proposto: R$ {negociacao.valor_proposto:.2f}').classes('text-green-600 font-medium')
                        
                        if negociacao.valor_final > 0:
                            ui.label(f'Valor Final: R$ {negociacao.valor_final:.2f}').classes('text-green-700 font-bold')
                    
                    # Informações de contato
                    if tipo_usuario == 'locatario':
                        ui.label(f'Proprietário: {negociacao.proprietario_email}').classes('text-sm text-gray-600 mt-1')
                    else:
                        ui.label(f'Locatário Interessado: {negociacao.locatario_email}').classes('text-sm text-gray-600 mt-1')
                    
                    # Observações
                    if negociacao.observacoes:
                        with ui.card().classes('w-full p-2 bg-yellow-50 mt-2'):
                            ui.label(f'Observações: {negociacao.observacoes}').classes('text-xs text-gray-700')

                # Coluna da direita - Botões de ação
                with ui.column().classes('gap-2 flex-shrink-0'):
                    if tipo_usuario == 'proprietario':
                        ui.button('Ver Perfil do Locatário',
                                  on_click=lambda n=negociacao: self._abrir_perfil_locatario(n.locatario_email)
                                  ).props('color=info outline size=sm icon=person')
                    
                    ui.button('Ver Visitas',
                              on_click=lambda n=negociacao: self._ver_visitas_negociacao(n.id)
                              ).props('color=secondary outline size=sm icon=event')
                    
                    if negociacao.status == StatusNegociacao.INICIADA and tipo_usuario == 'proprietario':
                        ui.button('Aprovar',
                                  on_click=lambda n=negociacao: self._abrir_dialogo_aprovar(n)).props('color=positive size=sm icon=check')
                        ui.button('Cancelar',
                                  on_click=lambda n=negociacao: self._cancelar_negociacao(n.id)).props('color=negative size=sm icon=close')
                    
                    elif negociacao.status == StatusNegociacao.APROVADA:
                        ui.button('Finalizar',
                                  on_click=lambda n=negociacao: self._finalizar_negociacao(n.id)).props('color=primary size=sm icon=done_all')
                    
                    elif negociacao.status == StatusNegociacao.FINALIZADA:
                        if tipo_usuario == 'proprietario' and negociacao.avaliacao_locatario == 0:
                            ui.button('Avaliar Locatário',
                                      on_click=lambda n=negociacao: self._abrir_dialogo_avaliar_locatario(n)).props('color=warning size=sm icon=star')
                        
                        if tipo_usuario == 'locatario' and negociacao.avaliacao_proprietario == 0:
                            ui.button('Avaliar Proprietário',
                                      on_click=lambda n=negociacao: self._abrir_dialogo_avaliar_proprietario(n)).props('color=warning size=sm icon=star')

    def _ver_visitas_negociacao(self, negociacao_id):
        ui.navigate.to(f'/visitas?negociacao_id={negociacao_id}')

    def _abrir_perfil_locatario(self, email_locatario):
        locatario = self._cadastro_repo.get_pessoa_email(email_locatario)
        
        if not locatario:
            ui.notify('Locatário não encontrado', type='negative')
            return
        
        dialog = ui.dialog()
        with dialog:
            with ui.card().classes('p-6 w-full max-w-3xl'):
                with ui.row().classes('w-full justify-between items-center mb-4'):
                    ui.label('Perfil do Locatário Interessado').classes('text-2xl font-bold text-primary')
                    ui.icon('person', size='lg').classes('text-primary')
                
                ui.separator()
                
                with ui.card().classes('w-full p-4 mb-4 bg-gray-50'):
                    ui.label('Informações Pessoais').classes('text-lg font-bold mb-3')
                    
                    with ui.grid(columns=2).classes('w-full gap-4'):
                        with ui.column():
                            ui.label('Nome Completo:').classes('text-sm font-semibold text-gray-600')
                            ui.label(locatario.nome).classes('text-base')
                        
                        with ui.column():
                            ui.label('E-mail:').classes('text-sm font-semibold text-gray-600')
                            ui.label(locatario.email).classes('text-base')
                        
                        with ui.column():
                            ui.label('Telefone:').classes('text-sm font-semibold text-gray-600')
                            telefone_status = "✓ Verificado" if locatario.telefone_verificado else "✗ Não Verificado"
                            ui.label(f'{locatario.telefone} ({telefone_status})').classes('text-base')
                        
                        with ui.column():
                            ui.label('CPF:').classes('text-sm font-semibold text-gray-600')
                            ui.label(locatario.cpf).classes('text-base')
                        
                        with ui.column():
                            ui.label('Data de Nascimento:').classes('text-sm font-semibold text-gray-600')
                            ui.label(locatario.data_nascimento).classes('text-base')
                        
                        with ui.column():
                            ui.label('Profissão:').classes('text-sm font-semibold text-gray-600')
                            ui.label(locatario.profissao_str or 'Não informado').classes('text-base')
                
                with ui.card().classes('w-full p-4 mb-4 bg-blue-50'):
                    ui.label('Perfil e Preferências').classes('text-lg font-bold mb-3')
                    
                    with ui.grid(columns=3).classes('w-full gap-4'):
                        with ui.row().classes('items-center gap-2'):
                            if locatario.estudante:
                                ui.icon('school', size='sm').classes('text-blue-600')
                                ui.label('Estudante').classes('text-sm font-medium')
                            else:
                                ui.icon('work', size='sm').classes('text-gray-600')
                                ui.label('Não Estudante').classes('text-sm font-medium')
                        
                        with ui.row().classes('items-center gap-2'):
                            if locatario.fumante:
                                ui.icon('smoking_rooms', size='sm').classes('text-orange-600')
                                ui.label('Fumante').classes('text-sm font-medium')
                            else:
                                ui.icon('smoke_free', size='sm').classes('text-green-600')
                                ui.label('Não Fumante').classes('text-sm font-medium')
                        
                        with ui.row().classes('items-center gap-2'):
                            if locatario.possui_pet:
                                ui.icon('pets', size='sm').classes('text-purple-600')
                                ui.label('Possui Pet').classes('text-sm font-medium')
                            else:
                                ui.icon('block', size='sm').classes('text-gray-600')
                                ui.label('Sem Pets').classes('text-sm font-medium')
                    
                    if locatario.estudante and locatario.instituicao_ensino_str:
                        with ui.column().classes('mt-3'):
                            ui.label('Instituição de Ensino:').classes('text-sm font-semibold text-gray-600')
                            ui.label(locatario.instituicao_ensino_str).classes('text-base')
                    
                    if locatario.possui_pet and locatario.tipo_pet_str:
                        with ui.column().classes('mt-3'):
                            ui.label('Tipo de Pet:').classes('text-sm font-semibold text-gray-600')
                            ui.label(locatario.tipo_pet_str).classes('text-base')
                
                if locatario.observacoes_str:
                    with ui.card().classes('w-full p-4 mb-4 bg-yellow-50'):
                        ui.label('Observações Adicionais').classes('text-lg font-bold mb-2')
                        ui.label(locatario.observacoes_str).classes('text-sm text-gray-700')
                
                negociacoes_locatario = self._negociacao_service.listar_por_locatario(email_locatario)
                if negociacoes_locatario:
                    with ui.card().classes('w-full p-4 bg-green-50'):
                        ui.label('Histórico de Negociações').classes('text-lg font-bold mb-3')
                        
                        total_neg = len(negociacoes_locatario)
                        finalizadas = len([n for n in negociacoes_locatario if n.status == StatusNegociacao.FINALIZADA])
                        canceladas = len([n for n in negociacoes_locatario if n.status == StatusNegociacao.CANCELADA])
                        
                        with ui.grid(columns=3).classes('w-full gap-4'):
                            with ui.column().classes('items-center'):
                                ui.label(str(total_neg)).classes('text-3xl font-bold text-blue-600')
                                ui.label('Total').classes('text-sm text-gray-600')
                            
                            with ui.column().classes('items-center'):
                                ui.label(str(finalizadas)).classes('text-3xl font-bold text-green-600')
                                ui.label('Finalizadas').classes('text-sm text-gray-600')
                            
                            with ui.column().classes('items-center'):
                                ui.label(str(canceladas)).classes('text-3xl font-bold text-red-600')
                                ui.label('Canceladas').classes('text-sm text-gray-600')
                        
                        avaliacoes = [n.avaliacao_locatario for n in negociacoes_locatario if n.avaliacao_locatario > 0]
                        if avaliacoes:
                            media = sum(avaliacoes) / len(avaliacoes)
                            with ui.row().classes('mt-4 items-center justify-center gap-2'):
                                ui.label('Avaliação Média:').classes('text-sm font-semibold')
                                ui.label(f'{media:.1f}/5.0').classes('text-xl font-bold text-yellow-600')
                                ui.icon('star', size='sm').classes('text-yellow-600')
                
                with ui.row().classes('justify-end mt-4 gap-2'):
                    ui.button('Fechar', on_click=dialog.close).props('flat')
                    ui.button('Entrar em Contato', 
                              on_click=lambda: ui.notify(f'Entre em contato via: {locatario.telefone} ou {locatario.email}', type='info')
                              ).props('color=primary icon=contact_phone')
        
        dialog.open()

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
