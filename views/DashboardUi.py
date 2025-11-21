from nicegui import ui, app

class DashboardUi:
    def render(self):
        if 'usuario_logado' not in app.storage.user:
            ui.navigate.to('/login')
            return
        
        usuario = app.storage.user.get('usuario_logado', {})
        tipo_usuario = usuario.get('tipo', 'locatario')
        
        ui.query('body').style('background-color: #ffffff')
        
        with ui.header().classes('items-center justify-between'):
            ui.label('AlugaFacil - Dashboard').classes('text-xl font-bold text-primary')
            ui.button('Sair', on_click=self.fazer_logout).props('flat color=white')
        
        with ui.column().classes('w-full p-8'):
            ui.label(
                f'Bem-vindo, {usuario.get("nome", "Usuário")}!').classes('text-3xl font-bold mb-4 text-primary')
            
            ui.label(f'Perfil: {tipo_usuario.capitalize()}').classes('text-lg text-gray-600 mb-6')
            
            # Seção de Navegação Principal
            with ui.card().classes('w-full max-w-4xl p-6 mb-6'):
                ui.label('Navegação Rápida').classes('text-2xl font-bold mb-4')
                
                with ui.grid(columns=2).classes('w-full gap-4'):
                    # Card de Anúncios (ambos os tipos)
                    with ui.card().classes('p-4 cursor-pointer hover:shadow-lg').on('click', lambda: ui.navigate.to('/anuncios')):
                        ui.icon('home', size='3rem').classes('text-primary mb-2')
                        ui.label('Ver Anúncios').classes('text-xl font-bold')
                        if tipo_usuario == 'locatario':
                            ui.label('Navegue pelos imóveis disponíveis').classes('text-sm text-gray-600')
                        else:
                            ui.label('Visualize os anúncios cadastrados').classes('text-sm text-gray-600')
                    
                    # Card de Favoritos (apenas locatários)
                    if tipo_usuario == 'locatario':
                        with ui.card().classes('p-4 cursor-pointer hover:shadow-lg').on('click', lambda: ui.navigate.to('/favoritos')):
                            ui.icon('favorite', size='3rem').classes('text-red-500 mb-2')
                            ui.label('Meus Favoritos').classes('text-xl font-bold')
                            ui.label('Visualize seus anúncios salvos').classes('text-sm text-gray-600')
                    else:
                        # Placeholder para manter o grid 2x2
                        with ui.card().classes('p-4 cursor-pointer hover:shadow-lg').on('click', lambda: ui.navigate.to('/negociacoes')):
                            ui.icon('handshake', size='3rem').classes('text-green-600 mb-2')
                            ui.label('Negociações').classes('text-xl font-bold')
                            ui.label('Gerencie propostas recebidas').classes('text-sm text-gray-600')
                    
                    # Card de Negociações (locatários)
                    if tipo_usuario == 'locatario':
                        with ui.card().classes('p-4 cursor-pointer hover:shadow-lg').on('click', lambda: ui.navigate.to('/negociacoes')):
                            ui.icon('handshake', size='3rem').classes('text-green-600 mb-2')
                            ui.label('Negociações').classes('text-xl font-bold')
                            ui.label('Gerencie suas propostas de aluguel').classes('text-sm text-gray-600')
                    
                    # Card de Visitas (ambos os tipos, mas com textos diferentes)
                    with ui.card().classes('p-4 cursor-pointer hover:shadow-lg').on('click', lambda: ui.navigate.to('/visitas')):
                        ui.icon('event', size='3rem').classes('text-blue-600 mb-2')
                        if tipo_usuario == 'locatario':
                            ui.label('Minhas Visitas').classes('text-xl font-bold')
                            ui.label('Agende e gerencie suas visitas').classes('text-sm text-gray-600')
                        else:
                            ui.label('Minhas Visitas').classes('text-xl font-bold')
                            ui.label('Visitas agendadas nos seus imóveis').classes('text-sm text-gray-600')
            
            # Seção de Informações do Usuário
            with ui.card().classes('w-full max-w-4xl p-6'):
                ui.label('Informações do Usuário').classes('text-xl font-bold mb-4')
                
                with ui.column().classes('gap-2'):
                    with ui.row().classes('items-center gap-2'):
                        ui.icon('email', size='sm').classes('text-primary')
                        ui.label(f'E-mail: {usuario.get("email", "N/A")}').classes('text-md')
                    
                    with ui.row().classes('items-center gap-2'):
                        ui.icon('phone', size='sm').classes('text-primary')
                        ui.label(f'Telefone: {usuario.get("telefone", "N/A")}').classes('text-md')
                    
                    with ui.row().classes('items-center gap-2'):
                        ui.icon('person', size='sm').classes('text-primary')
                        ui.label(f'Tipo de Conta: {tipo_usuario.capitalize()}').classes('text-md')
    
    def fazer_logout(self):
        app.storage.user.clear()
        ui.notify('Logout realizado com sucesso!', type='info')
        ui.navigate.to('/login')
