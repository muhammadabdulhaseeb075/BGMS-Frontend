<template>
<div class="status-form">
    <!-- -->
    <div class="status-field">         
        <div class="flex">

            <!-- -->
            <div class="w-1/5">
            <form-section-field class="" label="Reference:">
                <input-field
                    type="number"
                    v-model="reference_number"
                    :disabled="true"
                />
            </form-section-field>
            </div>

            <!-- -->
            <div class="w-1/3">
            <form-section-field label="Deceased:">
                <div>
                    <input-field
                        v-model="firstname"
                        :disabled="true"
                    />
                </div>
                <div class="ml-5">
                    <input-field
                        v-model="lastname"
                        :disabled="true"
                    />
                </div>
            </form-section-field>
            </div>


        </div>


    </div>

</div>
</template>

<style scoped src="./status-event-fields.css"></style>

<script src="./status-event-fields.js"></script>
