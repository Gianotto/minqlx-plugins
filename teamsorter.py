import random

NUM_JOGADORES = 4
MAX_DIFERENCA = 100

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


# função para calcular a diferença na média dos pesos dos times
def diferenca_media(times):
    pesos = [sum([jogadores[jogador] for jogador in time]) / len(time) for time in times]
    return max(pesos) - min(pesos)

# função para sortear os jogadores para um time
def sortear_time(jogadores_lista, media_peso, max_diferenca):
    time = []
    while len(time) < 4:
        jogador = random.choice(list(jogadores_lista.keys()))
        if (sum([jogadores_lista[jogador] for jogador in time]) + jogadores_lista[jogador]) / (len(time) + 1) <= media_peso + max_diferenca:
            time.append(jogador)
            del jogadores_lista[jogador]
        elif len(jogadores) == 1:
            time.append(list(jogadores.keys())[0])
            del jogadores_lista[jogador]
    return time

# embaralha a lista de jogadores com base nos seus pesos
jogadores_ordenados = sorted(jogadores.items(), key=lambda x: x[1], reverse=True)
jogadores_embaralhados = [jogador[0] for jogador in jogadores_ordenados]
random.shuffle(jogadores_embaralhados)

# divide a lista de jogadores em times com média de peso igual ou próxima
media_peso = sum(jogadores.values()) / 4
max_diferenca = 100
times = []
while len(jogadores_embaralhados) > 0:
    time = sortear_time(jogadores, media_peso, max_diferenca)
    times.append(time)
    media_peso = sum([jogadores[jogador] for jogador in time]) / (4 * len(times))
    while diferenca_media(times) > max_diferenca and len(times) > 1:
        time = times.pop()
        jogadores.update({jogador: jogadores[jogador] for jogador in time})
        media_peso = sum([jogadores[jogador] for jogador in time]) / (4 * len(times))
    if len(jogadores) == 0:
        break

# exibe os times formados, incluindo o valor médio do peso de cada time
for i, time in enumerate(times):
    jogadores_time = [jogador for jogador, peso in jogadores_ordenados if jogador in time]
    print("Time {}: {}. Média de peso: {:.2f}".format(i+1, jogadores_time, sum([jogadores[jogador] for jogador in time]) / len(time)))