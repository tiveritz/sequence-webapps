
// Change Box
function showChangeBox(changeBoxId) {
	
	console.log(changeBoxId);
	selectedBox = document.querySelector('#' + changeBoxId);
	
	console.log(selectedBox);
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
