# Apresentação — UVA 1235 *Anti Brute Force Lock*

> Resolução de Problemas com Grafos — Grupo F  
> Árvore Geradora Mínima com Kruskal e Union-Find  
> Apresentado por: João Vitor Silva, Antonio Davi e Pablo Dornelles

---

## Slide 1 — Capa

# UVA 1235  
## *Anti Brute Force Lock*

**Árvore Geradora Mínima com Kruskal e Union-Find**

**Objetivo:** encontrar o menor total de rolagens para destravar todas as chaves do cadeado.

**Disciplina:** Resolução de Problemas com Grafos  
**Grupo F**

---

## Slide 2 — Como funciona o cadeado

O problema apresenta um cadeado com **4 rodas independentes**, e cada roda possui os dígitos de `0` a `9`.

- Cada movimento em uma roda custa exatamente **1 rolagem**.
- As rodas são **circulares**.
- Ir de `0` para `9` custa apenas **1 rolagem**, e não 9.
- O cadeado sempre começa no estado inicial `0000`.

```text
Estado inicial: 0000

0 0 0 0
```

### Rotação circular

```text
0 -> 9 custa 1 rolagem, não 9.
```

---

## Slide 3 — O papel do botão `JUMP`

O botão **`JUMP`** é uma regra importante do problema.

- `JUMP` teleporta de graça para uma chave **já destravada**.
- `JUMP` nunca permite retornar ao estado inicial `0000`.
- Após a primeira chave, podemos partir de qualquer chave já aberta.
- O objetivo é escolher uma sequência com **menor custo total**.

```text
0000 --custo real--> K1

K1 --custo--> K2
K2 --JUMP gratuito--> K1
K1 --custo--> K3

JUMP para 0000: não permitido
```

### Legenda

- **Custo real:** rolagem paga entre estados.
- **JUMP:** deslocamento gratuito para uma chave já destravada.
- **X para `0000`:** não é permitido voltar ao estado inicial.

---

## Slide 4 — Modelagem como grafo

O problema pode ser modelado como um grafo ponderado.

| Elemento do problema | Elemento no grafo |
|---|---|
| Cada chave de 4 dígitos | **Vértice** |
| Trocar uma chave por outra | **Aresta** |
| Número mínimo de rolagens entre duas chaves | **Peso** |

### Grafo completo

Como qualquer par de chaves pode ser comparado, o grafo entre as chaves é **completo**.

Isso significa que existe uma aresta entre todos os pares de chaves.

---

## Slide 5 — Cálculo do peso

Para calcular o peso entre duas chaves, analisamos cada dígito separadamente.

- Para cada dígito, calcula-se a menor distância circular.
- O peso da aresta é a soma das 4 distâncias.
- A fórmula evita escolher o caminho maior na roda circular.
- Exemplo: `0 -> 9` custa `1`, e não `9`.

### Fórmula

```text
dist(x, y) = min(|x - y|, 10 - |x - y|)
```

### Exemplo: `1234 -> 5678`

| Dígito | x | y | x - y | 10 - x - y | min |
|---|---:|---:|---:|---:|---:|
| 1º | 1 | 5 | 4 | 6 | 4 |
| 2º | 2 | 6 | 4 | 6 | 4 |
| 3º | 3 | 7 | 4 | 6 | 4 |
| 4º | 4 | 8 | 4 | 6 | 4 |

```text
Peso total = 16 rolagens
```

---

## Slide 6 — Ideia principal: `0000` é folha

O estado `0000` precisa ser tratado com cuidado.

- `0000` é apenas o estado inicial, não uma chave destravada.
- Após sair de `0000`, o `JUMP` nunca permite voltar a ele.
- Logo, `0000` participa somente da primeira rolagem.
- Erro comum: usar `0000` como vértice livre na MST.

### Errado: `0000` como vértice livre

```text
      0000
     / |  \
   K1  K2  K3
```

Nesse caso, o algoritmo poderia usar `0000` como intermediário, mas isso não é permitido.

### Correto: `0000` como folha

```text
0000 --entrada inicial--> K1
                           |
                          K2
                           |
                          K3
```

```text
0000 entra só uma vez; a MST liga as chaves.
```

---

## Slide 7 — Estratégia da solução

A solução é dividida em duas partes independentes.

### Parte 1 — Menor rolagem inicial

Escolhe-se a chave que está mais perto de `0000`. Esse é o custo da primeira rolagem.

```text
min dist(0000, Ki)
```

### Parte 2 — MST entre as chaves

Conecta todas as chaves com o menor custo total possível, sem usar o vértice `0000`.

```text
MST(chaves)
```

### Resposta final

```text
Resposta = MST(chaves) + menor rolagem inicial
```

---

## Slide 8 — Kruskal + Union-Find

Para calcular a MST entre as chaves, usamos **Kruskal + Union-Find**.

### Passos do algoritmo

1. **Gerar arestas**  
   Lista todos os pares de chaves possíveis.

2. **Ordenar por peso**  
   Ordena as arestas em ordem crescente, das mais baratas para as mais caras.

3. **Union-Find**  
   Verifica se os vértices estão em componentes distintos.

4. **Aceitar aresta**  
   Se a aresta não fecha ciclo, ela entra na MST.

5. **Parar em `N - 1` arestas**  
   Esse é o total necessário para conectar todas as chaves.

### Union-Find em ação

```text
Antes: 4 componentes

K1    K2    K3    K4
```

```text
Depois: 1 componente conectado

K1 -- K2 -- K3 -- K4
```

Se uma aresta conecta componentes distintos, ela entra na MST.  
Se conecta vértices que já estão no mesmo componente, ela é descartada porque formaria ciclo.

---

## Slide 9 — Complexidade e casos especiais

### Complexidade

| Item | Complexidade | Motivo |
|---|---:|---|
| Arestas | `O(N²)` | Grafo completo com `N` vértices |
| Tempo | `O(N² log N)` | Ordenação das arestas domina |
| Limite | `N ≤ 500` | Solução eficiente para o problema |

A memória usada também é `O(N²)`, porque armazenamos todas as arestas do grafo completo.

### Casos especiais tratados

| Caso | Tratamento |
|---|---|
| `N = 1` | A resposta é só a distância até a única chave |
| Chaves repetidas | Geram arestas de peso zero |
| Chave igual a `0000` | A primeira rolagem custa zero |
| Pesos iguais | Kruskal aceita qualquer ordem entre eles |

---

## Slide 10 — Resultado e conclusão

### Submissão aceita na UVA

A solução foi testada com os casos oficiais do problema e obteve o resultado esperado.

### Saídas oficiais

| Teste | Saída |
|---|---:|
| Teste 1 | 16 |
| Teste 2 | 20 |
| Teste 3 | 26 |
| Teste 4 | 17 |

### Ideia central

1. **Grafo completo**  
   Modelar cada chave como vértice e cada par como aresta.

2. **`0000` como folha**  
   Usar `0000` somente na primeira rolagem.

3. **MST com Kruskal**  
   Ordenar arestas e usar Union-Find para evitar ciclos.

## Obrigado!

**Grupo F — UVA 1235**
