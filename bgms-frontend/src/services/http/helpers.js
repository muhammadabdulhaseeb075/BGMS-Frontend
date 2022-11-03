
/**
 * Become an object into a query url
 * i.e. {q1: "test-1", q2: "test-2"} => "q1=test-1&q2=test-2"
 * 
 * @param {Object} queries
 * @return {String} URL queries format
 */
export function urlQueries(queries) {
    let result = "";

    for (const query in queries) {
        const value = queries[query];
        result += `${query}=${value}&`;
    }

    return result;
}
