<template>
<div class="search-table">
    <!-- -->
    <div class="table-top">
        <h3>Results</h3>
        <div class="result-entries">
            <span>Total Results: </span>
            <span class="font-bold">{{ totalRows }}</span>
        </div>
    </div>

    <div class="table-results">
        <div class="table-content">
            <div class="table-header">
                <div class="row">
                    <div class="cell">Reference</div>
                    <div class="cell">Deceased</div>
                    <div class="cell">Date</div>
                    <div class="cell">Site</div>
                    <div class="cell">Funeral Director</div>
                    <div class="cell">Type</div>
                    <div class="cell">Status</div>
                    <div class="cell"></div>
                </div>
            </div>

            <!-- -->
            <div class="table-body">
                <div class="row" v-for="event in searchResultEvent" :key="event.id">
                    <div class="cell">{{event.reference}}</div>
                    <div class="cell">{{event.first_names}} {{event.last_name}}</div>
                    <div class="cell">{{event.start_date}} {{event.start_time}}</div>
                    <div class="cell">{{getSiteName(event.site_id)}}</div>
                    <div class="cell">{{ funeralDirectorOption(event.funeral_director_name, 
                      event.funeral_director_title,
                      event.funeral_director_company_name,
                      event.funeral_director_last_names) }}</div>
                    <div class="cell">{{event.cremated?"Ashes":"Burial"}}</div>
                    <div class="cell">
                      <b v-if="event.status == 2"> Pre-Burial Checks</b>
                      <b v-else-if="event.status == 3"> Awaiting Burial</b>
                      <b v-else-if="event.status == 4"> Post-Burial Checks</b>
                      <b v-else-if="event.status == 5"> Completed</b>
                      <b v-else-if="event.status == 7"> Cancelled</b>
                    </div>
                    <!--<div class="cell">{{event.status}}</div>-->
                    <div class="cell">
                        <i
                            class="fas fa-edit text-2xl mx-1"
                            title="View"
                            @click="editEvent(event.id, event.site_id)"
                        ></i>
                        <i class="far fa-file text-2xl mx-1"
                        title="Booking Status"
                          @click="editStatus(event.id, event.site_id)"
                        ></i>
                        <button class="text-center w-10" :disabled="!event?.map_management?.has_grave" @click="openMapWithGravePlot(event?.map_management, event.site_id)">
                          <i v-if="event?.map_management?.has_grave" class="fas fa-map-marker-alt  text-2xl mx-1"></i>
                          <span v-if="!event?.map_management?.has_grave" class="fa-stack fa-1x">
                            <i class="fas fa-map-marker-alt fa-stack-1x" style="color: gray"></i>
                            <i class="fas fa-ban fa-stack-2x" style="color: tomato" title="Go to Map"></i>
                          </span>
                        </button>
                    </div>
                </div>
            </div>

        </div>
    </div>
</div>
</template>

<style scoped src="./search-table.css"></style>

<script src="./search-table.js"></script>
