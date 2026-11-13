# hollin water

An orchard by a lake, drawn in pencil on white paper. Wherever you walk, the colour comes in.

**Click the scene, then:** WASD to move, mouse to look, Shift to run, Space to jump, wheel to zoom, Esc to let go of the mouse. Walk out to the end of the jetty and watch what happens to the lake and the sky. Keep walking for a couple of minutes and the last wash goes over everything.

## what you're looking at

Nothing here was drawn by hand or downloaded. The place is ordinary flat-coloured 3D, lit as usual, and each surface's shader repaints itself as either pencil or watercolour.

- **A map of where the paint has been.** A small float texture lies over the ground like a map seen from above. Each cell remembers how covered it is and the moment colour first got there. As you walk, the cells around you get stamped with "now, plus a little for every metre away", so the wash runs outward from your feet instead of appearing all at once.
- **Every thing knows where its colour comes from.** Each vertex carries a root: the ground below it, the foot of its tree, the nearest walkable field, or for the far hills and open water, the end of the jetty. The shader looks the root up in the map, subtracts a little for height so colour climbs walls and crowns a moment later, and subtracts noise so the edge comes in ragged.
- **Two drawings in one shader.** Before the paint arrives it is graphite: hatching that lives on the surfaces (level lines of a fixed world direction, kept a few pixels apart at any distance), short strokes in the grass, ripple lines on the lake. After, it is watercolour: paper nearly bare in the light under a warm glaze, pigment pooling in soft blooms, a dark wet rim at the edge that dries, a cool violet glaze in shade, a faint tide line where a wash stopped, haze far away.
- **The paper.** One last pass adds graphite outlines, grain, the sky (bare until you earn it) and a soft white watery margin.

## things worth stealing from the prompt

- **Store time, not colour.** "Stamp the time colour arrived into a map, and compute age in the shader" gives you spreading edges, wet rims that dry, climbing and a finale from one number per cell.
- **Give everything a root.** Deciding per vertex where its colour comes from is what lets a wash climb a tree, jump to a far hill, or cross a lake from the end of a jetty.
- **Make the unpainted world worth looking at.** The pencil state is half the piece; ask for it as carefully as the paint.
- **Name the wet edge.** "A darker rim at the advancing edge that dries" is the one line that makes it read as watercolour rather than a colour fade.

## limits

- Desktop first. On a phone you can watch the drift and drag to look, but not walk.
- The paint only remembers the near land (128 metres square); everything beyond gets its colour from the nearest edge of it or from the jetty.
- You can't swim, go inside the cottage, or take the boat out.

## credit

The wash technique (a time-of-arrival map over the ground, roots that colour climbs from, ragged noise edges, the watercolour paint and sky functions, grass strokes and the final wash) is adapted from [watercolour](https://patch.gg/blendi/watercolour) by @blendi, MIT / CC0. The surface pencil strokes come from 007 pencil town, itself after blendi's coloured pencil. The lake, the orchard and the painter are new.
