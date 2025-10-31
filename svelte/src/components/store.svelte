<script>
  import { onMount } from "svelte";

  const THEME = {
    primary: "#2f8f46",
    light: "#e8f8ef",
    contrast: "#ffffff",
    accent: "#1f6f36"
  };

  let products = [];
  let loading = true;
  let cart = {};

  onMount(() => {
    try {
      const raw = localStorage.getItem("svelte-food-cart");
      if (raw) cart = JSON.parse(raw);
    } catch (e) {
      cart = {};
    }

    fetch("http://127.0.0.1:8000/api/store/products/")
      .then(res => res.json())
      .then(data => {
        products = data.map(p => ({
          ...p,
          name: p.name.replace(/"/g, ''),
          price: parseFloat(p.price),
          image: p.image || null
        }));
        loading = false;
      })
      .catch(err => {
        console.error("Error cargando productos:", err);
        loading = false;
      });
  });

  $: localStorage.setItem("svelte-food-cart", JSON.stringify(cart));

  function addToCart(productId) {
    const product = products.find(p => p.id === productId);
    if (!product) return;
    if (!cart[productId]) {
      cart = { ...cart, [productId]: { product, qty: 1 } };
    } else {
      cart = {
        ...cart,
        [productId]: { product, qty: cart[productId].qty + 1 }
      };
    }
  }

  function increase(productId) {
    if (!cart[productId]) return;
    cart = {
      ...cart,
      [productId]: { product: cart[productId].product, qty: cart[productId].qty + 1 }
    };
  }

  function decrease(productId) {
    if (!cart[productId]) return;
    const newQty = cart[productId].qty - 1;
    if (newQty <= 0) {
      const { [productId]: _, ...rest } = cart;
      cart = rest;
    } else {
      cart = {
        ...cart,
        [productId]: { product: cart[productId].product, qty: newQty }
      };
    }
  }

  function removeItem(productId) {
    const { [productId]: _, ...rest } = cart;
    cart = rest;
  }

  function clearCart() {
    cart = {};
  }

  $: cartItems = Object.values(cart);
  $: totalItems = cartItems.reduce((s, it) => s + it.qty, 0);
  $: totalPrice = cartItems.reduce((s, it) => s + it.qty * it.product.price, 0).toFixed(2);

  function checkout() {
    if (totalItems === 0) {
      alert("Tu carrito está vacío.");
      return;
    }
    alert(`Gracias por tu compra: ${totalItems} items por $${totalPrice}`);
    clearCart();
  }
</script>

<style>
  :global(body) {
    margin: 0;
    font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
    background: linear-gradient(180deg, #e8f8ef 0%, #fbfffc 100%);
    color: #314a36;
    overflow-y: auto !important;
  }

  .store {
    display: grid;
    grid-template-columns: 1fr 370px;
    gap: 32px;
    padding: 32px;
    min-height: 100vh;
    background: inherit;
    box-sizing: border-box;
  }

  header {
    grid-column: span 2;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: var(--primary, #2f8f46);
    color: #fff;
    border-radius: 14px;
    padding: 16px 28px;
    margin-bottom: 16px;
    box-shadow: 0 4px 16px 0 rgba(47,143,70, 0.10);
  }

  .brand {
    display: flex;
    align-items: center;
    gap: 18px;
  }
  .logo {
    font-size: 2.6rem;
    background: var(--accent, #1f6f36);
    color: #fff;
    border-radius: 12px;
    padding: 8px 18px;
    display: flex;
    align-items: center;
    box-shadow: 0 2px 8px 0 rgba(47,143,70,0.13);
  }

  .products-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(230px, 1fr));
    gap: 28px;
    padding-bottom: 24px;
  }

  .card {
    display: flex;
    flex-direction: column;
    background: #fff;
    border-radius: 14px;
    padding: 18px 16px 16px 16px;
    box-shadow: 0 2px 14px rgba(47,143,70,0.09);
    transition: box-shadow 0.16s;
    border: 2px solid #e8f8ef;
    position: relative;
  }
  .card:hover {
    box-shadow: 0 4px 24px rgba(47,143,70,0.13);
    border-color: var(--primary, #2f8f46);
  }

  .product-image {
    width: 100%;
    height: 150px;
    object-fit: cover;
    border-radius: 12px;
    margin-bottom: 12px;
    background: #e8f8ef;
    border: 1.5px solid #e8f8ef;
    box-shadow: 0 2px 8px rgba(47,143,70,0.05);
  }

  .product-emoji {
    width: 100%;
    height: 150px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #e8f8ef;
    border-radius: 12px;
    font-size: 2.4rem;
    margin-bottom: 10px;
    color: var(--primary, #2f8f46);
    border: 1.5px solid #e8f8ef;
  }

  .product-info h3 {
    margin: 0;
    font-size: 1.13rem;
    color: var(--accent, #1f6f36);
    font-weight: 600;
  }

  .product-info p {
    margin: 6px 0 0 0;
    font-size: 0.98rem;
    color: #314a36;
    opacity: 0.9;
    min-height: 34px;
  }

  .price-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 14px;
    gap: 10px;
  }

  .price {
    font-size: 1.09rem;
    font-weight: bold;
    color: var(--primary, #2f8f46);
    background: #e8f8ef;
    border-radius: 7px;
    padding: 4px 10px;
  }

  .add {
    background: linear-gradient(90deg, var(--primary, #2f8f46) 80%, var(--accent, #1f6f36) 100%);
    color: #fff;
    border: none;
    padding: 7px 17px;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 600;
    font-size: 1rem;
    box-shadow: 0 2px 8px rgba(47,143,70,0.09);
    transition: background 0.14s, box-shadow 0.14s;
  }
  .add:hover {
    background: linear-gradient(90deg, var(--primary, #2f8f46) 60%, var(--accent, #1f6f36) 100%);
    box-shadow: 0 4px 16px rgba(47,143,70,0.13);
    opacity: 1;
  }

  /* Carrito y Footer */
  .cart-footer {
    position: sticky;
    bottom: 0;
    background: #fff;
    border-radius: 14px;
    box-shadow: 0 2px 16px 0 rgba(47,143,70,0.09);
    padding: 22px 18px;
    margin-top: 32px;
    display: flex;
    flex-direction: column;
    gap: 16px;
    border: 2px solid #e8f8ef;
  }

  .totals {
    display: flex;
    justify-content: space-between;
    font-size: 1.11rem;
    font-weight: 600;
    color: var(--primary, #2f8f46);
    margin-bottom: 8px;
  }

  .checkout {
    background: linear-gradient(90deg, var(--accent, #1f6f36) 80%, var(--primary, #2f8f46) 100%);
    color: #fff;
    border: none;
    padding: 8px 20px;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 600;
    font-size: 1.04rem;
    box-shadow: 0 2px 8px rgba(47,143,70,0.10);
    transition: background 0.14s, box-shadow 0.14s;
  }
  .checkout:hover {
    background: linear-gradient(90deg, var(--accent, #1f6f36) 60%, var(--primary, #2f8f46) 100%);
    box-shadow: 0 4px 16px rgba(47,143,70,0.13);
  }

  .clear {
    background: #e8f8ef;
    color: var(--primary, #2f8f46);
    border: none;
    padding: 7px 14px;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 500;
    font-size: 0.95rem;
    margin-left: 5px;
    box-shadow: 0 1px 4px rgba(47,143,70,0.07);
    transition: background 0.14s, color 0.14s;
  }
  .clear:hover {
    background: var(--primary, #2f8f46);
    color: #fff;
  }

  @media (max-width: 950px) {
    .store {
      grid-template-columns: 1fr;
      padding: 12px;
      gap: 12px;
    }
    header {
      flex-direction: column;
      align-items: flex-start;
      padding: 14px 8px;
    }
    .cart-footer {
      position: static;
      margin-top: 16px;
    }
  }
</style>

<div class="store" style="--primary: {THEME.primary}; --accent: {THEME.accent};">
  <header>
    <div class="brand">
      <div class="logo" title="Tienda">🍽️</div>
      <div>
        <h1 style="margin:0;font-size:1.5rem;">Tienda Verde — Comida</h1>
        <div style="font-size:0.97rem;opacity:0.88;">Sabor natural y rápido</div>
      </div>
    </div>
    <div style="display:flex;align-items:center;gap:18px">
      <div style="font-size:1.06rem;color:#fff;">
        <strong>{totalItems}</strong> ítems
      </div>
      <button class="clear" on:click={clearCart}>Vaciar</button>
    </div>
  </header>

  <main class="products" aria-live="polite">
    {#if loading}
      <p>Cargando productos...</p>
    {:else}
      <div class="products-grid">
        {#each products as p}
          <article class="card" aria-labelledby={"p-"+p.id}>
            {#if p.image}
              <img src={p.image} alt={p.name} class="product-image" />
            {:else}
              <div class="product-emoji">🍽️</div>
            {/if}
            <div class="product-info">
              <h3 id={"p-"+p.id}>{p.name}</h3>
              <p>{p.description}</p>
              <div class="price-row">
                <div class="price">${p.price.toFixed(2)}</div>
                <button class="add" on:click={() => addToCart(p.id)}>Agregar</button>
              </div>
            </div>
          </article>
        {/each}
      </div>
    {/if}
  </main>
  <div class="cart-footer">
    <div class="totals">
      <div>Total</div>
      <div>${totalPrice}</div>
    </div>
    <div style="display:flex;gap:12px">
      <button class="checkout" on:click={checkout}>Pagar</button>
      <button class="clear" on:click={clearCart}>Vaciar</button>
    </div>
  </div>
</div>