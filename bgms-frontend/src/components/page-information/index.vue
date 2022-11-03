<template>
 <div class="page-information">
      <div class="text-wrapper">
        <p>
          Showing
          <span> {{ firstItemIndexInPage }}</span>
          to
          <span> {{ lastItemIndexInPage }}</span>
          of
          <span>{{ totalItems }}</span>
          results
        </p>
      </div>
 </div>
</template>

<style scoped src="./page-information.css"></style>

<script src="./page-information.js"></script>
