/*  ____________________________________
 * |    _   _             _ _           |
 * |   | |_(_)   _ __ _ _(_) |_ ____    |
 * |   | __| |\ / /_ \ '_| | __|_  /    |
 * |   | |_| | ' / __/ | | | |__/ /_    |
 * |    \__|_|\_/\___|_| |_|\__/___/    |
 * |____________________________________|
 *
 * 1.  Render Viewer
 * 2.  Viewer Actions
 */

/* ----------------------------------------------------------------------------
 *    1. Render Viewer
 * ------------------------------------------------------------------------- */
function getStepAndRender(step_uri_id, ref_id) {
    url = URL_VIEWER_ACTION + step_uri_id + '/' + ref_id + '/'
    fetch(url, {
        method: 'GET',
        headers: {
            'contentType' : 'application/json; charset=UTF-8'},
    })
        .then(response => {
            if (response.status >= 200 && response.status < 300) {
                return response.text();
            } else {
                throw Error(response.statusText);
            }
        })
        .then(html => {
            /* document.querySelector('#preview').innerHTML = jsonResponse.data*/
            document.querySelector('#preview').innerHTML = html
        }
    )
}

/* ----------------------------------------------------------------------------
 *    2. Viewer Actions
 * ------------------------------------------------------------------------- */

function viewerActionPrevious(previous_uri_id, previous_ref) {
    getStepAndRender(previous_uri_id, previous_ref)
}

function viewerActionNext(next_uri_id, next_ref) {
    getStepAndRender(next_uri_id, next_ref)   
}

function viewerActionGoTo(step_uri_id, step_ref) {
    getStepAndRender(step_uri_id, step_ref)
}

function renderViewer() {
    fetch(URL_VIEWER_HOWTO_DATA, {
        method: 'GET',
        headers: {
            'contentType' : 'application/json; charset=UTF-8'},
    })
        .then(response => {
            if (response.status >= 200 && response.status < 300) {
                return response.json();
            } else {
                throw Error(response.statusText);
            }
        })
        .then(jsonResponse => {
            first_uri_id = jsonResponse['howto']['first']
            first_ref = jsonResponse['howto']['first_ref']
            getStepAndRender(first_uri_id, first_ref)
        }
    )
}
