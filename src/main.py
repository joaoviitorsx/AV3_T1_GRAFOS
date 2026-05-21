#!/usr/bin/env python3
import sys

START = (0, 0, 0, 0)

DIGIT_DIST = [[min(abs(x - y), 10 - abs(x - y)) for y in range(10)]
              for x in range(10)]


def roll_cost(a, b):
    return (DIGIT_DIST[a[0]][b[0]] + DIGIT_DIST[a[1]][b[1]]
            + DIGIT_DIST[a[2]][b[2]] + DIGIT_DIST[a[3]][b[3]])


class UnionFind:

    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.count = n

    def find(self, p):
        while self.parent[p] != p:
            self.parent[p] = self.parent[self.parent[p]]
            p = self.parent[p]
        return p

    def connected(self, p, q):
        return self.find(p) == self.find(q)

    def union(self, p, q):
        rp, rq = self.find(p), self.find(q)
        if rp == rq:
            return False
        if self.size[rp] < self.size[rq]:
            rp, rq = rq, rp
        self.parent[rq] = rp
        self.size[rp] += self.size[rq]
        self.count -= 1
        return True


def kruskal_mst(n, edges):
    edges.sort()
    uf = UnionFind(n)
    weight = 0
    chosen = 0
    for w, u, v in edges:
        if uf.union(u, v):
            weight += w
            chosen += 1
            if chosen == n - 1:
                break
    return weight


def prim_mst(nodes):
    n = len(nodes)
    if n <= 1:
        return 0
    in_mst = [False] * n
    dist = [1 << 30] * n
    dist[0] = 0
    weight = 0
    for _ in range(n):
        u = -1
        for v in range(n):
            if not in_mst[v] and (u == -1 or dist[v] < dist[u]):
                u = v
        in_mst[u] = True
        weight += dist[u]
        for v in range(n):
            if not in_mst[v]:
                c = roll_cost(nodes[u], nodes[v])
                if c < dist[v]:
                    dist[v] = c
    return weight


def solve_case(keys):
    nodes = [tuple(int(c) for c in k) for k in keys]
    n = len(nodes)
    edges = []
    for i in range(n):
        node_i = nodes[i]
        for j in range(i + 1, n):
            edges.append((roll_cost(node_i, nodes[j]), i, j))
    mst_weight = kruskal_mst(n, edges)
    entry = min(roll_cost(START, node) for node in nodes)
    return mst_weight + entry


def main():
    data = sys.stdin.read().split()
    if not data:
        return
    idx = 0
    t = int(data[idx]); idx += 1
    answers = []
    for _ in range(t):
        n = int(data[idx]); idx += 1
        keys = data[idx:idx + n]; idx += n
        answers.append(str(solve_case(keys)))
    sys.stdout.write("\n".join(answers) + "\n")


_SAMPLE_INPUT = """4
2 1155 2211
3 1111 1155 5511
3 1234 5678 9090
4 2145 0213 9113 8113"""
_SAMPLE_OUTPUT = ["16", "20", "26", "17"]


def run_tests():
    tokens = _SAMPLE_INPUT.split()
    idx = 0
    t = int(tokens[idx]); idx += 1
    all_ok = True
    for case in range(t):
        n = int(tokens[idx]); idx += 1
        keys = tokens[idx:idx + n]; idx += n
        nodes = [tuple(int(c) for c in k) for k in keys]
        got = solve_case(keys)
        prim = prim_mst(nodes) + min(roll_cost(START, x) for x in nodes)
        expected = int(_SAMPLE_OUTPUT[case])
        ok = (got == expected == prim)
        all_ok = all_ok and ok
        print("Caso %d  esperado=%-3d  kruskal=%-3d  prim=%-3d  [%s]"
              % (case + 1, expected, got, prim, "OK" if ok else "ERRO"))
    print("-> " + ("TODOS OS CASOS PASSARAM" if all_ok else "FALHOU"))
    return all_ok


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        sys.exit(0 if run_tests() else 1)
    main()
