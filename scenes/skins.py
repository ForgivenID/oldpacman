import pygame as pg

from objects import ButtonController, Text, Button, ImageObject
from scenes import base
from misc import Font


class Scene(base.Scene):
    class SkinButton(Button):
        def __init__(self, **args) -> object:
            self.value = args.pop("value")
            super().__init__(**args)

        def click(self):
            self.game.skins.current = self.value

        def process_event(self, event: pg.event.Event) -> None:
            super().process_event(event)

        def on_hover(self) -> None:
            self.game.scenes.current.preview.image = self.value.surface
            self.game.scenes.current.preview.scale(75, 75)

    def create_static_objects(self):
        self.__create_title()

    def create_objects(self) -> None:
        super().create_objects()
        self.preview = ImageObject(self.game, self.game.skins.current.surface, (130, 110))
        self.preview.scale(75, 75)
        self.objects.append(self.preview)

    def __create_title(self) -> None:
        title = Text(self.game, 'SELECT SKIN', 25, font=Font.TITLE)
        title.move_center(self.game.width // 2, 30)
        self.static_objects.append(title)

    def create_buttons(self) -> None:
        buttons = []

        skins = {
            0: ('PACMAN', self.game.skins.default),
            1: ('CHROME', self.game.skins.chrome),
            2: ('HALF-LIFE', self.game.skins.half_life),
        }

        for i in range(len(skins)):
            buttons.append(self.SkinButton(
                game=self.game,
                geometry=pg.Rect(0, 0, 120, 30),
                text=skins[i][0],
                value=skins[i][1],
                center=(self.game.width // 2 - 45, 115 + i * 33),
                text_size=Font.BUTTON_TEXT_SIZE,
                active=skins[i][1].name in self.game.unlocked_skins))

        buttons.append(self.SceneButton(
            game=self.game,
            geometry=pg.Rect(0, 0, 180, 40),
            text='MENU',
            scene=(self.game.scenes.MENU, False),
            center=(self.game.width // 2, 250),
            text_size=Font.BUTTON_TEXT_SIZE))

        self.objects.append(ButtonController(self.game, buttons))
