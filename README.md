## Usage

To effectively utilize this library, follow these steps:

**Step 1:** Build a language using the `Language` class, specifying function symbols, relation symbols, and whether to use '=' as the equality symbol.

```python
from first_order_logic import *

# Example of creating a language
LNT = Language(
    {"0": 0, "S": 1, "+": 2, "*": 2, "E": 2},
    {"<": 2}
)
```

**Step 2:** Define axioms by building a list of FORMULAs and using the `Axiom` class, specifying the language for which the axioms are defined.

```python
# Example of creating axioms
N = Axiom(LNT, [
    "N1  := ∀ x ¬ = S x 0",
    "N2  := ∀ x ∀ y → = S x S y = x y",
    "N3  := ∀ x = + x 0 x",
])
```

**Step 3:** Build a deduction by creating a list of FORMULAs.

```python
# Example of creating a deduction
deduction = [
    "∀ x ¬ = S x 0",
    "→ ∀ x ¬ = S x 0 ¬ = S 0 0",
    "¬ = S 0 0"
]
```

**Step 4:** Use the defined axioms to deduce the deduction using the `Axiom.Deduce` method.

```python
# Example of deducing with axioms
result = N.Deduce(deduction, update_axiom=True)

# Check the result
print(result)  # True
```

By following these steps, you can effectively use this library to work with first-order logic and perform deductions using axioms.

## Signature of Language
The signature of a language consists of two dictionaries: **functions** and **relations**. 

The keys of these two dictionaries are symbols, and the values are the arity of the symbols.

## Grammar of FORMULAs

1. **Variable**:
   - A string that adheres to the following rules:
     * Variables can be single letters such as `x`, `y`, and `z`.
     * Variables can also be represented as `v` followed by a string of numerals, for example, `v123`.

2. **WFF** (Well-Formed Formula):
   - A well-formed formula in the 1st order language expressed in Polish notation.

3. **NAME**:
   - A string used to assign a name to a FORMULA.

4. **FORMULA**:
   - A string that conforms to the following rules:
     * If `φ` is a WFF, then `φ` is a FORMULA.
     * If `φ` is a WFF and `n` is a NAME, then `n := φ` is a FORMULA.
     * If `φ` is a WFF and `a, b, c, ...` are either NAMEs or WFFs, then `φ by a b c ...` is a FORMULA.
