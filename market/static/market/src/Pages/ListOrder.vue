
<template>
<div id="list-order" class="container">
  <flash-messages/>
    <tabs />
  <h1 class="subtitle my-3">Orders</h1>
    <div class="container my-5" v-for="order in orders">
      <div class="my-3">
        <span class="has-text-weight-bold  is-family-sans-serif ">Order {{order.id}}</span>
        <span class="tag" 
          :class="{
          'is-light':'n' === order.status,
          'is-primary':'s' === order.status,
          'is-success':'r' === order.status,
          'is-danger':'c' === order.status }">
            {{status[order.status]}}
        </span>
            <div class="select is-small">
              <select v-model="order.current_status">
                <option v-for="(key, value) in status" :value="value"
                :selected="order.status === value">{{key}}</option>
              </select>
            </div>
         <button class="button is-small" @click="change(order)">Change</button>
         <button class="button is-small is-light is-danger" @click="deleteOrder(order)">Delete</button>
        
      </div>
        <table class="table is-fullwidth is-narrow">
          <tr>
            <th>Name</th>
            <th>Quantity</th>
            <th>Unit Price</th>
            <th>Total</th>
          </tr>
          <tr v-for="row in order.cart.cart_rows">
            <td>{{row.food.name}}</td>
            <td>{{row.quantity}}</td>
            <td>{{row.price}}</td>
            <td>{{ fixed(row.quantity*row.price)}}</td>
          </tr>
          <tr>
            <td colspan="2"></td>
            <td class="has-text-right has-text-weight-semibold  ">Total</td>
            <td>{{calc(order.cart.cart_rows)}}</td>
          </tr>
        </table>
    </div>
</div>
</template>


<script>
import fit from '../utils.js';
import FlashMessages from './_Flash';
import Tabs from './_Tabs';

export default {
  name: "ListOrder",
  components:{
    FlashMessages,
    Tabs
  },
  props: {
    orders: Array,
    status: Object,
  },
  data () {
    return {
    }
  },
  methods: {
    calc (elements) {
      let els = elements.map( (e) => fit.fit(e.quantity*e.price));
      return this.fixed(els.reduce((a,b) => parseFloat(a)+parseFloat(b)));
    },
    fixed (n) {
      return fit.fit(n)
    },
    change(order) {
      this.$inertia.put('/api/orders/'+order.id, {'status':order.current_status}).then(resp=>
        { 
          this.$inertia.reload();
        });
    },
    deleteOrder(order) {
      this.$inertia.delete('/api/orders/'+order.id).then(resp=>
        { 
          this.$inertia.reload();
        });
    }
  }
}
</script>


