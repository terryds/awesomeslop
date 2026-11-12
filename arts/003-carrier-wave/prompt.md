Make a single self-contained HTML file: a full-window canvas artwork called "carrier wave". No libraries, no controls.

The whole window is a grid of monospace characters on black, about 110 columns' worth of cells across the longer side. Nothing is drawn except characters.

Three invisible points wander slowly around the grid on looping paths. Each one sends out circular ripples, like a stone dropped in water: a sine wave of the distance from the point, moving outward over time. At every cell, add the three ripples together.

Turn that sum into a character using this brightness ramp, from empty to dense:  .:-=+*#%@  (the first character is a space). Low values are blank, high values are heavy glyphs. Brighter cells are also more opaque white.

Where the three waves pile up and the value is in the top 14%, draw the character in hot pink (#ff4fd8) instead of white. These pink crests are the focus of the piece: thin arcs that appear, slide and vanish where ripples cross.

Monospace characters are taller than they are wide. Correct for that so the ripples are round, not oval.

Handle window resize and high-density screens.
