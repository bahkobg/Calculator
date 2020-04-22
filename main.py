import pygame

WIDTH = 1000
HEIGHT = 700
GREY = (224, 224, 224)
GREY_LIGHT = (236, 236, 236)
GREY_WHITE = (246, 246, 246)
MAX_DIGITS = 15
pygame.init()


class Display(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, text: str, color: tuple) -> None:
        super().__init__()
        self.text = text
        self.width = 700
        self.height = 100
        self.display_var = text
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.color = color
        self.color_main = self.color
        self.color_border = GREY
        self.font = pygame.font.SysFont('segoeui', 48, bold=False)
        self.text_offset = self.font.size(self.text)
        self.text_offset_x = self.text_offset[0]
        self.text_offset_y = self.text_offset[1]

    def on_click(self):
        pass

    def on_hover(self, x, y):
        if self.rect.collidepoint(x, y):
            self.color_main = GREY
        else:
            self.color_main = self.color

    @property
    def get_display_var(self) -> str:
        return self.display_var

    def set_display_var(self, x: str) -> None:
        if self.display_var == '0':
            self.display_var = ''
        if len(self.display_var) + len(x) <= MAX_DIGITS:
            self.display_var += x
            self.text_offset = self.font.size(self.display_var)
            self.text_offset_x = self.text_offset[0]
            self.text_offset_y = self.text_offset[1]

    def draw(self, surface):
        pygame.draw.rect(surface, self.color_main, self.rect)
        pygame.draw.rect(surface, self.color_border, self.rect, 1)
        surface.blit(self.font.render(self.display_var, True, (32, 32, 32)),
                     (self.rect.topright[0] - self.text_offset_x - 20, self.rect.topright[1]))


class Button(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, button_id, text: str, color: tuple, digit=False) -> None:
        super().__init__()
        self.button_id = button_id
        self.text = text
        self.width = 178
        self.height = 78
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.color = color
        self.color_main = self.color
        self.color_border = GREY
        self.digit = digit
        if digit:
            self.font = pygame.font.SysFont('segoeui', 28, bold=True)
        else:
            self.font = pygame.font.SysFont('segoeui', 28)
        self.text_offset = self.font.size(self.text)
        self.text_offset_x = self.text_offset[0] // 2
        self.text_offset_y = self.text_offset[1] // 2

    def on_click(self, x: int, y: int) -> bool:
        if self.rect.collidepoint(x, y):
            return True

    @property
    def get_button_text(self):
        return self.text

    def on_hover(self, x, y):
        if self.rect.collidepoint(x, y):
            self.color_main = GREY
        else:
            self.color_main = self.color

    @property
    def get_digit(self) -> bool:
        return self.digit

    def draw(self, surface):
        pygame.draw.rect(surface, self.color_main, self.rect)
        pygame.draw.rect(surface, self.color_border, self.rect, 1)
        surface.blit(self.font.render(self.text, True, (32, 32, 32)),
                     (self.rect.centerx - self.text_offset_x, self.rect.centery - self.text_offset_y))


class Runtime:

    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.buttons = pygame.sprite.Group()
        self.display = Display(10, 100, '0', GREY_LIGHT)
        self.display_var = '0'
        self.buttons.add(
            Button(0, 232, 22, '%', GREY_LIGHT),
            Button(0, 310, 22, 'CE', GREY_LIGHT),
            Button(0, 388, 22, '7', GREY_WHITE, True),
            Button(0, 466, 22, '4', GREY_WHITE, True),
            Button(0, 544, 22, '1', GREY_WHITE, True),
            Button(0, 622, 22, '+-', GREY_LIGHT),
            Button(178, 232, 22, '√', GREY_LIGHT),
            Button(178, 310, 22, 'C', GREY_LIGHT),
            Button(178, 388, 22, '8', GREY_WHITE, True),
            Button(178, 466, 22, '5', GREY_WHITE, True),
            Button(178, 544, 22, '2', GREY_WHITE, True),
            Button(178, 622, 22, '0', GREY_WHITE, True),
            Button(356, 232, 22, 'x²', GREY_LIGHT),
            Button(356, 310, 22, '<-', GREY_LIGHT),
            Button(356, 388, 22, '9', GREY_WHITE, True),
            Button(356, 466, 22, '6', GREY_WHITE, True),
            Button(356, 544, 22, '3', GREY_WHITE, True),
            Button(356, 622, 22, '.', GREY_LIGHT),
            Button(534, 232, 22, '1/x', GREY_LIGHT),
            Button(534, 310, 22, '÷', GREY_LIGHT),
            Button(534, 388, 22, '*', GREY_LIGHT),
            Button(534, 466, 22, '-', GREY_LIGHT),
            Button(534, 544, 22, '+', GREY_LIGHT),
            Button(534, 622, 22, '=', GREY_LIGHT)
        )

    def on_mouse_button_down(self):
        pos = pygame.mouse.get_pos()
        x = pos[0]
        y = pos[1]
        for button in self.buttons:
            if button.on_click(x, y) and button.digit:
                self.display.set_display_var(button.get_button_text)
                print(button.get_button_text)

    def on_mouse_button_up(self):
        pass

    def update(self):
        pos = pygame.mouse.get_pos()
        x = pos[0]
        y = pos[1]

        for button in self.buttons:
            button.on_hover(x, y)

    def draw(self):
        self.display.draw(self.screen)
        for button in self.buttons:
            button.draw(self.screen)

    def run(self):
        running = True

        while running:
            pygame.display.set_caption(f"Calculator by Ivan Ivanov | FPS: {round(self.clock.get_fps())}")
            self.screen.fill(GREY)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                if e.type == pygame.MOUSEBUTTONDOWN:
                    self.on_mouse_button_down()
                if e.type == pygame.MOUSEBUTTONUP:
                    self.on_mouse_button_up()

            self.update()

            self.draw()
            self.clock.tick(24)
            pygame.display.update()


g = Runtime()
g.run()
