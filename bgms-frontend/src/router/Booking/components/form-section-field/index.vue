<template>
<div class="form-field">
    <div class="field-label">{{ label }}</div>
    <div class="option-group" :class="optionClasses">
        <slot></slot>
    </div>
</div>
</template>

<style scoped src="./form-section-field.css"></style>

<script src="./form-section-field.js"></script>
