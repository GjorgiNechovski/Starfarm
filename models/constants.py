TILE_SIZE = (64, 64)
MAP_WIDTH = 15
MAP_HEIGHT = 9

INVENTORY_SLOT_SIZE = (80, 80)
NUM_INVENTORY_SLOTS = 8
INVENTORY_HEIGHT = INVENTORY_SLOT_SIZE[1]

SCREEN_WIDTH = MAP_WIDTH * TILE_SIZE[0]
SCREEN_HEIGHT = MAP_HEIGHT * TILE_SIZE[1] + INVENTORY_HEIGHT

MAX_ENERGY = 160
ENERGY_BAR_WIDTH = 20
ENERGY_BAR_HEIGHT = 200
ENERGY_BAR_X = SCREEN_WIDTH - 40
ENERGY_BAR_Y = SCREEN_HEIGHT - INVENTORY_HEIGHT - ENERGY_BAR_HEIGHT - 10
ENERGY_BAR_COLOR = (0, 128, 0)
ENERGY_BAR_BACKGROUND_COLOR = (139, 69, 19)

WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
SELL_TILE_COLOR = (139, 69, 19)
WATERED_COLOR = (100, 50, 19)

DAY_DURATION = 30
NIGHT_DURATION = 30

CHARACTER_SIZE = (40, 40)
WATERING_CHARACTER_SIZE = (80, 45)

PLANT_PRICES = {
    "deathBell": 450,
    "rose": 550,
    "pointy": 550,
    "daisy": 2200,
    "sunflower": 2300,
    "hydrangea": 2000,
    "lavender": 6000,
    "pink_rose": 9300,
    "magic_flower": 8000,
}

BUY_PRICES = {
    "Bluebell Seeds": 100,
    "Rose Seeds": 200,
    "Pointy Seeds": 250,
    "Daisy Seeds": 900,
    "Sunflower Seeds": 1100,
    "Hydrangea Seeds": 1050,
    "Lavender Seeds": 3500,
    "Pink Rose Seeds": 5000,
    "Magic Flower Seeds": 5000,
}

achievements = {
    "first_harvest": {
        "name": "First Harvest",
        "description": "Grow and harvest a single crop.",
        "completed": False
    },
    "sell_one_of_each": {
        "name": "Sell One of Each Crop",
        "description": "Sell at least one of each crop type.",
        "completed": False
    },
    "one_of_each": {
        "name": "One of Each",
        "description": "Have at least one of each crop fully grown on your farm at the same time.",
        "completed": False
    },
    "rich_farmer": {
        "name": "Rich Farmer",
        "description": "Reach 30,000 coins.",
        "completed": False
    }
}
