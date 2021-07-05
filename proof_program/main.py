import syntax_alpha
import architecture

proof1 = r'''
    1 + 1 = 2
    '''
proof2 = r'''
    let ε > 0 
    if | x - 3 | < ε / 2
    then 2 * | x - 3 | < ε
    then | 2 * x - 6 | < ε
    then 2 * x → 6 as x → 3
    '''
bases = architecture.the_basic
assumptions = "a = b"
grammar = syntax_alpha.alpha
new_area = architecture.area(bases, assumptions, grammar)
new_area = architecture.area(new_area, set(), grammar)

# thms = new_area.theorems
# for thm in thms:
#     thm.representation_structure()

thms = new_area.related
for thm in thms:
    thm.representation_structure()