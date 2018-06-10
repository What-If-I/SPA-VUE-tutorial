<template>
  <div>
    <b-alert :variant="variant"
             dismissible
             @dismissed="dismissCountDown=0"
             @dismiss-count-down="countDownChanged"
             :show="dismissCountDown"
             fade
    >{{ message }}</b-alert>
    <br>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        dismissSecs: 5,
        dismissCountDown: 0,
        message: '',
        variant: 'success',
      }
    },
    name: 'Alert',
    methods: {
      countDownChanged(dismissCountDown) {
        this.dismissCountDown = dismissCountDown
      },
      show(msg) {
        this.message = msg
        this.dismissCountDown = this.dismissSecs
      },
      showSuccess(msg) {
        this.variant = 'success'
        this.show(msg)
      },
      showError(msg) {
        this.variant = 'danger'
        this.show(msg)
      },
    },
  }
</script>

<style scoped>

</style>
