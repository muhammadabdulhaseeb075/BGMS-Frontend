<template>
  <div
      ref="time"
      tabindex="-1"
      @blur="showCardContainer = false"
      :class="{'time-picker-container': true, 'active': disabled}"
  >
    <input
        class="time-picker"
        v-model="timeValue"
        @input="updateTimeParts"
        v-bind="$props"
   />
     <div v-if="!disabled" class="fas fa-chevron-down time-picker-button" @click="openOrHideContainer" />
     <div
         class="time-container"
         v-show="showCardContainer"
     >
            <div class="time-row">
              <div
                class="time-option"
                v-for="(hour) in hours"
                :key="'hour'+hour"
                v-bind:class="{ 'time-active': hourSelected === hour }"
                @click="selectHour(hour)"
              >{{ hour }}</div>
            </div>
            <div class="time-row">
              <div
                class="time-option"
                v-for="(minute) in minutes"
                :key="'minute'+minute"
                v-bind:class="{ 'time-active': minuteSelected === minute }"
                @click="selectMinutes(minute)"
              >{{ minute }}</div>
            </div>
            <div class="time-row">
              <div
                class="time-option"
                v-for="(meridiemCategory) in meridiemCategories"
                :key="'meridiemCategory'+meridiemCategory"
                v-bind:class="{ 'time-active': meridiemCategorySelected === meridiemCategory }"
                @click="selectMeridiemCategory(meridiemCategory)"
              >{{ meridiemCategory }}</div>
            </div>
     </div>
  </div>
</template>

<style scoped src="./time-picker.css"></style>

<script src="./time-picker.js"></script>
