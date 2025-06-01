# Class 9 Maths - General Chapter 109
**Language:** English

```markdown
# [Class 9] Maths - Chapter 9: Circles

## 🌟 Core Concepts

This chapter delves into the properties of circles and their components like chords, arcs, and angles.

1.  **Introduction to Circles & Chords**
    *   Definition of a Circle: Collection of points equidistant from a fixed point (centre).
    *   Chord: Line segment joining any two points on the circle.
    *   Arc: A piece of the circle between two points. (Minor arc, Major arc, Semicircle)
    *   Segment: Region between a chord and either of its arcs. (Minor segment, Major segment)
    *   Angle Subtended by a Chord/Arc: Angle formed at a point (centre or on the circle) by the lines joining the point to the endpoints of the chord/arc.

2.  **Relationship between Chords and Angles at the Centre**
    *   Theorem 9.1: Equal chords subtend equal angles at the centre.
    *   Theorem 9.2 (Converse of 9.1): If angles subtended by chords at the centre are equal, the chords are equal.

3.  **Perpendicular from the Centre to a Chord**
    *   Theorem 9.3: The perpendicular from the centre of a circle to a chord bisects the chord.
    *   Theorem 9.4 (Converse of 9.3): The line drawn through the centre of a circle to bisect a chord is perpendicular to the chord.

4.  **Relationship between Chords and their Distances from the Centre**
    *   Distance of a point from a line: Length of the perpendicular from the point to the line.
    *   Theorem 9.5: Equal chords of a circle (or congruent circles) are equidistant from the centre (or centres).
    *   Theorem 9.6 (Converse of 9.5): Chords equidistant from the centre of a circle are equal in length.

5.  **Angles Subtended by Arcs**
    *   Congruent Arcs: Arcs that superimpose completely. Equal chords correspond to congruent arcs and vice-versa.
    *   Angle Subtended by an Arc: Angle at the centre (or reflex angle for major arc); Angle at any point on the remaining part of the circle.
    *   Theorem 9.7: The angle subtended by an arc at the centre is double the angle subtended by it at any point on the remaining part of the circle.

6.  **Angles in Segments**
    *   Theorem 9.8: Angles in the same segment of a circle are equal.
    *   Special Case: Angle in a semicircle is a right angle (90°).
    *   Theorem 9.9 (Converse of 9.8): If a line segment joining two points subtends equal angles at two other points on the same side of the line, the four points are concyclic (lie on a circle).

7.  **Cyclic Quadrilaterals**
    *   Definition: A quadrilateral whose vertices all lie on a circle.
    *   Theorem 9.10: The sum of either pair of opposite angles of a cyclic quadrilateral is 180°.
    *   Theorem 9.11 (Converse of 9.10): If the sum of a pair of opposite angles of a quadrilateral is 180°, the quadrilateral is cyclic.

## 📘 Key Learnings

**1. Chords and Angles at the Centre:**
*   **Theorem 9.1:** If chords AB and CD are equal (AB = CD), then the angles they subtend at the centre O are equal (∠AOB = ∠COD). This is proven using SSS congruence between ∆AOB and ∆COD (OA=OC, OB=OD radii; AB=CD given).
    ```mermaid
    graph TD
        subgraph Circle with Centre O
            A --- B
            C --- D
            O --- A
            O --- B
            O --- C
            O --- D
        end
        style A fill:#fff,stroke:#333,stroke-width:2px
        style B fill:#fff,stroke:#333,stroke-width:2px
        style C fill:#fff,stroke:#333,stroke-width:2px
        style D fill:#fff,stroke:#333,stroke-width:2px
        style O fill:#f9f,stroke:#333,stroke-width:2px
    ```
    *Diagram Concept for Th 9.1/9.2: Equal Chords AB, CD subtend angles AOB, COD at centre O.*
*   **Theorem 9.2 (Converse):** If ∠AOB = ∠COD, then AB = CD. Proven using SAS congruence (OA=OC, OB=OD radii; ∠AOB = ∠COD given).

**2. Perpendicular Bisector of a Chord:**
*   **Theorem 9.3:** If OM ⊥ AB, where O is the centre and AB is a chord, then M is the midpoint of AB (AM = MB). Proven using RHS congruence between ∆OAM and ∆OMB (OA=OB radii; OM common; ∠OMA = ∠OMB = 90°).
    ```mermaid
    graph TD
        subgraph Circle with Centre O
            A --- M --- B
            O --- M
            O --- A
            O --- B
        end
        style A fill:#fff,stroke:#333,stroke-width:2px
        style B fill:#fff,stroke:#333,stroke-width:2px
        style M fill:#fff,stroke:#333,stroke-width:1px
        style O fill:#f9f,stroke:#333,stroke-width:2px
    ```
    *Diagram Concept for Th 9.3/9.4: OM is perpendicular to/bisects chord AB.*
*   **Theorem 9.4 (Converse):** If M is the midpoint of chord AB, then OM ⊥ AB. Proven using SSS congruence between ∆OAM and ∆OMB (OA=OB radii; AM=BM given; OM common), leading to ∠OMA = ∠OMB. Since they form a linear pair, each must be 90°.

**3. Chord Length and Distance from Centre:**
*   The distance of a chord from the centre is the length of the perpendicular from the centre to the chord.
*   **Theorem 9.5:** If AB = CD, then their distances from the centre O are equal (OM = ON, where OM ⊥ AB, ON ⊥ CD).
*   **Theorem 9.6 (Converse):** If OM = ON, then AB = CD.
    *   *Key Idea:* Longer chords are closer to the centre. The diameter is the longest chord and its distance from the centre is zero.

**4. Arcs and Angles:**
*   Equal chords cut off congruent arcs. Congruent arcs subtend equal angles at the centre.
*   **Theorem 9.7:** ∠POQ = 2 ∠PAQ, where arc PQ subtends ∠POQ at the centre O and ∠PAQ at point A on the remaining part of the circle.
    ```mermaid
    graph TD
        subgraph Circle with Centre O
            P --- Q
            O --- P
            O --- Q
            A --- P
            A --- Q
        end
        style P fill:#fff,stroke:#333,stroke-width:2px
        style Q fill:#fff,stroke:#333,stroke-width:2px
        style A fill:#fff,stroke:#333,stroke-width:2px
        style O fill:#f9f,stroke:#333,stroke-width:2px
    ```
    *Diagram Concept for Th 9.7: Arc PQ subtends ∠POQ at centre O and ∠PAQ at point A.*
    *   This holds for minor arcs (∠POQ < 180°), semicircles (∠POQ = 180°), and major arcs (reflex ∠POQ).

**5. Angles in Segments:**
*   **Theorem 9.8:** Angles subtended by the same arc (or in the same segment) at different points on the remaining part of the circle are equal. (e.g., ∠PAQ = ∠PBQ).
*   **Angle in a Semicircle:** The angle subtended by a diameter at any point on the circumference is a right angle (90°). This is a special case of Th 9.7 where the angle at the centre is 180°.
*   **Theorem 9.9 (Concyclicity):** If points C and D lie on the same side of line segment AB such that ∠ACB = ∠ADB, then A, B, C, D are concyclic.

**6. Cyclic Quadrilaterals:**
*   **Theorem 9.10:** In a cyclic quadrilateral ABCD, opposite angles sum to 180° (∠A + ∠C = 180° and ∠B + ∠D = 180°).
    ```mermaid
    graph TD
        subgraph Circle
            A --- B --- C --- D --- A
        end
        style A fill:#fff,stroke:#333,stroke-width:2px
        style B fill:#fff,stroke:#333,stroke-width:2px
        style C fill:#fff,stroke:#333,stroke-width:2px
        style D fill:#fff,stroke:#333,stroke-width:2px
    ```
    *Diagram Concept for Th 9.10/9.11: Cyclic Quadrilateral ABCD.*
*   **Theorem 9.11 (Converse):** If a pair of opposite angles of a quadrilateral sum to 180°, it is cyclic.

## 🧩 Active Learning

*   **Activity: Research-based Case Study Analysis 🔍**
    *   Select examples of circular designs in Indian architecture (e.g., the old Indian Parliament House, Ashoka Chakra, stupas like Sanchi Stupa, city planning like Connaught Place in Delhi) or engineering (e.g., wheels, gears, circular parks).
    *   Research the dimensions (radius, chord lengths if applicable).
    *   Analyze how properties like equal chords implying equal angles/distances, or angles in segments, might have been relevant in their design or function. For instance, how does the equal spacing of the 24 spokes in the Ashoka Chakra relate to Theorem 9.1? How is the concept of 'centre' crucial in these designs?
    *   Prepare a short report evaluating the application of circle theorems in these real-world examples.

*   **Discussion: Critical Analysis of Real-World Impacts 🌍**
    *   Discuss: Why is Theorem 9.7 (angle at centre is double the angle at circumference) fundamental in fields like optics (lens design) or astronomy (calculating positions)?
    *   Evaluate the importance of cyclic quadrilateral properties (Theorem 9.10/9.11). How might these properties be used in designing structures or mechanisms that involve linked components moving on a circular path?
    *   Consider the problem of locating an epicentre of an earthquake using data from three seismograph stations. How do the concepts of circles and distances (related to perpendicular bisectors of chords) play a role? (Connecting to locating the centre of a circle passing through three non-collinear points).

## 📝 Assessment Prep

*   Focus on understanding and applying the theorems (9.1 - 9.11).
*   Practice problems involving calculations of angles and lengths related to chords, arcs, segments, and cyclic quadrilaterals.
*   Be prepared to provide reasons (citing theorems) for steps in proofs.
*   Expect questions based on diagrams, requiring identification of relevant properties.
*   Case studies similar to Example 1 (intersecting chords and diameter), Example 2 (angles in a circle with chord equal to radius), Example 3 (angles in cyclic quadrilateral), Example 4 (intersecting circles and diameters), and Example 5 (angle bisectors of a quadrilateral forming a cyclic quadrilateral) are important.
*   Diagrams are crucial. Practice drawing clear diagrams for given problems. Pay attention to details like centre, radii, chords, perpendiculars, and points on the circle.

## 🌏 Bharatiya Context

*   **Ashoka Chakra:** The 24 spokes in the Ashoka Chakra divide the circle into 24 equal arcs. By Theorem 9.2, the chords connecting the endpoints of these arcs would be equal. By Theorem 9.1, each spoke subtends an equal angle at the centre (360°/24 = 15°). This reflects principles of equality and uniformity.
*   **Circular Parks & Community Spaces:** Problems like Ex 9.2, Q5 (Reshma, Salma, Mandip) and Q6 (Ankur, Syed, David) are set in Indian parks/colonies. Solving these involves applying theorems about chords (equal chords equidistant from centre, perpendicular from centre bisects chord) and potentially coordinate geometry or trigonometry in practical settings common in India.
*   **Traditional Art & Design (Rangoli/Kolam):** Many traditional Indian floor designs use concentric circles, arcs, and symmetrical patterns. The creation of these often intuitively uses concepts like equal arcs, angles at the centre, and symmetry, which are formalized in circle theorems. The precision required relates to properties like equidistant chords being equal.
*   **Astronomy & Timekeeping (Historical):** Ancient Indian astronomers like Aryabhata made significant contributions involving calculations related to circles and chords (like creating tables of sines, which relate to half-chords). Instruments like the Jantar Mantar observatories (e.g., in Delhi and Jaipur) use large circular and semi-circular structures for astronomical measurements, relying heavily on the geometry of circles and angles.
```