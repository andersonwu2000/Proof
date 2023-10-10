from Node import Symbol

class Language:
    connectives = {"¬":1, "∨":2, "∧":2, "→":2, "↔":2}
    quantifier  = {"∀":2, "∃":2}

    def __init__(self, f:dict={}, r:dict={}, equal:bool=True) -> None:
        """ 
        Establish language.
        Constants as 0-ary functions.
        ∃xφ as ¬∀x¬φ.
        format: {symbol: ary}
        
        Args:
            f (dict): function symbols
            r (dict): relation symbols
            equal (bool): allow '='
        """
        self.function = f
        if equal and "=" not in r :
            self.relation = r|{"=":2}
        else:
            self.relation = r

    def tokenize(self, f:str) -> list:
        """
            A simple tokenization.
            format: polish notation
        """
        f = f.split(" ")
        for _ in range(f.count("")):
            f.remove("")
        return f

    def substitutable(self, x, t, f:Symbol) -> bool:
        if self.free(x, f):
            if type(t) == str:
                self.idx = 0
                self.expression = self.tokenize(t)
                t = self.gen()
            if f.kind == "QUANTIFIER":
                if self.free(f.args[0], t):
                    return False
                else:
                    return self.substitutable(x, t, f.args[1])
            elif f.kind == "CONNECTIVE":
                for node in f.args:
                    if not self.substitutable(x, t, node):
                        return False
                return True
            elif f.kind == "RELATION":
                return True
            elif f.kind == "FORMULA":
                return self.substitutable(x, t, f.args[0])
            else:
                raise ValueError(f"{f} not a formula")
        else:
            return True
    
    def substitution(self, x, t, f:Symbol) -> Symbol:
        if self.free(x, f):
            if type(t) == str:
                self.idx = 0
                self.expression = self.tokenize(t)
                t = self.gen()
            if not self.is_term(t):
                raise ValueError(f"{t} not a variable")
            if f.kind == "VARIABLE":
                return t
            f = f.copy()
            f.args = [self.substitution(x, t, node) 
                      for node in f.args]
            return f
        else:
            return f
    
    def free(self, x, f:Symbol) -> bool:
        if type(x) == Symbol:
            x = x.name
        return x in f.vars
    
    def is_var(self, s) -> bool:
        """
            Args:
                s (str/Symbol): tested variable
        """
        if type(s) is str:
            if s[0] == "v" and s[1:].isnumeric():
                return True
            return s in {"x", "y", "z"}
        elif type(s) == Symbol:
            return s.kind == "VARIABLE"
        else:
            raise TypeError("not str or Symbol")
    
    def is_term(self, s:Symbol) -> bool:
        return s.kind in {"VARIABLE", 
                          "FUNCTION", 
                          "CONSTANT"}
    
    def is_formula(self, s:Symbol) -> bool:
        return s.kind in {"QUANTIFIER", 
                          "RELATION", 
                          "CONNECTIVE"}
    
    def formulation(self, phi:str) -> Symbol:
        """ 
        Generate an abstract syntax tree for a formula.

        Args:
            phi (str): use polish notation
        """
        self.idx = 0
        self.expression = self.tokenize(phi)
        
        args = []
        if self.expression[1] == ":=":
            self.idx += 2
            sym = self.expression[0]
        else:
            sym = None
        args += [self.gen()]
        self.idx += 1
        if not self.is_formula(args[-1]):
            raise ValueError(f"{args[-1].name} not a formula")
        if self.idx == len(self.expression):
            return Symbol("FORMULA", sym, args, args[0].vars)
        if self.expression[self.idx] == "by":
            while self.idx != len(self.expression):
                args += [self.gen()]
                self.idx += 1
        else:
            raise ValueError(f"{args[-1].name} wrong format")
        return Symbol("FORMULA", sym, args, args[0].vars)
    
    def gen(self) -> Symbol:
        """ 
        Generate a abstract syntax tree.
        Need to set self.expression and self.idx in advance.

        Structure:
            FORMULA    - QUANTIFIER | RELATION | CONNECTIVE, [BY]
            QUANTIFIER - VARIABLE, QUANTIFIER | RELATION | CONNECTIVE
            CONNECTIVE - {QUANTIFIER | RELATION | CONNECTIVE}
            RELATION   - {VARIABLE   | FUNCTION | CONSTANT  }
            FUNCTION   - {VARIABLE   | FUNCTION | CONSTANT  }
        """
        sym = self.expression[self.idx]
        if sym in self.quantifier:
            v = Symbol("VARIABLE", self.expression[self.idx+1])
            if not self.is_var(v):
                raise ValueError(f"{args[-1].name} not a variable")
            self.idx += 2
            f = self.gen()
            if not self.is_formula(f):
                raise ValueError(f"{args[-1].name} not a formula")
            vars = f.vars.copy()
            vars.discard(v.name)
            if sym == "∃":
                f = Symbol("CONNECTIVE", "¬", f, f.vars.copy())
                f = Symbol("QUANTIFIER", "∀", [v, f], vars)
                return Symbol("CONNECTIVE", "¬", f, f.vars.copy())
            else:
                return Symbol("QUANTIFIER", sym, [v, f], vars)
        
        elif sym in self.connectives:
            args, vars = [], set()
            for _ in range(self.connectives[sym]):
                self.idx += 1
                args += [self.gen()]
                vars |= args[-1].vars
                if not self.is_formula(args[-1]):
                    raise ValueError(f"{args[-1].name} not a formula")
            return Symbol("CONNECTIVE", sym, args, vars)
        
        elif sym in self.relation:
            args, vars = [], set()
            for _ in range(self.relation[sym]):
                self.idx += 1
                args += [self.gen()]
                vars |= args[-1].vars
                if not self.is_term(args[-1]):
                    raise ValueError(f"{args[-1].name} not a term")
            return Symbol("RELATION", sym, args, vars)
        
        elif sym in self.function:
            args, vars = [], set()
            for _ in range(self.function[sym]):
                self.idx += 1
                args += [self.gen()]
                vars |= args[-1].vars
                if not self.is_term(args[-1]):
                    raise ValueError(f"{args[-1].name} not a term")
            if self.function[sym]:
                return Symbol("FUNCTION", sym, args, vars)
            else:
                return Symbol("CONSTANT", sym)
            
        elif self.is_var(sym):
            if not self.is_var(sym):
                raise ValueError(f"{sym} not a variable")
            return Symbol("VARIABLE", sym, vars={sym})
        
        elif sym == "by":
            args = []
            while self.idx != len(self.expression)-1:
                self.idx += 1
                args += [self.expression[self.idx]]
            return Symbol("BY", sym, args)

        else:
            raise ValueError(f"{sym} is not grammatical")