import pygame
import random

# --- Configuration & Colors ---
WIDTH, HEIGHT = 800, 600
SNAKE_SIZE = 20
SPEED = 15

COLOR_BG = (28, 28, 30)
COLOR_SNAKE = (48, 209, 88)
COLOR_FOOD = (255, 55, 95)
COLOR_TEXT = (242, 242, 247)
COLOR_OVERLAY = (0, 0, 0, 150) # Semi-transparent black

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Neon Snake v1.0")
        self.clock = pygame.time.Clock()
        self.font_main = pygame.font.SysFont("helvetica", 50, bold=True)
        self.font_sub = pygame.font.SysFont("helvetica", 30)
        self.reset_game()

    def reset_game(self):
        self.x, self.y = WIDTH // 2, HEIGHT // 2
        self.x_speed, self.y_speed = 0, 0
        self.snake_list = []
        self.snake_length = 1
        self.score = 0
        self.spawn_food()
        self.is_game_over = False

    def spawn_food(self):
        self.food_x = round(random.randrange(0, WIDTH - SNAKE_SIZE) / 20.0) * 20.0
        self.food_y = round(random.randrange(0, HEIGHT - SNAKE_SIZE) / 20.0) * 20.0

    def show_game_over(self):
        # Create a semi-transparent surface
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill(COLOR_OVERLAY)
        self.screen.blit(overlay, (0,0))

        # Render Text
        lost_txt = self.font_main.render("Haha You Lost!", True, COLOR_FOOD)
        score_txt = self.font_sub.render(f"Final Score: {self.score}", True, COLOR_TEXT)
        retry_txt = self.font_sub.render("Press [R] to Try Again or [Q] to Quit", True, (150, 150, 150))

        # Center Text
        self.screen.blit(lost_txt, (WIDTH//2 - lost_txt.get_width()//2, HEIGHT//2 - 60))
        self.screen.blit(score_txt, (WIDTH//2 - score_txt.get_width()//2, HEIGHT//2))
        self.screen.blit(retry_txt, (WIDTH//2 - retry_txt.get_width()//2, HEIGHT//2 + 60))
        
        pygame.display.update()

    def run(self):
        running = True
        while running:
            # --- Event Handling ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.KEYDOWN:
                    if self.is_game_over:
                        if event.key == pygame.K_r:
                            self.reset_game()
                        if event.key == pygame.K_q:
                            running = False
                    else:
                        if event.key == pygame.K_LEFT and self.x_speed <= 0:
                            self.x_speed, self.y_speed = -SNAKE_SIZE, 0
                        elif event.key == pygame.K_RIGHT and self.x_speed >= 0:
                            self.x_speed, self.y_speed = SNAKE_SIZE, 0
                        elif event.key == pygame.K_UP and self.y_speed <= 0:
                            self.y_speed, self.x_speed = -SNAKE_SIZE, 0
                        elif event.key == pygame.K_DOWN and self.y_speed >= 0:
                            self.y_speed, self.x_speed = SNAKE_SIZE, 0

            if not self.is_game_over:
                # --- Logic ---
                self.x += self.x_speed
                self.y += self.y_speed

                # Wall Collision
                if self.x >= WIDTH or self.x < 0 or self.y >= HEIGHT or self.y < 0:
                    self.is_game_over = True

                # Body Collision
                snake_head = [self.x, self.y]
                if snake_head in self.snake_list[:-1]:
                    self.is_game_over = True

                self.snake_list.append(snake_head)
                if len(self.snake_list) > self.snake_length:
                    del self.snake_list[0]

                # Food Collision
                if self.x == self.food_x and self.y == self.food_y:
                    self.spawn_food()
                    self.snake_length += 1
                    self.score += 10

                # --- Drawing ---
                self.screen.fill(COLOR_BG)
                
                # Draw Food
                pygame.draw.circle(self.screen, COLOR_FOOD, (int(self.food_x + SNAKE_SIZE/2), int(self.food_y + SNAKE_SIZE/2)), SNAKE_SIZE//2)

                # Draw Snake
                for block in self.snake_list:
                    pygame.draw.rect(self.screen, COLOR_SNAKE, [block[0], block[1], SNAKE_SIZE, SNAKE_SIZE], border_radius=4)

                # Live Score
                score_val = self.font_sub.render(f"Score: {self.score}", True, COLOR_TEXT)
                self.screen.blit(score_val, [20, 20])
                
                pygame.display.update()
            else:
                # Show Game Over Screen
                self.show_game_over()

            self.clock.tick(SPEED)

        pygame.quit()

if __name__ == "__main__":
    game = SnakeGame()
    game.run()