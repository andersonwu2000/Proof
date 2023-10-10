from first_order_logic import *

LNT = Language({"0":0, "S":1, "+":2, "*":2, "E":2},
               {"<":2})

N = Axiom(LNT,
          ["N1  := ∀ x ¬ = S x 0",
           "N2  := ∀ x ∀ y → = S x S y = x y",
           "N3  := ∀ x = + x 0 x",
           "N4  := ∀ x ∀ y = + x S y S + x y",
           "N5  := ∀ x = * x 0 0",
           "N6  := ∀ x ∀ y = * x S y + * x y x",
           "N7  := ∀ x = E x 0 S 0",
           "N8  := ∀ x ∀ y = E x S y * E x y x",
           "N9  := ∀ x ¬ < x 0",
           "N10 := ∀ x ∀ y ↔ < x S y ∨ < x y = x y",
           "N11 := ∀ x ∀ y ∨ ∨ < x y = x y < y x",
          ])

TEST = Axiom(LNT, 
             ["TEST1 := ∀ x < + x y z",
              "∀ y = x y",    # TEST[2]
              "∀ x ∀ y = x y",
              "→ ∀ x < + x y z < + + 0 0 y z"])

# print("∀ x < + x y z" in TEST)  # True
# print("= 0 x" in TEST)  # False
# print("TEST1" in TEST)  # True
# print(TEST["TEST1"])
# print(TEST["TEST1"].vars)
# print(LNT.substitution("y", "+ 0 0", TEST["TEST1"]))
# print(LNT.substitutable("y", "+ 0 0", TEST["TEST1"]))  # True
# print(LNT.substitutable("x", "S y", TEST["2"]))  # False
# print(LNT.substitutable("x", "S y", TEST["3"]))  # True
# print()

D1 = ["∀ y = x y",
      "∀ x < + x y z",
      "→ ∀ x < + x y z < + + 0 0 y z",
      "→ ∧ = v1 v2 = v3 v4 = + v1 v3 + v2 v4",
      "→ ∧ = v1 v2 = v3 v4 ↔ < v1 v3 < v2 v4",
      "→ ∀ x < + x y z ∀ x < + + 0 0 y z",
      "∨ = x x ∀ x < + x y z by TEST1 2"]

D2 = ["∀ y = x y",
      "¬ ∀ x < + x y z"]

D3 = ["∀ x ¬ = S x 0",
      "→ ∀ x ¬ = S x 0 ¬ = S 0 0",
      "¬ = S 0 0"]

print(TEST.Deduce(D1))  # True
print(TEST.Deduce(D2))  # False
print(N.Deduce(D2))  # False
print(N.Deduce(D3, True))  # True
