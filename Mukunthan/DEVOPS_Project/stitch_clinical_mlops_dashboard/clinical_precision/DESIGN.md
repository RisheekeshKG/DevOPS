# Design System Strategy: Clinical Precision & Editorial Calm

## 1. Overview & Creative North Star
**The Creative North Star: "The Clinical Curator"**

This design system rejects the cluttered, "dashboard-heavy" tropes of legacy healthcare software. Instead, it adopts the persona of a Clinical Curator: a system that synthesizes vast amounts of data into a serene, editorial experience. It is inspired by the precision of Swiss typography and the atmospheric depth of premium hardware interfaces.

We achieve a "High-End Editorial" feel by breaking the rigid, boxy grid. We use intentional asymmetry—such as oversized display type paired with condensed data points—and replace structural lines with "tonal layering." The result is a platform that feels like a high-end medical journal: authoritative, breathable, and unmistakably premium.

---

## 2. Colors: Tonal Architecture
The palette is rooted in a "Modern Medical" spectrum, replacing synthetic cyans with deep, authoritative blues and sophisticated neutrals.

*   **Primary Identity:** `primary` (#003d9b) serves as the anchor of trust, while `primary_container` (#0052cc) provides a more vibrant, digital-first blue for interactive elements.
*   **The "No-Line" Rule:** To achieve a premium aesthetic, **1px solid borders are strictly prohibited for sectioning.** Do not use lines to separate the sidebar from the main content or to box in a header. Boundaries must be defined solely through background shifts:
    *   Main Canvas: `surface` (#f7f9fb)
    *   Main Content Area: `surface_container_lowest` (#ffffff)
*   **Surface Hierarchy & Nesting:** Treat the UI as a series of stacked, physical layers. 
    *   Use `surface_container_low` (#f2f4f6) for the background of a page section.
    *   Place a `surface_container_lowest` (#ffffff) card on top to create a natural, borderless lift.
*   **The Glass & Gradient Rule:** For floating elements like "Quick Action" menus or "Patient Stats" overlays, use Glassmorphism. Apply `surface_container_lowest` at 80% opacity with a 24px backdrop blur. For primary CTAs, use a subtle linear gradient from `primary` to `primary_container` at a 135-degree angle to provide "visual soul."

---

## 3. Typography: The Editorial Scale
We utilize two typefaces to balance character with utility. **Manrope** provides a geometric, modern voice for headers, while **Inter** ensures maximum legibility for dense medical data.

*   **Display & Headlines (Manrope):** Use `display-lg` (3.5rem) for high-impact metrics (e.g., a patient’s heart rate or a primary diagnosis). Use `headline-sm` (1.5rem) for section titles. The generous scale of Manrope suggests confidence.
*   **Body & Labels (Inter):** All functional data, patient notes, and system labels use Inter. `body-md` (0.875rem) is our workhorse. 
*   **Intentional Contrast:** Pair a `display-md` value with a `label-sm` unit right next to it (e.g., **98** *bpm*). This high-contrast pairing breaks the "template" look and mimics professional data visualization.

---

## 4. Elevation & Depth: Tonal Layering
Traditional dropshadows are often "muddy." This system uses light and tone to imply three-dimensionality.

*   **The Layering Principle:** Depth is achieved by "stacking" surface tiers.
    *   *Level 0:* `surface` (The base)
    *   *Level 1:* `surface_container_low` (In-set regions)
    *   *Level 2:* `surface_container_lowest` (Cards and actionable surfaces)
*   **Ambient Shadows:** For floating modals, use a custom shadow: `0px 20px 40px rgba(25, 28, 30, 0.06)`. Note the 6% opacity; it should feel like a soft glow of light, not a dark stain.
*   **The "Ghost Border" Fallback:** If accessibility requires a stroke (e.g., in high-glare environments), use the `outline_variant` (#c3c6d6) at 20% opacity. Never use a 100% opaque border.
*   **Glassmorphism:** Use `surface_tint` (#0c56d0) at 5% opacity on top of white glass surfaces to "cool" the white, making it feel more medical and less like generic "web white."

---

## 5. Components: Refined Utility

### Buttons
*   **Primary:** A gradient of `primary` to `primary_container`. Corner radius: `md` (0.375rem).
*   **Secondary:** `surface_container_high` background with `on_surface` text. No border.
*   **Tertiary:** No background; `primary` text. Use for low-emphasis actions like "Cancel" or "View More."

### Input Fields
*   **Structure:** No 4-sided boxes. Use a `surface_container_low` background with a 2px bottom-border of `outline_variant`.
*   **State:** On focus, the bottom border transitions to `primary` and the background shifts to `surface_container_lowest`.

### Cards & Lists
*   **Forbid Dividers:** Do not use lines between list items. Use 16px or 24px of vertical white space from the Spacing Scale.
*   **Medical High-Risk Cards:** For critical alerts, use `tertiary_container` (#b90012) as a soft background with `on_tertiary_container` (#ffc5be) for text. This creates a "Red Alert" that is sophisticated, not jarring.

### Special Component: The "Vitality Badge"
*   A small, pill-shaped chip using `primary_fixed` (#dae2ff) background and `on_primary_fixed_variant` (#0040a2) text. Used for status indicators (e.g., "Stable," "In-Progress").

---

## 6. Do’s and Don’ts

### Do:
*   **Use Asymmetric Margins:** Give headers more top-margin (e.g., 64px) than bottom-margin (e.g., 16px) to create an editorial flow.
*   **Trust the White Space:** If a screen feels "busy," increase the padding rather than adding a divider line.
*   **Color as Information:** Use `tertiary` (#8c000a) only for life-critical data. If everything is red, nothing is urgent.

### Don’t:
*   **Don't use #000000:** Always use `on_background` (#191c1e) for text to maintain a soft, premium feel.
*   **Don't use Default Shadows:** Never use the standard browser or Figma "Drop Shadow" preset. Always tint the shadow with the surface color.
*   **Don't box in the data:** Avoid putting every single data point inside a card. Let some data sit "naked" on the `surface` background to create visual breathing room.