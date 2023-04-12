import random

MAX_PLAYERS = 4
MIN_DIFF = 100

# dicionário de jogadores com seus respectivos pesos
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
