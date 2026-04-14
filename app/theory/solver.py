"""
Positional Solver.
Calculates "Minimum Movement" fingerings for progressions.
"""
import logging
from typing import List, Dict, Tuple, Any
from .engine import STRINGS, NOTES, get_note_at_fret, get_standard_voicing

logger = logging.getLogger(__name__)

def find_notes_in_window(target_notes: List[str], start_fret: int, window_size: int = 4) -> List[Dict]:
    results = []
    for string_idx, open_note in enumerate(STRINGS):
        # Always check open string
        open_string_note = get_note_at_fret(open_note, 0)
        if open_string_note in target_notes:
            results.append({"string": string_idx, "fret": 0, "note": open_string_note})

        # Check window
        for fret in range(start_fret, start_fret + window_size + 1):
            if fret == 0: continue
            current_note = get_note_at_fret(open_note, fret)
            if current_note in target_notes:
                results.append({"string": string_idx, "fret": fret, "note": current_note})
    return results

def solve_with_standard_voicing(name: str) -> Tuple[List[Dict], Dict[int, str]]:
    voicelist = get_standard_voicing(name)
    if not voicelist: return None, None
    fingering, states = [], {}
    for s_idx, fret in enumerate(voicelist):
        if fret is None: states[s_idx] = 'X'
        elif fret == 0: states[s_idx] = 'O'
        else: fingering.append({"string": s_idx, "fret": fret})
    return fingering, states

def get_best_chord_fingering(chord_name: str, chord_notes: List[str], start_fret: int) -> Tuple[List[Dict], Dict[int, str]]:
    # Prefer standard for position 1
    if start_fret == 1:
        fingering, states = solve_with_standard_voicing(chord_name)
        if fingering is not None: return fingering, states

    # Positional solver
    all_possible = find_notes_in_window(chord_notes, start_fret)
    fingering, states = [], {}
    lowest_played = -1
    for s_idx in range(6):
        options = [p for p in all_possible if p['string'] == s_idx]
        if options:
            options.sort(key=lambda x: (x['fret'] != 0, x['fret']))
            best = options[0]
            if best['fret'] == 0: states[s_idx] = 'O'
            else: fingering.append(best)
            if lowest_played == -1: lowest_played = s_idx
        else: states[s_idx] = 'X'
    return fingering, states

def solve_movable_voicing(chord_name: str, target_fret: int) -> Tuple[List[Dict], Dict[int, str], int]:
    from .engine import MOVABLE_VOICINGS, NOTES, STRINGS, normalize_note
    
    # Extract root and type
    root = chord_name[:2] if len(chord_name) > 1 and chord_name[1] in ['#', 'b'] else chord_name[0]
    chord_type = chord_name[len(root):].lower()
    if not chord_type: chord_type = 'major'
    if chord_type == 'm': chord_type = 'minor'
    
    # Find matching templates
    templates = MOVABLE_VOICINGS.get(chord_type, MOVABLE_VOICINGS['major'])
    best_option = None
    min_dist = 99
    
    root_norm = normalize_note(root)
    
    for tmpl in templates:
        # Find where this shape's root would be on the root_string
        open_note = STRINGS[tmpl['root_string']]
        # Dist from open note to target root
        root_fret = (NOTES.index(root_norm) - NOTES.index(open_note)) % 12
        
        # We can play this root_fret at 0-12, 12-24, etc. 
        # Find the one closest to our target_fret
        possible_frets = [root_fret, root_fret + 12]
        for rf in possible_frets:
            dist = abs(rf - target_fret)
            if dist < min_dist:
                # Check if this shape fits on the neck at this rf
                # The template's frets are relative to its own root (which might be fret 0 or something else)
                # But our MOVABLE_VOICINGS are defined as "standard shapes"
                # E-shape has root at fret 0. A-shape has root at fret 0.
                # So rf IS the start fret for the shape.
                fingering, states = [], {}
                valid = True
                for s_idx, f_offset in enumerate(tmpl['frets']):
                    if f_offset is None: states[s_idx] = 'X'
                    else:
                        actual_fret = rf + f_offset
                        if actual_fret < 0 or actual_fret > 20: 
                            valid = False
                            break
                        if actual_fret == 0: states[s_idx] = 'O'
                        else: fingering.append({"string": s_idx, "fret": actual_fret})
                
                if valid:
                    min_dist = dist
                    start_fret = rf
                    best_option = (fingering, states, start_fret, tmpl['name'])
                    
    return best_option

def get_alternative_fingerings(chord_name: str, chord_notes: List[str], start_fret: int) -> List[Dict[str, Any]]:
    """Returns a list of different playable versions of a chord."""
    options = []
    seen_fingerings = set()

    def add_option(style: str, f, s, fr):
        # Create a unique key for the fingering to avoid duplicates
        key = tuple(sorted([(n['string'], n['fret']) for n in f]))
        if key not in seen_fingerings:
            options.append({"style": style, "fingering": f, "states": s, "fret": fr})
            seen_fingerings.add(key)

    # 1. Standard (Open/Traditional)
    std_f, std_s = solve_with_standard_voicing(chord_name)
    if std_f is not None:
        add_option("Open / Standard", std_f, std_s, 1)

    # 2. Movable Shapes at specific locations (1, 3, 5, 7, 9, 12)
    check_positions = sorted(list(set([1, 3, 5, 7, 9, 12, start_fret])))
    for pos in check_positions:
        mov_res = solve_movable_voicing(chord_name, pos)
        if mov_res:
            f, s, actual_fr, name = mov_res
            # Only add if it's reasonably close to the position we asked for
            if abs(actual_fr - pos) <= 2:
                add_option(f"{name} (fr {actual_fr})", f, s, actual_fr if actual_fr > 0 else 1)

    # 3. Fallback: Positional Solver (The "Greedy" one) - Label it clearly
    pos_f, pos_s = get_best_chord_fingering(chord_name, chord_notes, start_fret)
    if pos_f:
        add_option(f"Positional Solver (fr {start_fret})", pos_f, pos_s, start_fret)

    return options
