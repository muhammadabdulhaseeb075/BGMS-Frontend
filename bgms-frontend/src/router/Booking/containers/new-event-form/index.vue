<template>
  <div class="new-event-form">
    <new-booking-header
      :edit-mode="editMode"
      :update-event="isUpdatingEvent"
      :save-disabled="!isEventFormValid"
      :reference_number="reference_number"
      :redirect="fromCalendar"
      @save-event="submitEventForm"
      @remove-event="
        () => {
          //if (fromCalendar && !editMode) goToCalendar();
          if (isUpdatingEvent) editMode = false;
        }
      "
      @edit-event="
        () => {
          editMode = true;
        }
      "
    >
    </new-booking-header>

    <form-modals
      v-if="modalForm.show"
      :show="modalForm.show"
      :title="modalForm.title"
      :modal-name="modalForm.name"
      :data_id="modalForm.data_id"
      :namespace-fields="modalForm.namespaceFields"
      :form="eventForm"
      @submit-form="receiveModalForm"
      @close="modalForm.show = false"
    />

    <confirm-modal
        title="Confirmation needed"
        message="Event is not saved, Do you want to save it?"
        :show="showSaveConfirm"
        @close="showSaveConfirm = false"
        @reset="() => { 
          submitEventForm();
          showSaveConfirm = false;
        }"
    />

    <post-save-modal
        title=""
        :query="postSaveData"
        message="Event Saved. Would you like to go to another module?"
        :show="showPostSaveModal"
        @close="showPostSaveModal = false"
    />


    <div class="form">
      <!-- Booking section -->
      <form-section title="Booking">
        <!-- -->
        <div class="form-field-group">
          <form-section-field label="Type*:">
            <strong>
            <input-field
              class="input-booking"
              :class="{ 'view-mode': !editMode }"
              v-bind="eventForm.fields.type"
              v-model="eventForm.fields.type.value"
              :form-data="eventForm.data"
              :disabled="!editMode"
              @on-validate="validEventForm"
            />
            </strong>
          </form-section-field>
        </div>

        <!-- Date fields group -->
        <div class="form-field-group">
          <!-- -->
          <form-section-field label="Date:">
            <input-field
              class="input-booking"
              :class="{
                'view-mode': !editMode,
              }"
              v-bind="eventForm.fields.date"
              v-model="eventForm.fields.date.value"
              :form-data="eventForm.data"
              :disabled="!editMode"
              @on-validate="validEventForm"
            />
          </form-section-field>

          <!-- -->
          <form-section-field label="Time:">
            <time-picker
              :class="{ 'view-mode': !editMode }"
              :slot-min-time="slotMinTime"
              :slot-max-time="slotMaxTime"
              v-bind="eventForm.fields.time"
              v-bind:value="eventForm.fields.time.value"
              v-on:time-change="eventForm.fields.time.value = $event"
              :form-data="eventForm.data"
              :disabled="!editMode"
              @on-validate="validEventForm"
            ></time-picker>
          </form-section-field>

          <!-- -->
          <form-section-field label="Duration:">
            <input-field
              class="input-booking"
              :class="{ 'view-mode': !editMode }"
              v-bind="eventForm.fields.duration"
              v-model="eventForm.fields.duration.value"
              :form-data="eventForm.data"
              :disabled="!editMode"
              @on-validate="validEventForm"
              @format="eventForm.fields.duration.format"
            />
          </form-section-field>
        </div>
      </form-section>
      <!--/ Booking section -->

      <!-- Deceased section -->
      <form-section title="Deceased">
        <!-- person name -->
        <div class="form-field-group">
          <!-- -->
          <form-section-field
            label="Title:"
          >
            <input-field
              class="input-booking"
              :class="{
                'view-mode': !editMode,
              }"
              :placeholder="editMode ? 'Title' : ''"
              v-bind="eventForm.fields.deceaseTitle"
              v-model="eventForm.fields.deceaseTitle.value"
              :form-data="eventForm.data"
              :disabled="!editMode"
              @on-validate="validEventForm"
            />
          </form-section-field>

          <!-- -->
          <form-section-field
            label="First Name*:"
          >
            <input-field
              class="input-booking"
              :class="{ 'view-mode': !editMode }"
              :placeholder="editMode ? 'First Name' : ''"
              v-bind="eventForm.fields.deceaseFirstName"
              v-model="eventForm.fields.deceaseFirstName.value"
              :form-data="eventForm.data"
              :disabled="!editMode"
              @on-validate="validEventForm"
            />
          </form-section-field>

          <!-- -->
          <form-section-field label="Last Name*:">
            <input-field
              class="input-booking"
              :class="{ 'view-mode': !editMode }"
              :placeholder="editMode ? 'Last Name' : ''"
              v-bind="eventForm.fields.deceaseLastName"
              v-model="eventForm.fields.deceaseLastName.value"
              :form-data="eventForm.data"
              :disabled="!editMode"
              @on-validate="validEventForm"
              @format="eventForm.fields.deceaseLastName.format"
            />
          </form-section-field>
        </div>

        <!-- Age and Death date -->
        <div class="form-field-group">
          <!-- -->
          <form-section-field
            label="Age:"
          >
            <input-field
              class="input-booking noNeg"
              :placeholder="editMode ? 'Age' : ''"
              v-bind="eventForm.fields.deceaseAge"
              v-model="eventForm.fields.deceaseAge.value"
              :form-data="eventForm.data"
              :disabled="!editMode"
              @on-validate="validEventForm"
            />
          </form-section-field>

          <form-section-field
            label=""
          >
            <input-field
              class="input-booking"
              :placeholder="editMode ? 'Age Type' : ''"
              v-bind="eventForm.fields.deceaseAgeType"
              v-model="eventForm.fields.deceaseAgeType.value"
              :form-data="eventForm.data"
              :disabled="!editMode"
              @on-validate="validEventForm"
            />
          </form-section-field>

          <!-- -->
          <form-section-field
            label="Date of Death:"
          >
            <input-field
              class="input-booking"
              :class="{ 'view-mode': !editMode }"
              :placeholder="editMode ? 'yyy-mm-dd' : ''"
              v-bind="eventForm.fields.deceaseDateOfDeath"
              v-model="eventForm.fields.deceaseDateOfDeath.value"
              :form-data="eventForm.data"
              :disabled="!editMode"
              @on-validate="validEventForm"
              @format="eventForm.fields.deceaseDateOfDeath.format"
            />
          </form-section-field>
        </div>

        <!-- Address -->
        <div class="form-field-group">
          <!-- -->
          <form-section-field
            label="Address:"
          >
            <div class="flex addFlex">

              <div v-show="!fullDeceasedAddress && !editMode" class="mr-4 addFlex">
                <input-field :disabled="true" />
              </div>
              <div v-show="fullDeceasedAddress" class="mr-4 addFlex">
                <input-field :placeholder="editMode ? 'Postcode' : ''" :disabled="true" v-model="fullDeceasedAddress" />
              </div>

              <address-event-field
                v-if="editMode"
                :edit-mode="!!fullDeceasedAddress"
                @save-address="
                  (addressData) => {
                    addAddressFor('person.residence_address', addressData);
                  }
                "
                @remove-address="
                  () => {
                    eventForm.data.person.residence_address = null;
                    removePlaceOfDeathAsAddressIfNotExists();
                  }
                "
              />
            </div>
          </form-section-field>
        </div>

        <!-- Place -->
        <div class="form-field-group">
          <!-- -->
          <form-section-field
              v-if="editMode && fullOtherAddress"
              label="Place of Death:"
          >
            <div v-if="!editMode" class="flex addFlex">
              <div v-if="!editMode" class="mr-4 addFlex">
                <input-field
                    v-if="!editMode"
                    v-model="fullOtherAddress"
                    :form-data="eventForm.data"
                    :disabled="true"
                />
              </div>
            </div>
            <div v-if="editMode && fullOtherAddress" class="flex addFlex">
              <span v-if="editMode && fullOtherAddress" class="mr-2">As Address: </span>
              <div v-if="editMode && fullOtherAddress" class="inline-block">
                <input-field
                    v-if="editMode && fullOtherAddress"
                    class="input-booking"
                    :class="{ 'view-mode': !editMode }"
                    v-bind="eventForm.fields.deceasePlaceOfDeath"
                    v-model="eventForm.fields.deceasePlaceOfDeath.value"
                    :form-data="eventForm.data"
                    @change="(value) => {
                  eventForm.data.person.other_address = null;
                }"
                    @on-validate="validEventForm"
                />
              </div>
            </div>
          </form-section-field>

          <!-- -->
          <form-section-field
              v-if="editMode"
              :label="(editMode && !fullOtherAddress) ? 'Place of Death' : ''"
              :class="{ 'view-empty': !editMode && !fullOtherAddress, 'view-large': true}"
          >
            <span v-if="editMode && fullOtherAddress" class="mr-6, -ml-14">Other Address:&nbsp; </span>
             <div v-if="editMode" class="flex addFlex">
              <div v-if="editMode && fullOtherAddress" class="mr-4 addFlex">
                <input-field
                    v-if="editMode && fullOtherAddress"
                    class="bg-black"
                    v-model="fullOtherAddress"
                    :form-data="eventForm.data"
                    :disabled="true"
                />
              </div>
              <address-event-field
                  v-if="editMode"
                  :edit-mode="!!fullOtherAddress"
                  @save-address="
                    (addressData) => {
                      addAddressFor('person.other_address', addressData);
                    }
                  "
                  @remove-address="
                    () => {
                      eventForm.data.person.other_address = null;
                    }
                  "
                />
              </div>
          </form-section-field>
          <form-section-field
              v-if="!editMode"
              :label="(!editMode && fullOtherAddress) ? 'Place of Death' : ''"
              :class="{ 'view-empty': !editMode && !fullOtherAddress, 'view-large': true}"
          >
            <div v-if="!editMode" class="flex addFlex">
              <div v-if="!editMode && fullOtherAddress" class="mr-4 addFlex">
                <input-field
                    v-if="!editMode && fullOtherAddress"
                    class="bg-black"
                    v-model="fullOtherAddress"
                    :form-data="eventForm.data"
                    :disabled="true"
                />
              </div>
            </div>
          </form-section-field>
        </div>
      </form-section>
      <!--/ Deceased section -->

      <!-- Details section -->
      <form-section title="Details" v-if="editMode || !isEmptyDetailsSection">
        <!-- -->
        <div class="form-field-group">
          <form-section-field
            label="Funeral Director*:"
            :class="{
              'view-empty': !editMode && !eventForm.fields.detailsFuneralDirector.value,
            }"
          >
            <div class="w-3/5">
              <input-field
                class="input-booking"
                :class="{ 'view-mode': !editMode }"
                v-bind="eventForm.fields.detailsFuneralDirector"
                v-model="eventForm.fields.detailsFuneralDirector.value"
                :form-data="eventForm.data"
                :options="funeralDirectorOptions"
                :disabled="!editMode"
                @on-validate="validEventForm"
              />
            </div>
            <div class="w-1/6 ml-3">
              <i
                v-if="editMode"
                class="fa fa-edit cursor-pointer"
                @click="openEditFormModal('FuneralDirectorForm', 'Edit Funeral Director:', eventForm.fields.detailsFuneralDirector.value)"
              ></i>
              <span>&nbsp;&nbsp;</span>      
              <i
                v-if="editMode"
                class="fa fa-plus cursor-pointer"
                @click="openFormModal('FuneralDirectorForm', 'Add New Funeral Director:')"
              >
              </i>                                    
            </div>
          </form-section-field>
        </div>

        <!-- Grave group -->
        <div class="form-field-group">
          <!-- -->
          <form-section-field
            label="Grave:"
          >
           <span class="mr-1" v-if="editMode">Map Section: </span>
              <div class="inline-block w-1/12 mr-5">
                <input-field
                    v-if="editMode"
                class="input-booking"
                :class="{ 'view-mode': !editMode }"
                :placeholder="editMode ? 'Section' : ''"
                v-bind="eventForm.fields.detailsMapSection"
                v-model="eventForm.fields.detailsMapSection.value"
                :form-data="eventForm.data"
                :options="mapSectionOptions"
                :disabled="!editMode"
                @change="changeSelectedSection"
              />
              </div>

              <span v-if="editMode">New(open map): </span>
              <div v-if="editMode" class="inline-block w-10">
                <input
                    v-if="editMode"
                  type="checkbox"
                  v-bind="eventForm.fields.newBurialGrave"
                  v-model="eventForm.fields.newBurialGrave.value"
                  :false-value="null"
                  :true-value="true"
                  :checked="eventForm.fields.newBurialGrave.value === true"
                  :disabled="!editMode"
                  @change="openSiteMapForGrave"
                />
              </div>
              <span v-if="editMode">Existing(search map): </span>
              <div v-if="editMode" class="inline-block w-10">
                <input
                    v-if="editMode"
                  type="checkbox"
                  v-bind="eventForm.fields.newBurialGrave"
                  v-model="eventForm.fields.newBurialGrave.value"
                  :false-value="null"
                  :true-value="false"
                  :checked="eventForm.fields.newBurialGrave.value === false"
                  :disabled="!editMode"
                  @change="openSiteMapForGrave"
                />
              </div>
            <div class="inline-block w-1/4">
              <input-field
                class="input-booking makeBold"
                :class="{ 'view-mode': true }"
                v-bind="eventForm.fields.detailsGraveNumber"
                v-model="eventForm.fields.detailsGraveNumber.value"
                :form-data="eventForm.data"
                :disabled="!editMode || eventForm.fields.detailsGraveNumber.disabled"
                @on-validate="validEventForm"
              />
              <input-field
                  class="input-booking makeBold"
                  :class="{ 'view-mode': true }"
                  v-bind="eventForm.fields.detailsBurialUUID"
                  v-model="eventForm.fields.detailsBurialUUID.value"
                  :form-data="eventForm.data"
                  :disabled="true"
                  :hidden="true"
                  @on-validate="validEventForm"
              />
            </div>
            <div class="w-1/6 ml-3">
                <i
                  v-if="editMode && eventForm.fields.detailsGraveNumber"
                  class="fa fa-trash cursor-pointer"
                  @click="resetCurrentGraveNumber"
                />
            </div>
          </form-section-field>
        </div>

        <!-- Coffin -->
        <div class="form-field-group">
          <!-- -->
          <form-section-field
            label="Coffin Size:"
          >
            <div class="w-1/12 mr-2">
              <input-field
                class="input-booking"
                :class="{ 'view-mode': !editMode }"
                :placeholder="editMode ? '' : ''"
                v-bind="eventForm.fields.coffinSizeUnits"
                v-model="eventForm.fields.coffinSizeUnits.value"
                :form-data="eventForm.data"
                :disabled="!editMode"
                @on-validate="validEventForm"
              />
            </div>
            <div
              class="w-1/4 mr-2 flex justify-end"
            >
              <span class="inline-block mr-1">Length: </span>
              <div class="inline-block w-2/4">
                <input-field
                  class="input-booking"
                  :class="{ 'view-mode': !editMode }"
                  :disabled="!editMode"
                  v-bind="eventForm.fields.coffinSizeLength"
                  v-model="eventForm.fields.coffinSizeLength.value"
                  :form-data="eventForm.data"
                  @on-validate="validEventForm"
                />
              </div>
            </div>
            <div
              class="w-1/4 mr-2 flex justify-end"
            >
              <span class="inline-block mr-1">Width: </span>
              <div class="inline-block w-2/4">
                <input-field
                  class="input-booking"
                  :class="{ 'view-mode': !editMode }"
                  :disabled="!editMode"
                  v-bind="eventForm.fields.coffinSizeWidth"
                  v-model="eventForm.fields.coffinSizeWidth.value"
                  :form-data="eventForm.data"
                  @on-validate="validEventForm"
                />
              </div>
            </div>
            <div
              class="w-1/4 mr-2 flex justify-end"
            >
              <span class="inline-block mr-1">Height: </span>
              <div class="inline-block w-2/4">
                <input-field
                  class="input-booking"
                  :class="{ 'view-mode': !editMode }"
                  :disabled="!editMode"
                  v-bind="eventForm.fields.coffinSizeHeight"
                  v-model="eventForm.fields.coffinSizeHeight.value"
                  :form-data="eventForm.data"
                  @on-validate="validEventForm"
                />
              </div>
            </div>
          </form-section-field>
        </div>
        <div class="form-field-group">
          <!-- -->
          <form-section-field
            label="Comments:"
          >
            <input-field
            class="input-booking"
            :class="{ 'view-mode': !editMode }"
            :disabled="!editMode"
            v-bind="eventForm.fields.coffinComments"
            v-model="eventForm.fields.coffinComments.value"
            :placeholder="editMode ? 'Additional Coffin Comments' : ''"
            :form-data="eventForm.data"
            @on-validate="validEventForm"
          />
          </form-section-field>
        </div>
        <!-- Meeting location -->
        <div class="form-field-group">
          <!-- -->
          <form-section-field
            label="Meeting Location:"
          >
            <input-field
                class="input-booking"
                :class="{ 'view-mode': !editMode }"
                :placeholder="editMode ? 'Select Location' : ''"
                v-bind="eventForm.fields.meetingLocation"
                v-model="eventForm.fields.meetingLocation.value"
                :form-data="eventForm.data"
                :options="meetingLocationOptions"
                :disabled="!editMode"
                @on-validate="validEventForm"
              />
          </form-section-field>
        </div>
      </form-section>
      <!--/ Details section -->

      <!-- Next of Kin section -->
      <form-section title="Next of Kin" v-if="!editMode && isEmptyKinSection">
        <p><b>No next of kin recorded.</b></p>
        <p>&nbsp;</p><p>&nbsp;</p>
      </form-section>
      <form-section title="Next of Kin" v-if="editMode || !isEmptyKinSection">
        <!-- Name -->
        <div class="form-field-group">
          <!-- --->
          <form-section-field
            label="Title:"
          >
            <input-field
              class="input-booking"
              :class="{ 'view-mode': !editMode }"
              :disabled="!editMode"
              v-bind="eventForm.fields.kinTitle"
              v-model="eventForm.fields.kinTitle.value"
              :form-data="eventForm.data"
              @on-validate="validEventForm"
            />
          </form-section-field>

          <!-- --->
          <form-section-field
            label="First Name:"
          >
            <input-field
              class="input-booking"
              :class="{ 'view-mode': !editMode }"
              :placeholder="editMode ? 'First Name' : ''"
              :disabled="!editMode"
              v-bind="eventForm.fields.kinFirstName"
              v-model="eventForm.fields.kinFirstName.value"
              :form-data="eventForm.data"
              @on-validate="validEventForm"
            />
          </form-section-field>

          <!-- --->
          <form-section-field
            label="Last Name:"
          >
            <input-field
              class="input-booking"
              :class="{ 'view-mode': !editMode }"
              :placeholder="editMode ? 'Last Name' : ''"
              :disabled="!editMode"
              v-bind="eventForm.fields.kinLastName"
              v-model="eventForm.fields.kinLastName.value"
              :form-data="eventForm.data"
              @on-validate="validEventForm"
              @format="eventForm.fields.deceaseLastName.format"
            />
          </form-section-field>
        </div>

        <!-- Relation -->
        <div class="form-field-group">
          <!-- --->
          <form-section-field
            label="Relationship:"
          >
            <input-field
              class="input-booking"
              :class="{ 'view-mode': !editMode }"
              :placeholder="editMode ? 'Relationship' : ''"
              :disabled="!editMode"
              v-bind="eventForm.fields.kinRelationship"
              v-model="eventForm.fields.kinRelationship.value"
              :form-data="eventForm.data"
              @on-validate="validEventForm"
            />
          </form-section-field>
          <!-- -->
          <form-section-field
              label="Date of Birth:"
          >
            <input-field
                class="input-booking"
                :class="{ 'view-mode': !editMode }"
                :placeholder="editMode ? 'yyy-mm-dd' : ''"
                v-bind="eventForm.fields.kinDateOfBirth"
                v-model="eventForm.fields.kinDateOfBirth.value"
                :form-data="eventForm.data"
                :disabled="!editMode"
                @on-validate="validEventForm"
                @format="eventForm.fields.kinDateOfBirth.format"
            />
          </form-section-field>
        </div>

        <!-- Address -->
        <div class="form-field-group">
          <!-- --->
          <form-section-field
            label="Address:"
          >
            <div class="flex addFlex">
              <div v-show="!fullKinAddress && !editMode" class="mr-4 addFlex">
                <input-field :disabled="true" />
              </div>
              <div v-show="fullKinAddress" class="mr-4 addFlex">
                <input-field :placeholder="editMode ? 'Postcode' : ''" :disabled="true" v-model="fullKinAddress" />
              </div>
              <address-event-field
                v-if="editMode"
                :edit-mode="!!fullKinAddress"
                @save-address="
                  (addressData) => {
                    addAddressFor('next_of_kin_person.address', addressData);
                  }
                "
                @remove-address="
                  () => {
                    eventForm.data.next_of_kin_person.address = null;
                  }
                "
              />
            </div>
          </form-section-field>
        </div>
      </form-section>
      <!--/ Next of kin section -->

      <!-- Authority section -->
      <form-section title="Authority for Interment" v-if="!editMode && isEmptyAuthSection">
        <p><b>No authority for interment recorded.</b></p>
        <p>&nbsp;</p><p>&nbsp;</p><p>&nbsp;</p>
      </form-section>
      <form-section
        title="Authority for Interment"
        v-if="editMode || !isEmptyAuthSection"
      >
        <!-- Name -->
        <div class="form-field-group">
          <!-- --->
          <form-section-field
            label="Title:"
          >
            <input-field
              class="input-booking"
              :class="{ 'view-mode': !editMode }"
              :disabled="!editMode"
              v-bind="eventForm.fields.authTitle"
              v-model="eventForm.fields.authTitle.value"
              :form-data="eventForm.data"
              @on-validate="validEventForm"
            />
          </form-section-field>

          <!-- --->
          <form-section-field
            label="First Name:"
          >
            <input-field
              class="input-booking"
              :class="{ 'view-mode': !editMode }"
              :placeholder="editMode ? 'First Name' : ''"
              :disabled="!editMode"
              v-bind="eventForm.fields.authFirstName"
              v-model="eventForm.fields.authFirstName.value"
              :form-data="eventForm.data"
              @on-validate="validEventForm"
            />
          </form-section-field>

          <!-- --->
          <form-section-field
            label="Last Name:"
          >
            <input-field
              class="input-booking"
              :class="{ 'view-mode': !editMode }"
              :placeholder="editMode ? 'Last Name' : ''"
              :disabled="!editMode"
              v-bind="eventForm.fields.authLastName"
              v-model="eventForm.fields.authLastName.value"
              :form-data="eventForm.data"
              @on-validate="validEventForm"
              @format="eventForm.fields.deceaseLastName.format"
            />
          </form-section-field>
        </div>

        <!-- Role -->
        <div class="form-field-group">
          <!-- --->
          <form-section-field
            label="Role:"
          >
            <input-field
              class="input-booking"
              :class="{ 'view-mode': !editMode }"
              :placeholder="editMode ? 'Role' : ''"
              :disabled="!editMode"
              v-bind="eventForm.fields.authRole"
              v-model="eventForm.fields.authRole.value"
              :form-data="eventForm.data"
              @on-validate="validEventForm"
            />
          </form-section-field>
        </div>
      </form-section>
      <!--/ Authority section -->

      <!-- Comments section -->
      <form-section title="Comments" v-if="!editMode && isEmptyCommentsSection">
        <p><b>No comments recorded.</b></p>
        <p>&nbsp;</p><p>&nbsp;</p>
      </form-section>
      <form-section title="Comments" v-if="editMode || !isEmptyCommentsSection">
        <!-- -->
        <div class="form-field-group">
          <!-- --->
          <form-section-field>
            <input-field
              class="input-booking"
              :class="{ 'view-mode': !editMode }"
              :placeholder="editMode ? 'Additional Details' : ''"
              :disabled="!editMode"
              v-bind="eventForm.fields.comments"
              v-model="eventForm.fields.comments.value"
              :form-data="eventForm.data"
              @on-validate="validEventForm"
            />
          </form-section-field>
        </div>
      </form-section>
      <!--/ Comments section -->

      <!-- Status section -->
      <form-section title="Booking Status">
        <!-- -->
        <div class="form-field-group">
          <form-section-field>
            <div class="w-3/5">
              <input-field
                class="input-booking"
                :class="{ 'view-mode': !editMode }"
                :disabled="!editMode"
                v-bind="eventForm.fields.status"
                v-model="getbookingStatusChoices"
                :form-data="eventForm.data"
                @on-validate="validEventForm"
              />
            </div>
            <div class="w-1/6 ml-2">
              <i class="fas fa-arrow-alt-circle-right" @click="goToStatusPage"> </i>
            </div>
          </form-section-field>
        </div>
      </form-section>
      <!--/ Status section -->
    </div>
  </div>
  <notifications-list/>
</template>

<style scoped src="./new-event-form.css"></style>

<script src="./new-event-form.js"></script>
