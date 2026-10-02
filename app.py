import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
page_title="벽돌깨기",
page_icon="🧱",
layout="centered"
)

st.title("🧱 벽돌깨기 게임")
st.caption("← → 방향키로 패들을 움직이세요. | Space로 게임을 다시 시작할 수 있습니다.")

html_code = """

<!DOCTYPE html> <html> <head> <meta charset="UTF-8"> <style> body { margin: 0; background: #0f172a; display: flex; justify-content: center; align-items: center; } canvas { border: 3px solid #38bdf8; border-radius: 12px; background: #020617; max-width: 100%; } </style> </head> <body>

<canvas id="game" width="500" height="650"></canvas>

<script> const canvas = document.getElementById("game"); const ctx = canvas.getContext("2d"); // ==================== // 게임 설정 // ==================== let score = 0; let lives = 3; let gameOver = false; let gameClear = false; let ball = { x: 250, y: 570, radius: 9, dx: 4, dy: -4 }; let paddle = { x: 200, y: 610, width: 100, height: 15, speed: 8 }; let leftPressed = false; let rightPressed = false; // ==================== // 벽돌 설정 // ==================== const rows = 6; const columns = 8; const brickWidth = 50; const brickHeight = 22; const brickPadding = 8; const brickTop = 60; const brickLeft = 22; let bricks = []; function createBricks() { bricks = []; for (let row = 0; row < rows; row++) { bricks[row] = []; for (let col = 0; col < columns; col++) { bricks[row][col] = { x: 0, y: 0, alive: true }; } } } createBricks(); // ==================== // 키보드 조작 // ==================== document.addEventListener("keydown", function(event) { if (event.key === "ArrowLeft") { leftPressed = true; event.preventDefault(); } if (event.key === "ArrowRight") { rightPressed = true; event.preventDefault(); } if (event.code === "Space") { if (gameOver || gameClear) { restartGame(); } event.preventDefault(); } }); document.addEventListener("keyup", function(event) { if (event.key === "ArrowLeft") { leftPressed = false; } if (event.key === "ArrowRight") { rightPressed = false; } }); // ==================== // 공 그리기 // ==================== function drawBall() { ctx.beginPath(); ctx.arc( ball.x, ball.y, ball.radius, 0, Math.PI * 2 ); ctx.fillStyle = "#facc15"; ctx.fill(); ctx.closePath(); } // ==================== // 패들 그리기 // ==================== function drawPaddle() { ctx.fillStyle = "#38bdf8"; ctx.fillRect( paddle.x, paddle.y, paddle.width, paddle.height ); } // ==================== // 벽돌 그리기 // ==================== function drawBricks() { const colors = [ "#ef4444", "#f97316", "#eab308", "#22c55e", "#06b6d4", "#8b5cf6" ]; for (let row = 0; row < rows; row++) { for (let col = 0; col < columns; col++) { let brick = bricks[row][col]; if (!brick.alive) { continue; } brick.x = brickLeft + col * (brickWidth + brickPadding); brick.y = brickTop + row * (brickHeight + brickPadding); ctx.fillStyle = colors[row]; ctx.fillRect( brick.x, brick.y, brickWidth, brickHeight ); } } } // ==================== // 점수와 목숨 // ==================== function drawInformation() { ctx.fillStyle = "white"; ctx.font = "18px Arial"; ctx.fillText( "점수: " + score, 15, 30 ); ctx.fillText( "목숨: " + lives, 420, 30 ); } // ==================== // 벽돌 충돌 검사 // ==================== function collisionDetection() { for (let row = 0; row < rows; row++) { for (let col = 0; col < columns; col++) { let brick = bricks[row][col]; if (!brick.alive) { continue; } if ( ball.x + ball.radius > brick.x && ball.x - ball.radius < brick.x + brickWidth && ball.y + ball.radius > brick.y && ball.y - ball.radius < brick.y + brickHeight ) { brick.alive = false; ball.dy = -ball.dy; score += 10; if (score === rows * columns * 10) { gameClear = true; } } } } } // ==================== // 공 리셋 // ==================== function resetBall() { ball.x = canvas.width / 2; ball.y = 570; ball.dx = 4; ball.dy = -4; paddle.x = (canvas.width - paddle.width) / 2; } // ==================== // 게임 메시지 // ==================== function showMessage(title, subtitle) { ctx.fillStyle = "rgba(0, 0, 0, 0.75)"; ctx.fillRect( 0, 0, canvas.width, canvas.height ); ctx.textAlign = "center"; ctx.fillStyle = "white"; ctx.font = "45px Arial"; ctx.fillText( title, canvas.width / 2, canvas.height / 2 ); ctx.font = "18px Arial"; ctx.fillText( subtitle, canvas.width / 2, canvas.height / 2 + 40 ); ctx.textAlign = "left"; } // ==================== // 게임 재시작 // ==================== function restartGame() { score = 0; lives = 3; gameOver = false; gameClear = false; createBricks(); resetBall(); gameLoop(); } // ==================== // 게임 루프 // ==================== function gameLoop() { ctx.clearRect( 0, 0, canvas.width, canvas.height ); drawInformation(); drawBricks(); drawBall(); drawPaddle(); if (gameOver) { showMessage( "GAME OVER", "Space를 눌러 다시 시작" ); return; } if (gameClear) { showMessage( "🎉 CLEAR!", "Space를 눌러 다시 시작" ); return; } collisionDetection(); // 벽 충돌 if ( ball.x + ball.dx > canvas.width - ball.radius || ball.x + ball.dx < ball.radius ) { ball.dx = -ball.dx; } if ( ball.y + ball.dy < ball.radius ) { ball.dy = -ball.dy; } // 패들 충돌 if ( ball.y + ball.radius >= paddle.y && ball.y - ball.radius <= paddle.y + paddle.height && ball.x >= paddle.x && ball.x <= paddle.x + paddle.width && ball.dy > 0 ) { ball.dy = -Math.abs(ball.dy); // 패들 어느 부분에 맞았는지에 따라 // 공의 방향을 변경 let hitPosition = (ball.x - paddle.x) / paddle.width; ball.dx = (hitPosition - 0.5) * 10; } // 바닥에 떨어짐 if ( ball.y - ball.radius > canvas.height ) { lives--; if (lives <= 0) { gameOver = true; } else { resetBall(); } } // 패들 이동 if (leftPressed) { paddle.x -= paddle.speed; } if (rightPressed) { paddle.x += paddle.speed; } // 패들이 화면 밖으로 나가지 않도록 함 if (paddle.x < 0) { paddle.x = 0; } if ( paddle.x + paddle.width > canvas.width ) { paddle.x = canvas.width - paddle.width; } // 공 이동 ball.x += ball.dx; ball.y += ball.dy; requestAnimationFrame(gameLoop); } // 게임 시작 gameLoop(); </script> </body> </html> """

components.html(
html_code,
height=700,
scrolling=False
)
"""

3. requirements.txt

GitHub에 requirements.txt 파일도 만들고 다음 한 줄만 넣으세요.

streamlit

4. GitHub에 올리기

GitHub에서 새 Repository를 만든 다음:

app.py 파일 생성

위의 app.py 코드 전체 복사

requirements.txt 파일 생성

streamlit 입력

두 파일을 Commit합니다.

최종적으로:

📁 brick-breaker
   ├── 📄 app.py
   └── 📄 requirements.txt


가 되면 됩니다.

5. Streamlit에서 실행하기

Streamlit Cloud에서 GitHub 저장소를 연결하고 다음과 같이 설정하면 됩니다.

Repository: 내 GitHub 저장소
Branch: main
Main file: app.py


배포가 완료되면 웹 주소가 생성되고, 그 주소로 들어가서 바로 게임을 할 수 있습니다.

현재 게임 기능

🧱 48개의 벽돌

🎮 ← → 패들 조작

🏓 공과 벽돌 충돌

💯 점수 시스템

❤️ 목숨 3개

🎉 클리어 화면

💀 게임 오버 화면

🔄 Space로 재시작

🌐 Streamlit을 통한 웹 실행

원하시면 다음 답변에서 **"진짜 게임처럼 보이는 버전"**으로 바꿔서 시작 화면 + 레벨 1~5 + 공 속도 증가 + 아이템 + 목숨 아이콘 + 모바일 터치 버튼 + 최고점수까지 넣은 app.py 전체 코드를 만들어드릴게요.
