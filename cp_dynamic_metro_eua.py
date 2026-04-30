# -*- coding: utf-8 -*-
"""CP-DYNAMIC-METRO-EUA — San Francisco (BART)

Checkpoint 2 — Dynamic Programming — FIAP
"""

import time
import tracemalloc
import functools
import math

# =====================================
# GRAFO BART (SAN FRANCISCO)
# Grafo nao-dirigido (bidirecional): cada conexao e representada
# nos dois sentidos, pois os trens circulam em ambas as direcoes.
# Pesos = tempo base em minutos. Custo efetivo depende do horario.
# =====================================

grafo = {

    # =====================
    # LINHA AZUL (Dublin -> Daly City)
    # =====================
    "Dublin/Pleasanton": [
        {"destino": "West Dublin", "linha": "azul", "tempo": 5}
    ],
    "West Dublin": [
        {"destino": "Dublin/Pleasanton", "linha": "azul", "tempo": 5},
        {"destino": "Castro Valley", "linha": "azul", "tempo": 4}
    ],
    "Castro Valley": [
        {"destino": "West Dublin", "linha": "azul", "tempo": 4},
        {"destino": "Bay Fair", "linha": "azul", "tempo": 6}
    ],

    # =====================
    # INTERSECAO (HUB Bay Fair)
    # =====================
    "Bay Fair": [
        {"destino": "Castro Valley", "linha": "azul", "tempo": 6},
        {"destino": "San Leandro", "linha": "azul", "tempo": 4},
        {"destino": "Coliseum", "linha": "amarela", "tempo": 6},
        {"destino": "MacArthur", "linha": "amarela", "tempo": 8}
    ],

    # =====================
    # LINHA AMARELA
    # =====================
    "Pittsburg/Bay Point": [
        {"destino": "Walnut Creek", "linha": "amarela", "tempo": 8}
    ],
    "Walnut Creek": [
        {"destino": "Pittsburg/Bay Point", "linha": "amarela", "tempo": 8},
        {"destino": "MacArthur", "linha": "amarela", "tempo": 10}
    ],
    "MacArthur": [
        {"destino": "Walnut Creek", "linha": "amarela", "tempo": 10},
        {"destino": "19th St Oakland", "linha": "amarela", "tempo": 3},
        {"destino": "Bay Fair", "linha": "amarela", "tempo": 8}
    ],

    # =====================
    # LINHA VERDE
    # =====================
    "Berryessa": [
        {"destino": "Fremont", "linha": "verde", "tempo": 10}
    ],
    "Fremont": [
        {"destino": "Berryessa", "linha": "verde", "tempo": 10},
        {"destino": "Coliseum", "linha": "verde", "tempo": 12}
    ],

    # =====================
    # TRECHO CENTRAL
    # =====================
    "San Leandro": [
        {"destino": "Bay Fair", "linha": "azul", "tempo": 4},
        {"destino": "Coliseum", "linha": "azul", "tempo": 4}
    ],
    "Coliseum": [
        {"destino": "San Leandro", "linha": "azul", "tempo": 4},
        {"destino": "Fruitvale", "linha": "azul", "tempo": 3},
        {"destino": "Fremont", "linha": "verde", "tempo": 12},
        {"destino": "Bay Fair", "linha": "amarela", "tempo": 6}
    ],
    "Fruitvale": [
        {"destino": "Coliseum", "linha": "azul", "tempo": 3},
        {"destino": "Lake Merritt", "linha": "azul", "tempo": 4}
    ],
    "Lake Merritt": [
        {"destino": "Fruitvale", "linha": "azul", "tempo": 4},
        {"destino": "12th St Oakland", "linha": "azul", "tempo": 3}
    ],
    "12th St Oakland": [
        {"destino": "Lake Merritt", "linha": "azul", "tempo": 3},
        {"destino": "19th St Oakland", "linha": "azul", "tempo": 2}
    ],
    "19th St Oakland": [
        {"destino": "12th St Oakland", "linha": "azul", "tempo": 2},
        {"destino": "MacArthur", "linha": "amarela", "tempo": 3},
        {"destino": "West Oakland", "linha": "azul", "tempo": 6}
    ],
    "West Oakland": [
        {"destino": "19th St Oakland", "linha": "azul", "tempo": 6},
        {"destino": "Embarcadero", "linha": "azul", "tempo": 7}
    ],

    # =====================
    # SAN FRANCISCO
    # =====================
    "Embarcadero": [
        {"destino": "West Oakland", "linha": "azul", "tempo": 7},
        {"destino": "Montgomery", "linha": "azul", "tempo": 2}
    ],
    "Montgomery": [
        {"destino": "Embarcadero", "linha": "azul", "tempo": 2},
        {"destino": "Powell", "linha": "azul", "tempo": 2}
    ],
    "Powell": [
        {"destino": "Montgomery", "linha": "azul", "tempo": 2},
        {"destino": "Civic Center", "linha": "azul", "tempo": 2}
    ],
    "Civic Center": [
        {"destino": "Powell", "linha": "azul", "tempo": 2},
        {"destino": "16th St Mission", "linha": "azul", "tempo": 3}
    ],
    "16th St Mission": [
        {"destino": "Civic Center", "linha": "azul", "tempo": 3},
        {"destino": "24th St Mission", "linha": "azul", "tempo": 3}
    ],
    "24th St Mission": [
        {"destino": "16th St Mission", "linha": "azul", "tempo": 3},
        {"destino": "Daly City", "linha": "azul", "tempo": 6}
    ],
    "Daly City": [
        {"destino": "24th St Mission", "linha": "azul", "tempo": 6}
    ]
}

# =====================================
# CONFIGURACOES
# =====================================

PENALIDADE_TROCA = 4  # minutos para trocar de linha (plataforma, escadas)

def fator_horario(hora):
    if 5 <= hora < 7:
        return 0.6    # bonus: metro vazio
    elif 7 <= hora < 9:
        return 1.5    # pico manha
    elif 9 <= hora < 17:
        return 1.0    # horario normal
    elif 17 <= hora < 20:
        return 2.0    # pico tarde (maior penalidade)
    else:
        return 1.2    # noturno

# =====================================
# MENOR CAMINHO (COM MEMORIZACAO)
# =====================================

@functools.lru_cache(maxsize=None)
def menor_custo_com_memo(origem, destino, hora, linha_atual=None, visitados=frozenset()):
    if origem == destino:
        return (0, [origem])

    melhor = (float('inf'), [])

    for aresta in grafo.get(origem, []):
        vizinho = aresta["destino"]
        linha = aresta["linha"]
        tempo = aresta["tempo"]

        if vizinho in visitados:
            continue

        custo_extra = tempo * fator_horario(hora)

        if linha_atual is not None and linha != linha_atual:
            custo_extra += PENALIDADE_TROCA

        custo_rec, caminho = menor_custo_com_memo(
            vizinho, destino, hora, linha, visitados | {origem}
        )

        if custo_rec == float('inf'):
            continue

        custo_total = custo_extra + custo_rec

        if custo_total < melhor[0]:
            melhor = (custo_total, [origem] + caminho)

    return melhor

# =====================================
# MENOR CAMINHO (SEM MEMORIZACAO)
# =====================================

def menor_custo_sem_memo(origem, destino, hora, linha_atual=None, visitados=frozenset()):
    if origem == destino:
        return (0, [origem])

    melhor = (float('inf'), [])

    for aresta in grafo.get(origem, []):
        vizinho = aresta["destino"]
        linha = aresta["linha"]
        tempo = aresta["tempo"]

        if vizinho in visitados:
            continue

        custo_extra = tempo * fator_horario(hora)

        if linha_atual is not None and linha != linha_atual:
            custo_extra += PENALIDADE_TROCA

        custo_rec, caminho = menor_custo_sem_memo(
            vizinho, destino, hora, linha, visitados | {origem}
        )

        if custo_rec == float('inf'):
            continue

        custo_total = custo_extra + custo_rec

        if custo_total < melhor[0]:
            melhor = (custo_total, [origem] + caminho)

    return melhor

# =====================================
# MAIOR CAMINHO (backtracking, sem ciclos)
# =====================================

def maior_caminho(origem, destino, hora, linha_atual=None, visitados=None):
    if visitados is None:
        visitados = set()

    if origem == destino:
        return (0, [origem])

    maior = (float('-inf'), [])

    for aresta in grafo.get(origem, []):
        vizinho = aresta["destino"]
        linha = aresta["linha"]
        tempo = aresta["tempo"]

        if vizinho in visitados:
            continue

        custo_extra = tempo * fator_horario(hora)

        if linha_atual is not None and linha != linha_atual:
            custo_extra += PENALIDADE_TROCA

        custo_rec, caminho = maior_caminho(
            vizinho, destino, hora, linha, visitados | {origem}
        )

        if custo_rec == float('-inf'):
            continue

        custo_total = custo_extra + custo_rec

        if custo_total > maior[0]:
            maior = (custo_total, [origem] + caminho)

    return maior

# =====================================
# FORMATADOR
# =====================================

def formatar_tempo(minutos):
    if math.isinf(minutos):
        return "Sem caminho"
    minutos = int(minutos)
    h = minutos // 60
    m = minutos % 60
    return f"{h}h {m}min" if h > 0 else f"{m} min"

# =====================================
# EXECUCAO
# =====================================

origem = "Dublin/Pleasanton"
destino = "Daly City"
hora = int(input("Digite a hora (0-23): "))

# Limpar cache antes de medir (evita contaminacao em Jupyter/Colab)
menor_custo_com_memo.cache_clear()

tracemalloc.start()

# COM MEMO
t0 = time.perf_counter()
custo_min_memo, caminho_min_memo = menor_custo_com_memo(origem, destino, hora)
t1 = time.perf_counter()

# SEM MEMO
t2 = time.perf_counter()
custo_min_sem_memo, caminho_min_sem_memo = menor_custo_sem_memo(origem, destino, hora)
t3 = time.perf_counter()

mem = tracemalloc.get_traced_memory()
tracemalloc.stop()

# MAIOR CAMINHO
custo_max, caminho_max = maior_caminho(origem, destino, hora)

# =====================================
# RESULTADOS
# =====================================

print("=== MENOR CAMINHO (COM MEMO) ===")
print(" -> ".join(caminho_min_memo))
print("Tempo:", formatar_tempo(custo_min_memo))

print("\n=== MENOR CAMINHO (SEM MEMO) ===")
print(" -> ".join(caminho_min_sem_memo))
print("Tempo:", formatar_tempo(custo_min_sem_memo))

print("\n=== MAIOR CAMINHO ===")
print(" -> ".join(caminho_max))
print("Tempo:", formatar_tempo(custo_max))

print("\n=== DESEMPENHO ===")
print(f"Com memo:  {(t1-t0)*1000:.3f} ms")
print(f"Sem memo:  {(t3-t2)*1000:.3f} ms")
print(f"Memoria:   {mem[1] / 1024:.2f} KB")

# =====================================
# MAPA FOLIUM
# =====================================

coords = {
    "Dublin/Pleasanton": (37.7017, -121.8992),
    "West Dublin": (37.6997, -121.9281),
    "Castro Valley": (37.6907, -122.0758),
    "Bay Fair": (37.6969, -122.1269),
    "San Leandro": (37.7219, -122.1608),
    "Coliseum": (37.7540, -122.1970),
    "Fruitvale": (37.7748, -122.2241),
    "Lake Merritt": (37.7970, -122.2650),
    "12th St Oakland": (37.8037, -122.2715),
    "19th St Oakland": (37.8079, -122.2680),
    "MacArthur": (37.8291, -122.2672),
    "West Oakland": (37.8048, -122.2940),
    "Embarcadero": (37.7929, -122.3971),
    "Montgomery": (37.7894, -122.4014),
    "Powell": (37.7840, -122.4075),
    "Civic Center": (37.7795, -122.4142),
    "16th St Mission": (37.7650, -122.4195),
    "24th St Mission": (37.7525, -122.4185),
    "Daly City": (37.7061, -122.4691),
    "Fremont": (37.5575, -121.9766),
    "Berryessa": (37.3688, -121.8747),
    "Walnut Creek": (37.9057, -122.0672),
    "Pittsburg/Bay Point": (38.0189, -121.9440)
}

import folium

lat_media = sum([c[0] for c in coords.values()]) / len(coords)
lon_media = sum([c[1] for c in coords.values()]) / len(coords)

mapa = folium.Map(location=[lat_media, lon_media], zoom_start=10, tiles="CartoDB positron")

for estacao, (lat, lon) in coords.items():
    cor = "green" if estacao == origem else ("red" if estacao == destino else "blue")
    folium.Marker([lat, lon], popup=estacao, icon=folium.Icon(color=cor)).add_to(mapa)

arestas_desenhadas = set()
for orig in grafo:
    for aresta in grafo[orig]:
        dest = aresta["destino"]
        chave = tuple(sorted((orig, dest)))
        if chave in arestas_desenhadas:
            continue
        arestas_desenhadas.add(chave)
        if orig in coords and dest in coords:
            folium.PolyLine([coords[orig], coords[dest]], color="gray", weight=2, opacity=0.4).add_to(mapa)

folium.PolyLine([coords[e] for e in caminho_min_memo if e in coords], color="green", weight=8, opacity=0.8).add_to(mapa)
folium.PolyLine([coords[e] for e in caminho_max if e in coords], color="red", weight=4, opacity=0.9).add_to(mapa)

mapa.save("mapa_bart.html")
print("Mapa salvo como mapa_bart.html")
