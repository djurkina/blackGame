import random

def roll_dice(num_dice=2, min_value=1, max_value=6):
    if not 1 <= num_dice <= 5:
        raise ValueError("the dice must be from 1 to 5.")
    if min_value > max_value:
        raise ValueError("invalid value range.")

    results = [random.randint(min_value, max_value) for _ in range(num_dice)]
    total = sum(results)
    return results, total
