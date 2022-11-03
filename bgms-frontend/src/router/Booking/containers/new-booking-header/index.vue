<template>
<div class="new-booking-header">
    <!-- -->
    <!-- <confirm-modal
        title="Confirmation needed"
        message="Are you sure you want to clear all fields?"
        :show="showConfirmModal"
        @close="showConfirmModal = false"
        @reset="onRemoveEvent"
    /> -->

    <confirm-modal
        title="Confirmation needed"
        message="Are you sure you want to update this event?"
        :show="showEditConfirm"
        @close="showEditConfirm = false"
        @reset="() => { 
            onSaveEvent();
            showEditConfirm = false;
        }"
    />

     <site-select-modal
        title="Confirmation needed"
        message="Are you sure you wish to change site?"
        :show="showSiteSelectConfirm"
    />

    <div class="operation-buttons">
        <!-- View mode -->
        <span @click="changeEditMode" v-if="!editMode">
            <i class="far fa-edit"></i>
        </span>
        <span @click="changeViewMode" v-if="!editMode && redirect">
            <!--<i class="fa fa-times"></i>-->
        </span>

        <!-- Edit mode -->
        <span

            @click="updateEvent ? openEditConfirm() : onSaveEvent()"
            v-if="editMode"
        >
            <i class="far fa-save"></i>
        </span>
        <span @click="changeViewMode" v-if="editMode">
            <i class="fa fa-times"></i>
        </span>
    </div>

    <!-- -->
    <div class="booking-name-wrapper">
        <h3 class="site-name">{{ currentSiteName }}</h3>
    </div>

    <!-- -->
    <div class="booking-references-fields flex items-center">
        <div class="flex mr-4">
            <span>Reference: </span>
            <div class="w-32 ml-2">
                <input-field
                    v-model="reference_number"
                    :disabled="true"
                    :highlight="true"
                />
            </div>
        </div>

        <div class="flex">
            <span>Date: </span>
            <div class="w-32 ml-2">
                <input-field
                    v-model="bookingDate"
                    :disabled="true"
                    :highlight="true"
                />
            </div>
        </div>
    </div>

</div>
</template>

<style scoped src="./new-booking-header.css"></style>

<script src="./new-booking-header.js"></script>