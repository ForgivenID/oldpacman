import pygame as pg
from objects import ButtonController, Button, Text
from objects.button.button import SceneButton
from scenes import base, levels
from misc import Color, Font, Maps


class Scene(base.Scene):
    def create_static_objects(self):
        self.__create_title()

    def create_objects(self) -> None:
        super().create_objects()
        self.__save_record()
        self.__create_score_text()
        self.__create_highscore_text()
        self.__unlock_level()

    def __create_title(self) -> None:
        text = ["YOU", "WON"]
        for i in range(2):
            text[i] = Text(self.game, text[i], 40, font=Font.TITLE)
            text[i].move_center(self.game.width // 2, 30+40)
            self.static_object.append(text[1])

    def create_buttons(self) -> None:
        buttons = [
            Button(
                self.game, pg.Rect(0, 0, 180, 35),
                self.__next_level, 'NEXT LEVEL',
                center=(self.game.width // 2, 210),
                text_size=Font.BUTTON_TEXT_SIZE)
            if self.__is_last_level() else SceneButton(
                self.game, pg.Rect(0, 0, 180, 35),
                text='EXIT',
                scene=(self.game.scenes.MENU, False),
                center=(self.game.width // 2, 210),
                text_size=Font.BUTTON_TEXT_SIZE
            ),
            SceneButton(
                self.game, pg.Rect(0, 0, 180, 35),
                text='MENU',
                scene=(self.game.scenes.MENU, False),
                center=(self.game.width // 2, 250),
                text_size=Font.BUTTON_TEXT_SIZE
            )
        ]
        self.objects.append(ButtonController(self.game, buttons))

    def __create_score_text(self) -> None:
        self.__text_score = Text(self.game, f'Score: {self.game.score}', 20)
        self.__text_score.move_center(self.game.width // 2, 135)
        self.objects.append(self.__text_score)

    def __create_highscore_text(self) -> None:
        self.__text_highscore = Text(self.game, f'High score: {self.game.records.data[-1]}', 20)
        self.__text_highscore.move_center(self.game.width // 2, 165)
        self.objects.append(self.__text_highscore)

    def __save_record(self) -> None:
        self.game.records.add_new_record(int(self.game.score))

    def __unlock_level(self):
        if self.__is_last_level():
            next_level = self.game.level_id + 1
            self.game.unlock_level(next_level)

    def __next_level(self):
        next_level = self.game.level_id + 1
        self.game.level_id = next_level
        self.game.records.update_records()
        self.game.scenes.set(self.game.scenes.MAIN, reset=True)

    def __is_last_level(self):
        return (self.game.level_id + 1) < Maps.count
