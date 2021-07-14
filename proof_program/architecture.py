import syntax

class environment:
    def __init__(self, bases=set(), assumptions=set(), grammar=syntax.syntax) -> None:
        """
        Parameters
            bases      (set of environment): 該環境的基礎環境
            assumptions (set of str): 該環境的假設
            grammar  (syntax.syntax): 該環境的語法
        Variables
            self.theorems (set of syntax): 該環境的所有定理
            self.bases      (set of environment): 該環境的基礎環境
        """
        self.grammar   = grammar
        self.theorems  = set()
        self.bases     = set()
        self.bases_thm = set()

        self.add_thm(assumptions)
        self.add_base(bases)

        for base in self.bases:
            self.bases_thm.update(base.bases_thm)
            self.bases_thm.update(base.theorems)

    def __call__(self, proof) -> bool:
        """ 檢查敘述對於該環境是否正確 """
        proof = self.grammar(proof)
        return proof.logical(self)

    def get_thm(self) -> list:
        """ 取得該環境的所有相關定理 """
        return list(self.theorems) + list(self.bases_thm)

    def add_base(self, bases) -> None:
        """ 對該環境添加新的基礎 """
        if type(bases) is environment:
            self.bases.add(bases)
        elif type(bases) in {list, tuple, set}:
            for base in bases:
                self.add_base(base)
        else:
            raise TypeError

    def add_thm(self, theorems) -> None:
        """ 對該環境添加新的定理 """
        if type(theorems) in {str, syntax.Node}:
            self.theorems.add(self.grammar(theorems))
        elif type(theorems) is self.grammar:
            self.theorems.add(theorems)
        elif type(theorems) in {list, tuple, set}:
            for thm in theorems:
                self.add_thm(thm)
        else:
            raise TypeError

the_basic = environment()