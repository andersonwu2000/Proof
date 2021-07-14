import syntax_alpha
import architecture

bases = architecture.the_basic  # 可省略
assumptions = {"a ∧ b .", "a ."}  # 該環境的假設
grammar = syntax_alpha.alpha  # 使用的語法
new_area = architecture.environment(bases, assumptions, grammar)  # 環境

proof1 = "b ∧ a ."
proof2 = "¬ b ∧ a ."

new_area(proof1)  # True
new_area(proof2)  # False


assumptions = {"¬ ( ( c ∈ A ) ∧  ( d ∈ B ) ) ."}  # 新環境的假設
new_area = architecture.environment(new_area, assumptions, grammar)  # 繼承舊環境

proof1 = "b ∧ a ."
proof2 = "suppose c ∈ A . d ∈ B ."

new_area(proof1)  # 依然是 True
new_area(proof2)  # Fasle


assumptions = {"a ∧ b .", "¬ ( a ∧ b ) ."}  # 矛盾
new_area = architecture.environment(bases, assumptions, grammar)

proof1 = "b ∧ a ."

new_area(proof1)  # 矛盾
