# over the vale

Ride a dragon over a river valley: under a stone aqueduct, round floating islands, out over the sea, from midday into dusk.

**Click the scene, then:** steer with the mouse, or W A S D and the arrows. Shift or Space to go faster. T jumps between day and dusk. Esc lets go of the mouse.

There are eight stone gates in a loop round the island. Fly through one and it lights gold. The river is the best place to fly low: the arches of the aqueduct are wide enough to go through.

## what you're looking at

Nothing here is a model or a texture file. The detail is in the surfaces.

- **Stock materials, extra shader.** Everything is lit by three.js's own materials, so sun, shadows and haze behave. Each one has a few lines added: the land works out its colour per pixel (greens, flowers, sand, wet sand, banded rock), the aqueduct draws its own stone blocks, mortar and moss, the trees draw their leaves, the dragon draws its scales.
- **Grass that follows you.** 150,000 blades live in one square patch that moves with the camera and wraps round, so the meadow never runs out. Each blade looks up the height of the land in a texture.
- **Water that mirrors the world.** Every frame the scene is drawn twice: once from a camera turned upside down under the water, then normally, with that first picture laid on the river and bent by ripples. That is why the aqueduct stands in the water.
- **Crowns, not balls.** A tree is a pile of lumpy balls, but each ball is lit as part of the whole crown, so it reads as one soft mass.
- **A dragon with a spine.** Its body is a skin rebuilt round sixteen points every frame. A wave runs down it, the neck leads a turn, the tail follows late, and the wings fold at the wrist.

## things worth stealing from the prompt

- **Add to the engine's materials instead of replacing them.** You keep lighting, shadows and fog for free and only write the part that is yours.
- **Put the detail in the pixel, not the mesh.** Stone courses, scales and flowers cost a few lines each.
- **One patch of grass, wrapped.** The oldest trick for an endless meadow.
- **Mirror the camera for water.** Ask for it by name ("draw the world a second time from a camera mirrored in the surface") or you get a blue plane.
- **Say how big things are.** "Nine arches wide enough to fly through" decided the whole layout.

## limits

- Desktop first. On a phone you can watch, and drag to steer after a tap.
- The mirrored world leaves out the grass and the drifting specks.
- You bump off stone and islands, but there is no landing, and no sound.

## credit

The look this aims for, a lush hand-painted valley with an aqueduct over a river, comes from ["a painted 3D world"](https://x.com/LexnLin/status/2121634005745635683) by Leon Lin. No code or assets were used from it. The island, the gates, the dragon and rider and all the shaders here are new.
