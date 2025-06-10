let canvas, ctx;
let player1 = { y: 150, score: 0, moveUp: false, moveDown: false };
let player2 = { y: 150, score: 0, moveUp: false, moveDown: false };
let ball = { x: 400, y: 200, vx: 7, vy: 7 };
let gameRunning = false;
let serveToLeft = false;
let player1Name = "Gracz 1";
let player2Name = "Gracz 2";

const PADDLE_HEIGHT = 60;   
const PADDLE_SPEED = 8;     

document.addEventListener("DOMContentLoaded", () => {
  canvas = document.getElementById("pongCanvas");
  ctx = canvas.getContext("2d");

  document.getElementById("startBtn").onclick = () => {
    player1Name = document.getElementById("player1").value || "Gracz 1";
    player2Name = document.getElementById("player2").value || "Gracz 2";
    document.getElementById("loginScreen").style.display = "none";
    document.getElementById("gameOverlay").style.display = "none";
    resetBall();
    gameRunning = true;
  };

  document.addEventListener("keydown", (e) => {
    if (e.key === "w") player1.moveUp = true;
    if (e.key === "s") player1.moveDown = true;
    if (e.key === "ArrowUp") player2.moveUp = true;
    if (e.key === "ArrowDown") player2.moveDown = true;
  });

  document.addEventListener("keyup", (e) => {
    if (e.key === "w") player1.moveUp = false;
    if (e.key === "s") player1.moveDown = false;
    if (e.key === "ArrowUp") player2.moveUp = false;
    if (e.key === "ArrowDown") player2.moveDown = false;
  });

  gameLoop();
});

function resetBall() {
  ball.x = 400;
  ball.y = 200;

  const speed = 7;
  const directionX = serveToLeft ? -1 : 1;
  const directionY = Math.random() < 0.5 ? -1 : 1;

  ball.vx = speed * directionX;
  ball.vy = speed * directionY;
}

function showOverlay(message) {
  const overlay = document.getElementById("gameOverlay");
  overlay.innerText = message + " (Naciśnij Spację)";
  overlay.style.display = "flex";
  resetControls();
  gameRunning = false;
}

function resetControls() {
  player1.moveUp = player1.moveDown = false;
  player2.moveUp = player2.moveDown = false;
}

document.addEventListener("keydown", (e) => {
  if (e.key === " " && !gameRunning && document.getElementById("loginScreen").style.display === "none") {
    document.getElementById("gameOverlay").style.display = "none";
    resetBall();
    gameRunning = true;
  }
});

function gameLoop() {
  requestAnimationFrame(gameLoop);
  if (!gameRunning) return;

  if (player1.moveUp && player1.y > 0) player1.y -= PADDLE_SPEED;
  if (player1.moveDown && player1.y < canvas.height - PADDLE_HEIGHT) player1.y += PADDLE_SPEED;
  if (player2.moveUp && player2.y > 0) player2.y -= PADDLE_SPEED;
  if (player2.moveDown && player2.y < canvas.height - PADDLE_HEIGHT) player2.y += PADDLE_SPEED;

  ball.x += ball.vx;
  ball.y += ball.vy;

  if (ball.y <= 0 || ball.y >= canvas.height) ball.vy *= -1;

  if (
    (ball.x <= 20 && ball.y >= player1.y && ball.y <= player1.y + PADDLE_HEIGHT) ||
    (ball.x >= 780 && ball.y >= player2.y && ball.y <= player2.y + PADDLE_HEIGHT)
  ) {
    ball.vx *= -1;
  }

  if (ball.x < 0) {
    player2.score++;
    serveToLeft = true;
    showOverlay(`${player2Name} zdobywa punkt!`);
  } else if (ball.x > canvas.width) {
    player1.score++;
    serveToLeft = false;
    showOverlay(`${player1Name} zdobywa punkt!`);
  }

  ctx.fillStyle = "black";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  ctx.fillStyle = "white";
  ctx.fillRect(10, player1.y, 10, PADDLE_HEIGHT);
  ctx.fillRect(780, player2.y, 10, PADDLE_HEIGHT);

  ctx.beginPath();
  ctx.arc(ball.x, ball.y, 10, 0, Math.PI * 2);
  ctx.fill();

  ctx.font = "24px monospace";
  ctx.fillText(`${player1Name}: ${player1.score}`, 50, 30);
  ctx.fillText(`${player2Name}: ${player2.score}`, 600, 30);
}