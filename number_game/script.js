const guessInput = document.getElementById("guessInput");
const guessBtn = document.getElementById("guessBtn");
const message = document.getElementById("message");
const triesEl = document.getElementById("tries");
const restartBtn = document.getElementById("restartBtn");
const inputRow = document.querySelector(".input-row");

let target;
let tries;
let won;

function resetGame() {
  target = Math.floor(Math.random() * 100) + 1;
  tries = 0;
  won = false;
  triesEl.textContent = tries;
  message.textContent = "숫자를 입력하고 확인을 눌러보세요.";
  guessInput.value = "";
  inputRow.classList.remove("hidden");
  restartBtn.classList.add("hidden");
  guessInput.focus();
}

function checkGuess() {
  if (won) return;

  const raw = guessInput.value.trim();
  const guess = Number(raw);

  if (raw === "" || Number.isNaN(guess) || !Number.isInteger(guess) || guess < 1 || guess > 100) {
    message.textContent = "1~100 사이의 숫자를 입력해주세요.";
    guessInput.value = "";
    guessInput.focus();
    return;
  }

  tries += 1;
  triesEl.textContent = tries;

  if (guess === target) {
    won = true;
    message.textContent = `정답입니다! 🎉 ${tries}번 만에 맞히셨어요.`;
    inputRow.classList.add("hidden");
    restartBtn.classList.remove("hidden");
  } else if (guess < target) {
    message.textContent = "더 높은 숫자예요! ⬆️";
    guessInput.value = "";
    guessInput.focus();
  } else {
    message.textContent = "더 낮은 숫자예요! ⬇️";
    guessInput.value = "";
    guessInput.focus();
  }
}

guessBtn.addEventListener("click", checkGuess);

guessInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") checkGuess();
});

restartBtn.addEventListener("click", resetGame);

resetGame();
