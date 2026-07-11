const gameDialog = document.getElementById('easter-game');
const gameCells = [...document.querySelectorAll('.easter-game-cell')];
const gameScore = document.getElementById('gameScore');
const gameTime = document.getElementById('gameTime');
const gameStart = document.getElementById('gameStart');
const gameMessage = document.getElementById('gameMessage');
const gameMessageText = document.getElementById('gameMessageText');
const gameLauncher = document.getElementById('gameLauncher');

let activeCell = -1;
let score = 0;
let timeLeft = 20;
let gameTimer;
let targetTimer;

function clearTarget() {
    gameCells.forEach((cell) => {
        cell.classList.remove('is-target');
        cell.textContent = '';
        cell.setAttribute('aria-label', 'Empty game cell');
    });
    activeCell = -1;
}

function moveTarget() {
    clearTarget();
    activeCell = Math.floor(Math.random() * gameCells.length);
    const target = gameCells[activeCell];
    target.classList.add('is-target');
    target.textContent = 'BUG';
    target.setAttribute('aria-label', 'Catch the bug');
}

function stopGame(message) {
    clearInterval(gameTimer);
    clearInterval(targetTimer);
    clearTarget();
    gameStart.disabled = false;
    gameStart.textContent = 'Play Again';
    gameMessageText.textContent = message;
}

function startGame() {
    clearInterval(gameTimer);
    clearInterval(targetTimer);
    score = 0;
    timeLeft = 20;
    gameScore.value = score;
    gameTime.value = timeLeft;
    gameStart.disabled = true;
    gameMessageText.textContent = 'Bug detected. Catch it!';
    moveTarget();

    targetTimer = setInterval(moveTarget, 700);
    gameTimer = setInterval(() => {
        timeLeft -= 1;
        gameTime.value = timeLeft;
        if (timeLeft <= 0) {
            stopGame(`Scan complete. Final score: ${score}.`);
        }
    }, 1000);
}

gameCells.forEach((cell, index) => {
    cell.addEventListener('click', () => {
        if (index !== activeCell || gameStart.disabled === false) return;
        score += 1;
        gameScore.value = score;
        moveTarget();
    });
});

gameStart.addEventListener('click', startGame);
gameLauncher.addEventListener('click', () => {
    gameDialog.hidden = false;
    gameDialog.focusWindow?.();
});
gameDialog.addEventListener('gs-close', () => {
    clearInterval(gameTimer);
    clearInterval(targetTimer);
    clearTarget();
    gameStart.disabled = false;
});
