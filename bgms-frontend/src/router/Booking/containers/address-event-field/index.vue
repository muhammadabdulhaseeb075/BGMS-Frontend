<template>
<div class="address-event-field flex">
    <div class="flex" v-if="!this.editMode">
        <fill-button @click="onFindAddress">
            <div class="mx-5">Find Address</div>
        </fill-button>
        <span
            class="manual-address underline ml-3 cursor-pointer"
            @click="onManualAddress"
        >
            or enter address manually
        </span>
    </div>

    <div v-else>
        <i class="fa fa-trash cursor-pointer" @click="onEdit" />
        <!--<i class="fa fa-edit cursor-pointer" @click="onEdit" />-->
    </div>

    <modal-panel :show="openModal">
        <div class="form-modals">
            <div class="modal-header flex justify-between px-3 py-2">
                <div class="title">{{ modalTitle }}</div>
                <div class="close-button cursor-pointer" @click="onClose">
                    <i class="fa fa-times p-1"></i>
                </div>
            </div>
            <div class="modal-body p-7">
                <!-- -->
                <div v-if="addressType === 'manual'">
                    <div
                        class="fields flex justify-between mb-2"
                        v-for="field in addressForm.fields"
                        :key="field.id"
                    >
                        <label class="mr-3">
                            {{ field.placeholder }}:     
                        </label>
                        <div>
                            <input-field
                                v-bind="field"
                                v-model="field.value"
                                :form-data="addressForm.data"
                            />
                        </div>
                    </div>
                </div>

                <!-- -->
                <div v-if="addressType === 'postcode'">
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
                            v-model="addressSelected"
                            :name="'address'"
                            :type="'select'"
                            :placeholder="addressPlaceholder"
                            :options="addressOptions"
                            @change="selectPostcodeAddress"
                        />
                    </div>
                </div>

                <footer class="mt-2">
                    <fill-button @click="onConfirm">Confirm</fill-button>
                </footer>
            </div>
        </div>
    </modal-panel>
</div>
<notifications-list/>
</template>


<script src="./address-event-field.js"></script>

<style src="./address-event-field.css"></style>
