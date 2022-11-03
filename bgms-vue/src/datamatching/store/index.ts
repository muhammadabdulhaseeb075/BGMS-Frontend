import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

Vue.config.devtools = process.env.NODE_ENV === "development";

export default new Vuex.Store({
  state: {
  },
  mutations: {
  },
  modules: {
  }
})

// hot reloading
/*if ((module as any).hot) {
  // accept actions and mutations as hot modules
  (module as any).hot.accept(['./modules/Sidebar', './modules/MemorialCaptureSidebar', './modules/AngularMapController', './modules/Offline'], () => {
    // require the updated modules
    // have to add .default here due to babel 6 module output
    const Sidebar = require('./modules/Sidebar').default;
    const MemorialCaptureSidebar = require('./modules/MemorialCaptureSidebar').default;
    const AngularMapController = require('./modules/AngularMapController').default;
    const Offline = require('./modules/Offline').default;
    // swap in the new actions and mutations
    this.$store.hotUpdate({
      modules: {
        Sidebar: Sidebar,
        MemorialCaptureSidebar: MemorialCaptureSidebar,
        AngularMapController: AngularMapController,
        Offline: Offline
      }
    });
  })
}*/
