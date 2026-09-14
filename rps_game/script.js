const HANDS = {
  rock: { label: "바위", emoji: "✊", beats: "scissors" },
  scissors: { label: "가위", emoji: "✌️", beats: "paper" },
  paper: { label: "보", emoji: "🖐️", beats: "rock" },
};

const CHOICES = Object.keys(HANDS);

const playerHandEl = document.getElementById("playerHand");
const computerHandEl = document.getElementById("computerHand");
const resultMessage = document.getElementById("resultMessage");
const winCountEl = document.getElementById("winCount");
const drawCountEl = document.getElementById("drawCount");
const loseCountEl = document.getElementById("loseCount");
const resetBtn = document.getElementById("resetBtn");

let winCount = 0;
let drawCount = 0;
let loseCount = 0;

function randomChoice() {
  return CHOICES[Math.floor(Math.random() * CHOICES.length)];
}

function judge(player, computer) {
  if (player === computer) return "draw";
  return HANDS[player].beats === computer ? "win" : "lose";
}

function play(playerChoice) {
  const computerChoice = randomChoice();

  playerHandEl.textContent = HANDS[playerChoice].emoji;
  computerHandEl.textContent = HANDS[computerChoice].emoji;

  const result = judge(playerChoice, computerChoice);

  if (result === "win") {
    winCount += 1;
    resultMessage.textContent = `${HANDS[playerChoice].label} > ${HANDS[computerChoice].label} — 승리! 🎉`;
  } else if (result === "lose") {
    loseCount += 1;
    resultMessage.textContent = `${HANDS[playerChoice].label} < ${HANDS[computerChoice].label} — 패배 😢`;
  } else {
    drawCount += 1;
    resultMessage.textContent = `${HANDS[playerChoice].label} = ${HANDS[computerChoice].label} — 무승부`;
  }

  winCountEl.textContent = winCount;
  drawCountEl.textContent = drawCount;
  loseCountEl.textContent = loseCount;
}

document.querySelectorAll(".choice-btn").forEach((btn) => {
  btn.addEventListener("click", () => play(btn.dataset.choice));
});

resetBtn.addEventListener("click", () => {
  winCount = 0;
  drawCount = 0;
  loseCount = 0;
  winCountEl.textContent = 0;
  drawCountEl.textContent = 0;
  loseCountEl.textContent = 0;
  playerHandEl.textContent = "❔";
  computerHandEl.textContent = "❔";
  resultMessage.textContent = "가위, 바위, 보 중 하나를 선택하세요!";
});
