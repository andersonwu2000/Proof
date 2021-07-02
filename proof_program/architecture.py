import syntax

class area:
    def __init__(self, bases=set(), assumptions=set()) -> None:
        """
        Parameters
            bases      (set of area): 該環境的基礎環境
            assumptions (set of str): 該環境的假設
        Variables
            self.theorems  (set of AST): 該環境的所有定理
            self.bases    (set of area): 該環境的基礎環境
            self.related (list of area): 該環境的相關定理
        """
        self.theorems = set()
        self.add(assumptions)

        if type(bases) is area:
            self.bases = {bases}
        elif type(bases) in {list, tuple, set}:
            self.bases = set(bases)
        else:
            raise TypeError

        self.related = {thm for base in self.bases for thm in base.related}
        self.related = list(self.theorems) + list(self.related)

    def __call__(self, proof, sep="\n") -> bool:
        """ 
        檢查證明對於該環境是否正確
        Parameters
            proof (str): 證明
            sep   (str): 語句的分隔符
        """
        proof = proof.split(sep)
        proof = [syntax.alpha(narrative) for narrative in proof]
        for narrative in proof:
            for thm in self.related:
                if narrative.logical(thm):
                    break
            else:
                return False
        return True

    def add(self, theorems) -> None:
        """ 對該環境添加新的定理 """
        if type(theorems) is str:
            tmp = {syntax.alpha(theorems)}
        elif type(theorems) in {list, tuple, set}:
            tmp = {syntax.alpha(thm) for thm in theorems}
        else:
            raise TypeError
        self.theorems = self.theorems.union(tmp)

the_basic = area()

# class area:
#     def __init__(self, bases=set()) -> None:
#         if type(bases) is area:
#             self.bases = {bases}
#         elif type(bases) in {list, tuple, set}:
#             self.bases = set(bases)
#         self.l = [self] + list(self.bases)