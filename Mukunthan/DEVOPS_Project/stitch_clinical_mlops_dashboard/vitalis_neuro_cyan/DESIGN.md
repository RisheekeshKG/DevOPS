# Design System Strategy: Clinical MLOps & Patient Risk

## 1. Overview & Creative North Star: "The Sentinel Lens"
The North Star for this design system is **The Sentinel Lens**. In a high-stakes MLOps clinical environment, the UI must transition from a passive dashboard to an active diagnostic partner. We avoid the "generic SaaS" look by rejecting flat, boxy layouts in favor of an **Architectural Deep-Space** aesthetic.

This system prioritizes "Luminous Precision." By utilizing a deep charcoal foundation and neon-cyan accents, we create a high-contrast environment where critical data "glows" with importance. We break the standard grid through intentional asymmetry—using large, editorial typographic anchors (Manrope) against dense, microscopic data visualizations (Inter). The result is a futuristic, medical-grade interface that feels like a mission-critical heads-up display (HUD) rather than a spreadsheet.

---

## 2. Colors & Surface Philosophy
The palette is engineered for prolonged cognitive focus in low-light clinical environments.

### The Palette
*   **Background (`#0d1321`):** The "Infinite Void." This is the base layer for all views.
*   **Primary Action / Neon Cyan (`#00f2ff`):** Used for "Living Data" and primary interactions.
*   **Vivid Amber (`#fdaf00`):** Reserved strictly for "Warning/Moderate Risk."
*   **Red / Error (`#ffb4ab` / `#93000a`):** Reserved for "Immediate Intervention/High Risk."

### The "No-Line" Rule
To achieve a premium, medical-grade feel, **1px solid borders are prohibited for sectioning.** We do not "box" data. Instead:
*   **Tonal Transitions:** Use the `surface-container` tokens to define areas. A `surface-container-low` card sitting on a `surface` background creates a sophisticated boundary without visual noise.
*   **Negative Space:** Use the spacing scale to let sections "breathe" into existence.

### Surface Hierarchy & Nesting
Treat the UI as a series of nested, translucent layers:
1.  **Level 0 (Base):** `surface` (`#0d1321`) - The canvas.
2.  **Level 1 (Sub-section):** `surface-container-low` (`#151b29`) - Subtle grouping.
3.  **Level 2 (Active Element):** `surface-container-high` (`#242a39`) - Focused content.
4.  **Level 3 (Overlay):** `surface-container-highest` (`#2f3544`) - Modals and popovers.

### The Glass & Gradient Rule
To add "soul," use **Glassmorphism** for floating elements (e.g., patient detail sidebars). Use a backdrop-blur of `12px` combined with a 10% opacity `surface-tint`. Apply a subtle linear gradient to Primary CTAs: from `primary_container` (`#00f2ff`) to `primary_fixed_dim` (`#00dbe7`) at a 135° angle.

---

## 3. Typography: Editorial Authority
We use a dual-typeface system to balance human readability with machine-precision data.

*   **Display & Headlines (Manrope):** Chosen for its geometric, modern personality. Use `display-lg` and `headline-md` to create editorial "anchors" on the page (e.g., a patient’s name or a high-level risk score). This breaks the monotony of data-dense screens.
*   **Body & Labels (Inter):** The workhorse. Inter’s high x-height ensures that microscopic clinical notes and MLOps logs remain legible at `body-sm` (`0.75rem`).
*   **Intentional Scale:** Use `label-sm` (`0.6875rem`) in all-caps with `0.05em` letter spacing for metadata to create a "technical" HUD feel.

---

## 4. Elevation & Depth: Tonal Layering
Traditional drop shadows feel "dirty" in a medical dark mode. We use light, not shadow, to convey depth.

*   **The Layering Principle:** Stack `surface-container-lowest` on top of `surface` to create a "recessed" look for data tables. Stack `surface-container-highest` on top of `surface` to create "elevated" priority alerts.
*   **Ambient Shadows:** If a floating element (like a Tooltip) requires a shadow, use a large `40px` blur at `4%` opacity, tinted with the `primary` color (`#e1fdff`). It should look like a soft blue glow, not a grey smudge.
*   **The Ghost Border:** If a boundary is required for accessibility, use `outline-variant` at `15%` opacity. It should be felt, not seen.

---

## 5. Components

### Buttons
*   **Primary:** Gradient fill (`primary_container` to `primary_fixed_dim`), `on_primary` text, `md` (`0.375rem`) corner radius. No border.
*   **Tertiary (Ghost):** No background. `primary` text. On hover, a `surface-variant` background at 20% opacity.

### Medical Risk Chips
*   **High Risk:** `error_container` background with `on_error_container` text.
*   **Active Monitoring:** `secondary_container` (Amber) with `on_secondary_container` text.
*   **Structure:** Minimalist pill shape (`full` roundedness), no border, `label-md` typography.

### Data Tables & Lists
*   **No Dividers:** Prohibit horizontal lines. Use `surface-container-low` for alternating row backgrounds (zebra striping) or simply 12px of vertical padding to separate entries.
*   **Interactive Rows:** On hover, shift the background to `surface-bright`.

### Vital Sign Inputs
*   **Input Fields:** Use `surface-container-highest` with a bottom-only `ghost border` (2px). When focused, the border transforms into a 2px `primary` neon glow.

### Specialized MLOps Components
*   **Model Confidence Gauge:** A semi-circular SVG stroke using `primary`. Use `surface-variant` for the "empty" track.
*   **Risk Trend Sparklines:** Ultra-thin (1.5px) neon cyan lines with a subtle outer glow filter to simulate a CRT medical monitor.

---

## 6. Do’s and Don’ts

### Do
*   **Do** use `surface-container` shifts to group patient data.
*   **Do** use `display-sm` for hero numbers (e.g., "88% Risk Score").
*   **Do** allow 24px–32px of "breathing room" between major data widgets.
*   **Do** use `backdrop-blur` on navigation rails to show hints of the data scrolling behind them.

### Don’t
*   **Don't** use pure white (`#FFFFFF`) for text. Use `on_surface` (`#dde2f6`) to reduce eye fatigue.
*   **Don't** use 1px solid borders to separate sidebar from main content. Use a background color shift.
*   **Don't** use standard "Material Design" shadows. They are too heavy for this medical aesthetic.
*   **Don't** clutter the UI with icons. Use typography and color first; icons should only be used as "wayfinders" for primary navigation.