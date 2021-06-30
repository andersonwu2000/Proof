
class area:
    def __init__(self, bases=set(), axioms=set()) -> None:
        """
        Parameters
            bases (set of areas): 該 area 的基礎 area 
            axioms  (set of str): 該 area 的所有公理或基本假設
        Variables
            self.theorems (dict of str&AST): 該 area 的所有定理
            self.bases       (set of areas): 該 area 的基礎 area 
            self.ancestor    (set of areas): 該 area 的所有基本 area 
        """
        self.theorems = self.syntax_analysis(axioms)
        if type(bases) is area:
            self.bases = {bases}
        elif type(bases) in {list, tuple, set}:
            self.bases = set(bases)
        else:
            raise TypeError
        self.ancestor = self.search_bases()
    
    def __call__(self, content:str, check_bases=True) -> bool:
        """ 檢查敘述對於該 area 是否正確 """
        # 對該 area 的所有定理進行檢查
        for thm in self.theorems:
            if self.logical(thm, content):
                return True
        if not check_bases:
            return False
        # 對所有基本 area 的定理進行檢查
        for bases in self.ancestor:
            if bases(content, False):
                return True
        return False

    # def add(self, theorems) -> dict:
    #     """ 對該 area 添加新的定理 """
    #     if type(theorems) is str:
    #         self.theorems.add(theorems)
    #     elif type(theorems) in {list, tuple, set}:
    #         self.theorems.update(theorems)

    def search_bases(self) -> None:
        """ 收集所有基本 area  """
        ancestor = self.bases
        for base in self.bases:
            ancestor = ancestor.union(base.search_bases())
        return ancestor

    def logical(self, theorem:str, content:str) -> bool:
        """ 檢查敘述對於該定理是否正確 """
        pass
        return True

    def syntax_analysis(self, theorems) -> dict:
        """ 為定理建立抽象語法樹 """
        if type(theorems) is str:
            pass
        elif type(theorems) in {list, tuple, set}:
            pass

the_basic = area()

# 字母表和語法
#  let P
#  if P1 ⇒ P2
#  a ∈ b
## a V b
#! a ∧ b
#! ¬ a
## a ⇔ b
## ∀ a ∈ b : P(a)
## ∃ a ∈ b : P(a)
#! a = b
#  ( a ) 
#  a , b