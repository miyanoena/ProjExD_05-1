import logging
import pygame
import random
import sys

# 画面サイズ
SURFACE_WIDTH = 800
SURFACE_HEIGHT = 550

# STEP
STEP_READY = 0
STEP_PLAY = 1
STEP_GAMEOVER = 2
STEP_GAMECLEAR = 3

# アイテム設定
ITEM_TYPE_NUM = 2
ITEM_WIDTH = 10
ITEM_HEIGHT = 10 
ITEM_MAX = 60

# こうかとん設定
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 72
PLAYER_Y = 520

# 満腹メータMAX
STUFFED_MAX = 200

# 各種初期値を設定
step = STEP_READY  
timer = 0 
is_jump = 0
p_width = PLAYER_WIDTH
p_height = PLAYER_HEIGHT
stuffed = STUFFED_MAX
item_hit = [False] * ITEM_MAX
item_x = [0] * ITEM_MAX
item_y = [0] * ITEM_MAX
item_type = [''] * ITEM_MAX
item_num = 10
flg_turn = False
last_key = pygame.K_RIGHT
dmg_effect = 0

# 画像読み込み
# アイコン
icon = pygame.image.load('ex05/img/6.png')
# 背景
img_bg = pygame.image.load('ex05/img/pg_bg.jpg')
# プレイヤー
img_player = pygame.image.load('ex05/img/3.png')
# アイテム（鶏肉）
img_donuts = pygame.transform.rotozoom(pygame.image.load('ex05/img/toriniku.png'),0,0.15)
# アイテム（豆）
img_red_hot = pygame.transform.rotozoom(pygame.image.load('ex05/img/mame.png'),0,0.15)
# ゲームオーバー
txt_gameover = pygame.transform.rotozoom(pygame.image.load('ex05/img/txt_gameover.png'),0, 0.6)
# ゲームクリア
txt_gameclear = pygame.transform.rotozoom(pygame.image.load('ex05/img/text_gameclear.png'),0, 0.6)
# プレイヤーの移動
def move_player(key):
    global px, is_jump, last_key, flg_turn, p_width, p_height

    # 「⇦」キー押下の動き
    if key[pygame.K_LEFT] == 1:  
        px -= 10
        if px < 50+p_width/2:
            px = 50+p_width/2
        if last_key == pygame.K_RIGHT:
            flg_turn = True
            last_key = pygame.K_LEFT
    # 「→」キー押下した時の動き
    elif key[pygame.K_RIGHT] == 1: 
        px += 10
        if px > SURFACE_WIDTH-50-p_width/2:
            px = SURFACE_WIDTH-50-p_width/2
        if last_key == pygame.K_LEFT:
            flg_turn = True
            last_key = pygame.K_RIGHT

# アイテムの作成
def locate_item():
    # アイテム数MAX値まで繰り返し
    for i in range(ITEM_MAX):
        # ランダムで鶏肉か豆どっちかを設定する
        item_x[i] = random.randint(50, SURFACE_WIDTH-50-ITEM_WIDTH/2)
        item_y[i] = random.randint(-500, 0)

        if i % ITEM_TYPE_NUM == 0:  
            # 鶏肉
            item_type[i] = 'd'
        else:
            # 豆
            item_type[i] = 'r'

# アイテムの落下と当たり判定
def move_item(surface):
    for i in range(item_num):
        item_y[i] += 6 + i / 5 
        if item_y[i] > SURFACE_HEIGHT:
            item_hit[i] = False
            item_x[i] = random.randint(50, SURFACE_WIDTH-50-ITEM_WIDTH/2)
            item_y[i] = random.randint(-500, 0)

        if item_hit[i] == False:
            # プレイヤーとアイテムの座標を見て当たったか判定
            if is_item_hit(px, PLAYER_Y, item_x[i], item_y[i]) == True:
                item_hit[i] = True
                hit_item(item_type[i], surface)

# アイテムを描画
def draw_item(surface):
    for i in range(item_num):
        if item_hit[i] == False and item_type[i] == 'd':
            surface.blit(
                img_donuts, [item_x[i]-ITEM_WIDTH/2, item_y[i]-ITEM_HEIGHT/2])
        elif item_hit[i] == False and item_type[i] == 'r':
            surface.blit(
                img_red_hot, [item_x[i]-ITEM_WIDTH/2, item_y[i]-ITEM_HEIGHT/2])

# アイテムに当たったときの処理
def hit_item(category, surface):
    global stuffed, dmg_effect

    # 鶏肉の時は満腹メータプラス
    if category == 'd':
        stuffed += 10 
        if stuffed > STUFFED_MAX:
            stuffed = STUFFED_MAX
    # 豆の場合は満腹メータ激減り
    elif category == 'r':
        stuffed -= 20
        if stuffed < 0:
            stuffed = 0
        dmg_effect = 1

# 当たり判定
def is_item_hit(x1, y1, x2, y2):
    if (abs(x1-x2) <= +p_width/2+ITEM_WIDTH/2 and abs(y1-y2) <= p_height/2+ITEM_HEIGHT/2):
        return True
    return False

# main関数
def main():
    global step, timer, stuffed, px, is_jump
    global item_num, img_player, flg_turn, dmg_effect
    global p_width, p_height

    # ウィンドウを作成
    pygame.init()
    pygame.display.set_caption('こうかとんは食いしん坊')
    pygame.display.set_icon(icon)
    clock = pygame.time.Clock()
    surface = pygame.display.set_mode((SURFACE_WIDTH, SURFACE_HEIGHT))

    # ループ
    while True:
        timer += 1

        # イベントごとの処理
        for event in pygame.event.get():
            # 閉じるボタン押下された時はゲーム終了
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # プレイ開始時
        if step == STEP_READY:
            # プレイモードへ
            step = STEP_PLAY

            # 満腹メータMAX
            stuffed = STUFFED_MAX

            flg_turn = False

            # こうかとんスタンバイ
            px = SURFACE_WIDTH / 2
            p_width = PLAYER_WIDTH
            p_height = PLAYER_HEIGHT
            img_player = pygame.image.load('ex05/img/3.png')

            # 最初は10個からスタートし、だんだん増えてくる
            item_num = 10

            # アイテム落下
            locate_item()

        # プレイモード
        elif step == STEP_PLAY:
            if stuffed <= 0:
                step = STEP_GAMEOVER
                timer = 0
            if item_num != ITEM_MAX and timer % 15 == 0:
                item_num += 10
            if timer >= 1200:
                step = STEP_GAMECLEAR
                timer = 0

            # 時間経過でも徐々に満腹メータ減る
            stuffed -= 0.5

            # キャラクター、アイテム移動
            move_player(pygame.key.get_pressed())
            move_item(surface)

        # ゲームオーバー
        elif step == STEP_GAMEOVER:
            if timer == 50:
                step = STEP_READY
                timer = 0

        # 各種描画
        bx = 0
        by = 0

        if dmg_effect > 0:
            # ダメージ受けた場合は画面揺らす
            bx = random.randint(-60, 20)
            by = random.randint(-40, 10)
            dmg_effect = 0
            # # ダメージ受けたらこうかとん巨大化
            # p_width = p_width*1.2
            # p_height = p_height*1.2
            # img_player = pygame.transform.scale(img_player, (p_width,p_height))

        # 背景
        surface.blit(img_bg, [bx, by])

        if flg_turn == True:
            img_player = pygame.transform.flip(img_player, True, False)
            flg_turn = False

        # こうかとん描画
        surface.blit(img_player, [px-p_width/2, PLAYER_Y-p_height/2])

        # アイテム描画
        draw_item(surface)

        # ゲームオーバー
        if step == STEP_GAMEOVER:
            logging.info(stuffed)

            # ゲームオーバーの文言のサブ画面を作ってメーン画面へかぶせる
            sub_surface = pygame.Surface((SURFACE_WIDTH, SURFACE_HEIGHT), pygame.SRCALPHA)
            sub_surface.fill((0, 0, 0, 100))

            # テキストの矩形を取得
            txt_rect = txt_gameover.get_rect()

            # 画面の中央に配置するための座標を計算
            text_x = (SURFACE_WIDTH - txt_rect.width) // 2
            text_y = (SURFACE_HEIGHT - txt_rect.height) // 2

            surface.blit(sub_surface, [0, 0])
            surface.blit(txt_gameover, [text_x, text_y])
            stuffed = 0

        if step == STEP_GAMECLEAR:
            logging.info(stuffed)

            sub_surface = pygame.Surface((SURFACE_WIDTH, SURFACE_HEIGHT), pygame.SRCALPHA)
            sub_surface.fill((0, 0, 0, 100))

            # テキストの矩形を取得
            txt_rect = txt_gameclear.get_rect()

            # 画面の中央に配置するための座標を計算
            text_x = (SURFACE_WIDTH - txt_rect.width) // 2
            text_y = (SURFACE_HEIGHT - txt_rect.height) // 2

            surface.blit(sub_surface, [0, 0])
            surface.blit(txt_gameclear, [text_x, text_y])
            stuffed = 0

        # 満腹メータ
        surface.fill((250, 237, 240), (50, 30, STUFFED_MAX, 40))
        stuffed_r = 100
        stuffed_g = 100
        stuffed_b = 255
        if stuffed < STUFFED_MAX/5:
            # メーターが残り1/5になったら赤くする　
            stuffed_r = 255
            stuffed_g = 100
            stuffed_b = 128
        surface.fill((stuffed_r, stuffed_g, stuffed_b), (50, 30, stuffed, 40))

        # ゲーム画面更新
        pygame.display.update()
        clock.tick(10)

# main実行
main()