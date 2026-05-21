# Trabalho Prático 1 — UVA 1235 *Anti Brute Force Lock*

> Resolução de Problemas com Grafos — Unidade 3
> Prof. Me. Ricardo Carubbi — **Grupo F**

Solução do problema **UVA 1235 — Anti Brute Force Lock**, modelado como
**Árvore Geradora Mínima (MST)** e resolvido com **Kruskal + Union-Find (DSU)**.

---

## 1. Problema

| | |
|---|---|
| **Nome** | Anti Brute Force Lock |
| **Plataforma** | UVA Online Judge — problema **1235** |
| **Link** | <https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=3676> |
| **Tema** | Árvore Geradora Mínima · Kruskal · Prim · Union-Find/DSU |

## 2. Integrantes do grupo

| Nome | Matrícula |
|---|---|
| João Vitor Silva | `2210358` |
| `Pablo Dornelles` | `2315750` |
| `Antônio Davi` | `2220247` |

## 3. Linguagem

**Python 3** (testado no Python 3.14). A solução usa **apenas a biblioteca
padrão** (`sys`). Nenhuma biblioteca externa de grafos é utilizada — Kruskal,
Prim e Union-Find foram implementados pelo grupo (ver `src/main.py`).

## 4. Estrutura do repositório

```text
.
├── README.md                       <- este arquivo
├── T1.md                           <- enunciado do trabalho
├── src/
│   └── main.py                     <- solução completa (Kruskal + Union-Find + Prim)
├── dados/
│   ├── entradas_do_problema.txt    <- entrada de exemplo (exemplo oficial da UVA)
│   └── saida_esperada.txt          <- saída esperada para a entrada acima
├── evidencias/
│   ├── COMO_OBTER_A_EVIDENCIA.md   <- passo a passo da submissão
│   └── accepted.png                <- print do Accepted (adicionar após submeter)
├── apresentacao/
│   ├── apresentacao.pdf            <- slides da apresentação
│   └── apresentacao.md             <- fonte dos slides
└── algs4-py/                       <- base algs4 usada como referência conceitual
```

## 5. Como executar

Pré-requisito: **Python 3** instalado (`python3 --version`).

A solução lê da **entrada padrão** e escreve na **saída padrão**.

```sh
# executar com o arquivo de entrada de exemplo
python3 src/main.py < dados/entradas_do_problema.txt

# saída esperada:
# 16
# 20
# 26
# 17
```

```sh
# conferir contra a saída esperada (não deve imprimir diferenças)
python3 src/main.py < dados/entradas_do_problema.txt | diff - dados/saida_esperada.txt
```

```sh
# modo de autoteste: roda o exemplo oficial da UVA e confere os 4 resultados,
# verificando ainda que Kruskal e Prim chegam ao mesmo valor
python3 src/main.py --test
```

## 6. O problema em resumo

Um cadeado tem **4 rodas**, cada uma com os dígitos **0 a 9**. As rodas são
**circulares**: do `9` passa-se ao `0` e do `0` ao `9`, cada movimento conta
como **uma rolagem**.

O cadeado começa em `0000`. São dadas **N chaves** de 4 dígitos
(`1 ≤ N ≤ 500`) que precisam **todas ser destravadas**. As regras:

- destravar uma chave = ajustar as rodas até ela e apertar `UNLOCK`;
- o botão **`JUMP`** muda as rodas, **de graça**, para **qualquer chave já
  destravada** — *nunca* para `0000`;
- objetivo: destravar todas as chaves com o **menor total de rolagens**
  (o `JUMP` não conta).

**Saída:** para cada caso, o número mínimo de rolagens.

## 7. Modelagem como grafo

| Elemento do problema | Elemento do grafo |
|---|---|
| cada chave de 4 dígitos | **vértice** |
| trocar uma chave por outra | **aresta** (grafo **completo** entre chaves) |
| rolagens para ir de uma chave a outra | **peso** da aresta |

**Peso de uma aresta** entre duas chaves = soma, sobre as 4 rodas, da
**distância circular** de cada dígito:

```
dist_digito(x, y) = min(|x - y|, 10 - |x - y|)
peso(A, B)        = Σ  dist_digito(A_i, B_i),  i = 0..3
```

Exemplo: `peso(1155, 2211)` = `1 + 1 + 4 + 4 = 10`.

### Por que `0000` é uma *folha* (o ponto-chave da modelagem)

O `JUMP` só teleporta para chaves **já destravadas**. O `0000` é o estado
inicial, **não é uma chave** — então, assim que rolamos para fora dele para
destravar a primeira chave, **nunca mais conseguimos voltar a `0000`**.

Logo, `0000` é "usado" **uma única vez**: a rolagem inicial até a primeira
chave. No grafo, isso significa que **`0000` tem grau 1 — é uma folha**.

Toda chave seguinte é alcançada rolando a partir de **alguma chave já
destravada** (pula-se de graça até ela). É exatamente o crescimento de uma
MST: um conjunto que se expande sempre pela aresta mais barata.

> ⚠️ **Cuidado:** *não* basta calcular a MST de `N+1` vértices
> (`0000` + chaves). Se `0000` pudesse ser um vértice intermediário (grau ≥ 2),
> ele funcionaria como um "atalho" — o que é fisicamente impossível aqui.
> No 3º caso do exemplo oficial, a MST livre dos 4 vértices vale **24**,
> mas a resposta correta é **26**, justamente porque `0000` é forçado a ser folha.

### Estratégia derivada da modelagem

Como uma árvore geradora com `0000` fixado como folha é sempre
*(uma aresta de `0000` até uma chave)* + *(uma árvore geradora das chaves)*,
e essas duas partes são **independentes**, basta minimizar cada uma:

```
RESPOSTA = peso da MST sobre as N chaves
         + menor rolagem de "0000" até alguma chave
```

## 8. Algoritmo utilizado

### Kruskal + Union-Find (DSU) — algoritmo principal

1. Geram-se **todas** as `E = N(N-1)/2` arestas do grafo completo das chaves.
2. As arestas são **ordenadas por peso crescente**.
3. Percorrem-se as arestas da mais leve para a mais pesada. Para cada aresta
   `(u, v)`, o **Union-Find** responde se `u` e `v` **já estão na mesma
   componente**:
   - se já estão → a aresta fecharia um **ciclo** → é **descartada**;
   - se não estão → as componentes são **unidas** e a aresta **entra na MST**.
4. Para quando a árvore tem `N-1` arestas.

Por fim, soma-se a menor distância de `0000` até uma chave.

**Papel do Union-Find:** é a estrutura que torna o Kruskal eficiente. Ele
mantém as componentes conexas parciais e responde, em tempo praticamente
constante (`O(α(N))`, amortizado), à pergunta *"adicionar esta aresta cria um
ciclo?"*. Nossa implementação usa **weighted quick-union** (pendura a árvore
menor sob a maior) com **compressão de caminho**, a mesma lógica de
`algs4-py/algs4/uf.py`.

### Prim `O(V²)` — alternativa incluída

O arquivo também traz `prim_mst()`, uma implementação de **Prim** sem fila de
prioridade (`O(V²)`), usada como **verificação cruzada** no modo `--test`
(Kruskal e Prim devem dar o mesmo resultado).

### Kruskal × Prim — justificativa da escolha

O grafo é **completo e denso** (`E = Θ(V²)`). Nesse cenário, **Prim `O(V²)`**
é assintoticamente *melhor* que Kruskal `O(E log E) = O(V² log V)`. Ainda
assim, escolhemos **Kruskal** como algoritmo principal porque:

1. o foco da unidade é **Union-Find/DSU**, que o Kruskal exercita diretamente;
2. a base de referência `algs4-py` implementa MST com Kruskal + `UF`;
3. com `N ≤ 500` a diferença de desempenho é **irrelevante** — os dois rodam
   em frações de milissegundo para os dados reais do problema.

Ambos estão implementados; o `--test` confirma que concordam.

## 9. Análise de complexidade

Seja `N` o número de chaves (`N ≤ 500`). Cada chave tem 4 dígitos (constante).

| Etapa | Custo |
|---|---|
| Construir o grafo completo (`E = N(N-1)/2` arestas) | `O(N²)` — cada peso é `O(1)` com a tabela `DIGIT_DIST` |
| Ordenar as arestas (Kruskal) | `O(E log E) = O(N² log N)` |
| Operações de Union-Find | `O(E · α(N))` ≈ `O(N²)` (α = inversa de Ackermann, ≤ 4 na prática) |
| Menor distância de `0000` | `O(N)` |
| **Total por caso de teste** | **`O(N² log N)`** (dominado pela ordenação) |
| **Memória** | `O(N²)` (lista de arestas) |

- **Prim `O(V²)`** (alternativa): tempo `O(N²)`, memória `O(N)`.
- Como todo peso de aresta é um inteiro em `[0, 20]`, a ordenação poderia ser
  feita por **contagem** em `O(E)`; usamos `sort` padrão por clareza.
- Medição: o pior caso sintético (`T = 20`, `N = 500` em todos) roda em ≈ 2,5 s;
  os dados reais da UVA são muito menores e rodam praticamente instantâneos.

## 10. Casos especiais testados

- **`N = 1`** — não há arestas entre chaves; a MST vale 0; a resposta é apenas
  a rolagem de `0000` até a única chave.
- **`0000` como folha** — usar `0000` como vértice intermediário daria um valor
  *menor e errado* (ver caso 3 do exemplo oficial: 24 ≠ 26).
- **Roda circular** — a distância de um dígito é `min(d, 10-d)`; o par `0↔9`
  custa 1, não 9.
- **Chaves repetidas ou chave igual a `0000`** — geram arestas de peso 0;
  o Kruskal as trata normalmente.
- **Pesos iguais** — a ordem de desempate não afeta o *peso* da MST.
- **Ordem de destravamento livre** — não importa: a MST independe da ordem e o
  `JUMP` é gratuito.

## 11. Exemplo resolvido passo a passo (1º caso oficial)

Entrada: `N = 2`, chaves `1155` e `2211`.

1. **Vértices (chaves):** `1155`, `2211`. O estado inicial `0000` é folha.
2. **MST sobre as chaves:** só há uma aresta —
   `peso(1155, 2211) = 1+1+4+4 = 10`. MST = **10**.
3. **Aresta de entrada (de `0000`):**
   `peso(0000, 1155) = 1+1+5+5 = 12` e `peso(0000, 2211) = 2+2+1+1 = 6`.
   Menor = **6**.
4. **Resposta = 10 + 6 = 16.** ✔️

Verificação dos quatro casos oficiais (`python3 src/main.py --test`):

| Caso | Entrada | Saída esperada | Saída obtida |
|---|---|---|---|
| 1 | `1155 2211` | 16 | **16** ✔️ |
| 2 | `1111 1155 5511` | 20 | **20** ✔️ |
| 3 | `1234 5678 9090` | 26 | **26** ✔️ |
| 4 | `2145 0213 9113 8113` | 17 | **17** ✔️ |

## 12. Evidência de submissão (Accepted)

A solução (`src/main.py`) foi submetida no UVA Online Judge e obteve o
veredito **Accepted**:

| Submissão | Problema | Veredito | Linguagem | Tempo | Data |
|---|---|---|---|---|---|
| `31141236` | 1235 — Anti Brute Force Lock | **Accepted** | Python 3 | 0,700 s | 2026-05-21 |

![Evidência de Accepted na UVA](evidencias/accepted.png)

> O print da página de submissões está em `evidencias/accepted.png`. O passo a
> passo da submissão está em
> [`evidencias/COMO_OBTER_A_EVIDENCIA.md`](evidencias/COMO_OBTER_A_EVIDENCIA.md).

## 13. Base de referência `algs4`

Conforme o enunciado, a base `algs4-py` foi usada como **referência conceitual
e estrutural**. A classe `UnionFind` de `src/main.py` segue a mesma lógica de
`algs4-py/algs4/uf.py` (weighted quick-union + compressão de caminho), e o
fluxo do Kruskal espelha `algs4-py/algs4/kruskal_mst.py`. Nenhuma biblioteca
pronta de MST foi utilizada — toda a lógica algorítmica é do grupo.

## 14. Apresentação

Os slides estão em [`apresentacao/apresentacao.pdf`](apresentacao/apresentacao.pdf)
(fonte editável em `apresentacao/apresentacao.md`).

## 15. Tutorial de execução (passo a passo para o professor testar)

Roteiro completo para **clonar, executar e reproduzir** a solução do zero. Não é
preciso instalar nada além do **Python 3** — a solução não tem dependências
externas. Todos os comandos são executados **a partir da raiz do repositório**.

### Passo 1 — Clonar o repositório

```sh
git clone <URL_DO_REPOSITORIO>
cd <pasta-do-repositorio>
```

### Passo 2 — Confirmar que o Python 3 está instalado

```sh
python3 --version
```

Deve aparecer algo como `Python 3.x`. No **Windows**, use `python` no lugar de
`python3` em todos os comandos seguintes.

### Passo 3 — Teste rápido *(recomendado)*: autoteste embutido

Roda o exemplo oficial da UVA, confere os 4 resultados e ainda verifica que
**Kruskal e Prim** chegam ao mesmo valor:

```sh
python3 src/main.py --test
```

Saída esperada:

```text
Caso 1  esperado=16   kruskal=16   prim=16   [OK]
Caso 2  esperado=20   kruskal=20   prim=20   [OK]
Caso 3  esperado=26   kruskal=26   prim=26   [OK]
Caso 4  esperado=17   kruskal=17   prim=17   [OK]
-> TODOS OS CASOS PASSARAM
```

### Passo 4 — Executar com o arquivo de entrada

O programa lê da **entrada padrão** (`stdin`). Para usar o arquivo de exemplo:

```sh
python3 src/main.py < dados/entradas_do_problema.txt
```

Saída esperada:

```text
16
20
26
17
```

### Passo 5 — Conferir automaticamente contra a saída esperada

```sh
python3 src/main.py < dados/entradas_do_problema.txt | diff - dados/saida_esperada.txt
```

Se o comando **não imprimir nada**, a saída está idêntica à esperada. ✔️

### Passo 6 — Testar com uma entrada própria *(opcional)*

Crie um arquivo, por exemplo `meu_teste.txt`, no formato da UVA — a primeira
linha é `T` (número de casos); cada caso é `N` seguido das `N` chaves de 4
dígitos:

```text
1
3 1234 5678 9090
```

Execute:

```sh
python3 src/main.py < meu_teste.txt
```

Resultado: `26`.

> Também é possível digitar a entrada direto no teclado: rode `python3 src/main.py`,
> digite os números e encerre com `Ctrl+D` (Linux/macOS) ou `Ctrl+Z` + `Enter`
> (Windows).

### Resumo dos comandos

| Comando | O que faz |
|---|---|
| `python3 src/main.py --test` | autoteste com o exemplo oficial da UVA |
| `python3 src/main.py < dados/entradas_do_problema.txt` | executa com o arquivo de entrada |
| `python3 src/main.py < dados/entradas_do_problema.txt \| diff - dados/saida_esperada.txt` | confere contra a saída esperada |
