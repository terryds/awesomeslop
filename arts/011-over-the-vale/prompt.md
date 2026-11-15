Make a single self-contained HTML file: a free-roam flying scene called "over the vale", where you ride a dragon over a river valley. There is no goal, no score and nothing to collect: the place is the point. Use three.js 0.170 from a CDN through an import map. No other libraries, no downloaded models, textures, fonts or sounds: everything is made in code.

THE LOOK
A bright, clean, stylised game world in high detail, like a hand-painted animated film turned into a game: saturated greens, a deep blue sky with soft white cumulus, turquoise water, lilac-grey stone. Smooth shading, soft shadows from one sun, filmic tone mapping, light haze in the distance, a faint vignette. No post-processing filter over the picture. Get the detail from the surfaces themselves:
- Keep three.js's own lit materials (so lights, shadows and fog all work) and add to their shaders: colour computed per pixel from world position, and vertices moved in the vertex shader.
- Land: a smooth height field. Per pixel: three greens mottled by noise at several scales, scattered yellow and pink flower dots that fade with distance, sand along the water going dark and wet at the edge, banded lilac rock on steep slopes, pale stone on the heights.
- Grass: 150,000 blades in one square patch that follows the camera and wraps, so the meadow never ends. Each blade reads the land's height from a texture, bends in the wind, is dark at the root and light at the tip, and is lit like the ground under it. Some carry a flower. None on sand, rock or steep ground.
- Trees: three kinds, instanced, about 560: round oaks built from seventeen lumpy balls of leaf with a trunk and two branches, tall narrow poplars, and tiered pines on the high ground. Shade each crown as one soft mass (blend each ball's normals toward the crown's centre), darker underneath, with leaf clumps and leaves drawn by noise, swaying a little. Mostly greens, some in pink blossom, a few gold.
- Water: draw the whole world a second time each frame from a camera mirrored in the water's surface, and show that upside-down picture in the river and sea, bent by ripples. Turquoise in the shallows and deep blue further out (use the land's height for the depth), white foam along the shore, a glittering path under the sun.
- Sky: a gradient with a sun and thin drifting cloud, lit on the side facing the sun, plus big solid cumulus you can fly through.

THE WORLD
One green island about 1.4 km across in an open sea, with a river winding across the middle and mountains to the north. Grey boulders along the river and on the slopes.
A great stone aqueduct crosses the river valley: 330 m long, 62 m high, nine round arches wide enough to fly through. Draw the stonework in its shader: courses of blocks in several greys and the odd sandstone one, dark mortar, moss creeping down from the top, damp near the water. Ivy hangs down both faces and scrub grows along the top.
Eight islands float in the sky at different heights: grass on top, rock tapering below, vines hanging, trees on top (many in blossom), bobbing slowly. Three have a thread of water falling off the edge all the way down.
Two flocks of birds circle. Small pale specks drift in the air: petals by day, gold like fireflies at dusk.
A day lasts 120 seconds: blue midday, the sun sliding down to an orange, pink and violet dusk, and back. T jumps to the other half.

THE DRAGON AND THE RIDER
A crimson dragon about 17 m long. The body is one smooth skin rebuilt round a spine every frame, so it bends: dark banded back, scales drawn in the shader, a gold plated belly, bone-coloured spines all the way down, a small fin at the tail. A slow wave runs down the spine; the neck leads into a turn and the tail trails it; the whole animal banks. A head with a long snout, an open jaw with teeth, nostrils, brows, six horns, cheek frills and yellow eyes with slit pupils. Four legs tucked up, with claws. Two wide bat wings with dark bones and orange membrane between scalloped fingers; they fold at the wrist as they beat, harder when climbing and nearly still in a dive.
On a saddle at its shoulders sits a small rider: white tunic, belt, dark hair, goggles, a red scarf with a loose end, boots, and a blue cape streaming out behind.

FLYING
Before the first click the dragon flies itself in a wide loop round the island while the camera drifts round it, with a "click to fly" hint. On click the visitor takes over, with the controls of a third-person game:
- The mouse is the camera (pointer lock, with drag as a fallback). It orbits the dragon: left and right to turn, up and down to raise or lower the view.
- W A S D and the arrows move the dragon relative to where the camera looks: W flies the way you are looking, including up or down; S comes back toward the camera; A and D go sideways. Space or E goes straight up, C or Q straight down. Shift is faster.
- With no key held, the dragon slows, stops and hovers in place, beating its wings hard and bobbing. It never moves by itself.
- The dragon turns to face the way it is travelling, noses up or down with its climb, and banks into turns.
It cannot go through the ground, is stopped by the aqueduct's stone but passes through its arches, and is pushed off the floating islands.

Hide all text when the page is loaded with ?thumb=1, and when the window is very small. Keep it smooth on a laptop: draw the mirrored world at half size, leave the grass out of it, cap the pixel ratio and lower it if frames get slow. Handle window resize.
