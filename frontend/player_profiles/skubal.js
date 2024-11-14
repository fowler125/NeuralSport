// Get all the buttons in the .nft-list class
const buttons = document.querySelectorAll('.nft-list .item .bid a');

// Add an event listener to each button
buttons.forEach((button) => {
  button.addEventListener('click', (event) => {
    // Prevent the default link behavior
    event.preventDefault();

    // Get the parent element (the .item element)
    const item = button.parentNode.parentNode;

    // Get the image source and player name
    const imageSrc = item.querySelector('img').src;
    const playerName = item.querySelector('.info h5').textContent;

    // Perform the desired action (e.g. navigate to a different page)
    console.log(`Button clicked for ${playerName}!`);
    window.location.href = 'player_profiles/players.html?player=' + encodeURIComponent(playerName);;
    // TODO: Add your desired functionality here
  });
});