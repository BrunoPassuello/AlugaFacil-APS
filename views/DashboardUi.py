from nicegui import ui

class DashboardUi:
    
    def render(self):
        if 'usuario_logado' not in ui.storage.user:
            ui.navigate.to('/login')
            return
        
        usuario = ui.storage.user.get('usuario_logado', {})
        
        with ui.header().classes('items-center justify-between'):
            ui.label('AlugaFacil - Dashboard').classes('text-xl font-bold')
            ui.button('Sair', on_click=self.fazer_logout).props('flat')
        
        with ui.column().classes('w-full p-8'):
            ui.label(f'Bem-vindo, {usuario.get("nome", "Usuário")}!').classes('text-3xl font-bold mb-4')
            
            with ui.card().classes('w-full max-w-2xl p-6'):
                ui.label('Informações do Usuário').classes('text-xl font-bold mb-4')
                ui.label(f'E-mail: {usuario.get("email", "N/A")}')
                ui.label(f'Telefone: {usuario.get("telefone", "N/A")}')
                ui.label(f'Tipo: {usuario.get("tipo", "N/A")}')
    
    def fazer_logout(self):
        ui.storage.user.clear()
        ui.notify('Logout realizado com sucesso!', type='info')
        ui.navigate.to('/login')
