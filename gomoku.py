import pygame as pg, sys
import time, math, datetime as dt
from pygame.locals import *

class Gomoku():
    def __init__(self):
        self.win1 = 0
        self.win2 = 0
        self.CLOCK = pg.time.Clock()
        self.end_game = False
        self.start = False
        self.czas_1 = 0
        self.czas_2 = 0
        self.tut = True
        self.player = 'GRACZ 1'
        self.msg = self.player + ' :WYBIERZ KOLOR'
        self.stone_color = (0, 0, 0)
        self.winner = None
        self.remis = False
        self.width = 600
        self.height = 600
        self.size = 16
        self.break_s = self.width / self.size
        self.line_color = (0, 0, 0)
        self.fps = 30
        self.player1_time = 600
        self.player2_time = 600
        self.p1_start = time.time()
        self.p2_start = time.time()
        self.line_size = 1
        self.white = (255,255,255)
        self.black = (0, 0, 0)
        self.screen_color = (102, 255, 102)
        self.intersections = list()
        self.taken = list()
        self.fps = 30

        self.img_finish_button_path = r"C:\Users\lenovo\PycharmProjects\pythonProject\gomoku\finish.png"
        self.img_start_button_path = r"C:\Users\lenovo\PycharmProjects\pythonProject\gomoku\start.png"
        self.img_start_path = r"C:\Users\lenovo\PycharmProjects\pythonProject\gomoku\gomoku.jpg"

        self.screen = pg.display.set_mode((self.width + 150 + math.ceil(self.break_s), self.height + 100), 0, 32)

        self.img_finish_button = pg.image.load(self.img_finish_button_path)
        self.img_finish_button = pg.transform.scale(self.img_finish_button, (150, 150))

        self.img_start_button = pg.image.load(self.img_start_button_path)
        self.img_start_button = pg.transform.scale(self.img_start_button, (150, 150))

        self.img_start = pg.image.load(self.img_start_path)
        self.img_start = pg.transform.scale(self.img_start,
                                            (self.width + 150 + math.ceil(self.break_s), self.height + 100))

    def draw(self, mes, area, ctr, color):
        font = pg.font.Font(None, 28)
        message = mes
        text = font.render(message, 1, self.black)
        self.screen.fill(color, area)
        text_rect = text.get_rect(center=ctr)
        self.screen.blit(text, text_rect)
        pg.display.update()

    def draw_board(self):
        # vertical lines
        for i in range(0, self.size - 1):
            pg.draw.line(self.screen, self.black, (self.width * i / self.size + self.break_s, self.break_s),
                         (self.width * i / self.size + self.break_s, self.height - self.break_s), self.line_size)
        # horizontal lines
        for i in range(0, self.size - 1):
            pg.draw.line(self.screen, self.black, (self.break_s, self.height * i / self.size + self.break_s),
                         (self.width - self.break_s, self.height * i / self.size + self.break_s), self.line_size)
        # przecięcia krawędzi, na których można ustawiać kamyki
        for i in range(1, 16):
            for j in range(1, 16):
                self.intersections.append((i * self.break_s, j * self.break_s))

    def game_start(self):
        self.screen.fill(self.screen_color)
        self.screen.blit(self.img_start_button, (self.width, 150))
        self.screen.blit(self.img_finish_button, (self.width, 400))
        pg.display.update()

        pg.draw.rect(self.screen, self.black, [self.width / 4, self.height + 50, self.width / 4, 50])
        pg.draw.rect(self.screen, self.white, [self.width / 2, self.height + 50, self.width / 4, 50])

        self.screen.blit(self.img_start_button, (self.width, 150))
        pg.display.update()
        self.screen.blit(self.img_finish_button, (self.width, 400))
        pg.display.update()
        self.draw_board()

        self.draw(self.msg, (self.width / 4, self.height, self.width / 2, 50), (self.width / 2, self.height + 25),
                  self.screen_color)
        self.start = True
        self.p1_start = self.p2_start = time.time()
        self.czas_1 = self.czas_2 = 0

    def set_time(self):
        if self.start is True:
            if self.player == "GRACZ 1":
                self.czas_1 = math.floor(time.time() - self.p1_start)
                if self.czas_1 == 1:
                    self.p1_start = time.time()
                    self.player1_time = self.player1_time - self.czas_1
            elif self.player == 'GRACZ 2':
                self.czas_2 = math.floor(time.time() - self.p2_start)
                if self.czas_2 == 1:
                    self.p2_start = time.time()
                    self.player2_time = self.player2_time - self.czas_2
            # pg.draw.line(self.screen , self.black , (0 , self.height + 50) ,
            #              (self.width , self.height + 50) , self.line_size)
            self.draw(time.strftime("%M:%S", time.gmtime(self.player1_time)), (0, self.height + 50, self.width / 4, 50),
                      (self.width / 8, self.height + 75), self.screen_color)
            self.draw(time.strftime("%M:%S", time.gmtime(self.player2_time)),
                      (self.width * 6 / 8, self.height + 50, self.width / 4, 50),
                      (self.width * 7 / 8, self.height+75),
                      self.screen_color)

            mes = 'GRACZ 1 (' + str(self.win1) + ')'
            mes2 = 'GRACZ 2 (' + str(self.win2) + ')'
            if self.player == 'GRACZ 1':
                self.draw(mes, (0, self.height, self.width / 4, 50), (self.width / 8, self.height + 25), (0, 255, 0))
                self.draw(mes2, (self.width * 6 / 8, self.height, self.width / 4, 50),
                          (self.width * 7 / 8, self.height + 25), self.screen_color)
            else:
                self.draw(mes, (0, self.height, self.width / 4, 50), (self.width / 8, self.height + 25),
                          self.screen_color)
                self.draw(mes2, (self.width * 6 / 8, self.height, self.width / 4, 50),
                          (self.width * 7 / 8, self.height + 25), (0,255,0))

    def checkwin(self, last_element, stone_color, pl):
        g = 0
        # sprawdzamy kamienie w poziomie
        for i in range(-5, 5):
            if ((last_element[0] + self.break_s * i, last_element[1]), stone_color) in self.taken:
                g += 1
                # print('if= ',last_element)
                # print("if g = ",g)
            else:
                if g == 5:
                    break
                else:
                    g = 0
        # sprawdzamy kamienie w pionie
        if g != 5:
            for i in range(-5, 5):
                if ((last_element[0], last_element[1] + self.break_s * i), stone_color) in self.taken:
                    g += 1
                else:
                    if g == 5:
                        break
                    else:
                        g = 0
        # sprawdzamy kamienie po skosie od lewej do prawej w dół
        if g != 5:
            for i in range(-5, 5):
                if (
                        (last_element[0] + self.break_s * i, last_element[1] + self.break_s * i),
                        stone_color) in self.taken:
                    g += 1
                    # print('if 2= ', last_element)
                    # print("if 2 g = ", g)
                else:
                    if g == 5:
                        break
                    else:
                        g = 0
        # sprawdzamy po skosie kamienie od lewej do prawej w górę
        if g != 5:
            for i in range(-5, 5):
                if (
                        (last_element[0] - self.break_s * i, last_element[1] + self.break_s * i),
                        stone_color) in self.taken:
                    g += 1
                    # print('if 2= ', last_element)
                    # print("if 2 g = ", g)
                else:
                    if g == 5:
                        break
                    else:
                        g = 0
        if g == 5:
            self.winner = pl
        else:
            if len(self.taken) == 225:
                self.winner = None

    def click(self):
        x, y = pg.mouse.get_pos()
        print('click working')
        if self.end_game is True:
            if self.width < x < self.width + 150 and 150 < y < 300:
                self.reset()
                self.end_game = False
            if self.width < x < self.width + 150 and 400 < y < 550:
                pg.quit()
                sys.exit()
                self.end_game = False
        else:
            if self.tut is False:
                # x , y = pg.mouse.get_pos()
                # kliknięcie na planszę
                if 0 < x < self.width and 0 < y < self.height + 100:
                    if ' : BIAŁY KAMIEŃ' in self.msg or ' : CZARNY KAMIEŃ' in self.msg:
                        for i in self.intersections:
                            if (i, self.black) not in self.taken and (i, self.white) not in self.taken:
                                if i[0] - self.break_s / 2 < x < i[0] + self.break_s / 2 and i[
                                    1] - self.break_s / 2 < y < i[1] + self.break_s / 2:
                                    # RYSOWANIE KAMIENI NA PLANSZY
                                    pg.draw.circle(self.screen, self.stone_color, (i[0], i[1]),
                                                   math.floor(self.break_s / 2),
                                                   math.floor(self.break_s / 2))
                                    if self.stone_color == self.black:
                                        pg.draw.circle(self.screen, self.white, (i[0], i[1]),
                                                       math.floor(self.break_s / 2),
                                                       1)
                                    else:
                                        pg.draw.circle(self.screen, self.black,
                                                       (i[0], i[1]), math.floor(self.break_s / 2),
                                                       1)
                                    pg.display.update()
                                    # taken - przechowuje wpółrzędne, na których już położono kamień
                                    self.taken.append((i, self.stone_color))
                                    self.checkwin(i, self.stone_color, self.player)

                                    # po każdym ruchu jest zmiana graczy
                                    if self.winner is None:
                                        if (self.player == 'GRACZ 1'):
                                            self.player = 'GRACZ 2'
                                            self.p2_start = time.time()
                                        else:
                                            self.player = 'GRACZ 1'
                                            self.p1_start = time.time()

                    if self.winner:
                        if self.winner == "GRACZ 1":
                            self.win1 += 1
                        else:
                            self.win2 += 1
                        self.msg = self.player + " WIN !!!"
                    else:
                        if self.width / 4 < x < self.width / 2 and self.height + 50 < y < self.height + 100:
                            self.msg = self.player + " : CZARNY KAMIEŃ"
                            self.stone_color = self.black
                        elif self.width / 2 < x < self.width * 3 / 4 and self.height + 50 < y < self.height + 100:
                            self.msg = self.player + " : BIAŁY KAMIEŃ"
                            self.stone_color = self.white
                        else:
                            self.msg = self.player + " : WYBIERZ KOLOR"

                    self.draw(self.msg, (self.width / 4, self.height, self.width / 2, 50),
                              (self.width / 2, self.height + 25), self.screen_color)
            elif self.width < x < self.width + 150 and 150 < y < 300 and self.tut is True:
                self.tut = False
                self.game_start()

    def reset(self):
        self.player = 'GRACZ 1'
        self.msg = 'GRACZ 1 : WYBIERZ KOLOR'
        self.winner = None
        self.player1_time = self.player2_time = 600
        self.taken = list()
        print("reset() is working")
        self.start = False
        self.game_start()

    def game_over(self):
        self.end_game = True
        self.screen.blit(self.img_start_button, (self.width, 150))
        pg.display.update()
        self.screen.blit(self.img_finish_button, (self.width, 400))
        pg.display.update()

    def tutorial(self):
        self.screen.blit(self.img_start, (0, 0))
        pg.display.update()
        time.sleep(2)
        w = 150
        x = 40
        self.screen.fill(self.screen_color)

        pg.display.update()
        self.draw("ZASADY GRY GOMOKU", (0, self.width, self.width, self.width), (self.width / 2, 50), self.screen_color)
        self.draw('Gracze układają na zmianę kamienie na przecięciach linii.',
                  (100, self.width, self.width, self.width), (self.width / 2, w),
                  self.screen_color)
        self.draw('Każdy gracz może położyć czarny lub biały kamień.', (100, self.width, self.width, self.width),
                  (self.width / 2, w + x),
                  self.screen_color)
        self.draw('Aby wybrać kamień kliknij na dany kolor na dole planszy', (100, self.width, self.width, self.width),
                  (self.width / 2, w + 2 * x), self.screen_color)
        self.draw('Aby umieścić kamień na planszy kliknij tam myszką', (100, self.width, self.width, self.width),
                  (self.width / 2, w + 3 * x),
                  self.screen_color)
        self.draw(' Wygrywa gracz, który ułoży', (100, self.width, self.width, self.width), (self.width / 2, w + 4 * x),
                  self.screen_color)
        self.draw('DOKŁADNIE 5 kamieni tego samego koloru', (100, self.width, self.width, self.width),
                  (self.width / 2, w + 5 * x),
                  self.screen_color)
        self.draw('W PIONIE, POZIOMIE lub SKOSIE ', (100, self.width, self.width, self.width),
                  (self.width / 2, w + 6 * x), self.screen_color)

        self.screen.blit(self.img_start_button, (self.width, 150))
        pg.display.update()
        self.screen.blit(self.img_finish_button, (self.width, 400))
        pg.display.update()


# KONIEC KLASY


pg.init()
pg.display.set_caption("GOMOKU")

g = Gomoku()
# najpierw wyświetlamy zasady gry
g.tutorial()

while (True):
    if g.end_game is False:
        g.set_time()
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            g.click()
            if g.winner:
                g.end_game = True
                g.game_over()
    g.CLOCK.tick(g.fps)
