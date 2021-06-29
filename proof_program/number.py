import area

axioms = {
    "1 != 0", 
    "∀ a ∈ R : 0 + a = a", 
    "∀ a ∈ R : 1 * a = a", 
    "∀ a , b ∈ R : a + b ∈ R", 
    "∀ a , b ∈ R : a * b ∈ R", 
    "∀ a , b ∈ R : a + b = b + a", 
    "∀ a , b ∈ R : a * b = b * a", 
}
real_number = area.area(area.the_basic, axioms)

