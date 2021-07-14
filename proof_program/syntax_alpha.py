from syntax import *
import architecture

class alpha(syntax):
    """
    EBNF 文法 (依優先級)
    (* 空白和換行用於分隔 token *)
    declarative = quantifier "."
    proposition = [ "suppose" ] quantifier
    quantifier  = [ quan_operator obj ":" ] operation_2
    operation_2 = operation_l { bin_operator operation_l }
    operation_l = { l_operator } operation_r
    operation_r = primary { r_operator }
    primary     = obj | "(" quantifier ")"
    obj         = ? all visible characters ?

    quan_operator = "∀" | "∃"
    bin_operator  = "∧" | "V" | "⇒" | "⇔" | "∈" | "="
    l_operator    = "¬"
    r_operator    = ε
    TODO 加入 'let', 'if', 'then', 'since', 'by' 等
    TODO 函數、語法定義、集合定義、反證法的支持
    """
    alphabet = {"suppose", ".", ":", "(", ")"}
    quan_operator = {"∀", "∃"}
    alphabet.update(quan_operator)
    bin_operator = {"∧", "V", "⇒", "⇔", "∈", "="}
    alphabet.update(bin_operator)
    l_operator = {"¬"}
    alphabet.update(l_operator)
    r_operator = set()
    alphabet.update(r_operator)
    
    def __init__(self, narrative) -> None:
        """
        為該敘述依序建立抽象語法樹
        Parameters
            narrative (str / Node): 使用本語法表達的一個敘述
        Variables
            self.structure (list of Node): 與該敘述語法結構依序對應的抽象語法樹
            self.obj_dict (dict of Node.kind:Node): 含有所有物件的字典
        """
        if type(narrative) is str:
            self.obj_dict  = {}
            self.narrative = self.tokennize(narrative)
            self.structure = self.parser()
        elif type(narrative) is Node:
            self.structure = [narrative]
            self.obj_dict  = self.get_obj()
        else:
            raise TypeError

    # Logic check
    def logical(self, environment) -> bool:
        """ 驗證該敘述於對應環境是否正確 """
        self.environment = architecture.environment(environment, grammar=alpha)
        for node in self.structure:
            result = self.proposition_analysis(node)
            if result is not True:
                return result
        return True

    def proposition_analysis(self, node:Node) -> bool:
        """ proposition 的驗證 """
        if node.kind == "suppose":
            self.environment.add_thm(node.args[0])
            return True
        else:
            if result := self.node_analysis(node):
                self.environment.add_thm(node)
            return result

    def node_analysis(self, node:Node) -> bool:
        result = self.thm_analysis_method(node)
        if result is not None:
            return result
        if node.kind == "∃":
            replace, node.args[0].kind = node.args[0].kind, None
            result = self.node_analysis(node.args[1])
            node.args[0].kind = replace
        args = [self.node_analysis(i) for i in node.args]
        if None in args:
            return
        elif ValueError in args:
            return ValueError
        if node.kind == "¬":
            result = not args[0]
        elif node.kind == "∧":
            result = args[0] and args[1]
        elif node.kind == "V":
            result = args[0] or args[1]
        elif node.kind == "⇒":
            result = not args[0] or args[1]
        elif node.kind == "⇔":
            result = args[0] == args[1]
        return result

    def thm_analysis_method(self, node:Node) -> bool:
        """ 驗證環境中所有定理 """
        result_list = []
        for thm in self.environment.get_thm():
            result = self.thm_analysis(thm.structure[0], node)
            if result is True:
                self.environment.add_thm(node)
            result_list.append(result)
        if ValueError in result_list:
            return ValueError  # 矛盾
        elif True in result_list and False in result_list:
            return ValueError
        elif True in result_list:
            return True
        elif False in result_list:
            return False
        else:
            return None  # 不足以證明或證偽

    def thm_analysis(self, thm:Node, node:Node) -> bool:
        result = None
        if thm.kind == node.kind or None in {thm.kind, node.kind}:
            for t, n in zip(thm.args, node.args):
                if self.thm_analysis(t, n) is not True:
                    break
            else:
                return True
        if thm.kind == "∀":
            replace, thm.args[0].kind = thm.args[0].kind, None
            result = self.thm_analysis(thm.args[1], node)
            thm.args[0].kind = replace
            if result:
                return result
        if thm.kind == "¬":
            result = self.thm_analysis(thm.args[0], node)
            if result not in {None, ValueError}:
                return not result
            else:
                return result
        elif thm.kind == "∧":
            args = [self.thm_analysis(i, node) for i in thm.args]
            if True in args and False in args:
                result = ValueError
            else:
                result = args[0] or args[1]
        elif thm.kind == "⇒":
            if self.thm_analysis_method(thm.args[0]):
                return self.thm_analysis(thm.args[1], node)
        return result

    # Tokennize
    def tokennize(self, narrative:str) -> list:
        """ 標記化 """
        narrative = narrative.replace("\n", " ").split(" ")
        narrative = [i for i in narrative if not i==""] + [None]
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
        TODO 應用關於 EBNF 的編譯器編譯程式替代
        """
        self.idx = 0
        structure = []
        while self.narrative[self.idx] not in {None}:
            structure.append(self.declarative())
        return structure

    def declarative(self) -> Node:
        node = self.proposition()
        self.claim({"."})
        return node
    
    def proposition(self) -> Node:
        if self.check({"suppose"}):
            node = Node(self.narrative[self.idx-1], self.quantifier())
        else:
            node = self.quantifier()
        return node
    
    def quantifier(self) -> Node:
        if self.check(alpha.quan_operator):
            node = self.obj()
            self.claim({":"})
            node = Node(self.narrative[self.idx-3], node, self.operation_2())
        else:
            node = self.operation_2()
        return node
    
    def operation_2(self) -> Node:
        node = self.operation_l()
        while self.check(alpha.bin_operator):
            node = Node(self.narrative[self.idx-1], node, self.operation_l())
        return node
    
    def operation_l(self) -> Node:
        if self.check(alpha.l_operator):
            node = Node(self.narrative[self.idx-1], self.operation_l())
        else:
            node = self.operation_r()
        return node
    
    def operation_r(self) -> Node:
        node = self.primary()
        while self.check(alpha.r_operator):
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
        kind = self.narrative[self.idx-1]
        if kind not in self.obj_dict:
            self.obj_dict[kind] = Node(kind)
        return self.obj_dict[kind]

    # Auxiliary tools
    def get_obj(self, structure:list=None) -> dict:
        """ 取得所有 obj """
        obj_dict = {}
        if structure is None:
            structure = self.structure
        for i in structure:
            obj_dict[i.kind] = i
            obj_dict.update(self.get_obj(i.args))
        return obj_dict

    def representation(self, structure:list=None, space=0) -> None:
        """ 表示該敘述的語法結構 """
        if structure is None:
            structure = self.structure
        if space == 0:
            print("-"*25)
        for i in structure:
            print("    "*space, end="")
            print(i.kind)
            self.representation(i.args, space+1)

if __name__ == "__main__":
    # 範例

    proof = "∀ a : ( ∃ b : ( ( a ∈ A ) ⇒ ( a = b ) ) ) ."
    c = alpha(proof)
    c.representation()

    proof = "¬ True ∧ ¬ ¬ ¬ True ∧ True ."
    c = alpha(proof)
    c.representation()

    proof = """ 
        a ∈ A .
        ( a = b )
        ⇒ ( a ∈ B )
        ⇒ ( b ∈ A ) .
        """
    c = alpha(proof)
    c.representation()
    c.representation(c.structure[1].args)
    print(c.obj_dict)