import Vue from 'vue'
import Component from 'vue-class-component'
import axios from 'axios'

@Component
export default class SecurityMixin extends Vue {

  /**
   * Promise resolves to true if user is in given group
   * @param groupNames 
   */
  getGroupRequiredValue(groupNames) {
    return new Promise((resolve, reject) => {
      axios.get('/bgsite/group_required/', { 'params': { 'group_names': JSON.stringify(groupNames) }})
      .then(function(response) {
        resolve(response.data.group_required);
      })
      .catch(function(response) {
        console.log('could not load data' + response);
        resolve(false);
      });
    });
  }

  /**
   * Promise resolves to return users groups
   * @param groupNames 
   */
  getGroups() {
    return new Promise((resolve, reject) => {
      axios.get('/bgsite/user_groups/')
      .then(function(response) {
        resolve(response.data.groups);
      })
      .catch(function(response) {
        console.log('could not load data' + response);
        resolve(false);
      });
    });
  }
}