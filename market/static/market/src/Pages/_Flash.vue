<template >
<div>
  <div v-if="$page.flash.success && show" class="px-5 py-5">
      <div class="message is-small" v-bind:class="{'is-success': !$page.flash.error, 'is-danger': $page.flash.error }">
        <div class="message-header">
          <p>Message</p>
          <button class="delete is-small" @click="show=false"></button>
        </div>
        <div class="message-body">
            {{$page.flash.success}}
        </div>
      </div>
  </div>

    <div v-if="($page.flash.error || Object.keys($page.errors).length > 0 ) && show" class="px-5 py-5">
      <div class="message is-small" v-bind:class="{'is-success': !$page.flash.error, 'is-danger': $page.flash.error }">
        <div class="message-header">
          <p>Message</p>
          <button class="delete is-small" @click="show=false"></button>
        </div>
        <div v-if="$page.flash.error" class="message-body">
            {{$page.flash.error}}
        </div>
      </div>
  </div>
</div>
</template>
<script>
export default {
  name: 'flash-message',
  data() {
    return {
      show: true,
    }
  },
  watch: {
    '$page.flash': {
      handler() {
        this.show = true
      },
      deep: true,
    },
  },
}
</script>
