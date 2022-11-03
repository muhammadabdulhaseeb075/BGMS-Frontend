<template>
  <div>
    <v-row>
      <v-col cols="12" sm="2" class="py-4">
        <h3>Name</h3>
      </v-col>
      <v-col v-if="!recordIsCompany" cols="12" sm="10" class="py-0">
        <v-row>
          <v-col cols="12" sm="2" class="py-1">
            <v-text-field
              v-model="personOrCompany['title']"
              label="Title"
              :disabled="readonly || readonlyEssential"
            ></v-text-field>
          </v-col>
          <v-col cols="12" sm="5" class="py-1">
            <v-text-field
              v-model="personOrCompany['first_names']"
              label="First Names*"
              :disabled="readonly || readonlyEssential"
              :rules="[() => !!personOrCompany['first_names'] || 'This field is required']"
            ></v-text-field>
          </v-col>
          <v-col cols="12" sm="5" class="py-1">
            <v-text-field
              v-model="personOrCompany['last_name']"
              label="Last Name*"
              required
              :disabled="readonly || readonlyEssential"
              :rules="[() => !!personOrCompany['last_name'] || 'This field is required']"
            ></v-text-field>
          </v-col>
        </v-row>
      </v-col>
      <v-col v-else cols="12" sm="10" class="py-0">
        <v-row>
          <v-col cols="12" class="py-1">
            <v-text-field
              v-model="personOrCompany['name']"
              label="Name*"
              :disabled="readonly || readonlyEssential"
              :rules="[() => !!personOrCompany['name'] || 'This field is required']"
            ></v-text-field>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
    
    <v-row v-if="recordIsCompany">
      <v-col cols="12" sm="2" class="py-4">
        <h3>Contact Name</h3>
      </v-col>
      <v-col cols="12" sm="10" class="py-0">
        <v-row>
          <v-col cols="12" class="py-1">
            <v-text-field
              v-model="personOrCompany['contact_name']"
              label="Contact Name*"
              :disabled="readonly || readonlyEssential"
              :rules="[() => !!personOrCompany['contact_name'] || 'This field is required']"
            ></v-text-field>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
    
    <v-row>
      <v-col cols="12" sm="2" class="py-4">
        <h3>Email</h3>
      </v-col>
      <v-col cols="12" sm="10" class="py-0">
        <v-row>
          <v-col cols="12" class="py-1">
            <v-text-field
              ref="email"
              v-model="personOrCompany['email']"
              label="Email Address"
              type="email"
              prepend-icon="fa-envelope"
              :disabled="readonly"
              :rules="[() => (!personOrCompany['email'] || validateEmail(personOrCompany['email'])) || 'Invalid email address']"
            ></v-text-field>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
    
    <v-row>
      <v-col cols="12" sm="2" class="py-4">
        <h3>Phone</h3>
      </v-col>
      <v-col cols="12" sm="10" class="py-0">
        <v-row>
          <v-col cols="12" sm="6" class="py-1">
            <v-text-field
              v-model="personOrCompany['phone_number']"
              label="Phone Number 1"
              maxlength="20"
              :disabled="readonly"
            ></v-text-field>
          </v-col>
          <v-col cols="12" sm="6" class="py-1">
            <v-text-field
              v-model="personOrCompany['phone_number_2']"
              label="Phone Number 2"
              maxlength="20"
              :disabled="readonly"
            ></v-text-field>
          </v-col>
        </v-row>
      </v-col>
    </v-row>

    <v-row v-if="address && (!readonlyEssential || address['display_address'])">
      <v-col cols="12" sm="2" class="py-4">
        <h3>Address</h3>
      </v-col>
      <v-col cols="12" sm="10" class="py-4 pl-6" v-if="address['display_address']">
        <v-row>
          {{ address['display_address'] }}
        </v-row>
      </v-col>
      <v-col cols="12" sm="10" class="py-0" v-else>
        <v-row>
          <v-col cols="12" class="py-1">
            <v-text-field
              v-model="address['first_line']"
              label="First Line"
              maxlength="200"
              :disabled="readonly">
            </v-text-field>
          </v-col>
          <v-col cols="12" class="py-1">
            <v-text-field
              v-model="address['second_line']"
              label="Second Line"
              maxlength="200"
              :disabled="readonly">
            </v-text-field>
          </v-col>
          <v-col cols="12" sm="6" class="py-1">
            <v-text-field
              v-model="address['town']"
              label="Town"
              maxlength="50"
              :disabled="readonly">
            </v-text-field>
          </v-col>
          <v-col cols="12" sm="6" class="py-1">
            <v-text-field
              v-model="address['county']"
              label="County"
              maxlength="50"
              :disabled="readonly">
            </v-text-field>
          </v-col>
          <v-col cols="12" sm="6" class="py-1">
            <v-text-field
              v-model="address['postcode']"
              label="Post Code"
              maxlength="10"
              :disabled="readonly">
            </v-text-field>
          </v-col>
          <v-col cols="12" sm="6" class="py-1">
            <v-text-field
              v-model="address['country']"
              label="Country"
              maxlength="50"
              :disabled="readonly">
            </v-text-field>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue';
import Component from 'vue-class-component';
import { Prop } from 'vue-property-decorator';
import { validateEmailAddress } from '@/global-static/dataFormattingAndValidation.ts';

@Component
export default class PersonCompanyForm extends Vue {

  @Prop() personOrCompany;
  @Prop() address;
  @Prop() readonly;
  @Prop() readonlyEssential;
  @Prop() recordIsCompany

  /*** Lifecycle hooks ***/

  /*** Getters and setters ***/

  /*** Methods ***/
  
  /**
   * Validate email address
   */
  validateEmail(email): boolean {
    // only validate when email is not selected
    if (this.$refs.email && (this.$refs.email as any).isFocused)
      return true;

    return validateEmailAddress(email);
  }

}
</script>