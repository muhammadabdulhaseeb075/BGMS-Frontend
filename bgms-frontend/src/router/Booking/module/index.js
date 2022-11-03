import * as actions from "./actions";
import * as getters from "./getters";
import * as mutations from "./mutations";
import state from "./state";

const bookingStore = {
    namespaced: true,
    actions,
    state,
    mutations,
    getters,
};

export default bookingStore;
