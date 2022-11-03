<template>
    <div
    class="add-to-table-btn">
        <v-btn
        color="rgb(195, 175, 66)"
        dark
        @click="toggleMenu">
            Add To Table
        </v-btn>

        <div
        v-if="displayModelMenu"
        class="models-menu">
            <div
            v-for="(modelData, modelName) in models"
            :key="modelName"
            class="model-item">
                <div>
                    {{modelName}}
                </div>

                <div class="fields-submenu">
                    <div
                    class="field-item"
                    v-for="(fieldData, index) in modelData.fields"
                    :key="index"
                    @click="clickOnItem(fieldData, modelName, modelData)"
                    >
                        <span>
                            {{fieldData.field}}
                            <!-- <i>({{fieldData.type}})</i> -->
                        </span>
                    </div>
                </div>
            </div>
        </div>

    </div>
</template>

<style scoped>
.add-to-table-btn {
    display: block;
    position: relative;
}

.add-to-table-btn .models-menu {
    min-width: 200px;
    position: absolute;
    background: white;
    z-index: 999;
    border: 1px solid gray;
}

.add-to-table-btn .model-item {
    margin: 2px 0;
    padding: 7px;
}

.add-to-table-btn .model-item .fields-submenu {
    position: absolute;
    background: gray;
    padding: 10px 7px;
    display: none;
    transform: translateY(-24px);
    left: 100%;
}

.add-to-table-btn .model-item:hover .fields-submenu {
    display: block;
}

.add-to-table-btn .model-item .fields-submenu .field-item {
    margin: 3px 0;
    cursor: pointer;
}

.add-to-table-btn .model-item .fields-submenu .field-item i {
    font-size: 10px;
}

</style>


<script lang='ts'>
import Vue from "vue";
import Component from "vue-class-component";

/**
 * Class representing Table component
 * @extends Vue
 */
@Component({
    props: {
        models: Object
    }
})
export default class AddToTableBtn extends Vue {
    displayModelMenu: boolean = false;

    toggleMenu(): void {
        this.displayModelMenu = !this.displayModelMenu;
    }

    clickOnItem(field, modelName, modelData): void {
        this.$emit('select-field', field, modelName, modelData);
    }
}
</script>
