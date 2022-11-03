<template>
<div class="search-event px-8">
    <search-form></search-form>
    <search-table></search-table>
    <search-pagination></search-pagination>
</div>
</template>

<script>
import SearchForm from "../containers/search-form";
import SearchTable from "../containers/search-table";
import SearchPagination from "../containers/search-pagination";

export default {
    components: {
        SearchForm,
        SearchTable,
        SearchPagination
    },
};

</script>
