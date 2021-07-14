
class Node:
    def __init__(self, kind=None, *args) -> None:
        """
        抽象語法樹的節點
        Variables
            self.args (list of Node): 節點下派生的節點
        """
        self.kind = kind
        self.args = list(args)

class syntax:
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

    def tokennize(self, content:str) -> list:
        """ 標記化 """
        return list(content)
    
    def parser(self) -> list:
        """ 生成抽象語法樹 """
        return []

    def logical(self, area) -> bool:
        """ 檢查敘述對於該環境是否正確 """
        return True