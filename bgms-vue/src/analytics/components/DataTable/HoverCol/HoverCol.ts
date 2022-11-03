import Vue from "vue";
import Component from "vue-class-component";

/**
 * Class representing Table component
 * @extends Vue
 */
@Component({
    props: {
        name: String,
        model: Object
    }
})
export default class HoverCol extends Vue {
    clickOnItem(field): void {
        this.$emit('select-field', field, this.$props.name, this.$props.model);
    }
}
