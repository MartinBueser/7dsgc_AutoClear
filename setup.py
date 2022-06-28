import cv2
import numpy as np
import queue
import time
from tkinter import StringVar, Tk


class IterRegistry(type):
    def __iter__(cls):
        return iter(cls._registry)


class Skills(metaclass=IterRegistry):
    _registry = []

    def __init__(self, name, level, path, img, width, height, color, thickness):
        self.name = name
        self.level = level
        self.path = path
        self.img = img
        self.width = width
        self.height = height
        self.color = color
        self.thickness = thickness
        self._registry.append(self)
    threshold = .90
    result = None
    maxVal = None
    maxLoc = None
    xLoc = None
    yLoc = None
    rectangles = None
    count = 0


def init():
    global sct
    sct = None

    global skill_delay
    skill_delay = 2.5
    global menu_delay
    menu_delay = 4

    global current_time
    current_time = time.time()
    global skill_delay_time
    skill_delay_time = time.time()
    global menu_delay_time
    menu_delay_time = time.time()
    global p_delay_time
    p_delay_time = time.time()

    global skillQueue
    skillQueue = queue.PriorityQueue()
    global skill_frame
    skill_frame = None

    global ready_frame
    ready_frame = None
    global phase_frame
    phase_frame = None
    global ok_reset_frame
    ok_reset_frame = None
    global select_stage_1_frame
    select_stage_1_frame = None
    global select_stage_2_frame
    select_stage_2_frame = None
    global select_stage_3_frame
    select_stage_3_frame = None
    global STAGE_1
    STAGE_1 = False
    global STAGE_2
    STAGE_2 = True
    global STAGE_3
    STAGE_3 = False
    global phase
    phase = 1
    global RUSH_STAGE2_PHASE3
    RUSH_STAGE2_PHASE3 = False
    global STAGE3_PHASE3_HP_MIN
    STAGE3_PHASE3_HP_MIN = False
    global confirm_reset_frame
    confirm_reset_frame = None
    global save_team_frame
    save_team_frame = None
    global confirm_team_frame
    confirm_team_frame = None
    global use_stamina_potion_frame
    use_stamina_potion_frame = None
    global team_frame
    team_frame = None
    global matrona_health_frame
    matrona_health_frame = None
    global beast_status_bar_frame
    beast_status_bar_frame = None
    global boss_hp_frame
    boss_hp_frame = None
    global forfeit_battle_frame
    forfeit_battle_frame = None

    # tkinter gui
    global root
    root = Tk()
    global RUN_LOOP
    RUN_LOOP = True
    global MOUSE_ACTIVE
    MOUSE_ACTIVE = True
    global PAUSE
    PAUSE = False
    global BIRD_AUTO
    BIRD_AUTO = False
    global DEER_AUTO
    DEER_AUTO = False
    global DEATH_MATCH
    DEATH_MATCH = False
    global DAILY
    DAILY = False

    global skill_delay_text
    skill_delay_text = StringVar()
    skill_delay_text.set(str(skill_delay))
    global menu_delay_text
    menu_delay_text = StringVar()
    menu_delay_text.set(str(menu_delay))

    global skill_label_frame
    skill_label_frame = None
    global mouse_text
    mouse_text = StringVar()
    global bird_completions_text
    bird_completions_text = StringVar()
    global bird_failures_text
    bird_failures_text = StringVar()
    global deer_completions_text
    deer_completions_text = StringVar()
    global deer_failures_text
    deer_failures_text = StringVar()

    # bird
    global mat2_delay
    mat2_delay = int()
    global mat2_delay_counter
    mat2_delay_counter = 0
    global ATTACK
    ATTACK = False
    global EVASION
    EVASION = False
    global REFLECT
    REFLECT = False
    global buff_remove_forward
    buff_remove_forward = 0
    global BIRD_COMPLETION_COUNTER_SET
    BIRD_COMPLETION_COUNTER_SET = False
    global BIRD_FAILURE_COUNTER_SET
    BIRD_FAILURE_COUNTER_SET = False
    global bird_completion_counter1
    bird_completion_counter1 = 0
    global bird_completion_counter2
    bird_completion_counter2 = 0
    global bird_completion_counter3
    bird_completion_counter3 = 0
    global bird_failure_counter1
    bird_failure_counter1 = 0
    global bird_failure_counter2
    bird_failure_counter2 = 0
    global bird_failure_counter3
    bird_failure_counter3 = 0
    # deer
    global red_card_delay_phase2
    red_card_delay_phase2 = 0
    global green_card_delay_phase2
    green_card_delay_phase2 = 100
    global blue_card_delay_phase2
    blue_card_delay_phase2 = 100
    global red_card_delay_phase4
    red_card_delay_phase4 = 100
    global green_card_delay_phase4
    green_card_delay_phase4 = 100
    global blue_card_delay_phase4
    blue_card_delay_phase4 = 0
    global DEER_COMPLETION_COUNTER_SET
    DEER_COMPLETION_COUNTER_SET = False
    global DEER_FAILURE_COUNTER_SET
    DEER_FAILURE_COUNTER_SET = False
    global deer_completion_counter
    deer_completion_counter = 0
    global deer_failure_counter
    deer_failure_counter = 0


def setup_frame():
    ## ready frame (center)
    global ready_frame_top
    global ready_frame_left
    global ready_frame_width
    global ready_frame_height
    global ready_frame_box
    ready_frame_top = 715
    ready_frame_left = 820
    ready_frame_width = 280
    ready_frame_height = 100
    ready_frame_box = {"top": ready_frame_top, "left": ready_frame_left, "width": ready_frame_width, "height": ready_frame_height}

    ## phase frame (top left)
    global phase_frame_top
    global phase_frame_left
    global phase_frame_width
    global phase_frame_height
    global phase_frame_box
    phase_frame_top = 130
    phase_frame_left = 70
    phase_frame_width = 110
    phase_frame_height = 50
    phase_frame_box = {"top": phase_frame_top, "left": phase_frame_left, "width": phase_frame_width, "height": phase_frame_height}

    ## skill frame (bottom right)
    global skill_frame_top
    global skill_frame_left
    global skill_frame_width
    global skill_frame_height
    global skill_frame_box
    skill_frame_top = 830
    skill_frame_left = 1150
    skill_frame_width = 700
    skill_frame_height = 200
    skill_frame_box = {"top": skill_frame_top, "left": skill_frame_left, "width": skill_frame_width, "height": skill_frame_height}

    ## ok reset frame (+set party //+start // (+skip)) (bottom center)
    global ok_reset_frame_top
    global ok_reset_frame_left
    global ok_reset_frame_width
    global ok_reset_frame_height
    global ok_reset_frame_box
    ok_reset_frame_top = 950
    ok_reset_frame_left = 870
    ok_reset_frame_width = 180
    ok_reset_frame_height = 80
    ok_reset_frame_box = {"top": ok_reset_frame_top, "left": ok_reset_frame_left, "width": ok_reset_frame_width, "height": ok_reset_frame_height}

    ## select stage 1 (center)
    global select_stage_1_frame_top
    global select_stage_1_frame_left
    global select_stage_1_frame_width
    global select_stage_1_frame_height
    global select_stage_1_frame_box
    select_stage_1_frame_top = 700
    select_stage_1_frame_left = 890
    select_stage_1_frame_width = 100
    select_stage_1_frame_height = 100
    select_stage_1_frame_box = {"top": select_stage_1_frame_top, "left": select_stage_1_frame_left, "width": select_stage_1_frame_width, "height": select_stage_1_frame_height}

    ## select stage 2 (center)
    global select_stage_2_frame_top
    global select_stage_2_frame_left
    global select_stage_2_frame_width
    global select_stage_2_frame_height
    global select_stage_2_frame_box
    select_stage_2_frame_top = 540
    select_stage_2_frame_left = 890
    select_stage_2_frame_width = 100
    select_stage_2_frame_height = 100
    select_stage_2_frame_box = {"top": select_stage_2_frame_top, "left": select_stage_2_frame_left, "width": select_stage_2_frame_width, "height": select_stage_2_frame_height}

    ## select stage 3 (center)
    global select_stage_3_frame_top
    global select_stage_3_frame_left
    global select_stage_3_frame_width
    global select_stage_3_frame_height
    global select_stage_3_frame_box
    select_stage_3_frame_top = 380
    select_stage_3_frame_left = 890
    select_stage_3_frame_width = 100
    select_stage_3_frame_height = 100
    select_stage_3_frame_box = {"top": select_stage_3_frame_top, "left": select_stage_3_frame_left, "width": select_stage_3_frame_width, "height": select_stage_3_frame_height}

    ## confirm reset (center right)
    global confirm_reset_frame_top
    global confirm_reset_frame_left
    global confirm_reset_frame_width
    global confirm_reset_frame_height
    global confirm_reset_frame_box
    confirm_reset_frame_top = 590
    confirm_reset_frame_left = 970
    confirm_reset_frame_width = 160
    confirm_reset_frame_height = 60
    confirm_reset_frame_box = {"top": confirm_reset_frame_top, "left": confirm_reset_frame_left, "width": confirm_reset_frame_width, "height": confirm_reset_frame_height}

    ## save team (bottom center)
    global save_team_frame_top
    global save_team_frame_left
    global save_team_frame_width
    global save_team_frame_height
    global save_team_frame_box
    save_team_frame_top = 845
    save_team_frame_left = 870
    save_team_frame_width = 180
    save_team_frame_height = 80
    save_team_frame_box = {"top": save_team_frame_top, "left": save_team_frame_left, "width": save_team_frame_width, "height": save_team_frame_height}

    ## confirm team (center right)
    global confirm_team_frame_top
    global confirm_team_frame_left
    global confirm_team_frame_width
    global confirm_team_frame_height
    global confirm_team_frame_box
    confirm_team_frame_top = 650
    confirm_team_frame_left = 970
    confirm_team_frame_width = 160
    confirm_team_frame_height = 60
    confirm_team_frame_box = {"top": confirm_team_frame_top, "left": confirm_team_frame_left, "width": confirm_team_frame_width, "height": confirm_team_frame_height}

    ## use stamina potion (bottom center)
    global use_stamina_potion_frame_top
    global use_stamina_potion_frame_left
    global use_stamina_potion_frame_width
    global use_stamina_potion_frame_height
    global use_stamina_potion_frame_box
    use_stamina_potion_frame_top = 770
    use_stamina_potion_frame_left = 920
    use_stamina_potion_frame_width = 80
    use_stamina_potion_frame_height = 70
    use_stamina_potion_frame_box = {"top": use_stamina_potion_frame_top, "left": use_stamina_potion_frame_left, "width": use_stamina_potion_frame_width, "height": use_stamina_potion_frame_height}

    ## team
    global team_frame_top
    global team_frame_left
    global team_frame_width
    global team_frame_height
    global team_frame_box
    team_frame_top = 877
    team_frame_left = 824
    team_frame_width = 270
    team_frame_height = 67
    team_frame_box = {"top": team_frame_top, "left": team_frame_left, "width": team_frame_width, "height": team_frame_height}

    ## matrona health
    global matrona_health_frame_top
    global matrona_health_frame_left
    global matrona_health_frame_width
    global matrona_health_frame_height
    global matrona_health_frame_box
    matrona_health_frame_top = 948
    matrona_health_frame_left = 960
    matrona_health_frame_width = 70
    matrona_health_frame_height = 10
    matrona_health_frame_box = {"top": matrona_health_frame_top, "left": matrona_health_frame_left, "width": matrona_health_frame_width, "height": matrona_health_frame_height}

    ## beast status bar frame
    global beast_status_bar_frame_top
    global beast_status_bar_frame_left
    global beast_status_bar_frame_width
    global beast_status_bar_frame_height
    global beast_status_bar_frame_box
    beast_status_bar_frame_top = 46
    beast_status_bar_frame_left = 178
    beast_status_bar_frame_width = 400
    beast_status_bar_frame_height = 35
    beast_status_bar_frame_box = {"top": beast_status_bar_frame_top, "left": beast_status_bar_frame_left, "width": beast_status_bar_frame_width, "height": beast_status_bar_frame_height}

    ## boss hp frame
    global boss_hp_frame_top
    global boss_hp_frame_left
    global boss_hp_frame_width
    global boss_hp_frame_height
    global boss_hp_frame_box
    boss_hp_frame_top = 80
    boss_hp_frame_left = 160
    boss_hp_frame_width = 310
    boss_hp_frame_height = 20
    boss_hp_frame_box = {"top": boss_hp_frame_top, "left": boss_hp_frame_left, "width": boss_hp_frame_width, "height": boss_hp_frame_height}

    ## forfeit battle frame
    global forfeit_battle_frame_top
    global forfeit_battle_frame_left
    global forfeit_battle_frame_width
    global forfeit_battle_frame_height
    global forfeit_battle_frame_box
    forfeit_battle_frame_top = 643
    forfeit_battle_frame_left = 870
    forfeit_battle_frame_width = 180
    forfeit_battle_frame_height = 30
    forfeit_battle_frame_box = {"top": forfeit_battle_frame_top, "left": forfeit_battle_frame_left, "width": forfeit_battle_frame_width, "height": forfeit_battle_frame_height}

    ## full frame
    global frame_top
    global frame_left
    global frame_width
    global frame_height
    global frame_box
    frame_top = 30
    frame_left = 50
    frame_width = 1820
    frame_height = 1050
    frame_box = {"top": frame_top, "left": frame_left, "width": frame_width, "height": frame_height}


def setup_death_match():
    ## image pathes
    battle_path = "images/menu/Battle.png"
    boss_battle_path = "images/menu/Boss_Battle.png"
    death_match_chance_0_path = "images/menu/death_match_chance_0.png"
    boss_battle_extreme_path = "images/menu/boss_battle_extreme.png"
    auto_clear_path = "images/menu/auto_clear.png"
    start_auto_clear_path = "images/menu/start_auto_clear.png"
    death_match_ok_path = "images/menu/death_match_ok.png"
    death_match_hell_path = "images/menu/death_match_hell.png"
    ai_path = "images/menu/AI.png"
    invite_ai_path = "images/menu/invite_ai.png"
    preparation_complete_path = "images/menu/preparation_complete.png"
    death_match_start_path = "images/menu/death_match_start.png"
    death_match_success_ok_path = "images/menu/death_match_success_ok.png"
    auto_path = "images/battle/auto.png"

    global battle_img
    battle_img = cv2.imread(battle_path)
    global boss_battle_img
    boss_battle_img = cv2.imread(boss_battle_path)
    global death_match_chance_0_img
    death_match_chance_0_img = cv2.imread(death_match_chance_0_path)
    global boss_battle_extreme_img
    boss_battle_extreme_img = cv2.imread(boss_battle_extreme_path)
    global auto_clear_img
    auto_clear_img = cv2.imread(auto_clear_path)
    global start_auto_clear_img
    start_auto_clear_img = cv2.imread(start_auto_clear_path)
    global death_match_ok_img
    death_match_ok_img = cv2.imread(death_match_ok_path)
    global death_match_hell_img
    death_match_hell_img = cv2.imread(death_match_hell_path)
    global ai_img
    ai_img = cv2.imread(ai_path)
    global invite_ai_img
    invite_ai_img = cv2.imread(invite_ai_path)
    global preparation_complete_img
    preparation_complete_img = cv2.imread(preparation_complete_path)
    global death_match_start_img
    death_match_start_img = cv2.imread(death_match_start_path)
    global death_match_success_ok_img
    death_match_success_ok_img = cv2.imread(death_match_success_ok_path)
    global auto_img
    auto_img = cv2.imread(auto_path)


# def setup_daily_menu():
#     ## image pathes
#     tavern_path = "images/menu/Tavern.png"
#     quests_path = "images/menu/Quests.png"
#     heroes_path = "images/menu/Heroes.png"
#     draw_path = "images/menu/Draw.png"
#     shop_path = "images/menu/Shop.png"
#
#     menu_path = "images/menu/Menu.png"
#     friends_path = "images/menu/Friends.png"
#     send_all_path = "images/menu/Send_All.png"
#
#     mail_path = "images/menu/mail.png"
#     friendship_path = "images/menu/Friendship.png"
#     claim_all_path = "images/menu/Claim_All.png"
#     claim_all_gray_path = "images/menu/Claim_All_gray.png"
#
#     global tavern_img
#     tavern_img = cv2.imread(tavern_path)
#     global quests_img
#     quests_img = cv2.imread(quests_path)
#     global heroes_img
#     heroes_img = cv2.imread(heroes_path)
#     global draw_img
#     draw_img = cv2.imread(draw_path)
#     global shop_img
#     shop_img = cv2.imread(shop_path)
#
#     global menu_img
#     menu_img = cv2.imread(menu_path)
#     global friends_img
#     friends_img = cv2.imread(friends_path)
#     global send_all_img
#     send_all_img = cv2.imread(send_all_path)
#
#     global mail_img
#     mail_img = cv2.imread(mail_path)
#     global friendship_img
#     friendship_img = cv2.imread(friendship_path)
#     global claim_all_img
#     claim_all_img = cv2.imread(claim_all_path)
#     global claim_all_gray_img
#     claim_all_gray_img = cv2.imread(claim_all_gray_path)


# def setup_daily_states():
#     global FRIENDS_STATE
#     FRIENDS_STATE = True
#
#     global MAIL_STATE
#     MAIL_STATE = False
#
#     global SHOP_STATE
#     SHOP_STATE = False
#     global EQUIPMENT_DRAW_STATE
#     EQUIPMENT_DRAW_STATE = False
#     global COIN_SHOP_STATE
#     COIN_SHOP_STATE = False


def setup_demonic_beast_battle_menu():
    ## image pathes
    ready_path = "images/battle/ready.png"
    phase1_path = "images/battle/phase1.png"
    phase2_path = "images/battle/phase2.png"
    phase3_path = "images/battle/phase3.png"
    phase4_path = "images/battle/phase4.png"
    ok_path = "images/menu/ok.png"
    reset_path = "images/menu/reset.png"
    set_party_path = "images/menu/set_party.png"
    start_path = "images/menu/start.png"
    confirm_reset_path = "images/menu/confirm_reset.png"
    save_team_path = "images/menu/save.png"
    confirm_team_path = "images/menu/confirm_ok.png"
    weekly_reset_ok_path = "images/menu/weekly_reset_ok.png"
    use_stamina_potion_path = "images/menu/use_stamina_potion.png"
    reconnect_path = "images/menu/reconnect.png"
    failed_ok_path = "images/menu/failed_ok.png"
    attack_buff_path = "images/battle/attack_buff.png"
    evasion_buff_path = "images/battle/evasion_buff.png"
    reflect_buff_path = "images/battle/reflect_buff.png"
    forfeit_battle_path = "images/menu/forfeit_battle.png"

    # bird
    stage_open_bird_1_path = "images/demonic_beast/stage_open_bird_1.png"
    stage_open_bird_2_path = "images/demonic_beast/stage_open_bird_2.png"
    stage_open_bird_3_path = "images/demonic_beast/stage_open_bird_3.png"
    stage_cleared_bird_path = "images/demonic_beast/stage_cleared_bird.png"
    team_bird_path = "images/demonic_beast/team_bird.png"
    matrona_health_min2_path = "images/demonic_beast/matrona_health_min2.png"
    matrona_health_min3_path = "images/demonic_beast/matrona_health_min3.png"
    stage3_phase3_hp_min_path = "images/demonic_beast/stage3_phase3_hp_min.png"
    # deer
    stage_open_deer_path = "images/demonic_beast/stage_open_deer.png"
    stage_cleared_deer_path = "images/demonic_beast/stage_cleared_deer.png"
    # team_deer_path = "images/demonic_beast/team_deer.png"

    ## images
    global ready_img
    ready_img = cv2.imread(ready_path)
    global phase1_img
    phase1_img = cv2.imread(phase1_path)
    global phase2_img
    phase2_img = cv2.imread(phase2_path)
    global phase3_img
    phase3_img = cv2.imread(phase3_path)
    global phase4_img
    phase4_img = cv2.imread(phase4_path)
    global ok_img
    ok_img = cv2.imread(ok_path)
    global reset_img
    reset_img = cv2.imread(reset_path)
    global set_party_img
    set_party_img = cv2.imread(set_party_path)
    global start_img
    start_img = cv2.imread(start_path)
    global confirm_reset_img
    confirm_reset_img = cv2.imread(confirm_reset_path)
    global save_team_img
    save_team_img = cv2.imread(save_team_path)
    global confirm_team_img
    confirm_team_img = cv2.imread(confirm_team_path)
    global weekly_reset_ok_img
    weekly_reset_ok_img = cv2.imread(weekly_reset_ok_path)
    global use_stamina_potion_img
    use_stamina_potion_img = cv2.imread(use_stamina_potion_path)
    global reconnect_img
    reconnect_img = cv2.imread(reconnect_path)
    global failed_ok_img
    failed_ok_img = cv2.imread(failed_ok_path)
    global attack_buff_img
    attack_buff_img = cv2.imread(attack_buff_path)
    global evasion_buff_img
    evasion_buff_img = cv2.imread(evasion_buff_path)
    global reflect_buff_img
    reflect_buff_img = cv2.imread(reflect_buff_path)
    global forfeit_battle_img
    forfeit_battle_img = cv2.imread(forfeit_battle_path)

    # bird
    global stage_open_bird_1_img
    stage_open_bird_1_img = cv2.imread(stage_open_bird_1_path)
    global stage_open_bird_2_img
    stage_open_bird_2_img = cv2.imread(stage_open_bird_2_path)
    global stage_open_bird_3_img
    stage_open_bird_3_img = cv2.imread(stage_open_bird_3_path)
    global stage_cleared_bird_img
    stage_cleared_bird_img = cv2.imread(stage_cleared_bird_path)
    global team_bird_img
    team_bird_img = cv2.imread(team_bird_path)
    global matrona_health_min2_img
    matrona_health_min2_img = cv2.imread(matrona_health_min2_path)
    global matrona_health_min3_img
    matrona_health_min3_img = cv2.imread(matrona_health_min3_path)
    global stage3_phase3_hp_min_img
    stage3_phase3_hp_min_img = cv2.imread(stage3_phase3_hp_min_path)
    # deer
    global stage_open_deer_img
    stage_open_deer_img = cv2.imread(stage_open_deer_path)
    global stage_cleared_deer_img
    stage_cleared_deer_img = cv2.imread(stage_cleared_deer_path)
    # global team_deer_img
    # team_deer_img = cv2.imread(team_deer_path)


def setup_cards():
    ## image pathes
    # brun
    brun1_lvl1_path = "images/skills/brun1_lvl1.png"
    brun2_lvl1_path = "images/skills/brun2_lvl1.png"
    brun1_lvl2_path = "images/skills/brun1_lvl2.png"
    brun2_lvl2_path = "images/skills/brun2_lvl2.png"
    brun1_lvl3_path = "images/skills/brun1_lvl3.png"
    brun2_lvl3_path = "images/skills/brun2_lvl3.png"
    brun_ult_path = "images/skills/brun_ult.png"
    # mat
    mat1_lvl1_path = "images/skills/mat1_lvl1.png"
    mat2_lvl1_path = "images/skills/mat2_lvl1.png"
    mat1_lvl2_path = "images/skills/mat1_lvl2.png"
    mat2_lvl2_path = "images/skills/mat2_lvl2.png"
    mat1_lvl3_path = "images/skills/mat1_lvl3.png"
    mat2_lvl3_path = "images/skills/mat2_lvl3.png"
    mat_ult_path = "images/skills/mat_ult.png"
    # gow
    gow1_lvl1_path = "images/skills/gow1_lvl1.png"
    gow2_lvl1_path = "images/skills/gow2_lvl1.png"
    gow1_lvl2_path = "images/skills/gow1_lvl2.png"
    gow2_lvl2_path = "images/skills/gow2_lvl2.png"
    gow1_lvl3_path = "images/skills/gow1_lvl3.png"
    gow2_lvl3_path = "images/skills/gow2_lvl3.png"
    gow_ult_path = "images/skills/gow_ult.png"
    # mel
    mel1_lvl1_path = "images/skills/mel1_lvl1.png"
    mel2_lvl1_path = "images/skills/mel2_lvl1.png"
    mel1_lvl2_path = "images/skills/mel1_lvl2.png"
    mel2_lvl2_path = "images/skills/mel2_lvl2.png"
    mel1_lvl3_path = "images/skills/mel1_lvl3.png"
    mel2_lvl3_path = "images/skills/mel2_lvl3.png"
    mel_ult_path = "images/skills/mel_ult.png"
    # jor
    jor1_lvl1_path = "images/skills/jor1_lvl1.png"
    jor2_lvl1_path = "images/skills/jor2_lvl1.png"
    jor1_lvl2_path = "images/skills/jor1_lvl2.png"
    jor2_lvl2_path = "images/skills/jor2_lvl2.png"
    jor1_lvl3_path = "images/skills/jor1_lvl3.png"
    jor2_lvl3_path = "images/skills/jor2_lvl3.png"
    jor_ult_path = "images/skills/jor_ult.png"
    # skadi
    skadi1_lvl1_path = "images/skills/skadi1_lvl1.png"
    skadi2_lvl1_path = "images/skills/skadi2_lvl1.png"
    skadi1_lvl2_path = "images/skills/skadi1_lvl2.png"
    skadi2_lvl2_path = "images/skills/skadi2_lvl2.png"
    skadi1_lvl3_path = "images/skills/skadi1_lvl3.png"
    skadi2_lvl3_path = "images/skills/skadi2_lvl3.png"
    skadi_ult_path = "images/skills/skadi_ult.png"
    # one
    one1_lvl1_path = "images/skills/one1_lvl1.png"
    one2_lvl1_path = "images/skills/one2_lvl1.png"
    one1_lvl2_path = "images/skills/one1_lvl2.png"
    one2_lvl2_path = "images/skills/one2_lvl2.png"
    one1_lvl3_path = "images/skills/one1_lvl3.png"
    one2_lvl3_path = "images/skills/one2_lvl3.png"
    one_ult_path = "images/skills/one_ult.png"

    ## images
    # brun
    brun1_lvl1_img = cv2.imread(brun1_lvl1_path)
    brun2_lvl1_img = cv2.imread(brun2_lvl1_path)
    brun1_lvl2_img = cv2.imread(brun1_lvl2_path)
    brun2_lvl2_img = cv2.imread(brun2_lvl2_path)
    brun1_lvl3_img = cv2.imread(brun1_lvl3_path)
    brun2_lvl3_img = cv2.imread(brun2_lvl3_path)
    brun_ult_img = cv2.imread(brun_ult_path)
    # mat
    mat1_lvl1_img = cv2.imread(mat1_lvl1_path)
    mat2_lvl1_img = cv2.imread(mat2_lvl1_path)
    mat1_lvl2_img = cv2.imread(mat1_lvl2_path)
    mat2_lvl2_img = cv2.imread(mat2_lvl2_path)
    mat1_lvl3_img = cv2.imread(mat1_lvl3_path)
    mat2_lvl3_img = cv2.imread(mat2_lvl3_path)
    mat_ult_img = cv2.imread(mat_ult_path)
    # gow
    gow1_lvl1_img = cv2.imread(gow1_lvl1_path)
    gow2_lvl1_img = cv2.imread(gow2_lvl1_path)
    gow1_lvl2_img = cv2.imread(gow1_lvl2_path)
    gow2_lvl2_img = cv2.imread(gow2_lvl2_path)
    gow1_lvl3_img = cv2.imread(gow1_lvl3_path)
    gow2_lvl3_img = cv2.imread(gow2_lvl3_path)
    gow_ult_img = cv2.imread(gow_ult_path)
    # mel
    mel1_lvl1_img = cv2.imread(mel1_lvl1_path)
    mel2_lvl1_img = cv2.imread(mel2_lvl1_path)
    mel1_lvl2_img = cv2.imread(mel1_lvl2_path)
    mel2_lvl2_img = cv2.imread(mel2_lvl2_path)
    mel1_lvl3_img = cv2.imread(mel1_lvl3_path)
    mel2_lvl3_img = cv2.imread(mel2_lvl3_path)
    mel_ult_img = cv2.imread(mel_ult_path)
    # jor
    jor1_lvl1_img = cv2.imread(jor1_lvl1_path)
    jor2_lvl1_img = cv2.imread(jor2_lvl1_path)
    jor1_lvl2_img = cv2.imread(jor1_lvl2_path)
    jor2_lvl2_img = cv2.imread(jor2_lvl2_path)
    jor1_lvl3_img = cv2.imread(jor1_lvl3_path)
    jor2_lvl3_img = cv2.imread(jor2_lvl3_path)
    jor_ult_img = cv2.imread(jor_ult_path)
    # skadi
    skadi1_lvl1_img = cv2.imread(skadi1_lvl1_path)
    skadi2_lvl1_img = cv2.imread(skadi2_lvl1_path)
    skadi1_lvl2_img = cv2.imread(skadi1_lvl2_path)
    skadi2_lvl2_img = cv2.imread(skadi2_lvl2_path)
    skadi1_lvl3_img = cv2.imread(skadi1_lvl3_path)
    skadi2_lvl3_img = cv2.imread(skadi2_lvl3_path)
    skadi_ult_img = cv2.imread(skadi_ult_path)
    # one
    one1_lvl1_img = cv2.imread(one1_lvl1_path)
    one2_lvl1_img = cv2.imread(one2_lvl1_path)
    one1_lvl2_img = cv2.imread(one1_lvl2_path)
    one2_lvl2_img = cv2.imread(one2_lvl2_path)
    one1_lvl3_img = cv2.imread(one1_lvl3_path)
    one2_lvl3_img = cv2.imread(one2_lvl3_path)
    one_ult_img = cv2.imread(one_ult_path)

    ## skill images width and height
    # brun
    brun1_lvl1_width  = brun1_lvl1_img.shape[1]
    brun1_lvl1_height = brun1_lvl1_img.shape[0]
    brun2_lvl1_width  = brun2_lvl1_img.shape[1]
    brun2_lvl1_height = brun2_lvl1_img.shape[0]
    brun1_lvl2_width  = brun1_lvl2_img.shape[1]
    brun1_lvl2_height = brun1_lvl2_img.shape[0]
    brun2_lvl2_width  = brun2_lvl2_img.shape[1]
    brun2_lvl2_height = brun2_lvl2_img.shape[0]
    brun1_lvl3_width  = brun1_lvl3_img.shape[1]
    brun1_lvl3_height = brun1_lvl3_img.shape[0]
    brun2_lvl3_width  = brun2_lvl3_img.shape[1]
    brun2_lvl3_height = brun2_lvl3_img.shape[0]
    brun_ult_width = brun_ult_img.shape[1]
    brun_ult_height = brun_ult_img.shape[0]
    # mat
    mat1_lvl1_width  = mat1_lvl1_img.shape[1]
    mat1_lvl1_height = mat1_lvl1_img.shape[0]
    mat2_lvl1_width  = mat2_lvl1_img.shape[1]
    mat2_lvl1_height = mat2_lvl1_img.shape[0]
    mat1_lvl2_width  = mat1_lvl2_img.shape[1]
    mat1_lvl2_height = mat1_lvl2_img.shape[0]
    mat2_lvl2_width  = mat2_lvl2_img.shape[1]
    mat2_lvl2_height = mat2_lvl2_img.shape[0]
    mat1_lvl3_width  = mat1_lvl3_img.shape[1]
    mat1_lvl3_height = mat1_lvl3_img.shape[0]
    mat2_lvl3_width  = mat2_lvl3_img.shape[1]
    mat2_lvl3_height = mat2_lvl3_img.shape[0]
    mat_ult_width = mat_ult_img.shape[1]
    mat_ult_height = mat_ult_img.shape[0]
    # gow
    gow1_lvl1_width  = gow1_lvl1_img.shape[1]
    gow1_lvl1_height = gow1_lvl1_img.shape[0]
    gow2_lvl1_width  = gow2_lvl1_img.shape[1]
    gow2_lvl1_height = gow2_lvl1_img.shape[0]
    gow1_lvl2_width  = gow1_lvl2_img.shape[1]
    gow1_lvl2_height = gow1_lvl2_img.shape[0]
    gow2_lvl2_width  = gow2_lvl2_img.shape[1]
    gow2_lvl2_height = gow2_lvl2_img.shape[0]
    gow1_lvl3_width  = gow1_lvl3_img.shape[1]
    gow1_lvl3_height = gow1_lvl3_img.shape[0]
    gow2_lvl3_width  = gow2_lvl3_img.shape[1]
    gow2_lvl3_height = gow2_lvl3_img.shape[0]
    gow_ult_width = gow_ult_img.shape[1]
    gow_ult_height = gow_ult_img.shape[0]
    # mel
    mel1_lvl1_width  = mel1_lvl1_img.shape[1]
    mel1_lvl1_height = mel1_lvl1_img.shape[0]
    mel2_lvl1_width  = mel2_lvl1_img.shape[1]
    mel2_lvl1_height = mel2_lvl1_img.shape[0]
    mel1_lvl2_width  = mel1_lvl2_img.shape[1]
    mel1_lvl2_height = mel1_lvl2_img.shape[0]
    mel2_lvl2_width  = mel2_lvl2_img.shape[1]
    mel2_lvl2_height = mel2_lvl2_img.shape[0]
    mel1_lvl3_width  = mel1_lvl3_img.shape[1]
    mel1_lvl3_height = mel1_lvl3_img.shape[0]
    mel2_lvl3_width  = mel2_lvl3_img.shape[1]
    mel2_lvl3_height = mel2_lvl3_img.shape[0]
    mel_ult_width = mel_ult_img.shape[1]
    mel_ult_height = mel_ult_img.shape[0]
    # jor
    jor1_lvl1_width = jor1_lvl1_img.shape[1]
    jor1_lvl1_height = jor1_lvl1_img.shape[0]
    jor2_lvl1_width = jor2_lvl1_img.shape[1]
    jor2_lvl1_height = jor2_lvl1_img.shape[0]
    jor1_lvl2_width = jor1_lvl2_img.shape[1]
    jor1_lvl2_height = jor1_lvl2_img.shape[0]
    jor2_lvl2_width = jor2_lvl2_img.shape[1]
    jor2_lvl2_height = jor2_lvl2_img.shape[0]
    jor1_lvl3_width = jor1_lvl3_img.shape[1]
    jor1_lvl3_height = jor1_lvl3_img.shape[0]
    jor2_lvl3_width = jor2_lvl3_img.shape[1]
    jor2_lvl3_height = jor2_lvl3_img.shape[0]
    jor_ult_width = jor_ult_img.shape[1]
    jor_ult_height = jor_ult_img.shape[0]
    # skadi
    skadi1_lvl1_width = skadi1_lvl1_img.shape[1]
    skadi1_lvl1_height = skadi1_lvl1_img.shape[0]
    skadi2_lvl1_width = skadi2_lvl1_img.shape[1]
    skadi2_lvl1_height = skadi2_lvl1_img.shape[0]
    skadi1_lvl2_width = skadi1_lvl2_img.shape[1]
    skadi1_lvl2_height = skadi1_lvl2_img.shape[0]
    skadi2_lvl2_width = skadi2_lvl2_img.shape[1]
    skadi2_lvl2_height = skadi2_lvl2_img.shape[0]
    skadi1_lvl3_width = skadi1_lvl3_img.shape[1]
    skadi1_lvl3_height = skadi1_lvl3_img.shape[0]
    skadi2_lvl3_width = skadi2_lvl3_img.shape[1]
    skadi2_lvl3_height = skadi2_lvl3_img.shape[0]
    skadi_ult_width = skadi_ult_img.shape[1]
    skadi_ult_height = skadi_ult_img.shape[0]
    # one
    one1_lvl1_width = one1_lvl1_img.shape[1]
    one1_lvl1_height = one1_lvl1_img.shape[0]
    one2_lvl1_width = one2_lvl1_img.shape[1]
    one2_lvl1_height = one2_lvl1_img.shape[0]
    one1_lvl2_width = one1_lvl2_img.shape[1]
    one1_lvl2_height = one1_lvl2_img.shape[0]
    one2_lvl2_width = one2_lvl2_img.shape[1]
    one2_lvl2_height = one2_lvl2_img.shape[0]
    one1_lvl3_width = one1_lvl3_img.shape[1]
    one1_lvl3_height = one1_lvl3_img.shape[0]
    one2_lvl3_width = one2_lvl3_img.shape[1]
    one2_lvl3_height = one2_lvl3_img.shape[0]
    one_ult_width = one_ult_img.shape[1]
    one_ult_height = one_ult_img.shape[0]

    ## skill rectangle colors
    # brun
    brun1_lvl1_color = (0, 128, 255)  # same as one
    brun2_lvl1_color = (0, 255, 255)
    brun1_lvl2_color = (0, 128, 255)
    brun2_lvl2_color = (0, 255, 255)
    brun1_lvl3_color = (0, 128, 255)
    brun2_lvl3_color = (0, 255, 255)
    brun_ult_color = (0, 0, 255)
    # mat
    mat1_lvl1_color = (128, 255, 128)  # same as skadi
    mat2_lvl1_color = (255, 255, 255)
    mat1_lvl2_color = (128, 255, 128)
    mat2_lvl2_color = (255, 255, 255)
    mat1_lvl3_color = (128, 255, 128)
    mat2_lvl3_color = (255, 255, 255)
    mat_ult_color = (0, 255, 0)
    # gow
    gow1_lvl1_color = (128, 0, 255)  # same as jor
    gow2_lvl1_color = (255, 0, 255)
    gow1_lvl2_color = (128, 0, 255)
    gow2_lvl2_color = (255, 0, 255)
    gow1_lvl3_color = (128, 0, 255)
    gow2_lvl3_color = (255, 0, 255)
    gow_ult_color = (0, 0, 0)
    # mel
    mel1_lvl1_color = (255, 128, 0)  # same as
    mel2_lvl1_color = (255, 255, 0)
    mel1_lvl2_color = (255, 128, 0)
    mel2_lvl2_color = (255, 255, 0)
    mel1_lvl3_color = (255, 128, 0)
    mel2_lvl3_color = (255, 255, 0)
    mel_ult_color = (255, 0, 0)
    # jor
    jor1_lvl1_color = (128, 0, 255)  # same as gow
    jor2_lvl1_color = (255, 0, 255)
    jor1_lvl2_color = (128, 0, 255)
    jor2_lvl2_color = (255, 0, 255)
    jor1_lvl3_color = (128, 0, 255)
    jor2_lvl3_color = (255, 0, 255)
    jor_ult_color = (0, 0, 0)
    # skadi
    skadi1_lvl1_color = (128, 255, 128)  # same as mat
    skadi2_lvl1_color = (255, 255, 255)
    skadi1_lvl2_color = (128, 255, 128)
    skadi2_lvl2_color = (255, 255, 255)
    skadi1_lvl3_color = (128, 255, 128)
    skadi2_lvl3_color = (255, 255, 255)
    skadi_ult_color = (0, 255, 0)
    # one
    one1_lvl1_color = (0, 128, 255)  # same as brun
    one2_lvl1_color = (0, 255, 255)
    one1_lvl2_color = (0, 128, 255)
    one2_lvl2_color = (0, 255, 255)
    one1_lvl3_color = (0, 128, 255)
    one2_lvl3_color = (0, 255, 255)
    one_ult_color = (0, 0, 255)

    ## skill rectangle thickness
    # brun
    brun1_lvl1_thickness = 1
    brun2_lvl1_thickness = 1
    brun1_lvl2_thickness = 5
    brun2_lvl2_thickness = 5
    brun1_lvl3_thickness = 10
    brun2_lvl3_thickness = 10
    brun_ult_thickness = 10
    # mat
    mat1_lvl1_thickness = 1
    mat2_lvl1_thickness = 1
    mat1_lvl2_thickness = 5
    mat2_lvl2_thickness = 5
    mat1_lvl3_thickness = 10
    mat2_lvl3_thickness = 10
    mat_ult_thickness = 10
    # gow
    gow1_lvl1_thickness = 1
    gow2_lvl1_thickness = 1
    gow1_lvl2_thickness = 5
    gow2_lvl2_thickness = 5
    gow1_lvl3_thickness = 10
    gow2_lvl3_thickness = 10
    gow_ult_thickness = 10
    # mel
    mel1_lvl1_thickness = 1
    mel2_lvl1_thickness = 1
    mel1_lvl2_thickness = 5
    mel2_lvl2_thickness = 5
    mel1_lvl3_thickness = 10
    mel2_lvl3_thickness = 10
    mel_ult_thickness = 10
    # jor
    jor1_lvl1_thickness = 1
    jor2_lvl1_thickness = 1
    jor1_lvl2_thickness = 5
    jor2_lvl2_thickness = 5
    jor1_lvl3_thickness = 10
    jor2_lvl3_thickness = 10
    jor_ult_thickness = 10
    # skadi
    skadi1_lvl1_thickness = 1
    skadi2_lvl1_thickness = 1
    skadi1_lvl2_thickness = 5
    skadi2_lvl2_thickness = 5
    skadi1_lvl3_thickness = 10
    skadi2_lvl3_thickness = 10
    skadi_ult_thickness = 10
    # one
    one1_lvl1_thickness = 1
    one2_lvl1_thickness = 1
    one1_lvl2_thickness = 5
    one2_lvl2_thickness = 5
    one1_lvl3_thickness = 10
    one2_lvl3_thickness = 10
    one_ult_thickness = 10

    ## initialize skill objects
    # brun
    brun1_lvl1_Skill = Skills("brun1", 1, brun1_lvl1_path, brun1_lvl1_img, brun1_lvl1_width, brun1_lvl1_height, brun1_lvl1_color, brun1_lvl1_thickness)
    brun2_lvl1_Skill = Skills("brun2", 1, brun2_lvl1_path, brun2_lvl1_img, brun2_lvl1_width, brun2_lvl1_height, brun2_lvl1_color, brun2_lvl1_thickness)
    brun1_lvl2_Skill = Skills("brun1", 2, brun1_lvl2_path, brun1_lvl2_img, brun1_lvl2_width, brun1_lvl2_height, brun1_lvl2_color, brun1_lvl2_thickness)
    brun2_lvl2_Skill = Skills("brun2", 2, brun2_lvl2_path, brun2_lvl2_img, brun2_lvl2_width, brun2_lvl2_height, brun2_lvl2_color, brun2_lvl2_thickness)
    brun1_lvl3_Skill = Skills("brun1", 3, brun1_lvl3_path, brun1_lvl3_img, brun1_lvl3_width, brun1_lvl3_height, brun1_lvl3_color, brun1_lvl3_thickness)
    brun2_lvl3_Skill = Skills("brun2", 3, brun2_lvl3_path, brun2_lvl3_img, brun2_lvl3_width, brun2_lvl3_height, brun2_lvl3_color, brun2_lvl3_thickness)
    brun_ult_Skill = Skills("brun_ult", 3, brun_ult_path, brun_ult_img, brun_ult_width, brun_ult_height, brun_ult_color, brun_ult_thickness)
    # mat
    mat1_lvl1_Skill = Skills("mat1", 1, mat1_lvl1_path, mat1_lvl1_img, mat1_lvl1_width, mat1_lvl1_height, mat1_lvl1_color, mat1_lvl1_thickness)
    mat2_lvl1_Skill = Skills("mat2", 1, mat2_lvl1_path, mat2_lvl1_img, mat2_lvl1_width, mat2_lvl1_height, mat2_lvl1_color, mat2_lvl1_thickness)
    mat1_lvl2_Skill = Skills("mat1", 2, mat1_lvl2_path, mat1_lvl2_img, mat1_lvl2_width, mat1_lvl2_height, mat1_lvl2_color, mat1_lvl2_thickness)
    mat2_lvl2_Skill = Skills("mat2", 2, mat2_lvl2_path, mat2_lvl2_img, mat2_lvl2_width, mat2_lvl2_height, mat2_lvl2_color, mat2_lvl2_thickness)
    mat1_lvl3_Skill = Skills("mat1", 3, mat1_lvl3_path, mat1_lvl3_img, mat1_lvl3_width, mat1_lvl3_height, mat1_lvl3_color, mat1_lvl3_thickness)
    mat2_lvl3_Skill = Skills("mat2", 3, mat2_lvl3_path, mat2_lvl3_img, mat2_lvl3_width, mat2_lvl3_height, mat2_lvl3_color, mat2_lvl3_thickness)
    mat_ult_Skill = Skills("mat_ult", 3, mat_ult_path, mat_ult_img, mat_ult_width, mat_ult_height, mat_ult_color, mat_ult_thickness)
    # gow
    gow1_lvl1_Skill = Skills("gow1", 1, gow1_lvl1_path, gow1_lvl1_img, gow1_lvl1_width, gow1_lvl1_height, gow1_lvl1_color, gow1_lvl1_thickness)
    gow2_lvl1_Skill = Skills("gow2", 1, gow2_lvl1_path, gow2_lvl1_img, gow2_lvl1_width, gow2_lvl1_height, gow2_lvl1_color, gow2_lvl1_thickness)
    gow1_lvl2_Skill = Skills("gow1", 2, gow1_lvl2_path, gow1_lvl2_img, gow1_lvl2_width, gow1_lvl2_height, gow1_lvl2_color, gow1_lvl2_thickness)
    gow2_lvl2_Skill = Skills("gow2", 2, gow2_lvl2_path, gow2_lvl2_img, gow2_lvl2_width, gow2_lvl2_height, gow2_lvl2_color, gow2_lvl2_thickness)
    gow1_lvl3_Skill = Skills("gow1", 3, gow1_lvl3_path, gow1_lvl3_img, gow1_lvl3_width, gow1_lvl3_height, gow1_lvl3_color, gow1_lvl3_thickness)
    gow2_lvl3_Skill = Skills("gow2", 3, gow2_lvl3_path, gow2_lvl3_img, gow2_lvl3_width, gow2_lvl3_height, gow2_lvl3_color, gow2_lvl3_thickness)
    gow_ult_Skill = Skills("gow_ult", 3, gow_ult_path, gow_ult_img, gow_ult_width, gow_ult_height, gow_ult_color, gow_ult_thickness)
    # mel
    mel1_lvl1_Skill = Skills("mel1", 1, mel1_lvl1_path, mel1_lvl1_img, mel1_lvl1_width, mel1_lvl1_height, mel1_lvl1_color, mel1_lvl1_thickness)
    mel2_lvl1_Skill = Skills("mel2", 1, mel2_lvl1_path, mel2_lvl1_img, mel2_lvl1_width, mel2_lvl1_height, mel2_lvl1_color, mel2_lvl1_thickness)
    mel1_lvl2_Skill = Skills("mel1", 2, mel1_lvl2_path, mel1_lvl2_img, mel1_lvl2_width, mel1_lvl2_height, mel1_lvl2_color, mel1_lvl2_thickness)
    mel2_lvl2_Skill = Skills("mel2", 2, mel2_lvl2_path, mel2_lvl2_img, mel2_lvl2_width, mel2_lvl2_height, mel2_lvl2_color, mel2_lvl2_thickness)
    mel1_lvl3_Skill = Skills("mel1", 3, mel1_lvl3_path, mel1_lvl3_img, mel1_lvl3_width, mel1_lvl3_height, mel1_lvl3_color, mel1_lvl3_thickness)
    mel2_lvl3_Skill = Skills("mel2", 3, mel2_lvl3_path, mel2_lvl3_img, mel2_lvl3_width, mel2_lvl3_height, mel2_lvl3_color, mel2_lvl3_thickness)
    mel_ult_Skill = Skills("mel_ult", 3, mel_ult_path, mel_ult_img, mel_ult_width, mel_ult_height, mel_ult_color, mel_ult_thickness)
    # jor
    jor1_lvl1_Skill = Skills("jor1", 1, jor1_lvl1_path, jor1_lvl1_img, jor1_lvl1_width, jor1_lvl1_height, jor1_lvl1_color, jor1_lvl1_thickness)
    jor2_lvl1_Skill = Skills("jor2", 1, jor2_lvl1_path, jor2_lvl1_img, jor2_lvl1_width, jor2_lvl1_height, jor2_lvl1_color, jor2_lvl1_thickness)
    jor1_lvl2_Skill = Skills("jor1", 2, jor1_lvl2_path, jor1_lvl2_img, jor1_lvl2_width, jor1_lvl2_height, jor1_lvl2_color, jor1_lvl2_thickness)
    jor2_lvl2_Skill = Skills("jor2", 2, jor2_lvl2_path, jor2_lvl2_img, jor2_lvl2_width, jor2_lvl2_height, jor2_lvl2_color, jor2_lvl2_thickness)
    jor1_lvl3_Skill = Skills("jor1", 3, jor1_lvl3_path, jor1_lvl3_img, jor1_lvl3_width, jor1_lvl3_height, jor1_lvl3_color, jor1_lvl3_thickness)
    jor2_lvl3_Skill = Skills("jor2", 3, jor2_lvl3_path, jor2_lvl3_img, jor2_lvl3_width, jor2_lvl3_height, jor2_lvl3_color, jor2_lvl3_thickness)
    jor_ult_Skill = Skills("jor_ult", 3, jor_ult_path, jor_ult_img, jor_ult_width, jor_ult_height, jor_ult_color, jor_ult_thickness)
    # skadi
    skadi1_lvl1_Skill = Skills("skadi1", 1, skadi1_lvl1_path, skadi1_lvl1_img, skadi1_lvl1_width, skadi1_lvl1_height, skadi1_lvl1_color, skadi1_lvl1_thickness)
    skadi2_lvl1_Skill = Skills("skadi2", 1, skadi2_lvl1_path, skadi2_lvl1_img, skadi2_lvl1_width, skadi2_lvl1_height, skadi2_lvl1_color, skadi2_lvl1_thickness)
    skadi1_lvl2_Skill = Skills("skadi1", 2, skadi1_lvl2_path, skadi1_lvl2_img, skadi1_lvl2_width, skadi1_lvl2_height, skadi1_lvl2_color, skadi1_lvl2_thickness)
    skadi2_lvl2_Skill = Skills("skadi2", 2, skadi2_lvl2_path, skadi2_lvl2_img, skadi2_lvl2_width, skadi2_lvl2_height, skadi2_lvl2_color, skadi2_lvl2_thickness)
    skadi1_lvl3_Skill = Skills("skadi1", 3, skadi1_lvl3_path, skadi1_lvl3_img, skadi1_lvl3_width, skadi1_lvl3_height, skadi1_lvl3_color, skadi1_lvl3_thickness)
    skadi2_lvl3_Skill = Skills("skadi2", 3, skadi2_lvl3_path, skadi2_lvl3_img, skadi2_lvl3_width, skadi2_lvl3_height, skadi2_lvl3_color, skadi2_lvl3_thickness)
    skadi_ult_Skill = Skills("skadi_ult", 3, skadi_ult_path, skadi_ult_img, skadi_ult_width, skadi_ult_height, skadi_ult_color, skadi_ult_thickness)
    # one
    one1_lvl1_Skill = Skills("one1", 1, one1_lvl1_path, one1_lvl1_img, one1_lvl1_width, one1_lvl1_height, one1_lvl1_color, one1_lvl1_thickness)
    one2_lvl1_Skill = Skills("one2", 1, one2_lvl1_path, one2_lvl1_img, one2_lvl1_width, one2_lvl1_height, one2_lvl1_color, one2_lvl1_thickness)
    one1_lvl2_Skill = Skills("one1", 2, one1_lvl2_path, one1_lvl2_img, one1_lvl2_width, one1_lvl2_height, one1_lvl2_color, one1_lvl2_thickness)
    one2_lvl2_Skill = Skills("one2", 2, one2_lvl2_path, one2_lvl2_img, one2_lvl2_width, one2_lvl2_height, one2_lvl2_color, one2_lvl2_thickness)
    one1_lvl3_Skill = Skills("one1", 3, one1_lvl3_path, one1_lvl3_img, one1_lvl3_width, one1_lvl3_height, one1_lvl3_color, one1_lvl3_thickness)
    one2_lvl3_Skill = Skills("one2", 3, one2_lvl3_path, one2_lvl3_img, one2_lvl3_width, one2_lvl3_height, one2_lvl3_color, one2_lvl3_thickness)
    one_ult_Skill = Skills("one_ult", 3, one_ult_path, one_ult_img, one_ult_width, one_ult_height, one_ult_color, one_ult_thickness)

    for p in Skills:
        match p.name:
            case "brun1":
                p.threshold = 0.9
            case "brun2":
                p.threshold = 0.9
            case "brun_ult":
                p.threshold = 0.9
            case "mat1":
                p.threshold = 0.85
            case "mat2":
                p.threshold = 0.8
            case "mat_ult":
                p.threshold = 0.9
            case "gow1":
                p.threshold = 0.9
            case "gow2":
                p.threshold = 0.85
            case "gow_ult":
                p.threshold = 0.9
            case "mel1":
                p.threshold = 0.93
            case "mel2":
                p.threshold = 0.9
            case "mel_ult":
                p.threshold = 0.9
            case "jor1":
                p.threshold = 0.93
            case "jor2":
                p.threshold = 0.9
            case "jor_ult":
                p.threshold = 0.85
            case "skadi1":
                p.threshold = 0.93
            case "skadi2":
                p.threshold = 0.9
            case "skadi_ult":
                p.threshold = 0.9
            case "one1":
                p.threshold = 0.9
            case "one2":
                p.threshold = 0.9
            case "one_ult":
                p.threshold = 0.9
