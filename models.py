import math
import random
import pygame
from constants import *

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
        self.width = random.randrange(10 - 3, 10 + 3)
        self.height = random.randrange(10 - 3, 10 + 3)
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WINDOW_WIDTH - 10)
        self.rect.y = random.randrange(0, math.floor(WINDOW_HEIGHT * 0.4)) # Only spawn at the top 40% of the screen 
        self.food_level = 8
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
                    reproduction_rate=1,
                    prey=[],
                    predators=[]
                ):
        
        super().__init__()
        self.instance_id = random.randrange(0, 1000000)
        self.name = name
        self.width = random.randrange(width - int((width*0.1)), width + int((width*0.1))) 
        self.height = random.randrange(height - int((height*0.1)), width + int((height*0.1))) 
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
        self.prey = prey
        self.predators = predators
        self.last_food_update_time = pygame.time.get_ticks()
        self.last_reproduction_time = pygame.time.get_ticks()
        self.creation_time = pygame.time.get_ticks()
        self.predator = None # The predator the Organism has detected
        self.predator_detected_time = 0 # The time at which the predator was detected
        self.move_direction = random.uniform(0, 2 * math.pi)
        self.move_timer = pygame.time.get_ticks() + random.randint(1000, 3000)
        
    def update(self):
        #current_time = pygame.time.get_ticks()
        self.screen_wrap()
        self.find_prey()
        # Check if organism should reproduce
        self.reproduce()
        # Reduce the food levels of the organism from hunger
        self.hunger()
        # Check if organism should die
        self.die()
        
    def screen_wrap(self):
        if self.rect.left > WINDOW_WIDTH:
            self.rect.right = 0
        elif self.rect.right < 0:
            self.rect.left = WINDOW_WIDTH
        if self.rect.top > WINDOW_HEIGHT:
            self.rect.bottom = 0
        elif self.rect.bottom < 0:
            self.rect.top = WINDOW_HEIGHT
            
    # Checks if the target is within the vision range
    def is_within_vision(self, target_sprite):
        dx = target_sprite.rect.centerx - self.rect.centerx
        dy = target_sprite.rect.centery - self.rect.centery
        distance = (dx ** 2 + dy ** 2) ** 0.5
        return distance <= self.vision_range
    
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
        
    # Predation behavior
    def find_prey(self):
        # Exit early if this organism has no preys
        if self.prey == []:
            return 0 
        # Check if a prey is nearby
        nearby_prey = [
            prey
            for prey in all_sprites
            if prey.name in self.prey and self.is_within_vision(prey)
        ]
        # Nearby prey is found
        if nearby_prey:
            target_prey = nearby_prey[0]
            # Move towards prey
            dx = target_prey.rect.centerx - self.rect.centerx
            dy = target_prey.rect.centery - self.rect.centery
            distance = max(1, (dx ** 2 + dy ** 2) ** 0.5)
            self.rect.x += (dx / distance) * self.speed
            self.rect.y += (dy / distance) * self.speed
            
            # Eat prey
            if self.rect.colliderect(target_prey.rect):
                    self.food_level += target_prey.food_level * 0.5 
                    target_prey.kill()
        # Move(coast) in random direction when no prey found
        elif not nearby_prey:
            if pygame.time.get_ticks() < self.move_timer:
                self.move_in_current_direction()
            else:
                self.choose_new_direction()
                
    def reproduce(self): #new_organism_cls
        current_time = pygame.time.get_ticks()
        if self.food_level >= self.max_food_level and current_time - self.last_reproduction_time > self.reproduction_rate:        
            self.food_level *= 0.5
            offset = 50
            new_organism = name_to_class[self.name]
            new_organism.rect.centerx = self.rect.centerx + random.randint(-(offset + self.width), offset + self.width)
            new_organism.rect.centery = self.rect.centery + random.randint(-(offset + self.height), offset + self.height)
            all_sprites.add(new_organism)
            self.last_reproduction_time = current_time
            return new_organism
    
    # Reduce the food level of the organism from hunger
    def hunger(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_food_update_time > self.food_loss_rate:
            self.food_level -= 1
            self.last_food_update_time = current_time

    # When and what happens on death
    def die(self):
        if self.food_level <= 0:
            self.kill()

class SmallFish(Organism):
    def __init__(self):
        super().__init__("small_fish", 20, 10, BLUE, 2, 3, 40, random.randint(3, 6), 10, 2000, 10000, ["algae"], [])

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
            # else:
            #     # Continue with normal behavior

class BigFish(Organism):
    def __init__(self):
        super().__init__("big_fish", 30, 20, RED, 3, 3, 40, random.randint(7, 13), 20, 3000, 10000, ["small_fish"], [])

    def update(self):
        super().update()

class Shark(Organism):
    def __init__(self):
        super().__init__("shark", 40, 30, (100, 100, 100), 4, 4, 45, random.randint(12, 18), 25, 3000, 1000, ["small_fish, big_fish"], [])

    def update(self):
        super().update()

class Orca(Organism):
    def __init__(self):
        super().__init__("orca", 50, 35, (230, 230, 230), 4, 4, 45, random.randint(12, 18), 25, 3000, 1000, ["shark"], [])

    def update(self):
        super().update()

# Name to class mapping
# Input: name of organism
# Output: corresponding class
name_to_class = {
    "algae": Algae(),
    "small_fish": SmallFish(),
    "big_fish": BigFish(),
    "shark": Shark(),
    "orca": Orca()
}