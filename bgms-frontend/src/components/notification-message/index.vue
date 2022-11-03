
<template>
  <div :class="typeClass" class="alert" role="alert">
    <button type="button" class="closebtn" data-dismiss="alert" aria-label="close" v-on:click="removeNotification">
      <span aria-hidden="true">&times;</span>
    </button>
    {{ notification.message }}
  </div>
</template>

<style scoped src="./notification-message.css"></style>
<script src="./notification-message.js"></script>
