import NotificationMessage from "../notification-message";
import { mapState } from "vuex";
export default {
    components: {
        NotificationMessage
    },
    computed: mapState(["notifications"])
};

