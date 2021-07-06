from syntax import *
import architecture

class alpha(syntax):
    """
    EBNF 文法 (依優先級)
    declarative = "let" proposition { "then" proposition } 
                | "if" proposition "then" proposition { "then" proposition }
                | proposition
    proposition = quantifier [ "\n" ]
    quantifier  = [ quan_operator obj [ "∈" obj ] ":" ] operation_2
    operation_2 = operation_l { bin_operator operation_l }
    operation_l = { operator_l } operation_r
    operation_r = primary { operator_r }
    primary     = obj | "(" quantifier ")"
    obj         = ? all visible characters ?

    quan_operator = "∀" | "∃"
    bin_operator  = "∧" | "V" | "⇒" | "⇔" | "∈" | "="
    operator_l    = "¬"
    operator_r    = ε
    """
    alphabet = {"let", "if", "then", "\n", ":", "(", ")"}
    quan_operator = {"∀", "∃"}
    alphabet.update(quan_operator)
    bin_operator = {"∧", "V", "⇒", "⇔", "∈", "="}
    alphabet.update(bin_operator)
    operator_l = {"¬"}
    alphabet.update(operator_l)
    operator_r = set()
    alphabet.update(operator_r)
    
    def __init__(self, narrative) -> None:
        """
        為該敘述依序建立抽象語法樹
        Parameters
            narrative (str / Node): 使用本語法表達的一個敘述
        Variables
            self.structure (list of Node): 與該敘述語法結構依序對應的抽象語法樹
        """
        if type(narrative) is str:
            self.narrative = self.tokennize(narrative)
            self.structure = self.parser()
        elif type(narrative) is Node:
            self.structure = [narrative]
        else:
            raise TypeError

    # Logic check
    def logical(self, area) -> bool:
        """ 驗證該敘述於對應環境是否正確 """
        self.area = architecture.area(area, grammar=alpha)
        for node in self.structure:
            if self.declarative_analysis(node) is False:
                return False
        return True

    def declarative_analysis(self, node:Node) -> bool:
        if node.kind == "let":
            self.area.add(node.args[0])
            for arg in node.args[1:]:
                if self.declarative_analysis(arg) is False:
                    return False
        elif node.kind == "if":
            self.area = architecture.area(self.area, node.args[0], alpha)
            for arg in node.args[1:]:
                if self.declarative_analysis(arg) is False:
                    return False
            self.area = self.area.bases.pop()
            # add args[0] => args[n] to area for all n>0
        elif node.kind == "then":
            if self.quantifier_analysis(node.args[1]):
                self.area.add(node.args[1])
                return True
            else:
                return False
        else:
            if self.quantifier_analysis(node):
                self.area.add(node)
                return True
            else:
                return False

    def quantifier_analysis(self, node:Node) -> bool:
        # I guess the most difficult place starts here
        pass

    # Tokennize
    def tokennize(self, narrative:str) -> list:
        """ 
        標記化
        token 以空白分隔
        """
        narrative = narrative.replace("\n", " \n ").split(" ")
        narrative = [i for i in narrative if not i==""] + [None]
        if narrative[0] == "\n":
            narrative.pop(0)
        return narrative

    def check(self, check_set:set):
        """ 判斷 token 是否相符 """
        if self.narrative[self.idx] in check_set:
            self.idx += 1
            return True
        else:
            return False

    def claim(self, check_set:set):
        """ 判斷 token 是否有闕失 """
        token = self.narrative[self.idx]
        if token not in check_set:
            raise SyntaxError(f"Asked to be in {check_set}, but got '{token}'")
        else:
            self.idx += 1

    # Parsing
    def parser(self) -> None:
        """ 
        生成抽象語法樹
        下列函數用於實現遞歸下降解析器
        """
        self.idx = 0
        structure = []
        while self.narrative[self.idx] not in {None}:
            structure.append(self.declarative())
        return structure

    def declarative(self) -> Node:
        if self.check({"let"}):
            node = Node(self.narrative[self.idx-1], self.proposition())
        elif self.check({"if"}):
            node = Node(self.narrative[self.idx-1], self.proposition())
            self.claim({"then"})
            node.args.append(Node(self.narrative[self.idx-1], self.proposition()))
        else:
            return self.proposition()
        while self.check({"then"}):
            node.args.append(Node(self.narrative[self.idx-1], self.proposition()))
        return node
    
    def proposition(self) -> Node:
        node = self.quantifier()
        self.check({"\n"})
        return node
    
    def quantifier(self) -> Node:
        if self.check(alpha.quan_operator):
            kind = self.narrative[self.idx-1]
            node = self.obj()
            if self.check({"∈"}):
                node = Node(self.narrative[self.idx-1], node, self.obj())
            self.claim({":"})
            node = Node(kind, node, self.operation_2())
        else:
            node = self.operation_2()
        return node
    
    def operation_2(self) -> Node:
        node = self.operation_l()
        while self.check(alpha.bin_operator):
            node = Node(self.narrative[self.idx-1], node, self.operation_l())
        return node
    
    def operation_l(self) -> Node:
        if self.check(alpha.operator_l):
            node = Node(self.narrative[self.idx-1], self.operation_l())
        else:
            node = self.operation_r()
        return node
    
    def operation_r(self) -> Node:
        node = self.primary()
        while self.check(alpha.operator_r):
            node = Node(self.narrative[self.idx-1], node)
        return node
    
    def primary(self) -> Node:
        if self.check({"("}):
            node = self.quantifier()
            self.claim({")"})
        else:
            node = self.obj()
        return node
    
    def obj(self) -> Node:
        self.idx += 1
        return Node(self.narrative[self.idx-1])

    # Auxiliary tools
    def representation_structure(self, structure=None, space=0):
        """ 表示該敘述的語法結構 """
        if structure is None:
            structure = self.structure
        if space == 0:
            print("-"*25)
        for i in structure:
            print("    "*space, i.kind)
            self.representation_structure(i.args, space+1)

if __name__ == "__main__":
    # 範例

    proof = "∀ a ∈ A : ( ∃ b : ( ( b ∈ A ) ⇒ ( a = b ) ) )"
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
    c.representation_structure(c.structure[1].args)