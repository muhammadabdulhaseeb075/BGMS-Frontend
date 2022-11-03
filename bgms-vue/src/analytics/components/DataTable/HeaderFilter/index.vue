<template>
    <div class="header-filter">
        <div
        class="header-name"
        @click="toggleFilter">
            <div>
                <span>{{data.text}}</span>
                <span v-if="isValidToFilter"><v-icon>mdi-chevron-down</v-icon></span>
            </div>
            <div v-if="data.props.type">
                ({{data.props.type}})
            </div>
        </div>
        <div v-if="isValidToFilter && showFilter" class="float-filter">
            <div class="filter-input">
                <v-text-field
                v-model="filterInput"
                label="Filter"
                @keydown.enter="selectInputFilter"
                @click:append-outer="selectInputFilter"
                :append-outer-icon="getIconType()"/>
            </div>
            <div>
                {{data.props.type}}
            </div>
            <div>
                <span v-if="!suggestionNotLoaded">loading suggestions...</span>
                <div v-else>
                    <div
                    v-for="(suggestion, itr) in suggestions"
                    :key="itr"
                    @click="selectSuggestionFilter(suggestion)">
                        {{suggestion}}
                    </div>
                </div>
            </div>
        </div>
    </div>    
</template>

<style>

.header-filter {
    cursor: pointer;
    position: relative;
}

.header-filter .float-filter {
    background-color: white;
    border: 1px solid rgba(0,0,0,0.3);
    border-radius: 5px;
    position: absolute;
    min-width: 160px;
    width: 100%;
    z-index: 1;
    padding: 7px;
}

.header-filter .header-name .float-filter .filter-input {
    border-bottom: 1px solid rgba(0,0,0,.54);
    padding-bottom: 5px;
}

</style>

<script lang="ts">
import Vue from "vue";
import Component from "vue-class-component";

type Header = {
    props: {type: string}
};

/**
 * Class representing Table component
 * @extends Vue
 */
@Component({
    props: {
        data: Object,
        modelName: String
    }
})
export default class HeaderFilter extends Vue {
    showFilter = false;
    suggestions = [];

    filterInput = '';

    get isValidToFilter(): boolean {
        const headerData = this.$props.data;

        return headerData.text !== 'id';
    }

    get suggestionNotLoaded(): boolean {
        return !!this.suggestions.length;
    }

    selectInputFilter(): void {
        const headerData = this.$props.data;
        this.$emit('trigger-filter', this.filterInput, headerData);
    }

    selectSuggestionFilter(suggestion): void {
        const headerData = this.$props.data;
        this.filterInput = suggestion;
        this.$emit('trigger-filter', suggestion, headerData);
    }

    toggleFilter(): void {
        this.showFilter = !this.showFilter;
        const { modelName, data } = this.$props;

        if(this.showFilter) {
            this.$store.dispatch(
                'filterSuggestions',
                {modelName, field: data.value}
            )
            .then(response => {
                this.suggestions = response.data;
            });
        }
    }

    getIconType(): string {
        const header = this.$props.data;
        let vIcon = 'mdi-magnify';

        switch(header.props.type) {
            case 'CharField':
            case 'TextField':
                break;
            case 'DateField':
            case 'DateTimeField':
                break;
            case 'IntegerField':
                break;
            case 'BooleanField':
            case 'NullBooleanField':
                break;
            default:
                break;
        }

        return vIcon;
    }
}
</script>
