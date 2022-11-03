import axios from "axios";

import { urlQueries } from "./helpers";
import setup from "./setup";

class Http {
    static get(
        url,
        queries = {}
    ) {
        const finalUrl = Http.addQueries(url, queries);

        return axios.get(finalUrl);
    }

    static post(
        url,
        payload,
        queries = {},
    ) {
        const finalUrl = Http.addQueries(url, queries);

        return axios.post(finalUrl, payload);
    }

    static put(
        url,
        payload,
        queries = {},
    ) {
        const finalUrl = Http.addQueries(url, queries);

        return axios.put(finalUrl, payload);
    }

    static patch(
        url,
        payload,
        queries = {},
    ) {
        const finalUrl = Http.addQueries(url, queries);
        console.log("PAYLOAD: ", payload);
        return axios.patch(finalUrl, payload);
    }

    static addQueries(url, queries) {
        let finalUrl = url; 

        if (queries) {
            const parsedQueries = urlQueries(queries);
            finalUrl = parsedQueries
                ? `${url}?${parsedQueries}`
                : url;
        }

        return finalUrl;
    }
}

export default Http;
export {
    setup,
};
