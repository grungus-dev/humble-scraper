function removeElements(selector) {
  document.querySelectorAll(selector).forEach(el => el.remove());
}

function appendElements(targetItems) {
  const fragment = document.createDocumentFragment();

  for (const item of targetItems) {
    const header = document.createElement('h1');
    header.textContent = item.textContent.trim();
    fragment.appendChild(header);
  }

  document.body.appendChild(fragment);
}

function getRandomColor() {
  // ensures a valid 6-digit hex
  return `#${Math.floor(Math.random() * 0xFFFFFF).toString(16).padStart(6, '0')}`;
}

function main() {
  const currentUrl = window.location.href;

  // Skip modification on homepage
  if (currentUrl === 'https://www.humblebundle.com/membership/home') { 
    return;
  }

  // Remove already claimed games
  removeElements('.content-choice.claimed');

  // Collect remaining game titles
  const mainGames = document.querySelectorAll('.content-choice-title');
  const extraGames = document.querySelectorAll('.extra-human-name');

  // Append selected items first (so we can remove the rest safely)
  appendElements(mainGames);
  appendElements(extraGames);

  // Set random background color for Python detection
  document.body.style.backgroundColor = getRandomColor();

  // Now strip the page but keep <body> and appended <h1> elements
  const elementsToRemove = ['div', 'ul', 'header', 'script'];

  for (const tag of elementsToRemove) {
    document.querySelectorAll(tag).forEach(el => {
      // Only remove if it's not one of our newly added headers
      if (!el.closest('body > h1')) el.remove();
    });
  }

  // Clear any injected styles/scripts from head
  document.head.textContent = '';
}

main();