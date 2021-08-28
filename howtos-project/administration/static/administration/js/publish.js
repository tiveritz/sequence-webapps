/*  ____________________________________
 * |    _   _             _ _           |
 * |   | |_(_)   _ __ _ _(_) |_ ____    |
 * |   | __| |\ / /_ \ '_| | __|_  /    |
 * |   | |_| | ' / __/ | | | |__/ /_    |
 * |    \__|_|\_/\___|_| |_|\__/___/    |
 * |____________________________________|
 *
 * 1.  Publish
 * 2.  Preview
 */

/* ----------------------------------------------------------------------------
 *    1. Publish
 * ------------------------------------------------------------------------- */

function publishHowTo(uri_id) {
    fetch(URL_PUBLISH_HOWTO, {
        method: 'POST',
        headers: {
            'X-CSRFToken' : csrftoken, // for Django
            'contentType' : 'application/json; charset=UTF-8'},
        body: JSON.stringify({spaces: ['public']})
    })
        .then(response => {
            if (response.status >= 200 && response.status < 300) {
                return response.json();
            } else {
                throw Error(response.statusText);
            }
        })
        .then(jsonResponse => {
            location.reload()
        }
    )
}

/* ----------------------------------------------------------------------------
 *    1. Publish
 * ------------------------------------------------------------------------- */

function previewHowTo(uri_id) {
    fetch(URL_PUBLISH_HOWTO, {
            method: 'POST',
            headers: {
                'X-CSRFToken' : csrftoken, // for Django
                'contentType' : 'application/json; charset=UTF-8'},
            body: JSON.stringify({spaces: ['preview']})
        })
        .then(response => {
            if (response.status >= 200 && response.status < 300) {
                return response.json();
            } else {
                throw Error(response.statusText);
            }
        })
        .then(jsonResponse => {
            location.reload()
        }
    )
}
