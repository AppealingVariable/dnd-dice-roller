import FreeSimpleGUI as sg
import random
from InfoDict import attacks_dict
from InfoDict import current_max_level
from InfoDict import attack_roll_bonus
from InfoDict import attack_flat_damage
from pathlib import Path
import subprocess

def create_row(key):

    column_L = [sg.Text(key)]
    column_M = [sg.Push()]
    column_R = [sg.Text('Level')]
    for i in range(current_max_level + 1):
        if i == 0:
            column_R.append(sg.Radio(text=str(i), group_id=f"{key}RadioGroup", key=f"{key}Radio{i}",default=True))
        elif i <= attacks_dict[key]['Max Level'] :
            column_R.append(sg.Radio(text=str(i), group_id=f"{key}RadioGroup", key=f"{key}Radio{i}"))
        else:
            column_R.append(sg.Radio(text=str(i), group_id=f"{key}RadioGroup", key=f"{key}Radio{i}", disabled=True))
    return column_L + column_M + column_R

def roll_damage(roll_dict, crit=False):
    total_damage = []
    for key in roll_dict:
        if not key == 'Attack modifier' and roll_dict[key] and int(key[-1]) > 0: #checks for which radio buttons selected above 0
            attack_name = key[:-6] #easier to read what is happening
            dice_to_roll = attacks_dict[attack_name]['Start Dice Quantity']
            dice_rolls = []
            if attacks_dict[attack_name]['Per Level'] > 0:
                dice_to_roll += attacks_dict[attack_name]['Per Level'] * (int(key[-1]) - 1)
            print(f"{attack_name} rolls")
            for i in range(dice_to_roll):
                dice_rolls.append(random.randint(1, attacks_dict[key[:-6]]['Dice Size']))
            if crit:
                for i in range(dice_to_roll):
                    dice_rolls.append(attacks_dict[key[:-6]]['Dice Size'])
            print(f"{dice_rolls} \nTotal: {sum(dice_rolls)} {attacks_dict[attack_name]['Damage Type']} damage")
            total_damage.append(sum(dice_rolls))
    #print(f"All dice: {total_damage}")

    if total_damage != []:
        print(f"Flat modifiers: {attack_flat_damage}")
        print(f"Total damage: {sum(total_damage) + attack_flat_damage}")

def roll_attack(roll_dict):
    roll = random.randint(1, 20)
    print(f"Attack Roll: {roll}")
    print(f"Attack Modifier: {roll_dict['Attack modifier']}")
    if roll == 20:
        print(print(f"Total Attack Roll: {roll + int(roll_dict['Attack modifier'])} CRIT!"))
    else:
        print(f"Total Attack Roll: {roll + int(roll_dict['Attack modifier'])}")


def main_menu():
    layout = [[sg.Button('Roll Attack!'), sg.Text('Attack modifier'), sg.Input(key='Attack modifier', default_text=attack_roll_bonus)],
              [sg.Button('Roll Damage!'), sg.Button('Roll Critical Damage!'), sg.Push(), sg.Button('Clear and Roll'), sg.Push(), sg.Button('Clear Rolls')]]
    for key in attacks_dict:
        layout.append(create_row(key))
    layout.append([sg.Output(size=(30,20), key="Output", expand_x=True)])
    window = sg.Window(title='Dice Roller', layout=layout)
    while True:                             # The Event Loop
        event, values = window.read()
        #print(event,values)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'Roll Damage!':
            roll_damage(values)
        if event == 'Roll Critical Damage!':
            roll_damage(values, crit=True)
        if event == 'Roll Attack!':
            roll_attack(values)
        if event == 'Clear Rolls':
            window.find_element('Output').Update('')
        if event == 'Clear and Roll':
            window.find_element('Output').Update('')
            roll_damage(values)
main_menu()

# def main():
#     Path.cwd()
#     run_command = f'''cmd /k "cd /d {Path.cwd()} & .venv/Scripts/activate & python DiceRoller.pyw'''
#     subprocess.Popen(run_command, shell=True)