import { mapActions, mapGetters, mapMutations } from "vuex";
import PageInformation from "../../../../components/page-information/index";
import Pagination from "../../../../components/pagination/index";

const INITIAL_ROW_NUMBER = 0;

function data() {
    return {
        currentPage: 0,
        itemsPerPage: 2,
        debug: false,
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
            //debugger; // eslint-disable-line no-debugger 
            if(newTotalRows > 0) {
                const limit = this.itemsPerPage;
                var page = Math.floor(newTotalRows/limit);
                const remainder = newTotalRows%limit;
                if(remainder > 0){
                    page += 1;
                }
                //const slideIndex = ((page - 1)*limit); //go to first slide in page 
                if(this.debug) console.log("NewPage: " + page);
                //this.$parent.goToSlideIndex(slideIndex);              
                //this.onChangePage(page);
            } else {
                this.currentPage = INITIAL_ROW_NUMBER;
            }
        },
        deep: true
    },
};

const computed = {
    //...mapGetters("booking"),
    pages: function () {
        if(this.$parent.slideCount){
            return Math.ceil(this.$parent.slideCount / this.itemsPerPage);   
        } else {
            return 0;
        }
    },
    lastPageItem: function (){
        if ( this.$parent.slideCount ) {
            return Math.min(this.currentPage * this.itemsPerPage, this.$parent.slideCount);
        } else {
            return INITIAL_ROW_NUMBER;
        }
    },
    initialPageItem: function (){
        return Math.max(calculateOffset(this.currentPage, this.itemsPerPage) + 1, INITIAL_ROW_NUMBER);
    },
    totalRows: function(){
        return this.$parent.slideCount;
    },
};

const methods = {
    //...mapActions("booking"),
    onChangePage: function (page) {
        //debugger; // eslint-disable-line no-debugger 
        this.currentPage = page;
        //const offset = calculateOffset(page, this.itemsPerPage);
        const limit = this.itemsPerPage;
        const slideIndex = ((page - 1)*limit); //go to first slide in page         
        if(this.debug) console.log("SlideINDEX: " + slideIndex);
        this.$parent.goToSlideIndex(slideIndex);
    }
};

function mounted(){
    if(this.debug) console.log("Mounting CalendarPagination");
    if(this.debug) console.log("CPslideCount:" + this.$parent.slideCount);
    if ( this.$parent.slideCount > 0 ) {
        this.currentPage = 1;
    }
}

export default {
    name: "calendar-pagination",
    components,
    mounted,
    data,
    computed,
    methods,
    watch
};
