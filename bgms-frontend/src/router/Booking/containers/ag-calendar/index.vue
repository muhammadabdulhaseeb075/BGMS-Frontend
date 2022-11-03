<template>
<div>
<!--
    <ashes-modal
        title="Select Type &nbsp;&nbsp;&nbsp;"
        message="&nbsp;"    
        :query= "ashesQuery"   
        :show="showAshesModal"
        @close="showAshesModal = false"
        @reset="() => { 
            //deleteEvent();
            showAshesModal = false;
        }" 
        ref="AshesModal"
    />
    -->

<div class="ag-calendar-wrapper">
    <!-- CALENDAR VIEW -->
    <div class="calendar-header">
        <nav class="font-sans flex flex-col text-center sm:flex-row sm:text-left sm:justify-between py-4 px-6 bg-white shadow sm:items-baseline w-full">
          <div class="mb-2 sm:mb-0">
            <h3> <!--Site Select Stlyed via H3 Styles-->
            <select name="site_select" v-model="siteId" @change="$emit('changeSiteFromChildCalendar', {index: this.windowIdIndex, new:$event.target.value})">
            <!--<select name="site_select" v-model="siteId" @change="changeLocalSite($event.target.value)"> -->
              <option v-for="site in getSiteList" :key="site.id" :value="parseInt(site.id)">
                  {{ site.name}}
              </option>        
            </select>              
            </h3>
          </div> <!--Close Button-->
          <button v-if="showCloseButton" v-on:click="$emit('closeFromChildCalendar', this.windowIdIndex)" class="ag_calender_exit p-0 w-10 h-10 bg-white-600 rounded-full hover:bg-gray-700 active:shadow-lg mouse shadow transition ease-in duration-200 focus:outline-none">
            <i class="far fa-times-circle"></i>
          </button>
        </nav>
    </div>
    
      <FullCalendar
        ref='ag_calendar' 
        class='geomatics-calendar'        
        :options='calendarOptions'
      >
        <template v-slot:eventContent='arg'>
          <b>{{ arg.timeText }}</b>
          <i>{{ arg.event.title }}</i>
        </template>
      </FullCalendar>

    <!-- TOOLTIP INFO -->
    <div class="tooltip" :class="{visible: showTooltip}" ref="tooltipref" role="tooltip">
        <div class="toolip-body p-6">
            <div class="tooltip-title font-bold">
                {{selectedEvent && selectedEvent.details}}
            </div>
            <div class="tooltip-date text-xs mt-4">
               <i class="far fa-clock"></i> {{selectedEvent && selectedEvent.display_date}}<br/>
               <b> {{selectedEvent && selectedEvent.event_category}} </b>
            </div>
            <div class="footer-opt flex text-sm mt-2">
                <div class="cursor-pointer mr-6" @click="editEvent">
                  <i class="fas fa-eye"></i> <b>View/Edit</b>
                </div>
                <!-- uncomment to allow deletion for events -->
                <!-- <div  class="cursor-pointer mr-6" @click="() => showRemoveConfirm = true">
                    <i class="fas fa-trash-alt"></i> Delete
                </div> -->
              <div class="cursor-pointer mr-6" @click="editStatus">
                <i class="fas fa-stream"></i>
                <b v-if="selectedEvent && selectedEvent.status == 2"> Pre-Burial Checks</b>
                <b v-else-if="selectedEvent && selectedEvent.status == 3"> Awaiting Burial</b>
                <b v-else-if="selectedEvent && selectedEvent.status == 4"> Post-Burial Checks</b>
                <b v-else-if="selectedEvent && selectedEvent.status == 5"> Completed</b>
                <b v-else-if="SelectedEvent && selectedEvent.status == 7"> Cancelled</b>
              </div>

            </div>
        </div>
        <div class="arrow" data-popper-arrow :class="{visible: showTooltip}" ></div>
    </div>

    <!--Confirmation Modal for Deleting Events - Is this used?-->
    <confirm-modal
        title="Confirmation needed"
        message="Are you sure you want to remove this event?"
        :show="showRemoveConfirm"
        @close="showRemoveConfirm = false"
        @reset="() => { 
            deleteEvent();
            showRemoveConfirm = false;
        }"
    />

</div>
</div>
</template>
<script src="./ag-calendar.ts"></script>
<style src="./ag-calendar.css"></style>