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
            self.related   (list of area): 該環境的相關定理
        """
        self.grammar = grammar
        self.theorems = set()
        self.add(assumptions)

        if type(bases) is area:
            self.bases = {bases}
        elif type(bases) in {list, tuple, set}:
            self.bases = set(bases)
        else:
            raise TypeError

        self.related = {thm for base in self.bases for thm in base.related}
        self.related.update(self.theorems)
        self.related = list(self.related)

    def __call__(self, proof) -> bool:
        """ 
        檢查敘述對於該環境是否正確
        """
        proof = self.grammar(proof)
        return proof.logical(self)

    def add(self, theorems) -> None:
        """ 對該環境添加新的定理 """
        if type(theorems) is str:
            tmp = {self.grammar(theorems)}
        elif type(theorems) in {list, tuple, set}:
            tmp = {self.grammar(thm) for thm in theorems}
        else:
            raise TypeError
        self.theorems = self.theorems.union(tmp)

the_basic = area()