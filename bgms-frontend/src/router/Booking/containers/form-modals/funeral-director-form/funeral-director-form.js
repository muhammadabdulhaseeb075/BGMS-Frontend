import { mapActions, mapMutations, mapGetters } from "vuex";

import InputField from "src/components/fields/input-field";
import FillButton from "src/components/fill-button";
import { createForm, matchForm } from "src/utils/forms";

import formSchema from "./funeral-director-form-schema";

const PUSH_DATA_EMIT = "push-data";
const CLOSE_EMIT = "close";

const components = {
    InputField,
    FillButton,
};

function data() {    
    return  {                           
        isEditing: false,        
        form: createForm(formSchema),                
    };
}

const methods = {
    ...mapActions("booking", ["submitNewFuneralDirector", "updateFuneralDirector"]),    
    ...mapMutations(["addOneFuneralDirector", "updateOneFuneralDirector"]),
    ...mapGetters(["currentSite", "funeralDirectors", "getFuneralDirectorById", "currentSiteId"]),

    async onSubmitForm() {
        /* Create or Update a Funeral Director. If the ID is set then it updates via PATCH. If ID id empty then creates via POST.
        */
        
        var update_id = this.form.data.id;
        //var update_id = this.$attrs['data_id']; //a;ternate way to get id
        if(update_id != null && update_id.length != 0){ //if the id is already set then we are editing an existing Official
            try {
                const updatedDirector = await this.updateFuneralDirector({'update_id':update_id, 'data':this.form.data}); //the id is redundant but clear
                console.log("Update RESPONSE ", updatedDirector)
                this.updateOneFuneralDirector(updatedDirector);
                this.$emit(PUSH_DATA_EMIT, updatedDirector);
            } catch(error) {
                console.error("Error updating existing funeral director: ", error);
            }    
        }
        else{ //we are creating a new official
            try {
                const newDirector = await this.submitNewFuneralDirector(this.form.data);
                console.log("Create RESPONSE ", newDirector)
                this.addOneFuneralDirector(newDirector);
                this.$emit(PUSH_DATA_EMIT, newDirector);
            } catch(error) {
                console.error("Error creating new funeral director: ", error);
            }
        }        
        //this.$emit(PUSH_DATA_EMIT); //redunsant? there are two calls back to event form and second may not be needed
        
        this.$emit(CLOSE_EMIT); //assume something was updated but close anyway 
    },

    onClose() {
        this.$emit(CLOSE_EMIT);
    }
}

export default {
    name: "funeral-director-form",
    data,
    emits: [PUSH_DATA_EMIT, CLOSE_EMIT],
    components,
    methods,
    mounted() {        
        var data_id = this.$attrs['data_id']
        if(data_id.length != 0){ //Funeral Director ID has been passed in so editing                        
            //console.log("Director uid passed. " + data_id);            
            console.log(this.$store.getters.getFuneralDirectorById(data_id));
            this.form = matchForm(formSchema, this.$store.getters.getFuneralDirectorById(data_id));
        }
     },
};
