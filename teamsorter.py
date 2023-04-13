import sys, requests, time, random
from itertools import combinations

MAX_PLAYERS = 5
NUM_TEAMS = 7
VARIANCE_ACCEPTED = 20
RUNNING_TIME = 1*60
QLSTATS_URL = 'https://qlstats.net/elo/{}'
STEAM_KEY = '' # get one at https://steamcommunity.com/dev
STEAM_API_LINK = 'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={}'.format(STEAM_KEY)
STEAM_API_UID = STEAM_API_LINK + '&steamids={}'
NAME_KEY = 0
ELO_KEY = 1

sid_players = { 
                '76561197993190504' : ['x', 1],
                '76561198003765572' : ['x', 1],
                '76561198154996520' : ['x', 1],
                '76561198315999232' : ['x', 1],
                '76561198383687171' : ['x', 1],
                '76561198075370176' : ['x', 1],
                '76561198026118540' : ['x', 1],
                '76561197985502667' : ['x', 1],
                '76561198054894320' : ['x', 1],
                '76561198350007415' : ['x', 1],
                '76561198020698841' : ['x', 1],
                '76561198120362672' : ['x', 1],
                '76561198017151203' : ['x', 1],
                '76561198221203272' : ['x', 1],
                '76561198198545569' : ['x', 1],
                '76561199409120459' : ['x', 1],
                '76561198052156695' : ['x', 1],
                '76561197979265380' : ['x', 1],
                '76561198257497456' : ['x', 1],
                '76561198035810278' : ['x', 1],
                '76561198044624809' : ['x', 1],
                '76561198001099451' : ['x', 1],
                '76561198242559062' : ['x', 1],
                '76561198048262475' : ['x', 1],
                '76561198044013818' : ['x', 1],
                '76561198118398346' : ['x', 1],
                '76561197987529787' : ['x', 1],
                '76561199041428969' : ['x', 1],
                '76561198340444680' : ['x', 1],
                '76561197971071169' : ['x', 1],
                '76561197961495830' : ['x', 1],
                '76561198209854275' : ['x', 1],
                '76561198154953404' : ['x', 1],
                '76561198405178407' : ['x', 1],
                '76561198075370176' : ['x', 1],
                '76561198108655845' : ['x', 1]}

# find combinations with the list, teams and players
def unique_group(iterable, k, n, groups=0):
    if groups == k:
        yield []
    pool = set(iterable)
    for combination in combinations(pool, n):
        for rest in unique_group(pool.difference(combination), k, n, groups + 1):
            yield [combination, *rest]

# calculate elo variance between team members
def variance(groups, plist):
    total_skills = [sum(plist[player][ELO_KEY] for player in group) for group in groups]
    return max(total_skills) - min(total_skills)

def team_avg(team, plist):
    return sum([plist[player][ELO_KEY] for player in team]) / len(team)

def balance(player_list, num_players_team, num_teams):
    if len(player_list) % NUM_TEAMS != 0:
        print("Found {} players in list.\nNumber of players {} per team must match exact distribution to the amount of desired of {} teams.".format(len(player_list), MAX_PLAYERS, NUM_TEAMS))
        #return
    
    # search for players elos based on steamid
    # build player list
    print("Found total of {} players.".format(len(player_list)))
    print("Gathering ELO from QLStats.net...")
    for sid in player_list:
        player_list[sid].pop(ELO_KEY)
        player_list[sid].insert(ELO_KEY, fetch_elo(sid))
        player_list[sid].pop(NAME_KEY)
        player_list[sid].insert(NAME_KEY, getsteam_profile(sid))
        print("Player: {} ({}) : {}".format(player_list[sid][NAME_KEY], sid, player_list[sid][ELO_KEY]))

    print("Shuffling teams based on Elo stats...")
    initial_time = time.time()
    last_best = 100000000000
    i = 0
    r = 0
    for grouping in unique_group(player_list, num_teams, num_players_team):
        i += 1
        if i % 100000 == 0:
            sys.stdout.write('.')
            sys.stdout.flush()

        if time.time() - initial_time > RUNNING_TIME:
            sys.stdout.flush()
            sys.stdout.write(f"Reach maximum runnnning time. Ended with variance of {last_best}")
            break

        if variance(grouping, player_list) < last_best:
            r += 1
            last_best = variance(grouping, player_list)
            print("")
            print(f"Round #{r}.\nPlayers variance on same team: {last_best}")
            print("============")
            #print(grouping)
            
            team_avg_list = list()
            for i, team in enumerate(grouping):
                avg = team_avg(team, player_list)
                team_avg_list.append(avg)
                print("Time {}: (Elo: {:.0f}). {}".format(i+1, avg, [player_list[player][NAME_KEY] for player in team]))

            print("Teams variance {:.0f}.".format(sum(a for a in team_avg_list)/NUM_TEAMS))
            print("============")

        if last_best <= VARIANCE_ACCEPTED:
            print("Found best result.")
            break

# return elo, games stats
def fetch_elo(sid):
    url = QLSTATS_URL.format(sid)
    res = requests.get(url)
    if res.status_code != requests.codes.ok:
        return 0
    js = res.json()

    for p in js['players']:
        if 'ca' in p: return p['ca']['elo'] #, p['ca']['games']
        # If the gametype was not found
        else: return 0

# get Steam profile user nickname
def getsteam_profile(uid):
    url = STEAM_API_UID.format(uid)
    res = requests.get(url)
    if res.status_code != requests.codes.ok:
        return 0
    js = res.json()
    return(js['response']['players'][0]['personaname'])

# randomize dict
def randomKeys(dict_list):
    print("Randomizing player list...")
    keys = list(dict_list.keys())
    random.shuffle(keys)
    random_dict_list = {}
    for key in keys:
        random_dict_list[key] = dict_list[key]
    return random_dict_list

balance(randomKeys(sid_players), MAX_PLAYERS, NUM_TEAMS)