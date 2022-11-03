<template>
<div class="split-container">

    <ashes-modal
        title="Create Event&nbsp;&nbsp;&nbsp;"
        :message="ashesDate"
        :query="ashesQuery"
        :show="showAshesModal"
        @close="showAshesModal = false"
        @reset="() => { 
            //deleteEvent();
            showAshesModal = false;
        }" 
        ref="AshesModal"
    />
    
    <nav class="font-sans flex flex-col text-center sm:flex-row sm:text-left sm:justify-between py-4 px-6 bg-white shadow sm:items-baseline w-full">
        <div class="mb-2 sm:mb-0">
            <a href="./" class="text-2xl no-underline text-grey-darkest hover:text-blue-dark">&nbsp;</a>
        </div>
        <calendar-pagination></calendar-pagination>
        <div class="mb-5 sm:mb-0">                                    
            <div class="">
                <button @click="addNewCalendar();" class="split-view-plus p-0 w-12 h-12 bg-gray-600 rounded-full hover:bg-gray-700 active:shadow-lg mouse shadow transition ease-in duration-200 focus:outline-none">
                    <svg viewBox="0 0 20 20" enable-background="new 0 0 20 20" class="w-6 h-6 inline-block">
                        <path fill="#FFFFFF" d="M16,10c0,0.553-0.048,1-0.601,1H11v4.399C11,15.951,10.553,16,10,16c-0.553,0-1-0.049-1-0.601V11H4.601
                                    C4.049,11,4,10.553,4,10c0-0.553,0.049-1,0.601-1H9V4.601C9,4.048,9.447,4,10,4c0.553,0,1,0.048,1,0.601V9h4.399
                                    C15.952,9,16,9.447,16,10z" />
                    </svg>
                </button>
            </div>
        </div>        
    </nav>


    <agile ref="ag_canvas" :key="renderRequired" :options='slideOptions' v-on:close="onClose()">                           
        <div v-for="(slide) in slides" :key="slide.id">                       
            <geomatics-calendar ref="'ag_cal'+slide.id" :initialid="slide.siteId" :windowIdIndex="slide.windowIdIndex" @ashesModalFromChild="handleAshesModal" @closeFromChildCalendar="handleCloseEvent" @changeSiteFromChildCalendar="handleSiteChangeEvent"></geomatics-calendar>                          
        </div>       
    </agile>

</div>
</template>

<script src="./split-view.js"></script>
<style src="./split-view.css"></style>