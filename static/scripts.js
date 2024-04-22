class BoggleGame {
    constructor() {
        this.form = document.querySelector('#word-form');
        this.wordInput = document.querySelector('#word-input');
        this.scoreDisplay = document.querySelector('#score');
        this.timerDisplay = document.querySelector('#timer');
        this.score = 0;
        this.timeLeft = 60;
        this.timer = null;

        this.addEventListeners();
        this.startTimer();
    }
    addEventListeners() {
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
    }
startTimer() {
    this.timer = setInterval(() => {
        this.updateTimer();
    }, 1000);
}
updateTimer() {
    if (this.timeLeft === 0) {
        clearInterval(this.timer);
        alert('Time is up!');
        this.form.querySelector('button').disabled = true;
        this.wordInput.disabled = true;
    } else {
        this.timerDisplay.textContent = `Time left: ${this.timeLeft--}`;
    }
}
async handleSubmit(e) {
    e.preventDefault();
    const word = this.wordInput.value.trim();
    if (!word) return;

    try {
        const response = await axios.get('/check-word', { params: { word } });
        this.processResponse(response.data.result);
    } catch (error) {
        console.error('Error checking word:', error);
        alert('Failed to check the word. Please try again.');
    }
    this.wordInput.value = '';
}
processResponse(result) {
    alert(result);
    if (result === 'ok') {
        this.updateScore(this.wordInput.value.length);
    }
}
updateScore(points) {
    this.score += points;
    this.scoreDisplay.textContent = `Score: ${this.score}`;
}
}
document.addEventListener('DOMContentLoaded', () => new BoggleGame());