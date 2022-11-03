<template>
  <div class="pagination-wrapper">
   <page-information
       :total-items="totalRows"
       :first-item-index-in-page="initialPageItem"
       :last-item-index-in-page="lastPageItem"
   />
   <pagination
       :current-page="currentPage"
       :pages="pages"
       v-on:change-page="onChangePage"
   />
  </div>
</template>

<style scoped src="./search-pagination.css"></style>

<script src="./search-pagination.js"></script>
