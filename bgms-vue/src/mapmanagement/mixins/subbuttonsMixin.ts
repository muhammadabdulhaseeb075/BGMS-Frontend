import Vue from 'vue'
import Component, { mixins } from 'vue-class-component'
import { Prop, Watch } from 'vue-property-decorator'
import { SUBBUTTONNAMES } from '@/mapmanagement/static/constants.ts';
import globalConstants from '@/global-static/constants.ts';
import ManagementToolsMixin from '@/mapmanagement/mixins/managementToolsMixin';

interface SubbuttonsType {
  show: boolean,
  route: string
}

/**
 * Class representing SurveyMixin component
 */
@Component
export default class SurveyMixin extends mixins(ManagementToolsMixin) {

  managementToolRoute = null;

  subbuttons = {} as SubbuttonsType;
  subbuttonNames = null;

  mounted() {
    this.subbuttonNames = SUBBUTTONNAMES;
  }

  /**
   * Watcher: When the name is changed, close subbutton sections if required
   * @param {any} val
   * @param {any} oldVal
   */
  @Watch('$route.name', { immediate: true })
  onRouteNameChanged
  (val: any, oldVal: any) {

    // wait for subbuttons to be populated
    Vue.nextTick(() => {
      if (val !== this.managementToolRoute) {
        for(let subbutton in this.subbuttons) {
          if (this.subbuttons[subbutton].show && !this.isRouteActive(this.subbuttons[subbutton].route)) {
            this.subbuttons[subbutton].show = false;
            break;
          }
        }
      }

      for(let subbutton in this.subbuttons) {
        if (!this.subbuttons[subbutton].show && (this.isRouteActive(this.subbuttons[subbutton].route) 
        // add burial is exception
        || (this.subbuttons[subbutton].route===globalConstants.GRAVE_MANAGEMENT_CHILD_ROUTES.burials && this.isRouteActive(globalConstants.GRAVE_MANAGEMENT_CHILD_ROUTES.addBurial))
        // add person is exception
        || (this.subbuttons[subbutton].route===globalConstants.MEMORIAL_MANAGEMENT_CHILD_ROUTES.persons && this.isRouteActive(globalConstants.MEMORIAL_MANAGEMENT_CHILD_ROUTES.addPerson)))) {

          this.subbuttons[subbutton].show = true;
          break;
        }
      }
    });
  }

  /**
   * Closes all subbuttons appart from the exception
   */
  closeOtherSubbuttons(exception) {
    for(let subbutton in this.subbuttons) {
      if (subbutton!==exception)
        this.subbuttons[subbutton].show = false;
    }
  }

  /**
   * Show/hide survey subbuttons
   */
  toggleSubbuttons(subbuttonsName) {
    if (this.$route.name===this.managementToolRoute) {
      this.closeOtherSubbuttons(subbuttonsName);
      this.subbuttons[subbuttonsName].show = !this.subbuttons[subbuttonsName].show;
    }
    else if (!this.subbuttons[subbuttonsName].show) {
      // close open section
      this.$router.push(this.openOrCloseChildRoute(this.managementToolRoute, this.$route.name), () => {
        this.closeOtherSubbuttons(subbuttonsName);
        this.subbuttons[subbuttonsName].show = true;
      });
    }
    else {
      if (this.isRouteActive(this.subbuttons[subbuttonsName].route))
        // close open reservations section
        this.$router.push(this.openOrCloseChildRoute(this.managementToolRoute, this.subbuttons[subbuttonsName].route), () => {
          this.subbuttons[subbuttonsName].show = false;
        });
      // exception for burial
      else if (this.subbuttons[subbuttonsName].route===globalConstants.GRAVE_MANAGEMENT_CHILD_ROUTES.burials && this.isRouteActive(globalConstants.GRAVE_MANAGEMENT_CHILD_ROUTES.addBurial))
        // close open add burial section
        this.$router.push(this.openOrCloseChildRoute(this.managementToolRoute, globalConstants.GRAVE_MANAGEMENT_CHILD_ROUTES.addBurial), () => {
          this.subbuttons[subbuttonsName].show = false;
        });
      // exception for person
      else if (this.subbuttons[subbuttonsName].route===globalConstants.MEMORIAL_MANAGEMENT_CHILD_ROUTES.persons && this.isRouteActive(globalConstants.MEMORIAL_MANAGEMENT_CHILD_ROUTES.addPerson))
        // close open add burial section
        this.$router.push(this.openOrCloseChildRoute(this.managementToolRoute, globalConstants.MEMORIAL_MANAGEMENT_CHILD_ROUTES.addPerson), () => {
          this.subbuttons[subbuttonsName].show = false;
        });
      else
        this.subbuttons[subbuttonsName].show = false;
    }
  }
}