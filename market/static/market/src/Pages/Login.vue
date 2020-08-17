<template>
 <div class="hero is-success is-fullheight">
        <div class="hero-body">
            <div class="container has-text-centered">
                <div class="column is-4 is-offset-4">
                    <h3 class="title has-text-grey">Login</h3>
                    <p class="subtitle has-text-grey">Please login to proceed.</p>
                    <div class="box">
                        <figure class="avatar">
                            <img src="https://placekitten.com/128/128">
                        </figure>

										<form>
										

      <button :disabled="form.busy" type="submit" class="button is-block is-info is-large is-fullwidth" :class="{'is-loading': form.busy}">
        Log In
      </button>	

										</form>


										</div>
                    <p class="has-text-grey">
                        <a href="../">Sign Up</a> &nbsp;·&nbsp;
                        <a href="../">Forgot Password</a> &nbsp;·&nbsp;
                        <a href="../">Need Help?</a>
                    </p>
                </div>
            </div>
        </div>
    </div>

</template>


<script>

export default {
  name: "Login",
  props: {
  },
  data () {
    return {
      data:[]
    }
  }
}
</script>
