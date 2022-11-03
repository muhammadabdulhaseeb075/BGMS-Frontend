const LOGOUT_EMIT = "logout";
const LOGO_EMIT = "click-logo";

const props = {
    title: {type: String, default: "BGMS"},
};

const emits = [LOGOUT_EMIT];

const methods = {
    onLogout() {
        this.$emit(LOGOUT_EMIT);
    },
    onClickLogo() {
        this.$emit(LOGO_EMIT);
    }
};

export default {
    name: "header-bar",
    
    props,
    emits,
    methods,
};
