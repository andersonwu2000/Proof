# First Order Language - Proof Assistant

1. 建立語言：
   使用 first_order_logic.Language 建立語言。
   ```
   LNT = Language({"0":0, "S":1, "+":2, "*":2, "E":2},
                  {"<":2})
   ```
   
2. 語法：
   以波蘭表示法編寫一階邏輯公式，符號間以空白區隔。
   ```
   "∀ x ∀ y = x y"
   ```
   
   一階邏輯公式外部運算子：
   
   2.1. 命名 `name := formula`
        為公式命名，以供引用。
   
   2.2. 引用 `formula by name1 name2 ...`
        適用於命題邏輯推理，以加速證明。
   ```
   "S1 := → ∀ x < + x y z < + + 0 0 y z by N1 N2"
   ```
    
4. 證明：
