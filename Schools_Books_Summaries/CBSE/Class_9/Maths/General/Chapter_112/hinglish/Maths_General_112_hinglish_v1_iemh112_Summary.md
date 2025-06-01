# Class 9 Maths - General Chapter 112
**Language:** Hinglish

```markdown
# [Class 9] Statistics (सांख्यिकी) - Chapter 12

## 🌟 Core Concepts (मुख्य अवधारणाएँ) 📊

1.  **Data Representation (आंकड़ों का प्रस्तुतिकरण):**
    *   Tabular Form (सारणीबद्ध रूप) - Pehle discuss kiya gaya hai.
    *   **Graphical Representation (आलेखीय निरूपण):** Data ko visually represent karna, jisse samajhna aasan ho. "Ek tasveer hazar shabdon se behtar hoti hai."
        *   Comparisons (तुलना) graphs se easy ho jaati hain.

2.  **Types of Graphical Representations (आलेखीय निरूपण के प्रकार):**
    *   **(A) Bar Graphs (दंड आलेख):**
        *   Discrete data (असतत आंकड़े) ya categories compare karne ke liye.
        *   Uniform width (समान चौड़ाई) ke bars, equal spacing (समान दूरी) ke saath.
        *   Height of bar represents the value (दंड की ऊँचाई मान दर्शाती है).
    *   **(B) Histograms (आयतचित्र):**
        *   Continuous grouped data (सतत वर्गीकृत आंकड़े) ke liye.
        *   Bars ke beech koi gap nahi hota.
        *   **Uniform Width (समान चौड़ाई वाले):** Width class size ke barabar, length frequency ke proportional. Area frequency ke proportional hota hai.
        *   **Varying Widths (बदलती चौड़ाई वाले):** Widths alag-alag ho sakti hain. Lengths ko adjust karna padta hai taki area frequency ke proportional rahe.
            *   Adjustment Formula: (Frequency / Class Width) * Minimum Class Width
        *   Kink (निकुंज) or Break on Axis: Jab data zero se start nahi hota.
    *   **(C) Frequency Polygons (बारंबारता बहुभुज):**
        *   Continuous data ke trends ko dekhne ke liye, especially large data sets ya comparison ke liye.
        *   Histogram ke rectangles ke upper sides ke mid-points ko join karke banaya jaata hai.
        *   Ya phir, class marks (वर्ग-चिह्न) aur corresponding frequencies ko plot karke banaya jaata hai.
        *   **Class Mark (वर्ग-चिह्न):** (Upper Limit + Lower Limit) / 2
        *   Polygon ko x-axis par close karne ke liye imaginary classes (zero frequency ke saath) assume ki jaati hain.

## 📘 Key Learnings (मुख्य सीख) 📈

**A. Bar Graphs (दंड आलेख):**

*   **Kya Hai?** Ye data ko represent karne ka ek pictorial tareeka hai jisme uniform width ke bars use hote hain, jinke beech equal space hota hai. Ek axis par variable (jaise months, heads) aur doosre axis par value (jaise number of students, expenditure) dikhai jaati hai. Bar ki height value par depend karti hai.
*   **Example:**
    *   Class IX ke students ke birth months ka data (Fig 12.1). Isse easily dekh sakte hain ki August mein sabse zyada students paida hue.
    *   Ek family ka monthly expenditure (Table 12.1, Fig 12.2). Graph se turant pata chalta hai ki education par kharcha medicine se double se bhi zyada hai.
*   **Kaise Banayein?**
    1.  Horizontal axis (x-axis) par variable (Heads) represent karein, equal width aur gaps ke saath.
    2.  Vertical axis (y-axis) par value (Expenditure) represent karein, suitable scale choose karke.
    3.  Har variable ke liye corresponding height ka rectangular bar banayein.

    ```
    Example: Family Expenditure Bar Graph (Fig 12.2)

      ^ Expenditure (in thousand Rs)
    6 |
    5 |    +---+       +---+
      |    |   | +---+ |   |
    4 |+---+ |   | |   | |   |
      | |   | |   | |   | |   |
    3 | |   | |   | |   | |   |    +---+
      | |   | |   | |   | |   |    |   | +---+
    2 | | G | | R | | E | | M | +---+|   | |   | +---+
      | |   | |   | |   | |   | | F || E | | M | | M |
    1 | |   | |   | |   | |   | |   || n | | i | | i |
      | +---+ +---+ +---+ +---+ +---+| t | +---+ | s |
    0 +---------------------------------------------------> Heads
       Grocery Rent Educ. Med. Fuel Ent. Misc.
    ```

**B. Histograms (आयतचित्र):**

*   **Kya Hai?** Ye grouped frequency distribution (समूहीकृत बारंबारता बंटन) ko represent karta hai jisme continuous class intervals (सतत वर्ग अंतराल) hote hain. Isme consecutive rectangles ke beech koi gap nahi hota. Area of rectangle frequency ke proportional hota hai.
*   **Uniform Width:**
    *   **Example:** Students ke weights ka data (Table 12.2, Fig 12.3).
    *   **Kaise Banayein?**
        1.  Horizontal axis par class intervals (Weights) represent karein. Agar pehla interval zero se start nahi ho raha, toh 'kink' (break mark) use karein.
        2.  Vertical axis par frequency (Number of students) represent karein.
        3.  Har class interval ke liye, width = class size aur length = frequency ka rectangle banayein. Saare rectangles adjacent honge.

    ```
    Example: Student Weights Histogram (Fig 12.3)

      ^ Number of Students
    15|         +-------+
      |         |       |
      |         |       |
    10|         |       |
      |+-------+ |       |
      ||       | |       |
    5 ||       |+-------+|       |
      ||       ||       ||       |+---+   +---+
      ||       ||       ||       ||   |   |   |
    0 +---+---+---+---+---+---+---+---+---+---+---> Weights (kg)
       ^ 30.5  35.5  40.5  45.5  50.5  55.5  60.5
     (Kink)
    ```
*   **Varying Widths:**
    *   **Problem:** Agar class widths alag-alag hain (Table 12.3), toh sirf frequency ke hisaab se length banane par graph misleading ho sakta hai (Fig 12.4), kyunki area frequency ke proportional nahi rehta.
    *   **Solution:** Rectangles ki lengths ko adjust karna padta hai.
        1.  Minimum class size pata karein (Example 3 mein 10 hai).
        2.  Har class ke liye adjusted length calculate karein: `Adjusted Length = (Frequency / Width of this class) * Minimum class size`. (Table 12.4)
        3.  Adjusted lengths use karke histogram banayein (Fig 12.5). Ab area frequency ke proportional hoga.

**C. Frequency Polygons (बारंबारता बहुभुज):**

*   **Kya Hai?** Ye quantitative data aur uski frequencies ko represent karne ka ek aur visual tareeka hai, jo line segments se bana hota hai. Ye data trends ko show karne aur do datasets ko compare karne mein useful hai.
*   **Kaise Banayein (Method 1: Using Histogram):**
    1.  Histogram banayein.
    2.  Har rectangle ke upper side ke mid-point ko mark karein.
    3.  In mid-points ko line segments se join karein (Fig 12.6).
    4.  Polygon ko close karne ke liye, pehle class interval se pehle aur last class interval ke baad, zero frequency wali imaginary classes ke mid-points ko bhi join karein (Points A and H in Fig 12.6).
*   **Kaise Banayein (Method 2: Without Histogram):**
    1.  Har class interval ka **Class Mark (वर्ग-चिह्न)** calculate karein: `Class Mark = (Upper Limit + Lower Limit) / 2`. (Table 12.7)
    2.  Horizontal axis par Class Marks aur vertical axis par Frequencies plot karein.
    3.  Points ko plot karein (Class Mark, Frequency). Jaise (145, 5), (155, 10), etc. (Example 5, Fig 12.8).
    4.  In points ko line segments se join karein.
    5.  Polygon ko close karne ke liye, pehle class mark se pehle wale imaginary class mark (frequency 0 ke saath) aur last class mark ke baad wale imaginary class mark (frequency 0 ke saath) ko plot karke join karein (Points A and H in Fig 12.8).
*   **Usefulness:** Continuous aur large data ke liye, aur do datasets ko compare karne ke liye (jaise do sections ke marks - Exercise 12.1, Q6; do teams ke runs - Q7).

## 🧩 Active Learning (सक्रिय शिक्षण)

*   **Activity (गतिविधि): Research-based Case Study Analysis (शोध-आधारित केस स्टडी विश्लेषण) 🔍**
    *   **Topic:** Bharat mein alag-alag social groups (jaise SC, ST, Non SC/ST, Rural, Urban) mein 'Number of girls per thousand boys' (Exercise 12.1, Q2 ka data) ka analysis karein.
    *   **Task:**
        1.  Is data ka ek clear Bar Graph banayein.
        2.  Graph ko dekh kar kya conclusions (निष्कर्ष) nikal sakte hain? Kis group mein ratio sabse accha hai aur kis mein sabse kam?
        3.  Apne teacher ya internet ki madad se, in differences ke possible reasons (संभावित कारण) pata karne ki koshish karein. Kya social factors, economic conditions, ya government policies ka koi role hai? Apne findings ko class mein present karein.
*   **Discussion (चर्चा): Critical Analysis of Real-world Impacts (वास्तविक दुनिया के प्रभावों का महत्वपूर्ण विश्लेषण) 🌍**
    *   **Topic:** Women's health issues worldwide (Exercise 12.1, Q1 ka data). Data ke anusaar, 'Reproductive health conditions' sabse bada cause hai (31.8%).
    *   **Questions:**
        1.  Is data ko represent karne ke liye Bar Graph kyun ek accha choice hai?
        2.  Major cause (Reproductive health conditions) ke peeche kya mukhya kaaran (factors) ho sakte hain? (Hint: Education, healthcare access, social norms, economic status). Class mein discuss karein.
        3.  Statistics (सांख्यिकी) kaise government aur health organizations ko aisi problems ko samajhne aur solve karne mein madad karti hai?

## 📝 Assessment Prep (मूल्यांकन तैयारी) 📝

*   **Focus Areas:**
    *   Diye gaye data ke liye sahi graph type (Bar Graph, Histogram, Frequency Polygon) choose karna.
    *   Graphs ko accurately construct karna (Scales, Labels, Widths, Gaps/No Gaps, Kink).
    *   **Histograms with Varying Widths:** Adjusted lengths calculate karna aur unhe correctly represent karna seekhein. (Exercise 12.1, Q8, Q9)
    *   **Frequency Polygons:** Dono methods (with and without histogram) se banana seekhein. Class marks ka concept clear rakhein. (Exercise 12.1, Q6, Q7)
    *   Graphs ko interpret karna: Maximum/minimum values, comparisons, trends, conclusions nikalna. (Exercise 12.1, Q1, Q2, Q3, Q4(iii), Q5(ii))
    *   Data ko continuous banana: Agar class intervals discontinuous hain (jaise Q4, Q7 mein), toh unhe continuous kaise banayein (e.g., 118-126, 127-135 ko 117.5-126.5, 126.5-135.5 banana).
*   **Practice:** Exercise 12.1 ke sabhi questions solve karein, especially jisme graph banana hai aur interpret karna hai. Case studies (jaise Q1, Q2, Q4, Q5) par based questions expect karein.

## 🌏 Bharatiya Context (भारतीय संदर्भ) 📊

Statistics ka use Bharat ke social aur economic aspects ko samajhne mein bahut important hai. Is chapter mein diye gaye examples Bharat se related data ko represent karte hain:

1.  **Social Demographics (सामाजिक जनसांख्यिकी):** Exercise 12.1, Q2 mein different sections of Indian society (SC, ST, Rural, Urban etc.) mein 'Number of girls per thousand boys' ka data diya gaya hai. Is tarah ke data se Child Sex Ratio (बाल लिंगानुपात) jaise important social indicators ko track kiya jaata hai, jo "Beti Bachao, Beti Padhao" jaisi sarkari yojnaon ke liye crucial hai. Graph banane se regional disparities (क्षेत्रीय असमानताएं) saaf dikhti hain.
2.  **Political Landscape (राजनीतिक परिदृश्य):** Exercise 12.1, Q3 mein State Assembly Elections ke results diye gaye hain. Bar graph se easily compare kar sakte hain ki kis party ne kitni seats jeeti. Election results ko analyse karne ke liye graphical representation ka bahut use hota hai.
3.  **Economic Indicators (आर्थिक संकेतक):** Example 5 mein ek city ka 'Cost of Living Index' (जीवन निर्वाह सूचकांक) ka weekly data diya gaya hai. Frequency polygon se index ke trend ko visualise kiya ja sakta hai. Aise data inflation (मुद्रास्फीति) aur logon ki purchasing power (क्रय शक्ति) ko samajhne mein madad karte hain, jo economic policy making ke liye zaroori hai.
4.  **Health Statistics (स्वास्थ्य सांख्यिकी):** Exercise 12.1, Q1 mein women's health conditions ka data hai. Bharat mein bhi National Family Health Survey (NFHS) jaise surveys hote hain jo health indicators par detailed data collect karte hain. In aankdon ko graphically represent karke health priorities set ki jaati hain.

In examples se pata chalta hai ki graphical representation sirf maths ka concept nahi hai, balki yeh real-world Bharatiya data ko samajhne, analyse karne aur us par based decisions lene ka ek powerful tool hai.
```