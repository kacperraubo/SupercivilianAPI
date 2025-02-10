/**
 * Convert an object into a FormData object.
 *
 * @param {Object} data - The object to convert.
 */
const formData = ({ ...data }) => {
    const formData = new FormData();

    for (const [key, value] of Object.entries(data)) {
        formData.append(key, value);
    }

    return formData;
};

/**
 * Convert an object into a JSON string.
 *
 * @param {Object} data - The object to convert.
 */
const json = (data) => {
    return JSON.stringify(data);
};

export { formData, json };
