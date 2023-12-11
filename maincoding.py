import tkinter
import pygame
from tkinter import messagebox
from tkinter import simpledialog

key = ""
popup_opened = set()  # 여러 개의 좌표를 관리하기 위해 set 사용
selected_pokemon = None
popup=None
pygame.init()
pygame.mixer.init()

bgm_start_path = "bgm_start.mp3"
bgm_battle_path = "bgm_battle.wav"
bgm_boss_path = "bgm_boss.wav"
bgm_store_path = "bgm_store.mp3"
bgm_end_path ="bgm_end.mp3"

try:
    bgm_start = pygame.mixer.Sound(bgm_start_path)
    bgm_battle = pygame.mixer.Sound(bgm_battle_path)
    bgm_boss = pygame.mixer.Sound(bgm_boss_path)
    bgm_store = pygame.mixer.Sound(bgm_store_path)
    bgm_end = pygame.mixer.Sound(bgm_end_path)

except pygame.error as e:
    print(f"Error loading sound file: {e}")
    messagebox.showerror("Error", "Failed to load sound file. Check the file path and format.")

def play_bgm(bgm):
    pygame.mixer.music.load(bgm)
    pygame.mixer.music.play()

def stop_bgm():
    pygame.mixer.music.stop()


def playbgm_start():
    stop_bgm()
    play_bgm(bgm_start_path) 
    root.after(100, check_bgm)
    

def playbgm_battle():
    stop_bgm()
    play_bgm(bgm_battle_path)

def playbgm_boss():
    stop_bgm()
    play_bgm(bgm_boss_path)

def playbgm_store():
    stop_bgm()
    play_bgm(bgm_store_path)

def playbgm_end():
    stop_bgm()
    play_bgm(bgm_end_path)

def check_bgm():
    # 배경 음악이 종료되었으면, 다음 행동을 취하도록 설정
    if not pygame.mixer.music.get_busy():
        show_message(popup, "음악이 종료되었습니다. 다음 단계로 진행합니다.")
        pass
    else:
        # 아직 재생 중이면, 재귀 호출을 통해 계속 체크
        root.after(100, check_bgm)

def key_down(e):
    global key
    key = e.keysym

def key_up(e):
    global key
    key = ""


mx = 1
my = 1
player_firsthp=50
player_hp = 50
player_att = 15
player_def = 1

monster_hp = 50
monster2_hp = 70
boss_hp= 100

player_money = 0 

def set_background_image(image_path):
    # 캔버스에 배경 이미지 설정
    bg_img = tkinter.PhotoImage(file=image_path)
    canvas.create_image(400, 280, image=bg_img)
    canvas.image = bg_img  # 가비지 컬렉션을 피하기 위해 참조 유지

def close_popup(popup): 
    stop_bgm()  
    popup.destroy()

def reset_player_hp():
    global player_hp
    player_hp = player_firsthp

def reset_monster_hp():
    global monster_hp
    monster_hp = monster2_hp

def main_move():
    global mx, my, popup_opened, player_hp, maze, current_coord, end_coord, popup
    if key == "Up" and maze[my - 1][mx] == 0:
        my = my - 1
    if key == "Down" and maze[my + 1][mx] == 0:
        my = my + 1
    if key == "Left" and maze[my][mx - 1] == 0:
        mx = mx - 1
    if key == "Right" and maze[my][mx + 1] == 0:
        mx = mx + 1
    current_coord = (mx, my)

    if popup and not popup.winfo_exists():
        # 팝업이 존재하고, 창이 닫혔을 때
        popup = None
        root.after(300, main_move)

    target_coords = [(1, 1)]  # 원하는 좌표를 추가
    if current_coord in target_coords and current_coord not in popup_opened:
        stage_start(current_coord)
        popup_opened.add(current_coord)  # 해당 좌표가 열린 것으로 플래그 설정
    
    target_coords = [(1, 5)]  # 원하는 좌표를 추가
    if current_coord in target_coords and current_coord not in popup_opened:
        stage_ssal(current_coord)
        popup_opened.add(current_coord)  # 해당 좌표가 열린 것으로 플래그 설정

    target_coords = [(3, 1)]
    if current_coord in target_coords and current_coord not in popup_opened:
        stage_bon(current_coord)
        popup_opened.add(current_coord)  

    target_coords = [(5, 5)]
    if current_coord in target_coords and current_coord not in popup_opened:
        stage_gyeongcheon(current_coord)
        popup_opened.add(current_coord)  
    
    target_coords = [(7, 1)]
    if current_coord in target_coords and current_coord not in popup_opened:
        stage_store(current_coord)
        popup_opened.add(current_coord) 
    
    target_coords = [(9, 5)]
    if current_coord in target_coords and current_coord not in popup_opened:
        stage_igong(current_coord)
        popup_opened.add(current_coord)  

    target_coords = [(9, 6)]
    if current_coord in target_coords and current_coord not in popup_opened:
        stage_final(current_coord)
        popup_opened.add(current_coord)  
 
    if maze[my][mx] == 0:
        maze[my][mx] = 2
        canvas.create_rectangle(mx * 80, my * 80, mx * 80 + 79, my * 80 + 79, fill="pink", width=0)
    canvas.delete("MYCHR")
    canvas.create_image(mx * 80 + 40, my * 80 + 40, image=img, tag="MYCHR")
    root.after(300, main_move)

def show_message(popup, message):
    label_message = tkinter.Label(popup, text=message, font=("Helvetica", 12))
    label_message.place(relx=0.5, rely=0.8, anchor="center")

def stage_start(coord):
    global player_hp, player_money, player_att, player_def, popup
    popup = tkinter.Toplevel(root)
    popup.title("머리띠")
    popup.geometry("600x600")
    background_image_path = "bg1.png"
    background_image = tkinter.PhotoImage(file=background_image_path)
    background_label = tkinter.Label(popup, image=background_image)
    background_label.image = background_image
    background_label.place(relx=0, rely=0, anchor="nw")
    image_paths = ["green.png", "fire.png", "water.png"]
    popup_images = [tkinter.PhotoImage(file=path) for path in image_paths]

    for i, image in enumerate(popup_images):
        label_image = tkinter.Label(popup, image=image)
        label_image.image = image
        label_image.place(x=i * 200, y=130)

    choice_greenbutton = tkinter.Button(popup, text="풀 선택하기", command=lambda: choice_green(popup))
    choice_greenbutton.place(x=100, y=50)

    choice_firebutton = tkinter.Button(popup, text="불 선택하기", command=lambda: choice_fire(popup))
    choice_firebutton.place(x=250, y=50)

    choice_waterbutton = tkinter.Button(popup, text="물 선택하기", command=lambda: choice_water(popup))
    choice_waterbutton.place(x=400, y=50)

    playbgm_start()
    show_message(popup, "강남대에 오신걸 환영합니다!\n여러분은 이 3마리의 포켓몬 중 한마리의 포켓몬과 대학교를 졸업해야 합니다!\n 한마리의 포켓몬을 선택해 주세요.")
    popup.protocol("WM_DELETE_WINDOW", lambda: close_popup(popup))
    
    
    
def stage_ssal(coord):
    global player_hp, player_money, player_att, player_def, selected_pokemon, monster2_hp
    popup = tkinter.Toplevel(root)
    popup.title("샬롬관")
    popup.geometry("800x700")


    background_image_path = "bg2.png"
    background_image = tkinter.PhotoImage(file=background_image_path)
    background_label = tkinter.Label(popup, image=background_image)
    background_label.image = background_image
    background_label.place(relx=0, rely=0, anchor="nw")

    label = tkinter.Label(popup, text="앗!! 야생의 비버니가 나타났다")
    label.pack() 
    
    if selected_pokemon:
        pokemon_image_path = f"{selected_pokemon.lower()}.png"  # 선택한 포켓몬에 따른 이미지 경로
        pokemon_image = tkinter.PhotoImage(file=pokemon_image_path)
        label_pokemon = tkinter.Label(popup, image=pokemon_image)
        label_pokemon.image = pokemon_image
        label_pokemon.place(x=30, y=400)  

    monster_image_path = "monster1.png" 
    monster_image = tkinter.PhotoImage(file=monster_image_path)
    label_monster = tkinter.Label(popup, image=monster_image)
    label_monster.image = monster_image
    label_monster.place(x=450, y=290)

    # 버튼을 눌렀을 때 공격 실행
    attack_button = tkinter.Button(popup, text="공격하기", command=lambda: attack_action(popup, coord))
    attack_button.pack()

    if player_hp <= 0:
        label = tkinter.Label(popup, text="체력이 다 소진되어 패배하였습니다.")
        label.pack()
    else:
        playbgm_battle()
        popup.protocol("WM_DELETE_WINDOW", lambda: stop_bgm())  
    reset_player_hp()  

def stage_bon(coord):
    global player_hp, player_money, player_att, player_def, selected_pokemon, monster2_hp
    popup = tkinter.Toplevel(root)
    popup.title("본관")
    popup.geometry("800x700")
    background_image_path = "bg3.png"
    background_image = tkinter.PhotoImage(file=background_image_path)
    background_label = tkinter.Label(popup, image=background_image)
    background_label.image = background_image
    background_label.place(relx=0, rely=0, anchor="nw")
    label = tkinter.Label(popup, text="앗!! 야생의 피카츄가 나타났다")
    label.pack() 
    

    if selected_pokemon:
        pokemon_image_path = f"{selected_pokemon.lower()}.png"  # 선택한 포켓몬에 따른 이미지 경로
        pokemon_image = tkinter.PhotoImage(file=pokemon_image_path)
        label_pokemon = tkinter.Label(popup, image=pokemon_image)
        label_pokemon.image = pokemon_image
        label_pokemon.place(x=30, y=400)

    monster_image_path = "monster2.png" 
    monster_image = tkinter.PhotoImage(file=monster_image_path)
    label_monster = tkinter.Label(popup, image=monster_image)
    label_monster.image = monster_image
    label_monster.place(x=450, y=290)
    # 버튼을 눌렀을 때 공격 실행
    attack_button = tkinter.Button(popup, text="공격하기", command=lambda: attack_action(popup, coord))
    attack_button.pack()
    if player_hp <= 0:
        label = tkinter.Label(popup, text="체력이 다 소진되어 패배하였습니다.")
        label.pack()
    else:
        playbgm_battle()
        popup.protocol("WM_DELETE_WINDOW", lambda: close_popup(popup))

def stage_gyeongcheon(coord):
    global player_hp, player_money, player_att, player_def, selected_pokemon, monster2_hp
    popup = tkinter.Toplevel(root)
    popup.title("경천관")
    popup.geometry("800x700")
    background_image_path = "bg4.png"
    background_image = tkinter.PhotoImage(file=background_image_path)
    background_label = tkinter.Label(popup, image=background_image)
    background_label.image = background_image
    background_label.place(relx=0, rely=0, anchor="nw")
    label = tkinter.Label(popup, text="앗!! 야생의 럭시오가 나타났다")
    label.pack()

    if selected_pokemon:
        pokemon_image_path = f"{selected_pokemon.lower()}.png"  # 선택한 포켓몬에 따른 이미지 경로
        pokemon_image = tkinter.PhotoImage(file=pokemon_image_path)
        label_pokemon = tkinter.Label(popup, image=pokemon_image)
        label_pokemon.image = pokemon_image
        label_pokemon.place(x=30, y=400)

    monster_image_path = "monster3.png"
    monster_image = tkinter.PhotoImage(file=monster_image_path)
    label_monster = tkinter.Label(popup, image=monster_image)
    label_monster.image = monster_image
    label_monster.place(x=450, y=290)

    # 버튼을 눌렀을 때 공격 실행
    attack_button = tkinter.Button(popup, text="공격하기", command=lambda: attack_action(popup, coord))
    attack_button.pack()

    if player_hp <= 0:
        label = tkinter.Label(popup, text="체력이 다 소진되어 패배하였습니다.")
        label.pack()
    else:
        playbgm_battle()
        popup.protocol("WM_DELETE_WINDOW", lambda: close_popup(popup))

 

def stage_store(coord):
    global player_hp, player_money, player_att, player_def, selected_pokemon

    popup = tkinter.Toplevel(root)
    popup.title("상점")
    popup.geometry("800x500")
    background_image_path = "storebg.png"
    background_image = tkinter.PhotoImage(file=background_image_path)
    background_label = tkinter.Label(popup, image=background_image)
    background_label.image = background_image
    background_label.place(relx=0, rely=0, anchor="nw")

    # 아이템 목록과 가격
    items = {
        "체력 회복 포션": {"가격": 10, "효과": 20},
        "공격력 증가 포션": {"가격": 15, "효과": 5},
        "방어력 증가 포션": {"가격": 15, "효과": 2}
    }

    for item, info in items.items():
        label_item = tkinter.Label(popup, text=f"{item} - 가격: {info['가격']} gold")
        label_item.pack()

        buy_button = tkinter.Button(popup, text=f"{item} 구매", command=lambda item=item: buy_item(popup, item))
        buy_button.pack()

    if player_money <= 0:
        label = tkinter.Label(popup, text="골드가 부족하여 구매할 수 있는 물품이 없습니다.")
        label.pack()
    else:
        playbgm_store()
        popup.protocol("WM_DELETE_WINDOW", lambda: close_popup(popup))

def buy_item(popup, item):
    global player_hp, player_money, player_att, player_def

    items = {
        "체력 회복 포션": {"가격": 10, "효과": 20},
        "공격력 증가 포션": {"가격": 15, "효과": 5},
        "방어력 증가 포션": {"가격": 15, "효과": 2}
    }

    # 플레이어가 아이템을 구매할 충분한 골드를 가지고 있는지 확인
    item_price = items[item]["가격"]
    if player_money >= item_price:
        # 플레이어의 스탯을 구매한 아이템에 따라 업데이트
        if item == "체력 회복 포션":
            player_hp += items[item]["효과"]
        elif item == "공격력 증가 포션":
            player_att += items[item]["효과"]
        elif item == "방어력 증가 포션":
            player_def += items[item]["효과"]

        # 플레이어의 돈에서 아이템 가격 차감
        player_money -= item_price

        # 구매 메시지와 현재 골드 액수 표시
        purchase_message = f"{item}을(를) 구매했습니다! ({item_price} gold 차감)"
        current_gold_message = f"현재 보유한 골드: {player_money} gold"
        label_purchase = tkinter.Label(popup, text=purchase_message)
        label_current_gold = tkinter.Label(popup, text=current_gold_message)
        label_purchase.pack()
        label_current_gold.pack()

        # 현재 능력치를 표시
        show_player_stats()

    else:
        # 골드가 부족할 경우 메시지 표시
        label_insufficient_gold = tkinter.Label(popup, text="골드가 부족하여 물건을 구매할 수 없습니다.")
        label_insufficient_gold.pack()

    # 팝업 창 숨기기
    popup.protocol("WM_DELETE_WINDOW", lambda: popup.withdraw())


def update_main_window():
    # 메인 윈도우 업데이트를 위한 코드를 추가 (필요 시 구현)
    pass

def stage_igong(coord):
    global player_hp, player_money, player_att, player_def, selected_pokemon, monster2_hp
    popup = tkinter.Toplevel(root)
    popup.title("이공관")
    popup.geometry("800x700")
    background_image_path = "bg5.png"
    background_image = tkinter.PhotoImage(file=background_image_path)
    background_label = tkinter.Label(popup, image=background_image)
    background_label.image = background_image
    background_label.place(relx=0, rely=0, anchor="nw")
    label = tkinter.Label(popup, text="최종 보스 람브가 등장하였습니다!")
    label.pack()

    if selected_pokemon:
        pokemon_image_path = f"{selected_pokemon.lower()}.png"  # 선택한 포켓몬에 따른 이미지 경로
        pokemon_image = tkinter.PhotoImage(file=pokemon_image_path)
        label_pokemon = tkinter.Label(popup, image=pokemon_image)
        label_pokemon.image = pokemon_image
        label_pokemon.place(x=30, y=400)

    monster_image_path = "boss.png"
    monster_image = tkinter.PhotoImage(file=monster_image_path)
    label_monster = tkinter.Label(popup, image=monster_image)
    label_monster.image = monster_image
    label_monster.place(x=450, y=290)

    # 버튼을 눌렀을 때 공격 실행
    attack_button = tkinter.Button(popup, text="공격하기", command=lambda: attack_action(popup, coord))
    attack_button.pack()

    if player_hp <= 0:
        label = tkinter.Label(popup, text="체력이 다 소진되어 패배하였습니다.")
        label.pack()
    else:
        playbgm_boss()
        popup.protocol("WM_DELETE_WINDOW", lambda: close_popup(popup))

def stage_final(coord):
    global player_hp, player_money, player_att, player_def, selected_pokemon, monster2_hp
    popup = tkinter.Toplevel(root)
    popup.title("명예의 전당")
    popup.geometry("800x700")
    background_image_path = "bg6.png"
    background_image = tkinter.PhotoImage(file=background_image_path)
    background_label = tkinter.Label(popup, image=background_image)
    background_label.image = background_image
    background_label.place(relx=0, rely=0, anchor="nw")
    label = tkinter.Label(popup, text=" 축하합니다! 강남대 포켓몬 학사과정을 수료했습니다!\n 당신은 마스터입니다! \n 게임을 종료하려면 게임 종료 버튼을 눌러주세요")
    label.pack()

    if selected_pokemon:
        pokemon_image_path = f"{selected_pokemon.lower()}.png"  # 선택한 포켓몬에 따른 이미지 경로
        pokemon_image = tkinter.PhotoImage(file=pokemon_image_path)
        label_pokemon = tkinter.Label(popup, image=pokemon_image)
        label_pokemon.image = pokemon_image
        label_pokemon.place(x=30, y=400)

    monster_image_path = "sir.png"
    monster_image = tkinter.PhotoImage(file=monster_image_path)
    label_monster = tkinter.Label(popup, image=monster_image)
    label_monster.image = monster_image
    label_monster.place(x=450, y=290)

    label_ending = tkinter.Label(popup, text="명예의 전당에 등록되셨습니다!")
    label_ending.pack()


    ending_button = tkinter.Button(popup, text="게임 종료", command=root.destroy)
    ending_button.pack()

    playbgm_end()
    popup.protocol("WM_DELETE_WINDOW", lambda: close_popup(popup))
    popup.mainloop() 

def attack_action(popup, coord):
    global monster_hp, selected_pokemon, player_hp, player_att, player_money, monster2_hp, player_def, canvas

    # 플레이어 포켓몬이 몬스터를 공격
    actual_damage = max(0, player_att)

    if monster_hp <= 0:
        label = tkinter.Label(popup, text="적이 쓰러졌습니다.\n 몬스터를 쓰러트려서 10 gold를 획득합니다\n ----------당신의 포켓몬이 레벨업하였습니다----------")
        player_money += 10
        label.pack()
        reset_monster_hp()
        reset_player_hp()

        # 전투에서 승리했을 때 플레이어의 스탯을 올립니다.
        player_hp += 10  # 체력 증가
        player_att += 2  # 공격력 증가
        player_def += 1  # 방어력 증가

        # 현재 능력치를 표시
        show_player_stats()

        # 팝업 창을 숨기고 게임을 계속 진행
        popup.protocol("WM_DELETE_WINDOW", lambda: popup.withdraw())
    else:
        # 적이 플레이어에게 공격
        monster_damage = max(0, 8)  # 적의 기본 공격력 (임의의 값, 적절히 조절 필요)

        player_hp -= monster_damage
        result_text_to_monster = f"({selected_pokemon})이(가) 상대 몬스터에게 {actual_damage}의 피해를 입혔습니다!\n상대 몬스터의 남은 체력: {monster_hp}"

        # 상대 몬스터의 남은 체력 표시
        label_monster_hp = tkinter.Label(popup, text=result_text_to_monster)
        label_monster_hp.pack()

        # 몬스터의 체력 업데이트
        monster_hp -= actual_damage

        if player_hp <= 0:
            label = tkinter.Label(popup, text="체력이 다 소진되어 패배하였습니다.")
            label.pack()
            # 팝업 창을 숨기고 게임을 종료
            popup.protocol("WM_DELETE_WINDOW", lambda: popup.withdraw())
        else:
            # 플레이어의 남은 체력 표시
            result_text_to_player = f"적이 플레이어({selected_pokemon})에게 공격하여 {monster_damage}의 피해를 입혔습니다!\n플레이어의 남은 체력: {player_hp}"
            label_player_hp = tkinter.Label(popup, text=result_text_to_player)
            label_player_hp.pack()

            # 현재 능력치를 표시
            show_player_stats()

            # 창을 숨기고 게임을 계속 진행
            popup.protocol("WM_DELETE_WINDOW", lambda: popup.withdraw())

def show_player_stats():
    global player_hp, player_att, player_def, canvas

    # 기존에 표시된 능력치를 삭제
    canvas.delete("PLAYER_STATS")

    # 현재 능력치를 표시
    stats_text = f"체력: {player_hp}   공격력: {player_att}   방어력: {player_def}"
    label_stats = canvas.create_text(10, 10, anchor="nw", text=stats_text, font=("Helvetica", 12), fill="black", tag="PLAYER_STATS")


def choice_green(coord):
    global selected_pokemon, popup

    result_text = "풀 포켓몬 이상해 꽃을 선택하셨습니다"
    selected_pokemon = "green"
    label = tkinter.Label(popup, text=result_text)
    label.pack()
    popup.protocol("WM_DELETE_WINDOW", lambda: popup.withdraw())

def choice_fire(coord):
    global selected_pokemon, popup

    result_text = "불 포켓몬 파이리를 선택하셨습니다"
    selected_pokemon = "fire"
    label = tkinter.Label(popup, text=result_text)
    label.pack()
    popup.protocol("WM_DELETE_WINDOW", lambda: popup.withdraw())

def choice_water(coord):
    global selected_pokemon, popup

    result_text = "물 포켓몬 꼬부기를 선택하셨습니다"
    selected_pokemon = "water"
    label = tkinter.Label(popup, text=result_text)
    label.pack()
    popup.protocol("WM_DELETE_WINDOW", lambda: popup.withdraw())


# 메인 윈도우
root = tkinter.Tk()
root.title("강남대 졸업 여정기")
root.bind("<KeyPress>", key_down)
root.bind("<KeyRelease>", key_up)
canvas = tkinter.Canvas(width=800, height=560, bg="white")
canvas.pack()

maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    [1, 0, 0, 0, 1, 0, 0, 0, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
]
tile_image = tkinter.PhotoImage(file="tile.png")

# ..

# 벽 이미지 배치 부분 수정
for y in range(7):
    for x in range(10):
        if maze[y][x] == 1:
            canvas.create_image(x * 80, y * 80, image=tile_image, anchor="nw")

# 플레이어 이미지 배치 부분 수정
img = tkinter.PhotoImage(file="player.png")
player_image = canvas.create_image(mx * 80 + 40, my * 80 + 40, image=img, tag="MYCHR")
main_move()
root.mainloop()
