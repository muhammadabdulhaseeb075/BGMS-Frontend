import Vue from 'vue'
import Vuex from 'vuex';
import Component, { mixins } from 'vue-class-component'
import axios from 'axios'
import { Watch } from 'vue-property-decorator';
import constants from '@/mapmanagement/static/constants.ts';
import { makeUndefinedNumbersNull } from '@/global-static/dataFormattingAndValidation.ts';

const hash = require('object-hash');

Vue.use(Vuex);

/**
 * Class representing ManagementToolsMixin component
 */
@Component
export default class ManagementToolsMixin extends Vue {

  notificationHelper = this.$store.getters.notificationHelper;
  siteAdminOrSiteWarden: boolean = this.$store.state.siteAdminOrSiteWarden;

  // TODO: this field is probably unneccessary now
  editableFields = [];

  componentName = '';
  _id = null;

  // Component data is also stored in vuex. It's in Vuex for the so it can be accessed by Vue Router only.
  componentData = null;
  componentDataSaved = null;
  componentDataSavedHash = null;

  loadingDataFlag: boolean = false;
  editFlag: boolean = false;
  heightChangedFlag: number = 0;

  labelColumnClasses = constants.LABEL_COLUMN_CLASSES;
  fieldColumnClasses = constants.FIELD_COLUMN_CLASSES;
  
  /**
   * Vue mounted lifecycle hook
   * - get edit flag from URL
   */
  mounted() {
    window.setTimeout(() => {
      if (this.$route.query.edit != null)
        this.editFlag = this.$route.query.edit.toString() === "true";
    });

    // Listen for the screen being resized.
    // Used for scroll buttons.
    window.addEventListener('resize', () => {
      this.heightChangedFlag += 1;
    });
  }

  /**
   * Vue destroyed lifecycle hook
   * - Remove data from vuex
   * - Remove all router queries except refresh
   */
  destroyed() {
    this.$store.commit('removeComponentData', this.componentName);
  }

  /*** Computed ***/

  /**
   * @returns {boolean} True if a field has been changed
   */
  get fieldChanged(): boolean {

    if (this.componentData) {
      // this field isn't actually needed here and interfers with hash comparrison
      delete this.componentData.unsavedChanges;

      // if this is a new record or a field has been changed
      if (!this.componentDataSaved || (hash(this.componentData) != this.componentDataSavedHash)) {
        this.$store.commit('componentHasUnsavedChanges', this.componentName);
        return true;
      }
      else {
        this.$store.commit('componentHasNoUnsavedChanges', this.componentName);
        return false;
      }
    }

    return false;
  }

  /**
   * @returns {boolean} True if no details are saved
   */
  get noData(): boolean {

    return !this.editableFields.find(field => {
      if (typeof field === 'object') {
        // this is a nested object with it's own fields
        for (let fieldObject in field) {
          // if object is null
          if (this.componentData[fieldObject]) {
            for (let subField in field[fieldObject]) {
              subField = field[fieldObject][subField];
              if (this.componentData[fieldObject][subField]) {
                return true;
              }
            }
          }
        }
      }
      // if item is an array
      else if (Array.isArray(this.componentData[field])) {
        if(this.componentData[field].length > 0) {
          return true;
        }
      }

      else if (this.componentData[field]) {
        return true;
      }

      else {
        return false;
      }
    });
  }

  // Set by vue router for when the saved data needs restored. I.e. when discarding changes in a form.
  get restoreSavedDataFlag() {
    return this.$store.state.ManagementTool.restoreSavedDataFlag;
  }

  /*** Watchers ***/

  /**
   * Watcher: When restoreSavedDataFlag is changed
   * @param {any} val
   * @param {any} oldVal
   */
  @Watch('restoreSavedDataFlag', {immediate: true})
  onRestoreSavedData(val: any, oldVal: any) {
    // if flag is for this component
    if(val && val===this.componentName) {
      // restore saved data
      this.$store.commit('cloneSavedToUnsaved', this.componentName);
      this.$store.commit('componentHasNoUnsavedChanges', this.componentName);
      this.componentData = this.$store.state.ManagementTool.currentInformation[this.componentName];
      // reset flag
      this.$store.commit('commitRestoreSavedDataFlag', null);
    }
  }

  /**
   * Watcher: When edit in router query is changed
   * @param {any} val
   * @param {any} oldVal
   */
  @Watch('$route.query.edit')
  onEditChanged(val: any, oldVal: any) {
    if (val === 'true')
      this.editFlag = true;
    else
      this.editFlag = false;
    
    this.heightChangedFlag += 1;
  }

  /**
   * Used to update parent that size of component has changed
   */
  @Watch('heightChangedFlag')
  onHeightChangedFlagChanged(val: any, oldVal: any) {
    this.$emit('height-changed', null)
  }

  /**
   * Watches fieldChanged.
   * This doesn't actually do anything except ensure computed property is being calling.
   */
  @Watch('fieldChanged')
  onFieldChanged(val: any, oldVal: any) {
  }

  /*** Methods ***/

  /**
   * Opens the managemnt tool.
   * Sets width and moves other items on page to make way
   */
  openTool(narrow: boolean = false) {

    let toolWidth = narrow ? constants.TOOL_WIDTH_NARROW : constants.TOOL_WIDTH;
    let contentBarWidth = 0;

    if (document.getElementById("management-tool-contentbar"))
      // if page has been refreshed and contentbar is open, this will ensure button goes to correct position
      contentBarWidth = constants.TOOL_CONTENT_WIDTH + constants.TOOL_BORDER_WIDTH;

    // i.e. if this is not already open
    if (document.getElementById('management-tool-container').style.right != "5px" || document.getElementById('management-tool-container').style.width != (toolWidth + "px") || document.getElementById('management-tool-contentbar-container').style.right != toolWidth - constants.TOOL_BORDER_WIDTH + "px") {

      // set layers accordion position if it needs moved
      let layersAccordion = document.getElementById('layersAccordion');
      if (layersAccordion) {
        if (layersAccordion.style.right === "5px" || !layersAccordion.style.right)
          layersAccordion.style.right = toolWidth + contentBarWidth + 10 + "px";
        layersAccordion.style.top = "55px";
      }

      // hide tools accordion
      let horizontalToolsAccordion = document.getElementById('horizontalToolsAccordion');
      if (horizontalToolsAccordion)
        horizontalToolsAccordion.style.display = "none";

      // set widths (this is needed to allow for two tool widths)
      document.getElementById('management-tool-container').style.width = toolWidth + "px";
      document.getElementById('management-tool-title-vertical').style.left = toolWidth + "px";
      
      // set rights
      document.getElementById('management-tool-container').style.right = "5px";
      document.getElementById('management-tool-contentbar-container').style.right = toolWidth - constants.TOOL_BORDER_WIDTH + "px";
    }
  }

  /**
   * Update saved version for form fields with unsaved version (on successful save)
   */
  updateSavedVersion() {    
    // this field isn't actually needed here and interfers with hash comparrison
    delete this.componentData.unsavedChanges;

    this.$store.commit('cloneUnsavedToSaved', { componentName: this.componentName, data: this.componentData });
    this.$store.commit('componentHasNoUnsavedChanges', this.componentName);
    this.componentDataSaved = this.$store.state.ManagementTool.currentInformationSaved[this.componentName];
    this.componentDataSavedHash = hash(this.componentDataSaved);
  }

  /**
   * Checks each field to find if it has changed. If it has, add it to data object.
   */
  getChangedData() {
    
    let data = { id: this._id };

    this.editableFields.forEach(field => {

      // if this is new data
      if (!this.componentDataSaved && this.componentData[field])
        data[field] = this.componentData[field];
      // if this is an array
      else if (this.componentData[field] && Array.isArray(this.componentData[field])) {

        let changedObjectData = this.lookForChangedDataInArray(this.componentData[field], this.componentDataSaved[field]);
            if (changedObjectData)
              data[field] = changedObjectData;
      }
      // if this is an object
      else if (this.componentData[field] && ((typeof this.componentData[field] === 'object' && this.componentData[field].constructor === Object))) {

        let changedObjectData = this.lookForChangedDataInObject(this.componentData[field], this.componentDataSaved[field]);
            if (changedObjectData)
              data[field] = changedObjectData;
      }
      else {
        if (this.componentData[field] !== this.componentDataSaved[field])
          data[field] = this.componentData[field];
      }
    });

    data = makeUndefinedNumbersNull(data);

    return data;
  }

  /**
   * Recursive function for getting changed data within an array.
   * If one array has been changed, return the whole array.
   * @param array 
   * @param savedArray
   * @returns Object containing any unsaved data
   */
  lookForChangedDataInArray(array, savedArray) {    
    let changedData = [];

    // if array has just been added or deleted
    if ((array && !savedArray) 
    || (!array && savedArray)) {
      changedData = array;
    }
    else {
      for (let key in array) {
        // this array item contains another array
        if (array[key] && Array.isArray(array[key])) {
          let changedObjectData = this.lookForChangedDataInArray(array[key], savedArray[key]);
          if (changedObjectData) {
            changedData = array;
          }
        }
        // this array item contains an object
        else if (array[key] && typeof array[key] === 'object' && array[key].constructor === Object) {
          let changedObjectData = this.lookForChangedDataInObject(array[key], savedArray[key]);
          if (changedObjectData) {
            changedData = array;
          }
        }
        else if (array[key] != savedArray[key]) {
          changedData = array;
        }
      }
    }

    if (changedData.length === 0)
      return null;
    return changedData
  }

  /**
   * Recursive function for getting changed data within an object
   * @param object 
   * @param savedObject
   * @returns Object containing any unsaved data
   */
  lookForChangedDataInObject(object, savedObject) {    
    let changedData = {};

    // if object has just been added or deleted
    if ((object && !savedObject) 
    || (!object && savedObject)) {
      changedData = object;
    }
    else {
      for (let key in object) {
        // this object item contains an array
        if (object[key] && Array.isArray(object[key])) {
          let changedObjectData = this.lookForChangedDataInArray(object[key], savedObject[key]);
          if (changedObjectData) {
            changedData[key] = changedObjectData;
          }
        }
        // this object item contains another object
        else if (object[key] && typeof object[key] === 'object' && object[key].constructor === Object) {
          let changedObjectData = this.lookForChangedDataInObject(object[key], savedObject[key]);
          if (changedObjectData) {
            changedData[key] = changedObjectData;
          }
        }
        else if (object[key] != savedObject[key]) {
          changedData[key] = object[key];
        }
      }
    }

    if (Object.getOwnPropertyNames(changedData).length === 0)
      return null;
    return changedData
  }

  /**
   * Load data from server and resturn result in promise
   * @param url 
   */
  loadDataWithoutStoring(url, id) {
    let v = this;
    //debugger; // eslint-disable-line no-debugger //:BGMS-1555
    v.componentData = null;
    v.componentDataSaved = null;
    v.componentDataSavedHash = null;

    // Get data needed for component
    return new Promise((resolve, reject) => {

      if (id !== undefined) {
        v.loadingDataFlag = true;

        axios.get(url + id)
        .then(function(response) {
          resolve(response.data);
          v.loadingDataFlag = false;
        })
        .catch(function(response) {
          console.warn('Couldn\'t get data from server: ' + response.response.data);
          v.notificationHelper.createErrorNotification("Data cannot be loaded");
          reject();
          v.loadingDataFlag = false;
        });
      }
      else {
        reject();
      }
    });
  }

  /**
   * Load data from server and store
   * @param url 
   */
  loadData(url, id, extra=null) {
    let v = this;
    //debugger; // eslint-disable-line no-debugger //:BGMS-1555
    return this.loadDataWithoutStoring(url, id)
    .then((result) => {
      Object.assign(result,extra);
      v.storeData(result);
    })
    .catch(() => {});
  }

  /**
   * 
   * @param data Store data for this component
   */
  storeData(data) {
    this.$store.commit('setCurrentInformation', { componentName: this.componentName, data: data });
    this.componentData = this.$store.state.ManagementTool.currentInformation[this.componentName];
    // store a cloned version if changes need rolled back
    this.$store.commit('cloneUnsavedToSaved', { componentName: this.componentName, data: data });
    this.componentDataSaved = this.$store.state.ManagementTool.currentInformationSaved[this.componentName];
    this.componentDataSavedHash = hash(this.componentDataSaved);

    window.setTimeout(() => {
      this.heightChangedFlag += 1;
    });
  }

  /**
   * Create or modify item in query
   * @param itemName 
   * @param itemValue 
   */
  appendToOrModifyItemInQuery(itemName, itemValue) {
    let query = JSON.parse(JSON.stringify(this.$route.query));
    if (itemValue !== null)
      query[itemName] = itemValue;
    else
      delete query[itemName];

    this.$router.replace({ query: query });
  }

  /**
   * What happens when edit or cancel buttons are clicked in create mode
   */
  toggleEditCancelButtonsInCreateMode(edit, id, homePath) {
    if (!id)
      // this is create mode, so close the section
      this.$router.replace({ name: homePath });
    else
      this.appendToOrModifyItemInQuery('edit', edit)
  }

  /**
   * If route is currently parent, go to child.
   * If route if currently child, go to parent. 
   * @param parentName 
   * @param childName 
   * @param childParams array of objects {name, value}
   */
  openOrCloseChildRoute(parentName, childName, childParams=null) {
    let returnValue = {};
    
    if (this.$route.name === childName)
      returnValue['name'] = parentName;
    else {
      // route is different so go to child route
      returnValue['name'] = childName;

      if (childParams && childParams.length > 0) {
        let params = {};
        childParams.forEach((child) => {
          params[child.name] = child.value;
        });
        returnValue['params'] = params;
      }
    }
      
    let query = JSON.parse(JSON.stringify(this.$route.query));
    
    // keep queries that are needed to refresh parent data
    Object.keys(query).forEach(function(key,index) {
      if (key !== 'refresh' || key.indexOf('refresh') === -1) 
        delete query[key];
    });

    returnValue['query'] = query;

    return returnValue;
  }

  isRouteActive(routeName) {
    return this.$route.name===routeName || this.$route.path.indexOf('/' + routeName + '/') !== -1;
  }

  /**
   * Puts items into a string seperated by the delimiter
   * @param items Array
   * @param delimiter 
   */
  getJoinedText(items, delimiter): string {
    let returnText = "";

    for (let i in items) {
      if (items[i]) {
        if (returnText)
          returnText += delimiter;
        
        returnText += items[i];
      }
    }

    return returnText;
  }

  /**
   * Get field from a specific item within an object
   * @param matchField Object field to find
   * @param matchValue Find value
   * @param returnField Object field to return as restult
   */
  getFieldFromObjectItem(matchField, matchValue, returnField, searchData=null) {
    if (!searchData)
      searchData = this.componentData;

    let item = searchData.find(item => 
      item[matchField] === matchValue
    );
    
    if (item)
      return item[returnField];
    else
      return null;
  }
}
