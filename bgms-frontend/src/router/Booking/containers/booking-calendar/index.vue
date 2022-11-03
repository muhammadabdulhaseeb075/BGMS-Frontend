<template>

<div class="booking-calendar-wrapper">
    <!-- CALENDAR HEADER -->
    <div class="calendar-header">
        <div class="calendar-info flex" v-if="fCalendar">
            <div class="calendar-button">
                <button class="rounded-l-lg border border-gray-200" @click="goTodayCalendar">
                    Today
                </button>
                <button @click="prevRangeCalendar">
                    <i class="rounded-l-lg border border-gray-200 fas fa-chevron-left"></i>
                </button>
                <button @click="nextRangeCalendar">
                    <i class="rounded-l-lg border border-gray-200 fas fa-chevron-right"></i>
                </button>
            </div>
            <p class="date-range-title" >{{dateRangeTitle}}</p>
        

        <h3>{{currentSiteName}}</h3>
        <!-- Static Test Buttons Tailwind Styles Apply
        <div class="max-w-lg mx-auto">
            <div class="inline-flex shadow-sm rounded-md mb-5" role="group">
            <button type="button" class="rounded-l-lg border border-gray-200 bg-white text-sm font-medium px-4 py-2 text-gray-900 hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-2 focus:ring-blue-700 focus:text-blue-700">
                Profile
            </button>
            <button type="button" class="border-t border-b border-gray-200 bg-white text-sm font-medium px-4 py-2 text-gray-900 hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-2 focus:ring-blue-700 focus:text-blue-700">
                Settings
            </button>
            <button type="button" class="rounded-r-md border border-gray-200 bg-white text-sm font-medium px-4 py-2 text-gray-900 hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-2 focus:ring-blue-700 focus:text-blue-700">
                Messages
            </button>
            </div>        
        </div>-->
   
</div>
    </div>

    <!-- CALENDAR VIEW -->
    <div class="booking-calendar" ref="calendarref">
    </div>

    <!-- TOOLTIP INFO -->
    <div class="tooltip" :class="{visible: showTooltip}" ref="tooltipref" role="tooltip">
        <div class="toolip-body p-6">
            <div class="tooltip-title font-bold">
                {{selectedEvent && selectedEvent.details}}
            </div>
            <div class="tooltip-date text-xs mt-4">
               <i class="far fa-clock"></i> {{selectedEvent && selectedEvent.display_date}}
            </div>
            <div class="footer-opt flex text-sm mt-2">
                <div class="cursor-pointer mr-6" @click="editEvent">
                    <i class="fas fa-eye"></i> View
                </div>
                <!-- uncomment to allow deletion for events -->
                <!-- <div  class="cursor-pointer mr-6" @click="() => showRemoveConfirm = true">
                    <i class="fas fa-trash-alt"></i> Delete
                </div> -->
            </div>
        </div>
        <div class="arrow" data-popper-arrow :class="{visible: showTooltip}" ></div>
    </div>

    <!-- -->
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
</template>

<script src="./booking-calendar.js"></script>

<style src="./booking-calendar.css"></style>
