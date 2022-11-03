import ModalPanel from "src/components/modal-panel";


const CLOSE_EMIT = "close";
const RESET_EMIT = "reset"

const props = {
  show: { type: Boolean },
  title: { type: String },
  data_id: { type: String, default: "" },
  message: { type: String },
};

const components = {
  ModalPanel,
};

function data() {
  return {};
}

const methods = {
  onClose() {
    this.$emit(CLOSE_EMIT);
  },

  onRemoveEvent() {
    this.$emit(RESET_EMIT);
  }
};

export default {
  name: "confirm-modal",
  props,
  emits: [CLOSE_EMIT, RESET_EMIT],
  components,
  data,
  methods,
};
