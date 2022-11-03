<template>
    <div
    class="hover-col">
        <div class="hover-col-content">
            <slot></slot>
        </div>

        <v-list class="menu-options">
            <v-list-item class="option">
                <v-list-item-content>
                    field
                </v-list-item-content>
            </v-list-item>
        </v-list>

        <!-- <div class="hover-col-content">
            <slot></slot>
        </div>
        <b-list-group class="menu-options">
            <b-list-group-item
            class="option"
            v-for="(f, index) in model.fields"
            :key="index"
            @click="clickOnItem(f)">
                {{f.field}}
            </b-list-group-item>
        </b-list-group> -->
    </div>
</template>

<style scoped>
.hover-col {
    width: 100%;
    position: relative;
}

.hover-col .hover-col-content {
    /* width: 100%;
    text-align: center;
    color: #0157a2;
    font-weight: bold; */
}

.hover-col .menu-options {
    /* display: none; */
    position: absolute;
    padding: 5px;
    left: 100%;
    top: 5px;
    cursor: default;
}
/* 
.hover-col .menu-options {
    display: none;
    position: absolute;
    padding: 5px;
    left: 100%;
    top: -5px;
    cursor: default;
} */

.hover-col .menu-options .option {
    cursor: pointer;
    color: #383d41;
    background-color: #d6d8db;
}

.hover-col .menu-options .option:hover {
    cursor: pointer;
    background-color: #c8cbcf;
}

.hover-col:hover .menu-options {
    display: block;
}
</style>


<script lang='ts' src="./HoverCol.ts"></script>
