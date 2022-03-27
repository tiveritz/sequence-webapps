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
function getStepAndRender(step_api_id) {
    url = URL_VIEWER_ACTION + step_api_id + '/'
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

function viewerActionPrevious(previous_api_id) {
    getStepAndRender(previous_api_id)
}

function viewerActionNext(next_api_id) {
    getStepAndRender(next_api_id)   
}

function viewerActionGoTo(step_api_id) {
    getStepAndRender(step_api_id)
}

function renderViewer() {
    fetch(URL_VIEWER_SEQUENCE_DATA, {
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
            first_api_id = jsonResponse['sequence']['first']
            getStepAndRender(first_api_id)
        }
    )
}
