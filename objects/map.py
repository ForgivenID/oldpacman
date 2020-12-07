from random import randint

import pygame as pg

from misc import CELL_SIZE, get_path, Color
from objects import DrawableObject, ImageObject


class Map(DrawableObject):
    tile_names = [
        "space",
        "fat_up_wall", "fat_left_corner",
        "fat_y_corner", "up_wall",
        "left_corner", "ghost_left_corner",
        "ghost_door", "ghost_door_wall_left"
    ]
    tiles = []

    def __init__(self, game, map_data, x=0, y=20) -> None:
        super().__init__(game)
        self.x = x
        self.y = y
        self.map = map_data
        self.__size = (224, 248)
        self.surface = pg.Surface(self.__size)
        self.__load_tiles()
        self.color = self.rand_color()
        self.__render_map_surface()

    def __load_tiles(self) -> None:
        self.tiles = []
        for i in self.tile_names:
            tile_path = get_path(i, 'png', 'images', 'map')
            tile = pg.image.load(tile_path)
            self.tiles.append(tile)

    def __corner_preprocess(self, x, y, temp_surface: pg.surface.Surface) -> pg.surface.Surface:
        flip_x = self.map[y][x][1] // (CELL_SIZE // 2)
        flip_y = False
        temp_surface = pg.transform.flip(temp_surface, flip_x, flip_y)
        rotate_angle = self.map[y][x][1] % (CELL_SIZE // 2) * -90
        temp_surface = pg.transform.rotate(temp_surface, rotate_angle)
        return temp_surface

    def __draw_cell(self, x, y) -> None:
        temp_surface = self.tiles[self.map[y][x][0]]
        if len(self.map[y][x]) == 2:
            temp_surface = self.__corner_preprocess(x, y, temp_surface)
        self.surface.blit(temp_surface, (x * CELL_SIZE, y * CELL_SIZE))

    def __render_map_surface(self) -> None:
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                self.__draw_cell(x, y)

        for x in range(self.surface.get_width()):
            for y in range(self.surface.get_height()):
                if self.surface.get_at((x, y)) == Color.MAIN_MAP:
                    self.surface.set_at((x, y), self.color)  # Set the color of the pixel.

    def prerender_map_image(self) -> pg.Surface:
        surface = pg.Surface(self.__size)
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                temp_surface = self.tiles[self.map[y][x][0]]
                if len(self.map[y][x]) == 2:
                    temp_surface = self.__corner_preprocess(x, y, temp_surface)
                surface.blit(temp_surface, (x * CELL_SIZE, y * CELL_SIZE))

        image = ImageObject(self.game, surface, (110, 95))
        image.smoothscale(100, 100)

        # Threshold
        for x in range(image.image.get_width()):
            for y in range(image.image.get_height()):
                if image.image.get_at((x, y))[2] > 0:
                    image.image.set_at((x, y), (0, 0, 255, 255))  # Set the color of the pixel.
        return image

    def process_draw(self) -> None:
        self.game.screen.blit(self.surface, (self.x, self.y))

    def process_event(self, event: pg.event.Event) -> None:
        pass

    def process_logic(self) -> None:
        pass

    @staticmethod
    def rand_color():
        max_states = 7
        min_val = 200
        max_val = 230
        state = randint(0, max_states)
        if state == max_states:
            color = (255, 255, 255)
        elif state == max_states - 1:
            color = (randint(min_val, max_val), 0, 0)
        elif state == max_states - 2:
            color = (0, randint(min_val, max_val), 0)
        elif state == max_states - 3:
            color = (0, 0, randint(min_val, max_val))
        else:
            excluded_color = randint(0, 2)
            color = (randint(min_val, max_val) if excluded_color != 0 else 0,
                     randint(min_val, max_val) if excluded_color != 1 else 0,
                     randint(min_val, max_val) if excluded_color != 2 else 0)
        return color
