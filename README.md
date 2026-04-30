# 🚇 Checkpoint 2 — Dynamic Programming — FIAP

**Disciplina:** FIAP — Dynamic Programming  
**Checkpoint:** Checkpoint 2 — Em Grupo  
**Professor:** Andre Marques

---

## 👥 Integrantes do Grupo

| Nome | RA |
|------|----|
| *Davi Marques de Andrade Munhoz* | *566223* |
| *Diogo Oliveira Lima* | *562559* |
| *Leandro Simoneli da Silva* | *566539* |
| *Lucas dos Reis Aquino* | *562414* |
| *Lucas Perez Bonato* | *565356* |

---

## 📓 Notebooks Documentados

Os notebooks abaixo contêm os algoritmos executados com outputs completos, gráficos de desempenho e conclusões por cidade:

| Cidade | Notebook |
|--------|----------|
| 🇧🇷 São Paulo (Metrô + CPTM) | [FINAL_SP.ipynb](./SP_SUBWAY/FINAL_SP.ipynb) |
| 🇺🇸 San Francisco (BART) | [FINAL_EUA.ipynb](./EUA_SUBWAY/FINAL_EUA.ipynb) |
| 🇨🇳 Beijing (Metro) | [FINAL_CHINA.ipynb](./CHINA_SUBWAY/FINAL_CHINA.ipynb) |

---

## 📁 Estrutura do Repositório

```
CP02.DynamicProgramming/
│
├── .gitignore
├── README.md
│
├── CHINA_SUBWAY/
│   ├── cp_dynamic_metro_china.py
│   ├── FINAL_CHINA.ipynb
│   ├── desempenho_beijing.png
│   └── mapa_beijing.html
│
├── EUA_SUBWAY/
│   ├── cp_dynamic_metro_eua.py
│   ├── FINAL_EUA.ipynb
│   ├── desempenho_bart.png
│   └── mapa_bart.html
│
└── SP_SUBWAY/
    ├── cp_dynamic_metro_sp.py
    ├── FINAL_SP.ipynb
    ├── desempenho_sp.png
    └── mapa_sp.html               
```

---

## 🌐 Contexto

Sistema de roteamento para metrô em três metrópoles globais. O custo de cada trecho varia dinamicamente conforme o horário do dia — picos geram penalidades e madrugadas oferecem bônus. As redes são modeladas como grafos ponderados; a busca pelo menor e maior caminho é implementada com **recursão + memoização** (`functools.lru_cache`).

Cada script agora inclui:
- Documentação completa em docstrings e comentários inline
- Medição **independente** de tempo e memória para cada versão (com e sem memo)
- **Gráfico comparativo** gerado pelo matplotlib (barras lado a lado)
- Tabela de desempenho impressa no terminal
- **Conclusão** por cidade impressa antes de gerar o mapa folium

---

## 🗺️ Modelagem dos Grafos

### Tipo de grafo
Os três grafos são **não-dirigidos** (bidirecionais): cada conexão entre estações é representada em ambos os sentidos, pois trens operam nas duas direções. Cada aresta carrega:
- `destino` — estação vizinha
- `linha` — identificador da linha (azul, verde, amarela etc.)
- `tempo` — peso base em minutos

O **custo efetivo** de uma aresta é calculado como:

```
custo_efetivo = tempo × fator_horario(hora) + penalidade_troca(linha_atual, nova_linha)
```

> Em São Paulo, o `tempo` é adicionalmente multiplicado por `PESO_LINHA`
> (ex.: Linha Amarela = 0,9 — mais rápida; CPTM = 1,2 — mais lenta).

### Resumo dos grafos

| Cidade | Estações | Linhas | Origem | Destino |
|--------|----------|--------|--------|---------|
| 🇧🇷 São Paulo | 37 | 5 (azul, verde, amarela, lilás, esmeralda) | Tucuruvi | Capão Redondo |
| 🇺🇸 San Francisco | 23 | 3 (azul, amarela, verde) | Dublin/Pleasanton | Daly City |
| 🇨🇳 Beijing | 22 | 4 (1, 2, 4, 10) | Sihui East | Xizhimen |

Todos os grafos possuem **múltiplos caminhos** entre origem e destino — requisito essencial para que os algoritmos tenham escolhas reais a comparar.

---

## ⏱️ Fatores de Horário

| Faixa Horária | Fator | Justificativa |
|---------------|-------|---------------|
| 5h – 7h | ×0,6 | **Bônus** — metrô vazio, embarque rápido |
| 7h – 9h | ×1,5 | Pico da manhã — volume moderado-alto |
| 9h – 17h | ×1,0 | Horário normal, sem penalidade |
| 17h – 20h | ×2,0 | **Penalidade máxima** — pico da tarde, lotação |
| 20h – 5h | ×1,2 | Noturno — fluxo reduzido mas irregular |

---

## 🧮 Algoritmos Implementados

### 1. Menor Caminho com Memoização (`lru_cache`)

```python
@functools.lru_cache(maxsize=None)
def menor_custo_com_memo(origem, destino, hora, linha_atual=None, visitados=frozenset()):
    if origem == destino:
        return (0, [origem])
    # explora todos os vizinhos não visitados, retorna o mínimo
    ...
```

A chave de cache é a tupla `(origem, destino, hora, linha_atual, visitados)`.  
O `frozenset` de visitados é imutável e hashável, permitindo seu uso como chave.

### 2. Menor Caminho sem Memoização

Mesma lógica, mas sem cache — explora o grafo completamente a cada chamada.

### 3. Maior Caminho (Backtracking)

Busca exaustiva por recursão + backtracking, sem `lru_cache`.  
Garante que não há ciclos (nenhum nó é visitado duas vezes no mesmo caminho).  
Retorna o caminho com maior custo total.

---

## 📊 Análise de Desempenho

> Todos os testes foram realizados com `hora = 18` (pico da tarde, fator ×2,0).  
> Hardware: medido com `time.perf_counter()` e `tracemalloc`.  
> Cada versão (com memo / sem memo) é medida **separadamente** com `tracemalloc.start/stop` individual.

### 🇧🇷 São Paulo — Tucuruvi → Capão Redondo

| Métrica | Com Memoização | Sem Memoização |
|---------|---------------|----------------|
| Tempo de execução | ~2,3 ms | ~1,0 ms |
| Memória (pico) | ~138 KB | ~138 KB |
| Caminho encontrado | idêntico | idêntico |
| Tempo de viagem (h=18) | 1h 42min | 1h 42min |
| Nº de estações no caminho | 15 | 15 |

**Menor caminho (h=18):**  
`Tucuruvi → ... → Luz → Republica → Paulista → Pinheiros → Santo Amaro → Campo Limpo → Capão Redondo`  
*(via Linha Amarela — mais eficiente que seguir a Azul até Santa Cruz)*

**Maior caminho (h=18):**  
`Tucuruvi → ... → Ana Rosa → Chacara Klabin → Santa Cruz → Santo Amaro → Campo Limpo → Capão Redondo`

---

### 🇺🇸 San Francisco — Dublin/Pleasanton → Daly City

| Métrica | Com Memoização | Sem Memoização |
|---------|---------------|----------------|
| Tempo de execução | ~0,76 ms | ~0,56 ms |
| Memória (pico) | ~64 KB | ~64 KB |
| Caminho encontrado | idêntico | idêntico |
| Tempo de viagem (h=18) | 2h 2min | 2h 2min |
| Nº de estações no caminho | 14 | 14 |

**Menor caminho (h=18):**  
`Dublin/Pleasanton → West Dublin → Castro Valley → Bay Fair → San Leandro → Coliseum → Fruitvale → Lake Merritt → 12th St Oakland → 19th St Oakland → West Oakland → Embarcadero → ... → Daly City`

**Maior caminho (h=18):**  
`... → Bay Fair → Coliseum → Fruitvale → Lake Merritt → 12th St Oakland → 19th St Oakland → West Oakland → ...`  
*(desvia pelo trecho costeiro via Coliseum para maximizar o tempo)*

---

### 🇨🇳 Beijing — Sihui East → Xizhimen

| Métrica | Com Memoização | Sem Memoização |
|---------|---------------|----------------|
| Tempo de execução | ~0,54 ms | ~0,46 ms |
| Memória (pico) | ~46 KB | ~46 KB |
| Caminho encontrado | idêntico | idêntico |
| Tempo de viagem (h=18) | 40 min | 40 min |
| Nº de estações no caminho | 7 | 7 |

**Menor caminho (h=18):**  
`Sihui East → Sihui → Guomao → Yonganli → Jianguomen → Fuxingmen → Xizhimen`  
*(caminho direto pela Linha 1 → 2, apenas uma troca de linha)*

**Maior caminho (h=18):**  
`Sihui East → Sihui → Guomao → Jiaomenxi → Taoranting → Caishikou → Xuanwumen → Xidan → ... → Jianguomen → Fuxingmen → Xizhimen`  
*(15 estações — percorre o arco pela Linha 4, maximizando o tempo total)*

---

### 📈 Tabela Comparativa Consolidada (hora = 18)

| Cidade | Com Memo (ms) | Sem Memo (ms) | Razão Memo/SemMemo | Memória (KB) |
|--------|--------------|--------------|-------------------|-------------|
| São Paulo | 2,27 | 0,96 | **2,4×** mais lento | 137,7 |
| San Francisco | 0,76 | 0,56 | **1,4×** mais lento | 64,4 |
| Beijing | 0,54 | 0,46 | **1,2×** mais lento | 46,3 |

---

## 🔍 Por que a Memoização NÃO é Mais Rápida Neste Caso?

Esta é a observação mais importante do projeto. Em todos os três casos, a versão **sem memoização foi mais rápida** que a versão com `lru_cache`. Isso parece contraintuitivo — afinal, memoização deveria evitar recomputações. Existem algumas razões pela qual isso ocorreu:

### Razão 1 — O estado inclui o conjunto `visitados`

A chave do cache é `(origem, destino, hora, linha_atual, visitados)`.  
O `frozenset` `visitados` representa **qual caminho específico foi percorrido até aqui**.  
Dois caminhos diferentes que chegam ao mesmo nó terão `visitados` distintos, portanto **são entradas de cache diferentes**.

```
Caminho A: Tucuruvi → Parada Inglesa → Santana → ...
  cache key: (Santana, Capao Redondo, 18, "azul", frozenset({Tucuruvi, Parada Inglesa}))

Caminho B: Tucuruvi → Jardim SP → Santana → ...
  cache key: (Santana, Capao Redondo, 18, "azul", frozenset({Tucuruvi, Jardim SP}))
```

São **estados diferentes** → nenhum cache hit! O cache é preenchido mas raramente aproveitado.

### Razão 2 — Overhead do `lru_cache`

Cada chamada à função com cache paga um custo extra:
- Cálculo do hash de todos os argumentos (incluindo o `frozenset`)
- Consulta no dicionário interno do cache
- Eventual armazenamento do resultado

Para grafos pequenos (22–37 nós), esse overhead supera qualquer ganho.

### Razão 3 — Poucos subproblemas sobrepostos

Em DFS com backtracking e controle de `visitados`, os subproblemas raramente se repetem. A memoização clássica brilha em problemas onde os **mesmos subproblemas aparecem muitas vezes** (ex.: Fibonacci, mochila, LCS). Aqui, a profundidade da recursão é limitada pelo número de nós e o conjunto `visitados` garante unicidade.

### Quando a memoização VENCERIA?

Em grafos grandes (metrôs reais com 200–400 estações):
1. Subgrafos mais compactos → mais colisões de chave → mais cache hits
2. O ganho proporcional cresce conforme a explosão combinatória aumenta
3. Sem visitados na chave (ex.: programação dinâmica em DAGs), o benefício é máximo

### Resumo visual

```
Grafo pequeno (22-37 nós):
  memo:    [overhead_hash + overhead_dict] > [ganho_cache]  → MAIS LENTO
  no-memo: [computação_direta]                              → MAIS RÁPIDO

Grafo grande (200+ nós):
  memo:    [overhead_hash + overhead_dict] << [ganho_cache] → MAIS RÁPIDO
  no-memo: [explosão_combinatória]                          → INVIÁVEL
```

---

## 🧠 Análise de Complexidade

### Menor Caminho (DFS exaustivo)

- **Sem memoização:** `O(n!)` no pior caso — cada chamada pode explorar todos os nós não visitados. Para um grafo com `n` nós e múltiplos caminhos, a recursão percorre essencialmente todas as permutações possíveis dos nós acessíveis.
- **Com memoização:** Teoricamente `O(n × 2^n)` — o estado `(nó, visitados)` tem `n × 2^n` combinações únicas. Na prática, o número de caminhos simples em um grafo esparso é muito menor.

### Maior Caminho (Longest Simple Path)

O problema do caminho mais longo simples em grafos gerais é **NP-difícil**. Nossa implementação de backtracking exaustivo tem complexidade `O(n!)`, aceitável apenas para grafos pequenos como os modelados aqui.

### Por que não Dijkstra?

O algoritmo de Dijkstra encontra o menor caminho em `O((V + E) log V)` mas não é facilmente adaptável para:
- Penalidades que dependem da **linha atual** (histórico do caminho)
- Restrições de **nós visitados** (menor caminho simples)

O DFS recursivo com memoização é mais flexível para essas restrições, ao custo de maior complexidade.

---

## 🗺️ Visualização

Os três scripts geram mapas interativos com `folium`:

| Arquivo | Cidade | Descrição |
|---------|--------|-----------|
| `metro_sp.html` | São Paulo | Metrô + CPTM sobreposto ao mapa real |
| `mapa_bart.html` | San Francisco | Rede BART sobre a Bay Area |
| `mapa_beijing.html` | Beijing | Metro de Pequim |

**Legenda dos mapas:**
- 🟢 Marcador verde = estação de origem
- 🔴 Marcador vermelho = estação de destino
- 🔵 Marcadores azuis = demais estações
- **Linha verde (espessa)** = menor caminho
- **Linha vermelha** = maior caminho
- **Linhas cinzas** = todas as conexões do grafo

Para abrir os mapas localmente:
```bash
python -m http.server
# Acesse: http://localhost:8000/metro_sp.html
```

Os três scripts também geram **gráficos de barras comparativos** (matplotlib) salvos como:
- `desempenho_sp.png`
- `desempenho_bart.png`
- `desempenho_beijing.png`

---

## 🔬 Conclusões

1. **Memoização não garante ganho de desempenho em grafos pequenos.** O overhead do `lru_cache` (hashing de tuplas e frozensets) supera o ganho de cache em grafos com menos de ~50 nós.

2. **O benefício da memoização cresce com o tamanho do grafo.** Em redes reais (ex.: São Paulo completa com 90+ estações), a memoização se tornaria essencial para viabilizar a busca.

3. **Subproblemas sobrepostos são raros com `visitados` na chave.** A inclusão do conjunto de nós visitados na chave do cache cria estados quase únicos, eliminando a maioria dos hits. A memoização clássica de DP funciona melhor quando o estado não depende do caminho percorrido.

4. **O caminho mais longo simples é NP-difícil.** A abordagem de backtracking exaustivo funciona apenas para grafos pequenos; em redes reais, seria necessário usar heurísticas ou aproximações.

5. **Limpeza de cache é crítica em ambientes Jupyter/Colab.** Não chamar `cache_clear()` entre execuções pode produzir resultados incorretos, mascarando o verdadeiro desempenho do algoritmo — como observado nos testes iniciais do SP.

6. **Medição independente de memória.** Cada versão (com/sem memo) tem seu próprio bloco `tracemalloc.start/stop`, garantindo que o pico de memória de uma não contamine a medição da outra.

---

## ▶️ Como Executar

```bash
# Instalar dependências
pip install folium matplotlib

# Executar cada cidade
python cp_dynamic_metro_sp.py
python cp_dynamic_metro_eua.py
python cp_dynamic_metro_china.py

# Informar a hora quando solicitado (ex: 18)
```

**Requisitos:** Python 3.10+, folium, matplotlib, functools (stdlib), time (stdlib), tracemalloc (stdlib)