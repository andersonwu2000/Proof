
class Node:
    def __init__(self, kind="", *args) -> None:
        self.kind = kind
        self.args = args

class syntax:
    def __init__(self, content:str) -> None:
        """ 為敘述建立抽象語法樹 """
        self.content = self.tokennize(content)
        self.structure = self.parser()

    def tokennize(self, content:str) -> list:
        """ 標記化 """
        return list(content)
    
    def parser(self) -> list:
        """ 生成抽象語法樹 """
        return []

    def logical(self, area) -> bool:
        """ 檢查敘述對於該環境是否正確 """
        return True

class alpha(syntax):
    """ 以空白分隔 token
    EBNF 文法 (依優先級)
    narrative    = ("let" | "if")? proposition ("then" proposition)*
    proposition  = quantifier "\n"?
    quantifier   = ("∀" object "∈" object ":" | "∃" object "∈" object ":" )? operation_2
    operation_2  = operation_l (bin_operator operation_l)*
    operation_l  = operator_l* operation_r
    operation_r  = primary operator_r*
    primary      = object | "(" quantifier ")"
    bin_operator = "∧" | "V" | "⇒" | "⇔" | "∈" | "="
    operator_l   = "¬"
    operator_r   = ε
    """
    def __init__(self, content:str) -> None:
        """ 為敘述建立抽象語法樹 """
        self.bin_operator = {"∧", "V", "⇒", "⇔", "∈", "="}
        self.operator_l = {"¬"}
        self.operator_r = set()
        self.alphabet = {"let", "if", "then", "\n", "∀", "∃", ":", "(", ")"}
        self.alphabet = self.alphabet.union(self.bin_operator)
        self.alphabet = self.alphabet.union(self.operator_l).union(self.operator_r)

        self.content = self.tokennize(content)
        self.structure = self.parser()

    # Tokennize
    def tokennize(self, content:str) -> list:
        """ 標記化 """
        content = content.replace("\n", " \n ").split(" ")
        content = [i for i in content if not i==""] + ["EOF"]
        if content[0] == "\n":
            content.pop(0)
        return content

    # Parsing
    def parser(self) -> None:
        """ 生成抽象語法樹 """
        self.idx = 0
        structure = []
        while self.content[self.idx] not in {"EOF"}:
            structure += [self.narrative()]
        return structure

    def narrative(self) -> Node:
        if self.content[self.idx] in {"let", "if"}:
            self.idx += 1
            node = Node(self.content[self.idx-1], self.proposition())
        else:
            node = self.proposition()
        while self.content[self.idx] in {"then"}:
            self.idx += 1
            node = Node(self.content[self.idx-1], node, self.proposition())
        return node
    
    def proposition(self) -> Node:
        node = self.quantifier()
        if self.content[self.idx] in {"\n"}:
            self.idx += 1
        return node
    
    def quantifier(self) -> Node:
        if self.content[self.idx] in {"∀", "∃"}:
            form = [["∀", "∈", ":"], ["∃", "∈", ":"]] 
            if self.content[self.idx:self.idx+5:2] not in form:
                raise SyntaxError("not '∈' or ':'")

            self.idx += 5
            object_1 = Node(self.content[self.idx-4])
            object_2 = Node(self.content[self.idx-2])
            node = Node(self.content[self.idx-3], object_1, object_2)
            node = Node(self.content[self.idx-5], node, self.operation_2nd())
        else:
            node = self.operation_2nd()
        return node
    
    def operation_2nd(self) -> Node:
        node = self.operation_l()
        while self.content[self.idx] in self.bin_operator:
            self.idx += 1
            node = Node(self.content[self.idx-1], node, self.operation_l())
        return node
    
    def operation_l(self) -> Node:
        if self.content[self.idx] in self.operator_l:
            self.idx += 1
            node = Node(self.content[self.idx-1], self.operation_l())
        else:
            node = self.operation_r()
        return node
    
    def operation_r(self) -> Node:
        node = self.primary()
        while self.content[self.idx] in self.operator_r:
            self.idx += 1
            node = Node(self.content[self.idx-1], node)
        return node
    
    def primary(self) -> Node:
        if self.content[self.idx] in {"("}:
            self.idx += 1
            node = Node(self.content[self.idx-1], self.quantifier())
            if self.content[self.idx] not in {")"}:
                raise SyntaxError("not ')'")
            self.idx += 1
        else:
            self.idx += 1
            node = Node(self.content[self.idx-1])
        return node

    # Logic check
    def logical(self, area) -> bool:
        """ 檢查敘述對於該環境是否正確 """
        pass
        return True

proof = '∀ a ∈ A : a = b'
c = alpha(proof)
print(c.structure[0].kind)
print(c.structure[0].args)