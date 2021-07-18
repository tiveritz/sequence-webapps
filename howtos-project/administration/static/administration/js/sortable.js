/*  ____________________________________
 * |    _   _             _ _           |
 * |   | |_(_)   _ __ _ _(_) |_ ____    |
 * |   | __| |\ / /_ \ '_| | __|_  /    |
 * |   | |_| | ' / __/ | | | |__/ /_    |
 * |    \__|_|\_/\___|_| |_|\__/___/    |
 * |____________________________________|
 *
 * 1.  Sortable
 * 2.  Messages
 * 3.  CSRF Token
 */

/* ----------------------------------------------------------------------------
 *    1. Sortable
 * ------------------------------------------------------------------------- */
new Sortable.create(sortable, {
    animation: 150,
    ghostClass: 'hovering-background-class',
    handle: '.sortable-drag',
    onUpdate: function (/**Event*/evt) {
        updateDatabase(URL_SAVE_STEP_ORDER, evt.oldIndex, evt.newIndex)
        updateDomOrder(evt.to.children)
        updateInnerHtmlPosition(evt.to.children)
    },
})

new Sortable.create(sortablee, {
    animation: 150,
    ghostClass: 'hovering-background-class',
    handle: '.sortable-drag',
    onUpdate: function (/**Event*/evt) {
        updateDatabase(URL_SAVE_EXPLANATION_ORDER, evt.oldIndex, evt.newIndex)
        updateDomOrder(evt.to.children)
    },
})

function updateDomOrder(elements) {
    newIndexes = getIdList(elements)
    for (i = 0; i < elements.length; i++) {
        elements[i].id = newIndexes[i]
    }
}

function updateInnerHtmlPosition(elements) {
    for (i = 0; i < elements.length; i++) {
        var position = elements[i].querySelector('.sortable-position')
        position.innerHTML = i+1
    }
}

function getIdList(newIndexes) {
    var items = []
        for (i = 0; i < newIndexes.length; i++) {
            items.push(newIndexes[i].id)
        };
        return items;
};

function updateDatabase(url, oldIndex, newIndex) {
    fetch(url, {
        method: 'POST',
        body : JSON.stringify({'old_index': oldIndex, 'new_index' : newIndex}),
        headers: {
            'X-CSRFToken' : csrftoken, // for Django
            'contentType' : 'application/json; charset=UTF-8'}
        })
        .then(response => {
            if (response.status >= 200 && response.status < 300) {
                return response.json();
            } else {
                throw Error(response.statusText);
            }
        })
        .then(jsonResponse => {
            console.log(jsonResponse)
        }
    )
}


/* ----------------------------------------------------------------------------
 *    2. Message
 * ------------------------------------------------------------------------- */
var msgID = 0

function displayMessage(message) {
    siteMessage = document.getElementById('site-message')
    var msg = document.createElement('div')
    var id = 'site-message-'+ msgID
    msg.id = id
    msg.className = 'message'
    msg.innerHTML = message
    siteMessage.appendChild(msg)
    msgID++
    msgElement = document.getElementById(id)
    removeMessage(msgElement)
}

function removeMessage(msgElement) {
    msgElement.classList.add('message-active')
    setTimeout(function(){ msgElement.classList.remove('message-active') }, 3000)
    setTimeout(function(){ msgElement.remove() }, 4000)
}

/* ----------------------------------------------------------------------------
 *    3. CSRF Token
 * ------------------------------------------------------------------------- */

var csrftoken = getCookie('csrftoken')

// get csrf information for Django
function getCookie(name) {
    let cookieValue = null
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';')
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim()
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
                break
            }
        }
    }
    return cookieValue
}
