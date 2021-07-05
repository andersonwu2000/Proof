from syntax import *
import architecture

class alpha(syntax):
    """ 以空白分隔 token
    EBNF 文法 (依優先級)
    declarative = "let" proposition { "then" proposition } 
                | "if" proposition "then" proposition { "then" proposition }
                | proposition
    proposition = quantifier [ "\n" ]
    quantifier  = [ quan_operator obj [ "∈" obj ] ":" ] operation_2
    operation_2 = operation_l { bin_operator operation_l }
    operation_l = { operator_l } operation_r
    operation_r = primary { operator_r }
    primary     = obj | "(" declarative ")"
    obj         = ? all visible characters ?

    quan_operator = "∀" | "∃"
    bin_operator  = "∧" | "V" | "⇒" | "⇔" | "∈" | "="
    operator_l    = "¬"
    operator_r    = ε
    """
    
    def __init__(self, content:str) -> None:
        """ 為敘述建立抽象語法樹 """
        self.alphabet = {"let", "if", "then", "\n", ":", "(", ")"}
        self.quan_operator = {"∀", "∃"}
        self.alphabet.update(self.quan_operator)
        self.bin_operator = {"∧", "V", "⇒", "⇔", "∈", "="}
        self.alphabet.update(self.bin_operator)
        self.operator_l = {"¬"}
        self.alphabet.update(self.operator_l)
        self.operator_r = set()
        self.alphabet.update(self.operator_r)

        self.content   = self.tokennize(content)
        self.structure = self.parser()

    # Logic check
    def logical(self, area) -> bool:
        """ 檢查敘述對於該環境是否正確 """
        self.area = architecture.area(area)
        for narrative in self.structure:
            if narrative.kind == "let":
                self.area.add(narrative.args[0])
            elif narrative.kind == "then":
                pass
            else:
                pass
        # for narrative in proof:
        #     for thm in self.related:
        #         if proof.logical(self):
        #             break
        #     else:
        #         return False
        # return True
        return True

    def area_analysis(self) -> bool:
        pass

    # Tokennize
    def tokennize(self, content:str) -> list:
        """ 標記化 """
        content = content.replace("\n", " \n ").split(" ")
        content = [i for i in content if not i==""] + [None]
        if content[0] == "\n":
            content.pop(0)
        return content

    def check(self, check_set:set):
        """ 判斷 token 是否相符 """
        if self.content[self.idx] in check_set:
            self.idx += 1
            return True
        else:
            return False

    def claim(self, check_set:set):
        """ 若 token 不相符，則語法有誤 """
        token = self.content[self.idx]
        if token not in check_set:
            print(self.content[self.idx:self.idx+3])
            raise SyntaxError(f"Asked to be in {check_set}, but got '{token}'")
        else:
            self.idx += 1

    # Parsing
    def parser(self) -> None:
        """ 生成抽象語法樹 """
        self.idx = 0
        structure = []
        while self.content[self.idx] not in {None}:
            structure += [self.declarative()]
        return structure

    def declarative(self) -> Node:
        if self.check({"let"}):
            node = Node(self.content[self.idx-1], self.proposition())
        elif self.check({"if"}):
            node = Node(self.content[self.idx-1], self.proposition())
            self.claim({"then"})
            node = Node(self.content[self.idx-1], node, self.proposition())
        else:
            return self.proposition()
        while self.check({"then"}):
            node = Node(self.content[self.idx-1], node, self.proposition())
        return node
    
    def proposition(self) -> Node:
        node = self.quantifier()
        self.check({"\n"})
        return node
    
    def quantifier(self) -> Node:
        if self.check(self.quan_operator):
            kind = self.content[self.idx-1]
            node = self.obj()
            if self.check({"∈"}):
                node = Node(self.content[self.idx-1], node, self.obj())
            self.claim({":"})
            node = Node(kind, node, self.operation_2())
        else:
            node = self.operation_2()
        return node
    
    def operation_2(self) -> Node:
        node = self.operation_l()
        while self.check(self.bin_operator):
            node = Node(self.content[self.idx-1], node, self.operation_l())
        return node
    
    def operation_l(self) -> Node:
        if self.check(self.operator_l):
            node = Node(self.content[self.idx-1], self.operation_l())
        else:
            node = self.operation_r()
        return node
    
    def operation_r(self) -> Node:
        node = self.primary()
        while self.check(self.operator_r):
            node = Node(self.content[self.idx-1], node)
        return node
    
    def primary(self) -> Node:
        if self.check({"("}):
            node = self.declarative()
            self.claim({")"})
        else:
            node = self.obj()
        return node
    
    def obj(self) -> Node:
        self.idx += 1
        return Node(self.content[self.idx-1])

    # Auxiliary tools
    def representation_structure(self, structure=0, space=0):
        """ 顯示語法結構 """
        if structure == 0:
            print("-"*25)
            structure = self.structure
        for i in structure:
            print("    "*space, i.kind)
            self.representation_structure(i.args, space+1)

if __name__ == "__main__":
    # 範例

    proof = "∀ a ∈ A : ( ∃ b : ( if b ∈ A then a = b ) )"
    c = alpha(proof)
    c.representation_structure()

    proof = "¬ True ∧ ¬ ¬ ¬ True ∧ True"
    c = alpha(proof)
    c.representation_structure()

    proof = """
        let a ∈ A
        if a = b
        then a ∈ B
        then b ∈ A
        """
    c = alpha(proof)
    c.representation_structure()

    proof = """
        let a ∈ A
        if a = b
        then ( let b ∈ A then ¬ b
        then a ∈ A )
        then b ∈ A
        """
    c = alpha(proof)
    c.representation_structure()