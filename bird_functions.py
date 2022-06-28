from setup import *
import setup
from functions import *

def gow_bird():  # rank up
    gow2_lvl1_counter = 0
    gow2_lvl2_counter = 0
    gow2_lvl3_counter = 0
    for p in Skills:
        if p.name == "gow2" and p.count > 0:
            if p.level == 1:
                gow2_lvl1_counter = p.count
            elif p.level == 2:
                gow2_lvl2_counter = p.count
            elif p.level == 3:
                gow2_lvl3_counter = p.count

    gow2_counter = gow2_lvl1_counter + gow2_lvl2_counter + gow2_lvl3_counter
    if (gow2_lvl2_counter >= 1 or gow2_lvl3_counter >= 1) and (gow2_counter >= 2):
        for p in Skills:
            if p.name == "gow2" and p.count > 0:
                if p.level == 2:
                    setup.skillQueue.put((3, p, "use"))
                    break
                elif p.level == 3:
                    setup.skillQueue.put((2, p, "use"))
                    break


def brun_bird():  # power strike
    brun2_lvl1_counter = 0
    brun2_lvl2_counter = 0
    brun2_lvl3_counter = 0
    if setup.phase != 4:
        for p in Skills:
            if p.name == "brun2" and p.count > 0:
                if p.level == 1:
                    brun2_lvl1_counter = p.count
                elif p.level == 2:
                    brun2_lvl2_counter = p.count
                elif p.level == 3:
                    brun2_lvl3_counter = p.count

        brun2_counter = brun2_lvl1_counter + brun2_lvl2_counter + brun2_lvl3_counter
        if brun2_counter >= 4:
            for p in Skills:
                if p.name == "brun2" and p.count > 0:
                    if p.level == 1:
                        setup.skillQueue.put((90, p, "use"))
                        break
                    elif p.level == 2:
                        setup.skillQueue.put((110, p, "use"))
                        break
                    elif p.level == 3:
                        setup.skillQueue.put((120, p, "use"))
                        break


def mel_bird():  # amplify
    mel1_lvl1_counter = 0
    mel1_lvl2_counter = 0
    mel1_lvl3_counter = 0
    if setup.phase != 4:
        for p in Skills:
            if p.name == "mel1" and p.count > 0:
                if p.level == 1:
                    mel1_lvl1_counter = p.count
                elif p.level == 2:
                    mel1_lvl2_counter = p.count
                elif p.level == 3:
                    mel1_lvl3_counter = p.count

        mel1_counter = mel1_lvl1_counter + mel1_lvl2_counter + mel1_lvl3_counter
        if mel1_counter >= 2:
            for p in Skills:
                if p.name == "mel1" and p.count > 0:
                    if p.level == 1:
                        setup.skillQueue.put((70, p, "use"))
                        break
                    elif p.level == 2:
                        setup.skillQueue.put((80, p, "use"))
                        break
                    elif p.level == 3:
                        setup.skillQueue.put((100, p, "use"))
                        break


def mat_bird():  # taunt
    mat2_counter = 0
    for p in Skills:
        if p.name == "mat2" and p.count > 0:
            mat2_counter = mat2_counter + 1

    if mat2_counter >= 3:
        for p in Skills:
            if p.name == "mat2" and p.count > 0 and p.level < 3:
                setup.mat2_delay = 0


def bird_rules(skill_name):
    if setup.STAGE_1:
        if setup.phase == 3 and setup.mat2_delay_counter > 3:
            setup.mat2_delay_counter = 3

        if setup.mat2_delay_counter == 0:
            setup.mat2_delay = 0
        else:
            setup.mat2_delay_counter = setup.mat2_delay_counter - 1

        if skill_name == "mat2":
            setup.mat2_delay = 30
            if setup.phase != 3:
                setup.mat2_delay_counter = 11
            else:
                setup.mat2_delay_counter = 3
    elif setup.STAGE_2:
        if setup.phase == 2 and setup.mat2_delay_counter > 3:
            setup.mat2_delay_counter = 3

        if setup.mat2_delay_counter == 0:
            setup.mat2_delay = 0
        else:
            setup.mat2_delay_counter = setup.mat2_delay_counter - 1

        if skill_name == "mat2":
            setup.mat2_delay = 30
            if setup.phase != 2:
                setup.mat2_delay_counter = 11
            else:
                setup.mat2_delay_counter = 3
    elif setup.STAGE_3:
        if setup.mat2_delay_counter == 0:
            setup.mat2_delay = 0
        else:
            setup.mat2_delay_counter = setup.mat2_delay_counter - 1

        if skill_name == "mat2":
            setup.mat2_delay = 50
            setup.mat2_delay_counter = 11


def stage1_phase123_bird():
    for p in Skills:
        if p.count > 0:
            match p.name:
                case "brun1":
                    if p.level == 1:
                        setup.skillQueue.put((31, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((41, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((51, p, "use"))
                case "brun2":
                    pass
                case "brun_ult":
                    setup.skillQueue.put((28, p, "use"))
                case "mat1":
                    if p.level == 1:
                        setup.skillQueue.put((23, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((21, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((22, p, "use"))
                case "mat2":
                    if p.level == 3:
                        if p.count >= 2:
                            setup.skillQueue.put((5, p, "use"))
                        else:
                            pass
                    else:
                        setup.skillQueue.put((15 - p.level + setup.mat2_delay, p, "use"))
                case "mat_ult":
                    setup.skillQueue.put((29, p, "use"))
                case "gow1":
                    if p.level == 1:
                        setup.skillQueue.put((26, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((24, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((25, p, "use"))
                case "gow2":
                    if p.count == 1 or p.level >= 2:
                        pass
                    elif p.count > 1 and p.level == 1:
                        setup.skillQueue.put((10, p, "move"))
                case "gow_ult":
                    setup.skillQueue.put((19, p, "use"))
                case "mel1":
                    if p.count >= 2 and p.level == 1:
                        setup.skillQueue.put((17, p, "move"))
                case "mel2":
                    if p.level == 1:
                        setup.skillQueue.put((30, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((40, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((50, p, "use"))
                case "mel_ult":
                    setup.skillQueue.put((27, p, "use"))


def stage1_phase4_bird():
    for p in Skills:
        if p.count > 0:
            match p.name:
                case "brun1":
                    if p.level == 1:
                        setup.skillQueue.put((39, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((38, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((23, p, "use"))
                case "brun2":
                    if p.level == 1:
                        setup.skillQueue.put((22, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((21, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((20, p, "use"))
                case "brun_ult":
                    setup.skillQueue.put((35, p, "use"))
                case "mat1":
                    if p.level == 1:
                        setup.skillQueue.put((47, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((46, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((45, p, "use"))
                case "mat2":
                    if p.level == 3:
                        if p.count >= 2:
                            setup.skillQueue.put((5, p, "use"))
                        else:
                            pass
                    else:
                        setup.skillQueue.put((15 - p.level + setup.mat2_delay, p, "use"))
                case "mat_ult":
                    setup.skillQueue.put((36, p, "use"))
                case "gow1":
                    if p.level == 1:
                        setup.skillQueue.put((59, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((49, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((48, p, "use"))
                case "gow2":
                    if p.count == 1 or p.level >= 2:
                        pass
                    elif p.count > 1 and p.level == 1:
                        setup.skillQueue.put((10, p, "move"))
                case "gow_ult":
                    setup.skillQueue.put((37, p, "use"))
                case "mel1":
                    if p.level == 1:
                        if p.count >= 2:
                            setup.skillQueue.put((17, p, "move"))
                    elif p.level == 2:
                        setup.skillQueue.put((28, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((27, p, "use"))
                case "mel2":
                    if p.level == 1:
                        setup.skillQueue.put((32, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((31, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((30, p, "use"))
                case "mel_ult":
                    setup.skillQueue.put((26, p, "use"))


def stage2_phase12_bird():
    for p in Skills:
        if p.count > 0:
            match p.name:
                case "brun1":
                    if p.level == 1:
                        setup.skillQueue.put((33, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((34, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((56, p, "use"))
                case "brun2":
                    if p.level == 1:
                        setup.skillQueue.put((31, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((32, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((55, p, "use"))
                case "brun_ult":
                    setup.skillQueue.put((30, p, "use"))

                case "mel1":
                    if p.level == 1:
                        setup.skillQueue.put((60, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((61, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((62, p, "use"))
                case "mel2":
                    if p.level == 1:
                        setup.skillQueue.put((27, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((26, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((25, p, "use"))
                case "mel_ult":
                    setup.skillQueue.put((36 - setup.buff_remove_forward, p, "use"))

                case "mat1":
                    setup.skillQueue.put((40 - p.level - setup.buff_remove_forward, p, "use"))
                case "mat2":
                    if p.level == 3:
                        if p.count >= 2:
                            setup.skillQueue.put((5, p, "use"))
                        else:
                            pass
                    else:
                        setup.skillQueue.put((15 - p.level + setup.mat2_delay, p, "use"))
                case "mat_ult":
                    setup.skillQueue.put((40, p, "use"))

                case "gow1":
                    if p.level == 1:
                        setup.skillQueue.put((35, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((21, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((20, p, "use"))
                case "gow2":
                    if p.count == 1 or p.level >= 2:
                        pass
                    elif p.count > 1 and p.level == 1:
                        setup.skillQueue.put((10, p, "move"))
                case "gow_ult":
                    setup.skillQueue.put((41, p, "use"))


def stage2_phase3_bird(ready_count):
    damage_skills_count = 0
    for p in Skills:
        if (p.name == "brun1" and p.level >= 2) or p.name == "brun2" or p.name == "brun_ult" or p.name == "mel1" or p.name == "mel_ult":
            damage_skills_count = damage_skills_count + p.count  # TODO: auto merges can reduce damage skills

    if (damage_skills_count >= 4 and ready_count == 4) or setup.RUSH_STAGE2_PHASE3:
        setup.RUSH_STAGE2_PHASE3 = True
        clear_stage2_phase3_bird()
    else:
        stall_stage2_phase3_bird()
        gow_bird()
        mat_bird()


def clear_stage2_phase3_bird():
    for p in Skills:
        if p.count > 0:
            match p.name:
                case "brun1":
                    if p.level == 1:
                        setup.skillQueue.put((16, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((17, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((19, p, "use"))
                case "brun2":
                    if p.level == 1:
                        setup.skillQueue.put((13, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((14, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((18, p, "use"))
                case "brun_ult":
                    setup.skillQueue.put((11, p, "use"))

                case "mel1":
                    if p.level == 1:
                        setup.skillQueue.put((15, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((20, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((21, p, "use"))
                case "mel_ult":
                    setup.skillQueue.put((12, p, "use"))


def stall_stage2_phase3_bird():
    for p in Skills:
        if p.count > 0:
            match p.name:
                case "mel2":
                    if p.level == 1:
                        setup.skillQueue.put((26, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((27, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((28, p, "use"))

                case "mat1":
                    if p.level == 1:
                        setup.skillQueue.put((22, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((21, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((20, p, "use"))
                case "mat2":
                    if p.level == 3:
                        if p.count >= 2:
                            setup.skillQueue.put((5, p, "use"))
                        else:
                            pass
                    else:
                        setup.skillQueue.put((15 - p.level + setup.mat2_delay, p, "use"))
                case "mat_ult":
                    setup.skillQueue.put((29, p, "use"))

                case "gow1":
                    if p.level == 1:
                        setup.skillQueue.put((25, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((24, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((23, p, "use"))
                case "gow2":
                    if p.count == 1 or p.level >= 2:
                        pass
                    elif p.count > 1 and p.level == 1:
                        setup.skillQueue.put((10, p, "move"))
                case "gow_ult":
                    setup.skillQueue.put((30, p, "use"))


def stage2_phase4_bird():
    for p in Skills:
        if p.count > 0:
            match p.name:
                case "brun1":
                    if p.level == 1:
                        setup.skillQueue.put((30, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((24, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((22, p, "use"))
                case "brun2":
                    if p.level == 1:
                        setup.skillQueue.put((29, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((23, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((21, p, "use"))
                case "brun_ult":
                    setup.skillQueue.put((20, p, "use"))

                case "mel1":
                    if p.level == 1:
                        setup.skillQueue.put((31, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((26, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((25, p, "use"))
                case "mel2":
                    if p.level == 1:
                        setup.skillQueue.put((32, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((28, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((27, p, "use"))
                case "mel_ult":
                    setup.skillQueue.put((36 - setup.buff_remove_forward, p, "use"))

                case "mat1":
                    setup.skillQueue.put((40 - p.level - setup.buff_remove_forward, p, "use"))
                case "mat2":
                    if p.level == 3:
                        if p.count >= 2:
                            setup.skillQueue.put((5, p, "use"))
                        else:
                            pass
                    else:
                        setup.skillQueue.put((15 - p.level + setup.mat2_delay, p, "use"))
                case "mat_ult":
                    setup.skillQueue.put((33, p, "use"))

                case "gow1":
                    if p.level == 1:
                        setup.skillQueue.put((41, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((40, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((35, p, "use"))
                case "gow2":
                    if p.count == 1 or p.level >= 2:
                        pass
                    elif p.count > 1 and p.level == 1:
                        setup.skillQueue.put((10, p, "move"))
                case "gow_ult":
                    setup.skillQueue.put((34, p, "use"))


def stage3_phase12_bird():
    for p in Skills:
        if p.count > 0:
            match p.name:
                case "brun1":
                    if p.level == 1:
                        setup.skillQueue.put((30, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((31, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((48, p, "use"))
                case "brun2":
                    if p.level == 1:
                        setup.skillQueue.put((46, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((47, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((51, p, "use"))
                case "brun_ult":
                    setup.skillQueue.put((23, p, "use"))

                case "mel1":
                    if p.level == 1:
                        setup.skillQueue.put((49, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((50, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((52, p, "use"))
                case "mel2":
                    if p.level == 1:
                        setup.skillQueue.put((33, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((34, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((35, p, "use"))
                case "mel_ult":
                    setup.skillQueue.put((32, p, "use"))

                case "mat1":
                    if p.level == 1:
                        setup.skillQueue.put((25, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((26, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((27, p, "use"))
                case "mat2":
                    if p.level == 3:
                        if p.count >= 2:
                            setup.skillQueue.put((7, p, "use"))
                        else:
                            pass
                    else:
                        setup.skillQueue.put((15 - p.level + setup.mat2_delay, p, "use"))
                case "mat_ult":
                    setup.skillQueue.put((44, p, "use"))

                case "gow1":
                    if p.level == 1:
                        setup.skillQueue.put((20, p, "use"))
                    elif p.level == 2:
                        setup.skillQueue.put((21, p, "use"))
                    elif p.level == 3:
                        setup.skillQueue.put((22, p, "use"))
                case "gow2":
                    if p.count == 1 or p.level >= 2:
                        pass
                    elif p.count > 1 and p.level == 1:
                        setup.skillQueue.put((10, p, "move"))
                case "gow_ult":
                    setup.skillQueue.put((45, p, "use"))


def stage3_phase3_bird():
    for p in Skills:
        if p.count > 0:
            match p.name:
                case "brun1":
                    if not setup.EVASION:
                        if p.level == 1:
                            setup.skillQueue.put((23, p, "use"))
                        elif p.level == 2:
                            setup.skillQueue.put((22, p, "use"))
                        elif p.level == 3:
                            setup.skillQueue.put((21, p, "use"))
                case "brun2":
                    if not setup.EVASION:
                        if p.level == 1:
                            setup.skillQueue.put((29, p, "use"))
                        elif p.level == 2:
                            setup.skillQueue.put((25, p, "use"))
                        elif p.level == 3:
                            setup.skillQueue.put((24, p, "use"))
                case "brun_ult":
                    setup.skillQueue.put((20, p, "use"))

                case "mel1":
                    if not setup.EVASION:
                        if p.level == 1:
                            setup.skillQueue.put((31, p, "use"))
                        elif p.level == 2:
                            setup.skillQueue.put((32, p, "use"))
                        elif p.level == 3 and setup.STAGE3_PHASE3_HP_MIN:
                            setup.skillQueue.put((33, p, "use"))
                case "mel2":
                    if not setup.EVASION:
                        if p.level == 1:
                            setup.skillQueue.put((28, p, "use"))
                        elif p.level == 2:
                            setup.skillQueue.put((27, p, "use"))
                        elif p.level == 3:
                            setup.skillQueue.put((26, p, "use"))
                case "mel_ult":
                    setup.skillQueue.put((36 - setup.buff_remove_forward, p, "use"))

                case "mat1":
                    setup.skillQueue.put((40 - p.level - setup.buff_remove_forward, p, "use"))
                case "mat2":
                    if p.level == 3:
                        if p.count >= 2:
                            setup.skillQueue.put((5, p, "use"))
                        else:
                            pass
                    else:
                        setup.skillQueue.put((15 - p.level + setup.mat2_delay, p, "use"))
                case "mat_ult":
                    setup.skillQueue.put((40, p, "use"))

                case "gow1":
                    if not setup.EVASION:
                        if p.level == 1:
                            setup.skillQueue.put((97, p, "use"))
                        elif p.level == 2:
                            setup.skillQueue.put((96, p, "use"))
                        elif p.level == 3:
                            setup.skillQueue.put((95, p, "use"))
                    elif setup.EVASION:
                        if p.level == 1:
                            setup.skillQueue.put((46, p, "use"))
                        elif p.level == 2:
                            setup.skillQueue.put((45, p, "use"))
                        elif p.level == 3:
                            setup.skillQueue.put((20, p, "use"))
                case "gow2":
                    if p.count == 1 or p.level >= 2:
                        pass
                    elif p.count > 1 and p.level == 1:
                        setup.skillQueue.put((10, p, "move"))
                case "gow_ult":
                    setup.skillQueue.put((41, p, "use"))


def stage3_phase4_bird():
    for p in Skills:
        if p.count > 0:
            match p.name:
                case "brun1":
                    if not setup.EVASION:
                        if p.level == 1:
                            setup.skillQueue.put((31, p, "use"))
                        elif p.level == 2:
                            setup.skillQueue.put((27, p, "use"))
                        elif p.level == 3:
                            setup.skillQueue.put((26, p, "use"))
                case "brun2":
                    if not setup.EVASION:
                        if p.level == 1:
                            setup.skillQueue.put((30, p, "use"))
                        elif p.level == 2:
                            setup.skillQueue.put((25, p, "use"))
                        elif p.level == 3:
                            setup.skillQueue.put((24, p, "use"))
                case "brun_ult":
                    setup.skillQueue.put((23, p, "use"))

                case "mel1":
                    if not setup.EVASION:
                        if p.level == 1:
                            setup.skillQueue.put((22, p, "use"))
                        elif p.level == 2:
                            setup.skillQueue.put((21, p, "use"))
                        elif p.level == 3:
                            setup.skillQueue.put((20, p, "use"))
                case "mel2":
                    if not setup.EVASION:
                        if p.level == 1:
                            setup.skillQueue.put((32, p, "use"))
                        elif p.level == 2:
                            setup.skillQueue.put((29, p, "use"))
                        elif p.level == 3:
                            setup.skillQueue.put((28, p, "use"))
                case "mel_ult":
                    setup.skillQueue.put((36 - setup.buff_remove_forward, p, "use"))

                case "mat1":
                    setup.skillQueue.put((40 - p.level - setup.buff_remove_forward, p, "use"))
                case "mat2":
                    if p.level == 3:
                        if p.count >= 2:
                            setup.skillQueue.put((5, p, "use"))
                        else:
                            pass
                    else:
                        setup.skillQueue.put((15 - p.level + setup.mat2_delay, p, "use"))
                case "mat_ult":
                    setup.skillQueue.put((33, p, "use"))

                case "gow1":
                    if not setup.EVASION:
                        if p.level == 1:
                            setup.skillQueue.put((97, p, "use"))
                        elif p.level == 2:
                            setup.skillQueue.put((96, p, "use"))
                        elif p.level == 3:
                            setup.skillQueue.put((95, p, "use"))
                    elif setup.EVASION:
                        if p.level == 1:
                            setup.skillQueue.put((46, p, "use"))
                        elif p.level == 2:
                            setup.skillQueue.put((45, p, "use"))
                        elif p.level == 3:
                            setup.skillQueue.put((20, p, "use"))
                case "gow2":
                    if p.count == 1 or p.level >= 2:
                        pass
                    elif p.count > 1 and p.level == 1:
                        setup.skillQueue.put((10, p, "move"))
                case "gow_ult":
                    setup.skillQueue.put((34, p, "use"))
