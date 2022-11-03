<template>
    <div class="dropdown">
        <b-dropdown id="dropdown-left" text="Left align" variant="primary" class="m-2">
        </b-dropdown>
    </div>
</template>

<style scoped>
    .dropdown {
        position: relative
    }
</style>

<script>
import Vue from 'vue'
import Component from 'vue-class-component'

/**
 * Class representing Table component
 * @extends Vue
 */
@Component({})
export default class Dropdow extends Vue {
}
</script>
