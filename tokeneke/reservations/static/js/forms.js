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

document.addEventListener('DOMContentLoaded', function () {
	// Handle the click event for the "Delete Activity" button
	const deleteActivityButton = document.getElementById('delete-activity')
	deleteActivityButton.addEventListener('click', function () {
		const csrfToken = $('input[name=csrfmiddlewaretoken]').val()
		// Use SweetAlert to confirm the deletion
		Swal.fire({
			title: 'Are you sure?',
			text: "You won't be able to revert this!",
			icon: 'warning',
			showCancelButton: true,
			confirmButtonColor: '#3085d6',
			cancelButtonColor: '#d33',
			confirmButtonText: 'Yes, delete it!',
		}).then((result) => {
			if (result.isConfirmed) {
				// Send a DELETE request to delete the activity
				fetch(editActivityURL, {
					method: 'DELETE',
					headers: {
						'X-CSRFToken': csrfToken, // Include the CSRF token
					},
				}).then((response) => {
					if (response.status === 204) {
						// Successful deletion
						Swal.fire(
							'Deleted!',
							'Your activity has been deleted.',
							'success'
						).then(() => {
							// Redirect to the desired page
							window.location.href = homeURL
						})
					} else {
						// Error handling for unsuccessful deletion
						Swal.fire(
							'Error',
							'An error occurred while deleting the activity.',
							'error'
						)
					}
				})
			}
		})
	})
})
