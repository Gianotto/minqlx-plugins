import sys, requests
from valve.steam.id import SteamID
from itertools import combinations

MAX_PLAYERS = 4
VARIANCE_ACCEPTED = 20

# dicionário de jogadores com seus respectivos Elos
players = {"sn00per": 734,
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

sid_list = {'76561198026118540' : 0,
            '76561198043250656' : 0,
            '76561198340444680' : 0,
            '76561197971071169' : 0,
            '76561197961495830' : 0,
            '76561198052156695' : 0,
            '76561198257497456' : 0,
            '76561198001099451' : 0}

def unique_group(iterable, k, n, groups=0):
    if groups == k:
        yield []
    pool = set(iterable)
    for combination in combinations(pool, n):
        for rest in unique_group(pool.difference(combination), k, n, groups + 1):
            yield [combination, *rest]

def variance(groups, plist):
    total_skills = [sum(plist[player] for player in group) for group in groups]
    return max(total_skills) - min(total_skills)

def team_avg(team, plist):
    return sum([plist[player] for player in team]) / len(team)

#return elo, sames stats
def fetch_elo(sid):
    url = "https://qlstats.net/elo/{}".format(sid)
    res = requests.get(url)
    if res.status_code != requests.codes.ok:
        return 0
    js = res.json()

    for p in js['players']:
        _sid = int(p['steamid'])
        if 'ca' in p: return p['ca']['elo'] #, p['ca']['games']
        # If the gametype was not found
        else: return 0

def balance(player_list, num_players_team):
    last_best = 100000000000
    i = 0
    for grouping in unique_group(player_list, len(player_list)/num_players_team, num_players_team):
        i += 1
        if i % 100000 == 0:
            sys.stdout.write('.')
            sys.stdout.flush()
        if variance(grouping, player_list) < last_best:
            last_best = variance(grouping, player_list)
            print("")
            print(f"Variance: {variance(grouping, player_list)}")
            print("============")
            #print(grouping)
            
            for i, time in enumerate(grouping):
                print("Time {}: (Elo: {}). {}".format(i+1, team_avg(time, player_list), time))
        if last_best <= VARIANCE_ACCEPTED:
            print("Found best result.")
            break

#search for players elos based on steamid
#build player list
for sid in sid_list:
    elo = fetch_elo(sid)
    print("Steam ID: {} Elo: {}".format(sid, elo))
    #print(SteamID(sid))
    sid_list[sid] = elo

print([sid_list])

balance(sid_list, MAX_PLAYERS)

