<script>
  import { createEventDispatcher } from 'svelte';
  const dispatch = createEventDispatcher();
  import { navigate } from '../components/stores/router';

  let username = '';
  let email = '';
  let password = '';
  let success = '';
  let error = '';

  const validateEmail = (email) => {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
  };

  const handleRegister = async () => {
    success = '';
    error = '';

    if (!username || !email || !password) {
      error = 'Todos los campos son obligatorios';
      return;
    }
    if (!validateEmail(email)) {
      error = 'Email inválido';
      return;
    }
    if (password.length < 6) {
      error = 'La contraseña debe tener al menos 6 caracteres';
      return;
    }

    try {
      const res = await fetch('http://localhost:8000/api/users/register/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, email, password })
      });

      const data = await res.json();

      if (!res.ok) {
        error = data.error || 'Error en el registro';
        return;
      }

      success = 'Registro exitoso';
      error = '';

      setTimeout(() => {
        dispatch('navigate', { page: 'login' });
      }, 1000);

    } catch (err) {
      error = 'Error al conectar con el servidor';
    }
  };

  const goToLogin = () => {
    navigate('/login');
    dispatch('navigate', { page: 'login' });
  };
</script>

<div class="card-container">
  <div class="card">
    <h1>Registrarse</h1>

    {#if error}
      <p class="error">{error}</p>
    {/if}
    {#if success}
      <p class="success">{success}</p>
    {/if}

    <input type="text" placeholder="Nombre de usuario" bind:value={username} />
    <input type="email" placeholder="Correo electrónico" bind:value={email} />
    <input type="password" placeholder="Contraseña" bind:value={password} />

    <button on:click={handleRegister}>Crear cuenta</button>

    <p class="link">
      ¿Ya tienes cuenta?
      <a href="/login" on:click|preventDefault={goToLogin}>Inicia sesión</a>
    </p>
  </div>
</div>

<style>
  /* Fondo general */
  .card-container {
    width: 100%;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    background: linear-gradient(135deg, #e0f7e9, #ffffff);
    font-family: 'Segoe UI', sans-serif;
  }

  /* Card */
  .card {
    background: rgba(255, 255, 255, 0.95);
    padding: 2.5rem;
    border-radius: 2rem;
    width: 100%;
    max-width: 400px;
    box-shadow: 0 15px 40px rgba(0, 128, 0, 0.2);
    animation: fadeInUp 0.8s ease forwards;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
  }

  .card:hover {
    transform: translateY(-5px);
    box-shadow: 0 25px 50px rgba(0, 128, 0, 0.3);
  }

  .card h1 {
    color: #006400;
    text-align: center;
    margin-bottom: 2rem;
    letter-spacing: 1px;
    font-size: 2rem;
  }

  input {
    width: 100%;
    background: #f0fff5;
    border: 2px solid #b2ffcc;
    border-radius: 0.5rem;
    padding: 0.75rem 1rem;
    color: #004d00;
    margin-bottom: 1.5rem;
    font-size: 1rem;
    transition: all 0.3s ease;
  }

  input:focus {
    outline: none;
    border-color: #00cc66;
    box-shadow: 0 0 10px #00cc6644;
    transform: scale(1.03);
  }

  button {
    width: 100%;
    background: linear-gradient(90deg, #00cc66, #00ff88);
    border: none;
    color: #fff;
    padding: 0.75rem;
    font-weight: bold;
    border-radius: 1rem;
    cursor: pointer;
    font-size: 1rem;
    transition: all 0.3s ease;
  }

  button:hover {
    background: linear-gradient(90deg, #00ff88, #00cc66);
    box-shadow: 0 0 15px #00ff88aa;
    transform: translateY(-3px);
  }

  .error {
    color: #ff4444;
    text-align: center;
    margin-bottom: 1rem;
    animation: shake 0.3s;
  }

  .success {
    color: #008000;
    text-align: center;
    margin-bottom: 1rem;
    animation: fadeIn 0.5s ease forwards;
  }

  .link {
    color: #004d00;
    text-align: center;
    margin-top: 1.5rem;
    font-size: 0.95rem;
  }

  .link a {
    color: #00cc66;
    text-decoration: none;
    margin-left: 0.25rem;
    transition: color 0.3s;
  }

  .link a:hover {
    color: #00ff88;
  }

  /* Animaciones */
  @keyframes fadeInUp {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
  }

  @keyframes shake {
    0% { transform: translateX(0); }
    25% { transform: translateX(-5px); }
    50% { transform: translateX(5px); }
    75% { transform: translateX(-5px); }
    100% { transform: translateX(0); }
  }

  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }
</style>
