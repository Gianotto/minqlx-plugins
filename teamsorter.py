import sys, requests
from itertools import combinations

MAX_PLAYERS = 4
VARIANCE_ACCEPTED = 5
STEAM_KEY = '' # get one at https://steamcommunity.com/dev
STEAM_API_LINK = 'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={}'.format(STEAM_KEY)
STEAM_API_UID = STEAM_API_LINK + '&steamids={}'
NAME = 0
ELO = 1

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

sid_players = { 
                '76561197985502667' : ['x', 1],
                '76561198026118540' : ['x', 1],
                '76561199041428969' : ['x', 1],
                '76561198340444680' : ['x', 1],
                '76561197971071169' : ['x', 1],
                '76561197961495830' : ['x', 1],
                '76561198257497456' : ['x', 1],
                '76561198052156695' : ['x', 1],
                '76561197979265380' : ['x', 1],
                '76561198035810278' : ['x', 1],
                '76561198044624809' : ['x', 1],
                '76561198001099451' : ['x', 1]}#,
                #'7' : ['x', 1],
                #'7' : ['x', 1],
                #'7' : ['x', 1],
                #'7' : ['x', 1],}


def unique_group(iterable, k, n, groups=0):
    if groups == k:
        yield []
    pool = set(iterable)
    for combination in combinations(pool, n):
        for rest in unique_group(pool.difference(combination), k, n, groups + 1):
            yield [combination, *rest]

def variance(groups, plist):
    total_skills = [sum(plist[player][ELO] for player in group) for group in groups]
    return max(total_skills) - min(total_skills)

def team_avg(team, plist):
    return sum([plist[player][ELO] for player in team]) / len(team)

def balance(player_list, num_players_team):
    last_best = 100000000000
    i = 0
    for grouping in unique_group(player_list, len(player_list)/num_players_team, num_players_team):
        i += 1
        if i % 10000 == 0:
            sys.stdout.write('.')
            sys.stdout.flush()
        if variance(grouping, player_list) < last_best:
            last_best = variance(grouping, player_list)
            print("")
            print(f"Variance: {last_best}")
            print("============")
            #print(grouping)
            
            for i, time in enumerate(grouping):
                print("Time {}: (Elo: {}). {}".format(i+1, team_avg(time, player_list), [player_list[player][NAME] for player in time]))
        if last_best <= VARIANCE_ACCEPTED:
            print("Found best result.")
            break

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

def getSteamProfile(uid):
    url = STEAM_API_UID.format(uid)
    res = requests.get(url)
    if res.status_code != requests.codes.ok:
        return 0
    js = res.json()
    return(js['response']['players'][0]['personaname'])
             
#search for players elos based on steamid
#build player list
for sid in sid_players:
    sid_players[sid].pop(ELO)
    sid_players[sid].insert(ELO, fetch_elo(sid))
    sid_players[sid].pop(NAME)
    sid_players[sid].insert(NAME, getSteamProfile(sid))
    print("Player: {} ({}) : {}".format(sid_players[sid][NAME], sid, sid_players[sid][ELO]))


balance(sid_players, MAX_PLAYERS)