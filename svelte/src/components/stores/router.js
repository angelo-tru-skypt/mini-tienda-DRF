// src/stores/router.js
import { writable } from 'svelte/store';

const getPath = () => {
  const p = window.location.pathname || '/';
  return p.endsWith('/') && p !== '/' ? p.slice(0, -1) : p;
};

export const route = writable(getPath());

export function navigate(path = '/', { replace = false } = {}) {
  const target = path.startsWith('/') ? path : '/' + path;
  if (target === getPath()) return;
  if (replace) history.replaceState({}, '', target);
  else history.pushState({}, '', target);
  route.set(target);
}

window.addEventListener('popstate', () => {
  route.set(getPath());
});