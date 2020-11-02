import yahtzee_core


def create_player(player_number: int) -> dict:
    """Prompt for player name, and create player with blank score card, with that name"""
    name = yahtzee_core.input_non_empty_string(
        f'Please Enter Player {player_number + 1} Name: ', 'INVALID! Input SOMETHING, ANYTHING!: ')
    player = {'name': name, 'scorecard': yahtzee_core.blank_scorecard.copy()}
    return player


def print_yahtzee():
    print('     __   __ _    _   _ _____ __________ _____ ')
    print('     \ \ / // \  | | | |_   _|__  / ____| ____|')
    print('      \ V // _ \ | |_| | | |   / /|  _| |  _|  ')
    print('       | |/ ___ \|  _  | | |  / /_| |___| |___ ')
    print('       |_/_/   \_\_| |_| |_| /____|_____|_____|\n')


def print_bonus():
    print("  .----------------.  .----------------.  .-----------------. .----------------.  .----------------. ")
    print(" | .--------------. || .--------------. || .--------------. || .--------------. || .--------------. |")
    print(" | |   ______     | || |     ____     | || | ____  _____  | || | _____  _____ | || |    _______   | |")
    print(" | |  |_   _ \    | || |   .'    `.   | || ||_   \|_   _| | || ||_   _||_   _|| || |   /  ___  |  | |")
    print(" | |    | |_) |   | || |  /  .--.  \  | || |  |   \ | |   | || |  | |    | |  | || |  |  (__ \_|  | |")
    print(" | |    |  __'.   | || |  | |    | |  | || |  | |\ \| |   | || |  | '    ' |  | || |   '.___`-.   | |")
    print(" | |   _| |__) |  | || |  \  `--'  /  | || | _| |_\   |_  | || |   \ `--' /   | || |  |`\____) |  | |")
    print(" | |  |_______/   | || |   `.____.'   | || ||_____|\____| | || |    `.__.'    | || |  |_______.'  | |")
    print(" | |              | || |              | || |              | || |              | || |              | |")
    print(" | '--------------' || '--------------' || '--------------' || '--------------' || '--------------' |")
    print("  '----------------'  '----------------'  '----------------'  '----------------'  '----------------' ")


def conduct_rolls(player: dict) -> tuple:
    """Conduct rolls for a player's turn in a round and returns final dice result"""
    hand = []
    temp_hand = []
    for n in range(3):
        input(
            f"\n{player['name']}'s Roll #{n + 1}.  Press Enter to roll Dice: ")
        number_to_roll = 5-len(hand)
        roll = yahtzee_core.roll_dice(number_to_roll)
        if n != 0:
            print(f'You kept: {hand}')
        print(f'You rolled: {sorted(roll)}')
        hand.extend(roll)
        if n == 2:
            print(f'Final hand: {sorted(hand)}')
            if len(set(hand)) == 1:
                print_yahtzee()
            return tuple(sorted(hand))
        print(f'Current hand: {sorted(hand)}')
        if len(set(hand)) == 1:
            print_yahtzee()
            ychoice = yahtzee_core.input_positive_integer(
                f'Enter 1 to accept Yahtzee or 2 to keep rolling: ', 'Incorrect Choice', 1, 2)
            if ychoice == 1:
                return tuple(hand)
        while True:
            try:
                if n == 0:
                    keepers = yahtzee_core.values_from_comma_delimited_string(
                        input(f'Enter keepers separated by commas(0 for none, X to end turn): '))
                else:
                    keepers = yahtzee_core.values_from_comma_delimited_string(
                        input(f'Enter comma separated keepers(0 for none, X to end turn, R to reroll with {sorted(temp_hand)}): '))
            except ValueError:
                print('invalid input')
                continue
            if 0 in keepers:
                hand = []
                temp_hand = []
                break
            if ('x' in keepers) or ('X' in keepers):
                return tuple(sorted(hand))
            if (('r' in keepers) or ('R' in keepers)) and n != 0:
                hand = temp_hand
                break
            dicecheck = yahtzee_core.values_not_in_group(hand, keepers)
            if len(dicecheck) != 0:
                print(f'Invalid dice entered ({dicecheck}) try again')
                continue
            else:
                hand = list(keepers)
                temp_hand = list(keepers)
                break


def choose_score(result: tuple, player: dict):
    """Presents player with options to score their completed turn, dependent on categories already scored"""
    print(f'\nCategory Score Choices for roll of {result}')
    choice = 0
    selection = {}
    if player['scorecard']['Yahtzee'] == 50 and len(set(result)) == 1:
        player['scorecard']['Bonus'] = player['scorecard']['Bonus'] + 100
        print_yahtzee()
        print_bonus()
    for key in player['scorecard']:
        try:
            if '' in player['scorecard'][key]:
                choice += 1
                print(
                    f'{choice:02}: {key:<20} Score: {yahtzee_core.score_for_category(key,result):>3}')
                selection[key] = choice
        except TypeError:
            continue
    scored = yahtzee_core.input_positive_integer(
        f'Enter Category number above to score (1 - {choice}): ', 'Incorrect Choice', 1, choice)
    for k in selection:
        if scored == selection[k]:
            player['scorecard'][k] = yahtzee_core.score_for_category(
                k, result)


def play_turn(player: dict):
    yahtzee_core.display_scorecard(player, yahtzee_core.keys_in_order)
    final_roll = conduct_rolls(player)
    choose_score(final_roll, player)


def play_round(players: list):
    for p in players:
        play_turn(p)


play_again = 'y'
while play_again == 'y':
    print_yahtzee()
    players = []
    num_players = yahtzee_core.input_positive_integer(
        'Input Number of Players (1-4): ', 'Invalid Entry try again (1-4)', 1, 4)
    for i in range(num_players):
        new_player = create_player(i)
        players.append(new_player)

    for turn in range(13):
        print(f'\n************************************************************')
        print(f'\n***********************Round {turn +1}******************************')
        print(f'\n************************************************************')
        for p in range(num_players):
            temp_score = 0
            for k,v in players[p]['scorecard'].items():
                try:
                    if v > 0:
                        temp_score += v
                except TypeError or NameError or ValueError:
                    continue          
            print(f"XXX {players[p]['name']:9}Score(not counting top bonus): {temp_score:<3} XXX")
        play_round(players)
    final_scores = []
    for p in players:
        grand_total = yahtzee_core.display_final_scorecard(
            p, yahtzee_core.keys_in_order)
        final_scores.append(grand_total)

    winning_score = max(final_scores)

    while True:
        for np in range(num_players):
            if winning_score == final_scores[np]:
                print(
                    f"{players[np]['name']} is the WINNER with {final_scores[np]} points!!!!!")
            else:
                print(
                    f"{players[np]['name']} is a LOSER with {final_scores[np]} points!!!!!\n")
        print('\nGame Over Menu')
        for p in range(num_players):
            print(f"{p + 1}: {players[p]['name']}'s Scorecard")
        print(f'{num_players +1}: Quit')
        print(f'{num_players +2}: Play Again')
        menu_choice = yahtzee_core.input_positive_integer(
            f'Enter Menu Choice 1 - {num_players + 2}: ', 'Invalid Choice', 1, num_players + 2)
        if menu_choice in range(num_players + 1):
            yahtzee_core.display_final_scorecard(
                players[menu_choice - 1], yahtzee_core.keys_in_order)
        elif menu_choice == num_players + 1:
            print('Goodbye')
            play_again = 'n'
            break
        elif menu_choice == num_players + 2:
            play_again = 'y'
            break
