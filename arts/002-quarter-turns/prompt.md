Make a single self-contained HTML file: a full-window canvas artwork called "quarter turns". No libraries, no text on screen, no controls.

Fill the window with a grid of square tiles, about 14 tiles along the longer side, centered so the grid bleeds off every edge. Black background.

Every tile carries the same drawing: two thick white quarter-circle arcs, each connecting the midpoints of two neighbouring sides. Give each tile a random starting rotation of 0, 90, 180 or 270 degrees. Because every arc ends at the middle of a side, the tiles join into long wandering loops and blobs with no loose ends.

About ten times a second, pick one random tile and rotate it a quarter turn, taking 0.7 seconds with an ease-in-out. While a tile is turning, draw its arcs in orange (#ff5a1f); when it lands, it goes back to white. The paths should visibly break apart and reconnect as tiles turn.

The stroke should be heavy, about 12% of the tile size, with flat ends so arcs meet cleanly at tile borders.

Handle window resize and high-density screens.
