import axios from 'axios';

const token = (<HTMLInputElement>document.getElementsByName("csrfmiddlewaretoken")[0]).value;

axios.defaults.headers.post['X-CSRFToken'] = token;
axios.defaults.headers.put['X-CSRFToken'] = token;
axios.defaults.headers.delete['X-CSRFToken'] = token;
axios.defaults.headers.patch['X-CSRFToken'] = token;

function urlQueries(queries): string {
    let result = '';

    for(const query in queries) {
        const value = queries[query];
        result += `${query}=${value}&`;
    }

    return result;
}

class Http {
    static get(
        url: string,
        queries: object = {}
    ): Promise<object | string> {
        const parsedQueries = urlQueries(queries);
        const finalUrl = parsedQueries
        ? `${url}?${parsedQueries}`
        : url;

        return  axios.get(finalUrl);
    }

    static post(
        url: string,
        payload: object,
        queries?: object
    ): Promise<object | string> {
        let finalUrl = url;

        if (queries) {
            const parsedQueries = urlQueries(queries);
            finalUrl = parsedQueries
                ? `${url}?${parsedQueries}`
                : url;
        }

        return axios.post(finalUrl, payload);
    }

    static put(
        url: string,
        payload: object,
        queries?: object
    ): Promise<object | string> {
        let finalUrl = url;

        if(queries) {
            const parsedQueries = urlQueries(queries);
            finalUrl = parsedQueries
                ? `${url}?${parsedQueries}`
                : url; 
        }

        return axios.put(finalUrl, payload);
    }
}

export default Http;
