const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");
const scoreEl = document.getElementById("score");
const speedEl = document.getElementById("speed");
const overlay = document.getElementById("overlay");
const overlayText = document.getElementById("overlayText");
const restartBtn = document.getElementById("restartBtn");

const ROAD_LEFT = 20;
const ROAD_RIGHT = canvas.width - 20;
const ROAD_WIDTH = ROAD_RIGHT - ROAD_LEFT;

const PLAYER_WIDTH = 40;
const PLAYER_HEIGHT = 70;
const PLAYER_SPEED = 260; // px/sec

const OBSTACLE_WIDTH = 40;
const OBSTACLE_HEIGHT = 70;

const BASE_FALL_SPEED = 180; // px/sec at game start
const MAX_FALL_SPEED = 520;
const SPEED_UP_RATE = 6; // fall speed increase per second

let player;
let obstacles;
let keys;
let fallSpeed;
let spawnTimer;
let spawnInterval;
let score;
let running;
let lastTime;
let roadOffset;

function resetGame() {
  player = {
    x: canvas.width / 2 - PLAYER_WIDTH / 2,
    y: canvas.height - PLAYER_HEIGHT - 20,
  };
  obstacles = [];
  keys = { left: false, right: false };
  fallSpeed = BASE_FALL_SPEED;
  spawnTimer = 0;
  spawnInterval = 1.1;
  score = 0;
  roadOffset = 0;
  running = true;
  overlay.classList.add("hidden");
  lastTime = performance.now();
  requestAnimationFrame(loop);
}

function spawnObstacle() {
  const x = ROAD_LEFT + Math.random() * (ROAD_WIDTH - OBSTACLE_WIDTH);
  obstacles.push({ x, y: -OBSTACLE_HEIGHT });
}

function rectsOverlap(a, b) {
  return (
    a.x < b.x + OBSTACLE_WIDTH &&
    a.x + PLAYER_WIDTH > b.x &&
    a.y < b.y + OBSTACLE_HEIGHT &&
    a.y + PLAYER_HEIGHT > b.y
  );
}

function update(dt) {
  if (keys.left) player.x -= PLAYER_SPEED * dt;
  if (keys.right) player.x += PLAYER_SPEED * dt;
  player.x = Math.max(ROAD_LEFT, Math.min(ROAD_RIGHT - PLAYER_WIDTH, player.x));

  fallSpeed = Math.min(MAX_FALL_SPEED, fallSpeed + SPEED_UP_RATE * dt);
  roadOffset = (roadOffset + fallSpeed * dt) % 40;

  spawnTimer += dt;
  if (spawnTimer >= spawnInterval) {
    spawnTimer = 0;
    spawnInterval = Math.max(0.45, spawnInterval - 0.01);
    spawnObstacle();
  }

  for (const ob of obstacles) {
    ob.y += fallSpeed * dt;
  }
  obstacles = obstacles.filter((ob) => ob.y < canvas.height + OBSTACLE_HEIGHT);

  for (const ob of obstacles) {
    if (rectsOverlap(player, ob)) {
      gameOver();
      return;
    }
  }

  score += dt * 10 * (fallSpeed / BASE_FALL_SPEED);
}

function roundRectPath(x, y, w, h, r) {
  ctx.beginPath();
  ctx.moveTo(x + r, y);
  ctx.lineTo(x + w - r, y);
  ctx.quadraticCurveTo(x + w, y, x + w, y + r);
  ctx.lineTo(x + w, y + h - r);
  ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
  ctx.lineTo(x + r, y + h);
  ctx.quadraticCurveTo(x, y + h, x, y + h - r);
  ctx.lineTo(x, y + r);
  ctx.quadraticCurveTo(x, y, x + r, y);
  ctx.closePath();
}

// facing: "up" (플레이어, 위를 향해 달림) 또는 "down" (장애물, 아래로 달려옴)
function drawCar(x, y, w, h, bodyColor, facing) {
  const windshieldY = facing === "up" ? y + h * 0.12 : y + h * 0.6;
  const lightY = facing === "up" ? y + 4 : y + h - 4;
  const wheelW = w * 0.16;
  const wheelH = h * 0.22;

  // 차체
  roundRectPath(x, y, w, h, 8);
  ctx.fillStyle = bodyColor;
  ctx.fill();

  // 바퀴
  ctx.fillStyle = "#1a1a1a";
  ctx.fillRect(x - wheelW * 0.35, y + h * 0.14, wheelW, wheelH);
  ctx.fillRect(x + w - wheelW * 0.65, y + h * 0.14, wheelW, wheelH);
  ctx.fillRect(x - wheelW * 0.35, y + h * 0.64, wheelW, wheelH);
  ctx.fillRect(x + w - wheelW * 0.65, y + h * 0.64, wheelW, wheelH);

  // 앞유리
  roundRectPath(x + w * 0.18, windshieldY, w * 0.64, h * 0.22, 3);
  ctx.fillStyle = "rgba(190, 225, 255, 0.85)";
  ctx.fill();

  // 헤드라이트
  ctx.fillStyle = "#fff3a0";
  ctx.beginPath();
  ctx.arc(x + w * 0.22, lightY, 2.5, 0, Math.PI * 2);
  ctx.arc(x + w * 0.78, lightY, 2.5, 0, Math.PI * 2);
  ctx.fill();

  // 중앙 라인 포인트(지붕 디테일)
  ctx.fillStyle = "rgba(0, 0, 0, 0.15)";
  ctx.fillRect(x + w * 0.46, y + h * 0.38, w * 0.08, h * 0.14);
}

function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  ctx.fillStyle = "#444";
  ctx.fillRect(ROAD_LEFT, 0, ROAD_WIDTH, canvas.height);

  ctx.strokeStyle = "#fff";
  ctx.lineWidth = 3;
  ctx.setLineDash([20, 20]);
  ctx.beginPath();
  ctx.moveTo(canvas.width / 2, roadOffset - 40);
  ctx.lineTo(canvas.width / 2, canvas.height);
  ctx.stroke();
  ctx.setLineDash([]);

  drawCar(player.x, player.y, PLAYER_WIDTH, PLAYER_HEIGHT, "#e94560", "up");

  for (const ob of obstacles) {
    drawCar(ob.x, ob.y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT, "#2ec4b6", "down");
  }

  scoreEl.textContent = Math.floor(score);
  speedEl.textContent = Math.floor(fallSpeed);
}

function loop(now) {
  if (!running) return;
  const dt = Math.min(0.05, (now - lastTime) / 1000);
  lastTime = now;

  update(dt);
  if (!running) return;
  draw();

  requestAnimationFrame(loop);
}

function gameOver() {
  running = false;
  overlayText.textContent = `게임 오버! 최종 점수: ${Math.floor(score)}`;
  overlay.classList.remove("hidden");
}

document.addEventListener("keydown", (e) => {
  if (e.key === "ArrowLeft" || e.key === "a" || e.key === "A") keys.left = true;
  if (e.key === "ArrowRight" || e.key === "d" || e.key === "D") keys.right = true;
  if (e.key === " " && !running) {
    e.preventDefault();
    resetGame();
  }
});

document.addEventListener("keyup", (e) => {
  if (e.key === "ArrowLeft" || e.key === "a" || e.key === "A") keys.left = false;
  if (e.key === "ArrowRight" || e.key === "d" || e.key === "D") keys.right = false;
});

restartBtn.addEventListener("click", resetGame);

resetGame();
