<template>

  <div class="container">
    <div class="tabs">
      <ul>
        <li>
          <inertia-link :href="route('market:orders')">Orders</inertia-link> 
        </li>
        <li>
          <inertia-link :href="route('market:index')">Cart</inertia-link> 
        </li>
        <li>
          <inertia-link :href="route('market:logout')">Logout</inertia-link>
        </li>
        <li>
          <a href="/admin" target="_blank">Go to Admin</a>
        </li>
      </ul>
    </div>
  </div>


</template>
<script>
export default {
  name: 'tabs',
  data() {
    return {
    }
  },
}
</script>
