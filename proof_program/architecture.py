import syntax

class area:
    def __init__(self, bases=set(), assumptions=set(), grammar=syntax.syntax) -> None:
        """
        Parameters
            bases      (set of area): 該環境的基礎環境
            assumptions (set of str): 該環境的假設
            grammar  (syntax.syntax): 該環境的語法
        Variables
            self.theorems (set of syntax): 該環境的所有定理
            self.bases      (set of area): 該環境的基礎環境
            self.related    (set of area): 該環境的相關定理
        """
        self.grammar  = grammar
        self.theorems = set()
        self.bases    = set()
        self.related  = set()

        self.add_thm(self.theorems, assumptions)
        self.add_thm(self.related, assumptions)
        self.add_base(bases)
        for base in self.bases:
            self.add_thm(self.related, base.related)

    def __call__(self, proof) -> bool:
        """ 
        檢查敘述對於該環境是否正確
        """
        proof = self.grammar(proof)
        return proof.logical(self)

    def add_base(self, bases) -> None:
        """ 對該環境添加新的基礎 """
        if type(bases) is area:
            self.bases.add(bases)
        elif type(bases) in {list, tuple, set}:
            for base in bases:
                self.add_base(base)
        else:
            raise TypeError

    def add_thm(self, obj, theorems) -> None:
        """ 對該環境添加新的定理 """
        if type(theorems) in {str, syntax.Node}:
            obj.add(self.grammar(theorems))
        elif type(theorems) is self.grammar:
            obj.add(theorems)
        elif type(theorems) in {list, tuple, set}:
            for thm in theorems:
                self.add_thm(obj, thm)
        else:
            raise TypeError

the_basic = area()