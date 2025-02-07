/**
 * @typedef {Object} ResponseWrapper
 *
 * @property {boolean} success - Whether the request was successful.
 * @property {any} payload - The payload returned from the API.
 * @property {any} error - The error returned from the API.
 * @property {string | null} errorMessage - The error message returned from the API.
 * @property {Response | null} response - The response from the API.
 */

/**
 * Wrap a response from an API call into a standard format.
 *
 * @param {Promise<Response>} promise - The promise to wrap.
 * @returns {Promise<ResponseWrapper>}
 */
const wrapResponse = async (promise) => {
    const returnValue = {
        success: false,
        payload: null,
        error: null,
        errorMessage: null,
        response: null,
    };

    try {
        const response = await promise;
        returnValue.response = response;
        const json = await response.json();

        if (!json.success) {
            returnValue.error = json.error;
            returnValue.errorMessage = json.error.message;
        } else {
            returnValue.payload = json.payload;
            returnValue.success = true;
        }
    } catch (error) {
        returnValue.success = false;
        returnValue.error = error;
    }

    if (returnValue.error) {
        console.error(returnValue.error);
    }

    return returnValue;
};

export { wrapResponse };
