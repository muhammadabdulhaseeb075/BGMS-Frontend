<template>
<router-view></router-view>
</template>

<script>

import bookingStore from "../module";

export default {
    name: "booking-index",
    created() {
        this.$store.registerModule("booking", bookingStore);
    },
};

</script>
