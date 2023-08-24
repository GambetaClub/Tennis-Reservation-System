// JavaScript to redirect when a row is clicked
document.addEventListener('DOMContentLoaded', function () {
	const rows = document.querySelectorAll('.clickable-row')
	rows.forEach(function (row) {
		row.addEventListener('click', function () {
			const href = row.getAttribute('data-href')
			if (href) {
				window.location.href = href
			}
		})
	})
})

$(document).ready(function () {
	$('.form-error').parent().find('input, select').addClass('is-invalid')
})
