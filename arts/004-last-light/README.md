# last light

An island at dusk, and nothing to do there but walk.

**Click the scene, then:** WASD to move, mouse to look, Shift to run, **T** for night, M for sound, Esc to let go of the mouse. Walk up to the lighthouse, down to the cabin, out to the end of the pier.

## what you're looking at

Nothing here was drawn or downloaded. The island is a formula: a height for every point, made from layered noise, pushed up into a headland on one side and down into the sea at the edges. The same formula decides where trees may stand, where grass grows, where foam appears and where your feet are.

- **The meadow** is 90,000 separate blades, but only one 64-metre patch of them exists. It wraps around you as you move, so you never reach its edge.
- **The sea** is a single flat square. The waves are a trick of light: the shader tilts the surface a little at every pixel and reflects the sky in it.
- **The beam** is two things at once. The cones you see in the air are just transparent shapes; the light that crosses the grass and water is computed separately, so both can be tuned to look right.
- **The sound** is noise through two filters. No audio files.

## things worth stealing from the prompt

- **Say what the heart of the piece is.** "This sweep is the heart of the piece; if something has to give, keep this." A scene has a hundred details, and the agent needs to know which one is not negotiable.
- **Describe the trick, not just the result.** "Only draw one patch around the viewer and wrap it" and "no geometry waves, fake them in the shader" are what make it run on a laptop.
- **Match the haze to the horizon.** One sentence, and the sea stops having an edge.
- **A place plus a look.** The first section says what is there. The second says how it is painted. Mixing the two gets you a generic scene.

## limits

- Desktop first. On a phone you can watch the tour and drag to look, but not walk.
- One island, two hours of the day. You can't go inside anything.
- No shadows.
