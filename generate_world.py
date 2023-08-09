import math
import random
from models import *
from constants import *
from utils import *

def generate_world():
    print("Initializing...")
    # Add initial organisms
    BASE_PLANKTON = 1000
    total_plankton = 0
    total_small_fish = 0
    total_big_fish = 0
    total_shark = 0
    total_orca = 0
    total_whale = 0
    total_generated = 0
    
    # Add rocks
    # for _ in range(100):  # Add 5 rocks
    #     x = random.randint(0, WINDOW_WIDTH - 40)  # Random x position
    #     if x > WINDOW_WIDTH // 3 and x < 2 * WINDOW_WIDTH // 3:
    #         y = random.randint(WINDOW_HEIGHT - WINDOW_HEIGHT // 4, WINDOW_HEIGHT - 40)  # Bottom 1/4th of screen
    #     else:
    #         y = random.randint(WINDOW_HEIGHT - WINDOW_HEIGHT // 8, WINDOW_HEIGHT - 40)  # Slightly higher elevation
    #     rock = Rock(x, y)
    #     all_sprites.add(rock)
    
    # Add plankton with exponential distribution
    # With most plankton at the top of the screen
    # and least plankton at the bottom of the screen
    y_values = generate_exponential_numbers(0, WINDOW_HEIGHT, BASE_PLANKTON)
    for i in range(BASE_PLANKTON):
        #y = y_values[0]
        y = random.choice(y_values)
        # index = y_values.index(y)
        # del y_values[index]
        del y_values[0]
        plankton = Plankton(x=random.randrange(WINDOW_WIDTH - 5), y=y)
        all_sprites.add(plankton)
        total_plankton += 1
        
    # Add small fishes
    for i in range(math.ceil(BASE_PLANKTON * 0.04)):
        small_fish = SmallFish()
        all_sprites.add(small_fish)
        total_small_fish += 1

    # Add big fishes
    for i in range(math.ceil(BASE_PLANKTON * 0.004)):
        big_fish = BigFish()
        all_sprites.add(big_fish)
        total_big_fish += 1

    # Add sharks
    for i in range(math.ceil(BASE_PLANKTON * 0.001)):
        shark = Shark()
        all_sprites.add(shark)
        total_shark += 1

    # Add orcas
    for i in range(math.ceil(BASE_PLANKTON * 0.0004)):
        orca = Orca()
        all_sprites.add(orca)
        total_orca += 1

    # Add whales
    for i in range(math.ceil(BASE_PLANKTON * 0.0004)):
        whale = Whale()
        all_sprites.add(whale)
        total_whale += 1
        
    total_generated = sum([total_plankton, total_small_fish, total_big_fish, total_shark, total_orca, total_whale])

    print("Number of plankton generated: ", total_plankton)   
    print("Number of small_fish generated: ", total_small_fish)
    print("Number of big_fish generated: ", total_big_fish)
    print("Number of shark generated: ", total_shark)
    print("Number of orca generated: ", total_orca)
    print("Number of whale generated: ", total_whale)
    print("-------")
    print("Total non-plankton generated: ", total_generated-total_plankton)
    print("Total organisms generated: ", total_generated)

    print("Initializiation done.")
