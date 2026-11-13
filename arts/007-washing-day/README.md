# washing day

A hill village on laundry day, drawn in coloured pencil while you walk through it.

**Click the scene, then:** WASD to move, mouse to look, Shift to run, Space to jump, wheel to zoom, Esc to let go of the mouse. Climb the steps to the chapel, walk under the sheets in the lanes, look out over the valley from the low wall. Run at the pigeons.

## what you're looking at

Nothing here was drawn by hand or downloaded. The town is ordinary flat-coloured 3D, and one shader redraws every frame as a pencil drawing.

- **Two quick renders, one drawing.** The scene is drawn twice off-screen: once lit, with shadows, and once as raw facts (which way every surface faces, and how bright its flat colour is). Dividing one by the other tells the shader how much light each pixel got, separately from what colour it is.
- **The strokes live on the surfaces.** The shader works out where each pixel sits in the world and draws the level lines of a height measured along one fixed direction. So strokes stick to walls and roofs as you walk, run long and parallel, and keep the same spacing on screen near and far.
- **Pencil over white paper.** Colour is taken away from the paper's white in layers: a faint warm wash where the sun falls, the thing's own colour laid lightly, strokes of it pressed harder into the shade, and a cool violet shadow pencil crossing them where the light doesn't reach. The paper's tooth breaks every layer up.
- **Outlines** come from where depth bends, where faces turn and where the flat colour changes, wobbled by noise and faded with distance.
- **The paper** is noise: grain under everything, a torn white edge, a little smudge just inside it.

## things worth stealing from the prompt

- **Ask for the passes.** "Render the lit scene and its depth, then normals and flat colour, then draw it in one shader" is what turns a style wish into a technique. Without it you get a filter over a finished image, and shadows that can't become hatching.
- **Say what light becomes.** "Shadow is a layer of strokes, then a crossing layer, then a darker third" is a rule the shader can follow. "Make it look hand-drawn" is not.
- **Name the small imperfections.** Under-filled colour, paper tooth, wobbly lines, a torn border. Each is one line in the prompt and each is half the effect.
- **A place plus a look.** The town section says what is there. The look section says how it is drawn. The walker section says how it plays.

## limits

- Desktop first. On a phone you can watch the drift and drag to look, but not walk.
- You can't go inside anything, and the lanes end in walls.

## credit

The surface stroke technique (level lines in world space, octave-blended spacing, layered pencil over white) is adapted from [coloured pencil](https://patch.gg/blendi/coloured-pencil) by @blendi, MIT / CC0.
