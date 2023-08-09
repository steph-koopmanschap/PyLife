import pygame
from pygame.math import Vector2
import sys
import random
import math

pygame.init()

# Set up the dimensions of the game window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
# Game loop variables
FPS = 60  # Frames per second
clock = pygame.time.Clock()
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Create the game window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("PyLife")

# Sprite groups
all_sprites = pygame.sprite.Group()
algae_sprites = pygame.sprite.Group()
small_fish_sprites = pygame.sprite.Group()
big_fish_sprites = pygame.sprite.Group()
shark_sprites = pygame.sprite.Group()
orca_sprites = pygame.sprite.Group()

class Algae(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.name = "algae"
        self.width = 10
        self.height = 10
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WINDOW_WIDTH - 10)
        self.rect.y = random.randrange(0, math.floor(WINDOW_HEIGHT * 0.4)) # Only spawn at the top 40% of the screen 
        self.reproduction_time = random.randint(9000, 10000)
        self.lifespan = random.randint(10000, 12400) # Lifespan in miliseconds
        self.last_reproduction_time = pygame.time.get_ticks()
        self.creation_time = pygame.time.get_ticks()

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_reproduction_time > self.reproduction_time:
            self.reproduce()
            self.last_reproduction_time = current_time

        if current_time - self.creation_time > self.lifespan:
            self.die()
        else:
            # Make the Algae more transparant as its lifespan decreases
            # Calculate the remaining lifespan as a fraction (value between 0 and 1)
            remaining_lifespan_fraction = (self.lifespan - (current_time - self.creation_time)) / self.lifespan
            # Calculate the alpha value based on the remaining lifespan fraction
            alpha = int(remaining_lifespan_fraction * 255)
            # Set the alpha value to change the transparency of the Algae
            self.image.set_alpha(alpha)

    def reproduce(self):
        for i in range(random.randint(1, 3)):
            new_algae = Algae()
            new_algae.rect.centerx = self.rect.centerx + random.randint(-50, 50)
            new_algae.rect.centery = self.rect.centery + random.randint(-50, 50)
            algae_sprites.add(new_algae)
            all_sprites.add(new_algae)

    def die(self):
        self.kill()

class Organism(pygame.sprite.Sprite):
    def __init__(self, 
                    name="organism", 
                    width=1,
                    height=1, 
                    color=BLACK, 
                    speed=1, 
                    max_speed=1, 
                    vision_range=1, 
                    food_level=1, 
                    max_food_level=1, 
                    food_loss_rate=1, 
                    reproduction_rate=1
                ):
        
        super().__init__()
        self.name = name
        self.width = width
        self.height = height
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WINDOW_WIDTH - width)
        self.rect.y = random.randrange(WINDOW_HEIGHT - height)
        self.speed = speed
        self.max_speed = max_speed
        self.vision_range = vision_range
        self.food_level = food_level
        self.max_food_level = max_food_level
        self.food_loss_rate = food_loss_rate
        self.reproduction_rate = reproduction_rate
        self.last_food_update_time = pygame.time.get_ticks()
        self.last_reproduction_time = pygame.time.get_ticks()
        self.creation_time = pygame.time.get_ticks()
        
    def update(self):
        current_time = pygame.time.get_ticks()

class SmallFish(Organism):
    def __init__(self):
        super().__init__("small_fish", 20, 10, BLUE, 2, 3, 40, random.randint(3, 6), 10, 2000, 10000)
        self.move_direction = random.uniform(0, 2 * math.pi)
        self.move_timer = pygame.time.get_ticks() + random.randint(1000, 3000)
        self.predator = None # The predator the SmallFish has detected
        self.predator_detected_time = 0 # The time at which the predator was detected

    # Checks if the target is within the vision range
    def is_within_vision(self, target_sprite):
        dx = target_sprite.rect.centerx - self.rect.centerx
        dy = target_sprite.rect.centery - self.rect.centery
        distance = (dx ** 2 + dy ** 2) ** 0.5
        return distance <= self.vision_range

    def update(self):
        super().update()
        current_time = pygame.time.get_ticks()

        # Check if the SmallFish has a predator and if the predator is still within the vision range
        if self.predator and self.is_within_vision(self.predator):
            # Calculate the distance and direction to the predator
            dx = self.predator.rect.centerx - self.rect.centerx
            dy = self.predator.rect.centery - self.rect.centery
            distance = max(1, (dx ** 2 + dy ** 2) ** 0.5)

            # Move away from the predator at maximum speed
            self.rect.x -= (dx / distance) * self.max_speed
            self.rect.y -= (dy / distance) * self.max_speed

            # Update the predator detection time
            self.predator_detected_time = current_time
        else:
            # If no predator or predator is out of vision, move normally
            if current_time - self.predator_detected_time < 2000:
                # Move away at maximum speed for 2 seconds even if predator is not detected currently
                self.move_in_current_direction()
            else:
                # Continue with normal behavior
                if current_time - self.last_food_update_time > self.food_loss_rate:
                    self.food_level -= 1
                    self.last_food_update_time = current_time

                # Check if organism should die
                self.die()

                if self.food_level >= self.max_food_level and current_time - self.last_reproduction_time > self.reproduction_rate:
                    self.reproduce()
                    self.last_reproduction_time = current_time
            
    def reproduce(self):
        self.food_level *= 0.5
        new_fish = SmallFish()
        new_fish.rect.centerx = self.rect.centerx + random.randint(-50, 50)
        new_fish.rect.centery = self.rect.centery + random.randint(-50, 50)
        small_fish_sprites.add(new_fish)
        all_sprites.add(new_fish)

    # When and what happens on death
    def die(self):
        if self.food_level <= 0:
            self.kill()

    # This is very jittery
    def move_randomly(self):
        angle = random.uniform(0, 2 * math.pi)
        dx = math.cos(angle) * self.speed
        dy = math.sin(angle) * self.speed
        self.rect.x += dx + random.uniform(-0.2, 0.2)  # Small random offset
        self.rect.y += dy + random.uniform(-0.2, 0.2)  # Small random offset

    def move_in_current_direction(self):
        dx = math.cos(self.move_direction) * self.speed
        dy = math.sin(self.move_direction) * self.speed
        self.rect.x += dx
        self.rect.y += dy

    def choose_new_direction(self):
        self.move_direction = random.uniform(0, 2 * math.pi)
        self.move_timer = pygame.time.get_ticks() + random.randint(1000, 3000)

class BigFish(Organism):
    def __init__(self):
        super().__init__("big_fish", 30, 20, RED, 3, 3, 40, random.randint(7, 13), 20, 3000, 10000)
        self.move_direction = random.uniform(0, 2 * math.pi)
        self.move_timer = pygame.time.get_ticks() + random.randint(1000, 3000)
        self.predator = None # The predator the SmallFish has detected
        self.predator_detected_time = 0 # The time at which the predator was detected

    # Checks if the target is within the vision range
    def is_within_vision(self, target_sprite):
        dx = target_sprite.rect.centerx - self.rect.centerx
        dy = target_sprite.rect.centery - self.rect.centery
        distance = (dx ** 2 + dy ** 2) ** 0.5
        return distance <= self.vision_range

    def update(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_food_update_time > self.food_loss_rate:
            self.food_level -= 1
            self.last_food_update_time = current_time

        # Check if organism should die
        self.die()

        if self.food_level >= self.max_food_level and current_time - self.last_reproduction_time > self.reproduction_rate:
            self.reproduce()
            self.last_reproduction_time = current_time

    def reproduce(self):
        self.food_level *= 0.5
        new_fish = BigFish()
        new_fish.rect.centerx = self.rect.centerx + random.randint(-60, 60)
        new_fish.rect.centery = self.rect.centery + random.randint(-60, 60)
        big_fish_sprites.add(new_fish)
        all_sprites.add(new_fish)# When and what happens on death
    def die(self):
        if self.food_level <= 0:
            self.kill()

    # When and what happens on death
    def die(self):
        if self.food_level <= 0:
            self.kill()

    # This is very jittery
    def move_randomly(self):
        angle = random.uniform(0, 2 * math.pi)
        self.rect.x += math.cos(angle) * self.speed
        self.rect.y += math.sin(angle) * self.speed

    def move_in_current_direction(self):
        dx = math.cos(self.move_direction) * self.speed
        dy = math.sin(self.move_direction) * self.speed
        self.rect.x += dx
        self.rect.y += dy

    def choose_new_direction(self):
        self.move_direction = random.uniform(0, 2 * math.pi)
        self.move_timer = pygame.time.get_ticks() + random.randint(1000, 3000)

class Shark(Organism):
    def __init__(self):
        super().__init__("shark", 40, 30, (100, 100, 100), 4, 4, 45, random.randint(12, 18), 25, 3000, 1000)
        self.move_direction = random.uniform(0, 2 * math.pi)
        self.move_timer = pygame.time.get_ticks() + random.randint(1000, 3000)

    # Checks if the target is within the vision range
    def is_within_vision(self, target_sprite):
        dx = target_sprite.rect.centerx - self.rect.centerx
        dy = target_sprite.rect.centery - self.rect.centery
        distance = (dx ** 2 + dy ** 2) ** 0.5
        return distance <= self.vision_range

    def update(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_food_update_time > self.food_loss_rate:
            self.food_level -= 1
            self.last_food_update_time = current_time

        # Check if organism should die
        self.die()

        # reproduction behaviour
        if self.food_level >= self.max_food_level and current_time - self.last_reproduction_time > self.reproduction_rate:
            self.reproduce()
            self.last_reproduction_time = current_time

    def reproduce(self):
        self.food_level *= 0.5
        new_shark = Shark()
        new_shark.rect.centerx = self.rect.centerx + random.randint(-80, 80)
        new_shark.rect.centery = self.rect.centery + random.randint(-80, 80)
        shark_sprites.add(new_shark)
        all_sprites.add(new_shark)

    # When and what happens on death
    def die(self):
        if self.food_level <= 0:
            self.kill()

    def move_in_current_direction(self):
        dx = math.cos(self.move_direction) * self.speed
        dy = math.sin(self.move_direction) * self.speed
        self.rect.x += dx
        self.rect.y += dy

    def choose_new_direction(self):
        self.move_direction = random.uniform(0, 2 * math.pi)
        self.move_timer = pygame.time.get_ticks() + random.randint(1000, 3000)
        
class Orca(Organism):
    def __init__(self):
        super().__init__("orca", 50, 35, (230, 230, 230), 4, 4, 45, random.randint(12, 18), 25, 3000, 1000)
        self.move_direction = random.uniform(0, 2 * math.pi)
        self.move_timer = pygame.time.get_ticks() + random.randint(1000, 3000)

    # Checks if the target is within the vision range
    def is_within_vision(self, target_sprite):
        dx = target_sprite.rect.centerx - self.rect.centerx
        dy = target_sprite.rect.centery - self.rect.centery
        distance = (dx ** 2 + dy ** 2) ** 0.5
        return distance <= self.vision_range

    def update(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_food_update_time > self.food_loss_rate:
            self.food_level -= 1
            self.last_food_update_time = current_time

        # Check if organism should die
        self.die()

        # reproduction behaviour
        if self.food_level >= self.max_food_level and current_time - self.last_reproduction_time > self.reproduction_rate:
            self.reproduce()
            self.last_reproduction_time = current_time

    def reproduce(self):
        self.food_level *= 0.5
        new_orca = Orca()
        new_orca.rect.centerx = self.rect.centerx + random.randint(-80, 80)
        new_orca.rect.centery = self.rect.centery + random.randint(-80, 80)
        shark_sprites.add(new_orca)
        all_sprites.add(new_orca)

    # When and what happens on death
    def die(self):
        if self.food_level <= 0:
            self.kill()

    def move_in_current_direction(self):
        dx = math.cos(self.move_direction) * self.speed
        dy = math.sin(self.move_direction) * self.speed
        self.rect.x += dx
        self.rect.y += dy

    def choose_new_direction(self):
        self.move_direction = random.uniform(0, 2 * math.pi)
        self.move_timer = pygame.time.get_ticks() + random.randint(1000, 3000)

# Clear the screen
def clear_screen():
    window.fill(BLACK)
    #window.fill((4, 217, 255)) # Light blue
    #window.fill((255, 255, 255))

# Update game logic here
def update():
    all_sprites.update()

    # Screen wrapping
    for sprite in all_sprites:
        if sprite.rect.left > WINDOW_WIDTH:
            sprite.rect.right = 0
        elif sprite.rect.right < 0:
            sprite.rect.left = WINDOW_WIDTH
        if sprite.rect.top > WINDOW_HEIGHT:
            sprite.rect.bottom = 0
        elif sprite.rect.bottom < 0:
            sprite.rect.top = WINDOW_HEIGHT

    # Small fish behavior
    for small_fish in small_fish_sprites:
        nearby_algae = [
                algae
                for algae in algae_sprites
                if small_fish.is_within_vision(algae)
        ]
        if nearby_algae:
            target_algae = nearby_algae[0]
            dx = target_algae.rect.centerx - small_fish.rect.centerx
            dy = target_algae.rect.centery - small_fish.rect.centery
            distance = max(1, (dx ** 2 + dy ** 2) ** 0.5)
            small_fish.rect.x += (dx / distance) * small_fish.speed
            small_fish.rect.y += (dy / distance) * small_fish.speed

            if small_fish.rect.colliderect(target_algae.rect):
                small_fish.food_level += 2
                target_algae.kill()
        # Move(coast) in random direction when no prey found
        elif not nearby_algae:
            if pygame.time.get_ticks() < small_fish.move_timer:
                small_fish.move_in_current_direction()
            else:
                small_fish.choose_new_direction()

    # Big fish behavior
    for big_fish in big_fish_sprites:
        nearby_small_fish = [
                small_fish
                for small_fish in small_fish_sprites
                if big_fish.is_within_vision(small_fish)
        ]
        if nearby_small_fish:
            target_small_fish = nearby_small_fish[0]
            dx = target_small_fish.rect.centerx - big_fish.rect.centerx
            dy = target_small_fish.rect.centery - big_fish.rect.centery
            distance = max(1, (dx ** 2 + dy ** 2) ** 0.5)
            big_fish.rect.x += (dx / distance) * 4
            big_fish.rect.y += (dy / distance) * 4

            if big_fish.rect.colliderect(target_small_fish.rect):
                big_fish.food_level += 3
                target_small_fish.kill()
        # Move(coast) in random direction when no prey found
        elif not nearby_small_fish:
            if pygame.time.get_ticks() < big_fish.move_timer:
                big_fish.move_in_current_direction()
            else:
                big_fish.choose_new_direction()

    # Shark behavior
    for shark in shark_sprites:
        nearby_big_fish = [
            big_fish
            for big_fish in big_fish_sprites
            if shark.is_within_vision(big_fish)
        ]
        nearby_small_fish = [
            small_fish
            for small_fish in small_fish_sprites
            if shark.is_within_vision(small_fish)
        ]
        if nearby_big_fish:
            target_big_fish = nearby_big_fish[0]
            dx = target_big_fish.rect.centerx - shark.rect.centerx
            dy = target_big_fish.rect.centery - shark.rect.centery
            distance = max(1, (dx ** 2 + dy ** 2) ** 0.5)
            shark.rect.x += (dx / distance) * 4
            shark.rect.y += (dy / distance) * 4

            if shark.rect.colliderect(target_big_fish.rect):
                shark.food_level += 4
                target_big_fish.kill()
        elif nearby_small_fish:
            target_small_fish = nearby_small_fish[0]
            dx = target_small_fish.rect.centerx - shark.rect.centerx
            dy = target_small_fish.rect.centery - shark.rect.centery
            distance = max(1, (dx ** 2 + dy ** 2) ** 0.5)
            shark.rect.x += (dx / distance) * 4
            shark.rect.y += (dy / distance) * 4

            if shark.rect.colliderect(target_small_fish.rect):
                shark.food_level += 2
                target_small_fish.kill()
        # Move(coast) in random direction when no prey found
        elif not nearby_big_fish or not nearby_small_fish:
            if pygame.time.get_ticks() < shark.move_timer:
                shark.move_in_current_direction()
            else:
                shark.choose_new_direction()
                
    # Orca behavior
    for orca in orca_sprites:
        nearby_shark = [
            shark
            for shark in shark_sprites
            if orca.is_within_vision(shark)
        ]
        if nearby_shark:
            target_shark = nearby_shark[0]
            dx = target_shark.rect.centerx - shark.rect.centerx
            dy = target_shark.rect.centery - shark.rect.centery
            distance = max(1, (dx ** 2 + dy ** 2) ** 0.5)
            orca.rect.x += (dx / distance) * 4
            orca.rect.y += (dy / distance) * 4

            if orca.rect.colliderect(target_shark.rect):
                orca.food_level += 4
                target_shark.kill()
        # Move(coast) in random direction when no prey found
        elif not nearby_shark:
            if pygame.time.get_ticks() < orca.move_timer:
                orca.move_in_current_direction()
            else:
                orca.choose_new_direction()

# Draw game elements here
def draw():
    all_sprites.draw(window)

# Game loop
def game_loop():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        update()
        clear_screen()
        draw()

        # Update the display
        pygame.display.update()
        clock.tick(FPS)

def init():
    print("Initializing...")
    # Add initial organisms
    # Add algae
    for _ in range(30):
        algae = Algae()
        algae_sprites.add(algae)
        all_sprites.add(algae)

    # Add small fishes
    for _ in range(11):
        small_fish = SmallFish()
        small_fish_sprites.add(small_fish)
        all_sprites.add(small_fish)

    # Add big fishes
    for _ in range(6):
        big_fish = BigFish()
        big_fish_sprites.add(big_fish)
        all_sprites.add(big_fish)

    # Add sharks
    for _ in range(2):
        shark = Shark()
        shark_sprites.add(shark)
        all_sprites.add(shark)
        
    # Add orcas
    for _ in range(2):
        orca = Orca()
        orca_sprites.add(orca)
        all_sprites.add(orca)

    print("Initializiation done.")

def start():
    init()
    game_loop()

start()
#if __name__ = __main__:




