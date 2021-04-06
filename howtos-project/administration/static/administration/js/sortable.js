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
    handle: ".sortable-drag",
    onUpdate: function (/**Event*/evt) {
        updateDatabase(evt.oldIndex, evt.newIndex);
        updateDomOrder(evt.to.children);
        updateInnerHtmlPosition(evt.to.children);
    },
});

function updateDomOrder(elements) {
    newIndexes = getIdList(elements);
    for (i = 0; i < elements.length; i++) {
        elements[i].id = newIndexes[i];
    }
}

function updateInnerHtmlPosition(elements) {
    for (i = 0; i < elements.length; i++) {
        var position = elements[i].querySelector('.sortable-position');
        position.innerHTML = i+1;
    }
}

function getIdList(newIndexes) {
    var items = [];
        for (i = 0; i < newIndexes.length; i++) {
            items.push(newIndexes[i].id);
        };
        return items;
};

function updateDatabase(oldIndex, newIndex) {
    var xhttp = new XMLHttpRequest();
    var url = UPDATE_DATABASE_URL; // from Django (see html template)
    var data = JSON.stringify({'old_index': oldIndex, 'new_index' : newIndex} );
    xhttp.open('POST', url, true);

    xhttp.setRequestHeader('X-CSRFToken', csrftoken); // for Django
    xhttp.setRequestHeader('contentType', 'application/json');

    xhttp.onreadystatechange = function () {
        if(xhttp.readyState == 4 && xhttp.status == 200) {
            var response = JSON.parse(xhttp.responseText);
            var message = response.message;
            /* displayMessage(message); */
        };
    };
    xhttp.send(data);
};


/* ----------------------------------------------------------------------------
 *    2. Message
 * ------------------------------------------------------------------------- */
var msgID = 0;

function displayMessage(message) {
    siteMessage = document.getElementById('site-message');
    var msg = document.createElement('div');
    var id = 'site-message-'+ msgID;
    msg.id = id;
    msg.className = 'message';
    msg.innerHTML = message;
    siteMessage.appendChild(msg);
    msgID++;
    msgElement = document.getElementById(id);
    removeMessage(msgElement);
};

function removeMessage(msgElement) {
    msgElement.classList.add("message-active");
    setTimeout(function(){ msgElement.classList.remove("message-active"); }, 3000);
    setTimeout(function(){ msgElement.remove(); }, 4000);
};

/* ----------------------------------------------------------------------------
 *    3. CSRF Token
 * ------------------------------------------------------------------------- */

var csrftoken = getCookie('csrftoken');

// get csrf information for Django
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};
