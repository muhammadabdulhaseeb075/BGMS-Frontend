import Vue from 'vue';
import Component from 'vue-class-component';

@Component({})
export default class VerticalMenu extends Vue {
    resetReport(): void {
        this.$store.state.selectedReport = null;
    }
}
