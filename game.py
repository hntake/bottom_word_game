import pygame
import os
import random

# Pygameの初期化
pygame.init()

# ウィンドウのサイズ
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("しりとりゲーム")

# イラストが保存されているフォルダのパス
IMAGE_FOLDER = "images"

# しりとりの単語とイラストのファイル名の辞書
word_image_mapping = {
    "スイカ": "watermelon.png",
    "カラス": "crow.png",
    "すし": "sushi.png",
    "しまうま": "zebra.png",
    "マントヒヒ": "ape.png",
    "ひつじ": "sheep.png",
    "じどうしゃ": "car.png",
    "しゃけ": "salmon.png",
}

# イラストの読み込み
images = {}
for word, image_filename in word_image_mapping.items():
    image_path = os.path.join(IMAGE_FOLDER, image_filename)
    if os.path.exists(image_path):
        images[word] = pygame.image.load(image_path)
    else:
        print(f"Error: {image_filename} not found in {IMAGE_FOLDER}")

# しりとりの単語リスト
words = list(word_image_mapping.keys())
random.shuffle(words)  # 単語をランダムに並べる

# サウンドの読み込み
success_sound = pygame.mixer.Sound("goal.wav")
drag_sound = pygame.mixer.Sound("set.wav")

# 定数
GRID_COLS = 4
GRID_ROWS = 2
IMAGE_SIZE = (WIDTH // GRID_COLS, HEIGHT // (GRID_ROWS + 1))

# 空の箱の位置とサイズ
BOX_COLS = 8
BOX_SIZE = (WIDTH // BOX_COLS, HEIGHT // (GRID_ROWS + 1))
BOX_Y = HEIGHT - BOX_SIZE[1]

# やり直しボタンの位置とサイズ
REDO_BUTTON_SIZE = (100, 50)
REDO_BUTTON_POS = (WIDTH - REDO_BUTTON_SIZE[0] - 10, 10)  # 右上に配置

# やり直しボタンの読み込み
redo_button_image = pygame.image.load(os.path.join(IMAGE_FOLDER, "left-arrow.png"))
redo_button_image = pygame.transform.scale(redo_button_image, REDO_BUTTON_SIZE)

# ゲームループ
def main():
    global placed_images  # placed_imagesをグローバル変数として宣言
    running = True
    selected_image = None
    selected_rect = None
    placed_images = [None] * BOX_COLS
    clock = pygame.time.Clock()

    while running:
        clock.tick(30)

        # イベント処理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, word in enumerate(words):
                    col = i % GRID_COLS
                    row = i // GRID_COLS
                    x = col * (WIDTH // GRID_COLS)
                    y = row * (HEIGHT // (GRID_ROWS + 1))
                    rect = pygame.Rect(x, y, *IMAGE_SIZE)
                    if rect.collidepoint(event.pos):
                        selected_image = word
                        selected_rect = rect
                        drag_sound.play()
                        break
                # やり直しボタンがクリックされたかどうかをチェック
                if REDO_BUTTON_POS[0] <= event.pos[0] <= REDO_BUTTON_POS[0] + REDO_BUTTON_SIZE[0] \
                        and REDO_BUTTON_POS[1] <= event.pos[1] <= REDO_BUTTON_POS[1] + REDO_BUTTON_SIZE[1]:
                    redo_game()

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if selected_image:
                    for i in range(BOX_COLS):
                        x = i * BOX_SIZE[0]
                        rect = pygame.Rect(x, BOX_Y, *BOX_SIZE)
                        if rect.collidepoint(event.pos):
                            placed_images[i] = selected_image
                            words.remove(selected_image)
                            check_order(placed_images)
                            break
                    selected_image = None
                    selected_rect = None

        # 画面をクリア
        WIN.fill((255, 255, 255))

        # イラストを描画
        for i, word in enumerate(words):
            col = i % GRID_COLS
            row = i // GRID_COLS
            x = col * (WIDTH // GRID_COLS)
            y = row * (HEIGHT // (GRID_ROWS + 1))
            if word in images:
                image = images[word]
                image = pygame.transform.scale(image, IMAGE_SIZE)
                WIN.blit(image, (x, y))

        # 空の箱を描画
        for i in range(BOX_COLS):
            x = i * BOX_SIZE[0]
            rect = pygame.Rect(x, BOX_Y, *BOX_SIZE)
            pygame.draw.rect(WIN, (0, 0, 0), rect, 2)
            if placed_images[i]:
                word = placed_images[i]
                image = images[word]
                image = pygame.transform.scale(image, BOX_SIZE)
                WIN.blit(image, (x, BOX_Y))

        # やり直しボタンを描画
        WIN.blit(redo_button_image, REDO_BUTTON_POS)

        # 画面を更新
        pygame.display.update()

    pygame.quit()
# ゲームをやり直す関数
def redo_game():
    global words
    words = list(word_image_mapping.keys())
    random.shuffle(words)
    for i in range(len(placed_images)):  # placed_imagesの長さに合わせる
        placed_images[i] = None

def check_order(placed_images):
    if all(placed_images[i] == word for i, word in enumerate(words)):
        success_sound.play()

if __name__ == "__main__":
    main()
