let cachedToken = null;

/**
 * Get a CSRF token.
 *
 * @returns {string} The CSRF token.
 */
const getCsrfToken = () => {
    if (cachedToken) {
        return cachedToken;
    }

    cachedToken = document.querySelector('[name="csrfmiddlewaretoken"]').value;

    return cachedToken;
};

export { getCsrfToken };
