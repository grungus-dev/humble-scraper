function removeElementsByClass(className) {
    let elements = document.getElementsByClassName(className);
    while(elements.length > 0) {
        elements[0].parentNode.removeChild(elements[0]);
    }
}

function appendElements(targetItems){
	for (let i = 0; i < targetItems.length; i++){
			let header = document.createElement('h1');
			header.textContent = targetItems[i].textContent;
			document.body.appendChild(header);
		}
}

function getRandomNum(min, max) {
	return Math.floor(Math.random() * (max - min + 1)) + min;
}

function removeElements(element) {
	let elements = document.querySelectorAll(element);
	return elements.forEach(element => element.remove());   
}

function main() {
	const currentUrl = window.location.href;

	// if user is in the home page, no changes
	if (currentUrl == 'https://www.humblebundle.com/membership/home'){
		return;
	}

	// remove all already claimed games 
	removeElementsByClass('content-choice claimed')

	// find all remaining games
	const mainGamesClass = 'content-choice-title';
	const mainGames = document.getElementsByClassName(mainGamesClass);

	const extraGamesClass = 'extra-human-name';
	const extraGames = document.getElementsByClassName(extraGamesClass);

	// append all games to the end of webpage
	appendElements(mainGames);
	appendElements(extraGames);
	

	// change background to random color
	// this makes it easier for the python script 
	// to tell when the page has loaded
	let style = document.createElement('style');
	randomColor = getRandomNum(111111, 999999);
	style.textContent = 'body { background-color: #' + randomColor.toString() + '; }';
	document.body.appendChild(style);

	// remove all other existing elements
	const elements = ['div', 'ul', 'header', 'script'];

	for (let i = 0; i < elements.length; i++){
		removeElements(elements[i]);
	}

	// remove header styles
	document.head.textContent = '';
}

main();