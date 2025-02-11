import pygame
import math
import random
import time

from functions.load_and_scale import load_and_scale_image
from models.achivement_popup import AchievementPopup
from models.inventoryItem import InventoryItem
from models.constants import *
from models.constants import achievements
from models.plant import Plant
from models.sleep_popup import SleepPopup
from models.tile import Tile

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Starfarm')

river_tile = pygame.image.load('assets/tilemap/river.png').convert()
grass_tile = pygame.image.load('assets/tilemap/grass.png').convert()
farmland_tile = pygame.image.load('assets/tilemap/farm.png').convert()
bush_tile = pygame.image.load('assets/tilemap/bush.png').convert_alpha()

river_tile = pygame.transform.scale(river_tile, TILE_SIZE)
grass_tile = pygame.transform.scale(grass_tile, TILE_SIZE)
farmland_tile = pygame.transform.scale(farmland_tile, TILE_SIZE)
bush_tile = pygame.transform.scale(bush_tile, TILE_SIZE)

inventory_slot_image = load_and_scale_image('assets/inventory/Inventory_background.png', INVENTORY_SLOT_SIZE)
seedbag_image = load_and_scale_image('assets/plants/seeds/deathbell.png', (60, 60))
rose_seed_image = load_and_scale_image('assets/plants/seeds/rose.png', (60, 60))
pointy_seed_image = load_and_scale_image('assets/plants/seeds/pointy.png', (60, 60))
daisy_seed_image = load_and_scale_image('assets/plants/seeds/daisy.png', (60, 60))
inventory_select_image = load_and_scale_image('assets/inventory/Inventory_select.png', INVENTORY_SLOT_SIZE)
sunflower_seed_image = load_and_scale_image('assets/plants/seeds/sunflower.png', (60, 60))
hydrangea_seed_image = load_and_scale_image('assets/plants/seeds/hydrangea.png', (60, 60))
lavender_seed_image = load_and_scale_image('assets/plants/seeds/lavender.png', (60, 60))
pink_rose_seed_image = load_and_scale_image('assets/plants/seeds/pink_rose.png', (60, 60))
magic_flower_seed_image = load_and_scale_image('assets/plants/seeds/magic_flower.png', (60, 60))
watering_can_image = load_and_scale_image('assets/inventory/watering_can.png', (60, 60))

last_buy_time = 0
BUY_COOLDOWN = 0.2

last_consume_time = 0
CONSUME_COOLDOWN = 0.3

MOVEMENT_SPEED = 1
inventory = [None] * NUM_INVENTORY_SLOTS

inventory[1] = InventoryItem(
    item_type="tool",
    image=watering_can_image,
    name="Watering Can",
    quantity=1,
    price=0
)

inventory[2] = InventoryItem(
    item_type="seed",
    image=seedbag_image,
    name="Bluebell Seeds",
    quantity=10,
    price=100
)

achievements = achievements

DAY_DURATION = DAY_DURATION

tile_cooldown = {}
selected_item_index = 0

current_cycle_time = 0
is_day = True
last_time = time.time()

BUY_POSITION = (MAP_WIDTH - 4, 0)
BUY_GRID_SIZE = 15
buy_grid = [None] * BUY_GRID_SIZE
buy_active = False

buy_grid[0] = InventoryItem(
    item_type="seed",
    image=seedbag_image,
    name="Bluebell Seeds",
    quantity=1,
    price=BUY_PRICES["Bluebell Seeds"]
)
buy_grid[1] = InventoryItem(
    item_type="seed",
    image=rose_seed_image,
    name="Rose Seeds",
    quantity=1,
    price=BUY_PRICES["Rose Seeds"]
)

buy_grid[2] = InventoryItem(
    item_type="seed",
    image=pointy_seed_image,
    name="Pointy Seeds",
    quantity=1,
    price=BUY_PRICES["Pointy Seeds"]
)

buy_grid[3] = InventoryItem(
    item_type="seed",
    image=daisy_seed_image,
    name="Daisy Seeds",
    quantity=1,
    price=BUY_PRICES["Daisy Seeds"]
)

buy_grid[4] = InventoryItem(
    item_type="seed",
    image=sunflower_seed_image,
    name="Sunflower Seeds",
    quantity=1,
    price=BUY_PRICES["Sunflower Seeds"]
)
buy_grid[5] = InventoryItem(
    item_type="seed",
    image=hydrangea_seed_image,
    name="Hydrangea Seeds",
    quantity=1,
    price=BUY_PRICES["Hydrangea Seeds"]
)
buy_grid[6] = InventoryItem(
    item_type="seed",
    image=lavender_seed_image,
    name="Lavender Seeds",
    quantity=1,
    price=BUY_PRICES["Lavender Seeds"]
)
buy_grid[7] = InventoryItem(
    item_type="seed",
    image=pink_rose_seed_image,
    name="Pink Rose Seeds",
    quantity=1,
    price=BUY_PRICES["Pink Rose Seeds"]
)
buy_grid[8] = InventoryItem(
    item_type="seed",
    image=magic_flower_seed_image,
    name="Magic Flower Seeds",
    quantity=1,
    price=BUY_PRICES["Magic Flower Seeds"]
)

sold_crops = {
    "deathBell": False,
    "rose": False,
    "pointy": False,
    "daisy": False,
    "sunflower": False,
    "hydrangea": False,
    "lavender": False,
    "pink_rose": False,
    "magic_flower": False
}

plants = []


class Character:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = "front"
        self.facing_left = False
        self.is_moving = False
        self.is_watering = False

        self.animation_frames = {
            "front": [pygame.transform.scale(pygame.image.load(f'assets/character/front{i}.png').convert_alpha(),
                                             CHARACTER_SIZE) for i in range(1, 4)],
            "back": [pygame.transform.scale(pygame.image.load(f'assets/character/back{i}.png').convert_alpha(),
                                            CHARACTER_SIZE) for i in range(1, 4)],
            "side": [pygame.transform.scale(pygame.image.load(f'assets/character/side{i}.png').convert_alpha(),
                                            CHARACTER_SIZE) for i in range(1, 4)],
            "idle": [pygame.transform.scale(pygame.image.load(f'assets/character/front1.png').convert_alpha(),
                                            CHARACTER_SIZE)],
            "watering": [pygame.transform.scale(pygame.image.load(f'assets/character/watering{i}.png').convert_alpha(),
                                                WATERING_CHARACTER_SIZE) for i in range(1, 4)]
        }

        self.current_frame = 0
        self.frame_counter = 0
        self.frame_delay = 10
        self.watering_frame_delay = 20

        pygame.mixer.init()

        self.watering_sound = pygame.mixer.Sound("assets/sounds/wateringcan.mp3")
        self.walking_sound = pygame.mixer.Sound("assets/sounds/walking.mp3")
        self.walking_sound.set_volume(2)

    def move(self, dx, dy):
        new_x = self.x + dx / 25
        new_y = self.y + dy / 25

        tile_x = round(new_x)
        tile_y = round(new_y)

        if 0 <= tile_x < MAP_WIDTH and 0 <= tile_y < MAP_HEIGHT:
            tile = tilemap[tile_y][tile_x]

            if tile.is_walkable and not tile.is_river:
                self.x = new_x
                self.y = new_y
                self.x = max(0, min(MAP_WIDTH - 1, self.x))
                self.y = max(0, min(MAP_HEIGHT - 1, self.y))
        else:
            return

        if dx != 0 or dy != 0:
            if not self.is_moving:
                self.walking_sound.play(-1)
            self.is_moving = True
        else:
            if self.is_moving:
                self.walking_sound.stop()
            self.is_moving = False

    def start_watering(self):
        if not self.is_moving:
            self.is_watering = True
            self.watering_sound.play()

    def update_animation(self):
        self.frame_counter += 1

        if self.is_watering:
            frame_delay = self.watering_frame_delay
        else:
            frame_delay = self.frame_delay

        if self.frame_counter >= frame_delay:
            self.frame_counter = 0
            if self.is_watering:
                self.current_frame = (self.current_frame + 1) % len(self.animation_frames["watering"])
                if self.current_frame == 0:
                    self.is_watering = False
            elif self.is_moving:
                self.current_frame = (self.current_frame + 1) % len(self.animation_frames[self.direction])
            else:
                self.current_frame = 0

    def draw(self, screen):
        if self.is_watering:
            character_image = self.animation_frames["watering"][self.current_frame]
        elif self.is_moving:
            character_image = self.animation_frames[self.direction][self.current_frame]
        else:
            character_image = self.animation_frames["idle"][0]

        if self.direction == "side" and self.facing_left:
            character_image = pygame.transform.flip(character_image, True, False)

        character_draw_x = self.x * TILE_SIZE[0] + (TILE_SIZE[0] - CHARACTER_SIZE[0]) // 2
        character_draw_y = self.y * TILE_SIZE[1] + (TILE_SIZE[1] - CHARACTER_SIZE[1]) // 2

        screen.blit(character_image, (character_draw_x, character_draw_y))


achievement_popup = AchievementPopup()
sleep_popup = SleepPopup()

character = Character(MAP_WIDTH // 2, MAP_HEIGHT // 2)

SELL_POSITION = (MAP_WIDTH - 3, 0)
sell_grid = [None] * 9
sell_active = False

current_energy = MAX_ENERGY

dragging_item = None
dragging_item_index = None
dragging_item_offset = (0, 0)


def generate_map():
    tilemap = [[None for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]

    river_frequency = 0.2
    river_amplitude = 3

    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            wave_position = int(river_amplitude * math.sin(river_frequency * x + y))

            if abs(y - (MAP_HEIGHT // 2 + wave_position)) < 2:
                tilemap[y][x] = Tile('river', river_tile, (x, y))
                tilemap[y][x].is_river = True
                tilemap[y][x].is_walkable = False
            else:
                tilemap[y][x] = Tile('grass', grass_tile, (x, y))
                tilemap[y][x].is_walkable = True

    middle_width_start = MAP_WIDTH // 4
    middle_width_end = MAP_WIDTH * 3 // 4
    middle_height_start = MAP_HEIGHT // 4
    middle_height_end = MAP_HEIGHT * 3 // 4

    for y in range(middle_height_start, middle_height_end):
        for x in range(middle_width_start, middle_width_end):
            tilemap[y][x] = Tile('farmland', farmland_tile, (x, y))
            tilemap[y][x].is_walkable = True

    tilemap[SELL_POSITION[1]][SELL_POSITION[0]] = Tile('sell', grass_tile, SELL_POSITION)
    tilemap[BUY_POSITION[1]][BUY_POSITION[0]] = Tile('buy', grass_tile, BUY_POSITION)
    tilemap[SELL_POSITION[1]][SELL_POSITION[0]].is_walkable = True
    tilemap[BUY_POSITION[1]][BUY_POSITION[0]].is_walkable = True

    house1_image = pygame.image.load("assets/tilemap/house1.png").convert_alpha()
    house2_image = pygame.image.load("assets/tilemap/house2.png").convert_alpha()
    house3_image = pygame.image.load("assets/tilemap/house3.png").convert_alpha()
    house4_image = pygame.image.load("assets/tilemap/house4.png").convert_alpha()

    house_width = 64
    house_height = 64

    house1_image = pygame.transform.scale(house1_image, (house_width, house_height))
    house2_image = pygame.transform.scale(house2_image, (house_width, house_height))
    house3_image = pygame.transform.scale(house3_image, (house_width, house_height))
    house4_image = pygame.transform.scale(house4_image, (house_width, house_height))

    grass_color = grass_tile.get_at((0, 0))

    def create_house_tile(image, grass_color):
        new_surface = pygame.Surface((house_width, house_height), pygame.SRCALPHA)
        new_surface.fill(grass_color)
        new_surface.blit(image, (0, 0))
        return new_surface

    house1_image = create_house_tile(house1_image, grass_color)
    house2_image = create_house_tile(house2_image, grass_color)
    house3_image = create_house_tile(house3_image, grass_color)
    house4_image = create_house_tile(house4_image, grass_color)

    house_tiles = [
        (0, 0, house1_image), (0, 1, house2_image),
        (1, 0, house3_image), (1, 1, house4_image)
    ]

    for y, x, house_part in house_tiles:
        tilemap[y][x] = Tile('house', house_part, (x, y))
        tilemap[y][x].is_walkable = False

    tilemap[1][0].is_walkable = True
    tilemap[1][1].is_walkable = True

    return tilemap


def generate_bushes(tilemap):
    bushes_placed = 0
    max_bushes = random.randint(4, 5)
    bush_positions = []

    while bushes_placed < max_bushes:
        x = random.randint(0, MAP_WIDTH - 1)
        y = random.randint(0, MAP_HEIGHT - 1)

        if tilemap[y][x].tile_type == 'grass' and (x, y) not in bush_positions:
            bush_positions.append((x, y))
            bushes_placed += 1

    return bush_positions


def is_inventory_full():
    for slot in inventory:
        if slot is None:
            return False
    return True


def draw_map(tilemap, bush_positions):
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            tilemap[y][x].draw(screen)
            if (x, y) in bush_positions:
                screen.blit(bush_tile, (x * TILE_SIZE[0], y * TILE_SIZE[1]))


def draw_inventory():
    total_width = NUM_INVENTORY_SLOTS * INVENTORY_SLOT_SIZE[0]
    start_x = (SCREEN_WIDTH - total_width) // 2
    y = MAP_HEIGHT * TILE_SIZE[1]

    inventory_background_rect = pygame.Rect(0, y, SCREEN_WIDTH, INVENTORY_SLOT_SIZE[1])
    pygame.draw.rect(screen, BROWN, inventory_background_rect)

    font = pygame.font.Font(None, 24)
    mouse_x, mouse_y = pygame.mouse.get_pos()

    for i in range(NUM_INVENTORY_SLOTS):
        slot_x = start_x + i * INVENTORY_SLOT_SIZE[0]
        screen.blit(inventory_slot_image, (slot_x, y))

        if inventory[i]:
            item_image = inventory[i].image
            screen.blit(
                item_image,
                (slot_x + (INVENTORY_SLOT_SIZE[0] - item_image.get_width()) // 2,
                 y + (INVENTORY_SLOT_SIZE[1] - item_image.get_height()) // 2)
            )

            if inventory[i].quantity is not None:
                quantity_text = font.render(str(inventory[i].quantity), True, WHITE)
                text_x = slot_x + INVENTORY_SLOT_SIZE[0] - quantity_text.get_width() - 10
                text_y = y + INVENTORY_SLOT_SIZE[1] - quantity_text.get_height() - 5
                screen.blit(quantity_text, (text_x, text_y))

        if i == selected_item_index:
            screen.blit(inventory_select_image, (slot_x, y))

    for i in range(NUM_INVENTORY_SLOTS):
        slot_x = start_x + i * INVENTORY_SLOT_SIZE[0]
        slot_rect = pygame.Rect(slot_x, y, INVENTORY_SLOT_SIZE[0], INVENTORY_SLOT_SIZE[1])

        if inventory[i] and slot_rect.collidepoint(mouse_x, mouse_y) and inventory[i].item_type == "plant":
            tooltip_text = f"Restores {inventory[i].energy_restore} energy"
            tooltip_surface = font.render(tooltip_text, True, WHITE)
            tooltip_width = tooltip_surface.get_width()
            tooltip_height = tooltip_surface.get_height()

            tooltip_x = mouse_x - tooltip_width // 2
            tooltip_y = mouse_y - tooltip_height - 10

            if tooltip_x < 0:
                tooltip_x = 0
            elif tooltip_x + tooltip_width > SCREEN_WIDTH:
                tooltip_x = SCREEN_WIDTH - tooltip_width

            if tooltip_y < 0:
                tooltip_y = mouse_y + 20

            tooltip_bg = pygame.Surface((tooltip_width + 10, tooltip_height + 10), pygame.SRCALPHA)
            tooltip_bg.fill((0, 0, 0, 128))
            screen.blit(tooltip_bg, (tooltip_x - 5, tooltip_y - 5))

            screen.blit(tooltip_surface, (tooltip_x, tooltip_y))


def draw_plants():
    for plant in plants:
        plant.draw(screen)


def handle_input():
    global selected_item_index, is_day, current_cycle_time

    keys = pygame.key.get_pressed()

    dx, dy = 0, 0

    if not character.is_watering:
        if keys[pygame.K_w]:
            dy = -MOVEMENT_SPEED
            character.direction = "back"
        if keys[pygame.K_s]:
            dy = MOVEMENT_SPEED
            character.direction = "front"
        if keys[pygame.K_a]:
            dx = -MOVEMENT_SPEED
            character.direction = "side"
            character.facing_left = True
        if keys[pygame.K_d]:
            dx = MOVEMENT_SPEED
            character.direction = "side"
            character.facing_left = False

    character.move(dx, dy)

    character_tile_x = round(character.x)
    character_tile_y = round(character.y)
    if 0 <= character_tile_x < MAP_WIDTH and 0 <= character_tile_y < MAP_HEIGHT:
        tile = tilemap[character_tile_y][character_tile_x]
        if tile.tile_type == "house":
            sleep_popup.display()
        else:
            sleep_popup.show = False

    for i in range(1, NUM_INVENTORY_SLOTS + 1):
        if keys[getattr(pygame, f'K_{i}')]:
            selected_item_index = i - 1

    if keys[pygame.K_e]:
        consume_plant()

    character.update_animation()


def water_tile(tilemap, x, y):
    global current_energy, current_water

    selected_item = inventory[selected_item_index]
    if selected_item is None or selected_item.name != "Watering Can":
        return False

    tile = tilemap[y][x]
    if tile.tile_type == "farmland" and not tile.watered:
        if current_water > 0 and current_energy >= 5:
            tile.watered = True
            current_water -= 1
            current_energy -= 5
            character.start_watering()
            return True
    return False


def handle_mouse_input(tilemap):
    global selected_item_index

    if pygame.mouse.get_pressed()[0]:
        mouse_x, mouse_y = pygame.mouse.get_pos()

        total_width = NUM_INVENTORY_SLOTS * INVENTORY_SLOT_SIZE[0]
        start_x = (SCREEN_WIDTH - total_width) // 2
        y = MAP_HEIGHT * TILE_SIZE[1]

        for i in range(NUM_INVENTORY_SLOTS):
            slot_x = start_x + i * INVENTORY_SLOT_SIZE[0]
            slot_rect = pygame.Rect(slot_x, y, INVENTORY_SLOT_SIZE[0], INVENTORY_SLOT_SIZE[1])

            if slot_rect.collidepoint(mouse_x, mouse_y):
                selected_item_index = i
                break

        result = sleep_popup.handle_click(mouse_x, mouse_y)
        if result == "yes":
            global current_energy, is_day, current_cycle_time, last_time
            is_day = True
            current_cycle_time = 0
            last_time = time.time()

            current_energy = min(current_energy + 10, MAX_ENERGY)

            grow_plants()
            reset_watered_tiles()
        elif result == "no":
            pass
        else:
            grid_x = mouse_x // TILE_SIZE[0]
            grid_y = mouse_y // TILE_SIZE[1]

            if 0 <= grid_x < MAP_WIDTH and 0 <= grid_y < MAP_HEIGHT:
                if abs(character.x - grid_x) <= 1 and abs(character.y - grid_y) <= 1:
                    if not character.is_moving:
                        if not harvest_plant(grid_x, grid_y):
                            if not water_tile(tilemap, grid_x, grid_y):
                                if not refill_water_if_near_river(tilemap, grid_x, grid_y):
                                    plant_seed(tilemap, grid_x, grid_y)


def handle_drag_and_drop():
    global dragging_item, dragging_item_index, dragging_item_offset, inventory

    mouse_x, mouse_y = pygame.mouse.get_pos()

    if pygame.mouse.get_pressed()[0]:
        if dragging_item is None:
            total_width = NUM_INVENTORY_SLOTS * INVENTORY_SLOT_SIZE[0]
            start_x = (SCREEN_WIDTH - total_width) // 2
            y = MAP_HEIGHT * TILE_SIZE[1]

            for i in range(NUM_INVENTORY_SLOTS):
                slot_x = start_x + i * INVENTORY_SLOT_SIZE[0]
                slot_rect = pygame.Rect(slot_x, y, INVENTORY_SLOT_SIZE[0], INVENTORY_SLOT_SIZE[1])

                if slot_rect.collidepoint(mouse_x, mouse_y) and inventory[i] is not None:
                    dragging_item = inventory[i]
                    dragging_item_index = i
                    dragging_item_offset = (mouse_x - slot_x, mouse_y - y)
                    inventory[i] = None
                    break
        else:
            pass
    else:
        if dragging_item is not None:
            total_width = NUM_INVENTORY_SLOTS * INVENTORY_SLOT_SIZE[0]
            start_x = (SCREEN_WIDTH - total_width) // 2
            y = MAP_HEIGHT * TILE_SIZE[1]

            for i in range(NUM_INVENTORY_SLOTS):
                slot_x = start_x + i * INVENTORY_SLOT_SIZE[0]
                slot_rect = pygame.Rect(slot_x, y, INVENTORY_SLOT_SIZE[0], INVENTORY_SLOT_SIZE[1])

                if slot_rect.collidepoint(mouse_x, mouse_y):
                    if inventory[i] is not None:
                        inventory[dragging_item_index] = inventory[i]
                        inventory[i] = dragging_item
                    else:
                        inventory[i] = dragging_item
                    dragging_item = None
                    dragging_item_index = None
                    dragging_item_offset = (0, 0)
                    break
            else:
                inventory[dragging_item_index] = dragging_item
                dragging_item = None
                dragging_item_index = None
                dragging_item_offset = (0, 0)

    if dragging_item is not None:
        item_image = dragging_item.image
        screen.blit(item_image, (mouse_x - dragging_item_offset[0], mouse_y - dragging_item_offset[1]))

        if dragging_item.quantity is not None:
            font = pygame.font.Font(None, 24)
            quantity_text = font.render(str(dragging_item.quantity), True, WHITE)
            text_x = mouse_x - dragging_item_offset[0] + INVENTORY_SLOT_SIZE[0] - quantity_text.get_width() - 15
            text_y = mouse_y - dragging_item_offset[1] + INVENTORY_SLOT_SIZE[1] - quantity_text.get_height() - 10
            screen.blit(quantity_text, (text_x, text_y))


def draw_energy_bar():
    pygame.draw.rect(
        screen,
        ENERGY_BAR_BACKGROUND_COLOR,
        (ENERGY_BAR_X, ENERGY_BAR_Y, ENERGY_BAR_WIDTH, ENERGY_BAR_HEIGHT)
    )

    energy_height = (current_energy / MAX_ENERGY) * ENERGY_BAR_HEIGHT

    pygame.draw.rect(
        screen,
        ENERGY_BAR_COLOR,
        (ENERGY_BAR_X, ENERGY_BAR_Y + (ENERGY_BAR_HEIGHT - energy_height), ENERGY_BAR_WIDTH, energy_height)
    )


def refill_water_if_near_river(tilemap, grid_x, grid_y):
    global current_water

    if tilemap[grid_y][grid_x].is_river:
        current_water = MAX_WATER

        character.start_watering()

        return True
    return False


def harvest_plant(x, y):
    global inventory, achievements

    if is_inventory_full():
        print("Inventory is full! Cannot harvest.")
        return False

    plop_sound = pygame.mixer.Sound("assets/sounds/plop.mp3")

    for plant in plants:
        if plant.position == (x, y) and plant.is_grown():
            plant_price = PLANT_PRICES.get(plant.plant_type, 50)

            energy_restore = {
                "deathBell": 15,
                "rose": 25,
                "pointy": 40,
                "daisy": 30,
                "sunflower": 60,
                "hydrangea": 90,
                "lavender": 45,
                "pink_rose": 80,
                "magic_flower": 110,
            }.get(plant.plant_type, 0)

            for i in range(NUM_INVENTORY_SLOTS):
                if inventory[i] and inventory[i].name == plant.plant_type:
                    inventory[i].quantity += 1
                    break
            else:
                for i in range(NUM_INVENTORY_SLOTS):
                    if inventory[i] is None:
                        grown_image = pygame.image.load(f"assets/plants/grown/{plant.plant_type}.png").convert_alpha()
                        grown_image = pygame.transform.scale(grown_image, (60, 60))
                        inventory[i] = InventoryItem(
                            item_type="plant",
                            image=grown_image,
                            name=plant.plant_type,
                            quantity=1,
                            price=plant_price,
                            energy_restore=energy_restore
                        )
                        break

            plants.remove(plant)
            tile_cooldown[(x, y)] = time.time()

            plop_sound.play()

            if not achievements["first_harvest"]["completed"]:
                achievements["first_harvest"]["completed"] = True
                achievement_popup.display(f"Achievement Unlocked: {achievements['first_harvest']['name']}")

            return True

    return False


def plant_seed(tilemap, x, y):
    global inventory, selected_item_index

    current_time = time.time()

    if (x, y) in tile_cooldown and current_time - tile_cooldown[(x, y)] < 0.5:
        return

    if tilemap[y][x].tile_type == "farmland":
        for plant in plants:
            if plant.position == (x, y):
                return

        selected_item: InventoryItem = inventory[selected_item_index]
        if selected_item and selected_item.item_type == "seed":
            if selected_item.name == "Bluebell Seeds":
                deathbell = Plant("deathBell", "assets/plants/plantGrowing/deathbell", 4, (x, y), days_to_grow=1)
                plants.append(deathbell)
            elif selected_item.name == "Rose Seeds":
                rose = Plant("rose", "assets/plants/plantGrowing/rose", 4, (x, y), days_to_grow=1)
                plants.append(rose)
            elif selected_item.name == "Pointy Seeds":
                pointy = Plant("pointy", "assets/plants/plantGrowing/pointy", 4, (x, y), days_to_grow=1)
                plants.append(pointy)
            elif selected_item.name == "Daisy Seeds":
                daisy = Plant("daisy", "assets/plants/plantGrowing/daisy", 4, (x, y), days_to_grow=2)
                plants.append(daisy)
            elif selected_item.name == "Sunflower Seeds":
                sunflower = Plant("sunflower", "assets/plants/plantGrowing/sunflower", 4, (x, y), days_to_grow=2)
                plants.append(sunflower)
            elif selected_item.name == "Hydrangea Seeds":
                hydrangea = Plant("hydrangea", "assets/plants/plantGrowing/hydrangea", 4, (x, y), days_to_grow=2)
                plants.append(hydrangea)
            elif selected_item.name == "Lavender Seeds":
                lavender = Plant("lavender", "assets/plants/plantGrowing/lavender", 4, (x, y), days_to_grow=3)
                plants.append(lavender)
            elif selected_item.name == "Pink Rose Seeds":
                pink_rose = Plant("pink_rose", "assets/plants/plantGrowing/pink_rose", 4, (x, y), days_to_grow=3)
                plants.append(pink_rose)
            elif selected_item.name == "Magic Flower Seeds":
                magic_flower = Plant("magic_flower", "assets/plants/plantGrowing/magic_flower", 4, (x, y),
                                     days_to_grow=3)
                plants.append(magic_flower)

            selected_item.quantity -= 1

            if selected_item.quantity == 0:
                inventory[selected_item_index] = None


COIN_BALANCE = 0


def draw_buy_grid():
    if not buy_active:
        return

    buy_grid_width = 5 * INVENTORY_SLOT_SIZE[0]
    buy_grid_height = 3 * INVENTORY_SLOT_SIZE[1]
    start_x = (SCREEN_WIDTH - buy_grid_width) // 2
    start_y = (SCREEN_HEIGHT - buy_grid_height) // 2

    pygame.draw.rect(screen, BROWN, (start_x, start_y, buy_grid_width, buy_grid_height))

    for i in range(BUY_GRID_SIZE):
        slot_x = start_x + (i % 5) * INVENTORY_SLOT_SIZE[0]
        slot_y = start_y + (i // 5) * INVENTORY_SLOT_SIZE[1]
        screen.blit(inventory_slot_image, (slot_x, slot_y))

        if buy_grid[i]:
            item_image = buy_grid[i].image
            screen.blit(
                item_image,
                (slot_x + (INVENTORY_SLOT_SIZE[0] - item_image.get_width()) // 2,
                 slot_y + (INVENTORY_SLOT_SIZE[1] - item_image.get_height()) // 2)
            )

    mouse_x, mouse_y = pygame.mouse.get_pos()
    for i in range(BUY_GRID_SIZE):
        slot_x = start_x + (i % 5) * INVENTORY_SLOT_SIZE[0]
        slot_y = start_y + (i // 5) * INVENTORY_SLOT_SIZE[1]
        slot_rect = pygame.Rect(slot_x, slot_y, INVENTORY_SLOT_SIZE[0], INVENTORY_SLOT_SIZE[1])

        if buy_grid[i] and slot_rect.collidepoint(mouse_x, mouse_y):
            font = pygame.font.Font(None, 24)
            price_text = font.render(f"Price: {buy_grid[i].price}", True, WHITE)

            tooltip_x = mouse_x
            tooltip_y = mouse_y - 30

            if tooltip_y < 0:
                tooltip_y = mouse_y + 20
            if tooltip_x + price_text.get_width() > SCREEN_WIDTH:
                tooltip_x = SCREEN_WIDTH - price_text.get_width()

            tooltip_bg = pygame.Surface((price_text.get_width() + 10, price_text.get_height() + 10), pygame.SRCALPHA)
            tooltip_bg.fill((0, 0, 0, 128))
            screen.blit(tooltip_bg, (tooltip_x - 5, tooltip_y - 5))

            screen.blit(price_text, (tooltip_x, tooltip_y))


def handle_buy_interaction():
    global buy_active, COIN_BALANCE, last_buy_time

    coins_sound = pygame.mixer.Sound("assets/sounds/coins.mp3")

    character_tile_x = round(character.x)
    character_tile_y = round(character.y)

    if (character_tile_x, character_tile_y) == BUY_POSITION:
        buy_active = True
    else:
        buy_active = False

    if buy_active:
        draw_buy_grid()

        if pygame.mouse.get_pressed()[0]:
            current_time = time.time()
            if current_time - last_buy_time < BUY_COOLDOWN:
                return

            mouse_x, mouse_y = pygame.mouse.get_pos()
            shift_pressed = pygame.key.get_pressed()[pygame.K_LSHIFT] or pygame.key.get_pressed()[pygame.K_RSHIFT]

            for i in range(BUY_GRID_SIZE):
                slot_x = (SCREEN_WIDTH - 5 * INVENTORY_SLOT_SIZE[0]) // 2 + (i % 5) * INVENTORY_SLOT_SIZE[0]
                slot_y = (SCREEN_HEIGHT - 3 * INVENTORY_SLOT_SIZE[1]) // 2 + (i // 5) * INVENTORY_SLOT_SIZE[1]
                slot_rect = pygame.Rect(slot_x, slot_y, INVENTORY_SLOT_SIZE[0], INVENTORY_SLOT_SIZE[1])

                if buy_grid[i] and slot_rect.collidepoint(mouse_x, mouse_y):
                    if is_inventory_full():
                        return

                    item = buy_grid[i]
                    quantity = 5 if shift_pressed else 1
                    total_cost = item.price * quantity

                    if COIN_BALANCE >= total_cost:
                        COIN_BALANCE -= total_cost

                        for j in range(NUM_INVENTORY_SLOTS):
                            if inventory[j] and inventory[j].name == item.name:
                                inventory[j].quantity += quantity
                                break
                        else:
                            for j in range(NUM_INVENTORY_SLOTS):
                                if inventory[j] is None:
                                    inventory[j] = InventoryItem(
                                        item_type=item.item_type,
                                        image=item.image,
                                        name=item.name,
                                        quantity=quantity,
                                        price=item.price
                                    )
                                    break

                        coins_sound.play()

                        last_buy_time = current_time


def draw_sell_grid():
    if not sell_active:
        return

    sell_grid_width = 3 * INVENTORY_SLOT_SIZE[0]
    sell_grid_height = 3 * INVENTORY_SLOT_SIZE[1]
    start_x = (SCREEN_WIDTH - sell_grid_width) // 2
    start_y = (SCREEN_HEIGHT - sell_grid_height) // 2

    pygame.draw.rect(screen, BROWN, (start_x, start_y, sell_grid_width, sell_grid_height))

    for i in range(9):
        slot_x = start_x + (i % 3) * INVENTORY_SLOT_SIZE[0]
        slot_y = start_y + (i // 3) * INVENTORY_SLOT_SIZE[1]
        screen.blit(inventory_slot_image, (slot_x, slot_y))

        if sell_grid[i]:
            item_image = sell_grid[i].image
            screen.blit(
                item_image,
                (slot_x + (INVENTORY_SLOT_SIZE[0] - item_image.get_width()) // 2,
                 slot_y + (INVENTORY_SLOT_SIZE[1] - item_image.get_height()) // 2)
            )

            if sell_grid[i].quantity is not None:
                font = pygame.font.Font(None, 24)
                quantity_text = font.render(str(sell_grid[i].quantity), True, WHITE)
                text_x = slot_x + INVENTORY_SLOT_SIZE[0] - quantity_text.get_width() - 10
                text_y = slot_y + INVENTORY_SLOT_SIZE[1] - quantity_text.get_height() - 5
                screen.blit(quantity_text, (text_x, text_y))

    sell_button_rect = pygame.Rect(start_x + sell_grid_width - 100, start_y + sell_grid_height + 10, 80, 40)
    pygame.draw.rect(screen, (0, 255, 0), sell_button_rect)
    font = pygame.font.Font(None, 24)
    sell_text = font.render("Sell", True, WHITE)
    screen.blit(sell_text, (sell_button_rect.x + 20, sell_button_rect.y + 10))

    return sell_button_rect


last_transfer_time = 0
TRANSFER_COOLDOWN = 0.2


def handle_sell_interaction():
    global sell_active, COIN_BALANCE, last_transfer_time

    coins_sound = pygame.mixer.Sound("assets/sounds/coins.mp3")

    character_tile_x = round(character.x)
    character_tile_y = round(character.y)

    if (character_tile_x, character_tile_y) == SELL_POSITION:
        sell_active = True
    else:
        sell_active = False

    if sell_active:
        sell_button_rect = draw_sell_grid()

        if pygame.mouse.get_pressed()[0]:
            current_time = time.time()
            if current_time - last_transfer_time < TRANSFER_COOLDOWN:
                return

            mouse_x, mouse_y = pygame.mouse.get_pos()
            shift_pressed = pygame.key.get_pressed()[pygame.K_LSHIFT] or pygame.key.get_pressed()[pygame.K_RSHIFT]

            if sell_button_rect.collidepoint(mouse_x, mouse_y):
                for i in range(len(sell_grid)):
                    if sell_grid[i]:
                        COIN_BALANCE += sell_grid[i].price * sell_grid[i].quantity
                        sold_crops[sell_grid[i].name] = True
                        sell_grid[i] = None

                        coins_sound.play()

                if all(sold_crops.values()) and not achievements["sell_one_of_each"]["completed"]:
                    achievements["sell_one_of_each"]["completed"] = True
                    achievement_popup.display(f"Achievement Unlocked: {achievements['sell_one_of_each']['name']}")

            for i in range(len(sell_grid)):
                slot_x = (SCREEN_WIDTH - 3 * INVENTORY_SLOT_SIZE[0]) // 2 + (i % 3) * INVENTORY_SLOT_SIZE[0]
                slot_y = (SCREEN_HEIGHT - 3 * INVENTORY_SLOT_SIZE[1]) // 2 + (i // 3) * INVENTORY_SLOT_SIZE[1]
                slot_rect = pygame.Rect(slot_x, slot_y, INVENTORY_SLOT_SIZE[0], INVENTORY_SLOT_SIZE[1])

                if sell_grid[i] and slot_rect.collidepoint(mouse_x, mouse_y):
                    item_found = False
                    for j in range(NUM_INVENTORY_SLOTS):
                        if inventory[j] and inventory[j].name == sell_grid[i].name:
                            if shift_pressed:
                                inventory[j].quantity += sell_grid[i].quantity
                                sell_grid[i] = None
                            else:
                                inventory[j].quantity += 1
                                sell_grid[i].quantity -= 1
                                if sell_grid[i].quantity == 0:
                                    sell_grid[i] = None
                            item_found = True
                            break

                    if not item_found:
                        for j in range(NUM_INVENTORY_SLOTS):
                            if inventory[j] is None:
                                if shift_pressed:
                                    inventory[j] = sell_grid[i]
                                    sell_grid[i] = None
                                else:
                                    if sell_grid[i].quantity > 1:
                                        sell_grid[i].quantity -= 1
                                        inventory[j] = InventoryItem(
                                            item_type=sell_grid[i].item_type,
                                            image=sell_grid[i].image,
                                            name=sell_grid[i].name,
                                            quantity=1,
                                            price=sell_grid[i].price
                                        )
                                    else:
                                        inventory[j] = sell_grid[i]
                                        sell_grid[i] = None
                                break

                    last_transfer_time = current_time

            for i in range(NUM_INVENTORY_SLOTS):
                slot_rect = pygame.Rect(
                    (SCREEN_WIDTH - NUM_INVENTORY_SLOTS * INVENTORY_SLOT_SIZE[0]) // 2 + i * INVENTORY_SLOT_SIZE[0],
                    SCREEN_HEIGHT - INVENTORY_SLOT_SIZE[1],
                    INVENTORY_SLOT_SIZE[0],
                    INVENTORY_SLOT_SIZE[1]
                )
                if inventory[i] and slot_rect.collidepoint(mouse_x, mouse_y):
                    if inventory[i].is_tool():
                        continue

                    item_found = False
                    for j in range(len(sell_grid)):
                        if sell_grid[j] and sell_grid[j].name == inventory[i].name:
                            if shift_pressed:
                                sell_grid[j].quantity += inventory[i].quantity
                                inventory[i] = None
                            else:
                                sell_grid[j].quantity += 1
                                inventory[i].quantity -= 1
                                if inventory[i].quantity == 0:
                                    inventory[i] = None
                            item_found = True
                            break

                    if not item_found:
                        for j in range(len(sell_grid)):
                            if sell_grid[j] is None:
                                if shift_pressed:
                                    sell_grid[j] = inventory[i]
                                    inventory[i] = None
                                else:
                                    if inventory[i].quantity > 1:
                                        inventory[i].quantity -= 1
                                        sell_grid[j] = InventoryItem(
                                            item_type=inventory[i].item_type,
                                            image=inventory[i].image,
                                            name=inventory[i].name,
                                            quantity=1,
                                            price=inventory[i].price
                                        )
                                    else:
                                        sell_grid[j] = inventory[i]
                                        inventory[i] = None
                                break

                    last_transfer_time = current_time


MAX_WATER = 10
current_water = MAX_WATER
WATER_BAR_WIDTH = 20
WATER_BAR_HEIGHT = 200
WATER_BAR_X = SCREEN_WIDTH - 40 - WATER_BAR_WIDTH - 10
WATER_BAR_Y = SCREEN_HEIGHT - INVENTORY_HEIGHT - WATER_BAR_HEIGHT - 10
WATER_BAR_COLOR = (0, 0, 255)
WATER_BAR_BACKGROUND_COLOR = (139, 69, 19)


def check_grown_crops():
    grown_crops = {
        "deathBell": False,
        "rose": False,
        "pointy": False,
        "daisy": False,
        "sunflower": False,
        "hydrangea": False,
        "lavender": False,
        "pink_rose": False,
        "magic_flower": False
    }

    for plant in plants:
        if plant.is_grown():
            grown_crops[plant.plant_type] = True

    return grown_crops


def draw_achievements_menu(screen):
    menu_width = 400
    menu_height = 500
    menu_x = (SCREEN_WIDTH - menu_width) // 2
    menu_y = (SCREEN_HEIGHT - menu_height) // 2

    pygame.draw.rect(screen, BROWN, (menu_x, menu_y, menu_width, menu_height))
    pygame.draw.rect(screen, WHITE, (menu_x, menu_y, menu_width, menu_height), 2)

    font = pygame.font.Font(None, 48)
    title_text = font.render("Achievements", True, WHITE)
    title_x = menu_x + (menu_width - title_text.get_width()) // 2
    title_y = menu_y + 20
    screen.blit(title_text, (title_x, title_y))

    font = pygame.font.Font(None, 24)
    y_offset = title_y + 60
    max_text_width = menu_width - 40

    for achievement in achievements.values():
        if achievement["completed"]:
            color = (200, 200, 200)
        else:
            color = (100, 100, 100)

        name_text = font.render(achievement["name"], True, color)
        screen.blit(name_text, (menu_x + 20, y_offset))

        description = achievement["description"]
        description_lines = []
        current_line = ""
        for word in description.split():
            test_line = current_line + " " + word if current_line else word
            test_width, _ = font.size(test_line)
            if test_width <= max_text_width:
                current_line = test_line
            else:
                description_lines.append(current_line)
                current_line = word
        if current_line:
            description_lines.append(current_line)

        for line in description_lines:
            description_text = font.render(line, True, color)
            screen.blit(description_text, (menu_x + 20, y_offset + 30))
            y_offset += 30

        y_offset += 40

    close_button_rect = pygame.Rect(menu_x + menu_width - 40, menu_y + 10, 30, 30)
    pygame.draw.rect(screen, (255, 0, 0), close_button_rect)
    close_text = font.render("X", True, WHITE)
    screen.blit(close_text, (close_button_rect.x + 10, close_button_rect.y + 5))

    return close_button_rect


def draw_water_bar():
    pygame.draw.rect(
        screen,
        WATER_BAR_BACKGROUND_COLOR,
        (WATER_BAR_X, WATER_BAR_Y, WATER_BAR_WIDTH, WATER_BAR_HEIGHT)
    )

    water_height = (current_water / MAX_WATER) * WATER_BAR_HEIGHT

    pygame.draw.rect(
        screen,
        WATER_BAR_COLOR,
        (WATER_BAR_X, WATER_BAR_Y + (WATER_BAR_HEIGHT - water_height), WATER_BAR_WIDTH, water_height)
    )


def update_day_night_cycle():
    global current_cycle_time, is_day, last_time

    current_time = time.time()
    elapsed_time = current_time - last_time

    if elapsed_time >= 1:
        current_cycle_time += 1
        last_time = current_time

        if is_day and current_cycle_time >= DAY_DURATION:
            is_day = False
            current_cycle_time = 0
        elif not is_day and current_cycle_time >= NIGHT_DURATION:
            is_day = True
            current_cycle_time = 0
            update_day_night_cycle()
            grow_plants()
            reset_watered_tiles()


def calculate_night_opacity():
    global current_cycle_time, DAY_DURATION

    progress = current_cycle_time / DAY_DURATION

    if is_day:
        opacity = int(128 * progress)
    else:
        opacity = int(128 * (1 - progress))

    return opacity


def reset_watered_tiles():
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            tile = tilemap[y][x]
            if tile.tile_type == "farmland":
                tile.watered = False


def consume_plant():
    global current_energy, selected_item_index, last_consume_time

    current_time = time.time()
    if current_time - last_consume_time < CONSUME_COOLDOWN:
        return

    selected_item = inventory[selected_item_index]
    if selected_item and selected_item.item_type == "plant":
        if selected_item.quantity > 0:
            current_energy = min(MAX_ENERGY, current_energy + selected_item.energy_restore)
            selected_item.quantity -= 1
            if selected_item.quantity == 0:
                inventory[selected_item_index] = None

            last_consume_time = current_time


def grow_plants():
    for plant in plants:
        tile = tilemap[plant.position[1]][plant.position[0]]
        if tile.watered:
            plant.grow()
        tile.watered = False


def draw_day_night_overlay():
    opacity = calculate_night_opacity()

    if opacity > 0:
        night_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        night_overlay.fill((0, 0, 0, opacity))
        screen.blit(night_overlay, (0, 0))


def draw_coin_balance():
    font = pygame.font.Font(None, 36)
    coin_text = font.render(f"Coins: {COIN_BALANCE}", True, (255, 215, 0))
    screen.blit(coin_text, (SCREEN_WIDTH - 150, 10))


START_SCREEN_COLOR = (255, 0, 0)
BUTTON_SIZE = (150, 50)
BUTTON_IMAGE = pygame.image.load('assets/tilemap/button.png').convert_alpha()
BUTTON_IMAGE = pygame.transform.scale(BUTTON_IMAGE, BUTTON_SIZE)


def draw_start_screen(screen):
    screen.fill(START_SCREEN_COLOR)

    for i in range(SCREEN_HEIGHT):
        color = (
            int((1 - i / SCREEN_HEIGHT) * 255),
            int((i / SCREEN_HEIGHT) * 255),
            0
        )
        pygame.draw.rect(screen, color, (0, i, SCREEN_WIDTH, 1))

    start_button_rect = pygame.Rect(
        (SCREEN_WIDTH - BUTTON_SIZE[0]) // 2,
        (SCREEN_HEIGHT - BUTTON_SIZE[1]) // 2 - 60,
        BUTTON_SIZE[0],
        BUTTON_SIZE[1]
    )

    screen.blit(BUTTON_IMAGE, start_button_rect.topleft)

    font = pygame.font.Font(None, 36)
    start_text = font.render("Start", True, (255, 255, 0))

    screen.blit(start_text, (
        start_button_rect.centerx - start_text.get_width() // 2,
        start_button_rect.centery - start_text.get_height() // 2))

    return start_button_rect


pygame.mixer.init()

pygame.mixer.music.load("assets/sounds/background.mp3")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)


def main():
    global COIN_BALANCE, sell_active, buy_active, current_cycle_time, is_day, last_time, tilemap

    tilemap = generate_map()
    bush_positions = generate_bushes(tilemap)

    running = True
    clock = pygame.time.Clock()

    start_screen = True
    while start_screen:
        screen.fill(START_SCREEN_COLOR)
        start_button_rect = draw_start_screen(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                start_screen = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button_rect.collidepoint(mouse_pos):
                    start_screen = False

        pygame.display.flip()
        clock.tick(60)

    show_achievements_menu = False

    while running:
        screen.fill(WHITE)

        update_day_night_cycle()

        draw_map(tilemap, bush_positions)
        handle_mouse_input(tilemap)
        draw_plants()
        handle_input()
        character.update_animation()
        character.draw(screen)
        draw_day_night_overlay()
        draw_inventory()
        draw_coin_balance()
        handle_sell_interaction()
        handle_buy_interaction()
        draw_buy_grid()
        draw_energy_bar()
        draw_water_bar()
        sleep_popup.draw(screen)
        handle_drag_and_drop()

        grown_crops = check_grown_crops()
        if all(grown_crops.values()) and not achievements["one_of_each"]["completed"]:
            achievements["one_of_each"]["completed"] = True
            achievement_popup.display(f"Achievement Unlocked: {achievements['one_of_each']['name']}")

        if COIN_BALANCE >= 30000 and not achievements["rich_farmer"]["completed"]:
            achievements["rich_farmer"]["completed"] = True
            achievement_popup.display(f"Achievement Unlocked: {achievements['rich_farmer']['name']}")

        achievement_popup.update()
        achievement_popup.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    show_achievements_menu = not show_achievements_menu
            elif event.type == pygame.MOUSEBUTTONDOWN and show_achievements_menu:
                mouse_pos = pygame.mouse.get_pos()
                close_button_rect = draw_achievements_menu(screen)
                if close_button_rect.collidepoint(mouse_pos):
                    show_achievements_menu = False

        if show_achievements_menu:
            close_button_rect = draw_achievements_menu(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()
