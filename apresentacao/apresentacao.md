# Apresentação — UVA 1235 *Anti Brute Force Lock*

> Fonte editável dos slides. O PDF entregue é `apresentacao.pdf`.
> Trabalho Prático 1 · Unidade 3 · **Grupo F** · Prof. Me. Ricardo Carubbi.

---

## Slide 1 — Capa

**Anti Brute Force Lock — UVA 1235**
Árvore Geradora Mínima · Kruskal · Union-Find

Grupo F — Resolução de Problemas com Grafos (Unidade 3)

---

## Slide 2 — O problema

Cadeado com **4 rodas** de dígitos `0–9`. As rodas são **circulares**:
do `9` passa ao `0`, do `0` ao `9`. Cada movimento = **1 rolagem**.

- O cadeado começa em `0000`.
- São dadas **N chaves** (`1 ≤ N ≤ 500`) que precisam **todas** ser destravadas.
- Botão **`JUMP`**: pula de graça para qualquer chave **já destravada** —
  **nunca** para `0000`.
- **Objetivo:** destravar todas as chaves com o **menor total de rolagens**.

---

## Slide 3 — Exemplo (2º caso oficial)

Chaves: `1111`, `1155`, `5511`.

- `0000 → 1111` : **4** rolagens (entrada)
- `1111 → 1155` : **8** rolagens
- `JUMP 1155 → 1111` : grátis (`1111` já destravada)
- `1111 → 5511` : **8** rolagens
- **Total = 4 + 8 + 8 = 20**

---

## Slide 4 — Modelagem como grafo

| Problema | Grafo |
|---|---|
| cada chave de 4 dígitos | **vértice** |
| trocar uma chave por outra | **aresta** (grafo **completo**) |
| rolagens entre duas chaves | **peso** da aresta |

Peso = soma da **distância circular** das 4 rodas:
`dist(x, y) = min(|x − y|, 10 − |x − y|)`.
Do dígito `0` ao `9` custa **1** (não 9).

---

## Slide 5 — A pegadinha: `0000` é uma FOLHA

`JUMP` só volta para chaves **já destravadas** → **nunca** para `0000`.
Ao sair de `0000` uma vez, não se volta mais.

➡️ `0000` tem **grau 1 (folha)**: participa só na 1ª rolagem.

**Erro comum:** calcular a MST de `N+1` vértices com `0000` livre.
No 3º caso oficial isso dá **24**, mas a resposta correta é **26**.

---

## Slide 6 — Estratégia

Uma árvore geradora com `0000` fixado como folha é sempre:

`(1 aresta 0000 → chave)` + `(árvore geradora das N chaves)`

As duas partes são **independentes** → minimizar cada uma:

**RESPOSTA = MST(chaves) + menor rolagem(`0000` → chave)**

---

## Slide 7 — Algoritmo: Kruskal + Union-Find

1. Gera todas as `E = N(N−1)/2` arestas do grafo completo.
2. **Ordena** as arestas por peso crescente.
3. Para cada aresta, o **Union-Find** verifica se ela fecha um **ciclo**:
   fecha → descarta; não fecha → une componentes e entra na MST.
4. Soma a aresta de entrada de `0000`.

Union-Find = *weighted quick-union* + compressão de caminho.
Prim `O(V²)` também implementado (verificação cruzada).

---

## Slide 8 — Complexidade

`N` = número de chaves (`≤ 500`).

- Construir o grafo completo: `O(N²)`
- Ordenar as arestas (Kruskal): `O(N² log N)` ← **domina**
- Union-Find: `O(N² · α(N))`, α ≤ 4 na prática
- **Total por caso: `O(N² log N)`** · Memória: `O(N²)`

Prim `O(V²)`: alternativa assintoticamente ótima para grafo denso.

---

## Slide 9 — Casos especiais

- **`N = 1`**: sem MST entre chaves; resposta = rolagem(`0000` → chave).
- **`0000` sempre folha** — é o núcleo da modelagem.
- **Roda circular**: o par `0 ↔ 9` custa 1.
- **Chaves repetidas / iguais a `0000`**: arestas de peso 0, tratadas normalmente.
- **Ordem de destravamento é livre**: a MST não depende da ordem.

---

## Slide 10 — Resultado

Exemplo oficial da UVA — 4 casos: **16 · 20 · 26 · 17** → todos corretos ✔️

Kruskal e Prim concordam (modo `--test`).
Solução autocontida em **Python 3**, pronta para submissão na UVA.

**Obrigado!**
