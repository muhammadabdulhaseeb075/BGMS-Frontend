
const OPEN_EMIT = "open";
const CLOSE_EMIT = "close";

const props = {
    show: {type: Boolean, default: false},
};

export default {
    name: "modal-panel",
    props,
    emits: [OPEN_EMIT, CLOSE_EMIT],
};
