<template>
<div class="container">
  <flash-messages />
    <tabs></tabs>
    <h1 class="subtitle my-3">Cart of {{user}} </h1>
        <div class="field is-grouped">
            <div class="control ">
              <div class="select">
                <select v-model="foodSelected">
                  <option v-for="food in foods" v-bind:value="food" >{{food.name}}</option>
                </select>
              </div>
            </div>
            <div class="control">
              <button class="button is-info" v-on:click="addFood()">+</button>
            </div>
          </div>
  <table class="table is-fullwidth">
    <tr>
      <th>Name</th>
      <th>Unit Price</th>
      <th>Quantity</th>
      <th>Total</th>
      <th></th>
    </tr>

    <tr v-for="food in rows">
      <td>{{food.name}}</td>
      <td>{{food.price}}</td>
       <td>
         {{food.quantity}}
        <button class="button is-small" v-on:click="addQuantity(food)">+</button>
        <button class="button is-small" v-on:click="removeQuantity(food)">-</button>
       </td>
       <td>
         {{calcPrice(food)}}
       </td>
       <td>
        <button class="button is-small is-danger" v-on:click="removeRow(food)">-</button>
       </td>
    </tr>
    <tr>
      <td colspan="3" class="has-text-right"> Total</td>
      <td>{{bigTotal}}</td>
    </tr>
    <tr>
      <td colspan="3"></td>
      <td colspan="2">
        <button v-on:click="submitOrder()" v-bind:class="{'is-loading':sending}"
          v-bind:disabled="sending || rows.length==0" 
                class="button is-success">Send Order</button>
      </td>
    </tr>
  </table>
</div>

</template>

<script>
import FlashMessages from './_Flash';
import Tabs from './_Tabs';
import utils from '../utils';

export default {
  name: 'Index',
  props: {
    foods: Array,
    user: String
  },
  components:{
    FlashMessages,
    Tabs
  },
  data() {
    return {
      sending: false,
      foodSelected: false,
      rows:[],
      bigTotal: 0,
    }
  },
  methods:{
    calcPrice(food) {
      return utils.fit(food.price*food.quantity);
    },
    removeQuantity(food) {
      if (food.quantity > 1) {
        food.quantity-=1;
      }
      this.updateTotal();
    },
    addQuantity(food){
      food.quantity+=1;
      this.updateTotal();
    },
    addFood() {
      let row = JSON.parse(JSON.stringify(this.foodSelected));
      // init quantity yey!!
      row.quantity=1;
      row.food = row.id;
      this.rows.push(row);
      this.updateTotal();
    },
    removeRow(food){
      this.rows.splice(this.rows.indexOf(food),1);
      this.updateTotal();
    },
    updateTotal(){
      let rowsTotal = this.rows.map(e => e.quantity*e.price);
      // TODO: fix the biggerFloat
      if( this.rows.length > 0 ) {
        this.bigTotal = utils.fit(rowsTotal.reduce( (a,b) => a+b));
      } else {
        this.bigTotal = 0;
      }
    },
    submitOrder() {
      this.sending = true;
      this.$inertia.post(this.route('market:create_cart'), this.rows).then(() => {
        this.sending = false;
      });
    }
  }
}
</script>
