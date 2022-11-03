<template>
  <div class="notifications-list">
    <notification-message
      v-for="notification in notifications"
      :key="notification.id"
      :notification="notification"
    />
  </div>
</template>

<style scoped src="./notifications-list.css"></style>
<script src="./notifications-list.js"></script> 
