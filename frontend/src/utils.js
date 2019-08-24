/***
 * Raises non-200 responses as errors, mostly so they can be handled by catch().
 * If no error occurred, the response is passed along as-is.
 * @param response the server's (possibly) failure response
 * @returns {{ok}|*} the original response if no error occurred
 */

export function handleErrors(response) {
    if (!response.ok && response.error) {
        console.warn("Failed: ", response);
        throw response;
    }
    return response;
}
