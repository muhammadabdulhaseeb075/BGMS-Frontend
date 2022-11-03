<template>
<div class="search-form">
    <!-- -->
    <div class="search-field">
        
        <div class="flex">
            <!-- -->
            <!--
            <div class="w-1/5">
            <form-section-field class="" label="Reference:">
                <input-field
                    v-bind="searchForm.fields.reference_number"
                    v-model="searchForm.fields.reference_number.value"
                    :form-data="searchForm.data"
                />
            </form-section-field>
            </div>
            -->
            <!-- -->
            <div class="w-1/3">
            <form-section-field label="Deceased:">
                <div>
                    <input-field
                        v-bind="searchForm.fields.deceasedFirstName"
                        v-model="searchForm.fields.deceasedFirstName.value"
                        :form-data="searchForm.data"
                    />
                </div>
                <div class="ml-5">
                    <input-field
                        v-bind="searchForm.fields.deceasedLastName"
                        v-model="searchForm.fields.deceasedLastName.value"
                        @format="searchForm.fields.deceasedLastName.format"
                        :form-data="searchForm.data"
                        
                    />
                </div>
            </form-section-field>
            </div>

            <!-- -->
            <div class="w-1/3">
            <form-section-field label="Date(from):" option-classes="w-1/2">
                <div class="w-full">
                <input-field
                    v-bind="searchForm.fields.dateFrom"
                    v-model="searchForm.fields.dateFrom.value"
                    :form-data="searchForm.data"
                />
                </div>
            </form-section-field>
            </div>

            <!-- -->
            <div class="w-1/3">
            <form-section-field label="Date(to):" option-classes="w-1/2">
                <div class="w-full">
                <input-field
                    v-bind="searchForm.fields.dateTo"
                    v-model="searchForm.fields.dateTo.value"
                    :form-data="searchForm.data"
                />
                </div>
            </form-section-field>
            </div>

        </div>

        <div class="flex mt-3">
            <!-- -->
            <form-section-field class="" label="Site:">
                <input-field
                    v-bind="searchForm.fields.site"
                    v-model="searchForm.fields.site.value"
                    :form-data="searchForm.data"
                    :options="siteOptions"
                />
            </form-section-field>

            <!-- -->
            <form-section-field class="" label="Funeral Director:">
                <input-field
                    v-bind="searchForm.fields.funeralDirector"
                    v-model="searchForm.fields.funeralDirector.value"
                    :form-data="searchForm.data"
                    :options="funeralDirectorOptions"
                />
            </form-section-field>

            <!-- -->
            <form-section-field class="" label="Type:">
                <input-field
                    v-bind="searchForm.fields.type"
                    v-model="searchForm.fields.type.value"
                    :form-data="searchForm.data"
                />
            </form-section-field>

            <!-- -->
            <form-section-field class="" label="Status:">
                <input-field
                    v-bind="searchForm.fields.status"
                    v-model="searchForm.fields.status.value"
                    :form-data="searchForm.data"
                />
            </form-section-field>
        </div>

    </div>

    <!-- -->
    <div class="search-buttons flex justify-end text-3xl mt-7">
        <div class="cursor-pointer mr-5">
            <i class="icon-Clear-02-Filled" @click="onCleanForm"></i>
        </div>
        <div class="cursor-pointer mr-5">
            <i class="fas fa-search" @click="onSearchEvents"></i>
        </div>
    </div>
</div>
</template>

<style scoped src="./search-form.css"></style>

<script src="./search-form.js"></script>
