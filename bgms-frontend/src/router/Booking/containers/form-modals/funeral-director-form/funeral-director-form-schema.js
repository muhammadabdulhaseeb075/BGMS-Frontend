
export default {    
    companyName: {
        id: "companyName",
        name: "company_name",
        type: "text",
        defaultValue: "",
        placeholder: "Company Name",
    },
    contact: {
        id: "title",
        name:"title",
        type: "select",
        placeholder: "Title",
        options: [
            { label: "Mr", value: "1" },
            { label: "Mrs", value: "2" },
            { label: "Miss", value: "3" },
            { label: "Ms", value: "4" },
        ],
    },
    firstname: {
        id: "firstname",
        name: "first_names",
        type: "text",
        placeholder: "First Name",
    },
    lastname: {
        id: "lastname",
        name: "last_name",
        type: "text",
        placeholder: "Last Name",
      format(value, resolve) {
        resolve(value.toUpperCase());
      },
    },
    jobTitle: {
        id: "jobTitle",
        name: "job_title",
        type: "text",
        placeholder: "Job Title",
    },
    email: {
        id: "email",
        name: "email",
        defaultValue: "",
        type: "text",
        placeholder: "Email",
    },
    phone1: {
        id: "phone1",
        name: "phone_number",
        type: "text",
        placeholder: "Phone 1",
    },
    phone2: {
        id: "phone2",
        name: "second_phone_number",
        type: "text",
        placeholder: "Phone 2",
    },
    firstLine: {
        id: "firstLine",
        name: "address.first_line",
        type: "text",
        placeholder: "First Line",
    },
    secondLine: {
        id: "secondLine",
        name: "address.second_line",
        type: "text",
        placeholder: "Second Line",
    },
    town: {
        id: "town",
        name: "address.town",
        type: "text",
        placeholder: "Town",
    },
    county: {
        id: "county",
        name: "address.county",
        type: "text",
        placeholder: "County",
    },
    postcode: {
        id: "postcode",
        name: "address.postcode",
        defaultValue: "",
        type: "text",
        placeholder: "Postcode",
    },
    /*postcode2: {
        id: "postcode2",
        type: "text",
        placeholder: "Postcode",
    },*/
    country: {
        id: "country",
        name: "address.country",
        type: "text",
        placeholder: "Country",
    },
    id: {
        id: "id",
        name: "id",
        type: "hidden",        
    },
};
