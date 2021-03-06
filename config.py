
FPS = 60

WINDOW_CAPTION = 'Bhabhi Thula'

FOLDER_PATH = 'assets/cards/'

SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 600

CARD_DRAW_OFFSET = 30
CARD_DRAW_PADDING_BOTTOM = 30

ALL_TARGET_OFFSET_Y = 50

CARD_WIDTH = 100
CARD_HEIGHT = 145

CARD_ANIMATION_SPEED = 50

FONTFACE = 'Arial'
FONT_SIZE = 20

PLAYER_A_TEXT_X = 250
PLAYER_A_TEXT_Y = SCREEN_HEIGHT - (CARD_HEIGHT//2) + 50

PLAYER_B_TEXT_X = 20
PLAYER_B_TEXT_Y = SCREEN_HEIGHT // 2 - 50

PLAYER_C_TEXT_X = 250
PLAYER_C_TEXT_Y = 10

PLAYER_D_TEXT_X = SCREEN_WIDTH - 200
PLAYER_D_TEXT_Y = SCREEN_HEIGHT // 2

TEXT_RECT = [
    (PLAYER_A_TEXT_X, PLAYER_A_TEXT_Y),
    (PLAYER_B_TEXT_X, PLAYER_B_TEXT_Y),
    (PLAYER_C_TEXT_X, PLAYER_C_TEXT_Y),
    (PLAYER_D_TEXT_X, PLAYER_D_TEXT_Y)
]

DELAY_AFTER_THULA = 2000
DELAY_AFTER_ROUND_NO_THULA = 2000

ELIGIBLE_CARD_HEIGHT_OFFSET = 20

PLAYING_CARD_CENTERED_HEIGHT =  int(CARD_HEIGHT * 0.80) 
PLAYING_CARD_CENTERED_WIDTH = int(CARD_WIDTH * 0.80)

PLAYER_A_TARGET_CENTERED_X = 500 + (PLAYING_CARD_CENTERED_WIDTH // 2)
PLAYER_A_TARGET_CENTERED_Y = 280 + (PLAYING_CARD_CENTERED_HEIGHT // 2) - ALL_TARGET_OFFSET_Y

PLAYER_B_TARGET_CENTERED_X = 300 + (PLAYING_CARD_CENTERED_WIDTH // 2)
PLAYER_B_TARGET_CENTERED_Y = 200 + (PLAYING_CARD_CENTERED_HEIGHT // 2) - ALL_TARGET_OFFSET_Y

PLAYER_C_TARGET_CENTERED_X = 500 + (PLAYING_CARD_CENTERED_WIDTH // 2) 
PLAYER_C_TARGET_CENTERED_Y = 110 + (PLAYING_CARD_CENTERED_HEIGHT // 2) - ALL_TARGET_OFFSET_Y

PLAYER_D_TARGET_CENTERED_X = 710 + (PLAYING_CARD_CENTERED_WIDTH // 2)
PLAYER_D_TARGET_CENTERED_Y = 200 + (PLAYING_CARD_CENTERED_HEIGHT // 2) - ALL_TARGET_OFFSET_Y

TARGET_RECT = [
    (PLAYER_A_TARGET_CENTERED_X, PLAYER_A_TARGET_CENTERED_Y),
    (PLAYER_B_TARGET_CENTERED_X, PLAYER_B_TARGET_CENTERED_Y),
    (PLAYER_C_TARGET_CENTERED_X, PLAYER_C_TARGET_CENTERED_Y),
    (PLAYER_D_TARGET_CENTERED_X, PLAYER_D_TARGET_CENTERED_Y)
]

PLAYER_A_DECK_CENTER_X = SCREEN_WIDTH // 2
PLAYER_A_DECK_CENTER_Y = SCREEN_HEIGHT - CARD_DRAW_PADDING_BOTTOM - (CARD_HEIGHT // 2)

PLAYER_B_DECK_CENTER_X = -20
PLAYER_B_DECK_CENTER_Y = SCREEN_HEIGHT // 2

PLAYER_C_DECK_CENTER_X = SCREEN_WIDTH // 2
PLAYER_C_DECK_CENTER_Y = -20

PLAYER_D_DECK_CENTER_X = SCREEN_WIDTH +20 
PLAYER_D_DECK_CENTER_Y = SCREEN_HEIGHT // 2

DECK_RECT = [
    (PLAYER_A_DECK_CENTER_X, PLAYER_A_DECK_CENTER_Y),
    (PLAYER_B_DECK_CENTER_X, PLAYER_B_DECK_CENTER_Y),
    (PLAYER_C_DECK_CENTER_X, PLAYER_C_DECK_CENTER_Y),
    (PLAYER_D_DECK_CENTER_X, PLAYER_D_DECK_CENTER_Y)
]

OFFSCREEN_RECT = (-100,-100)

GLOW_THICKNESS = 10
GLOW_COLOR = (0,255,0)

IS_ANYTHING_MOVING = False