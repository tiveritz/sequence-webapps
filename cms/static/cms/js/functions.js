/*  ____________________________________
 * |    _   _             _ _           |
 * |   | |_(_)   _ __ _ _(_) |_ ____    |
 * |   | __| |\ / /_ \ '_| | __|_  /    |
 * |   | |_| | ' / __/ | | | |__/ /_    |
 * |    \__|_|\_/\___|_| |_|\__/___/    |
 * |____________________________________|
 *
 * 1.  List Boxes
 * 2.  Mobile Menu Button
 * 
 */

/* ----------------------------------------------------------------------------
 *    1. List Boxes
 * ------------------------------------------------------------------------- */
function showChangeBox(changeBoxId) {
    selectedBox = document.querySelector('#' + changeBoxId);
    
    elements = document.querySelectorAll('.change-box');
    for (i = 0; i < elements.length; i++) {
        if (elements[i] == selectedBox) {
            selectedBox.classList.toggle('change-box-active');
        } else {
            elements[i].classList.remove('change-box-active');
        }
    }
}

function showEditBox(editBoxId) {
    selectedBox = document.querySelector('#change-box-' + editBoxId);
    selectedBox.classList.toggle('edit-box-active');
}


/* ----------------------------------------------------------------------------
 *    2.  Mobile Menu Button
 * ------------------------------------------------------------------------- */
document.querySelector('#toggle-menu-button').addEventListener('click', toggleMobileMenu);

function toggleMobileMenu() {
	document.querySelector('#menu').classList.toggle('active');
	document.querySelector('#toggle-menu-button').classList.toggle('menu-active');
};