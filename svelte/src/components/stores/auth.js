// src/stores/auth.js
import { writable, derived } from 'svelte/store';

const LS_KEY = 'svelte-food-user';

// Inicializar desde localStorage (si existe)
let initial = null;
try {
  const raw = localStorage.getItem(LS_KEY);
  if (raw) initial = JSON.parse(raw);
} catch (e) {
  initial = null;
}

export const user = writable(initial);
user.subscribe(u => {
  try {
    localStorage.setItem(LS_KEY, JSON.stringify(u));
  } catch (e) {
    // ignorar
  }
});

export const loggedIn = derived(user, $user => !!$user);

// Simula login: en una app real validas contra backend
export async function login({ username, password }) {
  if (!username || !password) {
    throw new Error('Usuario o contraseña vacíos');
  }
  // simulación: aceptar cualquier username/password no vacío
  const simulatedUser = { name: username };
  user.set(simulatedUser);
  return simulatedUser;
}

export function logout() {
  user.set(null);
}