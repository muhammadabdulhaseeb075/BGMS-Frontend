<template>
<div id="booking-add-event-page">
    <new-event-form></new-event-form>
</div>
</template>

<style scoped>
@import "styles/theme.css";

#booking-add-event-page {
    @apply px-6;
}
</style>

<script>
import NewEventForm from "../containers/new-event-form";

const components = {
    NewEventForm,
};

export default {
    name: "add-event",
    components, 
};
</script>
