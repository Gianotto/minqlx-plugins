import sys
from itertools import combinations

last_best = 100000000000
MAX_PLAYERS = 4
VARIANCE_ACCEPTED = 20

# dicionário de jogadores com seus respectivos Elos
jogadores = {"sn00per": 734,
                "Luanzeyra": 1417,
                "Bobi Mauley": 1488,
                "razor": 1403,
                "rakz": 1315,
                "Fbz": 1286,
                "kasparov": 1219,
                "Muka": 1182,
                "Chaka": 1121,
                "Out_Brasil": 958,
                "DoomRG": 927,
                "PCPmineiro": 909,
                "Shark": 897,
                "13me": 784,
                "3Ti-HyperX": 503,
                "n00t!": 451}

def unique_group(iterable, k, n, groups=0):
    if groups == k:
        yield []
    pool = set(iterable)
    for combination in combinations(pool, n):
        for rest in unique_group(pool.difference(combination), k, n, groups + 1):
            yield [combination, *rest]

def variance(groups):
    total_skills = [sum(jogadores[player] for player in group) for group in groups]
    return max(total_skills) - min(total_skills)

def team_avg(team):
    return sum([jogadores[player] for player in team]) / len(team)

i = 0
for grouping in unique_group(jogadores, len(jogadores)/MAX_PLAYERS, 4):
    i += 1
    if i % 100000 == 0:
        sys.stdout.write('.')
        sys.stdout.flush()
    if variance(grouping) < last_best:
        last_best = variance(grouping)
        print("")
        print(f"Variance: {variance(grouping)}")
        print("============")
        #print(grouping)
        
        for i, time in enumerate(grouping):
            print("Time {}: {}. Elo: {}".format(i+1, time, team_avg(time)))
    if last_best <= VARIANCE_ACCEPTED:
        print("Found best result.")
        break