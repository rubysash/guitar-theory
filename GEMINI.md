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
- **Favorites System:** Save custom combinations with a Title and Description (e.g. "distortion settings", "fingerpicking style"). Persistent JSON storage for custom vibes.
- **Scale Family Selector:** Real-time theory detection suggests compatible scales (e.g. "A Harmonic Minor" for an Andalusian Cadence) without forcing chord changes.
- **Solver Sync:** Entering a manual progression automatically updates the "Note" and "Mood" dropdowns to match the detected theory.
- **Student Ready:** Built-in "One Neighborhood" practice guide and printable drill sheets.
- **Cross-Platform Support:** Official setup instructions and direct Python 3.12 download links for Windows, macOS, and Linux.

## Technical Stack
- **Backend:** Flask (Python 3.12+)
- **Frontend:** HTMX (AJAX without JS), Tailwind CSS (Modern Styling)
- **Graphics:** svgwrite (Dynamic vector generation)
- **Infrastructure:** Local development ready; Cloudflare Workers (Edge) roadmap.

## Documentation Standards
- **Emoji Usage:** NEVER use emojis in any output documentation (README.md, GEMINI.md, etc.) except for the README.md which has a sign of the horns (🤘) after the last line "...for guitarists ..."
- application code may use specific music symbols if they are standard and best practice, but not emojies for general header/comment text output, which should always appear as professional output.
- applicaiton code should prefer svg icons from free font awesome resources if needed (the star for favorites), and should avoid smart quotes, em dashes, and other use of emojies not already specified.

## Version Log
- keep updated version history in the README.md
- update the config.py with the correct version number
- Add version history notes to the workflow so it is automated

## Project Architecture
- app/theory/engine.py: The "Brain". Mathematical interval and triad calculation.
- app/theory/solver.py: The "Navigator". Finds optimal fingerings and movable CAGED shapes.
- app/graphics/svg_builder.py: The "Artist". Handles all vector rendering and positional color zoning.
- app/templates/: Pure HTML/HTMX partials for ultra-fast UI swaps.
- favorites/: Local JSON storage for user favorites.

## Theory Logic Architecture
To maintain professional accuracy, the suite uses a three-tier logic hierarchy:

### Tier 1: Fixed Knowledge (Hard-Coded)
- **Interval Maps:** 15+ scale semitone patterns and 8+ chord type patterns.
- **Fretboard Constants:** E-A-D-G-B-E tuning and 12-note chromatic scale.
- **Voicing Templates:** ~30 standard/movable chord shapes (CAGED) to ensure physical playability.

### Tier 2: Heuristic Logic (Best Guess)
- **Key Detection:** Uses weighted scoring (100% note match + 15% tonic bias + 5% common scale bonus).
- **Fingering Priority:** Prefers "Open" shapes at Fret 1, "Movable" shapes at higher frets, and "Positional Solver" (greedy algorithm) as fallback.

### Tier 3: Dynamic Logic (Mathematical)
- **Nashville Numbering:** Dynamically calculates Roman Numerals by comparing roots to major-scale benchmarks.
- **Analytical Triads:** Builds 1-3-5 chords from any 7-note scale using internal interval walking.
- **Scale Mapping:** Checks every fret on the 6 strings against calculated scale notes for vector rendering.

## Strategic Roadmap
- [x] Full CAGED movable voicing support.
- [x] Mathematical triad building for exotic scales.
- [x] "Proven Winners" interactive dashboard.
- [x] Favorites system with Titles and Descriptions.
- [ ] TypeScript port for Cloudflare Workers deployment.
- [ ] Stripe integration for "Pro" tier features.
