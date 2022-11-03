<template>
    <div class="vertical-menu">
        <router-link to="/"
            @click.native="resetReport">
            <i class="glyphicon glyphicon-th-list"></i>
        </router-link>
        <router-link to="/report">
            <i class="glyphicon glyphicon-signal"></i>
        </router-link>
        <!-- It is commented for now, while the dashboard definition is done.
            <a>
            <i class="glyphicon glyphicon-save-file"></i>
            </a>
        -->
    </div>
</template>

<style src="./VerticalMenu.css"></style>
<script lang="ts" src="./VerticalMenu.ts"></script>
