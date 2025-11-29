from math import ceil
from collections import deque

class BPlusNode:
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys = []        # lista de chaves
        self.children = []    # se leaf: valores; se interno: filhos (BPlusNode)
        self.next = None      # para folhas: ponteiro para próxima folha

    def __repr__(self):
        if self.leaf:
            return f"Leaf(keys={self.keys})"
        else:
            return f"Int(keys={self.keys})"

class BPlusTree:
    def __init__(self, order=4):
        if order < 3:
            raise ValueError("order mínimo é 3")
        self.order = order
        self.root = BPlusNode(leaf=True)

    def _find_leaf(self, key, path=None):
        """Retorna folha onde key deveria estar. Se path fornecido (lista), preenche com o caminho de nós."""
        node = self.root
        if path is not None:
            path.clear()
            path.append(node)
        while not node.leaf:
            # encontrar filho apropriado
            i = 0
            while i < len(node.keys) and key >= node.keys[i]:
                i += 1
            node = node.children[i]
            if path is not None:
                path.append(node)
        return node

    def insert(self, key, value=None):
        """Insere chave (com valor opcional). Se chave já existe, atualiza o valor na folha."""
        path = []
        leaf = self._find_leaf(key, path)

        # inserir ou atualizar na folha
        i = 0
        while i < len(leaf.keys) and leaf.keys[i] < key:
            i += 1
        if i < len(leaf.keys) and leaf.keys[i] == key:
            # atualiza valor
            leaf.children[i] = value
            return
        leaf.keys.insert(i, key)
        leaf.children.insert(i, value)

        # se excedeu capacidade, dividir
        if len(leaf.keys) > self.order - 1:
            self._split_leaf(leaf, path)

    def _split_leaf(self, leaf, path):
        mid = ceil(len(leaf.keys) / 2)
        new_leaf = BPlusNode(leaf=True)
        # mover metade superior para new_leaf
        new_leaf.keys = leaf.keys[mid:]
        new_leaf.children = leaf.children[mid:]
        leaf.keys = leaf.keys[:mid]
        leaf.children = leaf.children[:mid]

        # ajustar ponteiros folha
        new_leaf.next = leaf.next
        leaf.next = new_leaf

        # promover chave (primeira chave do new_leaf) para o pai
        promote_key = new_leaf.keys[0]

        # se leaf era root -> novo root
        if leaf is self.root:
            new_root = BPlusNode(leaf=False)
            new_root.keys = [promote_key]
            new_root.children = [leaf, new_leaf]
            self.root = new_root
            return

        # senão localizar o pai no path (penúltimo elemento)
        # path contém a sequência root->...->leaf
        parent = path[-2]  # pai direto
        self._insert_into_parent(parent, promote_key, new_leaf, path[:-1])

    def _insert_into_parent(self, parent, key, right_node, path_to_parent):
        """
        Insere key e right_node no parent (path_to_parent é caminho até parent).
        Se necessário, divide o parent recursivamente.
        """
        # achar posição para inserir a chave
        i = 0
        while i < len(parent.keys) and key >= parent.keys[i]:
            i += 1
        parent.keys.insert(i, key)
        parent.children.insert(i + 1, right_node)

        # se overflow no parent
        if len(parent.children) > self.order:
            # dividir interno
            self._split_internal(parent, path_to_parent)

    def _split_internal(self, node, path_to_node):
        """
        Divide um nó interno que excedeu a capacidade.
        path_to_node é o caminho root->...->node (último elemento é node).
        """
        # encontrar índice de promoção
        mid_index = len(node.keys) // 2  # promove a chave do meio
        promote_key = node.keys[mid_index]

        # criar novo nó à direita
        new_node = BPlusNode(leaf=False)
        # left keeps keys[:mid_index], children[:mid_index+1]
        # right gets keys[mid_index+1:], children[mid_index+1:]
        new_node.keys = node.keys[mid_index+1:]
        new_node.children = node.children[mid_index+1:]

        # shrink original node (left)
        node.keys = node.keys[:mid_index]
        node.children = node.children[:mid_index+1]

        # se node era root -> novo root
        if node is self.root:
            new_root = BPlusNode(leaf=False)
            new_root.keys = [promote_key]
            new_root.children = [node, new_node]
            self.root = new_root
            return

        # senão inserir promote_key no pai
        # path_to_node tem root..parent..node; parent é último
        parent = path_to_node[-1]
        # inserir no parent: posição determinada por promote_key
        j = 0
        while j < len(parent.keys) and promote_key >= parent.keys[j]:
            j += 1
        parent.keys.insert(j, promote_key)
        parent.children.insert(j + 1, new_node)

        # se o parent agora overflow, dividir recursivamente
        # precisamos do caminho até parent; para isso, remover último (que era node) do path_to_node
        if len(parent.children) > self.order:
            # construir caminho até parent (path_to_node sem último)
            new_path_to_parent = path_to_node[:-1]
            # se new_path_to_parent vazio, parent é root
            self._split_internal(parent, new_path_to_parent)

    # VISUALIZAÇÕES ------------------------------------------------------

    def print_tree(self):
        """Imprime a árvore por níveis (BFS) mostrando as chaves de cada nó."""
        q = deque()
        q.append(self.root)
        level = 0
        while q:
            sz = len(q)
            print(f"Level {level}: ", end="")
            for _ in range(sz):
                node = q.popleft()
                if node.leaf:
                    print(f"[Leaf:{node.keys}]", end="  ")
                else:
                    print(f"[Int:{node.keys}]", end="  ")
                    for ch in node.children:
                        q.append(ch)
            print()
            level += 1
    
    def get_root(self):
        return self.root

    def print_leaves(self):
        """Imprime a lista ligada das folhas (em ordem)."""
        # ir até a folha mais à esquerda
        node = self.root
        while not node.leaf:
            node = node.children[0]
        # agora iterar pelas folhas usando next
        idx = 0
        while node:
            print(f"Leaf {idx}: keys={node.keys} values={node.children}")
            node = node.next
            idx += 1

    def find(self, key):
        """Retorna o valor associado à chave (ou None se não existir)."""
        leaf = self._find_leaf(key)
        for i, k in enumerate(leaf.keys):
            if k == key:
                return leaf.children[i]
        return None
    
    def search_index(self, key):
        #Retorna (found, value) value = endereço no arquivo referente à chave Se não encontrado, retorna o último offset <= key.
        leaf = self._find_leaf(key)
        last_value = None

        for i, k in enumerate(leaf.keys):
            last_value = leaf.children[i]   # children[] CONTÉM offsets nas folhas
            if k == key:
                # chave encontrada: retorna offset exato
                return True, leaf.children[i]

        # não achou: retorna último offset menor/igual à key
        return False, last_value