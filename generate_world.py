from models import *

def generate_world():
    print("Initializing...")
    # Add initial organisms
    BASE_ALGAE = 30
    # Add algae
    for _ in range(BASE_ALGAE):
        algae = Algae()
        algae_sprites.add(algae)
        all_sprites.add(algae)

    # Add small fishes
    for _ in range(int(BASE_ALGAE * 0.75)):
        small_fish = SmallFish()
        small_fish_sprites.add(small_fish)
        all_sprites.add(small_fish)

    # Add big fishes
    for _ in range(int(BASE_ALGAE * 0.2)):
        big_fish = BigFish()
        big_fish_sprites.add(big_fish)
        all_sprites.add(big_fish)

    # Add sharks
    for _ in range(int(BASE_ALGAE * 0.06)):
        shark = Shark()
        shark_sprites.add(shark)
        all_sprites.add(shark)
        
    # Add orcas
    for _ in range(int(BASE_ALGAE * 0.06)):
        orca = Orca()
        orca_sprites.add(orca)
        all_sprites.add(orca)

    print("Initializiation done.")