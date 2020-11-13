import pygame
from lib.BasicObjects.text import Text
from py.constants import *


class Lives:
    def __init__(self, screen, coord, size, lives=1, max_lives=5, font="Arial"):
        self.screen = screen
        self.font = font
        self.x = coord[0]
        self.y = coord[1]
        self.size = size
        self.lives = lives
        self.max_lives = max_lives
        self.text = Text(self.format_live_text(), self.size, [self.x, self.y],
                         color=Color.WHITE, font=self.font)

    def format_live_text(self):  # Функция форматирования текста для вывода
        return f'Lives: {self.lives}'

    def change_count_lives(self, number):  # Функция для изменеия количества жизней
        if self.max_lives >= self.lives + number >= 0:
            self.lives += number

    def process_logic(self):  # Логика класса
        self.text.update_text(self.format_live_text())
        self.text.update_position([self.x, self.y])

    def process_draw(self):  # Отрисовка класса
        self.text.draw(self.screen)


def main():
    gameover = False
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    lives = Lives(screen, [10, 100], 50)  # Создание объекта типа Lives с координатами\
    # 10,100 и размером текста 50
    while not gameover:
        screen.fill(Color.BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameover = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    lives.change_count_lives(1)
                elif event.key == pygame.K_a:
                    lives.change_count_lives(-1)

        lives.process_logic()
        lives.process_draw()
        pygame.display.flip()


if __name__ == '__main__':
    main()
