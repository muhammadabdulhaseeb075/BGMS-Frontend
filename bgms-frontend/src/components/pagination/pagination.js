const ON_CHANGE_PAGE_EMIT = "change-page";

function data(){
    return {
        pagesOptions: 0,
        adjacents: 2,
        padding: 2,
        headPages: [],
        bodyPages: [],
        tailPages: [],
        leftEllipsisButtonActive: false,
        rightEllipsisButtonActive: false
    }
}
const props = {
    pages: {type: Number, default: 0},
    currentPage: {type: Number, default: 1},
}


function createPagesFromRange(start, end , offsetStart = 0) {
    if(end - start < 1) {
        return [];
    } else {
        return Array(end - start).fill().map((_, index) => (start + offsetStart) + index);

    }
}


const watch ={
    pages: {
        handler: function (newPages) {
            const padding = this.padding;
            const currentPage = this.currentPage;
            const adjacents = this.adjacents;
            this.updatePageOptions({ pages: newPages, padding , currentPage, adjacents });
        },
        deep: true
    },
    currentPage: {
        handler: function (newCurrentPage) {
            const padding = this.padding;
            const adjacents = this.adjacents;
            const pages = this.pages;
            this.updatePageOptions({ pages, padding, currentPage: newCurrentPage, adjacents });
        },
        deep: true
    }
}

const methods = {
    updatePageOptions: function({ pages, padding, currentPage, adjacents }) {
        const allPages = Array(pages).fill().map((_,index) => index + 1);
        const bodyPagesOptions = allPages.map((_, index) =>  Math.max(1, currentPage - adjacents) + index);
        const headPagesCalculation = Math.min(1 + padding, currentPage - adjacents );

        const headPages = createPagesFromRange(1, headPagesCalculation);
        const bodyPages = bodyPagesOptions.filter(currentBodyPage => currentBodyPage <= Math.min(pages, currentPage + adjacents));
        const tailPages = allPages.filter((currentTailPage) => currentTailPage > Math.max(pages - padding, currentPage + adjacents))

        this.headPages = headPages;
        this.bodyPages = bodyPages;
        this.tailPages = tailPages;
        this.leftEllipsisButtonActive = currentPage - adjacents > 1 + padding;
        this.rightEllipsisButtonActive = currentPage + adjacents < pages - padding;
    },
    changePage: function (mouseEvent, page) {
        mouseEvent.preventDefault();
        this.$emit(ON_CHANGE_PAGE_EMIT, page);
        /*
             use this to test the pagination in isolation, the current method allows to update the page within the component.
        this.currentPage = page;
        this.updatePageOptions({
            pages: this.pages, padding: this.padding, currentPage: this.currentPage, adjacents: this.adjacents
        }) */
    },
    nextPage: function (mouseEvent) {
        mouseEvent.preventDefault();
        const nextPage = this.currentPage + 1;
        const maxPage = Math.min(this.pages, nextPage);
        if (maxPage !== this.currentPage) {
            this.changePage(mouseEvent, maxPage);
        }
    },
    previousPage: function (mouseEvent) {
        mouseEvent.preventDefault();
        const previousPage = this.currentPage - 1;
        const minPage = Math.max(1, previousPage);
        if (minPage !== this.currentPage) {
            this.changePage(mouseEvent, minPage);
        }
    }
}

export default {
    name: "pagination",
    data,
    props,
    methods,
    watch
};
