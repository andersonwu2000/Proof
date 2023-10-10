from first_order_language import *
import sympy
from itertools import combinations

class Axiom:
    """
        Members:
            __contains__
            __getitem__
            Deduce
    """
    def __init__(self, L:Language, Sigma:list=[]) -> None:
        """
        Establish axioms.
        
        Args:
            L (Language): language
            Sigma (list): formulas of axiom
        """
        self.L = L
        self.formulas = []
        for idx in range(len(Sigma)):
            phi = self.L.formulation(Sigma[idx])
            if phi.name == None:
                phi.name = str(idx+1)
            self.formulas += [phi]

    def __contains__(self, f) -> bool:
        """
            Checks whether a formula or its name is an axiom.
        """
        if type(f) == str:
            # if f is a name of formula
            if len(self.L.tokenize(f)) == 1:
                for phi in self.formulas:
                    if f == phi.name:
                        return True
                return False
            # if f is formula
            f = self.L.formulation(f)
        for phi in self.formulas:
            if f.args[0] == phi.args[0]:
                return True
        return False
    
    def __getitem__(self, key:str) -> Symbol:
        """
            Get formula by name.
        """
        for phi in self.formulas:
            if key == phi.name:
                return phi
        raise KeyError(f"The axiom has no {key}")

    def PC(self, priority:list, GAMMA:list, f) -> bool:
        expr = True
        for phi in priority:
            expr &= phi
        if not sympy.logic.inference.satisfiable(expr & ~f):
            return True
        for num in range(len(GAMMA)):
            expr_case = expr
            for gamma in combinations(GAMMA, num):
                for phi in gamma:
                    expr_case &= phi
                if not sympy.logic.inference.satisfiable(expr_case & ~f):
                    return True
        return False

    def QR(self, gamma:Symbol, f) -> bool:
        """
            ψ → φ : ψ → ∀xφ
        """
        gamma, f = gamma.args[0], f.args[0]
        if gamma.name != "→" or f.name != "→": 
            return False
        f1 = f.args[0]   # ψ
        f2 = f.args[1]   # ∀xφ
        if f2.name != "∀": return False
        x = f2.args[0]   # x
        if self.L.free(x, f1): return False
        f2 = f2.args[1]  # φ
        if gamma.args[0] != f1 or gamma.args[1] != f2:
            return False
        return True

    def Rule_of_Inference(self, f) -> bool:
        by = []
        for node in f.args:
            if node.name == "by":
                by = [self[phi] for phi in node.args]

        priority, gamma = [], []
        # reduce premise and QR
        for phi in self.__deduction:
            if self.QR(phi, f):
                return True
            if phi in by:
                priority += [phi.bool]
            else:
                gamma += [phi.bool]
        if self.PC(priority, gamma, f.bool):
            return True
        return False

    def Equality(self, f) -> bool:
        """ 
            1. x1=x1
            2. (x1=y1)∧...∧(xn=yn) → 
                f(x1, ..., xn) = f(y1, ..., yn)
            3. (x1=y1)∧...∧(xn=yn) → 
                R(x1, ..., xn) ↔ R(y1, ..., yn)
        """
        if f.kind != "CONNECTIVE" or \
           f.name not in {"=", "→"}:
            return False  
        f1 = f.args[0]
        f2 = f.args[1]

        # 1.
        if f.name == "=" and \
           f1.kind == f2.kind == "VARIABLE" and \
           f1.name == f2.name:
            return True

        # 2. & 3.  
        self.lhs_vars = []
        if f.kind == "CONNECTIVE" and \
           f2.name in {"=", "↔"} and \
           self.Equality_get_vars(f1):
            f1 = f2.args[0]  # f(x1, ..., xn) / R(x1, ..., xn)
            f2 = f2.args[1]  # f(y1, ..., yn) / R(y1, ..., yn)
        else:
            return False
        
        vars_num = len(self.lhs_vars)
        if f1.kind == f2.kind and \
           f1.kind in {"FUNCTION", "RELATION"} and \
           f1.name == f2.name and \
           len(f1.args) == len(f2.args) == vars_num:
            vars1 = f1.args  # x1, ..., xn
            vars2 = f2.args  # y1, ..., yn
        else:
            return False
    
        self.rhs_vars = [(x.name, y.name)
                         for x, y in zip(vars1, vars2)]
        if self.lhs_vars == self.rhs_vars:
            return True
        else:
            return False

    def Equality_get_vars(self, f) -> bool:
        # f = (x1=y1)∧...∧(xn=yn)
        if f.name == "=":
            var1 = f.args[0]
            var2 = f.args[1]
            if var1.kind == var2.kind == "VARIABLE":
                self.lhs_vars += [(var1.name, var2.name)]
                return True
            else:
                return False
        elif f.name == "∧":
            return self.Equality_get_vars(f.args[0]) and \
                   self.Equality_get_vars(f.args[1])
        else:
            return False

    def Quantifier(self, f:Symbol) -> bool:
        """
            (∀xφ) → φ^x_t
        """
        if f.name != "→": return False
        f1 = f.args[0]
        if f1.name != "∀": return False
        x  = f1.args[0]  # x
        f1 = f1.args[1]  # φ
        f2 = f.args[1]   # φ^x_t

        self.t = None
        if not self.Quantifier_get_t(x, f1, f2):
            return False
        
        if self.L.substitutable(x, self.t, f1) and \
           self.L.substitution(x, self.t, f1) == f2:
            return True
        return False
    
    def Quantifier_get_t(self, x, f1, f2) -> bool:
        # from x, φ, φ^x_t get t
        if f1 == x and self.L.is_term(f2):
            self.t = f2
            return True
        if f1.kind != f2.kind or \
           f1.name != f2.name or \
           len(f1.args) != len(f2.args):
            return False
        for node1, node2 in zip(f1.args, f2.args):
            if self.Quantifier_get_t(x, node1, node2):
                return True
        return False

    def Logical_Axiom(self, f) -> bool:
        f = f.args[0]
        return self.Equality(f) or self.Quantifier(f)

    def In_Axiom(self, f) -> bool:
        for phi in self.formulas:
            if f.args[0] == phi.args[0]:
                return True
        return False
    
    def get_bool(self, f:Symbol):
        if f.kind == "FORMULA":
            expr = self.get_bool(f.args[0])
            f.bool = sympy.logic.boolalg.to_cnf(expr)
        elif f.kind in {"RELATION", "QUANTIFIER"}:
            f = str(f)
            if f not in self.prime_list:
                num = len(self.prime_list)
                self.prime_list[f] = sympy.Symbol(f"p{num}")
            return self.prime_list[f]
        elif f.kind == "CONNECTIVE":
            if f.name == "¬":
                return ~self.get_bool(f.args[0])
            a = self.get_bool(f.args[0])
            b = self.get_bool(f.args[1])
            if f.name == "∨":
                return a | b
            elif f.name == "∧":
                return a & b
            elif f.name == "→":
                return a >> b
            elif f.name == "↔":
                return ~(a ^ b)
        else:
            raise ValueError(f"{f} not a formula")

    def Deduce(self, deduction:list, update_axiom=False) -> bool:
        """
            Deduce a deduction

            Args:
                deduction (list): deduction
                update_axiom (bool): Add conclusion to axiom
        """
        self.__deduction = []
        self.prime_list = {}
        for phi in deduction:
            phi = self.L.formulation(phi)
            self.get_bool(phi)
            if self.In_Axiom(phi) or \
               self.Logical_Axiom(phi) or \
               self.Rule_of_Inference(phi):
                self.__deduction += [phi]
            else:
                return False
        
        if update_axiom:
            self.formulas += [self.__deduction[-1]]
        return True