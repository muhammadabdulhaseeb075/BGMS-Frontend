import { mapActions } from "vuex";
export default {
    props: ["notification"],
    data() {
        return {
            timeout: null
        };
    },
    computed: {
        typeClass() {
            return `alert-${this.notification.type}`;
        }
    },
    created() {
        this.timeout = setTimeout(() => {
            this.removeNotification(this.notification);
        }, 6000);
    },
    beforeDestroy() {
        clearTimeout(this.timeout);
    },
    methods: mapActions(["removeNotification"])
};