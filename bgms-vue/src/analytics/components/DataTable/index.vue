<template>
    <div class="report-table">
        <div class="save-form">
            <v-row no-gutters>
                <v-col
                cols="12"
                sm="4"
                >
                    <v-text-field
                    v-model="reportName"
                    label="Report name"
                    />
                </v-col>
                <v-col
                cols="12"
                sm="4"
                >
                    <v-btn
                    class="btn-create-and-save"
                    :disabled="selectedModelName === '' || reportName === ''"
                    color="rgb(195, 175, 66)"
                    @click="submitReportTable">
                        <span v-if="loaded || created">Save</span>
                        <span v-else>Create Report</span>
                    </v-btn>
                    <v-btn
                    class="btn-export"
                    :href="reportUrlExport"
                    v-if="loaded || created"
                    color="rgb(41, 43, 51)"
                    dark
                    target="_blank">
                        <span>Export report</span>
                    </v-btn>
                </v-col>
            </v-row>
            
            
        </div>
        <div>
            <add-to-table-btn :models="modelsList" @select-field="addingRow"/>
            <v-text-field
            v-model="pagination.limit"
            type="number"
            label="Entries limit"
            filled
            @change="changeLimit"/>
        </div>
        <div>
            <v-data-table
            :headers="headers"
            :items="recordItems"
            :disable-pagination="true"
            :must-sort="false"
            :disable-sort="true"
            hide-default-footer
            class="elevation-1">

                <template v-slot:top>
                    <v-toolbar v-if="reportHasData" flat color="white">
                        <v-toolbar-title>
                            {{selectedModelName}}
                        </v-toolbar-title>
                    </v-toolbar>
                </template>

                <template
                    v-for="(header, index) in headers"
                    :slot="'header.' + header.value">
                    <header-filter
                    :key="index"
                    :data="header"
                    :model-name="selectedModelName"
                    @trigger-filter="addFilterField"/>
                </template>
                
            </v-data-table>
        </div>
        <div class="text-center">
            <v-pagination
            v-model="pagination.currentPage"
            :total-visible="5"
            :length="pagination.total"
            @input="changePage"
            ></v-pagination>
            <div v-if="reportHasData">
                <i class="table-header-title">
                    Total Records: {{pagination.perPage}}
                </i>
            </div>
        </div>
    </div>
</template>

<style>
.report-table .b-dropdown {
    width: 100%;
}

.report-table .v-data-table__wrapper {
    overflow: inherit !important;
}

.report-table .b-dropdown .btn-secondary {
    width: 100%;
}

.report-table .model-field {
    text-align: left;
}

.report-table .model-name {
    color: #0157a2;
    margin: 0;
    text-align: center;
}

.report-table .info {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 10px;
}

.report-table .info i {
    font-size: 18px;
    padding-left: 30px;
    display: inline-block;
}

.report-table .save-form {
    margin-bottom: 10px;
}

.report-table .table-bordered,
.report-table .table-bordered > thead > tr > th,
.report-table .table-bordered > tbody > tr > td,
.report-table .table-bordered > tfoot > tr > td {
    border: 1px solid #dbdbdb;
}

.report-table .table-bordered > thead > tr > th {
    border-bottom-width: 2px;
}

.report-table .table-header-title {
    font-size: 12px;
}

</style>

<script lang='ts' src="./DataTable.ts"></script>
