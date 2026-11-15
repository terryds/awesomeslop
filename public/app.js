// Copy buttons: <button data-copy="#selector" data-copied="label after copying">
async function copyText(text) {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch {
    const ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    const ok = document.execCommand('copy');
    ta.remove();
    return ok;
  }
}

document.addEventListener('click', async (event) => {
  const button = event.target.closest('[data-copy]');
  if (!button) return;
  const source = document.querySelector(button.dataset.copy);
  if (!source) return;
  const ok = await copyText(source.textContent.trim());
  const original = button.dataset.label ?? (button.dataset.label = button.textContent);
  button.textContent = ok ? button.dataset.copied || 'copied' : 'copy failed, select the text instead';
  button.classList.toggle('is-copied', ok);
  clearTimeout(button._t);
  button._t = setTimeout(() => {
    button.textContent = original;
    button.classList.remove('is-copied');
  }, 2000);
});

// "/" jumps to the gallery search, like a terminal pager.
document.addEventListener('keydown', (event) => {
  const search = document.querySelector('.search input');
  if (event.key !== '/' || !search || /^(INPUT|TEXTAREA)$/.test(document.activeElement.tagName)) return;
  event.preventDefault();
  search.focus();
});

// Play buttons: <a href="piece" data-play="#stage"> fullscreens the stage in place, so the running piece
// keeps its state and a game can grab the pointer. Without the Fullscreen API (iPhone) the link just opens the piece.
document.addEventListener('click', async (event) => {
  const link = event.target.closest('[data-play]');
  const stage = link && document.querySelector(link.dataset.play);
  if (!stage || !stage.requestFullscreen) return;
  event.preventDefault();
  try {
    await stage.requestFullscreen({ navigationUI: 'hide' });
    stage.querySelector('iframe')?.focus(); // keys go straight to the piece
  } catch {
    window.open(link.href, '_blank', 'noopener');
  }
});

// Gallery cards show a still cover. On a device with a mouse, resting the pointer on a card runs the real piece
// inside its frame (<div class="frame" data-live="piece url">) and leaving the card puts the cover back.
// Only one piece runs at a time. Touch screens keep the cover: a tap opens the piece's page.
if (matchMedia('(hover: hover)').matches) {
  let timer;
  const stop = (frame) => frame.querySelector('iframe')?.remove();
  document.querySelectorAll('.card').forEach((card) => {
    const frame = card.querySelector('[data-live]');
    if (!frame) return;
    card.addEventListener('pointerenter', () => {
      clearTimeout(timer);
      // A short wait, so sweeping the pointer across the grid does not start every piece it passes.
      timer = setTimeout(() => {
        document.querySelectorAll('[data-live] iframe').forEach((f) => f.remove());
        const piece = document.createElement('iframe');
        piece.src = frame.dataset.live;
        piece.title = frame.querySelector('img')?.alt ?? '';
        piece.setAttribute('sandbox', 'allow-scripts'); // same as before: no access to this site's cookies or DOM
        piece.tabIndex = -1;
        frame.append(piece);
      }, 200);
    });
    card.addEventListener('pointerleave', () => {
      clearTimeout(timer);
      stop(frame);
    });
  });
}
