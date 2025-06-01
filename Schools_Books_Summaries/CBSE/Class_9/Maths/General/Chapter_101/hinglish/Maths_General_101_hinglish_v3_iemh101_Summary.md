# Class 9 Maths - General Chapter 101
**Language:** Hinglish

```markdown
# [Class 9] Number Systems - Chapter 1

## 🌟 Core Concepts

Yeh chapter Number Systems (संख्या प्रणालियाँ) ke baare mein hai. Hum alag-alag tarah ke numbers aur unke relationships ko samjhenge.

**Number Hierarchy 📊:**

1.  **Natural Numbers (N) (प्राकृतिक संख्याएँ):** Counting numbers. Jaise 1, 2, 3, ... Anant (infinitely many) hote hain.
2.  **Whole Numbers (W) (पूर्ण संख्याएँ):** Natural numbers + Zero (0). Jaise 0, 1, 2, 3, ...
3.  **Integers (Z) (पूर्णांक):** Whole numbers + Negative numbers. Jaise ..., -3, -2, -1, 0, 1, 2, 3, ... (Z 'zahlen' German word se aata hai, meaning 'to count').
4.  **Rational Numbers (Q) (परिमेय संख्याएँ):** Numbers jo **p/q** form mein likhe ja sakte hain, jahan p aur q integers hain aur **q ≠ 0**. Jaise 1/2, -3/4, 5 (kyunki 5 = 5/1), 0 (kyunki 0 = 0/1). 'Q' 'Quotient' se aata hai.
    *   Equivalent Rational Numbers: Ek hi rational number ko alag fractions se represent kar sakte hain, jaise 1/2 = 2/4 = 10/20. Hum simplest form (co-prime p aur q) use karte hain.
5.  **Irrational Numbers (अपरिमेय संख्याएँ):** Numbers jo **p/q** form mein **nahi** likhe ja sakte. Inka decimal expansion non-terminating aur non-recurring hota hai. Jaise √2, √3, π (pi), 0.101101110...
6.  **Real Numbers (R) (वास्तविक संख्याएँ):** Saare rational aur irrational numbers milakar Real Numbers banate hain. Number line par har point ek unique real number represent karta hai, aur har real number number line par ek unique point represent karta hai.

```mermaid
graph TD
    R(Real Numbers / वास्तविक संख्याएँ) --> Q(Rational Numbers / परिमेय संख्याएँ);
    R --> I(Irrational Numbers / अपरिमेय संख्याएँ);
    Q --> Z(Integers / पूर्णांक);
    Z --> W(Whole Numbers / पूर्ण संख्याएँ);
    W --> N(Natural Numbers / प्राकृतिक संख्याएँ);
    Z --> Neg(-ve Integers / ऋणात्मक पूर्णांक);
```

## 📘 Key Learnings

**1. Rational Numbers (परिमेय संख्याएँ):**
*   **Definition:** p/q form, where p, q are integers, q ≠ 0.
*   **Finding Rationals Between Two Numbers:**
    *   Method 1 (Average): (r+s)/2 r aur s ke beech mein hoga. Repeat karke aur find kar sakte hain.
    *   Method 2 (Equivalent Fractions): Agar 'n' numbers find karne hain, toh denominator ko (n+1) ya usse bada banakar beech ke numbers likh do. Jaise 1 aur 2 ke beech 5 numbers: 1 = 6/6, 2 = 12/6. Beech ke numbers: 7/6, 8/6, 9/6, 10/6, 11/6.
*   **Important:** Do rational numbers ke beech infinitely many rational numbers hote hain.

**2. Irrational Numbers (अपरिमेय संख्याएँ):**
*   **Definition:** Jo rational nahi hain (p/q form mein nahi likh sakte).
*   **Examples:** √2, √3, √5, π, 0.121221222...
*   **Discovery:** Pythagoreans ne discover kiya (around 400 BC). Hippacus ne √2 ko irrational prove kiya. π ko irrational Lambert aur Legendre ne prove kiya (late 1700s).
*   **Locating on Number Line:**
    *   √2: Unit square (side 1) ka diagonal √2 hota hai. Use number line par transfer karo (Pythagoras Theorem: 1² + 1² = (√2)²).
    *   √3: √2 ke end point par 1 unit perpendicular banao, hypotenuse √3 hoga (Pythagoras Theorem: (√2)² + 1² = (√3)²).
    *   √n: √ (n-1) locate karne ke baad, uske end point par 1 unit perpendicular banao, hypotenuse √n hoga.
    *   Geometric Method for √x (x > 0):
        1.  Line par AB = x units mark karo.
        2.  B se BC = 1 unit mark karo.
        3.  AC ka midpoint O find karo.
        4.  O ko center aur OA/OC ko radius lekar semicircle banao.
        5.  B par AC ke perpendicular line draw karo jo semicircle ko D par intersect kare. BD = √x hoga.

    ![Geometric Location of Sqrt(x)](https://i.imgur.com/gJk8t7E.png)
    *(Diagram showing construction to find sqrt(x) geometrically)*

**3. Real Numbers and Decimal Expansions (वास्तविक संख्याएँ और उनके दशमलव प्रसार):**
*   **Rational Numbers:**
    *   **Terminating (सांत):** Remainder 0 ho jata hai. Jaise 7/8 = 0.875, 1/2 = 0.5. Yeh tab hota hai jab denominator (q in p/q simplest form) ke prime factors sirf 2 aur/ya 5 hote hain.
    *   **Non-terminating Recurring (अनवसानी आवर्ती):** Remainder repeat hota hai, quotient mein digits ka block repeat hota hai. Jaise 10/3 = 3.333... (3.), 1/7 = 0.142857142857... (0.142857).
*   **Irrational Numbers:**
    *   **Non-terminating Non-recurring (अनवसानी अनावर्ती):** Decimal expansion na kabhi end hota hai, na hi repeat hota hai. Jaise √2 = 1.41421356..., π = 3.14159265...
*   **Conversion:**
    *   Terminating decimal ko p/q mein easily convert kar sakte hain (e.g., 3.142 = 3142/1000).
    *   Non-terminating recurring ko p/q mein convert karne ke liye:
        *   x = number maano.
        *   Agar 1 digit repeat ho raha hai toh 10x, 2 digits repeat ho rahe hain toh 100x, etc. calculate karo.
        *   Subtract karke x ke liye solve karo. (Example 7, 8, 9 in NCERT).

**4. Operations on Real Numbers (वास्तविक संख्याओं पर संक्रियाएँ):**
*   Rational + Irrational = Irrational
*   Rational - Irrational = Irrational
*   Non-zero Rational × Irrational = Irrational
*   Non-zero Rational / Irrational = Irrational
*   Irrational +,-,×,/ Irrational = Result Rational bhi ho sakta hai, Irrational bhi. (e.g., √2 + (-√2) = 0 (Rational), √2 × √2 = 2 (Rational), √2 × √3 = √6 (Irrational)).
*   **Identities for positive real numbers a, b:**
    *   √(ab) = √a √b
    *   √(a/b) = √a / √b
    *   (√a + √b)(√a - √b) = a - b
    *   (a + √b)(a - √b) = a² - b
    *   (√a + √b)² = a + 2√(ab) + b

**5. Rationalizing the Denominator (हर का परिमेयकरण):**
*   Process jisse denominator ko rational number banate hain.
*   Agar denominator mein √b hai, toh √b/√b se multiply karo (e.g., 1/√2 = √2/2).
*   Agar denominator mein a + √b hai, toh (a - √b)/(a - √b) se multiply karo (using identity (x+y)(x-y)=x²-y²).
*   Agar denominator mein √a + √b hai, toh (√a - √b)/(√a - √b) se multiply karo.

**6. Laws of Exponents for Real Numbers (वास्तविक संख्याओं के लिए घातांक नियम):**
Let a > 0 be a real number and p, q be rational numbers.
*   aᵖ ⋅ a<0xE1><0xB5><0xA1> = aᵖ⁺<0xE1><0xB5><0xA1>
*   (aᵖ)<0xE1><0xB5><0xA1> = aᵖ<0xE1><0xB5><0xA1>
*   aᵖ / a<0xE1><0xB5><0xA1> = aᵖ⁻<0xE1><0xB5><0xA1>
*   aᵖ bᵖ = (ab)ᵖ
*   a⁰ = 1
*   a⁻ⁿ = 1/aⁿ
*   ⁿ√a = a¹/ⁿ
*   <0xE2><0x81><0xBF>√aᵐ = (ⁿ√a)ᵐ = aᵐ/ⁿ

## 🧩 Active Learning

*   **Activity 1: Square Root Spiral (वर्गमूल सर्पिल बनाना) 🌀:**
    *   Ek large paper par, point O se start karo. OP₁ = 1 unit banaye.
    *   P₁ par OP₁ ke perpendicular P₁P₂ = 1 unit banaye. Join OP₂ (length = √2).
    *   P₂ par OP₂ ke perpendicular P₂P₃ = 1 unit banaye. Join OP₃ (length = √3).
    *   Aise hi continue karein P₃P₄, P₄P₅... Aapko √2, √3, √4, √5... depict karta hua ek sundar spiral milega.
    *   *Task:* Spiral ko √10 tak banaye aur *evaluate* karein ki consecutive points ke beech angle kaise change ho raha hai. *Create* a table showing OPn length for n=1 to 10.

*   **Activity 2: Research π (Pi) ka Itihaas 📜:**
    *   Research karein ki π ko calculate karne ki koshish kaise shuru hui. Archimedes aur Aryabhatta ke contributions ko note karein.
    *   *Evaluate* karein ki π ke accurate value nikalne mein kya challenges the purane mathematicians ke liye.

*   **Discussion: 0.999... = 1 ?? 🤔:**
    *   Class mein discuss karein ki 0.999... (0.9̄) ko p/q form mein convert karne par 1 kyun aata hai (Example 4 hint).
    *   *Critically analyze* karein ki kya 0.999... aur 1 number line par alag points hain ya same? Apne arguments ko justify karein.

*   **Discussion: Irrationality ka Impact 🌍:**
    *   Socho aur discuss karo: Agar irrational numbers discover na hue hote, toh Maths aur Science (especially geometry, engineering) par kya *impact* padta? Kya Pythagoras theorem utna useful hota?

## 📝 Assessment Prep

*   **Case Study 1:** Ek carpenter ko ek table banana hai jiska top square hai aur area 5 square meters hai. Usko top ki side length kitni rakhni hogi? Kya yeh length ek rational number hai? Agar usko measurement lena hai, toh woh is value ko kaise approximate karega? *Evaluate* the practical difficulty.
*   **Case Study 2:** Aapko ek circular garden ke চারপাশে fence lagani hai. Aapne diameter (व्यास) measure kiya 7 meters. Circumference (परिधि) c = πd formula se nikali. Agar aap π ki value 22/7 lete hain, toh circumference kya aati hai? Agar aap π ki value 3.14 lete hain, toh kya aati hai? Actual circumference (jo πd hai) rational hai ya irrational? *Analyze* the difference between using rational approximations and the actual irrational value.
*   **Diagram Based Questions:**
    *   Number line par √5 ko accurately *locate* karke dikhayein. Steps likhein.
    *   Ek number diya hai, jaise 7.478478... (7.478). Iska decimal expansion dekh kar *classify* karein ki yeh rational hai ya irrational. Reason dein. Agar rational hai, toh p/q form mein *create* karein.
    *   Geometric construction method use karke √6.5 ko number line par *represent* karein.
*   **Problem Solving:**
    *   Simplify: (√7 + √3)²
    *   Rationalise the denominator: 1 / (√5 - √2)
    *   Simplify: (32)²/⁵
    *   Find 3 irrational numbers between 5/7 and 9/11.

## 🌏 Bharatiya Context

*   **Shunya (Zero):** Bharat ka sabse bada contribution mathematics mein '0' (zero) ka concept hai, jo Whole Numbers (पूर्ण संख्याएँ) aur Integers (पूर्णांक) ka base hai. Iske bina modern number system possible nahi tha.
*   **Aryabhatta (आर्यभट्ट):** Mahan Indian mathematician aur astronomer (476–550 CE) ne π ki value 4 decimal places tak correct nikali (3.1416). Unhone likha: "Add four to 100, multiply by eight, and then add 62,000. By this rule the circumference of a circle with a diameter of 20,000 can be approached." Isse π ≈ 62832 / 20000 = 3.1416 aata hai.
*   **Sulbasutras (शुल्बसूत्र):** Vedic period (approx 800 BC - 500 BC) ke mathematical texts hain jinmein geometric constructions ke rules hain. Inmein √2 ka ek remarkable approximation milta hai:
    √2 ≈ 1 + 1/3 + 1/(3×4) - 1/(3×4×34) ≈ 1.4142156... Yeh modern value ke kaafi close hai! Yeh dikhata hai ki ancient India mein irrational numbers ki understanding thi.
*   **Large Numbers:** India ki population approx 1.4 billion (1,400,000,000) hai. Ise scientific notation (exponents use karke) mein 1.4 × 10⁹ likh sakte hain. Yeh large numbers ko handle karne mein exponents ki utility dikhata hai.

```