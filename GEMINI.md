# Fretboard Compass Project Specifications

## Overview
Fretboard Compass is a high-performance Music Theory Suite for guitarists. It transforms complex theory into printable, "Binder-Ready" practice sheets. It features a mathematical theory engine that calculates diatonic chords across exotic scales and maps them to the fretboard using the CAGED system.

## Core Features
- **Pro Theory Engine:** Dynamically calculates triads and Roman Numerals for 20+ scales, including exotic moods like Byzantine and Spanish Gypsy.
- **Visual Mastery:**
    - **Vertical Chords:** Symmetrical 5-column grid optimized for 8.5x11 Portrait printing.
    - **Horizontal Scales:** 12-fret neck maps with "Diamond Root" markers and "Positional Zoning" (Color-coded zones for Frets 1-4, 5-8, and 9-12).
- **Interactive Library:**
    - **Proven Winners:** A dashboard of 20 timeless chord/scale combinations with play-style tips and sample songs.
    - **Pattern Presets:** 22 standard and advanced progressions synced with professional theory benchmarks.
- **Student Ready:** Built-in "One Neighborhood" practice guide and printable drill sheets.

## Technical Stack
- **Backend:** Flask (Python 3.12+)
- **Frontend:** HTMX (AJAX without JS), Tailwind CSS (Modern Styling)
- **Graphics:** `svgwrite` (Dynamic vector generation)
- **Infrastructure:** Local development ready; Cloudflare Workers (Edge) roadmap.

## Project Architecture
- `app/theory/engine.py`: The "Brain". Mathematical interval and triad calculation.
- `app/theory/solver.py`: The "Navigator". Finds optimal fingerings and movable CAGED shapes.
- `app/graphics/svg_builder.py`: The "Artist". Handles all vector rendering and positional color zoning.
- `app/templates/`: Pure HTML/HTMX partials for ultra-fast UI swaps.

## Strategic Roadmap
- [x] **Phase 1:** Refactor to robust `TheoryEngine` with analytical triad building.
- [x] **Phase 2:** Implement HTMX-powered "Proven Winners" and "Practice Guide".
- [ ] **Phase 3:** Port Python logic to TypeScript for Cloudflare Workers deployment.
- [ ] **Phase 4:** Integrate Stripe/Newsletter gatekeeping for commercial launch.
