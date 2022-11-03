<template>
    <div>
           <v-row align="center">
            <v-col cols="12" sm="2">
                Type*
            </v-col>
             <v-col cols="12" sm="10">
                  <v-radio-group v-model="value" :column="false">
                      <v-radio
                        label="Ashes"
                        :value="this.ashes"
                        hide-details
                      ></v-radio>
                      <v-radio
                         label="Burial"
                         :value="this.burial"
                         class="ml-12"
                         hide-details
                      ></v-radio>
                   </v-radio-group>
            </v-col>
            <v-col sm="12" class="pa-0">
               <v-divider style="background-color: #c3af42"/>
           </v-col>
    </v-row>
    </div>
</template>

<script lang='ts'>

const ASHES = 0;
const BURIAL = 1;

export default {
    props: {
        burialType: {
            default: ASHES
        }
    },
    data: () => ({
        ashes: ASHES,
        burial: BURIAL
    }),
    computed: {
        value: {
          get() {
            return this.burialType;
          },
          set(burialTypeChanged) {
           this.$emit('input', burialTypeChanged)
          }
        }
  },
    methods: {
        isAshes: () => {
            return this.value === "Ashes";
        },
        isBurial: () => {
            return this.value === "Burial"
        }
    },
}
</script>