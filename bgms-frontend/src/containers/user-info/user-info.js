import { useStore } from "vuex";

const setup = () => {
    const { state } = useStore();

    return {
        user: state.user,
    };
};

export default {
    name: "user-info",
    setup,
};
