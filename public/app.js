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
