<template>
<div class="form-modal-content">
    <div class="fields flex justify-between mb-2">
        <label class="mr-3">
            Postcode:
        </label>
        <div>
            <input-field
                v-model="postcodeValue"
                :placeholder="'Postcode'"
                @change="insertPostcode"
            />
        </div>
    </div>
    <div class="postcode-options">
        <input-field
            v-model="form.fields.deceasedAddressLine1.value"
            :name="form.fields.deceasedAddressLine1.name"
            :type="'select'"
            :placeholder="addressPlaceholder"
            :options="addressOptions"
            :form-data="form.data"
            @change="selectAddress"
        />
    </div>
    <footer class="mt-2">
        <fill-button @click="onAdd">Confirm</fill-button>
    </footer>
</div>
</template>

<script src="./postcode-form.js"></script>
