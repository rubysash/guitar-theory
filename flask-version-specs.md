# Flask Version Specification: Music Theory Suite

## Overview
This specification defines the professional local version of the Fretboard Compass Music Theory Suite. It is optimized for high-speed local use, printer-friendly output, and "Binder-Ready" practice materials.

## 1. Functional Requirements

### **Theory Solving**
- **Dynamic Triads:** Build Major, Minor, Diminished, Augmented, and Suspended chords mathematically from any 7-note scale.
- **Harmonic Borrowing:** Force specific chord qualities for presets (e.g., Major V in Flamenco) to ensure musicality over strict diatonicism.
- **CAGED Integration:** Automatically find movable fingerings across the entire neck (12+ frets).

### **Visual Generation**
- **Chord Cards:** Fixed 150px cards, symmetrical 5-column grid for 8.5x11 Portrait printing.
- **Scale Maps:** Full-width 12-fret diagrams with:
    - **Diamond Roots:** Solid (Fretted) and Hollow (Open) geometric identifiers.
    - **Color Zoning:** Zone 1 (Black: 1-4), Zone 2 (Blue: 5-8), Zone 3 (Purple: 9-12).

### **User Experience (HTMX)**
- **Proven Winners:** Interactive 20-card dashboard for instant loading of classic "Vibe" combinations.
- **Practice Guide:** Built-in "One Neighborhood" printable manual.
- **Nashville Numbering:** Dynamic Roman Numeral calculation with support for accidentals (bII, #IV) and casing (I vs i).

## 2. Technical Implementation

### **Data Flow**
1. User selects Key/Scale/Pattern in `index.html`.
2. HTMX triggers `/get_preset_chords` to update the progression text box (300ms debounce).
3. HTMX `POST` to `/generate` sends theory parameters to `WorkbookService`.
4. `TheoryEngine` calculates notes; `Solver` finds fingerings; `SVGBuilder` generates vector markup.
5. HTMX swaps results into `#workbook-results` with zero page refresh.

### **Printer Optimization (@media print)**
- Hide non-essential UI elements (Discovery Panel, Buttons).
- Force background colors and high-contrast borders.
- Centered grid alignment for aesthetic symmetry.

## 3. Core Components
- **`app/routes.py`:** Flask endpoints for partial delivery.
- **`app/theory/engine.py`:** The interval and Nashville logic.
- **`app/graphics/svg_builder.py`:** Geometry and color-zoning logic.
- **`app/templates/partials/`:** winners.html, instructions.html, workbook.html.
