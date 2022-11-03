import axios from 'axios';
import Vue from 'vue'
import Component from 'vue-class-component';
import XLSX from 'xlsx';
import AddToTableBtn from './AddToTableBtn/index.vue';
import HoverCol from './HoverCol/index.vue';
import HeaderFilter from './HeaderFilter/index.vue';

enum ModelRelation {
    ONE_TO_ONE = 'OneToOneField',
    MANY_TO_ONE = 'ForeignKey',
    MANY_TO_MANY = 'ManyToManyField'
}

function withRelation(type): boolean {
    return (
        type === ModelRelation.MANY_TO_ONE ||
        type === ModelRelation.MANY_TO_MANY ||
        type === ModelRelation.ONE_TO_ONE
    );
}

function filterFieldsByModel(
    modelFields
) {
    return modelFields.filter(({type}) => {
        return !withRelation(type);
    });
}


/**
 * Class representing Table component
 * @extends Vue
 */
@Component({ components: {
    AddToTableBtn,
    HeaderFilter,
    HoverCol
}})
export default class Table extends Vue {
    // When the report has just been created
    created: boolean = false;
    // When it's a loaded report
    loaded: boolean = false;
    // table schema
    headers = [];
    filters = {};

    reportName: string = '';
    selectedModelName: string = '';

    pagination = {
        currentPage: 1,
        perPage: 0,
        total: 0,
        limit: 10
    };

    records: number = 0;

    get modelsList(): object {
        const { $store, selectedModelName } = this;
        const { reportModels } = $store.state; 
        let models = {};

        if (selectedModelName) {
            const filteredModels = this.filterModelsByRelation();
            for(let itr = 0; itr < filteredModels.length; itr++) {
                const fmodelName = filteredModels[itr];
                models[fmodelName] = reportModels[fmodelName]; 
            }
        } else {
            models = Object.assign({}, reportModels);
        }

        for(let modelName in models) {
            const records = models[modelName].records;
            models[modelName] = {
                fields: filterFieldsByModel(
                    models[modelName].fields 
                ),
                records
            };
        }

        return models;
    }

    get recordItems(): object {
        const {reportData} = this.$store.state;
        let items = [];

        if(reportData) {
            items = reportData.map((itemData) => {
                const keys = Object.keys(itemData);
                let item = {};
                
                for(let itr = 0; itr < keys.length; itr++) {
                    const key = keys[itr];
                    const value = itemData[key];
                    item[key] = value !== null ? value : 'null';
                }

                return item;
            });
        }

        return items; 
    }

    get reportHasData(): boolean {
        const modelHasBeenSelected = !!this.selectedModelName;
        const isThereData = !!this.$store.state.reportData;
        
        return modelHasBeenSelected && isThereData;
    }

    get reportUrlExport(): string {
        const selectedReport = this.$store.state.selectedReport;
        return selectedReport
        ? `/analytics/export-reports/${selectedReport.id}/`
        : '';
    }

    addingRow({field, type}, modelName): void {
        let fieldName = field;

        if(this.selectedModelName === '') {
            this.selectedModelName = modelName;
        }

        if(
            this.selectedModelName !== '' &&
            modelName !== this.selectedModelName
        ) {
            const fieldRelated = this.getFieldForRelatedModel(modelName);
            fieldName = `${fieldRelated.field}__${field}`;
        }

        if(!this.headers.length) {
            this.addHeader('id');
        }        
        this.addHeader(fieldName, type);


        const options = this.getOptions();
        this.$store.dispatch('getModelEntries', {
            name: this.selectedModelName,
            options
        }).then(({headers}) => {
            this.pagination.currentPage = 1;
            this.pagination.perPage = Number(headers.total_records);
            this.pagination.total = Number(headers.pagination_num_pages);
        });

    }
    
    changePage(page: number): void {
        const name = this.selectedModelName;
        const options = this.getOptions();
        this.$store.dispatch('getModelEntries', {
            name,
            options
        });
    }

    addFilterField(value, headerData): void {
        if(value) {
            this.filters[headerData.value] = value;
        } else if(value === '') {
            // remove the filter field if the input filter is empty again
            this.filters[headerData.value] = undefined;
        }

        const name = this.selectedModelName;
        const options = this.getOptions();
        this.$store.dispatch('getModelEntries', {
            name,
            options
        }).then(({ headers }) => {
            this.pagination.currentPage = 1;
            this.pagination.perPage = Number(headers.total_records);
            this.pagination.total = Number(headers.pagination_num_pages);
        });
    }
    
    changeLimit(value: string): void {
        if(this.headers.length) {
            this.pagination.currentPage = 1;
            const name = this.selectedModelName;
            const options = this.getOptions();

            this.$store.dispatch('getModelEntries', {
                name,
                options
            }).then(({ headers, data }) => {
                this.pagination.perPage = Number(headers.total_records);
                this.pagination.total = Number(headers.pagination_num_pages);
            }); 
        }
    }

    addHeader(headerKey: string, type?: string, ): void {
        this.headers.push({
            text: headerKey,
            value: headerKey,
            props: {
                type
            }
        });
    }

    getOptions(): object {
        const fields = this.getQueriesByFields();
        const { limit, currentPage } = this.pagination; 
        const options: any = {
            fields,
            limit,
            page: currentPage
        };

        if(Object.keys(this.filters).length) {
            options.filters = this.filters;
        }

        return options;
    }

    getQueriesByFields(): string {
        const keys = this.headers
            .map((head) => head.value)
            // removing id as a query 
            .filter((key: string) => key !== 'id');
        const remainFields = keys.join(',');
        const fieldsList = remainFields;

        return fieldsList;
    }

    getFieldForRelatedModel(relatedModel) {
        const { reportModels } = this.$store.state;
        const selectedModel = reportModels[this.selectedModelName];
        const foundField = selectedModel.fields.find((field) =>
            relatedModel === field.related_model
        );

        return foundField;
    }

    filterModelsByRelation() {
        const {selectedModelName, $store} = this;
        const reportModels = $store.state.reportModels;
        const selectedModelFields = reportModels[selectedModelName].fields;
        const models = [selectedModelName];

        for(let itr = 0; itr < selectedModelFields.length; itr++) {
            const field = selectedModelFields[itr];
            if(withRelation(field.type)) {
                const relatedModelName = field.related_model;
                if(reportModels[relatedModelName]) {
                    models.push(relatedModelName);
                }
            }
        }

        return models;
    }

    getTableSchema() {
        const headers = this.headers
            .filter(header => header.value !== 'id')
            .map(header => header.value);
        const selectedModelName = this.selectedModelName;
        const filters = this.filters;

        return {
            headers,
            selectedModelName,
            filters
        };
    }

    submitReportTable(): void {
        if(this.loaded || this.created) {
            const {state, dispatch} = this.$store;
            const {selectedReport} = state;
            dispatch('updateReport', {
                id: selectedReport.id,
                payload: {
                    name: this.reportName,
                    tableSchema: this.getTableSchema()
                }
            });
        } else {
            this.$store.dispatch('createReport', {
                payload: {
                    name: this.reportName,
                    tableSchema: this.getTableSchema()
                }
            }).then(() => {
                this.created = true;
            });
        }
    }

    loadingReport(): void {
        const { selectedReport } = this.$store.state;
        const { name, table_schema } = selectedReport;
        this.reportName = name;
        this.selectedModelName = table_schema.selectedModelName;
        this.addHeader('id');
        table_schema.headers.forEach((headerKey: string) => {
            this.addHeader(headerKey);
        });

        const modelName = this.selectedModelName;
        const options = this.getOptions();

        this.$store.dispatch('getModelEntries', {
            name: modelName,
            options
        }).then(({ headers, data }) => {
            this.loaded = true;
            this.pagination.perPage = Number(headers.total_records);
            this.pagination.total = Number(headers.pagination_num_pages);
        }); 

    }

    exportReport(): void {
        const reportId = this.$store.state.selectedReport.id;
        this.$store.dispatch('exportReport', reportId)
        .then((response: any) => console.log(response))
        .catch((error) => console.error("Exporting error: ", error));
    }

    mounted() {
        this.$store.dispatch('getAllModels')
        .then(() => {
            if (this.$store.state.selectedReport) {
                this.loadingReport();
            }
        });
    }
}
