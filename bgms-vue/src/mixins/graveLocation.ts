import Vue from 'vue'
import Component from 'vue-class-component'
import { Watch } from 'vue-property-decorator';
import axios from 'axios';
import { ModelListSelect } from 'vue-search-select';
import 'vue-search-select/dist/VueSearchSelect.css'

@Component({
  components: {
    ModelListSelect
  }
})
export default class GraveLocation extends Vue {

  enteredGraveNumber: string = "";
  selectedSection: string = "";
  selectedSubsection: string = "";
  selectedGraveId: string = "";
  selectedFeatureID: string = "";

  loadingSections: boolean = false;
  loadingSubsections: boolean = false;
  loadingGraves: boolean = false;

  domainURL: string = "";
  includeGraves: boolean = false;

  beforeMount() {
    // These are used for the booking form which needs to store for multiple sites
    if (this.domainURL) {
      if (!this.$store.state.allSections[this.domainURL])
        this.$store.state.allSections[this.domainURL] = [];

      if (!this.$store.state.allSubsections[this.domainURL])
        this.$store.state.allSubsections[this.domainURL] = [];

      if (!this.$store.state.allGraves[this.domainURL])
        this.$store.state.allGraves[this.domainURL] = [];
      
      this.includeGraves = true;
    }
  }

  /**
   * Vue mounted lifecycle hook
   * - gets list of grave_numbers, sections, subsections
   */
  mounted() {

    if ((!this.$store.state.Offline || this.$store.state.Offline.online) && (!this.allSections || !this.allSections.length)) {
      this.loadingSections = true;

      // Get all sections
      axios.get(this.domainURL + '/mapmanagement/getSections/')
        .then(response => {

          if (response.data && response.data.length > 0)
            this.allSections = response.data;

          this.loadingSections = false;
        })
        .catch(response => {
          console.warn('Couldn\'t get sections:', response);
          this.loadingSections = false;
        });
    }

    if (!this.allSubsections || !this.allSubsections.length) {
      this.loadingSubsections = true;

      // Get all subsections
      axios.get(this.domainURL + '/mapmanagement/getSubsections/')
        .then(response => {

          if (response.data && response.data.length > 0)
            this.allSubsections = response.data;

          this.loadingSubsections = false;
        })
        .catch(response => {
          console.warn('Couldn\'t get subsections:', response);
          this.loadingSubsections = false;
        });
    }

    if (this.includeGraves && (!this.allGraves || !this.allGraves.length)) {
      this.loadingGraves = true;

      // Get all subsections
      axios.get(this.domainURL + '/mapmanagement/getGraveNumbers/')
      .then(response => {

        if (response.data && response.data.length > 0)
          this.allGraves = response.data;

        this.loadingGraves = false;
      })
      .catch(response => {
        console.warn('Couldn\'t get grave numbers:', response);
        this.loadingGraves = false;
      });
    }
  }

  /*** Watchers ***/

  /**
   * Watcher: When the selected subsection is changed, this selects the section and resets the grave
   * @param {any} val
   * @param {any} oldVal
   */
  @Watch('selectedGraveId')
  onGraveChanged(val: any, oldVal: any) {
    if (val) {
      const grave = this.allGraves.find(grave => grave.id === val);

      if (grave) {
        if (this.allSections && !this.selectedSection)
          this.selectedSection = grave.section ? grave.section : "";

        if (this.allSubsections && !this.selectedSubsection)
          this.selectedSubsection = grave.subsection ? grave.subsection : "";
      }
    }
  }

  /**
   * Watcher: When the selected subsection is changed, this selects the section and resets the grave
   * @param {any} val
   * @param {any} oldVal
   */
  @Watch('selectedSubsection')
  onSubsectionChanged(val: any, oldVal: any) {
    if (val) {
      const subsection = this.allSubsections.find((subsection: any) => subsection.id === val);

      if (subsection) {
        if (this.allSections && !this.selectedSection)
          this.selectedSection = subsection.section;
          
        // if grave is selected but it does not belong to subsection
        if (this.includeGraves && this.allGravesFiltered && this.selectedGraveId && 
          !this.allGravesFiltered.find(grave => grave.id === this.selectedGraveId)) {
          this.selectedGraveId = "";
        }
      }
    }
  }

  /**
   * Watcher: When the selected section is changed, this resets the grave
   * @param {any} val
   * @param {any} oldVal
   */
  @Watch('selectedSection')
  onSectionChanged(val: any, oldVal: any) {
    // reset the subsection
    if (val) {
      // if subsection is selected but it does not belong to section
      if (this.allSubsectionsFiltered && this.selectedSubsection && 
        !this.allSubsectionsFiltered.find((subsection: any) => subsection.id === this.selectedSubsection)) {
        this.selectedSubsection = "";
      }

      // if grave is selected but it does not belong to section
      if (this.includeGraves && this.allGravesFiltered && this.selectedGraveId && 
        !this.allGravesFiltered.find(grave => grave.id === this.selectedGraveId)) {
        this.selectedGraveId = "";
      }
    }
    else {
      this.selectedSubsection = "";
    }
  }

  /*** Computed ***/

  /**
   * Computed property: Get the available sections
   * @returns {any} 
   */
  get allSections() {
    if (this.domainURL)
      return this.$store.state.allSections[this.domainURL];
    else
      return this.$store.state.allSections
  }
  set allSections(sections) {
    if (this.domainURL) {
      let currentSections = this.$store.state.allSections[this.domainURL];

      // add blank value first
      if (sections) currentSections.push({ id: null, section_name: "" });
      currentSections.push.apply(currentSections, sections);
    }
    else
      this.$store.commit('populateSections', sections);
  }

  /**
   * Computed property: Get the available subsections
   * @returns {any}
   */
  get allSubsections() {
    if (this.domainURL)
      return this.$store.state.allSubsections[this.domainURL];
    else
      return this.$store.state.allSubsections
  }
  set allSubsections(subsections) {
    if (this.domainURL) {
      let currentSubsections = this.$store.state.allSubsections[this.domainURL];

      // add blank value first
      if (subsections) currentSubsections.push({ id: null, subsection_name: "" });
      currentSubsections.push.apply(currentSubsections, subsections);
    }
    else
      this.$store.commit('populateSubsections', subsections);
  }

  /**
   * Computed property: Get subsections filtered depending on what section is selected
   * @returns {any} memorial
   */
  get allSubsectionsFiltered() {
    if (this.selectedSection)
      return this.allSubsections.filter(subsection => subsection.section === this.selectedSection);
    else
      return this.allSubsections
  }

  /**
   * Computed property: Get the available graves
   * @returns {any}
   */
  get allGraves() {
    if (this.domainURL)
      return this.$store.state.allGraves[this.domainURL];
    else
      return this.$store.state.allGraves
  }
  set allGraves(graves) {
    if (this.domainURL) {
      let currentGraves = this.$store.state.allGraves[this.domainURL];

      currentGraves.push.apply(currentGraves, graves);
    }
    else
      this.$store.commit('populateGraves', graves);
  }

  /**
   * Computed property: Get graves filtered depending on what section/subsection is selected
   * @returns {any} memorial
   */
  get allGravesFiltered() {
    if (this.selectedSubsection)
      return this.allGraves.filter(grave => grave.subsection === this.selectedSubsection);
    else if (this.selectedSection)
      return this.allGraves.filter(grave => grave.section === this.selectedSection);
    else
      return this.allGraves
  }
}
