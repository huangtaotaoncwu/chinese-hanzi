import streamlit as st
import json
import random
from data.dict import CHINESE_TO_PINYIN

st.set_page_config(page_title="汉字消消乐", page_icon="🎯", layout="wide")

# 隐藏部分默认元素，但保留侧边栏切换
st.markdown(
    """
<style>
    /* 与 theme 一致，避免左侧菜单切换时整页白屏闪烁 */
    .stApp, [data-testid="stAppViewContainer"], main { background-color: #f0f2f6 !important; }
    [data-testid="stStatusWidget"] { visibility: hidden !important; height: 0 !important; overflow: hidden !important; }
    .block-container { animation: stPageFadeIn 0.2s ease-out; }
    @keyframes stPageFadeIn { from { opacity: 0; } to { opacity: 1; } }
    .block-container { padding-top: 1rem; padding-bottom: 0; max-width: 100%; }
    footer { visibility: hidden; }
    [data-testid="stSidebarNav"] span { font-weight: 500; font-size: 1.125rem !important; }
    [data-testid="stSidebarNav"] li { padding: 8px 0; }
</style>
""",
    unsafe_allow_html=True,
)

# 侧栏由入口 汉字乐园.py 统一绘制，本页不再输出侧栏，避免切换时侧栏刷新

# 检测是否需要自动开始（从"再玩一次"跳转过来）
_auto_start = "autostart" in st.query_params
if _auto_start:
    st.query_params.clear()

# 生成汉字数据
all_chars = list(CHINESE_TO_PINYIN.keys())
if len(all_chars) < 20:
    st.error("字表中汉字不足，无法开始游戏。")
else:
    # 随机选择汉字并包含拼音信息
    selected_chars = random.sample(all_chars, min(50, len(all_chars)))
    chars_with_pinyin = {char: CHINESE_TO_PINYIN[char][0] for char in selected_chars}

    data_json = json.dumps(
        {
            "allChars": selected_chars,
            "charPinyin": chars_with_pinyin,
            "autoStart": _auto_start,
        },
        ensure_ascii=False,
    )

    html_template = """
    <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    
    .game-container {
        width: 100%;
        height: 700px;
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        position: relative;
        overflow: hidden;
        border-radius: 16px;
        font-family: 'Helvetica Neue', Arial, sans-serif;
        padding-top: 8px;
        box-sizing: border-box;
    }
    
    /* 顶部状态栏：与练页面保持一致（g-topbar / g-topbar-item / g-end-btn） */
    .g-topbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 18px 24px 12px;
        flex-shrink: 0;
    }
    .g-topbar-item {
        display: flex;
        align-items: center;
        gap: 8px;
        background: rgba(255,255,255,0.18);
        backdrop-filter: blur(6px);
        padding: 8px 18px;
        border-radius: 20px;
        color: #fff;
        font-weight: 700;
        font-size: 14px;
    }
    .g-topbar-item .num { color: #ffd54f; font-size: 20px; margin-left: 4px; }
    .g-topbar-item.warning { background: rgba(255,107,107,0.8); animation: pulse 0.5s infinite; }
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    .g-end-btn {
        background: rgba(255,80,80,0.7);
        backdrop-filter: blur(6px);
        border: none;
        color: #fff;
        padding: 8px 18px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.2s;
    }
    .g-end-btn:hover { background: rgba(255,60,60,0.9); }
    
    /* 汉字显示区域 */
    .hanzi-area {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 15px;
        padding: 20px 40px;
        min-height: 350px;
        align-content: flex-start;
    }
    
    /* 汉字卡片 */
    .hanzi-card {
        width: 80px;
        height: 80px;
        background: linear-gradient(145deg, #ffffff, #f0f0f0);
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 42px;
        font-weight: bold;
        color: #333;
        cursor: pointer;
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        transition: all 0.2s ease;
        font-family: "KaiTi", "楷体", serif;
        position: relative;
    }
    
    .hanzi-card:hover {
        transform: translateY(-5px) scale(1.05);
        box-shadow: 0 12px 30px rgba(0,0,0,0.25);
    }
    
    .hanzi-card:active {
        transform: scale(0.95);
    }
    
    .hanzi-card.correct {
        animation: correctAnim 0.6s ease forwards;
    }
    
    .hanzi-card.wrong {
        animation: wrongAnim 0.5s ease;
    }
    
    .hanzi-card .wrong-icon {
        position: absolute;
        font-size: 50px;
        animation: popIn 0.3s ease;
    }
    
    @keyframes correctAnim {
        0% { transform: scale(1); }
        30% { transform: scale(1.3); background: #4CAF50; color: white; }
        100% { transform: scale(0); opacity: 0; }
    }
    
    @keyframes wrongAnim {
        0%, 100% { transform: translateX(0); }
        20% { transform: translateX(-15px); background: #ff6b6b; }
        40% { transform: translateX(15px); }
        60% { transform: translateX(-15px); }
        80% { transform: translateX(15px); }
    }
    
    @keyframes popIn {
        0% { transform: scale(0); }
        50% { transform: scale(1.3); }
        100% { transform: scale(1); }
    }
    
    /* 飘出的汉字阴影 */
    .flying-char {
        position: absolute;
        font-size: 60px;
        font-weight: bold;
        font-family: "KaiTi", "楷体", serif;
        color: rgba(255,255,255,0.95);
        text-shadow: 0 4px 20px rgba(0,0,0,0.4), 0 0 40px rgba(102,126,234,0.6);
        z-index: 999;
        pointer-events: none;
        transition: all 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    }
    
    .flying-char.from-top {
        animation: flyFromTop 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94) forwards;
    }
    
    .flying-char.from-bottom {
        animation: flyFromBottom 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94) forwards;
    }
    
    @keyframes flyFromTop {
        0% { transform: scale(1) translateY(0); opacity: 1; }
        100% { transform: scale(1.2) translateY(var(--fly-distance)); opacity: 1; }
    }
    
    @keyframes flyFromBottom {
        0% { transform: scale(1) translateY(0); opacity: 1; }
        100% { transform: scale(1.2) translateY(var(--fly-distance)); opacity: 1; }
    }
    
    /* 碰撞效果 */
    .collision-effect {
        position: absolute;
        z-index: 1000;
        pointer-events: none;
        animation: collisionPop 0.6s ease-out forwards;
    }
    
    .collision-effect.success {
        font-size: 80px;
    }
    
    .collision-effect.fail {
        font-size: 100px;
    }
    
    @keyframes collisionPop {
        0% { transform: scale(0) rotate(-10deg); opacity: 0; }
        30% { transform: scale(1.4) rotate(5deg); opacity: 1; }
        50% { transform: scale(1.2) rotate(-3deg); opacity: 1; }
        70% { transform: scale(1.3) rotate(2deg); opacity: 1; }
        100% { transform: scale(0) rotate(0deg); opacity: 0; }
    }
    
    /* 碰撞光环 */
    .collision-ring {
        position: absolute;
        width: 20px;
        height: 20px;
        border-radius: 50%;
        border: 4px solid;
        z-index: 998;
        pointer-events: none;
        animation: ringExpand 0.6s ease-out forwards;
    }
    
    .collision-ring.success {
        border-color: #4CAF50;
        box-shadow: 0 0 20px #4CAF50;
    }
    
    .collision-ring.fail {
        border-color: #ff6b6b;
        box-shadow: 0 0 20px #ff6b6b;
    }
    
    @keyframes ringExpand {
        0% { transform: translate(-50%, -50%) scale(1); opacity: 1; }
        100% { transform: translate(-50%, -50%) scale(8); opacity: 0; }
    }
    
    /* 目标汉字区域 */
    .target-area {
        position: absolute;
        bottom: 30px;
        left: 50%;
        transform: translateX(-50%);
        text-align: center;
    }
    
    .target-label {
        color: rgba(255,255,255,0.8);
        font-size: 18px;
        margin-bottom: 15px;
        text-align: center;
        display: block;
        width: 100%;
    }
    
    .target-char {
        width: 120px;
        height: 120px;
        background: linear-gradient(145deg, #ffd54f, #ffb300);
        border-radius: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 70px;
        font-weight: bold;
        color: #333;
        box-shadow: 0 10px 40px rgba(255,213,79,0.5);
        font-family: "KaiTi", "楷体", serif;
        animation: targetPulse 2s ease-in-out infinite;
    }
    
    @keyframes targetPulse {
        0%, 100% { box-shadow: 0 10px 40px rgba(255,213,79,0.5); }
        50% { box-shadow: 0 15px 50px rgba(255,213,79,0.8); }
    }
    
    /* 连击显示：置于汉字卡片之上，避免被遮挡 */
    .combo {
        position: absolute;
        top: 80px;
        right: 30px;
        z-index: 200;
        color: #ffd54f;
        font-size: 24px;
        font-weight: bold;
        opacity: 0;
        transition: all 0.3s ease;
        pointer-events: none;
    }
    
    .combo.show {
        opacity: 1;
        animation: comboAnim 0.3s ease;
    }
    
    @keyframes comboAnim {
        0% { transform: scale(0.5); }
        50% { transform: scale(1.2); }
        100% { transform: scale(1); }
    }
    
    /* 开始遮罩 */
    .start-overlay {
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        z-index: 1000;
        border-radius: 16px;
    }
    
    .start-overlay h2 {
        font-size: 48px;
        margin-bottom: 20px;
        color: white;
    }
    
    .start-overlay p {
        font-size: 20px;
        color: rgba(255,255,255,0.8);
        margin-bottom: 40px;
        text-align: center;
        line-height: 1.8;
    }
    
    .start-btn {
        padding: 18px 60px;
        font-size: 24px;
        font-weight: bold;
        background: linear-gradient(135deg, #ffd54f, #ffb300);
        color: #333;
        border: none;
        border-radius: 35px;
        cursor: pointer;
        box-shadow: 0 8px 30px rgba(255,213,79,0.5);
        transition: all 0.3s ease;
    }
    
    .start-btn:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 12px 40px rgba(255,213,79,0.7);
    }
    
    /* 结果弹窗 */
    .result-modal {
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: rgba(0,0,0,0.85);
        display: none;
        align-items: center;
        justify-content: center;
        z-index: 1000;
    }
    
    .result-content {
        background: white;
        padding: 50px 60px;
        border-radius: 25px;
        text-align: center;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    }
    
    .result-content h2 {
        font-size: 36px;
        margin-bottom: 10px;
        color: #333;
    }
    
    .result-content .subtitle {
        color: #666;
        font-size: 18px;
        margin-bottom: 30px;
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
        margin-bottom: 30px;
    }
    
    .stat-item {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        padding: 20px;
        border-radius: 15px;
    }
    
    .stat-item .value {
        font-size: 36px;
        font-weight: bold;
        color: #667eea;
    }
    
    .stat-item .label {
        font-size: 14px;
        color: #666;
        margin-top: 5px;
    }
    
    .result-content button {
        padding: 15px 50px;
        font-size: 20px;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 30px;
        cursor: pointer;
        margin: 8px;
        transition: all 0.3s ease;
    }
    
    .result-content button:hover {
        transform: scale(1.05);
    }
    
    /* 彩带粒子 */
    .confetti {
        position: absolute;
        pointer-events: none;
        z-index: 500;
    }
    
    @keyframes confettiFall {
        0% { transform: translateY(0) rotate(0deg); opacity: 1; }
        100% { transform: translateY(600px) rotate(720deg); opacity: 0; }
    }
    </style>
    
    <div class="game-container" id="game-container">
        <!-- 开始遮罩 -->
        <div class="start-overlay" id="start-overlay">
            <h2>🎯 汉字消消乐</h2>
            <p>在30秒内点击与下方目标匹配的汉字<br>连续正确可获得连击加分！</p>
            <button class="start-btn" onclick="startGame()">开始游戏</button>
        </div>
        
        <!-- 顶部状态栏（与练页面一致） -->
        <div class="g-topbar">
            <div class="g-topbar-item" id="timer-panel">⏱️ 剩余：<span id="timer">30</span>秒</div>
            <div class="g-topbar-item">🏆 得分：<span class="num" id="score">0</span></div>
            <button class="g-end-btn" id="end-btn" onclick="endGame(false)" style="display:none;">🛑 结束</button>
        </div>
        
        <!-- 连击显示 -->
        <div class="combo" id="combo">🔥 连击 x<span id="combo-count">0</span></div>
        
        <!-- 汉字显示区域 -->
        <div class="hanzi-area" id="hanzi-area"></div>
        
        <!-- 目标汉字区域 -->
        <div class="target-area">
            <div class="target-char" id="target-char">字</div>
        </div>
        
        <!-- 结果弹窗 -->
        <div class="result-modal" id="result-modal">
            <div class="result-content">
                <h2 id="result-title">🎉 时间到！</h2>
                <div class="subtitle">游戏结束</div>
                <div class="stats-grid">
                    <div class="stat-item">
                        <div class="value" id="final-score">0</div>
                        <div class="label">总得分</div>
                    </div>
                    <div class="stat-item">
                        <div class="value" id="final-correct">0</div>
                        <div class="label">正确数</div>
                    </div>
                    <div class="stat-item">
                        <div class="value" id="final-combo">0</div>
                        <div class="label">最高连击</div>
                    </div>
                </div>
                <button onclick="restartGame()">🔄 再玩一次</button>
            </div>
        </div>
    </div>
    
    <script>
    const DATA = @@DATA_JSON@@;
    const allChars = DATA.allChars;
    const charPinyin = DATA.charPinyin;
    
    let score = 0;
    let correctCount = 0;
    let combo = 0;
    let maxCombo = 0;
    let timeLeft = 30;
    let gameStarted = false;
    let timerInterval = null;
    let startDelayTimeout = null; // 开始游戏后的延时（生成第一轮 + 计时器）
    let targetChar = '';
    let displayedChars = [];
    let pinyinTimeout = null;  // 首次发音延时
    let pinyinInterval = null; // 拼音循环播放定时器
    let processing = false; // 防止动画期间重复点击
    
    const container = document.getElementById('game-container');
    const hanziArea = document.getElementById('hanzi-area');
    const targetCharEl = document.getElementById('target-char');
    const scoreEl = document.getElementById('score');
    const timerEl = document.getElementById('timer');
    const timerPanel = document.getElementById('timer-panel');
    const comboEl = document.getElementById('combo');
    const comboCountEl = document.getElementById('combo-count');
    
    // 生成新一轮汉字
    function generateRound() {
        // 随机选择8个汉字
        const shuffled = [...allChars].sort(() => Math.random() - 0.5);
        displayedChars = shuffled.slice(0, 8);
        
        // 随机选择一个作为目标
        targetChar = displayedChars[Math.floor(Math.random() * displayedChars.length)];
        targetCharEl.innerText = targetChar;
        
        // 清空并重新渲染汉字区域
        hanziArea.innerHTML = '';
        displayedChars.forEach((char, index) => {
            const card = document.createElement('div');
            card.className = 'hanzi-card';
            card.innerText = char;
            card.dataset.char = char;
            card.onclick = () => handleClick(card, char);
            hanziArea.appendChild(card);
        });
        
        // 开始循环播放目标汉字拼音
        startPinyinLoop();
    }
    
    // 处理点击
    function handleClick(card, char) {
        if (!gameStarted || processing) return;
        processing = true;
        
        // 获取位置信息
        const containerRect = container.getBoundingClientRect();
        const cardRect = card.getBoundingClientRect();
        const targetRect = targetCharEl.getBoundingClientRect();
        
        // 计算碰撞点（中间位置）
        const cardCenterX = cardRect.left - containerRect.left + cardRect.width / 2;
        const cardCenterY = cardRect.top - containerRect.top + cardRect.height / 2;
        const targetCenterX = targetRect.left - containerRect.left + targetRect.width / 2;
        const targetCenterY = targetRect.top - containerRect.top + targetRect.height / 2;
        const collisionX = (cardCenterX + targetCenterX) / 2;
        const collisionY = (cardCenterY + targetCenterY) / 2;
        
        // 创建从上方飘出的汉字阴影
        const flyingTop = document.createElement('div');
        flyingTop.className = 'flying-char from-top';
        flyingTop.innerText = char;
        flyingTop.style.left = cardCenterX + 'px';
        flyingTop.style.top = cardCenterY + 'px';
        flyingTop.style.setProperty('--fly-distance', (collisionY - cardCenterY) + 'px');
        flyingTop.style.transform = 'translate(-50%, -50%)';
        container.appendChild(flyingTop);
        
        // 创建从下方飘出的目标汉字阴影
        const flyingBottom = document.createElement('div');
        flyingBottom.className = 'flying-char from-bottom';
        flyingBottom.innerText = targetChar;
        flyingBottom.style.left = targetCenterX + 'px';
        flyingBottom.style.top = targetCenterY + 'px';
        flyingBottom.style.setProperty('--fly-distance', (collisionY - targetCenterY) + 'px');
        flyingBottom.style.transform = 'translate(-50%, -50%)';
        container.appendChild(flyingBottom);
        
        // 隐藏原卡片
        card.style.opacity = '0.3';
        
        // 延迟后显示碰撞效果
        setTimeout(() => {
            if (char === targetChar) {
                // 正确匹配
                showCollisionEffect(collisionX, collisionY, true);
                card.classList.add('correct');
                combo++;
                correctCount++;
                
                // 计算得分（基础10分 + 连击加成）
                const comboBonus = Math.min(combo - 1, 5) * 2;
                const points = 10 + comboBonus;
                score += points;
                scoreEl.innerText = score;
                
                // 更新最高连击
                if (combo > maxCombo) maxCombo = combo;
                
                // 显示连击
                if (combo >= 2) {
                    comboCountEl.innerText = combo;
                    comboEl.classList.add('show');
                }
                
                // 播放成功音效和彩带
                playSuccessSound();
                createConfetti(null, collisionX, collisionY);
                
                // 生成新一轮
                setTimeout(() => {
                    processing = false;
                    generateRound();
                }, 400);
            } else {
                // 错误
                showCollisionEffect(collisionX, collisionY, false);
                card.style.opacity = '1';
                card.classList.add('wrong');
                
                // 重置连击
                combo = 0;
                comboEl.classList.remove('show');
                
                playFailSound();
                
                setTimeout(() => {
                    card.classList.remove('wrong');
                    processing = false;
                }, 500);
            }
            
            // 移除飘出的汉字
            flyingTop.remove();
            flyingBottom.remove();
        }, 500);
    }
    
    // 显示碰撞效果
    function showCollisionEffect(x, y, success) {
        // 创建光环
        const ring = document.createElement('div');
        ring.className = 'collision-ring ' + (success ? 'success' : 'fail');
        ring.style.left = x + 'px';
        ring.style.top = y + 'px';
        container.appendChild(ring);
        
        // 创建碰撞图标
        const effect = document.createElement('div');
        effect.className = 'collision-effect ' + (success ? 'success' : 'fail');
        effect.innerText = success ? '✨' : '❌';
        effect.style.left = x + 'px';
        effect.style.top = y + 'px';
        effect.style.transform = 'translate(-50%, -50%)';
        container.appendChild(effect);
        
        // 移除效果
        setTimeout(() => {
            ring.remove();
            effect.remove();
        }, 700);
    }
    
    // 创建彩带效果
    function createConfetti(element, cx, cy) {
        // 如果没有提供坐标，从元素获取
        if (element && (cx === undefined || cy === undefined)) {
            const rect = element.getBoundingClientRect();
            const containerRect = container.getBoundingClientRect();
            cx = rect.left - containerRect.left + rect.width / 2;
            cy = rect.top - containerRect.top + rect.height / 2;
        }
        
        const colors = ['#ff6b6b', '#ffd54f', '#4CAF50', '#2196F3', '#9c27b0', '#ff9800'];
        
        for (let i = 0; i < 30; i++) {
            const confetti = document.createElement('div');
            confetti.className = 'confetti';
            const size = 8 + Math.random() * 10;
            const color = colors[Math.floor(Math.random() * colors.length)];
            const isRibbon = Math.random() > 0.5;
            
            confetti.style.cssText = `
                left: ${cx}px;
                top: ${cy}px;
                width: ${isRibbon ? size/2 : size}px;
                height: ${isRibbon ? size*2 : size}px;
                background: ${color};
                border-radius: ${isRibbon ? '2px' : '50%'};
                animation: confettiFall ${1 + Math.random()}s ease-out forwards;
                transform: translate(${(Math.random() - 0.5) * 200}px, 0);
            `;
            
            container.appendChild(confetti);
            setTimeout(() => confetti.remove(), 1500);
        }
    }
    
    // 开始游戏
    function startGame() {
        gameStarted = true;
        score = 0;
        correctCount = 0;
        combo = 0;
        maxCombo = 0;
        timeLeft = 30;
        
        scoreEl.innerText = '0';
        timerEl.innerText = '30';
        timerPanel.classList.remove('warning');
        comboEl.classList.remove('show');
        
        document.getElementById('start-overlay').style.display = 'none';
        document.getElementById('end-btn').style.display = 'block';
        
        // 延时后再加载第一轮并开始计时，避免一打开就听到汉字发音
        startDelayTimeout = setTimeout(function() {
            startDelayTimeout = null;
            generateRound();
        }, 200);
        
        // 与第一轮同步开始倒计时（200ms 后）
        setTimeout(function() {
            timerInterval = setInterval(() => {
                timeLeft--;
                timerEl.innerText = timeLeft;
                
                if (timeLeft <= 10) {
                    timerPanel.classList.add('warning');
                }
                
                if (timeLeft <= 0) {
                    endGame(true);
                }
            }, 1000);
        }, 200);
    }
    
    // 结束游戏：isTimeUp 为 true 表示时间到，false 表示用户点击结束
    function endGame(isTimeUp) {
        if (!gameStarted && timerInterval === null && !startDelayTimeout) return;
        gameStarted = false;
        if (startDelayTimeout) {
            clearTimeout(startDelayTimeout);
            startDelayTimeout = null;
        }
        clearInterval(timerInterval);
        timerInterval = null;
        stopPinyinLoop();
        
        document.getElementById('end-btn').style.display = 'none';
        
        document.getElementById('final-score').innerText = score;
        document.getElementById('final-correct').innerText = correctCount;
        document.getElementById('final-combo').innerText = maxCombo;
        
        var title;
        if (isTimeUp) {
            title = '🎉 时间到！';
            if (score >= 200) title = '🏆 太厉害了！';
            else if (score >= 100) title = '🌟 做得好！';
            else if (score >= 50) title = '👍 继续加油！';
        } else {
            title = '🛑 游戏结束';
        }
        
        document.getElementById('result-title').innerText = title;
        document.getElementById('result-modal').style.display = 'flex';
        
        playEndSound();
    }
    
    // 重新开始：在顶层窗口跳转并带 autostart，确保整页刷新后自动开始
    function restartGame() {
        try {
            var topWin = window.top;
            var base = topWin.location.origin + topWin.location.pathname;
            var sep = base.indexOf('?') >= 0 ? '&' : '?';
            var url = base + sep + 'autostart=1';
            topWin.location.assign(url);
        } catch (e) {
            try {
                var u = new URL(window.top.location.href);
                u.searchParams.set('autostart', '1');
                window.top.location.href = u.toString();
            } catch (e2) {
                window.top.location.reload();
            }
        }
    }
    
    // 音效系统
    let audioCtx = null;
    function getAudioContext() {
        if (!audioCtx) {
            audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        }
        return audioCtx;
    }
    
    // 播放汉字发音
    function speakPinyin(char) {
        if (!gameStarted) return;
        
        // 使用 Web Speech API 播放汉字发音
        if ('speechSynthesis' in window) {
            // 停止当前正在播放的语音
            window.speechSynthesis.cancel();
            
            const utterance = new SpeechSynthesisUtterance(char);
            utterance.lang = 'zh-CN';
            utterance.rate = 0.8;
            utterance.pitch = 1.1;
            utterance.volume = 0.8;
            
            // 尝试选择中文语音
            const voices = window.speechSynthesis.getVoices();
            const chineseVoice = voices.find(v => v.lang.includes('zh'));
            if (chineseVoice) {
                utterance.voice = chineseVoice;
            }
            
            window.speechSynthesis.speak(utterance);
        }
    }
    
    // 开始循环播放目标汉字拼音（首次延时播放，避免刚打开就听到声音）
    function startPinyinLoop() {
        stopPinyinLoop();
        // 首次播放延时 1.5 秒，之后每 3 秒播放一次
        pinyinTimeout = setTimeout(function firstSpeak() {
            pinyinTimeout = null;
            if (gameStarted && targetChar) speakPinyin(targetChar);
            pinyinInterval = setInterval(function() {
                if (gameStarted && targetChar) speakPinyin(targetChar);
            }, 3000);
        }, 1500);
    }
    
    // 停止循环播放
    function stopPinyinLoop() {
        if (pinyinTimeout) {
            clearTimeout(pinyinTimeout);
            pinyinTimeout = null;
        }
        if (pinyinInterval) {
            clearInterval(pinyinInterval);
            pinyinInterval = null;
        }
        if ('speechSynthesis' in window) {
            window.speechSynthesis.cancel();
        }
    }
    
    // 确保语音列表加载完成
    if ('speechSynthesis' in window) {
        window.speechSynthesis.getVoices();
        window.speechSynthesis.onvoiceschanged = () => {
            window.speechSynthesis.getVoices();
        };
    }
    
    function playSuccessSound() {
        const ctx = getAudioContext();
        const now = ctx.currentTime;
        
        // 根据连击数调整音高
        const baseFreq = 523.25 + (combo * 50);
        const notes = [baseFreq, baseFreq * 1.25, baseFreq * 1.5];
        
        notes.forEach((freq, i) => {
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.frequency.setValueAtTime(Math.min(freq, 2000), now + i * 0.08);
            osc.type = 'sine';
            gain.gain.setValueAtTime(0.25, now + i * 0.08);
            gain.gain.exponentialRampToValueAtTime(0.01, now + i * 0.08 + 0.2);
            osc.start(now + i * 0.08);
            osc.stop(now + i * 0.08 + 0.25);
        });
    }
    
    function playFailSound() {
        const ctx = getAudioContext();
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.frequency.setValueAtTime(200, ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(100, ctx.currentTime + 0.2);
        osc.type = 'square';
        gain.gain.setValueAtTime(0.15, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.2);
        osc.start(ctx.currentTime);
        osc.stop(ctx.currentTime + 0.2);
    }
    
    function playEndSound() {
        const ctx = getAudioContext();
        const now = ctx.currentTime;
        const notes = [392, 440, 494, 523.25];
        
        notes.forEach((freq, i) => {
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.frequency.setValueAtTime(freq, now + i * 0.15);
            osc.type = 'sine';
            gain.gain.setValueAtTime(0.2, now + i * 0.15);
            gain.gain.exponentialRampToValueAtTime(0.01, now + i * 0.15 + 0.4);
            osc.start(now + i * 0.15);
            osc.stop(now + i * 0.15 + 0.5);
        });
    }
    
    // 自动开始检查（由 Python 端传入标志）
    if (DATA.autoStart) {
        setTimeout(startGame, 100);
    }
    </script>
    """

    # 注入数据
    html = html_template.replace("@@DATA_JSON@@", data_json)

    # 嵌入 HTML
    import streamlit.components.v1 as components

    components.html(html, height=750, scrolling=False)
