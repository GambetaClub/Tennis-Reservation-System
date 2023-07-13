document.addEventListener('DOMContentLoaded', function () {
	var listView = document.querySelector('.list-view')
	var gridView = document.querySelector('.grid-view')
	var newProject = document.querySelector('.add-btn')
	var projectsList = document.querySelector('.project-boxes')

	listView.addEventListener('click', function () {
		gridView.classList.remove('active')
		listView.classList.add('active')
		projectsList.classList.remove('jsGridView')
		projectsList.classList.add('jsListView')
	})

	gridView.addEventListener('click', function () {
		gridView.classList.add('active')
		listView.classList.remove('active')
		projectsList.classList.remove('jsListView')
		projectsList.classList.add('jsGridView')
	})

	newProject.addEventListener('click', function () {
		const swalWithBootstrapButtons = Swal.mixin({
			customClass: {
				confirmButton: 'btn btn-success',
				cancelButton: 'btn btn-success',
			},
			buttonsStyling: false,
		})

		swalWithBootstrapButtons
			.fire({
				title: 'What would you like to create?',
				text: 'If you want to create a new event from scratch, you should start with event.',
				icon: 'question',
				showCancelButton: true,
				confirmButtonText: 'Event',
				cancelButtonText: 'Activity',
			})
			.then((result) => {
				if (result.isConfirmed) {
					location.href = '/create_event'
				} else if (
					/* Read more about handling dismissals below */
					result.dismiss === Swal.DismissReason.cancel
				) {
					location.href = '/create_activity'
				}
			})
	})
})

$(document).ready(function () {
	$('#search-input').on('input', function () {
		var searchInput = $('#search-input').val()
		var current_events = $('.box-content-header')
			.map(function () {
				return this.innerHTML
			})
			.get()
		$.ajax({
			type: 'POST',
			url: 'filter_events',
			data: {
				input: searchInput,
				curr_events: JSON.stringify(current_events),
				csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
			},
			success: function (response) {
				var searched_events = response.data
				var events = $('.box-content-header')
					.map(function () {
						return this
					})
					.get()
				console.log(events)
				console.log(searched_events)
				$.each(events, function (index, element) {
					if (
						jQuery.inArray(element.innerHTML, searched_events) != -1
					) {
						$(element).parent().parent().parent().show()
					} else {
						$(element).parent().parent().parent().hide()
					}
				})
			},
		})
	})
})
