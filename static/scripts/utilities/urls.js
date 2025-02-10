/**
 * Add parameters to a URL.
 *
 * @param {string} url - The URL to add parameters to.
 * @param {Object} params - The parameters to add.
 * @param {boolean} [excludeUndefined=true] - Whether to exclude undefined parameters.
 */
const urlWithParams = (url, params, excludeUndefined = true) => {
    if (excludeUndefined) {
        params = Object.fromEntries(
            Object.entries(params).filter(([_, value]) => value !== undefined),
        );
    }

    if (Object.keys(params).length === 0) {
        return url;
    }

    return url + '?' + new URLSearchParams(params).toString();
};

export { urlWithParams };
