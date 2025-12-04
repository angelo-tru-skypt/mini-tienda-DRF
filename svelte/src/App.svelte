<script>
  import { onMount } from 'svelte';
  import { get } from 'svelte/store';
  import { route, navigate } from './components/stores/router';
  import { loggedIn } from './components/stores/auth.js';

  import Login from './components/Login.svelte'
  import Store from './components/store.svelte';
  import Register from './components/Register.svelte'; 

  onMount(() => {
    const current = get(route);
    const isLogged = get(loggedIn);

    if (current === '/' || current === '') {
      if (isLogged) navigate('/store', { replace: true });
      else navigate('/login', { replace: true });
    }

  });

  $: if ($route === '/store' && !$loggedIn) {
    navigate('/store', { replace: true });
  } else if (($route === '/login' || $route === '/') && $loggedIn) {
    navigate('/login', { replace: true });
  }
</script>

{#if $route === '/store'}
  <Store />
{:else if $route === '/login'}
  <Login />
{:else if $route === '/register'}
  <Register />
{:else}
  <Login />
{/if}
