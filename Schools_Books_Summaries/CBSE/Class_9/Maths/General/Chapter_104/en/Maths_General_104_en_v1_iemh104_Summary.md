# Class 9 Maths - General Chapter 104
**Language:** English

# [Class 9] Maths - Chapter 4: Linear Equations in Two Variables

## 🌟 Core Concepts

A hierarchical overview of the fundamental ideas presented:

1.  **Recall: Linear Equations in One Variable**
    *   Form: `ax + b = 0` (where `a ≠ 0`)
    *   Solution: Unique solution (e.g., for `2x + 5 = 0`, the solution is `x = -5/2`)
    *   Representation: Can be shown on a number line.
    *   Properties: Solution unaffected by adding/subtracting the same number to both sides, or multiplying/dividing both sides by the same non-zero number.

2.  **Introduction to Linear Equations in Two Variables**
    *   Motivation: Situations involving two unknown quantities (e.g., total runs scored by two batsmen).
    *   Variables: Typically denoted by `x` and `y`, but other letters can be used.
    *   **Definition:** An equation that can be written in the form `ax + by + c = 0`.
        *   `a`, `b`, `c`: Real numbers.
        *   **Crucial Condition:** `a` and `b` are not *both* zero (i.e., `a² + b² ≠ 0`).
        *   Examples: `x + y = 176`, `1.2s + 3t = 5`, `p + 4q = 7`, `2x - 7y - 3 = 0`.

3.  **Standard Form and Coefficients**
    *   Standard Form: `ax + by + c = 0`.
    *   Identifying Coefficients: Ability to rewrite given equations into standard form and identify the values of `a`, `b`, and `c`. (See Example 1).
    *   Special Cases: Equations like `ax + b = 0` or `cy + d = 0` can be expressed as linear equations in two variables (e.g., `ax + 0y + b = 0`, `0x + cy + d = 0`). (See Example 2).

4.  **Solutions of Linear Equations in Two Variables**
    *   Definition of Solution: A pair of values (one for each variable) that makes the equation true. Represented as an **ordered pair** `(x, y)`.
    *   Verification: Substituting the values of `x` and `y` into the equation to check if LHS = RHS.
    *   **Key Property:** A linear equation in two variables has **infinitely many solutions**.
    *   Finding Solutions:
        *   Choose a value for one variable (e.g., `x`).
        *   Substitute this value into the equation.
        *   Solve the resulting linear equation in one variable to find the value of the other variable (e.g., `y`).
        *   Common strategy: Set `x = 0` to find `y`, then set `y = 0` to find `x`. (See Examples 3 & 4).

## 📘 Key Learnings

**1. From One Variable to Two:**
We recall that a linear equation in one variable, like `2x + 5 = 0`, has a unique solution (`x = -5/2`), which can be plotted on a number line.

```mermaid
graph TD
    A[Equation: 2x + 5 = 0] --> B{Solve for x};
    B --> C[x = -5/2];
    C --> D(Representation on Number Line);

    subgraph Number Line Representation
        direction LR
        E(---) --- F(-3) --- G(-2.5) --- H(-2) --- I(---);
        style G fill:#f9f,stroke:#333,stroke-width:2px
        G ---|Solution: -5/2| G;
    end
    D --> E;

```
*Fig: Representation of the solution of `2x + 5 = 0` (similar to Fig 4.1 in NCERT)*

However, many real-world situations involve two related unknown quantities. For instance, if two batsmen, scoring `x` runs and `y` runs respectively, together score 176 runs, we represent this as `x + y = 176`. This is a **linear equation in two variables**.

**2. Defining and Standardising Linear Equations in Two Variables:**
Any equation that can be expressed in the form `ax + by + c = 0`, where `a`, `b`, `c` are real numbers and `a` and `b` are not both zero, is a linear equation in two variables.

*   **Standard Form:** `ax + by + c = 0`
*   **Example:** Convert `2x + 3y = 4.37` to standard form.
    *   Subtract 4.37 from both sides: `2x + 3y - 4.37 = 0`.
    *   Compare with `ax + by + c = 0`: Here, `a = 2`, `b = 3`, `c = -4.37`.
*   **Example:** Convert `x = 3y` to standard form.
    *   Subtract `3y` from both sides: `x - 3y = 0`.
    *   This can be written as `1x - 3y + 0 = 0`.
    *   Here, `a = 1`, `b = -3`, `c = 0`.
*   **Example:** Express `y = 2` as a linear equation in two variables.
    *   Rewrite as `0x + 1y = 2`.
    *   Standard form: `0x + 1y - 2 = 0`.
    *   Here, `a = 0`, `b = 1`, `c = -2`.

**3. Understanding Solutions:**
A solution is an **ordered pair `(x, y)`** that satisfies the equation. For `2x + 3y = 12`:
*   Is `(3, 2)` a solution? Substitute `x=3`, `y=2`: `2(3) + 3(2) = 6 + 6 = 12`. Yes, it is.
*   Is `(1, 4)` a solution? Substitute `x=1`, `y=4`: `2(1) + 3(4) = 2 + 12 = 14`. No, `14 ≠ 12`.
*   Is `(0, 4)` a solution? Substitute `x=0`, `y=4`: `2(0) + 3(4) = 0 + 12 = 12`. Yes, it is.
*   Is `(6, 0)` a solution? Substitute `x=6`, `y=0`: `2(6) + 3(0) = 12 + 0 = 12`. Yes, it is.

**4. Infinitely Many Solutions:**
Unlike linear equations in one variable, linear equations in two variables have **infinitely many solutions**. We can find solutions by choosing a value for one variable and calculating the corresponding value for the other.

*   **Example:** Find solutions for `x + 2y = 6`.
    1.  Choose `x = 0`: `0 + 2y = 6` => `2y = 6` => `y = 3`. Solution: `(0, 3)`.
    2.  Choose `y = 0`: `x + 2(0) = 6` => `x = 6`. Solution: `(6, 0)`.
    3.  Choose `x = 2`: `2 + 2y = 6` => `2y = 4` => `y = 2`. Solution: `(2, 2)`.
    4.  Choose `y = 1`: `x + 2(1) = 6` => `x + 2 = 6` => `x = 4`. Solution: `(4, 1)`.
    We can continue this process indefinitely to find more solutions like `(-2, 4)`, `(8, -1)`, etc.

```mermaid
graph TD
    L[Linear Equation in Two Variables: ax + by + c = 0] --> M{How many solutions?};
    M --> N[Infinitely Many Solutions];
    N --> O{How to find them?};
    O --> P[Choose a value for x (or y)];
    P --> Q[Substitute the value into the equation];
    Q --> R[Solve the resulting equation for the other variable];
    R --> S[Write the solution as an ordered pair (x, y)];
    S --> O;

    subgraph Example: x + 2y = 6
        T[Choose x=0] --> U[0 + 2y = 6] --> V[y=3] --> W[(0, 3)];
        X[Choose y=0] --> Y[x + 2(0) = 6] --> Z[x=6] --> AA[(6, 0)];
        AB[Choose x=2] --> AC[2 + 2y = 6] --> AD[y=2] --> AE[(2, 2)];
    end
    S --> T;
    S --> X;
    S --> AB;
```
*Fig: Process of finding solutions for a linear equation in two variables.*

## 🧩 Active Learning

**Activity: Modelling Real-World Costs 🔍**

1.  **Scenario:** Recall the statement: "The cost of a notebook is twice the cost of a pen." If the cost of a notebook is `₹ x` and the cost of a pen is `₹ y`, the equation is `x = 2y` or `x - 2y = 0`.
2.  **Research:** Visit a local stationery shop or check online stores. Find the actual cost of a specific type of notebook (`x`) and a specific type of pen (`y`).
3.  **Analysis:**
    *   Do the prices you found satisfy the equation `x = 2y`?
    *   If not, what is the actual relationship? Can you write a different linear equation relating them (perhaps involving multiple notebooks and pens, like `2x + 5y = Total Cost`)?
    *   Find three different pairs of `(notebook_cost, pen_cost)` from different brands/types. Do any of these pairs satisfy `x = 2y`?
4.  **Extension:** Think of another real-world scenario involving two quantities with a linear relationship (e.g., cost of apples and oranges, distance travelled at constant speed over time). Formulate a linear equation in two variables for it. Find at least two possible solutions for your equation.

**Discussion: Interpreting Solutions in Context 🌍**

Consider the India-Sri Lanka cricket match example: `x + y = 176`, where `x` and `y` are runs scored by two batsmen.
1.  We know `(100, 76)`, `(88, 88)`, `(176, 0)` are some possible solutions. Are these practically valid in a cricket match? (Yes)
2.  Mathematically, we can also find solutions like:
    *   `x = 200`, then `200 + y = 176` => `y = -24`. Solution: `(200, -24)`.
    *   `x = 100.5`, then `100.5 + y = 176` => `y = 75.5`. Solution: `(100.5, 75.5)`.
3.  **Critical Analysis:**
    *   Are the solutions `(200, -24)` and `(100.5, 75.5)` practically possible in the context of runs scored in cricket? Why or why not?
    *   What constraints does the real-world context (cricket scores) place on the possible values of `x` and `y`? (Runs must be non-negative integers).
    *   While the equation `x + y = 176` has infinitely many mathematical solutions, how many *practical* solutions does it have in this specific context? Discuss the difference between mathematical solutions and contextually relevant solutions.

## 📝 Assessment Prep

Focus on mastering the following types of problems, often presented as case studies or direct questions:

1.  **Formulating Equations:** Translating word problems into linear equations in two variables.
    *   *Case Study Example:* The total cost of 5 kg of sugar and 2 kg of flour is ₹ 350. If the cost per kg of sugar is `₹ x` and the cost per kg of flour is `₹ y`, write a linear equation to represent this information. (Answer: `5x + 2y = 350`)
    *   Practice Exercise 4.1, Question 1.

2.  **Standard Form and Coefficients:** Expressing given equations in the form `ax + by + c = 0` and identifying `a`, `b`, and `c`.
    *   *Example:* Express `3x = 8 - 2y` in standard form and find a, b, c. (Answer: `3x + 2y - 8 = 0`; `a=3`, `b=2`, `c=-8`)
    *   Practice Exercise 4.1, Question 2.

3.  **Verifying Solutions:** Checking if a given ordered pair `(x, y)` is a solution to a given equation.
    *   *Example:* Is `(2, 0)` a solution for `x - 2y = 4`? (Check: `2 - 2(0) = 2 ≠ 4`. No.)
    *   Practice Exercise 4.2, Question 3.

4.  **Finding Solutions:** Determining multiple solutions for a given linear equation in two variables.
    *   *Example:* Find three different solutions for `2x + y = 7`. (Possible answers: `(0, 7)`, `(1, 5)`, `(3, 1)`)
    *   Practice Exercise 4.2, Question 2.

5.  **Finding Unknown Constants:** Using a given solution to find the value of a constant in the equation.
    *   *Example:* If `x = 2, y = 1` is a solution of `2x + 3y = k`, find `k`. (Solution: `2(2) + 3(1) = 4 + 3 = 7`. So, `k = 7`)
    *   Practice Exercise 4.2, Question 4.

*(Note: Diagrams are primarily used for conceptual understanding (like the number line) at this stage. Graphical representation of two-variable equations comes later.)*

## 🌏 Bharatiya Context

Linear equations in two variables are useful for modelling various simple scenarios relevant to India:

1.  **Sports Statistics:** The example `x + y = 176` directly relates to a cricket match involving India, a hugely popular sport. Similar equations can model partnerships, total wickets taken by two bowlers, etc.
2.  **Everyday Economics:** The notebook (`₹ x`) and pen (`₹ y`) cost problem (`x = 2y` or variations) is relatable to students' daily expenses in India. This can be extended:
    *   **Budgeting:** A family spends a fixed amount, say ₹ 5000, monthly on rice (`x` kg at `₹ R` per kg) and wheat (`y` kg at `₹ W` per kg). The equation could be `R*x + W*y = 5000`. Discussing prices `R` and `W` can involve looking at data from the Public Distribution System (PDS) or local market rates.
    *   **Small Businesses:** A street vendor sells `x` plates of idli at `₹ I` per plate and `y` plates of dosa at `₹ D` per plate. If their total revenue is `₹ T`, the equation is `I*x + D*y = T`.
3.  **Social Schemes:** While often more complex, simple models can be illustrative. For instance, under a scheme like MNREGA, if the daily wage is `₹ W_m` for men and `₹ W_w` for women, and a household has `m` men working for `d_m` days and `w` women working for `d_w` days, the total earning `E` could be modelled in parts, sometimes simplifying to linear relationships depending on the knowns and unknowns. For example, if total person-days are fixed, say `d_m + d_w = 50`, this is a linear equation.

These examples help connect the abstract mathematical concept to tangible, culturally relevant situations within India, enhancing understanding and application.