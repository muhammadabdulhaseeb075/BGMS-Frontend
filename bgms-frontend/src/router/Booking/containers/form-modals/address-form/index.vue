<template>
<div class="form-modal-content">
    <div
        class="fields flex justify-between mb-2"
        v-for="field in form.fields"
        :key="field.id"
    >
        <label class="mr-3" v-if="field.type">
            {{ field.placeholder }}:     
        </label>
        <div v-if="field.type">
            <input-field
                v-bind="field"
                v-model="field.value"
                :form-data="form.data"
            />
        </div>
    </div>
    <footer class="mt-2">
        <fill-button @click="onAdd">Add</fill-button>
    </footer>
</div>
</template>

<script src="./address-form.js"></script>
