const capitalize = (word) => `${word.charAt(0).toUpperCase()}${word.slice(1)}`

var activityData = {}

const courtColor = '#005C29'
const privateColor = '#960018'
const semiPrivateColor = '#ED2939'
const clinicColor = '#0077B6'
const courtDurationOptions = {
	'30': '30 minutes',
	'60': '1 hour',
	'90': '1 hour and 30 minutes',
	'120': '2 hours',
}

const schedulePanel = document.getElementById('schedule')

function createActivity() {
	// Send a POST request to Django view
	const csrfToken = $('input[name=csrfmiddlewaretoken]').val()
	var jsonData = JSON.stringify(activityData)
	return $.ajax({
		url: 'create_activity',
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrfToken,
		},
		data: JSON.stringify(jsonData),
		success: function (data) {
			console.log('Success: ', data)
		},
		error: function (error) {
			console.log('Error', error)
		},
	})
}

document.addEventListener('DOMContentLoaded', function () {
	const cellHeight = document.querySelector('.schedule-cell').offsetHeight

	function createReservationBlock(date) {
		const { color, blockString } = getColorAndStringForBlock(date)
		const reservationContainer = document.createElement('div')
		reservationContainer.className = 'reservation-container'
		const reservationContent = document.createElement('div')
		reservationContent.className = 'reservation-content'
		reservationContent.style.height = date.duration * cellHeight + 'px'
		const block = document.createElement('div')
		block.className = 'block'
		block.style.backgroundColor = color
		block.innerHTML = blockString
		reservationContent.appendChild(block)
		reservationContainer.appendChild(reservationContent)
		return reservationContainer
	}

	function getColorAndStringForBlock(date) {
		// Date is a dictionary with all the properties of the Date object
		let color = ''
		let blockString = ''
		switch (date.activity.type) {
			case 'clinic':
				color = clinicColor
				blockString = 'Clinic ' + date.activity.title
				break
			case 'court':
				color = courtColor
				blockString = 'Court ' + (date.host ? date.host : '')
				break
			case 'private':
				color = date.pros.length > 0 ? date.pros[0].color : privateColor
				blockString =
					'Private ' +
					(date.host ? date.host : '') +
					' ' +
					(date.pros ? date.pros[0].name : '')
				break
			case 'semiprivate':
				color =
					date.pros.length > 0 ? date.pros[0].color : semiPrivateColor
				blockString =
					'Semi-Private ' +
					(date.host ? date.host : '') +
					' ' +
					(date.pros ? date.pros[0].name : '')
				break
			default:
				color = 'gray' // Default color
				blockString = date.activity.title
				break
		}

		return { color, blockString }
	}

	function insertReservationIntoSchedule(date, court, timeIndex) {
		const courtElement = document.getElementById(court)
		const timeSlotElement = courtElement.children[timeIndex]

		// Disabling the cells under the block
		for (let i = timeIndex; i < timeIndex + date.duration; i++) {
			courtElement.children[i].classList.add('schedule-cell', 'disabled')
		}

		timeSlotElement.appendChild(createReservationBlock(date))
	}

	dates.forEach(function (date) {
		date.court.forEach(function (court) {
			const startTime = new Date(date.datetime_start)

			// Convert time to index for positioning.
			let timeIndex = (startTime.getHours() - 6) * 2
			if (startTime.getMinutes() >= 30) timeIndex += 1

			insertReservationIntoSchedule(date, court, timeIndex)
		})
	})
})

const transformToAMPM = (time24) => {
	const [hours, minutes] = time24.split(':').map(Number)

	const period = hours >= 12 ? 'PM' : 'AM'

	const hours12 = hours % 12 || 12

	const time12 = `${hours12}:${minutes.toString().padStart(2, '0')} ${period}`

	return time12
}

async function askForDuration() {
	// Returns the duration if the user selected one
	const result = await Swal.fire({
		title: 'How long would you like to play?',
		icon: 'question',
		input: 'select',
		inputPlaceholder: 'Select a duration',
		confirmButtonColor: courtColor,
		confirmButtonText: `Continue`,
		inputOptions: courtDurationOptions,
		inputValidator: (value) => {
			if (!value) {
				return 'You need to choose a duration'
			}
		},
	})
	return result.value
}

function fetchAvailablePros() {
	return $.ajax({
		url: '/get_available_pros',
		method: 'GET',
		dataType: 'json',
		data: {
			date: activityData['date'],
			time: activityData['time'],
			duration: activityData['duration'],
		},
	})
}

async function askForPro() {
	try {
		// Fetch available pros via AJAX
		const response = await fetchAvailablePros()
		const availablePros = response.pros

		// Create an options object for the Swal input
		const proOptions = {}
		availablePros.forEach((pro) => {
			proOptions[pro.id] = pro.name
		})

		// Show the Swal alert with the dynamic options
		const { value: selectedPro } = await Swal.fire({
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

		if (selectedPro) {
			// Return an object with both ID and name
			return {
				id: selectedPro,
				name: proOptions[selectedPro],
			}
		} else {
			return null
		}
	} catch (error) {
		console.error('Error:', error)
		return null
	}
}

async function handleCourtReservation() {
	activityData['type'] = 'court'
	activityData['duration'] = await askForDuration()
	if (activityData['duration']) {
		return true
	}
	return false
}

async function handlePrivateLesson() {
	const result = await Swal.fire({
		title: 'Would you like a private or semiprivate lesson?',
		icon: 'question',
		showCloseButton: true,
		showDenyButton: true,
		html: 'A semiprivate consists of 2 to 4 people.',
		focusConfirm: false,
		confirmButtonColor: privateColor,
		denyButtonColor: semiPrivateColor,
		confirmButtonText: `Private Lesson`,
		confirmButtonAriaLabel: 'Private Lesson',
		denyButtonText: 'Semi-private Lesson',
		denyButtonAriaLabel: 'Semi-private Lesson',
	})

	if (result.isConfirmed) {
		activityData['type'] = 'private'
	} else if (result.isDenied) {
		activityData['type'] = 'semiprivate'
	}

	activityData['duration'] = await askForDuration()

	if (activityData['duration']) {
		const selectedPro = await askForPro()
		if (selectedPro) {
			activityData['pro'] = selectedPro.id
			activityData['proName'] = selectedPro.name
			return true
		}
	}

	return false // Return false if something goes wrong or nothing is selected
}

async function askForConfirmation(callback) {
	let description = `You want a <b>${
		activityData['type']
	}</b> at <b>${transformToAMPM(activityData['time'])}</b> on <b>${
		activityData['court']
	}</b>`
	if (activityData['type'] != 'court') {
		description += ` with <b>${activityData['proName']}</b>.`
	} else {
		description += `.`
	}

	const result = await Swal.fire({
		title: 'Please confirm your activity',
		icon: 'question',
		html: description,
		showCloseButton: true,
		showDenyButton: true,
		focusConfirm: false,
		confirmButtonColor: courtColor,
		denyButtonColor: privateColor,
		confirmButtonText: 'Confirm',
		confirmButtonAriaLabel: 'Confirm',
		denyButtonText: 'Cancel',
		denyButtonAriaLabel: 'Cancel',
	})

	if (result.isConfirmed) {
		callback()
	} else if (result.isDenied) {
	}
}

async function handleCreation(callback) {
	let isComplete = false
	try {
		const result = await Swal.fire({
			title: 'What would you like to create?',
			icon: 'question',
			showCloseButton: true,
			showDenyButton: true,
			focusConfirm: false,
			confirmButtonColor: courtColor,
			denyButtonColor: privateColor,
			confirmButtonText: `Court Reservation`,
			confirmButtonAriaLabel: 'Private Lesson',
			denyButtonText: 'Private Lesson',
			denyButtonAriaLabel: 'Private Lesson',
		})

		if (result.isConfirmed) {
			isComplete = await handleCourtReservation()
		} else if (result.isDenied) {
			isComplete = await handlePrivateLesson()
		}
		if (isComplete) {
			askForConfirmation(callback)
		}
	} catch (error) {
		console.error('Error:', error)
	}
}

schedulePanel.addEventListener('click', function (event) {
	// Check if the clicked element is a schedule cell
	if (event.target.classList.contains('schedule-cell')) {
		activityData['time'] = event.target.getAttribute('data-time')
		activityData['court'] = event.target.getAttribute('data-court')
		activityData['date'] = window.location.pathname.split('/')[2]

		handleCreation(createActivity)
	}
})
