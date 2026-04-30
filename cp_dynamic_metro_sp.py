# -*- coding: utf-8 -*-
"""CP-DYNAMIC-METRO-SP — São Paulo (Metrô + CPTM)

Checkpoint 2 — Dynamic Programming — FIAP
"""

import time
import tracemalloc
import functools
import math

grafo = {

  # =========================
  # LINHA 1 - AZUL
  # =========================
  "Tucuruvi":[
      {"destino":"Parada Inglesa","linha":"azul","tempo":2}
  ],
  "Parada Inglesa":[
      {"destino":"Tucuruvi","linha":"azul","tempo":2},
      {"destino":"Jardim Sao Paulo","linha":"azul","tempo":2}
  ],
  "Jardim Sao Paulo":[
      {"destino":"Parada Inglesa","linha":"azul","tempo":2},
      {"destino":"Santana","linha":"azul","tempo":2}
  ],
  "Santana":[
      {"destino":"Jardim Sao Paulo","linha":"azul","tempo":2},
      {"destino":"Carandiru","linha":"azul","tempo":2}
  ],
  "Carandiru":[
      {"destino":"Santana","linha":"azul","tempo":2},
      {"destino":"Portuguesa-Tiete","linha":"azul","tempo":2}
  ],
  "Portuguesa-Tiete":[
      {"destino":"Carandiru","linha":"azul","tempo":2},
      {"destino":"Armenia","linha":"azul","tempo":2}
  ],
  "Armenia":[
      {"destino":"Portuguesa-Tiete","linha":"azul","tempo":2},
      {"destino":"Tiradentes","linha":"azul","tempo":2}
  ],
  "Tiradentes":[
      {"destino":"Armenia","linha":"azul","tempo":2},
      {"destino":"Luz","linha":"azul","tempo":2}
  ],

  # =========================
  # HUB LUZ (AZUL + AMARELA)
  # =========================
  "Luz":[
      {"destino":"Tiradentes","linha":"azul","tempo":2},
      {"destino":"Sao Bento","linha":"azul","tempo":2},
      {"destino":"Republica","linha":"amarela","tempo":3}
  ],

  "Sao Bento":[
      {"destino":"Luz","linha":"azul","tempo":2},
      {"destino":"Se","linha":"azul","tempo":2}
  ],

  # =========================
  # HUB SE (AZUL)
  # =========================
  "Se":[
      {"destino":"Sao Bento","linha":"azul","tempo":2},
      {"destino":"Liberdade","linha":"azul","tempo":2}
  ],

  "Liberdade":[
      {"destino":"Se","linha":"azul","tempo":2},
      {"destino":"Sao Joaquim","linha":"azul","tempo":2}
  ],
  "Sao Joaquim":[
      {"destino":"Liberdade","linha":"azul","tempo":2},
      {"destino":"Vergueiro","linha":"azul","tempo":2}
  ],
  "Vergueiro":[
      {"destino":"Sao Joaquim","linha":"azul","tempo":2},
      {"destino":"Paraiso","linha":"azul","tempo":2}
  ],

  # =========================
  # HUB PARAISO (AZUL + VERDE)
  # =========================
  "Paraiso":[
      {"destino":"Vergueiro","linha":"azul","tempo":2},
      {"destino":"Ana Rosa","linha":"azul","tempo":2},
      {"destino":"Brigadeiro","linha":"verde","tempo":2}
  ],

  # =========================
  # HUB ANA ROSA (AZUL + VERDE)
  # =========================
  "Ana Rosa":[
      {"destino":"Paraiso","linha":"azul","tempo":2},
      {"destino":"Vila Mariana","linha":"azul","tempo":2},
      {"destino":"Chacara Klabin","linha":"verde","tempo":3}
  ],

  "Vila Mariana":[
      {"destino":"Ana Rosa","linha":"azul","tempo":2},
      {"destino":"Santa Cruz","linha":"azul","tempo":2}
  ],

  # =========================
  # HUB SANTA CRUZ (AZUL + LILAS)
  # =========================
  "Santa Cruz":[
      {"destino":"Vila Mariana","linha":"azul","tempo":2},
      {"destino":"Praca da Arvore","linha":"azul","tempo":2},
      {"destino":"Santo Amaro","linha":"lilas","tempo":8},
      {"destino":"Chacara Klabin","linha":"lilas","tempo":3}
  ],

  "Praca da Arvore":[
      {"destino":"Santa Cruz","linha":"azul","tempo":2},
      {"destino":"Saude","linha":"azul","tempo":2}
  ],
  "Saude":[
      {"destino":"Praca da Arvore","linha":"azul","tempo":2},
      {"destino":"Sao Judas","linha":"azul","tempo":2}
  ],
  "Sao Judas":[
      {"destino":"Saude","linha":"azul","tempo":2},
      {"destino":"Conceicao","linha":"azul","tempo":2}
  ],
  "Conceicao":[
      {"destino":"Sao Judas","linha":"azul","tempo":2},
      {"destino":"Jabaquara","linha":"azul","tempo":2}
  ],
  "Jabaquara":[
      {"destino":"Conceicao","linha":"azul","tempo":2}
  ],

  # =========================
  # LINHA 2 - VERDE
  # =========================
  "Brigadeiro":[
      {"destino":"Paraiso","linha":"verde","tempo":2},
      {"destino":"Trianon-Masp","linha":"verde","tempo":2}
  ],
  "Trianon-Masp":[
      {"destino":"Brigadeiro","linha":"verde","tempo":2},
      {"destino":"Consolacao","linha":"verde","tempo":2}
  ],
  "Consolacao":[
      {"destino":"Trianon-Masp","linha":"verde","tempo":2},
      {"destino":"Clinicas","linha":"verde","tempo":2}
  ],
  "Clinicas":[
      {"destino":"Consolacao","linha":"verde","tempo":2},
      {"destino":"Sumare","linha":"verde","tempo":2}
  ],
  "Sumare":[
      {"destino":"Clinicas","linha":"verde","tempo":2},
      {"destino":"Vila Madalena","linha":"verde","tempo":3}
  ],
  "Vila Madalena":[
      {"destino":"Sumare","linha":"verde","tempo":3}
  ],

  "Chacara Klabin":[
      {"destino":"Ana Rosa","linha":"verde","tempo":3},
      {"destino":"Santa Cruz","linha":"lilas","tempo":3}
  ],

  # =========================
  # LINHA 4 - AMARELA
  # =========================
  "Republica":[
      {"destino":"Luz","linha":"amarela","tempo":3},
      {"destino":"Paulista","linha":"amarela","tempo":3}
  ],
  "Paulista":[
      {"destino":"Republica","linha":"amarela","tempo":3},
      {"destino":"Pinheiros","linha":"amarela","tempo":5}
  ],
  "Pinheiros":[
      {"destino":"Paulista","linha":"amarela","tempo":5},
      {"destino":"Vila Sonia","linha":"amarela","tempo":5},
      {"destino":"Santo Amaro","linha":"esmeralda","tempo":10}
  ],
  "Vila Sonia":[
      {"destino":"Pinheiros","linha":"amarela","tempo":5}
  ],

  # =========================
  # LINHA 5 - LILAS
  # =========================
  "Santo Amaro":[
      {"destino":"Santa Cruz","linha":"lilas","tempo":8},
      {"destino":"Campo Limpo","linha":"lilas","tempo":5},
      {"destino":"Pinheiros","linha":"esmeralda","tempo":10}
  ],
  "Campo Limpo":[
      {"destino":"Santo Amaro","linha":"lilas","tempo":5},
      {"destino":"Capao Redondo","linha":"lilas","tempo":4}
  ],
  "Capao Redondo":[
      {"destino":"Campo Limpo","linha":"lilas","tempo":4}
  ]
}

# =====================================
# CONFIGURACOES
# =====================================

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

PESO_LINHA = {
    "azul": 1.0,
    "verde": 1.0,
    "amarela": 0.9,   # mais rapida (linha moderna)
    "lilas": 0.95,    # tambem eficiente
    "esmeralda": 1.2  # CPTM mais lenta
}

def penalidade_troca(linha_atual, nova_linha, estacao):
    """
    Penalidade por troca de linha.
    CORRECAO: nomes sem acento para bater com as chaves do grafo.
    Estacoes hub tem penalidade menor (2 min) pois possuem
    infraestrutura de integracao melhor que as demais (6 min).
    """
    if linha_atual is None or linha_atual == nova_linha:
        return 0

    # CORRIGIDO: nomes sem acento, identicos as chaves do grafo
    hubs = {"Se", "Luz", "Paraiso", "Pinheiros", "Santa Cruz"}

    if estacao in hubs:
        return 2
    else:
        return 6

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

        tempo_ajustado = tempo * PESO_LINHA.get(linha, 1.0)
        custo_extra = tempo_ajustado * fator_horario(hora)
        custo_extra += penalidade_troca(linha_atual, linha, origem)

        custo_rec, caminho = menor_custo_com_memo(
            vizinho,
            destino,
            hora,
            linha,
            visitados | {origem}
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

        tempo_ajustado = tempo * PESO_LINHA.get(linha, 1.0)
        custo_extra = tempo_ajustado * fator_horario(hora)
        custo_extra += penalidade_troca(linha_atual, linha, origem)

        custo_rec, caminho = menor_custo_sem_memo(
            vizinho,
            destino,
            hora,
            linha,
            visitados | {origem}
        )

        if custo_rec == float('inf'):
            continue

        custo_total = custo_extra + custo_rec

        if custo_total < melhor[0]:
            melhor = (custo_total, [origem] + caminho)

    return melhor

# =====================================
# MAIOR CAMINHO
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

        tempo_ajustado = tempo * PESO_LINHA.get(linha, 1.0)
        custo_extra = tempo_ajustado * fator_horario(hora)
        custo_extra += penalidade_troca(linha_atual, linha, origem)

        custo_rec, caminho = maior_caminho(
            vizinho,
            destino,
            hora,
            linha,
            visitados | {origem}
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

origem = "Tucuruvi"
destino = "Capao Redondo"
hora = int(input("Digite a hora (0-23): "))

# IMPORTANTE: limpar cache antes de medir para evitar
# resultados contaminados de execucoes anteriores (bug comum em Jupyter/Colab).
menor_custo_com_memo.cache_clear()

tracemalloc.start()

# COM MEMO
t0 = time.perf_counter()
custo_min_memo, caminho_min_memo = menor_custo_com_memo(origem, destino, hora)
t1 = time.perf_counter()

# SEM MEMO — cache ja foi usado, agora medimos apenas a versao sem cache
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
    "Tucuruvi": (-23.480, -46.603),
    "Parada Inglesa": (-23.487, -46.608),
    "Jardim Sao Paulo": (-23.492, -46.614),
    "Santana": (-23.500, -46.625),
    "Carandiru": (-23.507, -46.623),
    "Portuguesa-Tiete": (-23.516, -46.622),
    "Armenia": (-23.525, -46.629),
    "Tiradentes": (-23.531, -46.633),
    "Luz": (-23.536, -46.633),
    "Sao Bento": (-23.544, -46.634),
    "Se": (-23.550, -46.633),
    "Liberdade": (-23.556, -46.635),
    "Sao Joaquim": (-23.561, -46.638),
    "Vergueiro": (-23.568, -46.640),
    "Paraiso": (-23.575, -46.640),
    "Ana Rosa": (-23.582, -46.638),
    "Vila Mariana": (-23.589, -46.634),
    "Santa Cruz": (-23.600, -46.637),
    "Praca da Arvore": (-23.610, -46.637),
    "Saude": (-23.620, -46.636),
    "Sao Judas": (-23.628, -46.635),
    "Conceicao": (-23.635, -46.641),
    "Jabaquara": (-23.646, -46.641),
    "Republica": (-23.544, -46.642),
    "Paulista": (-23.555, -46.662),
    "Pinheiros": (-23.566, -46.702),
    "Vila Sonia": (-23.588, -46.734),
    "Brigadeiro": (-23.561, -46.655),
    "Trianon-Masp": (-23.561, -46.659),
    "Consolacao": (-23.557, -46.662),
    "Clinicas": (-23.555, -46.673),
    "Sumare": (-23.550, -46.680),
    "Vila Madalena": (-23.546, -46.692),
    "Chacara Klabin": (-23.592, -46.630),
    "Santo Amaro": (-23.650, -46.710),
    "Campo Limpo": (-23.650, -46.760),
    "Capao Redondo": (-23.660, -46.780)
}

import folium

mapa = folium.Map(location=[-23.55, -46.63], zoom_start=11, tiles="CartoDB positron")

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
            folium.PolyLine([coords[orig], coords[dest]], color="gray", weight=2, opacity=0.4).add_to(mapa)

folium.PolyLine([coords[e] for e in caminho_min_memo if e in coords], color="green", weight=6, opacity=0.9).add_to(mapa)
folium.PolyLine([coords[e] for e in caminho_max if e in coords], color="red", weight=4, opacity=0.8).add_to(mapa)

mapa.save("metro_sp.html")
print("Mapa salvo como metro_sp.html")
