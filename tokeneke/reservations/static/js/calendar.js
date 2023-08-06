const capitalize = (word) => `${word.charAt(0).toUpperCase()}${word.slice(1)}`

document.addEventListener('DOMContentLoaded', function () {
	const cellHeight = document.querySelector('.schedule-cell').offsetHeight
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

function handleCellClick(cell) {
	console.log('Clicked cell:', cell)
	if (cell.style.backgroundColor != 'red') {
		cell.style.backgroundColor = 'blue'
	} else {
		cell.style.backgroundColor = 'white'
	}
}
