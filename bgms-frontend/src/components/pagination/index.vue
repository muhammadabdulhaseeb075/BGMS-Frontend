<template>
   <div>
     <nav class="pagination" aria-label="Pagination">
          <div class="page-option option-left-rounded option-hover" @click="previousPage">
            <span class="sr-only">Previous</span>
            <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
              <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
            </svg>
          </div>
          <a class="page-option"
             v-for="headPage in headPages"
             v-bind:class="{ 'page-option-selected': currentPage === headPage}"
             @click="(mouseEvent) => changePage(mouseEvent, headPage)"
          >
            {{ headPage }}
          </a>
          <span class="page-option" v-if="leftEllipsisButtonActive">
            ...
          </span>
          <a class="page-option"
             v-for="bodyPage in bodyPages"
             v-bind:class="{ 'page-option-selected': currentPage === bodyPage}"
             @click="(mouseEvent) => changePage(mouseEvent, bodyPage)"
          >
            {{ bodyPage }}
          </a>
          <span class="page-option" v-if="rightEllipsisButtonActive">
            ...
          </span>
          <a class="page-option"
             v-for="tailPage in tailPages"
             v-bind:class="{ 'page-option-selected': currentPage === tailPage}"
             @click="(mouseEvent) => changePage(mouseEvent, tailPage)"
          >
            {{ tailPage }}
          </a>
          <div class="page-option option-right-rounded option-hover" @click="nextPage">
            <span class="sr-only">Next</span>
            <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
              <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
            </svg>
          </div>
        </nav>
    </div>
</template>

<style scoped src="./pagination.css"></style>

<script src="./pagination.js"></script>
