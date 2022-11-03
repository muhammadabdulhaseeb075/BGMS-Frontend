<template>
  <v-dialog
    value="true"
    persistent
    max-width="700px">
    <v-card>
      <v-card-title>
        <span class="headline">Add New Funeral Director</span>
      </v-card-title>
      <v-card-text>
        <v-form ref="form">
          <PersonCompanyForm :personOrCompany="funeralDirector" :address="funeralDirectorAddress" recordIsCompany="true"></PersonCompanyForm>
        </v-form>

      </v-card-text>
      <v-card-actions>
        <div class="flex-grow-1"></div>
        <v-btn color="blue darken-1" text @click="closeDialog">Cancel</v-btn>
        <v-btn color="blue darken-1" text @click="submit" :loading="saving">Save</v-btn>
      </v-card-actions>

    </v-card>
  </v-dialog>
</template>

<script lang='ts'>
import Vue from 'vue';
import Component, { mixins } from 'vue-class-component';
import { Prop } from 'vue-property-decorator';
import axios from 'axios'
import NotificationMixin from '@/mixins/notificationMixin.ts';
import PersonCompanyForm from '@/main/components/Booking/BookingFormComponents/PersonCompanyForm.vue';

@Component({
  components: {
    PersonCompanyForm,
  }
})
export default class FuneralDirectorDialog extends mixins(NotificationMixin) {

  @Prop() domain;

  funeralDirector = {};

  saving: boolean = false;

  get funeralDirectorAddress() {
    if (!this.funeralDirector['address'])
      this.funeralDirector['address'] = {};
    
    return this.funeralDirector['address'];
  }

  /*** Methods ***/

  submit() {
    if ((this.$refs.form as HTMLFormElement).validate()) {

      this.saving = true;

      axios.post(this.domain + "/cemeteryadmin/funeralDirector/", { company: this.funeralDirector })
      .then(response => {

        this.createSuccessNotification("Funeral director created successfully");

        // return fd info to parent
        const obj = {
          id: response.data.id,
          name: response.data.company.name,
          contact_name: response.data.company.contact_name,
          retired: false
        }
        this.$emit("new-fd", obj);
        this.closeDialog();
      })
      .catch(error => {
        this.createHTTPErrorNotificationandLog(error, "Failed to save new funeral director.");
        this.saving = false;
      });
    }
  }

  /**
   * Emit event to parent which will close this dialog
   */
  closeDialog() {
    this.$emit("close-dialog")
  }
}
</script>