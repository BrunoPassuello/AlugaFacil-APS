# DashboardUi.py - VERSÃO CENTRALIZADA
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

        with ui.column().classes('w-full items-center p-8'):
            with ui.column().classes('w-full max-w-6xl'):
                ui.label(
                    f'Bem-vindo, {usuario.get("nome", "Usuário")}!').classes('text-3xl font-bold mb-4 text-primary')
                ui.label(f'Perfil: {tipo_usuario.capitalize()}').classes('text-lg text-gray-600 mb-6')

                with ui.card().classes('w-full p-6 mb-6'):
                    ui.label('Navegação Rápida').classes('text-2xl font-bold mb-4')

                    with ui.grid(columns=2).classes('w-full gap-4'):
                        with ui.card().classes('p-4 cursor-pointer hover:shadow-lg transition-shadow').on('click',
                                                                                                          lambda: ui.navigate.to('/anuncios')):
                            ui.icon('home', size='lg').classes('text-primary mb-2')
                            ui.label('Anúncios').classes('text-xl font-semibold')
                            if tipo_usuario == 'locatario':
                                ui.label('Busque imóveis disponíveis para aluguel').classes('text-sm text-gray-600')
                            else:
                                ui.label('Veja todos os anúncios disponíveis').classes('text-sm text-gray-600')

                        with ui.card().classes('p-4 cursor-pointer hover:shadow-lg transition-shadow').on('click',
                                                                                                          lambda: ui.navigate.to('/negociacoes')):
                            ui.icon('handshake', size='lg').classes('text-primary mb-2')
                            ui.label('Negociações').classes('text-xl font-semibold')
                            if tipo_usuario == 'locatario':
                                ui.label('Gerencie suas propostas de aluguel').classes('text-sm text-gray-600')
                            else:
                                ui.label('Gerencie propostas recebidas').classes('text-sm text-gray-600')

                        if tipo_usuario == 'locatario':
                            with ui.card().classes('p-4 cursor-pointer hover:shadow-lg transition-shadow').on('click',
                                                                                                              lambda: ui.navigate.to('/favoritos')):
                                ui.icon('favorite', size='lg').classes('text-red-500 mb-2')
                                ui.label('Favoritos').classes('text-xl font-semibold')
                                ui.label('Acesse seus anúncios favoritados').classes('text-sm text-gray-600')

                            with ui.card().classes('p-4 cursor-pointer hover:shadow-lg transition-shadow').on('click',
                                                                                                              lambda: ui.navigate.to('/visitas')):
                                ui.icon('event', size='lg').classes('text-blue-500 mb-2')
                                ui.label('Minhas Visitas').classes('text-xl font-semibold')
                                ui.label('Gerencie suas visitas agendadas').classes('text-sm text-gray-600')

                        else:
                            with ui.card().classes('p-4 cursor-pointer hover:shadow-lg transition-shadow').on('click',
                                                                                                              lambda: ui.navigate.to('/meus-imoveis')):
                                ui.icon('apartment', size='lg').classes('text-green-500 mb-2')
                                ui.label('Meus Imóveis').classes('text-xl font-semibold')
                                ui.label('Cadastre e gerencie seus imóveis').classes('text-sm text-gray-600')

                            with ui.card().classes('p-4 cursor-pointer hover:shadow-lg transition-shadow').on('click',
                                                                                                              lambda: ui.navigate.to('/meus-anuncios')):
                                ui.icon('campaign', size='lg').classes('text-orange-500 mb-2')
                                ui.label('Meus Anúncios').classes('text-xl font-semibold')
                                ui.label('Crie e gerencie anúncios dos seus imóveis').classes('text-sm text-gray-600')

                            with ui.card().classes('p-4 cursor-pointer hover:shadow-lg transition-shadow').on('click',
                                                                                                              lambda: ui.navigate.to('/visitas')):
                                ui.icon('event', size='lg').classes('text-purple-500 mb-2')
                                ui.label('Minhas Visitas').classes('text-xl font-semibold')
                                ui.label('Veja visitas agendadas nos seus imóveis').classes('text-sm text-gray-600')

                with ui.card().classes('w-full p-6'):
                    ui.label('Sobre o Sistema').classes('text-2xl font-bold mb-4')
                    ui.label(
                        'AlugaFacil é uma plataforma completa para gestão de aluguéis de imóveis.').classes('text-md mb-2')

                    if tipo_usuario == 'locatario':
                        ui.label('Como Locatário, você pode:').classes('font-semibold mt-4 mb-2')
                        with ui.column().classes('ml-4'):
                            ui.label('✓ Buscar imóveis disponíveis').classes('text-sm')
                            ui.label('✓ Favoritar anúncios de interesse').classes('text-sm')
                            ui.label('✓ Fazer propostas de aluguel').classes('text-sm')
                            ui.label('✓ Agendar visitas aos imóveis').classes('text-sm')
                            ui.label('✓ Gerenciar negociações em andamento').classes('text-sm')
                    else:
                        ui.label('Como Proprietário, você pode:').classes('font-semibold mt-4 mb-2')
                        with ui.column().classes('ml-4'):
                            ui.label('✓ Cadastrar seus imóveis').classes('text-sm')
                            ui.label('✓ Criar anúncios personalizados').classes('text-sm')
                            ui.label('✓ Receber e gerenciar propostas de locatários').classes('text-sm')
                            ui.label('✓ Visualizar perfis de interessados').classes('text-sm')
                            ui.label('✓ Acompanhar visitas agendadas').classes('text-sm')
                            ui.label('✓ Aprovar e finalizar negociações').classes('text-sm')

    def fazer_logout(self):
        app.storage.user.clear()
        ui.navigate.to('/login')
        ui.notify('Logout realizado com sucesso', type='positive')
