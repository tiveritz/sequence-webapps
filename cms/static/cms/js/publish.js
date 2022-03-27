/*  ____________________________________
 * |    _   _             _ _           |
 * |   | |_(_)   _ __ _ _(_) |_ ____    |
 * |   | __| |\ / /_ \ '_| | __|_  /    |
 * |   | |_| | ' / __/ | | | |__/ /_    |
 * |    \__|_|\_/\___|_| |_|\__/___/    |
 * |____________________________________|
 *
 * 1.  Publish
 * 2.  Publish buttons
 */

/* ----------------------------------------------------------------------------
 *    1. Publish
 * ------------------------------------------------------------------------- */

function publishSequence(api_id, spaces, reloadRequired) {
    fetch(URL_PUBLISH_SEQUENCE, {
        method: 'POST',
        headers: {
            'X-CSRFToken' : csrftoken, // for Django
            'contentType' : 'application/json; charset=UTF-8'},
        body: JSON.stringify({spaces: spaces})
    })
        .then(response => {
            if (response.status >= 200 && response.status < 300) {
                return response.json();
            } else {
                throw Error(response.statusText);
            }
        })
        .then(jsonResponse => {
            if (reloadRequired) {
                location.reload()
            } else {
                renderViewer()
            }
        }
    )
}



/* ----------------------------------------------------------------------------
 *    2. Publish buttons
 * ------------------------------------------------------------------------- */

function publishSequenceForUser(api_id) {
    publishSequence(api_id, ['public'], true)
}

function publishSequenceForPreview(api_id) {
    publishSequence(api_id, ['preview'], false)
}
