function handleCellClick(cell) {
	console.log('Clicked cell:', cell)
	if (cell.style.backgroundColor != 'red') {
		cell.style.backgroundColor = 'red'
	} else {
		cell.style.backgroundColor = 'white'
	}
}
