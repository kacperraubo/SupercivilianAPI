let cachedToken = null;

/**
 * Get a CSRF token.
 */
const getCsrfToken = () => {
    if (cachedToken) {
        return cachedToken;
    }

    cachedToken = document.querySelector('[name="csrfmiddlewaretoken"]').value;

    return cachedToken;
};

export { getCsrfToken };
