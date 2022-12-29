import pygame
from tube import Tube
from player import Player
from coin import Coin
import random as r
from config import *


class FlappyDuck:

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.project_name = 'Flappy Duck'

        pygame.display.set_caption(self.project_name)

        # Loop until the user clicks the close button.
        self.running = True

        # Used to manage how fast the screen updates
        self.clock = pygame.time.Clock()

        self.background = pygame.image.load('assets/images/Background-01.png')
        self.flappy_bird_logo = pygame.image.load('assets/images/FlappyBirdLogo.png')

        self.tube_group = pygame.sprite.Group()
        self.coin_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()

        self.player = Player(200, 200, 50, self.screen, self)
        self.player_group.add(self.player)

        self.tube_creation_timer = TUBE_CREATION_DELAY
        self.coin_creation_timer = COIN_CREATION_DELAY

        self.score = 0
        self.font = pygame.font.SysFont("Papyrus", 30)
        self.big_font = pygame.font.SysFont("Papyrus", 100)

        self.collect_coin_sound = pygame.mixer.Sound('assets/audio/collect5.wav')

        self.hit_tube_sound = pygame.mixer.Sound('assets/audio/plop.wav')
        self.start_time = None

        # self.plop_sound = pygame.mixer.Sound('assets/audio/plop.wav')

        # self.plop_sound.set_volume(0.2)
        # self.collect_sound.set_volume(0.2)

        self.mode = GAME_NOT_STARTED

        self.play_button = pygame.image.load('assets/images/Play.png')

        self.credit_button = pygame.image.load('assets/images/credit_button.png')

    def create_tube(self):
        self.tube_creation_timer -= 1
        if self.tube_creation_timer == 0:
            self.tube_creation_timer = TUBE_CREATION_DELAY

            height1 = r.randint(100, 350)
            tube_down = Tube(WIDTH, height1, TUBE_DOWN, self.screen)
            self.tube_group.add(tube_down)

            height2 = HEIGHT - height1 - 200
            tube_up = Tube(WIDTH, height2, TUBE_UP, self.screen)
            self.tube_group.add(tube_up)

            upper_coin = Coin(WIDTH + 250, 80, self.screen)
            self.coin_group.add(upper_coin)

            lower_coin = Coin(WIDTH + 250, 470, self.screen)
            self.coin_group.add(lower_coin)

    def create_player(self):
        random_y = r.randint(0, WIDTH)
        x = 0
        new_player = Player(x, random_y, SPRITE_SIZE, self.screen)
        self.player_group.add(new_player)

    def handle_player_coin_collision(self, player, coin):
        if player.rect.colliderect(coin.rect):
            self.score += 1
            print(f'Score is {self.score}')
            self.collect_coin_sound.play()
            return True
        else:
            return False

    def draw_score_indicator(self):
        score_text = f'SCORE: {self.score}'
        score_msg = self.font.render(score_text, 1, BLACK)
        self.screen.blit(score_msg, (30, 30))

    """
    def create_coin(self):
        self.coin_creation_timer -=1
        if self.coin_creation_timer == 0:
            self.coin_creation_timer = COIN_CREATION_DELAY
            coin = Coin(WIDTH, 20, SPRITE_SIZE, self.screen)
            self.coin_group.add(coin)
    """

    def game_loop(self):
        # -------- Main Program Loop -----------
        while self.running:
            # --- Main event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.blit(self.background, (0, 0))

            if self.mode == GAME_NOT_STARTED:
                self.handle_landing_page()
            elif self.mode == GAME_OVER:
                self.handle_game_over_page()
            # elif self.mode == GAME_STARTED:
            elif self.mode == GAME_CREDITS:
                self.game_credits_page()
            elif self.mode == GAME_WON:
                self.handle_game_won_page()
            else:
                self.handle_game_in_session()

            pygame.display.flip()

            # --- Limit to 60 frames per second
            self.clock.tick(FPS)
            current_fps = str(self.clock.get_fps())
            pygame.display.set_caption(f'{self.project_name}, fps: {current_fps}')

        # Close the window and quit.
        pygame.quit()

    def handle_play_button(self, play_button_x, play_button_y):
        self.screen.blit(self.play_button, (play_button_x, play_button_y))

        mouse_x, mouse_y = pygame.mouse.get_pos()
        play_button_x2 = play_button_x + self.play_button.get_width()
        play_button_y2 = play_button_y + self.play_button.get_height()
        is_mouse_inside_button = play_button_x <= mouse_x <= play_button_x2 \
                                 and play_button_y <= mouse_y <= play_button_y2
        if pygame.mouse.get_pressed()[0] and is_mouse_inside_button:
            self.start_time = pygame.time.get_ticks()
            self.tube_group.empty()
            self.coin_group.empty()
            self.player_group.empty()
            self.score = 0
            self.player = Player(200, 200, 50, self.screen, self)
            self.player_group.add(self.player)
            self.mode = GAME_STARTED

    def draw_countdown_indicator(self):
        duration_seconds = (pygame.time.get_ticks() - self.start_time) // 1000
        countdown_seconds = GAME_DURATION_IN_SECONDS - duration_seconds
        score_text = f'COUNT DOWN: {countdown_seconds}'
        score_msg = self.font.render(score_text, 1, BLACK)
        self.screen.blit(score_msg, (WIDTH - 300, 30))
        if countdown_seconds <= 0:
            self.mode = GAME_WON

    def handle_credit_button(self, credit_button_x, credit_button_y):
        self.screen.blit(self.credit_button, (credit_button_x, credit_button_y))

        mouse_x2, mouse_y2 = pygame.mouse.get_pos()
        credit_button_x2 = credit_button_x + self.credit_button.get_width()
        credit_button_y2 = credit_button_x + self.credit_button.get_height()
        is_mouse_inside_button_2 = credit_button_x <= mouse_x2 <= credit_button_x2 \
                                   and credit_button_y <= mouse_y2 <= credit_button_y2
        if pygame.mouse.get_pressed()[0] and is_mouse_inside_button_2:
            self.tube_group.empty()
            self.coin_group.empty()
            self.player = Player(200, 200, 50, self.screen, self)
            self.player_group.add(self.player)
            self.mode = GAME_CREDITS

    def handle_landing_page(self):
        self.mode = GAME_NOT_STARTED
        middle_x = WIDTH / 2
        middle_y = HEIGHT / 2

        flappy_bird_logo_x = middle_x - self.flappy_bird_logo.get_width() / 2
        flappy_bird_logo_y = middle_y - self.flappy_bird_logo.get_height() / 2 + 20
        self.screen.blit(self.flappy_bird_logo, (flappy_bird_logo_x, flappy_bird_logo_y - 200))

        play_button_x = middle_x - self.play_button.get_width() / 2 - 150
        play_button_y = middle_y - self.play_button.get_height() / 2
        self.handle_play_button(play_button_x, play_button_y)

        credit_button_x = play_button_x + self.credit_button.get_width()
        credit_button_y = middle_y - self.play_button.get_height() / 2
        self.handle_credit_button(credit_button_x, credit_button_y)

    def handle_player_tube_collision(self, player, tube):
        if player.rect.colliderect(tube.rect) and player.mode == FLYING_MODE:
            self.hit_tube_sound.play()
            # self.player_hit_tube()
            self.player.player_hit_tube()
            return True
        else:
            return False

    def player_hit_tube(self):
        self.mode = DIZZY_MODE

    def handle_game_in_session(self):
        self.create_tube()
        self.tube_group.update()
        self.coin_group.update()
        self.player_group.update()
        self.draw_score_indicator()
        self.draw_countdown_indicator()
        pygame.sprite.groupcollide(self.player_group, self.coin_group, False, True,
                                   self.handle_player_coin_collision)
        pygame.sprite.groupcollide(self.player_group, self.tube_group, False, False,
                                   self.handle_player_tube_collision)

    def handle_game_over_page(self):
        middle_x = WIDTH / 2
        middle_y = HEIGHT / 2

        game_over_msg = self.big_font.render('GAME OVER', 1, BLUE)
        game_over_x = middle_x - game_over_msg.get_width() / 2
        game_over_y = middle_y - 200
        # game_over_y = play_button_y - game_over_msg (see teacher's code to compare)

        self.screen.blit(game_over_msg, (game_over_x, game_over_y))

        play_button_y = middle_y - self.play_button.get_height() / 2
        play_button_x = middle_x - self.play_button.get_width() / 2 - 150
        self.handle_play_button(play_button_x, play_button_y)

        credit_button_x = play_button_x + self.credit_button.get_width()
        credit_button_y = middle_y - self.play_button.get_height() / 2
        self.handle_credit_button(credit_button_x, credit_button_y)

    def handle_game_won_page(self):
        middle_x = WIDTH / 2
        middle_y = HEIGHT / 2

        game_won_msg = self.big_font.render('GAME WON', 1, BLUE)
        game_won_x = middle_x - game_won_msg.get_width() / 2
        game_won_y = middle_y - 200

        self.screen.blit(game_won_msg, (game_won_x, game_won_y))

        play_button_y = middle_y - self.play_button.get_height() / 2
        play_button_x = middle_x - self.play_button.get_width() / 2 - 150
        self.handle_play_button(play_button_x, play_button_y)

        credit_button_x = play_button_x + self.credit_button.get_width()
        credit_button_y = middle_y - self.play_button.get_height() / 2
        self.handle_credit_button(credit_button_x, credit_button_y)

    def game_credits_page(self):
        self.mode = GAME_CREDITS

        credits_text_1 = f'Game Designer: Gamas Chang'
        credits_msg_1 = self.font.render(credits_text_1, 1, BLUE)
        self.screen.blit(credits_msg_1, (350, 50))

        credits_text_2 = f'Software Engineer: Gamas Chang'
        credits_msg_2 = self.font.render(credits_text_2, 1, BLUE)
        self.screen.blit(credits_msg_2, (350, 100))

        credits_text_3 = f'Music By: Audio Jungle'
        credits_msg_3 = self.font.render(credits_text_3, 1, BLUE)
        self.screen.blit(credits_msg_3, (350, 150))

        credits_text_4 = f'Game Assets: Game Dev Market'
        credits_msg_4 = self.font.render(credits_text_4, 1, BLUE)
        self.screen.blit(credits_msg_4, (350, 200))

        middle_x = WIDTH / 2
        middle_y = HEIGHT / 2

        play_button_y = middle_y - self.play_button.get_height() / 2
        play_button_x = middle_x - self.play_button.get_width() / 2 - 150
        self.handle_play_button(play_button_x, play_button_y)

        credit_button_x = play_button_x + self.credit_button.get_width()
        credit_button_y = middle_y - self.play_button.get_height() / 2
        self.handle_credit_button(credit_button_x, credit_button_y)

if __name__ == '__main__':
    sb = FlappyDuck()
    sb.game_loop()
