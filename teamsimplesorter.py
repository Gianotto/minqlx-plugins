import random

MAX_PLAYERS = 5

# dicionário de jogadores com seus respectivos pesos
jogadores = players = {
    "PaquiTao": 722,
    "sn00per": 716,
    "caYer4": 1004,
    "Chaka": 1090,
    "13m3": 823,
    "Fbz": 1281,
    "kasparov": 1256,
    "GordOfWar": 999,
    "3Ti-HyperX": 487,
    "trololo": 977,
    "ov3rk1ll^^": 1072,
    "Shark": 888,
    "L1m4o": 921,
    "^2MΘDΞSTI∆": 857,
    "MacetA": 847,
    "lipe": 1209,
    "^3chicken": 886,
    "mix": 1084,
    "helm": 863,
    "Railer": 917,
    "gyodai": 932,
    "Ugakill": 997,
    "Out_Brasil": 906,
    "nhd": 1345,
    "Decao": 889,
    "terz": 922,
    "d3k0666": 869,
    "NetM wanted": 1161,
    "PCPmineiro": 871,
    "BOT Coelho": 1073,
    "Sr. Miyagi": 1221,
    "bjkkk": 1264,
    "DoomRG": 911,
    ".": 1276,
    "SpectralWizard": 952
}


def team_avg(team):
    return sum([jogadores[jogador] for jogador in team]) / len(team)


# embaralha a lista de jogadores com base nos seus pesos
jogadores_ordenados = sorted(jogadores.items(), key=lambda x: x[1], reverse=True)
jogadores_embaralhados = [jogador[0] for jogador in jogadores_ordenados]
random.shuffle(jogadores_embaralhados)

# divide a lista de jogadores em times com 4 jogadores cada
times = [jogadores_embaralhados[i:i+MAX_PLAYERS] for i in range(0, len(jogadores_embaralhados), MAX_PLAYERS)]

# calcula o valor médio do peso de cada time
for time in times:
    media_peso = team_avg(time)
    time.append(media_peso)

# exibe os times formados, incluindo o valor médio do peso de cada time
for i, time in enumerate(times):
    print("Time {}: {}. Média de peso: {:.2f}".format(i+1, time[:-1], time[-1]))
