

class syntax:
    def __init__(self, theorems) -> set:
        """ 為定理建立抽象語法樹 """
        if type(theorems) is str:
            pass
        elif type(theorems) in {list, tuple, set}:
            pass

class alpha:
    """
    字母表和語法
    P
    let P，用於句首
    if P，用於句首
    then P，用於句首
    a ∈ b
    a V b
    a ∧ b
    ¬ a
    a ⇔ b
    ∀ a ∈ b : P(a)
    ∃ a ∈ b : P(a)
    ! a = b
    ( a ) 
    a , b
     """
    def __init__(self, theorems) -> None:
        """ 為定理建立抽象語法樹 """
        if type(theorems) is str:
            pass
        elif type(theorems) in {list, tuple, set}:
            pass

    def logical(self, theorem) -> bool:
        """ 檢查敘述對於該定理是否正確 """
        pass
        return True