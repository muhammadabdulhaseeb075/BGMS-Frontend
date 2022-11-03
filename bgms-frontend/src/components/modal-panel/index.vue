<template>
<teleport to="#modals-teleport" disabled>
    <div class="modal-panel" v-if="show">
        <div class="modal-content">
            <slot></slot>
        </div>
    </div>
</teleport>
</template>

<style scoped src="./modal-panel.css"></style>

<script src="./modal-panel.js"></script>
