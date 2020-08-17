<template>
<div id="login">
  <flash-messages/>
 <div class="hero is-success ">
        <div class="hero-body">
            <div class="container has-text-centered">
                <div class="column is-4 is-offset-4">
                    <h3 class="title has-text-grey">Login</h3>
                    <p class="subtitle has-text-grey">Please login to proceed.</p>
                    <div class="box">
                        <figure class="avatar">
                            <img src="https://placekitten.com/128/128">
                        </figure>
										<form @submit.prevent="submit">
                       <div class="field">
                        <div class="control">
                            <input v-model="form.email" autofocus autocapitalize="off" type="text" 
                              autocomplete="off"
                              class="input is-large" placeholder="Username">
                        </div>
                      </div>
                       <div class="field">
                        <div class="control">
                            <input v-model="form.password" type="password" autocomplete="off" class="input is-large" placeholder="Password">
                        </div>
                      </div>
                      <button  type="submit" class="button is-block is-info is-large is-fullwidth"
                                :class="{'is-loading': sending}">
                        Log In
                      </button>	
										</form>
										</div>
                          <p class="has-text-grey">
                            <inertia-link :href="route('market:index')">Go to Index</inertia-link>
                          </p>
                </div>
            </div>
        </div>
    </div>

</div>
</template>


<script>
import FlashMessages from './_Flash'

export default {
  name: "Login",
  components:{
    FlashMessages
  },
  props: {
  },
  data () {
    return {
      sending:false,
      form: {
        email: "",
        password: ""
      }
    }
  },
  methods: {
    submit() {
      this.sending=true;
      this.$inertia.post(this.route('market:login'), {
                email: this.form.email,
                password: this.form.password
      }).then(() => this.sending = false).catch( (error) => {
        console.error(error);
      })
    }
  }
}
</script>


