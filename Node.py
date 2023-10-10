

class Symbol:
    def __init__(self, 
                 kind:str, 
                 name:str, 
                 args:list=[], 
                 vars:set=set()) -> None:
        self.kind = kind
        self.name = name
        self.args = args
        self.vars = vars
        self.bool = None

    def copy(self):
        args = [node.copy() for node in self.args]
        return Symbol(self.kind, self.name, args, self.vars.copy())

    def __eq__(self, __value) -> bool:
        if type(__value) != Symbol:
            return False
        if self.kind == "FORMULA":
            return self.args[0] == __value
        if __value.kind == "FORMULA":
            return self == __value.args[0]
        if self.kind != __value.kind or \
           self.name != __value.name or \
           len(self.args) != len(__value.args):
            return False
        for i, j in zip(self.args, __value.args):
            if i != j: 
                return False
        return True
    
    def __str__(self) -> str:
        s = ""
        for arg in self.args:
            s += " " + str(arg)
        if self.kind == "FORMULA":
            idx = s.index(" ")
            s = s[:idx] + " :=" + s[idx:]
        return f"{self.name}{s}"