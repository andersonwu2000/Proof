
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
