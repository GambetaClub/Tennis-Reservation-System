const capitalize = (word) => `${word.charAt(0).toUpperCase()}${word.slice(1)}`

document.addEventListener('DOMContentLoaded', function () {
	const cellHeight = document.querySelector('.schedule-cell').offsetHeight
	// This part populates each date passed from the backend to the calendar
	dates.forEach(function (date) {
		date.court.forEach(function (court) {
			var reservationContainer = document.createElement('div')
			reservationContainer.className = 'reservation-container'
			var reservationContent = document.createElement('div')
			reservationContent.className = 'reservation-content'
			reservationContent.style.height = date.duration * cellHeight + 'px'
			var block = document.createElement('div')
			block.className = 'block'
			block.innerHTML =
				capitalize(date.activity.type) + ' - ' + date.activity.title
			reservationContent.appendChild(block)
			reservationContainer.appendChild(reservationContent)
			const startTime = new Date(date.datetime_start)

			// Convert time to index for positioning.
			var timeIndex = (startTime.getHours() - 6) * 2
			if (startTime.getMinutes() >= 30) timeIndex += 1

			// Insert activity into the correct court and time slot
			var courtElement = document.getElementById(court)
			var timeSlotElement = courtElement.children[timeIndex]

			// Disabling the cells under the block
			for (var i = timeIndex; i < timeIndex + date.duration; i++) {
				courtElement.children[i].className = 'schedule-cell disabled'
			}
			timeSlotElement.appendChild(reservationContainer)
		})
	})
})

const getProColor = (pro) => {}

const schedulePanel = document.getElementById('schedule')

courtDurationOptions = {
	'30': '30 minutes',
	'60': '1 hour',
	'90': '1 hour and 30 minutes',
	'120': '2 hours',
}

function transformToAMPM(time24) {
	const [hours, minutes] = time24.split(':').map(Number)

	const period = hours >= 12 ? 'PM' : 'AM'

	const hours12 = hours % 12 || 12

	const time12 = `${hours12}:${minutes.toString().padStart(2, '0')} ${period}`

	return time12
}

function getColorForProByName(proName) {
	// Check if the name is in the mapping, use a default color if not found
	const color = nameToColorMap[proName] || 'gray' // Default to gray if not found
	return color
}

schedulePanel.addEventListener('click', function (event) {
	// Check if the clicked element is a schedule cell
	if (event.target.classList.contains('schedule-cell')) {
		const selectedTime = event.target.getAttribute('data-time')
		const court = event.target.getAttribute('data-court')
		const date = window.location.pathname.split('/')[2]
		var selectedDuration
		var activityType

		const handleCourtReservation = () => {
			activityType = 'court'
			Swal.fire({
				title: 'How long would you like to reserve the court?',
				icon: 'question',
				input: 'select',
				html: `You selected ${court} at ${transformToAMPM(
					selectedTime
				)}`,
				inputPlaceholder: 'Select a duration',
				confirmButtonColor: '#6BBB6B',
				confirmButtonText: `Reserve Court`,
				inputOptions: courtDurationOptions,
				inputValidator: (value) => {
					if (!value) {
						return 'You need to choose a duration'
					}
				},
			})
		}

		function fetchAvailablePros() {
			return $.ajax({
				url: '/get_available_pros/',
				method: 'GET',
				dataType: 'json',
				data: {
					date: date,
					time: selectedTime,
					duration: selectedDuration,
				},
			})
		}

		async function choosePro() {
			try {
				// Fetch available pros via AJAX
				const response = await fetchAvailablePros()
				const availablePros = response.pros

				// Create an options object for the Swal input
				const proOptions = {}
				availablePros.forEach((pro) => {
					proOptions[pro.id] = pro.name // Assuming 'id' and 'name' are the properties in your data
				})

				// Show the Swal alert with the dynamic options
				const { value: selectedProId } = await Swal.fire({
					title: 'Select a Pro',
					input: 'select',
					inputOptions: proOptions,
					inputPlaceholder: 'Select a Pro',
					showCancelButton: true,
					inputValidator: (value) => {
						return new Promise((resolve) => {
							if (value) {
								resolve() // User selected a pro, validation is successful
							} else {
								resolve('You need to choose a Pro') // Validation failed
							}
						})
					},
				})

				// Handle the selected Pro (e.g., store it or perform other actions)
				if (selectedProId) {
					console.log('Selected Pro ID:', selectedProId)
				} else {
					console.log('No Pro selected')
				}
			} catch (error) {
				console.error('Error:', error)
			}
		}

		const handleCreation = () => {
			Swal.fire({
				title: 'What would you like to create?',
				icon: 'question',
				showCloseButton: true,
				showDenyButton: true,
				focusConfirm: false,
				confirmButtonColor: '#6BBB6B',
				denyButtonColor: '#CC6666',
				confirmButtonText: `Court Reservation`,
				confirmButtonAriaLabel: 'Private Lesson',
				denyButtonText: 'Private Lesson',
				denyButtonAriaLabel: 'Private Lesson',
			}).then((result) => {
				if (result.isConfirmed) {
					// Handles a Court Reservation
					handleCourtReservation()
				} else if (result.isDenied) {
					// Handles Private or Semi-Private Lesson
					Swal.fire({
						title: 'How long would you like to play?',
						icon: 'question',
						input: 'select',
						html: `You selected ${court} at ${transformToAMPM(
							selectedTime
						)}`,
						inputPlaceholder: 'Select a duration',
						confirmButtonColor: '#CC6666',
						confirmButtonText: `Continue`,
						inputOptions: courtDurationOptions,
						inputValidator: (value) => {
							if (!value) {
								return 'You need to choose a duration'
							}
						},
					}).then((selection) => {
						console.log(selection.value)
						selectedDuration = selection.value
						if (selection.isConfirmed) {
							Swal.fire({
								title: 'Would you like a private or semiprivate lesson?',
								icon: 'question',
								showCloseButton: true,
								showDenyButton: true,
								html: 'A semiprivate consists of 2 to 4 people.',
								focusConfirm: false,
								confirmButtonColor: '#3085d6',
								denyButtonColor: '#CC6666',
								confirmButtonText: `Private Lesson`,
								confirmButtonAriaLabel: 'Private Lesson',
								denyButtonText: 'Semiprivate Lesson',
								denyButtonAriaLabel: 'Semi-private Lesson',
							}).then((lessonTypeResult) => {
								if (lessonTypeResult.isConfirmed) {
									// Handles Private Lesson
									choosePro()
								} else if (lessonTypeResult.isDenied) {
									// Handles Semi Private Lesson
									choosePro()
								}
							})
						}
					})
				}
			})
		}

		handleCreation()
	}
})
