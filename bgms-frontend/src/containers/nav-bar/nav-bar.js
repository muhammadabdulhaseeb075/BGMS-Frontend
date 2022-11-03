import { useStore } from "vuex";

const setup = () => {
    const { state } = useStore();
    const { router } = state;

    return {
        routes: router.routes,
    };
};

export default {
    name: "nav-bar",
    setup,
};
