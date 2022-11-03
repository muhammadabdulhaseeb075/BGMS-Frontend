import { mapActions, mapGetters, mapMutations } from "vuex";
import PageInformation from "../../../../components/page-information/index";
import Pagination from "../../../../components/pagination/index";

const INITIAL_ROW_NUMBER = 0;

function data() {
    return {
        currentPage: 0,
        itemsPerPage: 10
    };
}

const components = {
    PageInformation,
    Pagination
};

function calculateOffset(page, itemsperpage) {
    return (page - 1) * itemsperpage;
}

const watch = {
    totalRows: {
        handler: function (newTotalRows) {
            if(newTotalRows > 0) {
                this.currentPage = 1;
            } else {
                this.currentPage = INITIAL_ROW_NUMBER;
            }
        },
        deep: true
    },
};

const computed = {
    ...mapGetters("booking",["searchResultEvent", "totalRows", "searchEventCriteria"]),
    pages: function () {
        if( this.totalRows ){
            return Math.ceil(this.totalRows / this.itemsPerPage);   
        } else {
            return 0;
        }
    },
    lastPageItem: function (){
        if ( this.totalRows ) {
            return Math.min(this.currentPage * this.itemsPerPage, this.totalRows);
        } else {
            return INITIAL_ROW_NUMBER;
        }
    },
    initialPageItem: function (){
        return Math.max(calculateOffset(this.currentPage, this.itemsPerPage) + 1, INITIAL_ROW_NUMBER);
    }
};

const methods = {
    ...mapActions("booking", ["searchForEvents"]),
    onChangePage: function (page) {
        this.currentPage = page;
        const offset = calculateOffset(page, this.itemsPerPage);
        const limit = this.itemsPerPage;
        const searchPaginationArguments = {
            offset,
            limit
        };
        const searchEventsArguments = {
            filtersCriteria: this.searchEventCriteria,
            searchPaginationArguments
        };
        this.searchForEvents(searchEventsArguments);
    }
};

function mounted(){
    if ( this.searchResultEvent.length > 0 ) {
        this.currentPage = 1;
    }
}

export default {
    name: "search-pagination",
    components,
    mounted,
    data,
    computed,
    methods,
    watch
};
