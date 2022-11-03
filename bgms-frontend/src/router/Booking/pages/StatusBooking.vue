<template>
<div class="search-status px-8">
    <status-event-fields />
    <status-tabs />
</div>
</template>

<script>
import StatusEventFields from "../containers/status-event-fields";
import statusTabs from "../containers/status-tabs";

export default {
    components: {
        StatusEventFields,
        statusTabs,
    },
};

</script>
