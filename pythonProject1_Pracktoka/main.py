import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "PONG"

# Ракетка
class Bar(arcade.Sprite):
    def __init__(self):
        super().__init__('bar.png', 0.2)

    def update(self):
        self.center_x += self.change_x
        if self.right >= SCREEN_WIDTH:
            self.right = SCREEN_WIDTH
        if self.left <= 0:
            self.left = 0

# Мячик
class Ball(arcade.Sprite):
    def __init__(self):
        super().__init__('ball.png', 0.04)
        self.change_x = 5
        self.change_y = 5

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.right > SCREEN_WIDTH:
            self.change_x = -self.change_x
        if self.left <= 0:
            self.change_x = -self.change_x
        if self.top >= SCREEN_HEIGHT:
            self.change_y = -self.change_y
        if self.bottom <= 0:
            return True  # Возвращаем True, если мяч касается нижней части экрана
        return False

class Game(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.bar = Bar()
        self.ball = Ball()
        self.score = 0
        self.game_over = False  # Флаг окончания игры
        self.setup()

    def setup(self):
        self.bar.center_x = SCREEN_WIDTH / 2
        self.bar.center_y = SCREEN_HEIGHT / 5
        self.ball.center_x = SCREEN_WIDTH / 2
        self.ball.center_y = SCREEN_HEIGHT / 2

    def on_draw(self):
        self.clear((255, 255, 255))
        self.bar.draw()
        self.ball.draw()
        self.draw_score()

        if self.game_over:
            self.draw_game_over()  # Отображение сообщения о проигрыше

    def draw_score(self):
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10, SCREEN_HEIGHT - 30, arcade.color.BLACK, 20)

    def draw_game_over(self):
        arcade.draw_text("Game Over!", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.RED, 54, anchor_x="center")
        arcade.draw_text("Press R to Restart", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 60,
                         arcade.color.BLACK, 20, anchor_x="center")

    def update(self, delta):
        if self.game_over:
            return  # Если игра окончена, ничего не делаем

        if arcade.check_for_collision(self.ball, self.bar):
            self.ball.change_y = -self.ball.change_y
            self.score += 1

        if self.ball.update():  # Проверка на касание нижней границы
            self.game_over = True  # Устанавливаем флаг окончания игры

        self.bar.update()

    def on_key_press(self, key, modifiers):
        if self.game_over and key == arcade.key.R:  # Перезапуск игры
            self.score = 0
            self.game_over = False
            self.setup()
        elif not self.game_over:
            if key == arcade.key.LEFT:
                self.bar.change_x = -5
            if key == arcade.key.RIGHT:
                self.bar.change_x = 5

    def on_key_release(self, key, modifiers):
        if not self.game_over:
            if key == arcade.key.RIGHT or key == arcade.key.LEFT:
                self.bar.change_x = 0

if __name__ == "__main__":
    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()
