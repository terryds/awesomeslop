Make a single self-contained HTML file: a small third-person 3D game scene called "washing day", drawn as if in coloured pencil on paper. Use three.js 0.170 from a CDN through an import map. No other libraries, no downloaded models, textures, fonts or sounds: everything is made in code.

THE PLACE
Monteviola, an invented hill village in the south, on a bright afternoon. A paved square about 50 metres across, ringed by narrow pastel houses two and three storeys high: rose, mint, butter, lavender, peach, sky blue. Every house has white-framed windows with painted shutters, some open, some shut, window boxes of flowers, a door, a few little balconies with iron railings and a striped shop awning or two. Gable roofs in faded terracotta, some facing the square, some side-on, with chimneys.

In the middle of the square, an octagonal stone fountain with a small jet. On the north side a stone retaining wall and a wide flight of ten steps up to an upper walk, where a small cream chapel with a rose window and a bell tower stands under a big tree. Two lanes go off the sides between the houses. On the south side a low wall looks out over a valley of patchwork fields, cypress lines and olive trees, to far blue hills with another village on them. Behind the chapel the hill rises in rows of vines.

It is washing day: lines strung across the top of the steps, across both lanes and from a house to a pole, hung with sheets, shirts and towels in soft colours that sway in the wind. A cart of lemons, benches, lamp posts, potted geraniums, pigeons that scatter when you run at them, a ginger cat on the wall.

THE LOOK
This is the heart of the piece; if something has to give, keep this. Render the scene into targets first (the lit scene with shadows and its depth; then world normals plus the brightness of each surface's flat colour), then draw the whole frame in one post-processing shader:
- Colour stays, but pastel and a little under-filled: laid down as dense pencil strokes over paper, with the paper showing between them.
- Light becomes hatching. Lit faces get only a few loose strokes. Shadow gets a layer of strokes, then a crossing layer, then a third, darker one in the deepest shade, each thicker and denser as it darkens. Hatch colour is a deeper, cooler version of the surface colour.
- Stroke direction changes per surface, chosen from which way it faces. Strokes are short, tapered, a little uneven in pressure.
- The lines boil: four times a second the hand redraws, so strokes and outlines shift slightly.
- Soft, wobbly outlines from depth and normal breaks and from changes of flat colour, fading with distance.
- Paper grain everywhere. Far things fade into pale blue-grey. The sky is loose horizontal strokes of blue with paper-white clouds and lavender undersides.
- A torn white paper border around the whole frame, and a small handwritten caption in a corner naming where you are ("monteviola, the long steps"), changing as you walk.

THE WALKER
A small character built from primitives: a baker's lad in a straw hat with a red band, white shirt, blue neckerchief, mustard trousers, a bread basket on his back. Arms and legs swing as he walks, faster when he runs; he tucks his legs when he jumps. He turns to face the way he moves.

Before the first click, a slow camera drift across the square and a "click to walk" hint. On click: third-person camera behind him, mouse to look (pointer lock, drag as a fallback), WASD to move relative to the camera, Shift to run, Space to jump, mouse wheel to zoom. He collides with houses, walls, the fountain, trees and benches, walks up and down the steps, and can jump onto benches and the fountain rim. The camera pulls in when a wall gets between it and him. Hide the hint when the page is loaded with ?thumb=1.

Keep it smooth on a laptop: merge the static town into one mesh, cap the pixel ratio and lower it if frames get slow. Handle window resize.
