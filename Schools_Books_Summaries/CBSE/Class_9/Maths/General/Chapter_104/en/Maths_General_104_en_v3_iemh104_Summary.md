# Class 9 Maths - General Chapter 104
**Language:** English

```markdown
# [Class 9] Maths - Chapter 4: Linear Equations in Two Variables

## 🌟 Core Concepts

1.  **Recap: Linear Equations in One Variable:**
    *   Equations like `ax + b = 0` where `a ≠ 0`.
    *   Have a unique solution (e.g., for `2x + 5 = 0`, the solution is `x = -5/2`).
    *   Solution can be represented on a number line.

2.  **Introduction to Linear Equations in Two Variables:**
    *   Situations involving two unknown quantities that have a linear relationship.
    *   Example: Two batsmen score 176 runs together. If their scores are `x` and `y`, the equation is `x + y = 176`.

3.  **Definition:**
    *   An equation that can be written in the form **`ax + by + c = 0`** is called a linear equation in two variables.
    *   `x` and `y` are the **variables**.
    *   `a`, `b`, and `c` are **real numbers**.
    *   Crucial condition: **`a` and `b` are not both zero** (i.e., `a² + b² ≠ 0`).

4.  **Standard Form:**
    *   The form `ax + by + c = 0` is the standard form.
    *   Any linear equation in two variables can be expressed in this form.

5.  **Solutions of a Linear Equation in Two Variables:**
    *   A solution is a **pair of values**, one for `x` and one for `y`, that makes the equation true.
    *   A solution is written as an **ordered pair `(x, y)`**.
    *   Example: For `2x + 3y = 12`, the pair `(3, 2)` is a solution because `2(3) + 3(2) = 6 + 6 = 12`.
    *   **Infinitely Many Solutions:** Unlike linear equations in one variable, a linear equation in two variables has infinitely many solutions.

6.  **Representing One-Variable Equations in Two Variables:**
    *   Equations like `ax + b = 0` can be written as `ax + 0y + b = 0`.
    *   Equations like `by + c = 0` can be written as `0x + by + c = 0`.
    *   Example: `x = -5` can be written as `1x + 0y + 5 = 0`. `y = 2` can be written as `0x + 1y - 2 = 0`.

## 📘 Key Learnings

1.  **Identifying and Standardizing Equations:**
    *   Recognize if an equation is a linear equation in two variables.
    *   Rewrite any given linear equation in two variables into the standard form `ax + by + c = 0`.
    *   Identify the values of `a`, `b`, and `c` after converting to standard form.
    *   **Example (from NCERT Example 1):**
        *   Given: `x - 4 = √3y`
        *   Rearrange: `x - √3y - 4 = 0`
        *   Standard Form: `1x + (-√3)y + (-4) = 0`
        *   Here, `a = 1`, `b = -√3`, `c = -4`.
        *   *Note:* The equation `4 = 5x - 3y` can be written as `5x - 3y - 4 = 0` (`a=5, b=-3, c=-4`) OR `-5x + 3y + 4 = 0` (`a=-5, b=3, c=4`). Both are valid representations.

2.  **Understanding Solutions:**
    *   A solution `(x, y)` must satisfy the equation (make the Left Hand Side equal to the Right Hand Side).
    *   **Verification:** To check if a pair `(p, q)` is a solution for `ax + by + c = 0`, substitute `x = p` and `y = q` into the equation. If `ap + bq + c = 0` holds true, then `(p, q)` is a solution.
    *   **Example:** Is `(1, 4)` a solution for `2x + 3y = 12`?
        *   Substitute: `2(1) + 3(4) = 2 + 12 = 14`.
        *   Since `14 ≠ 12`, `(1, 4)` is **not** a solution.
    *   **Example:** Is `(6, 0)` a solution for `2x + 3y = 12`?
        *   Substitute: `2(6) + 3(0) = 12 + 0 = 12`.
        *   Since `12 = 12`, `(6, 0)` **is** a solution.

3.  **Finding Solutions:**
    *   Since there are infinitely many solutions, we can find them by choosing a value for one variable and calculating the corresponding value for the other variable.
    *   **Method:**
        1.  Choose any real value for `x` (or `y`). Often easy choices are `x=0` or `y=0`.
        2.  Substitute this chosen value into the equation.
        3.  The equation reduces to a linear equation in one variable. Solve it for the other variable.
        4.  Write the solution as an ordered pair `(x, y)`.
        5.  Repeat with different chosen values to find more solutions.
    *   **Example (Finding solutions for `x + 2y = 6`):**
        *   Let `x = 0`: `0 + 2y = 6` => `2y = 6` => `y = 3`. Solution: `(0, 3)`.
        *   Let `y = 0`: `x + 2(0) = 6` => `x = 6`. Solution: `(6, 0)`.
        *   Let `x = 2`: `2 + 2y = 6` => `2y = 4` => `y = 2`. Solution: `(2, 2)`.
        *   Let `y = 1`: `x + 2(1) = 6` => `x + 2 = 6` => `x = 4`. Solution: `(4, 1)`.

    *   **Diagrammatic Representation (Conceptual Flow):**
        ```mermaid
        graph LR
            A[Start with Eq: ax + by + c = 0] --> B{Choose a value for x (e.g., x=p)};
            B --> C{Substitute x=p: ap + by + c = 0};
            C --> D{Solve for y: y = (-ap - c) / b};
            D --> E[Found Solution (p, q) where q = (-ap - c) / b];
            A --> F{Choose a value for y (e.g., y=q)};
            F --> G{Substitute y=q: ax + bq + c = 0};
            G --> H{Solve for x: x = (-bq - c) / a};
            H --> I[Found Solution (p, q) where p = (-bq - c) / a];
        ```

## 🧩 Active Learning

1.  **Activity: Modelling Real-World Costs (Research-based Case Study)** 🔍
    *   **Scenario:** Imagine the government's Midday Meal Scheme in a school. Suppose the cost of providing a meal with `x` grams of rice and `y` grams of dal per child is fixed. Let the cost of rice be ₹R per kg and dal be ₹D per kg. The total cost of ingredients per child per meal is ₹C.
    *   **Task:**
        1.  Research approximate costs (₹/kg) for rice and dal commonly used in such schemes in your region (or use hypothetical but realistic values, e.g., Rice ₹30/kg, Dal ₹100/kg).
        2.  Assume a target ingredient cost per child, say ₹C = ₹5.00.
        3.  Remember to convert costs to ₹/gram (e.g., ₹30/kg = ₹0.03/g).
        4.  Formulate a linear equation in two variables (`x` grams of rice, `y` grams of dal) representing the total cost: `(Cost per gram of Rice) * x + (Cost per gram of Dal) * y = C`.
        5.  Find at least three different possible combinations (solutions `(x, y)`) of rice and dal quantities (in grams) that meet the target cost.
        6.  **Evaluate:** Are all mathematical solutions practical? (e.g., can you have negative grams? Should there be minimum nutritional requirements?)

2.  **Discussion: Interpreting Infinite Solutions** 🌍
    *   Consider the equation from the NCERT text: `x + y = 176` (runs scored by two Indian batsmen).
    *   Mathematically, this equation has infinite solutions (e.g., (177, -1), (80.5, 95.5), (100, 76), (0, 176)).
    *   **Critically Analyze:**
        *   Why does the mathematical model yield infinite solutions?
        *   What are the *real-world constraints* in this cricket scenario? (Scores must be non-negative integers).
        *   How do these constraints limit the number of *practical* or *valid* solutions compared to the infinite mathematical solutions?
        *   If the total score was different, say `x + y = 50`, how would the set of practical solutions change? Does the concept of "infinitely many solutions" still apply mathematically?

## 📝 Assessment Prep

1.  **Standard Form & Coefficients:**
    *   Express `3x = 8 - 2y` in the form `ax + by + c = 0` and state the values of `a`, `b`, and `c`.
    *   Write the equation `y/3 - x/2 = 1` in standard form and identify `a`, `b`, and `c`.
    *   Write `x = -7` as a linear equation in two variables.

2.  **Finding Solutions:**
    *   Find four different solutions for the equation `2x - y = 5`.
    *   Find two solutions for the equation `πx + 2y = 8`.
    *   Find two solutions for the equation `3x - 9 = 0` when written as an equation in two variables.

3.  **Verifying Solutions:**
    *   Check which of the following points are solutions to the equation `x - 3y = 7`:
        *   (7, 0)
        *   (1, -2)
        *   (4, -1)
        *   (10, 1)

4.  **Problem Solving & Modelling (Case Studies):**
    *   **Case Study 1 (Cost):** The cost of 5 kg of sugar (`x` per kg) and 2 kg of tea (`y` per kg) is ₹550. Write a linear equation to represent this. If sugar costs ₹40/kg, find the cost of tea per kg.
    *   **Case Study 2 (Geometry):** The perimeter of a rectangular park is 200m. If the length is `l` metres and the breadth is `b` metres, write a linear equation in two variables for this information. Find two possible pairs of dimensions (`l`, `b`).
    *   **Case Study 3 (Parameter Finding):** Find the value of `k` if `x = -1`, `y = 2` is a solution of the equation `kx - 3y = 10`.

## 🌏 Bharatiya Context

1.  **Cricket Partnership:** The example `x + y = 176` representing the total runs scored by two Indian batsmen (e.g., in a match against Sri Lanka in Nagpur) directly relates to a popular sport in India. Discuss how different pairs of scores `(x, y)` are possible.

2.  **Classroom Stationery Costs:** Exercise 4.1 (`The cost of a notebook is twice the cost of a pen.`) is a relatable scenario for students in India. Let cost of notebook be `x` (in ₹) and cost of pen be `y` (in ₹). The equation is `x = 2y` or `x - 2y = 0`. Students can find pairs of possible costs, e.g., if a pen costs ₹10 (`y=10`), a notebook costs ₹20 (`x=20`). Solution: `(20, 10)`. If a pen costs ₹15 (`y=15`), a notebook costs ₹30 (`x=30`). Solution: `(30, 15)`.

3.  **Budgeting for Essentials:** A family buys `x` kg of rice and `y` kg of wheat per month. Suppose rice costs ₹35/kg and wheat costs ₹25/kg. If their monthly budget for these two items is ₹1500, the equation is `35x + 25y = 1500`.
    *   **Evaluate:** Find three possible combinations `(x, y)` of rice and wheat they can buy within this budget. For example:
        *   If they buy 20 kg rice (`x=20`): `35(20) + 25y = 1500` => `700 + 25y = 1500` => `25y = 800` => `y = 32`. Solution: `(20, 32)`.
        *   If they buy 30 kg wheat (`y=30`): `35x + 25(30) = 1500` => `35x + 750 = 1500` => `35x = 750` => `x = 750/35 ≈ 21.43`. Solution: `(approx. 21.43, 30)`. Discuss if fractional kg makes sense in this context.

4.  **Social Schemes:** Consider a state government allocating funds for building `x` number of primary health centres (PHCs) and `y` number of schools. If each PHC costs ₹C1 crores and each school costs ₹C2 crores, and the total budget allocated is ₹B crores, the equation is `C1*x + C2*y = B`. Finding integer solutions `(x, y)` represents possible combinations of PHCs and schools that can be built within the budget.
```