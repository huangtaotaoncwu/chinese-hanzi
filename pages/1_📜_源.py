import streamlit as st

st.set_page_config(page_title="汉字起源", page_icon="📜", layout="wide")

# 隐藏部分默认元素
st.markdown(
    """
<style>
    /* 与 theme 一致，避免左侧菜单切换时整页白屏闪烁 */
    .stApp, [data-testid="stAppViewContainer"], main { background-color: #f0f2f6 !important; }
    [data-testid="stStatusWidget"] { visibility: hidden !important; height: 0 !important; overflow: hidden !important; }
    .block-container { animation: stPageFadeIn 0.2s ease-out; }
    @keyframes stPageFadeIn { from { opacity: 0; } to { opacity: 1; } }
    .block-container { padding-top: 0.5rem; padding-bottom: 0; max-width: 100%; }
    footer { visibility: hidden; }
    [data-testid="stSidebarNav"] span { font-weight: 500; font-size: 1.125rem !important; }
    [data-testid="stSidebarNav"] li { padding: 8px 0; }
</style>
""",
    unsafe_allow_html=True,
)

# 侧栏由入口 汉字乐园.py 统一绘制，本页不再输出侧栏，避免切换时侧栏刷新

# 背景音乐：仅使用 OSS 地址（若为签名 URL 过期后可在此替换）
BGM_OSS_URL = "https://sanctions.oss-cn-shanghai.aliyuncs.com/music_bg.mp3?OSSAccessKeyId=LTAI4Fh6KKLt4QuqBgdv8DKk&Expires=1804746853&Signature=Q1iQLne8%2BrmDX%2F0TEM9kmXQTz1g%3D"

# 整个页面作为一个大型 HTML 组件
import streamlit.components.v1 as components

html_content = """
<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700;900&display=swap');

* { margin:0; padding:0; box-sizing:border-box; }
body {
    font-family: 'Noto Serif SC', 'STSong', 'SimSun', serif;
    background: #faf6f0;
    color: #3a2e1f;
    overflow-x: hidden;
}

/* ========== 古典背景纹理 ========== */
.page-bg {
    position: fixed; top:0; left:0; right:0; bottom:0;
    background: 
        radial-gradient(ellipse at 20% 50%, rgba(212,165,116,0.08) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 20%, rgba(139,90,43,0.06) 0%, transparent 50%),
        radial-gradient(ellipse at 50% 80%, rgba(200,150,100,0.05) 0%, transparent 50%),
        #faf6f0;
    z-index: -1;
}

/* ========== 音乐控制 ========== */
.music-btn {
    position: absolute;
    top: 55px;
    right: 24px;
    z-index: 9999;
    width: 44px; height: 44px; border-radius: 50%;
    background: linear-gradient(135deg, #d4a574, #8b5a2b);
    border: 2px solid rgba(255,255,255,0.3);
    color: white; font-size: 22px;
    cursor: pointer; display: flex; align-items: center; justify-content: center;
    box-shadow: 0 4px 16px rgba(139,90,43,0.3);
    transition: all 0.3s;
}
.music-btn:hover { transform: scale(1.1); box-shadow: 0 6px 24px rgba(139,90,43,0.4); }
.music-btn.playing { animation: musicPulse 2s ease-in-out infinite; }
@keyframes musicPulse {
    0%,100% { box-shadow: 0 4px 16px rgba(139,90,43,0.3); }
    50% { box-shadow: 0 4px 16px rgba(139,90,43,0.3), 0 0 0 8px rgba(212,165,116,0.2); }
}

/* ========== 标题区 ========== */
.hero {
    text-align: center;
    padding: 50px 20px 40px;
    position: relative;
}
.hero h1 {
    font-size: 52px; font-weight: 900;
    background: linear-gradient(135deg, #8b5a2b, #d4a574, #8b5a2b);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 12px;
    letter-spacing: 8px;
}
.hero .subtitle {
    font-size: 20px; color: #8b7355;
    letter-spacing: 4px;
    font-weight: 400;
}
.hero .divider {
    width: 120px; height: 2px;
    background: linear-gradient(90deg, transparent, #d4a574, transparent);
    margin: 20px auto 0;
}

/* ========== 内容区 ========== */
.content {
    max-width: 900px;
    margin: 0 auto;
    padding: 0 24px 60px;
}

/* ========== 时间线 ========== */
.timeline {
    position: relative;
    padding: 20px 0;
}
.timeline::before {
    content: '';
    position: absolute;
    left: 50%;
    top: 0; bottom: 0;
    width: 3px;
    background: linear-gradient(180deg, #d4a574, #8b5a2b, #d4a574);
    transform: translateX(-50%);
    border-radius: 2px;
}

.era {
    position: relative;
    margin-bottom: 50px;
    display: flex;
    align-items: flex-start;
}
.era:nth-child(odd) { flex-direction: row; }
.era:nth-child(even) { flex-direction: row-reverse; }

.era-dot {
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    width: 20px; height: 20px;
    background: linear-gradient(135deg, #d4a574, #8b5a2b);
    border-radius: 50%;
    border: 3px solid #faf6f0;
    box-shadow: 0 0 0 4px rgba(212,165,116,0.3);
    z-index: 2;
}

.era-card {
    width: 42%;
    background: linear-gradient(135deg, #fff, #fdf8f2);
    border-radius: 16px;
    padding: 28px;
    box-shadow: 0 8px 30px rgba(139,90,43,0.1);
    border: 1px solid rgba(212,165,116,0.2);
    position: relative;
    transition: transform 0.3s, box-shadow 0.3s;
}
.era-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(139,90,43,0.18);
}
.era:nth-child(odd) .era-card { margin-right: auto; margin-left: 0; }
.era:nth-child(even) .era-card { margin-left: auto; margin-right: 0; }

.era-badge {
    display: inline-block;
    background: linear-gradient(135deg, #d4a574, #8b5a2b);
    color: white;
    padding: 4px 16px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 2px;
    margin-bottom: 12px;
}

.era-title {
    font-size: 24px;
    font-weight: 700;
    color: #5a3e28;
    margin-bottom: 8px;
}

.era-period {
    font-size: 13px;
    color: #a08060;
    margin-bottom: 14px;
    font-style: italic;
}

.era-text {
    font-size: 15px;
    line-height: 1.9;
    color: #5a4a3a;
}

.era-chars {
    display: flex;
    gap: 12px;
    margin-top: 16px;
    flex-wrap: wrap;
}

.era-char {
    width: 56px; height: 56px;
    background: linear-gradient(135deg, #fdf8f2, #f0e6d8);
    border: 1px solid #d4a574;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 28px;
    color: #5a3e28;
    font-weight: 700;
    transition: all 0.3s;
}
.era-char:hover {
    transform: scale(1.15) rotate(-5deg);
    box-shadow: 0 4px 16px rgba(139,90,43,0.2);
    background: linear-gradient(135deg, #d4a574, #c49464);
    color: white;
}
/* 古字形图片（甲骨文/金文/小篆等） */
.era-script-sample { display: inline-flex; flex-direction: column; align-items: center; gap: 6px; }
.era-chars .era-script-img {
    width: 64px; height: 64px;
    object-fit: contain;
    border-radius: 8px;
    border: 1px solid #d4a574;
    background: linear-gradient(135deg, #fdf8f2, #f0e6d8);
}
.era-chars .era-script-caption { font-size: 12px; color: #8b7355; }

/* ========== 特色展示区 ========== */
.showcase {
    background: linear-gradient(135deg, #5a3e28, #8b5a2b);
    border-radius: 20px;
    padding: 40px 32px;
    margin: 40px 0;
    color: white;
    text-align: center;
}
.showcase h2 {
    font-size: 30px;
    margin-bottom: 8px;
    letter-spacing: 4px;
}
.showcase .sub {
    font-size: 15px;
    opacity: 0.8;
    margin-bottom: 30px;
}

.evo-grid {
    display: flex;
    justify-content: center;
    gap: 16px;
    flex-wrap: wrap;
}
.evo-item {
    background: rgba(255,255,255,0.1);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 14px;
    padding: 20px 16px;
    width: 120px;
    text-align: center;
    transition: all 0.3s;
    backdrop-filter: blur(4px);
}
.evo-item:hover {
    background: rgba(255,255,255,0.2);
    transform: translateY(-4px);
}
.evo-item .evo-stage { font-size: 12px; opacity:0.7; margin-bottom:6px; }
.evo-item .evo-char { font-size: 36px; margin-bottom: 6px; }
.evo-item .evo-char img { width: 72px; height: 72px; object-fit: contain; vertical-align: middle; }
.evo-item .evo-label { font-size: 13px; font-weight: 600; }
.showcase .evo-evolution-img { max-width: 100%; width: 480px; height: auto; border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.15); }

.evo-arrow {
    display: flex; align-items: center; font-size: 24px; opacity: 0.5;
}

/* ========== 六书介绍 ========== */
.liushu {
    margin: 40px 0;
}
.liushu h2 {
    text-align: center;
    font-size: 30px;
    color: #5a3e28;
    margin-bottom: 8px;
    letter-spacing: 4px;
}
.liushu .sub {
    text-align: center;
    font-size: 15px;
    color: #a08060;
    margin-bottom: 30px;
}
.liushu-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
}
.liushu-card {
    background: linear-gradient(135deg, #fff, #fdf8f2);
    border-radius: 14px;
    padding: 24px 20px;
    border: 1px solid rgba(212,165,116,0.2);
    box-shadow: 0 4px 16px rgba(139,90,43,0.06);
    text-align: center;
    transition: all 0.3s;
}
.liushu-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 30px rgba(139,90,43,0.12);
}
.liushu-icon { font-size: 36px; margin-bottom: 10px; }
.liushu-name { font-size: 20px; font-weight: 700; color: #5a3e28; margin-bottom: 6px; }
.liushu-desc { font-size: 13px; color: #7a6a5a; line-height: 1.7; }
.liushu-example {
    margin-top: 10px;
    display: inline-block;
    background: linear-gradient(135deg, #f0e6d8, #fdf8f2);
    padding: 4px 14px;
    border-radius: 16px;
    font-size: 16px;
    color: #8b5a2b;
    font-weight: 600;
}

/* ========== 趣味数字 ========== */
.fun-facts {
    display: flex;
    gap: 16px;
    margin: 40px 0;
    flex-wrap: wrap;
    justify-content: center;
}
.fact-card {
    background: linear-gradient(135deg, #fff, #fdf8f2);
    border-radius: 14px;
    padding: 24px;
    text-align: center;
    flex: 1;
    min-width: 180px;
    border: 1px solid rgba(212,165,116,0.2);
    box-shadow: 0 4px 16px rgba(139,90,43,0.06);
}
.fact-num { font-size: 36px; font-weight: 900; color: #d4a574; }
.fact-label { font-size: 13px; color: #8b7355; margin-top: 6px; }

/* ========== 尾部 ========== */
.footer-quote {
    text-align: center;
    padding: 40px 20px;
    font-size: 18px;
    color: #a08060;
    font-style: italic;
    letter-spacing: 2px;
    border-top: 1px solid rgba(212,165,116,0.2);
    margin-top: 20px;
}

/* ========== 响应式 ========== */
@media (max-width: 768px) {
    .timeline::before { left: 20px; }
    .era { flex-direction: column !important; padding-left: 50px; }
    .era-dot { left: 20px; }
    .era-card { width: 100% !important; margin: 0 !important; }
    .liushu-grid { grid-template-columns: repeat(2, 1fr); }
    .hero h1 { font-size: 36px; }
}
</style>
</head>
<body>
<div class="page-bg"></div>

<!-- 标题区 -->
<div class="hero">
    <button class="music-btn playing" id="musicBtn" onclick="toggleMusic()" title="播放/暂停古典音乐">🎵</button>
    <h1>汉字起源</h1>
    <div class="subtitle">从结绳记事到书写文明</div>
    <div class="divider"></div>
</div>

<div class="content">

    <!-- 趣味数字 -->
    <div class="fun-facts">
        <div class="fact-card">
            <div class="fact-num">6000+</div>
            <div class="fact-label">年 · 汉字历史</div>
        </div>
        <div class="fact-card">
            <div class="fact-num">85,568</div>
            <div class="fact-label">字 · 收录于《康熙字典》</div>
        </div>
        <div class="fact-card">
            <div class="fact-num">3,500</div>
            <div class="fact-label">字 · 日常使用汉字</div>
        </div>
        <div class="fact-card">
            <div class="fact-num">14亿+</div>
            <div class="fact-label">人 · 使用汉字</div>
        </div>
    </div>

    <!-- 时间线 -->
    <div class="timeline">

        <!-- 结绳记事 -->
        <div class="era">
            <div class="era-dot"></div>
            <div class="era-card">
                <div class="era-badge">🪢 远古时期</div>
                <div class="era-title">结绳记事与刻画符号</div>
                <div class="era-period">约公元前6000年 — 公元前2000年</div>
                <div class="era-text">
                    在文字诞生之前，先民们用<strong>结绳记事</strong>的方式记录事物的数量和大小。
                    大事结大绳，小事结小绳。后来，人们开始在陶器上刻画简单的符号，
                    这些<strong>陶文符号</strong>被认为是汉字最早的萌芽。
                    半坡遗址出土的陶器上就有数十种刻画符号。
                </div>
                <div class="era-chars">
                    <div class="era-char">☰</div>
                    <div class="era-char">☷</div>
                    <div class="era-char">〇</div>
                    <div class="era-char">卜</div>
                </div>
            </div>
        </div>

        <!-- 甲骨文 -->
        <div class="era">
            <div class="era-dot"></div>
            <div class="era-card">
                <div class="era-badge">🦴 商朝</div>
                <div class="era-title">甲骨文 — 最早的成熟文字</div>
                <div class="era-period">约公元前1600年 — 公元前1046年</div>
                <div class="era-text">
                    商朝人将文字刻在<strong>龟甲和兽骨</strong>上，用来占卜吉凶，这就是甲骨文。
                    1899年，金石学家王懿荣首次发现甲骨文，震惊世界。
                    目前已发现甲骨文单字约<strong>4,500个</strong>，已识别约1,500个。
                    甲骨文是一种<strong>象形为主</strong>的文字，"日"像太阳，"月"像弯月，"山"像山峰。
                </div>
                <div class="era-chars">
                    <div class="era-script-sample">
                        <img src="https://upload.wikimedia.org/wikipedia/commons/5/50/%E9%A6%AC-oracle.svg" alt="马-甲骨文" class="era-script-img" title="马（甲骨文）">
                        <span class="era-script-caption">示例：马</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- 金文 -->
        <div class="era">
            <div class="era-dot"></div>
            <div class="era-card">
                <div class="era-badge">🏺 西周</div>
                <div class="era-title">金文 — 青铜器上的铭文</div>
                <div class="era-period">约公元前1046年 — 公元前771年</div>
                <div class="era-text">
                    西周时期，人们将文字铸刻在<strong>青铜器</strong>（钟鼎）上，称为金文或钟鼎文。
                    金文比甲骨文更加<strong>规范美观</strong>，笔画更加圆润饱满。
                    著名的毛公鼎上刻有近500字的铭文，是目前已知字数最多的西周青铜器铭文。
                    金文记录了祭祀、战争、封赏等重要事件。
                </div>
                <div class="era-chars">
                    <div class="era-script-sample">
                        <img src="https://upload.wikimedia.org/wikipedia/commons/1/18/%E9%A6%AC-bronze.svg" alt="马-金文" class="era-script-img" title="马（金文）">
                        <span class="era-script-caption">示例：马</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- 篆书 -->
        <div class="era">
            <div class="era-dot"></div>
            <div class="era-card">
                <div class="era-badge">📜 秦朝</div>
                <div class="era-title">小篆 — 书同文的统一</div>
                <div class="era-period">公元前221年 — 公元前207年</div>
                <div class="era-text">
                    秦始皇统一六国后，命丞相<strong>李斯</strong>主持文字统一工作，
                    以秦国的文字为基础，创制了<strong>小篆</strong>。
                    "书同文"是中国历史上第一次大规模的文字规范化运动，
                    对汉字的统一和传播产生了深远影响。小篆线条均匀，结构对称，是书法艺术的重要字体。
                </div>
                <div class="era-chars">
                    <div class="era-script-sample">
                        <img src="https://upload.wikimedia.org/wikipedia/commons/3/3a/%E9%A6%AC-seal.svg" alt="马-小篆" class="era-script-img" title="马（小篆）">
                        <span class="era-script-caption">示例：马</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- 隶书 -->
        <div class="era">
            <div class="era-dot"></div>
            <div class="era-card">
                <div class="era-badge">📝 汉朝</div>
                <div class="era-title">隶书 — 古今文字的分水岭</div>
                <div class="era-period">公元前206年 — 公元220年</div>
                <div class="era-text">
                    隶书在秦末汉初逐渐成熟，是汉字从<strong>古文字</strong>演变为<strong>今文字</strong>的关键转折。
                    隶书将篆书圆转的笔画变为<strong>方折</strong>，书写更加便捷高效。
                    "蚕头燕尾"是隶书最显著的特征——起笔如蚕头圆润，收笔如燕尾舒展。
                    汉朝是隶书的鼎盛时期，故隶书也被称为"汉隶"。
                </div>
                <div class="era-chars">
                    <div class="era-script-sample">
                        <div class="era-char">馬</div>
                        <span class="era-script-caption">示例：马（隶书）</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- 楷书 -->
        <div class="era">
            <div class="era-dot"></div>
            <div class="era-card">
                <div class="era-badge">✍️ 魏晋至今</div>
                <div class="era-title">楷书 — 今天使用的汉字</div>
                <div class="era-period">公元3世纪 — 至今</div>
                <div class="era-text">
                    楷书形成于魏晋时期，由隶书演变而来，笔画<strong>平直规范</strong>，结构方正。
                    "楷"即"楷模"之意，表示这种字体可以作为书写的标准。
                    唐朝是楷书的黄金时代，<strong>颜真卿、柳公权、欧阳询、赵孟頫</strong>
                    被尊为"楷书四大家"。楷书沿用至今，是我们日常书写和印刷的标准字体。
                </div>
                <div class="era-chars">
                    <div class="era-script-sample">
                        <div class="era-char">马</div>
                        <span class="era-script-caption">示例：马（楷书/今体）</span>
                    </div>
                </div>
            </div>
        </div>

    </div>

    <!-- 汉字演变展示（使用 Wikimedia 正确字形图） -->
    <div class="showcase">
        <h2>汉字演变之旅</h2>
        <div class="sub">以"马"字为例，看看汉字如何一步步演变</div>
        <div class="evo-grid">
            <div class="evo-item">
                <div class="evo-stage">甲骨文</div>
                <div class="evo-char"><img src="https://upload.wikimedia.org/wikipedia/commons/5/50/%E9%A6%AC-oracle.svg" alt="马-甲骨文"></div>
                <div class="evo-label">象形画马</div>
            </div>
            <div class="evo-arrow">→</div>
            <div class="evo-item">
                <div class="evo-stage">金文</div>
                <div class="evo-char"><img src="https://upload.wikimedia.org/wikipedia/commons/1/18/%E9%A6%AC-bronze.svg" alt="马-金文"></div>
                <div class="evo-label">线条简化</div>
            </div>
            <div class="evo-arrow">→</div>
            <div class="evo-item">
                <div class="evo-stage">小篆</div>
                <div class="evo-char"><img src="https://upload.wikimedia.org/wikipedia/commons/3/3a/%E9%A6%AC-seal.svg" alt="马-小篆"></div>
                <div class="evo-label">结构规范</div>
            </div>
            <div class="evo-arrow">→</div>
            <div class="evo-item">
                <div class="evo-stage">隶书</div>
                <div class="evo-char">馬</div>
                <div class="evo-label">笔画方折</div>
            </div>
            <div class="evo-arrow">→</div>
            <div class="evo-item">
                <div class="evo-stage">楷书</div>
                <div class="evo-char">马</div>
                <div class="evo-label">今日写法</div>
            </div>
        </div>
        <p style="text-align:center; font-size:12px; color:rgba(255,255,255,0.7); margin-top:12px;"></p>
    </div>

    <!-- 六书 -->
    <div class="liushu">
        <h2>造字六法 · 六书</h2>
        <div class="sub">古人是如何创造汉字的？</div>
        <div class="liushu-grid">
            <div class="liushu-card">
                <div class="liushu-icon">🌄</div>
                <div class="liushu-name">象形</div>
                <div class="liushu-desc">描摹事物的形状<br>最古老的造字法</div>
                <div class="liushu-example">日 月 山 水</div>
            </div>
            <div class="liushu-card">
                <div class="liushu-icon">☝️</div>
                <div class="liushu-name">指事</div>
                <div class="liushu-desc">用符号标记抽象概念</div>
                <div class="liushu-example">上 下 一 二</div>
            </div>
            <div class="liushu-card">
                <div class="liushu-icon">🤝</div>
                <div class="liushu-name">会意</div>
                <div class="liushu-desc">组合两个以上字<br>表达新的意义</div>
                <div class="liushu-example">休 明 林 森</div>
            </div>
            <div class="liushu-card">
                <div class="liushu-icon">🔤</div>
                <div class="liushu-name">形声</div>
                <div class="liushu-desc">一半表意一半表音<br>汉字中占比最大</div>
                <div class="liushu-example">河 铜 花 鸽</div>
            </div>
            <div class="liushu-card">
                <div class="liushu-icon">🔄</div>
                <div class="liushu-name">转注</div>
                <div class="liushu-desc">同部首字互相解释<br>意义相通的字</div>
                <div class="liushu-example">考 老</div>
            </div>
            <div class="liushu-card">
                <div class="liushu-icon">🔀</div>
                <div class="liushu-name">假借</div>
                <div class="liushu-desc">借用已有的字<br>表达新的意义</div>
                <div class="liushu-example">来 自 我</div>
            </div>
        </div>
    </div>

    <!-- 尾部名言 -->
    <div class="footer-quote">
        "仓颉之初作书，盖依类象形，故谓之文。其后形声相益，即谓之字。"<br>
        <span style="font-size:14px; opacity:0.7;">—— 许慎《说文解字》</span>
    </div>

</div>

<!-- 背景音乐：进入页面默认尝试播放，若被浏览器拦截可点击右侧 🎵 开启（使用 OSS URL） -->
<audio id="bgm" loop preload="auto" autoplay style="display:none;">
    <source src="__BGM_OSS_URL__" type="audio/mpeg">
</audio>
<script>
(function () {
    var bgm = document.getElementById("bgm");
    if (!bgm) return;
    bgm.volume = 0.28;
    function setBtn(playing) {
        var btn = document.getElementById("musicBtn");
        if (btn) { btn.classList.toggle("playing", playing); btn.innerText = playing ? "🎵" : "🔇"; }
    }
    bgm.addEventListener("play", function () { setBtn(true); });
    bgm.addEventListener("pause", function () { setBtn(false); });
    bgm.addEventListener("ended", function () { setBtn(false); });
    window.toggleMusic = function () {
        if (bgm.paused) { bgm.play().catch(function () { setBtn(false); }); }
        else bgm.pause();
    };
    setBtn(false);
    // 进入页面默认播放（部分浏览器需用户先与页面交互才允许声音，届时请点 🎵）
    bgm.play().catch(function () { setBtn(false); });
})();
</script>
</body>
</html>
"""

# 注入背景音乐 OSS URL
html_content = html_content.replace("__BGM_OSS_URL__", BGM_OSS_URL)

components.html(html_content, height=4200, scrolling=True)
