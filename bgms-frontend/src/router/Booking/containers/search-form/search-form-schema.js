
export default {
    deceasedFirstName: {
        id: "deceasedFirstName",
        name: "name",
        placeholder: "First Names",
        type: "text",
    },
    deceasedLastName: {
        id: "deceasedLastName",
        name: "last_name",
        placeholder: "Last Name",
        type: "text",
        format(value, resolve) {
            resolve(value.toUpperCase());
        },
    },
    dateFrom: {
        id: "dateFrom",
        name: "date.from",
        placeholder: "Date(from)",
        type: "date",
        format(value, resolve) {
            resolve(new Intl.DateTimeFormat("default", {dateStyle: "long"}).format(new Date(value)));
        },
    },
    dateTo: {
        id: "dateTo",
        name: "date.to",
        placeholder: "Date(to)",
        type: "date",
        format:"dd-MM-YYYY",
    },
    site: {
        id: "site",
        name: "site",
        placeholder: "Burial Ground Site",
        type: "multiselect",
    },
    funeralDirector: {
        id: "funeralDirector",
        name: "funeral_director_id",
        placeholder: "All Funeral Directors",
        type: "multiselect",
    },
    type: {
        id: "type",
        name: "cremated",
        options: [
            { value: "ashes", label: "Ashes" },
            { value: "burial", label: "Burial" },
        ],
        placeholder: "Type options",
        type: "multiselect",
    },
    status: {
        id: "status",
        name: "status",
        options: [
            { value: 2, label: "Pre-Burial Checks" },
            { value: 3, label: "Awaiting-Burial" },
            { value: 4, label: "Post-Burial Checks" },
            { value: 5, label: "Completed" },
            { value: 7, label: "Cancelled" },
        ],
        placeholder: "Status options",
        type: "multiselect",
    },
};


    /*
    reference: {
        id: "reference",
        name: "reference",
        placeholder: "Reference",
        type: "text",
    },*/