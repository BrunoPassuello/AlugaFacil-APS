from nicegui import ui, app
from services.ImovelService import ImovelService

class MeusImoveisUi:
    
    def __init__(self):
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
                ui.button('Meus Anúncios', on_click=lambda: ui.navigate.to('/meus-anuncios')).props('flat')
        
        with ui.column().classes('w-full p-6'):
            ui.label('Meus Imóveis').classes('text-3xl font-bold mb-4 text-primary')
            
            ui.button('Cadastrar Novo Imóvel', 
                     on_click=lambda: self._abrir_dialogo_cadastrar_imovel(email)).props('color=primary').classes('mb-4')
            
            imoveis = self._imovel_service.listar_por_proprietario(email)
            
            if not imoveis:
                ui.label('Você ainda não cadastrou nenhum imóvel.').classes('text-gray-600 italic')
            else:
                for imovel in imoveis:
                    self._render_card_imovel(imovel)
            
            ui.button('Voltar ao Dashboard', 
                     on_click=lambda: ui.navigate.to('/dashboard')).classes('mt-8').props('color=primary outline')
    
    def _render_card_imovel(self, imovel):
        with ui.card().classes('w-full mb-4 p-4'):
            with ui.row().classes('w-full justify-between items-start'):
                with ui.column().classes('flex-grow'):
                    ui.label(f'{imovel.tipo_imovel().capitalize()} #{imovel.id}').classes('text-xl font-bold text-primary')
                    ui.label(f'Endereço: {imovel.endereco}').classes('text-sm text-gray-700')
                    ui.label(f'Cidade: {imovel.cidade}').classes('text-sm text-gray-700')
                    ui.label(f'Metragem: {imovel.metragem}m²').classes('text-sm text-gray-600')
                    ui.label(f'Quartos: {imovel.quartos} | Banheiros: {imovel.banheiros}').classes('text-sm text-gray-600')
                    ui.label(f'Garagem: {"Sim" if imovel.possui_garagem else "Não"}').classes('text-sm text-gray-600')
                    
                    if imovel.tipo_imovel() == 'casa':
                        ui.label(f'Pisos: {imovel.numero_pisos} | Área de Lazer: {"Sim" if imovel.area_lazer else "Não"}').classes('text-sm text-gray-600')
                    elif imovel.tipo_imovel() == 'apartamento':
                        ui.label(f'Andar: {imovel.andar} | Varanda: {"Sim" if imovel.possui_varanda else "Não"}').classes('text-sm text-gray-600')
                
                with ui.column().classes('gap-2'):
                    ui.button('Editar', 
                            on_click=lambda i=imovel: self._abrir_dialogo_editar_imovel(i)).props('color=primary size=sm')
                    ui.button('Remover', 
                            on_click=lambda i=imovel: self._remover_imovel(i.id)).props('color=negative size=sm')


    def _abrir_dialogo_editar_imovel(self, imovel):
        dialog = ui.dialog()
        with dialog:
            with ui.card().classes('p-6 w-full max-w-2xl'):
                ui.label(f'Editar {imovel.tipo_imovel().capitalize()}').classes('text-2xl font-bold mb-4')
                
                endereco_input = ui.input(label='Endereço', value=imovel.endereco, placeholder='Rua, Número').classes('w-full')
                cidade_input = ui.input(label='Cidade', value=imovel.cidade, placeholder='Cidade - UF').classes('w-full')
                metragem_input = ui.number(label='Metragem (m²)', value=imovel.metragem, min=1, step=0.1).classes('w-full')
                quartos_input = ui.number(label='Quartos', value=imovel.quartos, min=0).classes('w-full')
                banheiros_input = ui.number(label='Banheiros', value=imovel.banheiros, min=0).classes('w-full')
                garagem_checkbox = ui.checkbox('Possui Garagem', value=imovel.possui_garagem).classes('w-full')
                
                campos_especificos = {}
                if imovel.tipo_imovel() == 'casa':
                    campos_especificos['area_lazer'] = ui.checkbox('Área de Lazer', value=imovel.area_lazer).classes('w-full')
                    campos_especificos['numero_pisos'] = ui.number(label='Número de Pisos', value=imovel.numero_pisos, min=1).classes('w-full')
                elif imovel.tipo_imovel() == 'apartamento':
                    campos_especificos['andar'] = ui.number(label='Andar', value=imovel.andar, min=0).classes('w-full')
                    campos_especificos['possui_varanda'] = ui.checkbox('Possui Varanda', value=imovel.possui_varanda).classes('w-full')
                
                with ui.row().classes('justify-end mt-4 gap-2'):
                    ui.button('Cancelar', on_click=dialog.close).props('flat')
                    ui.button('Salvar Alterações', 
                            on_click=lambda: self._editar_imovel(
                                dialog, imovel, endereco_input, cidade_input,
                                metragem_input, quartos_input, banheiros_input, garagem_checkbox, campos_especificos
                            )).props('color=primary')
        dialog.open()
        

    def _editar_imovel(self, dialog, imovel, endereco_input, cidade_input,
                    metragem_input, quartos_input, banheiros_input, garagem_checkbox, campos_especificos):
        endereco = endereco_input.value
        cidade = cidade_input.value
        metragem = metragem_input.value or 0
        quartos = int(quartos_input.value or 0)
        banheiros = int(banheiros_input.value or 0)
        possui_garagem = garagem_checkbox.value
        
        if not endereco or not cidade or metragem <= 0:
            ui.notify('Preencha todos os campos obrigatórios', type='warning')
            return
        
        # Prepara kwargs com campos específicos
        kwargs = {}
        if imovel.tipo_imovel() == 'casa':
            kwargs['area_lazer'] = campos_especificos['area_lazer'].value
            kwargs['numero_pisos'] = int(campos_especificos['numero_pisos'].value or 1)
        elif imovel.tipo_imovel() == 'apartamento':
            kwargs['andar'] = int(campos_especificos['andar'].value or 1)
            kwargs['possui_varanda'] = campos_especificos['possui_varanda'].value
        
        sucesso, mensagem = self._imovel_service.atualizar_imovel(
            imovel_id=imovel.id,
            proprietario_email=imovel.proprietario.email,
            endereco=endereco,
            cidade=cidade,
            metragem=metragem,
            quartos=quartos,
            banheiros=banheiros,
            possui_garagem=possui_garagem,
            **kwargs
        ) 
        
        if sucesso:
            ui.notify(mensagem, type='positive')
            dialog.close()
            ui.navigate.reload()
        else:
            ui.notify(mensagem, type='negative')


    
    def _abrir_dialogo_cadastrar_imovel(self, email_proprietario):
        dialog = ui.dialog()
        with dialog:
            with ui.card().classes('p-6 w-full max-w-2xl'):
                ui.label('Cadastrar Novo Imóvel').classes('text-2xl font-bold mb-4')
                
                tipo_select = ui.select(
                    label='Tipo de Imóvel',
                    options=['Casa', 'Apartamento'],
                    value='Casa'
                ).classes('w-full')
                
                endereco_input = ui.input(label='Endereço', placeholder='Rua, Número').classes('w-full')
                cidade_input = ui.input(label='Cidade', placeholder='Cidade - UF').classes('w-full')
                metragem_input = ui.number(label='Metragem (m²)', min=1, step=0.1).classes('w-full')
                quartos_input = ui.number(label='Quartos', min=0, value=2).classes('w-full')
                banheiros_input = ui.number(label='Banheiros', min=0, value=1).classes('w-full')
                garagem_checkbox = ui.checkbox('Possui Garagem', value=False).classes('w-full')
                
                campos_especificos = ui.column().classes('w-full')
                
                def atualizar_campos_especificos():
                    campos_especificos.clear()
                    with campos_especificos:
                        if tipo_select.value == 'Casa':
                            campos_especificos.area_lazer = ui.checkbox('Área de Lazer', value=False).classes('w-full')
                            campos_especificos.numero_pisos = ui.number(label='Número de Pisos', min=1, value=1).classes('w-full')
                        elif tipo_select.value == 'Apartamento':
                            campos_especificos.andar = ui.number(label='Andar', min=0, value=1).classes('w-full')
                            campos_especificos.possui_varanda = ui.checkbox('Possui Varanda', value=False).classes('w-full')
                
                atualizar_campos_especificos()
                tipo_select.on('update:model-value', lambda: atualizar_campos_especificos())
                
                with ui.row().classes('justify-end mt-4 gap-2'):
                    ui.button('Cancelar', on_click=dialog.close).props('flat')
                    ui.button('Cadastrar', 
                            on_click=lambda: self._cadastrar_imovel(
                                dialog, email_proprietario, tipo_select, endereco_input, cidade_input,
                                metragem_input, quartos_input, banheiros_input, garagem_checkbox, campos_especificos
                            )).props('color=primary')
        
        dialog.open()

    
    def _cadastrar_imovel(self, dialog, email, tipo_select, endereco_input, cidade_input, 
                        metragem_input, quartos_input, banheiros_input, garagem_checkbox, campos_especificos):
        tipo = tipo_select.value
        endereco = endereco_input.value
        cidade = cidade_input.value
        metragem = metragem_input.value or 0
        quartos = int(quartos_input.value or 0)
        banheiros = int(banheiros_input.value or 0)
        possui_garagem = garagem_checkbox.value
        
        if not endereco or not cidade or metragem <= 0:
            ui.notify('Preencha todos os campos obrigatórios', type='warning')
            return
        
        if tipo == 'Casa':
            area_lazer = campos_especificos.area_lazer.value
            numero_pisos = int(campos_especificos.numero_pisos.value or 1)
            
            sucesso, imovel, mensagem = self._imovel_service.cadastrar_casa(
                proprietario_email=email,
                endereco=endereco,
                cidade=cidade,
                metragem=metragem,
                quartos=quartos,
                banheiros=banheiros,
                possui_garagem=possui_garagem,
                area_lazer=area_lazer,
                numero_pisos=numero_pisos
            )
        else:  
            andar = int(campos_especificos.andar.value or 1)
            possui_varanda = campos_especificos.possui_varanda.value
            
            sucesso, imovel, mensagem = self._imovel_service.cadastrar_apartamento(
                proprietario_email=email,
                endereco=endereco,
                cidade=cidade,
                metragem=metragem,
                quartos=quartos,
                banheiros=banheiros,
                possui_garagem=possui_garagem,
                andar=andar,
                possui_varanda=possui_varanda
            )
        
        if sucesso:
            ui.notify(mensagem, type='positive')
            dialog.close()
            ui.navigate.reload()
        else:
            ui.notify(mensagem, type='negative')

    
    def _remover_imovel(self, imovel_id):
        sucesso, mensagem = self._imovel_service.remover(imovel_id)
        
        if sucesso:
            ui.notify(mensagem, type='positive')
            ui.navigate.reload()
        else:
            ui.notify(mensagem, type='negative')
