import random

n = 100
count_map = {"A": 0, "B": 0, "C": 0}


def get_random_choices():
    choices_with_weights = [("A", 0.75), ("B", 0.15), ("C", 0.1)]
    choices, weights = zip(*choices_with_weights)
    choice = random.choices(choices, weights=weights, k=1)[0]
    return choice


for i in range(n):
    count_map[get_random_choices()] += 1

for key, val in count_map.items():
    count_map[key] = round((val / n) * 100, 2)
print(count_map)