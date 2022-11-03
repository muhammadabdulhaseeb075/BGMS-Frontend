<template>
<div class="form-modal-content">
    <div class="fields flex mt-2" v-for="field in form.fields" :key="field.id">
        <label v-if='field.placeholder' class="w-1/3">        
            {{ field.placeholder }}:             
        </label>
        <label v-else class="w-1/3">        
            &nbsp;            
        </label>
        <div class="w-2/3">
            <input-field
                v-bind="field"
                v-model="field.value"
                :form-data="form.data"
                @format="field.format"
            />
        </div>
    </div>
    <footer class="mt-2">              
        <div class="flow-root ">            
            <fill-button v-if="$attrs['data_id']" class="float-left" @click="onSubmitForm">Update</fill-button>
            <fill-button v-else class="float-left" @click="onSubmitForm">Add</fill-button>
            <fill-button class="float-right" @click="onClose">Cancel</fill-button>
        </div>
    </footer>
</div>
</template>

<script src="./funeral-director-form.js"></script>
