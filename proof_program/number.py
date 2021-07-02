import architecture

axioms = {
    "1 != 0", 
    "∀ a ∈ R : 0 + a = a", 
    "∀ a ∈ R : 1 * a = a", 
    "∀ a , b ∈ R : a + b ∈ R", 
    "∀ a , b ∈ R : a * b ∈ R", 
    "∀ a , b ∈ R : a + b = b + a", 
    "∀ a , b ∈ R : a * b = b * a", 
}
real_number = architecture.area(architecture.the_basic, axioms)

