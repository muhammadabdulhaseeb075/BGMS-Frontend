<template>
    <div class="report-list">
        <v-card
            class="mx-auto"
            max-width="600"
            tile>
            <v-list>
                <v-subheader>REPORTS</v-subheader>
                <div>
                    <v-menu>
                        <template v-slot:activator="{ on }">
                            <v-btn
                            dark
                            v-on="on"
                            color="rgb(195, 175, 66)"
                            >
                            templates
                            </v-btn>
                        </template>
                        <v-list v-if="templates.length > 0">
                            <v-list-item
                            v-for="(item, index) in templates"
                            :key="index"
                            @click="selectTemplate(item)"
                            >
                            <v-list-item-title>{{ item.name }}</v-list-item-title>
                            </v-list-item>
                        </v-list>
                    </v-menu>
                </div>
                <v-list-item-group color="primary">
                    <v-list-item
                        v-for="(report, index) in reports"
                        :key="index">
                        <v-list-item-content @click="selectReport(report)">
                            <v-list-item-title v-html="report.name" />
                            <v-list-item-subtitle v-html="report.creation_date" />
                        </v-list-item-content>
                        <div v-if="isSuperuser" @click="saveAsTemplate(report)">
                            <button>save as template</button>
                        </div>
                    </v-list-item>
                </v-list-item-group>
            </v-list>
        </v-card>
    </div>
</template>

<style>
    .report-list {
        position: relative
    }
</style>

<script lang="ts">
import Vue from 'vue'
import Component from 'vue-class-component'

/**
 * @extends Vue
 */
@Component({})
class ReportList extends Vue {

    superuser: string = 'False';

    templates: any[] = [];

    get reports() {
        return this.$store.state.reportList;
    }

    get isSuperuser() {
        return this.superuser === 'True';
    }

    selectReport(report) {
        this.$store.dispatch('setReport', report);
        this.$router.push({name: 'Report'});
    }

    selectTemplate(template) {
        const payload = {
            name: template.name,
            tableSchema: template.table_schema
        }

        this.$store.dispatch('createReport', { payload })
        .then(() => this.$store.dispatch('getAllReports'))
        .then(({ headers }: any) => {
            this.superuser = headers.is_superuser;
        }).catch(error => {
            console.error('Couldnt create report based on template');
        });
    }

    saveAsTemplate(report) {
        const payload = {
            name: report.name,
            tableSchema: report.table_schema
        }
        this.$store.dispatch('saveReportTemplate', payload)
        .then((response: any) => this.$store.dispatch('getReportTemplates'))
        .then((response: any) => {
            this.templates = response.data;
        });
        
    }

    mounted() {
        this.$store.dispatch('getAllReports')
        .then(({ headers }: any) => {
            this.superuser = headers.is_superuser;
        });

        this.$store.dispatch('getReportTemplates')
        .then((response: any) => {
            this.templates = response.data;
        })
        .catch((error) => {
            console.error('Couldnt load report templates: ', error);
        });

    }
}

export default ReportList;
</script>
