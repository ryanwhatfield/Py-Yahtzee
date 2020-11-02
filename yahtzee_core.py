import random

blank_scorecard = {'Aces':'', 'Twos':'', 'Threes':'', 'Fours':'', 'Fives':'', 'Sixes':'', 'Three of a Kind':'', 'Four of a Kind':'', 'Full House':'', 'Small Straight':'', 'Large Straight':'', 'Chance':'', 'Yahtzee':'', 'Bonus':0}

keys_in_order = ['Aces', 'Twos', 'Threes', 'Fours', 'Fives', 'Sixes', 'Three of a Kind', 'Four of a Kind', 'Full House', 'Small Straight', 'Large Straight', 'Chance', 'Yahtzee', 'Bonus']

def input_positive_integer(prompt: str, warning: str, min: int, max: int) -> int:
    """Will present <prompt> for input, will not return until input is a positive integer in the given (inclusive) range of min and max. Will present <warning> if user inputs something invalid."""
    while True:
        try:
            num = int(input(prompt))
        except ValueError:
            print(warning)
            continue
        if num > max or num < min:
            print(warning)
            continue
        else:
            return num

def input_non_empty_string(prompt: str, warning: str) -> str:
    while True:
        entry = input(prompt)
        if entry.strip() != '':
            return entry
        print(warning)
    
def values_from_comma_delimited_string(input: str) -> tuple:
    """Takes a comma-delimited string and creates a tuple of the values between the commas.  Attempts to make each value an integer if possible.  Makes sure to handle the removal of any spaces the user may or may not have entered"""
    items = input.split(',')
    clean_items = []
    for a in items:
        clean_i = a.strip()
        if clean_i.isdigit():
            clean_items.append(int(clean_i))
        else:
            clean_items.append(clean_i)
    return tuple(clean_items)

def values_not_in_group(group: tuple, values: tuple) -> tuple:
    """Returns any values not present in group; empty tuple if all are present"""
    roll = list(group)
    picks = list(values)
    for p in values:
        if p in roll:
            roll.remove(p)
            picks.remove(p)
    return tuple(picks)

def roll_die() -> int:
    """Returns a value for a random roll of a six-sided die"""
    return random.randint(1, 6)

def roll_dice(count: int) -> tuple:
    """Returns a tuple containing the results of rolling <count> dice"""
    result = []
    for x in range(count):
        result.append(roll_die())
    return tuple(result)

def dice_frequency(roll: tuple) -> dict:
    """returns a dictionary with the number as the key and the frequency as the value"""
    counts = {}
    for n in range(1, 7):
        counts[n] = roll.count(n)
    return counts

def score_for_aces(roll: tuple) -> int:
    """returns score for the aces present in the roll"""
    return roll.count(1)

def score_for_twos(roll: tuple) -> int:
    """returns score for the twos present in the roll"""
    return roll.count(2) * 2

def score_for_threes(roll: tuple) -> int:
    """returns score for the threes present in the roll"""
    return roll.count(3) * 3

def score_for_fours(roll: tuple) -> int:
    """returns score for the fours present in the roll"""
    return roll.count(4) * 4

def score_for_fives(roll: tuple) -> int:
    """returns score for the fives present in the roll"""
    return roll.count(5) * 5

def score_for_sixes(roll: tuple) -> int:
    """returns score for the fives present in the roll"""
    return roll.count(6) * 6

def score_for_three_of_a_kind(roll: tuple) -> int:
    """returns total of dice if three or more of a kind are present, zero if not"""
    for n in dice_frequency(roll).values():
        if n >= 3:
            return sum(roll)
    return 0

def score_for_four_of_a_kind(roll: tuple) -> int:
    """returns total of dice if four or more of a kind are present, zero if not"""
    for n in dice_frequency(roll).values():
        if n >= 4:
            return sum(roll)
    return 0


def score_for_full_house(roll: tuple) -> int:
    """returns 25 if a full house is present, 0 if not"""
    counts = dice_frequency(roll)
    counts_list = list(counts.values())
    if 3 in counts_list and 2 in counts_list:
        return 25
    else:
        return 0

def score_for_small_straight(roll: tuple) -> int:
    """returns 30 if small straight is present, 0 if not"""
    roll_set = set(roll)
    if {1, 2, 3, 4}.issubset(roll_set):
        return 30
    if {2, 3, 4, 5}.issubset(roll_set):
        return 30
    if {3, 4, 5, 6}.issubset(roll_set):
        return 30
    return 0

def score_for_large_straight(roll: tuple) -> int:
    """returns 40 if large straight is present, 0 if not"""
    roll_set = set(roll)
    if {1, 2, 3, 4, 5}.issubset(roll_set):
        return 40
    if {2, 3, 4, 5, 6}.issubset(roll_set):
        return 40
    return 0

def score_for_chance(roll: tuple) -> int:
    """returns the sum of the dice roll"""
    return sum(roll)

def score_for_yahtzee(roll: tuple) -> int:
    """returns 50 if all dice are same number, 0 if not"""
    if len(set(roll)) == 1:
        return 50
    return 0

def score_for_category(category: str, roll: tuple) -> int:
    """uses the functions above to return the correct score for the given category using the given roll."""
    if category == 'Aces':
        return score_for_aces(roll)
    elif category == 'Twos':
        return score_for_twos(roll)
    elif category == 'Threes':
        return score_for_threes(roll)
    elif category == 'Fours':
        return score_for_fours(roll)
    elif category == 'Fives':
        return score_for_fives(roll)
    elif category == 'Sixes':
        return score_for_sixes(roll)
    elif category == 'Three of a Kind':
        return score_for_three_of_a_kind(roll)
    elif category == 'Four of a Kind':
        return score_for_four_of_a_kind(roll)
    elif category == 'Full House':
        return score_for_full_house(roll)
    elif category == 'Small Straight':
        return score_for_small_straight(roll)
    elif category == 'Large Straight':
        return score_for_large_straight(roll)
    elif category == 'Chance':
        return score_for_chance(roll)
    elif category == 'Yahtzee':
        return score_for_yahtzee(roll)
    else:
        return 0

def count_of_remaining_dice(group: tuple, keepers: tuple) -> int:
    """Returns the number of dice remaining after removing <keepers> from <group>. NOTE: ANY KEEPERS NOT IN THE GROUP ARE IGNORED."""
    return len(group) - len(keepers)

def display_scorecard(player:dict, categories:list=keys_in_order):
    """Given a player dictionary, fish out the scorecard and print the contents to the screen in a pleasing manner consistent with the real life scorecard"""
    players_name = player['name']
    scorecard = player['scorecard']
    header = f" Scorecard for {players_name} "
    print('')
    print(f"{header:*^30}")
    for i in categories:
        print(f'{i:<23} {player["scorecard"][i]:>3}')
    print('')
    
#def display_scorecard(player: dict, categories: list):
#    """Given a player dictionary, fish out the scorecard and print the contents to the screen in a pleasing manner consistent with the real life scorecard"""
#    print(f'{player["name"]}''s Scorecard')
#    for i in categories:
#        print(f'{i:<20} {player["scorecard"][i]:>4}')  

def display_final_scorecard(player: dict, categories: list):
    """Given a player dictionary, fish out the scorecard and print the contents to the screen in a pleasing manner consistent with the real life scorecard.  This function should also calculate the final score, including the use of the bonuses and fields not used during game play."""
    top_scores = 0
    lower_total = 0
    grand_total = 0
    display_scorecard(player, keys_in_order)
    for key, value in player["scorecard"].items():
        if key == 'Aces' or key == 'Twos' or key == 'Threes' or key == 'Fours' or key == 'Fives' or key == 'Sixes':
            top_scores = top_scores + value
        elif key == 'Bonus':
            yahtzee_bonus = value
        else:
            lower_total = lower_total + value
    if top_scores >= 63:
        top_total = top_scores + 35
        print(f'Top Section Total = {top_scores}')
        print(f'Top Section Bonus = 35')
    else:
        top_total = top_scores
        print(f'Top Section Total = {top_total}')
    print(f'Lower Section Total = {lower_total}')
    print(f'Yahtzee Bonus Score = {yahtzee_bonus}')
    grand_total = top_total + lower_total + yahtzee_bonus
    print(f'Grand Total Score = {grand_total}\n')
    return grand_total