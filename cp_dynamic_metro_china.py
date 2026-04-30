# -*- coding: utf-8 -*-
"""CP-DYNAMIC-METRO-CHINA — Beijing (Metro)

Checkpoint 2 — Dynamic Programming — FIAP
"""

import time
import tracemalloc
import functools
import math

# =====================================
# GRAFO BEIJING
# Grafo nao-dirigido (bidirecional): trens operam nos dois sentidos.
# Pesos = tempo base em minutos. Custo efetivo depende do horario.
# =====================================

grafo = {

    # =====================
    # LINHA 1
    # =====================
    "Sihui East": [
        {"destino": "Sihui", "linha": 1, "tempo": 2},
        {"destino": "Shuangjing", "linha": 1, "tempo": 3}
    ],
    "Sihui": [
        {"destino": "Sihui East", "linha": 1, "tempo": 2},
        {"destino": "Guomao", "linha": 1, "tempo": 3}
    ],
    "Guomao": [
        {"destino": "Sihui", "linha": 1, "tempo": 3},
        {"destino": "Yonganli", "linha": 1, "tempo": 2},
        {"destino": "Jiaomenxi", "linha": 10, "tempo": 5}
    ],
    "Yonganli": [
        {"destino": "Guomao", "linha": 1, "tempo": 2},
        {"destino": "Jianguomen", "linha": 1, "tempo": 2}
    ],
    "Jianguomen": [
        {"destino": "Yonganli", "linha": 1, "tempo": 2},
        {"destino": "Dongdan", "linha": 1, "tempo": 2},
        {"destino": "Fuxingmen", "linha": 2, "tempo": 5}
    ],
    "Dongdan": [
        {"destino": "Jianguomen", "linha": 1, "tempo": 2},
        {"destino": "Wangfujing", "linha": 1, "tempo": 2}
    ],
    "Wangfujing": [
        {"destino": "Dongdan", "linha": 1, "tempo": 2},
        {"destino": "Tiananmen East", "linha": 1, "tempo": 2}
    ],
    "Tiananmen East": [
        {"destino": "Wangfujing", "linha": 1, "tempo": 2},
        {"destino": "Tiananmen West", "linha": 1, "tempo": 2}
    ],
    "Tiananmen West": [
        {"destino": "Tiananmen East", "linha": 1, "tempo": 2},
        {"destino": "Xidan", "linha": 1, "tempo": 2}
    ],
    "Xidan": [
        {"destino": "Tiananmen West", "linha": 1, "tempo": 2},
        {"destino": "Fuxingmen", "linha": 1, "tempo": 2},
        {"destino": "Xuanwumen", "linha": 4, "tempo": 2}
    ],
    "Fuxingmen": [
        {"destino": "Xidan", "linha": 1, "tempo": 2},
        {"destino": "Xizhimen", "linha": 2, "tempo": 4}
    ],
    "Guangqumen": [
        {"destino": "Shuangjing", "linha": 1, "tempo": 2}
    ],
    "Shuangjing": [
        {"destino": "Guangqumen", "linha": 1, "tempo": 2},
        {"destino": "Sihui East", "linha": 1, "tempo": 3}
    ],

    # =====================
    # LINHA 2
    # =====================
    "Xizhimen": [
        {"destino": "Fuxingmen", "linha": 2, "tempo": 4},
        {"destino": "Xuanwumen", "linha": 2, "tempo": 5}
    ],

    # =====================
    # LINHA 4
    # =====================
    "Xuanwumen": [
        {"destino": "Xidan", "linha": 4, "tempo": 2},
        {"destino": "Caishikou", "linha": 4, "tempo": 2},
        {"destino": "Xizhimen", "linha": 2, "tempo": 5}
    ],
    "Caishikou": [
        {"destino": "Xuanwumen", "linha": 4, "tempo": 2},
        {"destino": "Taoranting", "linha": 4, "tempo": 3}
    ],
    "Taoranting": [
        {"destino": "Caishikou", "linha": 4, "tempo": 3},
        {"destino": "Jiaomenxi", "linha": 4, "tempo": 4}
    ],
    "Jiaomenxi": [
        {"destino": "Taoranting", "linha": 4, "tempo": 4},
        {"destino": "Guomao", "linha": 10, "tempo": 5}
    ],

    # =====================
    # LINHA 10
    # =====================
    "Haidian Huangzhuang": [
        {"destino": "Beitucheng", "linha": 10, "tempo": 4},
        {"destino": "Guomao", "linha": 10, "tempo": 6}
    ],
    "Beitucheng": [
        {"destino": "Haidian Huangzhuang", "linha": 10, "tempo": 4},
        {"destino": "Xizhimen", "linha": 10, "tempo": 5}
    ]
}

# =====================================
# CONFIGURACOES
# =====================================

PENALIDADE_TROCA = 4  # minutos para trocar de linha

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
# CORRECAO: adicionado parametro hora para aplicar fator de horario
# de forma consistente com as outras cidades.
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

        custo_extra = tempo * fator_horario(hora)  # CORRIGIDO: aplica fator de horario

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

origem = "Sihui East"
destino = "Xizhimen"
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
print(" -> ".join(str(e) for e in caminho_min_memo))
print("Tempo:", formatar_tempo(custo_min_memo))

print("\n=== MENOR CAMINHO (SEM MEMO) ===")
print(" -> ".join(str(e) for e in caminho_min_sem_memo))
print("Tempo:", formatar_tempo(custo_min_sem_memo))

print("\n=== MAIOR CAMINHO ===")
print(" -> ".join(str(e) for e in caminho_max))
print("Tempo:", formatar_tempo(custo_max))

print("\n=== DESEMPENHO ===")
print(f"Com memo:  {(t1-t0)*1000:.3f} ms")
print(f"Sem memo:  {(t3-t2)*1000:.3f} ms")
print(f"Memoria:   {mem[1] / 1024:.2f} KB")

# =====================================
# MAPA FOLIUM
# =====================================

coords = {
    "Sihui East": (39.908, 116.655),
    "Sihui": (39.907, 116.645),
    "Guomao": (39.914, 116.460),
    "Yonganli": (39.914, 116.450),
    "Jianguomen": (39.914, 116.435),
    "Dongdan": (39.914, 116.420),
    "Wangfujing": (39.915, 116.410),
    "Tiananmen East": (39.914, 116.403),
    "Tiananmen West": (39.914, 116.395),
    "Xidan": (39.913, 116.375),
    "Fuxingmen": (39.913, 116.350),
    "Xuanwumen": (39.907, 116.375),
    "Caishikou": (39.900, 116.375),
    "Taoranting": (39.890, 116.380),
    "Jiaomenxi": (39.860, 116.400),
    "Xizhimen": (39.940, 116.350),
    "Guangqumen": (39.905, 116.470),
    "Shuangjing": (39.906, 116.470),
    "Haidian Huangzhuang": (39.980, 116.310),
    "Beitucheng": (39.970, 116.340)
}

import folium

mapa = folium.Map(location=[39.91, 116.40], zoom_start=12, tiles="CartoDB positron")

for estacao, (lat, lon) in coords.items():
    cor = "green" if estacao == origem else ("red" if estacao == destino else "blue")
    folium.Marker([lat, lon], popup=estacao, icon=folium.Icon(color=cor)).add_to(mapa)

arestas_desenhadas = set()
for orig in grafo:
    for aresta in grafo[orig]:
        dest = aresta["destino"]
        chave = tuple(sorted([orig, dest]))
        if chave in arestas_desenhadas:
            continue
        arestas_desenhadas.add(chave)
        if orig in coords and dest in coords:
            folium.PolyLine([coords[orig], coords[dest]], color="gray", weight=2, opacity=0.5).add_to(mapa)

folium.PolyLine([coords[e] for e in caminho_min_memo if e in coords], color="green", weight=10, opacity=0.8).add_to(mapa)
folium.PolyLine([coords[e] for e in caminho_max if e in coords], color="red", weight=3, opacity=1.0).add_to(mapa)

mapa.save("mapa_beijing.html")
print("Mapa salvo como mapa_beijing.html")
