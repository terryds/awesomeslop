# lantern cove

A seaside fishing village as a pop-up paper diorama, at golden hour. The camera pans from the jetty past the lighthouse and the huts to a kid in a yellow raincoat, and everything folds up off the page as the camera reaches it. Fourteen seconds, looping.

**Click to pause**, space too, ← → to skip 5 seconds. The scene itself runs live at [scene/](/a/019-lantern-cove/scene/): walk the kid with WASD or the arrow keys, or open [scene/?pan](/a/019-lantern-cove/scene/?pan) for the fold-up pan. It prints around 800 paper cards when it loads, so give it a few seconds.

## how it was made

- **The papercraft skill.** [xikhar/papercraft](https://github.com/xikhar/papercraft) is an agent skill for a handcrafted pop-up paper look: matte card with thin cut edges, prints layered like paper collage, soft shadows tinted by the world, a tilt-shift macro lens, and pieces that rise on springy hinges. Its kit and harness are in [scene/papercraft/](/a/019-lantern-cove/scene/papercraft/) and [scene/harness.js](/a/019-lantern-cove/scene/harness.js) (MIT).
- **A new world.** [scene/scene.js](/a/019-lantern-cove/scene/scene.js) is all this piece: the palette, the printed sea, sand and boardwalk, and every piece drawn as a layered cut-out (palms, the lighthouse, crabs, gulls, nets, crates, buoys, boats). The huts and the hero's construction follow the skill's worked examples, recoloured and redressed.
- **No assets.** No images, no image generation: every card is cut and printed by code when the scene builds.
- **Fold up on camera.** In `?pan` mode every hinge is held flat until its foot projects into the frame, then it is released with a small per-piece delay so neighbours stagger. The camera follows a Catmull-Rom path through five points and turns 20° on the way.
- **Rendered headless.** The skill's `capture.py` runs the page in headless Chromium on a fixed clock and saves one PNG per frame, then ffmpeg encodes them. On this small VM with software GL that was about 6 frames a minute.

## credit

The paper style, kit and harness come from the papercraft skill by [xikhar](https://github.com/xikhar/papercraft). The cove, its pieces and the fold-up pan are new.
