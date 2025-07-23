import flet as ft
from metadados.metadadosMusic import get_capaAlbum

class MusicPlayerUI:
    def __init__(self, colors, page, player, musics):
        self.page = page
        self.player = player
        self.musics = musics
        self.index = 0
        self.colors = colors
        self.pasta_selecionada = ft.FilePicker(self.on_result)
        
        page.overlay.append(self.pasta_selecionada)
        
        self.image_album = ft.Image(
            src=get_capaAlbum(musics[self.index]), 
            error_content=ft.Image(src=r"assets\default_album.png"),
            fit=ft.ImageFit.COVER,
        )
        
        self.text_music = ft.Text(
            value=self._musicName(),
            size=16,
            color=colors["white"]
        )
        
        self.btn_play = self._buildPlayButton()
        self.btn_pause = self._buildPauseButton()
        self.btn_previous = self._buildPreviousButton()
        self.btn_next = self._buildNextButton()
        
    def _musicName(self):
        return self.musics[self.index].split("\\")[-1]
    
    def _updateDisplay(self):
        self.text_music.value = self._musicName()
        self.image_album.src = get_capaAlbum(self.musics[self.index])
        self.page.update()
        
    def _btn_play_on_click(self, e):
        e.control.visible = False
        self.btn_pause.visible = True
        self.page.update()
        
        self.player.unpause()
    
    def _buildPlayButton(self):
        return ft.IconButton(
            icon=ft.Icons.PLAY_ARROW,
            icon_color=self.colors["white"],
            icon_size=50,
            visible=False,
            on_click=self._btn_play_on_click,
        )

    def _btn_pause_on_click(self, e):
        e.control.visible = False
        self.btn_play.visible = True
        self.page.update()
        
        self.player.pause()

    def _buildPauseButton(self):
        return ft.IconButton(
            icon=ft.Icons.PAUSE,
            icon_color=self.colors["white"],
            icon_size=50,
            visible=True,
            on_click=self._btn_pause_on_click,
        )

    def _btn_previous_on_click(self, e):
        if self.index > 0:
            self.index -= 1
            self.player.play(self.musics[self.index])
            self._updateDisplay()

    def _buildPreviousButton(self):
        return ft.IconButton(
            icon=ft.Icons.SKIP_PREVIOUS,
            icon_color=self.colors["white"],
            icon_size=50,
            on_click=self._btn_previous_on_click,
        )

    def _btn_next_on_click(self, e):
        if self.index < len(self.musics) - 1:
            self.index += 1
            self.player.play(self.musics[self.index])
            self._updateDisplay()

    def _buildNextButton(self):
        return ft.IconButton(
            icon=ft.Icons.SKIP_NEXT,
            icon_color=self.colors["white"],
            icon_size=50,
            on_click=self._btn_next_on_click,
        )
        
    def _buildAppBar(self):
        return ft.AppBar(
            title=ft.Text("Player de Música"),
            bgcolor=self.colors["black"],
            center_title=True,
            actions=[
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(text="Selecionar Pasta", on_click=lambda e: self.pasta_selecionada.get_directory_path()),
                    ],
                    icon_color=self.colors["white"],
                )
            ]
        )
    
    def on_result(self, e: ft.FilePickerResultEvent):
        if e.path:
            from meu_player_musica.src.utils.directory import get_musics
            from config import salvar_configuracoes
            config = {}
            
            config["pasta_padrao"] = e.path
            salvar_configuracoes(config)
            
            # Carrega novas músicas e atualiza o player
            self.musics = get_musics(e.path)
            self.musics.sort()
            self.index = 0

            self.player.play(self.musics[self.index])
            self._updateDisplay()
            
    def buildView(self):
        return ft.View(
            "/",
            bgcolor=self.colors["black"],
            appbar=self._buildAppBar(),
            can_pop=True,
            controls=[
                ft.Column(
                    controls=[
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Container(
                                        content=self.image_album,
                                        expand=True,
                                        bgcolor=self.colors["white"],
                                    ),
                                    self.text_music,
                                ],
                                expand=True,
                                alignment=ft.alignment.center,
                            ),
                            expand=True,  # ocupa todo o espaço restante
                            alignment=ft.alignment.center,
                            padding=10,
                        ),
                        ft.Container(
                            content=ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,  # centraliza os botões
                                controls=[
                                    self.btn_previous,
                                    self.btn_play, 
                                    self.btn_pause,
                                    self.btn_next,
                                ]
                            ),
                            height=100,
                        )
                    ],
                    expand=True,
                    alignment=ft.MainAxisAlignment.END,  # empurra o segundo container para o fim
                )
            ]
        )