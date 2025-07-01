
function expandCard(cardId) {
    // Hide all other cards
    document.querySelector('.card-grid').classList.add('hide-all');
    const card = document.getElementById(cardId);
    card.classList.add('card-expanded');
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function closeCard(cardId) {
    // Show all cards again
    document.querySelector('.card-grid').classList.remove('hide-all');
    
    // Collapse the card
    const card = document.getElementById(cardId);
    card.classList.remove('card-expanded');
}