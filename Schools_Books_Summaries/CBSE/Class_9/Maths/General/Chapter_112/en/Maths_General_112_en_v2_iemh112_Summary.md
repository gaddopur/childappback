# Class 9 Maths - General Chapter 112
**Language:** English

```markdown
# [Class 9] Maths - Chapter 12: Statistics (Graphical Representation of Data)

## 🌟 Core Concepts

📊 **Graphical Representation of Data**
   - Purpose: Provides a visual understanding and comparison of data, often clearer than tables. "One picture is better than a thousand words."
   - Types Covered:
     1.  **Bar Graphs:** For comparing discrete categories.
     2.  **Histograms:** For representing continuous grouped frequency distributions.
         - Uniform Width
         - Varying Widths
     3.  **Frequency Polygons:** For visualizing continuous data trends, especially for comparison.

   ```mermaid
   graph TD
       A[Graphical Representation] --> B(Bar Graphs);
       A --> C(Histograms);
       A --> D(Frequency Polygons);
       C --> C1(Uniform Width);
       C --> C2(Varying Widths);
       C -- Leads to --> D;
       D -- Can be drawn from --> C;
       D -- Can be drawn using --> E(Class Marks);

       subgraph Key Elements
           F(Variable)
           G(Frequency / Value)
           H(Class Intervals)
           I(Class Marks)
           J(Width of Bars/Rectangles)
           K(Height/Length of Bars/Rectangles)
           L(Area Proportionality in Histograms)
       end

       B -- Uses --> F & G;
       C -- Uses --> H & G;
       C2 -- Requires --> L & Adjustment_of_Lengths;
       D -- Uses --> I & G;
   ```

## 📘 Key Learnings

**1. Bar Graphs**

*   **Purpose:** To compare individual items or categories visually.
*   **Construction:**
    *   Draw bars of **uniform width** on one axis (e.g., x-axis) representing the variable (categories), with **equal spacing** between them.
    *   Represent the corresponding values (frequencies) on the other axis (e.g., y-axis).
    *   The **height** of each bar is proportional to the value it represents.
*   **Example (Ref: Example 2, Fig 12.2):** Representing monthly expenditure of a family under different heads (Grocery, Rent, Education, etc.). The heights of the bars clearly show relative spending (e.g., Education expenditure is much higher than Medicine).
    📈 Diagram Sketch: Bars for Grocery (height 4), Rent (5), Education (5), Medicine (2), etc., with equal widths and gaps.

**2. Histograms**

*   **Purpose:** To represent the frequency distribution of **continuous** data grouped into class intervals.
*   **Key Difference from Bar Graphs:** Used for continuous data, bars (rectangles) are drawn adjacent to each other (**no gaps**), and the **width** of the bars represents the class interval size.
*   **Construction (Uniform Width - Ref: Table 12.2, Fig 12.3):**
    *   Represent class intervals on the horizontal axis (x-axis). Use a **kink** (break mark) if the scale doesn't start from zero.
    *   Represent frequencies on the vertical axis (y-axis).
    *   Draw rectangles with widths equal to the class size and heights proportional to the corresponding frequencies.
    *   Since widths are equal, **heights are directly proportional to frequencies**.
    *   The **area** of each rectangle is proportional to its frequency.
    📈 Diagram Sketch: Adjacent rectangles for weight intervals (30.5-35.5, 35.5-40.5, etc.) with heights corresponding to the number of students (9, 6, 15, etc.).

*   **Construction (Varying Widths - Ref: Example 3, Table 12.3/12.4, Fig 12.5):**
    *   **Problem:** If class intervals have different widths, drawing rectangles with heights equal to frequency gives a misleading picture because the **area** must be proportional to the frequency.
    *   **Solution:** Adjust the lengths (heights) of the rectangles.
        1.  Identify the **minimum class size**.
        2.  Calculate the **adjusted frequency (length of rectangle)** for each class using the formula:
            `Adjusted Frequency = (Frequency of the class / Width of the class) * Minimum Class Size`
        3.  Draw rectangles with the original class widths but use the **adjusted frequencies** as their heights.
    *   **Example:** For marks interval 0-20 (width 20, frequency 7) and minimum width 10, the adjusted length is (7/20) * 10 = 3.5. For 70-100 (width 30, frequency 8), adjusted length is (8/30) * 10 ≈ 2.67.
    📈 Diagram Sketch: Adjacent rectangles with varying widths (e.g., 0-20, 20-30, ..., 70-100) and heights adjusted as calculated (3.5, 10, 10, 20, 20, 15, 2.67).

**3. Frequency Polygons**

*   **Purpose:** Another way to represent grouped frequency distributions (continuous data), especially useful for comparing two datasets.
*   **Construction Methods:**
    1.  **Using Histogram:**
        *   Draw a histogram.
        *   Mark the **mid-points** of the top sides of adjacent rectangles.
        *   Join these mid-points using line segments.
        *   To close the polygon, join the first mid-point to the mid-point of an imaginary preceding class interval (with frequency 0) on the horizontal axis, and similarly join the last mid-point to the mid-point of an imaginary succeeding class interval (with frequency 0). (Ref: Fig 12.6)
    2.  **Without Histogram (Using Class Marks - Ref: Example 5, Fig 12.8):**
        *   Calculate the **class mark** for each class interval:
            `Class Mark = (Upper Limit + Lower Limit) / 2`
        *   Plot the points with class marks on the horizontal axis and corresponding frequencies on the vertical axis. (e.g., (145, 5), (155, 10), ...)
        *   Join these plotted points using line segments.
        *   Close the polygon by plotting points corresponding to the class marks of imaginary preceding and succeeding classes with frequency 0. (e.g., (135, 0) and (205, 0)).
*   **Key Feature:** The area under the frequency polygon is equal to the area of the corresponding histogram.
*   **Usefulness:** Effective for comparing distributions, like the performance of two different sections of a class on the same test (Ref: Exercise 12.1, Q6).
    📈 Diagram Sketch: Points plotted at (Class Mark, Frequency) and joined by lines, starting and ending on the x-axis.

## 🧩 Active Learning

*   **Activity: Research-based Case Study Analysis 🔍**
    *   Select data from Exercise 12.1, such as Q2 (Number of girls per thousand boys in different sections of Indian society) or Q1 (Female fatality causes).
    *   Represent this data using a suitable graph (Bar Graph for Q1/Q2).
    *   Research potential socio-economic factors contributing to the trends observed (e.g., reasons for varying sex ratios across sections, factors behind reproductive health conditions being a major cause of female fatality). Present findings alongside the graph.
*   **Discussion: Critical Analysis of Real-World Impacts 🌍**
    *   Using the bar graph created for Exercise 12.1 Q2 (Girls per thousand boys), discuss the social implications of the observed disparities between different sections (SC, ST, Non-SC/ST, Rural, Urban, etc.) in India.
    *   Analyze the histogram from Example 3 (student test performance with varying intervals). Discuss how the initial, unadjusted histogram (Fig 12.4) could lead to incorrect conclusions about student performance compared to the correctly adjusted histogram (Fig 12.5). Why is accurate data representation crucial?
    *   Discuss the utility of frequency polygons in comparing performance, e.g., using Exercise 12.1 Q6 (comparing two sections) or Q7 (comparing two cricket teams).

## 📝 Assessment Prep

*   **Case Studies & Diagrams 📝:**
    *   Be prepared to **construct** Bar Graphs, Histograms (both uniform and varying widths), and Frequency Polygons from given frequency distribution tables. Pay attention to choosing appropriate scales, labeling axes, using kinks where necessary, and calculating adjusted frequencies for histograms with varying widths.
    *   Practice **interpreting** given graphs:
        *   Reading values from Bar Graphs (e.g., Example 1).
        *   Identifying intervals with maximum/minimum frequencies from Histograms.
        *   Calculating the number of data points within a certain range from a Histogram (e.g., Exercise 12.1, Q5 - lamps with lifetime > 700 hours).
        *   Comparing distributions using Frequency Polygons (e.g., Exercise 12.1, Q6 & Q7).
    *   Understand the concept of **class marks** and their use in drawing frequency polygons independently.
    *   Know when to use each type of graph (Bar graph for discrete categories, Histogram/Frequency Polygon for continuous data).
    *   Be able to convert discontinuous class intervals to continuous ones before drawing a histogram (e.g., Exercise 12.1, Q4 - leaf lengths). [Hint: Subtract 0.5 from lower limits and add 0.5 to upper limits].

## 🌏 Bharatiya Context

This chapter uses several examples relevant to the Indian context to illustrate statistical concepts:

1.  **Family Expenditure (Example 2):** Planning monthly expenses (`₹20,000` income) on heads like Grocery, Rent, Education, Medicine, common in Indian households.
2.  **Demographic Data (Exercise 12.1, Q2):** Analyzing the number of girls per thousand boys across different sections of **Indian society** (Scheduled Caste (SC), Scheduled Tribe (ST), Non-SC/ST, Backward/Non-backward districts, Rural/Urban). This data highlights social indicators and regional disparities within India. 📊
3.  **State Elections (Exercise 12.1, Q3):** Representing seats won by different political parties (A, B, C, D, E, F) in a **state assembly election**, a common scenario in India's democratic process.
4.  **Cost of Living Index (Example 5):** Tracking the weekly cost of living index in an **Indian city**, reflecting economic trends relevant to the population. 📊
```