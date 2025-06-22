# Class 9 Maths - General Chapter 104
**Language:** Hinglish

```markdown
# [Class 9] Maths - Chapter 4: Linear Equations in Two Variables (Do Char Wale Raikhik Samikaran)

## 🌟 Core Concepts (Mukhya Avdharnayein)

1.  **Linear Equation in One Variable (Ek Char Wala Raikhik Samikaran) - Recall:**
    *   Format: `ax + b = 0` (jahan a ≠ 0).
    *   Solution: Unique (advitiya) solution hota hai. Jaise `2x + 5 = 0` ka solution `x = -5/2` hai.
    *   Representation: Number line par represent kar sakte hain.

2.  **Linear Equation in Two Variables (Do Char Wale Raikhik Samikaran) - Introduction:**
    *   **Definition:** Koi bhi equation jo `ax + by + c = 0` ke form mein likha ja sakta hai, jahan `a`, `b`, aur `c` vastavik sankhyaen (real numbers) hain, aur `a` aur `b` dono ek saath zero nahin hain (`a` and `b` are not both zero).
    *   **Variables (Char):** Usually `x` aur `y` use hote hain, par dusre letters bhi use ho sakte hain (jaise `s`, `t`, `p`, `q`).
    *   **Standard Form (Manak Roop):** `ax + by + c = 0`. Is form mein likhne se `a`, `b`, `c` ke values clear ho jate hain.
        *   `a`: Coefficient of `x` (`x` ka gunank)
        *   `b`: Coefficient of `y` (`y` ka gunank)
        *   `c`: Constant term (acharaank)

3.  **Solution of a Linear Equation in Two Variables (Do Char Wale Raikhik Samikaran ka Hal):**
    *   **Meaning:** Ek solution `x` aur `y` ka ek pair (yugm) hota hai, jo equation ko satisfy karta hai (santusht karta hai). Ise ordered pair `(x, y)` ke roop mein likhte hain.
    *   **Nature of Solutions:** Ek linear equation in two variables ke **infinitely many solutions (anant hal)** hote hain. Ek solution se equation satisfy hota hai, jaise `x + y = 176` mein `x=100, y=76` ek solution hai `(100, 76)`. `x=76, y=100` bhi ek solution hai `(76, 100)`. `x=170, y=6` bhi ek solution hai `(170, 6)`.

📊 **Concept Hierarchy:**
```mermaid
graph TD
    A[Linear Equations (Raikhik Samikaran)] --> B(In One Variable);
    A --> C(In Two Variables);
    B --> D{Unique Solution (Advitiya Hal)};
    B --> E{Format: ax + b = 0};
    C --> F{Standard Form: ax + by + c = 0};
    C --> G{Infinitely Many Solutions (Anant Hal)};
    C --> H{Solution is an Ordered Pair (x, y)};
    F --> I[a, b, c are Real Numbers];
    F --> J[a and b not both zero];
```

## 📘 Key Learnings (Mukhya Baatein)

1.  **Pehchan aur Standard Form:** Kisi bhi diye gaye equation ko `ax + by + c = 0` ke standard form mein badalna aur `a`, `b`, `c` ki values nikalna.
    *   *Udaharan (Example):* Equation `2x = y` ko standard form mein likhna hai.
        *   Ise `2x - y = 0` likh sakte hain.
        *   Ya phir `2x - 1y + 0 = 0`.
        *   Yahan, `a = 2`, `b = -1`, `c = 0`.
    *   *Udaharan (Example):* Equation `x - 4 = √3y` ko standard form mein likhna hai.
        *   Ise `x - √3y - 4 = 0` likh sakte hain.
        *   Yahan, `a = 1`, `b = -√3`, `c = -4`.

2.  **One Variable Equation as Two Variable Equation:** Ek char wale equation ko bhi do char wale equation ke roop mein express kiya ja sakta hai.
    *   *Udaharan (Example):* `x = -5` ko `1x + 0y = -5` ya `1x + 0y + 5 = 0` likh sakte hain. Yahan `a=1, b=0, c=5`.
    *   *Udaharan (Example):* `y = 2` ko `0x + 1y = 2` ya `0x + 1y - 2 = 0` likh sakte hain. Yahan `a=0, b=1, c=-2`.

3.  **Finding Solutions (Hal Gyat Karna):** Ek linear equation in two variables ke anant hal (infinitely many solutions) kaise nikalein.
    *   **Method:** Ek variable (jaise `x`) ki koi bhi value apni marzi se chunein (choose karein) aur use equation mein substitute karke dusre variable (`y`) ki corresponding value nikal lein.
    *   *Udaharan (Example):* Equation `x + 2y = 6` ke solutions nikalo.
        *   Agar `x = 0` rakhein: `0 + 2y = 6` => `2y = 6` => `y = 3`. Solution: `(0, 3)`.
        *   Agar `y = 0` rakhein: `x + 2(0) = 6` => `x = 6`. Solution: `(6, 0)`.
        *   Agar `x = 2` rakhein: `2 + 2y = 6` => `2y = 4` => `y = 2`. Solution: `(2, 2)`.
        *   Agar `y = 1` rakhein: `x + 2(1) = 6` => `x + 2 = 6` => `x = 4`. Solution: `(4, 1)`.
    *   **Tip:** `x = 0` ya `y = 0` rakhna calculations ko aasan bana sakta hai.

4.  **Checking Solutions (Hal ki Jaanch Karna):** Diye gaye ordered pair `(x, y)` ko equation mein substitute karke check karna ki woh uska solution hai ya nahin.
    *   *Udaharan (Example):* Check karo ki `(4, 0)` equation `x - 2y = 4` ka solution hai ya nahin.
        *   Substitute `x = 4` aur `y = 0` in LHS (Left Hand Side): `x - 2y = 4 - 2(0) = 4 - 0 = 4`.
        *   RHS (Right Hand Side) = `4`.
        *   Kyunki LHS = RHS, isliye `(4, 0)` ek solution hai.
    *   *Udaharan (Example):* Check karo ki `(0, 2)` equation `x - 2y = 4` ka solution hai ya nahin.
        *   Substitute `x = 0` aur `y = 2` in LHS: `x - 2y = 0 - 2(2) = -4`.
        *   RHS = `4`.
        *   Kyunki LHS ≠ RHS, isliye `(0, 2)` solution nahin hai.

📈 **Diagrammatic Representation (Concept):**
Jab hum in solutions ko Cartesian Plane (Graph paper) par plot karte hain, toh woh ek seedhi rekha (straight line) banate hain. Har point us line par equation ka ek solution hota hai. (Graphing details agle section mein hain).

## 🧩 Active Learning (Sakriya Adhyayan)

*   **Activity: Research-based Case Study 🔍**
    *   **Topic:** Local Transport Costs (Sthaniya Parivahan Ke Kharch)
    *   **Task:** Apne sheher/gaon mein auto-rickshaw ya taxi ke kiraye ka pattern pata karo. Kya wahan ek fixed charge hai aur phir per kilometer ka charge hai? Maan lo fixed charge `₹ c` hai aur per km charge `₹ m` hai. Agar `x` km travel karna hai aur total kiraya `₹ y` hai, toh is situation ko represent karne wala linear equation in two variables banao (`y = mx + c`). Apne dosto se data compare karo. Kya sabhi auto drivers ka rate same hai? Isse `m` aur `c` ki values par kya farak padega?
    *   **Socho:** Agar aapko 5 km jaana hai, toh equation use karke kiraya estimate karo. Agar aapne ₹100 diye, toh kitne km travel kar sakte ho (equation solve karke)?

*   **Discussion: Critical Analysis of Real-world Impacts 🌍**
    *   **Scenario:** India-Sri Lanka cricket match mein 2 batsmen ne milkar 176 runs banaye (`x + y = 176`).
    *   **Points:**
        *   Is equation ke kitne possible solutions hain jo cricket ke context mein valid hain? (Runs negative ya fraction mein nahin ho sakte). Discuss some possible pairs of scores.
        *   Agar ek batsman ne 100 se zyada run banaye (`x > 100`), toh dusre batsman ke score (`y`) par kya condition hogi? (`y < 76`).
        *   Kya `(88, 88)` ek possible solution hai? Iska kya matlab hua?
        *   Agar humein pata chale ki ek batsman ne dusre se double runs banaye (`x = 2y`), toh kya hum unique solution nikal sakte hain? (Yeh system of equations ka concept hai, jo aage aayega, par yahan soch sakte hain). `2y + y = 176` => `3y = 176`. Kya yeh possible hai cricket scores ke liye? Kyun? (Runs whole numbers hote hain).

## 📝 Assessment Prep (Mulyankan Ki Taiyari)

*   **Case Study Based Questions:**
    1.  Ek notebook ki keemat ek pen ki keemat se duguni (twice) hai. Agar notebook ki keemat `₹ x` aur pen ki keemat `₹ y` hai, toh is statement ko represent karne wala linear equation in two variables likho. (Write `x = 2y` or `x - 2y = 0`). Is equation ke 3 alag-alag solutions nikalo. Kya `(10, 5)` iska solution hai? Kya `(5, 10)` iska solution hai? Apne answer ko justify karo.
    2.  Ek parivar ka mahine ka doodh (`x` liters) aur sabzi (`y` kg) par कुल खर्च (total expenditure) `₹ 3000` hai. Is situation ko ek linear equation se represent karo, agar doodh `₹ 50` per liter aur sabzi average `₹ 40` per kg hai. (`50x + 40y = 3000`). Agar parivar ne 40 litre doodh istemal kiya, toh unhone kitni sabzi kharidi?

*   **Diagram/Equation Interpretation:**
    *   Neeche diye gaye equations ko `ax + by + c = 0` form mein likho aur `a`, `b`, `c` batao:
        *   `3x = -7y` (Answer: `3x + 7y + 0 = 0`, `a=3, b=7, c=0`)
        *   `y/2 - x/3 = 5` (Answer: Multiply by 6 -> `3y - 2x = 30` -> `-2x + 3y - 30 = 0`, `a=-2, b=3, c=-30` OR `2x - 3y + 30 = 0`, `a=2, b=-3, c=30`)
        *   `6 = 2x` (Answer: `2x + 0y - 6 = 0`, `a=2, b=0, c=-6`)
    *   Equation `πx + y = 9` ke chaar (four) solutions nikalo. (Example solutions: `(0, 9)`, `(9/π, 0)`, `(1, 9-π)`, `(2, 9-2π)`)
    *   Check karo ki `(√2, 4√2)` equation `x - 2y = 4` ka solution hai ya nahin. (Answer: `√2 - 2(4√2) = √2 - 8√2 = -7√2 ≠ 4`. So, it is not a solution.)
    *   Agar `x = 2`, `y = 1` equation `2x + 3y = k` ka ek solution hai, toh `k` ki value find karo. (Answer: `2(2) + 3(1) = k` => `4 + 3 = k` => `k = 7`).

## 🌏 Bharatiya Context (Indian Context)

1.  **Cricket Score Example:** Jaise text mein diya hai, India aur Sri Lanka ke match mein do batsmen ka total score 176 (`x + y = 176`) ek real-life situation hai jise linear equation se model kiya gaya hai. Iske anant mathematical solutions hain, par cricket ke context mein sirf non-negative whole number solutions hi valid hain.
2.  **Cost Comparison (Keemat Tulna):** Exercise 4.1 ka question (notebook aur pen ki keemat) `x = 2y` Bharatiya market mein aam taur par pai jaane wali situation ko darshata hai, jahan ek cheez ki keemat dusri se related hoti hai. Hum ise alag-alag items jaise "ek Kurti ki keemat ek T-shirt se `₹ 200` zyada hai" (`k = t + 200`) ya "5 kg chawal aur 3 kg daal ki kul keemat `₹ 800` hai" (`5c + 3d = 800`) jaise examples mein badal sakte hain.
3.  **Economic/Social Data (Conceptual):** Hum linear equations ka use simple economic ya social trends ko samajhne ke liye kar sakte hain (haalanki is chapter mein complex data analysis nahi hai). Jaise, agar humein pata ho ki Pradhan Mantri Jan Dhan Yojana (PMJDY) mein har hafte average `k` accounts khul rahe hain, toh `t` hafton mein khule total accounts `y` ko `y = kt` (agar shuru mein zero the) ya `y = kt + c` (agar shuru mein `c` accounts the) jaise simple linear model se *approximate* kar sakte hain. Yeh model vastavik data ko simplify karta hai. Isi tarah, National Family Health Survey (NFHS) ke data se kisi do simple parameters ke beech linear relationship (agar ho toh) explore karne ka socha ja sakta hai (higher classes mein).

---
**Note:** Yeh summary NCERT Chapter 4 ke Section 4.1, 4.2, aur 4.3 par based hai. Graphing of linear equations Section 4.4 mein cover hota hai.
```