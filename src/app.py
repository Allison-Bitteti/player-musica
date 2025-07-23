import flet as ft
import asyncio
import os
from ui.musicPlayerUI import MusicPlayerUI
from utils.directory import get_musics
from player.player import Player
from config import carregar_configuracoes, salvar_configuracoes

colors = {
    "white": ft.Colors.WHITE,
    "black": ft.Colors.BLACK,
}

def main(page: ft.Page):
    page.title = "Player de Música"
    page.window.height = 600
    page.window.width = 400
    page.window.bgcolor = colors["black"]
    page.window.maximizable = False
    page.window.resizable = False
    
    config = carregar_configuracoes()
    pasta = config.get("pasta_padrao", "")
    
    # Função para continuar após seleção da pasta
    def continuar_app(com_caminho):
        musics = get_musics(com_caminho)
        musics.sort()
        player = Player()
        player.play(music_path=musics[0])
        UI = MusicPlayerUI(colors=colors, page=page, player=player, musics=musics)

        def route_change(route):
            page.views.clear()
            page.views.append(UI.buildView())
            page.update()

        def view_pop(view):
            page.views.pop()
            top_view = page.views[-1]
            page.go(top_view.route)

        page.on_route_change = route_change
        page.on_view_pop = view_pop
        page.go(page.route)

    async def selecionar_pasta():
        picker = ft.FilePicker()

        async def on_result(e: ft.FilePickerResultEvent):
            if e.path:
                config["pasta_padrao"] = e.path
                salvar_configuracoes(config)
                await asyncio.sleep(0.1)  # espera o seletor fechar
                continuar_app(e.path)

        picker.on_result = on_result
        page.overlay.append(picker)
        page.update()
        picker.get_directory_path(dialog_title="Selecione a pasta de músicas")

    if not pasta or not os.path.exists(pasta):
        asyncio.run(selecionar_pasta())
    else:
        continuar_app(pasta)

ft.app(main)
