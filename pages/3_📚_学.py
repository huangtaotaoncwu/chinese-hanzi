import streamlit as st
import random
from html import escape as html_escape
from data.dict import WORD_TO_LEARN, CHINESE_TO_PINYIN, WORD_TO_CONTENT

st.set_page_config(page_title="汉字学习", page_icon="📚", layout="wide")

# 隐藏部分默认元素，但保留侧边栏切换
st.markdown(
    """
<style>
    /* 与 theme 一致，避免左侧菜单切换时整页白屏闪烁 */
    .stApp, [data-testid="stAppViewContainer"], main { background-color: #f0f2f6 !important; }
    [data-testid="stStatusWidget"] { visibility: hidden !important; height: 0 !important; overflow: hidden !important; }
    .block-container { animation: stPageFadeIn 0.2s ease-out; }
    @keyframes stPageFadeIn { from { opacity: 0; } to { opacity: 1; } }
    .block-container { padding-top: 1rem; padding-bottom: 0; }
    footer { visibility: hidden; }
    [data-testid="stSidebarNav"] span { font-weight: 500; }
    [data-testid="stSidebarNav"] li { padding: 8px 0; }
</style>
""",
    unsafe_allow_html=True,
)

# 学页侧栏保留随机/下一个/选择汉字，仅去掉标题与返回首页以减轻切换时侧栏刷新

# 获取所有汉字列表
all_words = [item["word"] for item in WORD_TO_LEARN]

# 初始化 session state - 默认选中第一个
if "current_word_index" not in st.session_state:
    st.session_state.current_word_index = 0

# 与 selectbox(key="word_selector") 同步，避免只改 current_word_index 时界面不更新
st.session_state.word_selector = all_words[st.session_state.current_word_index]

# 随机选择 和 下一个 按钮
sb_col1, sb_col2 = st.sidebar.columns(2)
with sb_col1:
    if st.button("🎲 随机", use_container_width=True, key="sidebar_random"):
        new_index = random.randint(0, len(WORD_TO_LEARN) - 1)
        st.session_state.current_word_index = new_index
        st.rerun()
with sb_col2:
    if st.button("⏭️ 下一个", use_container_width=True, key="sidebar_next"):
        next_index = (st.session_state.current_word_index + 1) % len(WORD_TO_LEARN)
        st.session_state.current_word_index = next_index
        st.rerun()


# 下拉选择汉字
def on_select_change():
    selected = st.session_state.word_selector
    for i, item in enumerate(WORD_TO_LEARN):
        if item["word"] == selected:
            st.session_state.current_word_index = i
            break


selected_word = st.sidebar.selectbox(
    "选择汉字",
    options=all_words,
    key="word_selector",
    on_change=on_select_change,
)

current = WORD_TO_LEARN[st.session_state.current_word_index]

# 嵌入 HTML 显示田字格和汉字
html_template = """
<script src="https://cdn.jsdelivr.net/npm/hanzi-writer@3.5/dist/hanzi-writer.min.js"></script>
<style>
.learn-container {
    display: flex;
    gap: 40px;
    padding: 20px;
    font-family: 'Helvetica Neue', Arial, sans-serif;
    align-items: flex-start;
    justify-content: center;
    flex-wrap: wrap;
}

/* 发音按钮 - 更大更明显 */
.speak-btn {
    background: linear-gradient(135deg, #ff6b6b, #ee5a5a);
    border: none;
    border-radius: 50%;
    width: 56px;
    height: 56px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 6px 20px rgba(238,90,90,0.4);
    transition: all 0.2s ease;
    font-size: 28px;
}
.speak-btn:hover {
    transform: scale(1.15);
    box-shadow: 0 8px 28px rgba(238,90,90,0.5);
}
.speak-btn:active {
    transform: scale(0.95);
}

/* 重播按钮 - 与喇叭按钮同尺寸 */
.replay-btn {
    background: linear-gradient(135deg, #667eea, #764ba2);
    border: none;
    border-radius: 50%;
    width: 56px;
    height: 56px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 6px 20px rgba(102,126,234,0.4);
    transition: all 0.2s ease;
    font-size: 28px;
}
.replay-btn:hover {
    transform: scale(1.15);
    box-shadow: 0 8px 28px rgba(102,126,234,0.5);
}
.replay-btn:active {
    transform: scale(0.95);
}


/* 小号发音按钮 - 更明显 */
.speak-btn-sm {
    background: linear-gradient(135deg, #ff9a9e, #fecfef);
    border: 2px solid rgba(255,255,255,0.5);
    border-radius: 50%;
    width: 36px;
    height: 36px;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 12px rgba(255,107,107,0.35);
    transition: all 0.2s ease;
    font-size: 18px;
    flex-shrink: 0;
}
.speak-btn-sm:hover {
    transform: scale(1.15);
    box-shadow: 0 6px 18px rgba(255,107,107,0.5);
}
.speak-btn-sm.green {
    background: linear-gradient(135deg, #a8edea, #fed6e3);
    box-shadow: 0 4px 12px rgba(168,237,234,0.4);
}

/* 田字格容器 - 下移至页面中上方 */
.tianzige-container {
    position: relative;
    width: 260px;
    flex-shrink: 0;
    margin-top: 80px;
}

/* 田字格 - 仅保留网格线，无厚重外框 */
.tianzige {
    width: 260px;
    height: 260px;
    border: 1px solid #ccc;
    background: #fff;
    position: relative;
    box-sizing: border-box;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 4px;
    box-shadow: none;
}

/* 田字格十字线 */
.tianzige::before {
    content: "";
    position: absolute;
    width: 100%;
    height: 1px;
    background: linear-gradient(90deg, transparent 0%, #ddd 10%, #ddd 90%, transparent 100%);
    top: 50%;
    left: 0;
    z-index: 1;
}
.tianzige::after {
    content: "";
    position: absolute;
    height: 100%;
    width: 1px;
    background: linear-gradient(180deg, transparent 0%, #ddd 10%, #ddd 90%, transparent 100%);
    left: 50%;
    top: 0;
    z-index: 1;
}

/* 对角虚线 */
.diagonal-lines {
    position: absolute;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
    pointer-events: none;
    z-index: 1;
}
.diagonal-lines::before {
    content: "";
    position: absolute;
    width: 141%;
    height: 1px;
    background: linear-gradient(90deg, transparent 0%, #e8e8e8 10%, #e8e8e8 90%, transparent 100%);
    top: 50%;
    left: -20.5%;
    transform: rotate(45deg);
}
.diagonal-lines::after {
    content: "";
    position: absolute;
    width: 141%;
    height: 1px;
    background: linear-gradient(90deg, transparent 0%, #e8e8e8 10%, #e8e8e8 90%, transparent 100%);
    top: 50%;
    left: -20.5%;
    transform: rotate(-45deg);
}

/* Hanzi Writer 容器 */
#hanzi-writer-container {
    position: relative;
    z-index: 2;
}

/* 词语和例句区域 - 无框，直接铺在页面上 */
.info-section {
    flex: 1;
    min-width: 300px;
    max-width: 700px;
}

.info-card {
    background: transparent;
    border-radius: 0;
    padding: 18px 0 22px 0;
    margin-bottom: 0;
    box-shadow: none;
    border: none;
    border-top: 1px solid #e0e0e0;
}
.info-card:first-child {
    border-top: none;
    padding-top: 0;
}
.info-card + .info-card {
    margin-top: 0;
}

.info-card h3 {
    margin: 0 0 10px 0;
    font-size: 16px;
    color: #444;
    display: flex;
    align-items: center;
    gap: 8px;
}

.info-card h3 .icon {
    font-size: 20px;
}

/* 拼音展示 - 无外框 */
.pinyin-card {}
.pinyin-display {
    display: flex;
    align-items: center;
    gap: 16px;
    flex-wrap: wrap;
}
.pinyin-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 2px;
    background: transparent;
    color: #e65100;
    padding: 8px 18px;
    border-radius: 0;
    box-shadow: none;
    font-weight: 700;
}
.pinyin-item .py-text {
    font-size: 24px;
    font-weight: 700;
    letter-spacing: 2px;
}

.word-list {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}

.word-item {
    background: transparent;
    color: #4527a0;
    padding: 6px 12px 6px 0;
    border-radius: 0;
    font-size: 18px;
    font-weight: 500;
    box-shadow: none;
    display: inline-flex;
    align-items: center;
    gap: 10px;
    border: none;
}
.word-item .speak-btn-sm {
    background: rgba(102,126,234,0.15);
    border: 1px solid rgba(102,126,234,0.3);
    box-shadow: none;
}
.word-item .speak-btn-sm:hover {
    background: rgba(102,126,234,0.25);
}

.sentence-list {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.sentence-item {
    background: transparent;
    color: #00695c;
    padding: 10px 0 10px 0;
    border-radius: 0;
    font-size: 18px;
    font-weight: 500;
    line-height: 1.6;
    box-shadow: none;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    border: none;
}
.sentence-item .text {
    flex: 1;
    font-size: 18px;
    font-weight: 500;
}
.sentence-item .speak-btn-sm {
    background: rgba(17,153,142,0.12);
    border: 1px solid rgba(17,153,142,0.3);
    box-shadow: none;
}
.sentence-item .speak-btn-sm:hover {
    background: rgba(17,153,142,0.22);
}

/* 按钮组 */
.btn-group {
    display: flex;
    justify-content: center;
    gap: 16px;
    margin-top: 16px;
}

/* 动画 */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.tianzige-container {
    animation: fadeInUp 0.5s ease;
}

.info-card {
    animation: fadeInUp 0.5s ease;
    animation-fill-mode: both;
}

.info-card:nth-child(1) { animation-delay: 0.1s; }
.info-card:nth-child(2) { animation-delay: 0.2s; }
.info-card:nth-child(3) { animation-delay: 0.3s; }
.info-card:nth-child(4) { animation-delay: 0.35s; }

/* 文字释义表格（页面下方，无外框） */
.meaning-card { width: 100%; max-width: 100%; background: transparent; }
.meaning-section table { width: 100%; border-collapse: collapse; font-size: 14px; }
.meaning-section th { background: transparent; color: #5d4037; padding: 10px 12px 8px 0; text-align: left; font-weight: 600; border: none; border-bottom: 2px solid #8d6e63; }
.meaning-section td { padding: 10px 12px 10px 0; border: none; border-bottom: 1px solid #e0e0e0; vertical-align: top; line-height: 1.6; background: transparent; }
.meaning-section tr:nth-child(even) td { background: transparent; }
.meaning-section .col-pinyin { width: 80px; color: #b4531a; font-weight: 600; }
.meaning-section .col-content { min-width: 180px; color: #333; }
.meaning-section .col-detail { min-width: 200px; color: #555; font-size: 13px; }
.meaning-section .col-detail .cite { color: #6d4c41; font-weight: 600; margin-right: 4px; }
.meaning-section .col-words { min-width: 160px; }
.meaning-section .meaning-word-tag { display: inline-block; background: transparent; color: #2e7d32; padding: 2px 6px 2px 0; border-radius: 0; font-size: 13px; margin: 2px 8px 2px 0; }
.meaning-section .meaning-word-tag .w { font-weight: 600; }
.meaning-section .meaning-word-tag .t { color: #558b2f; margin-left: 4px; }
.meaning-none { color: #999; font-style: italic; padding: 12px 0; }
</style>

<div class="learn-container">
    <div class="tianzige-container">
        <div class="tianzige">
            <div class="diagonal-lines"></div>
            <div id="hanzi-writer-container"></div>
        </div>
        <div class="btn-group">
            <button class="speak-btn" onclick="speakText('@@HANZI@@')" title="点击发音">🔊</button>
            <button class="replay-btn" onclick="replayAnimation()" title="重播笔画">🔄</button>
        </div>
    </div>
    
    <div class="info-section">
        <div class="info-card pinyin-card">
            <h3><span class="icon">🔤</span> 拼音</h3>
            <div class="pinyin-display">
                @@PINYIN@@
            </div>
        </div>
        
        <div class="info-card">
            <h3><span class="icon">📝</span> 组词</h3>
            <div class="word-list">
                @@WORDS@@
            </div>
        </div>
        
        <div class="info-card">
            <h3><span class="icon">📖</span> 例句</h3>
            <div class="sentence-list">
                @@SENTENCES@@
            </div>
        </div>
        
        <div class="info-card meaning-card">
            <h3><span class="icon">📜</span> 文字释义</h3>
            <div class="meaning-section">
                @@MEANING@@
            </div>
        </div>
    </div>
</div>

<script>
// 汉字笔画书写动画
const character = '@@HANZI@@';
let writer = null;
let writerInitialized = false;

function initHanziWriter() {
    // 防止重复初始化
    if (writerInitialized) return;
    
    // 检查 HanziWriter 是否已加载
    if (typeof HanziWriter === 'undefined') {
        // 如果还没加载，等待后重试
        setTimeout(initHanziWriter, 100);
        return;
    }
    
    // 检查容器是否存在
    const container = document.getElementById('hanzi-writer-container');
    if (!container) {
        setTimeout(initHanziWriter, 100);
        return;
    }
    
    writerInitialized = true;
    
    try {
        writer = HanziWriter.create('hanzi-writer-container', character, {
            width: 240,
            height: 240,
            padding: 5,
            strokeColor: '#cc0000',  // 红色笔画
            radicalColor: '#cc0000',
            outlineColor: '#ddd',
            drawingColor: '#cc0000',
            strokeAnimationSpeed: 1,
            delayBetweenStrokes: 300,
            showOutline: true,
            showCharacter: false,  // 先不显示完整汉字
        });
        
        // 自动开始动画
        setTimeout(() => {
            if (writer) {
                writer.animateCharacter({
                    onComplete: function() {
                        // 动画完成后自动发音
                        autoSpeak(character);
                    }
                });
            }
        }, 200);
    } catch (e) {
        console.error('HanziWriter init error:', e);
        // 出错后重试
        writerInitialized = false;
        setTimeout(initHanziWriter, 200);
    }
}

function replayAnimation() {
    if (writer) {
        writer.hideCharacter();
        writer.animateCharacter();
    }
}


// 中文发音函数
function speakText(text) {
    if (!window.speechSynthesis) return;
    
    // 移除拼音标注（括号内的内容）
    const cleanText = text.replace(/\\s*\\([^)]*\\)/g, '');
    
    // 停止当前正在播放的语音
    window.speechSynthesis.cancel();
    
    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.lang = 'zh-CN';
    utterance.rate = 0.8;  // 稍慢一点，便于学习
    utterance.pitch = 1;
    
    // 尝试选择中文语音
    const voices = window.speechSynthesis.getVoices();
    const chineseVoice = voices.find(v => v.lang.includes('zh'));
    if (chineseVoice) {
        utterance.voice = chineseVoice;
    }
    
    window.speechSynthesis.speak(utterance);
}

// 自动发音标志（确保只发音一次）
let hasAutoSpoken = false;

function autoSpeak(text) {
    if (hasAutoSpoken) return; // 已经发音过，不再重复
    
    // 检查语音是否可用
    const voices = window.speechSynthesis.getVoices();
    if (voices.length === 0) {
        // 语音列表还没加载，等待后重试
        setTimeout(() => autoSpeak(text), 300);
        return;
    }
    
    hasAutoSpoken = true;
    speakText(text);
}

// 确保语音列表加载完成
if (window.speechSynthesis) {
    // 预加载语音列表
    window.speechSynthesis.getVoices();
    
    // 监听语音加载事件
    window.speechSynthesis.onvoiceschanged = () => {
        window.speechSynthesis.getVoices();
    };
}

// 页面加载后初始化
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(initHanziWriter, 200);
});

// 备用：如果 DOMContentLoaded 已经触发
if (document.readyState === 'complete' || document.readyState === 'interactive') {
    setTimeout(initHanziWriter, 200);
}

// 额外保险：window.onload
window.addEventListener('load', function() {
    setTimeout(initHanziWriter, 100);
});
</script>
"""

# 生成拼音 HTML
pinyin_html = ""
char = current["word"]
pinyin_list = CHINESE_TO_PINYIN.get(char, [])
for py in pinyin_list:
    pinyin_html += f'<div class="pinyin-item"><span class="py-text">{py}</span></div>'
if not pinyin_list:
    pinyin_html = f'<div class="pinyin-item"><span class="py-text">—</span></div>'


def highlight_current_char(text: str, current_char: str) -> str:
    """将文本中的当前字用 span.char-highlight 包裹，用于词组和例句中突出显示。"""
    if not current_char or current_char not in text:
        return html_escape(text)
    parts = text.split(current_char)
    escaped_char = html_escape(current_char)
    result = html_escape(parts[0])
    for i in range(1, len(parts)):
        result += f'<span class="char-highlight">{escaped_char}</span>' + html_escape(parts[i])
    return result


# 生成词语 HTML（多行展示，与例句同款样式，当前字高亮）
words_html = ""
for word in current.get("words", []):
    word_escaped = word.replace("\\", "\\\\").replace("'", "\\'").replace('"', "&quot;")
    text_html = highlight_current_char(word, char)
    words_html += f'<div class="word-item"><span class="text">{text_html}</span><button class="speak-btn-sm" onclick="speakText(\'{word_escaped}\')" title="点击发音">🔊</button></div>'

# 生成例句 HTML（当前字高亮）
sentences_html = ""
for sentence in current.get("sentence", []):
    sentence_escaped = (
        sentence.replace("\\", "\\\\").replace("'", "\\'").replace('"', "&quot;")
    )
    text_html = highlight_current_char(sentence, char)
    sentences_html += f'<div class="sentence-item"><span class="text">{text_html}</span><button class="speak-btn-sm" onclick="speakText(\'{sentence_escaped}\')" title="点击发音">🔊</button></div>'


# 从 WORD_TO_CONTENT 生成文字释义表格 HTML（表格：读音 | 释义 | 出处 | 词语）
def build_meaning_html(character: str) -> str:
    entry = None
    for item in WORD_TO_CONTENT:
        if item.get("char") == character:
            entry = item
            break
    if not entry or not entry.get("pronunciations"):
        return '<p class="meaning-none">暂无释义</p>'
    rows = []
    for pron in entry.get("pronunciations", []):
        pinyin = html_escape(pron.get("pinyin", ""))
        expls = pron.get("explanations", [])
        if not expls:
            continue
        for expl in expls:
            content = expl.get("content", "")
            content_cell = html_escape(content) if content else "—"
            detail = expl.get("detail", [])
            if detail:
                detail_parts = []
                for d in detail:
                    text = d.get("text", "")
                    book = d.get("book", "")
                    if book:
                        detail_parts.append(
                            f'<span class="cite">{html_escape(book)}</span>{html_escape(text)}'
                        )
                    else:
                        detail_parts.append(html_escape(text))
                detail_cell = "<br>".join(detail_parts)
            else:
                detail_cell = "—"
            words_list = expl.get("words", [])
            if words_list:
                w_tags = []
                for w in words_list:
                    w_word = w.get("word", "")
                    w_text = w.get("text", "")
                    if w_text:
                        w_tags.append(
                            f'<span class="meaning-word-tag"><span class="w">{html_escape(w_word)}</span><span class="t">{html_escape(w_text)}</span></span>'
                        )
                    else:
                        w_tags.append(
                            f'<span class="meaning-word-tag"><span class="w">{html_escape(w_word)}</span></span>'
                        )
                words_cell = "".join(w_tags)
            else:
                words_cell = "—"
            rows.append(
                f'<tr><td class="col-pinyin">{pinyin}</td><td class="col-content">{content_cell}</td>'
                f'<td class="col-detail">{detail_cell}</td><td class="col-words">{words_cell}</td></tr>'
            )
    if not rows:
        return '<p class="meaning-none">暂无释义</p>'
    return (
        "<table><thead><tr><th>读音</th><th>释义</th><th>出处</th><th>词语</th></tr></thead>"
        f'<tbody>{"".join(rows)}</tbody></table>'
    )


meaning_html = build_meaning_html(current["word"])

# 左侧：仅田字格 + 发音/重播（小 iframe，无内层滚动）
tianzige_only_html = (
    html_template.replace("@@PINYIN@@", "")
    .replace("@@MEANING@@", "")
    .replace("@@WORDS@@", "")
    .replace("@@SENTENCES@@", "")
)
# 去掉 info-section 整块，只保留 learn-container 内的 tianzige-container + script
if '<div class="info-section">' in tianzige_only_html:
    _before, _after = tianzige_only_html.split('<div class="info-section">', 1)
    _script_start = _after.find("<script>")
    if _script_start >= 0:
        tianzige_only_html = _before + "\n</div>\n\n" + _after[_script_start:]
tianzige_only_html = tianzige_only_html.replace("@@HANZI@@", current["word"])

# 右侧：拼音、组词、例句、释义直接放在主页面，随页面滚动
RIGHT_SIDE_CSS = """
<style>
.info-section { max-width: 100%; padding-top: 8px; min-height: 120px; }
.info-card { background: transparent; border: none; border-top: 1px solid #e0e0e0; padding: 18px 0 22px 0; margin: 0; box-shadow: none; border-radius: 0; }
.info-card:first-child { border-top: none; padding-top: 12px; }
.info-card h3 { margin: 0 0 10px 0; font-size: 16px; color: #444; }
.info-card h3 .icon { font-size: 20px; }
.pinyin-display { display: flex; flex-wrap: wrap; gap: 16px; align-items: center; min-height: 32px; }
.pinyin-item { color: #e65100; font-size: 24px; font-weight: 700; }
/* 词组与例句：多行展示、统一字体与颜色 */
.word-list { display: flex; flex-direction: column; gap: 10px; }
.word-item, .sentence-item { color: #00695c; font-size: 18px; font-weight: 500; line-height: 1.6; display: flex; align-items: center; gap: 8px; }
/* 当前字高亮 */
.char-highlight { color: #c62828; font-weight: 700; }
/* 词组/例句喇叭 - 与田字格下方主喇叭同款红色渐变与特效 */
.word-item .speak-btn-sm,
.sentence-item .speak-btn-sm {
    width: 36px; height: 36px; border-radius: 50%; cursor: pointer; border: none;
    background: linear-gradient(135deg, #ff6b6b, #ee5a5a);
    box-shadow: 0 4px 14px rgba(238,90,90,0.4);
    font-size: 18px; display: inline-flex; align-items: center; justify-content: center;
    transition: all 0.2s ease; flex-shrink: 0;
}
.word-item .speak-btn-sm:hover,
.sentence-item .speak-btn-sm:hover {
    transform: scale(1.15);
    box-shadow: 0 6px 20px rgba(238,90,90,0.5);
}
.word-item .speak-btn-sm:active,
.sentence-item .speak-btn-sm:active {
    transform: scale(0.95);
}
.sentence-list { display: flex; flex-direction: column; gap: 10px; }
.meaning-section table { width: 100%; border-collapse: collapse; font-size: 14px; }
.meaning-section th { background: transparent; color: #5d4037; padding: 10px 12px 8px 0; text-align: left; font-weight: 600; border-bottom: 2px solid #8d6e63; }
.meaning-section td { padding: 10px 12px 10px 0; border: none; border-bottom: 1px solid #e0e0e0; vertical-align: top; line-height: 1.6; background: transparent; }
.meaning-section .col-pinyin { width: 80px; color: #b4531a; font-weight: 600; }
.meaning-section .col-detail .cite { color: #6d4c41; font-weight: 600; margin-right: 4px; }
.meaning-word-tag { display: inline-block; color: #2e7d32; font-size: 13px; margin: 2px 8px 2px 0; }
.meaning-word-tag .t { color: #558b2f; margin-left: 4px; }
.meaning-none { color: #999; font-style: italic; }
</style>
"""
# 右侧内容必须用 components.html 渲染，否则内联 script 不会执行，发音按钮无效
RIGHT_SIDE_SCRIPT = """
<script>
(function(){
if (window._learnSpeakLoaded) return;
window._learnSpeakLoaded = true;
window.speakText = function(text) {
  if (!window.speechSynthesis) return;
  var clean = (text || '').replace(/\\s*\\([^)]*\\)/g, '');
  window.speechSynthesis.cancel();
  var u = new SpeechSynthesisUtterance(clean);
  u.lang = 'zh-CN';
  u.rate = 0.8;
  var voices = window.speechSynthesis.getVoices();
  var v = voices && voices.find(function(x){ return x.lang.indexOf('zh') >= 0; });
  if (v) u.voice = v;
  window.speechSynthesis.speak(u);
};
if (window.speechSynthesis) {
  window.speechSynthesis.getVoices();
  window.speechSynthesis.onvoiceschanged = function() { window.speechSynthesis.getVoices(); };
}
})();
</script>
"""
right_side_html = (
    RIGHT_SIDE_SCRIPT
    + RIGHT_SIDE_CSS
    + '<div class="info-section">'
    + '<div class="info-card pinyin-card"><h3><span class="icon">🔤</span> 拼音</h3><div class="pinyin-display">'
    + pinyin_html
    + "</div></div>"
    + '<div class="info-card"><h3><span class="icon">📝</span> 组词</h3><div class="word-list">'
    + words_html
    + "</div></div>"
    + '<div class="info-card"><h3><span class="icon">📖</span> 例句</h3><div class="sentence-list">'
    + sentences_html
    + "</div></div>"
    + '<div class="info-card meaning-card"><h3><span class="icon">📜</span> 文字释义</h3><div class="meaning-section">'
    + meaning_html
    + "</div></div>"
    + "</div>"
)

import streamlit.components.v1 as components

col_left, col_right = st.columns([0.36, 0.64])
with col_left:
    # 高度加大以完整显示田字格 + 下方发音/重播按钮，避免被裁切
    components.html(tianzige_only_html, height=480, scrolling=False)
with col_right:
    # 用 components.html 渲染右侧，使内联 script 执行，词组/例句发音按钮才能调用 speakText
    components.html(right_side_html, height=800, scrolling=True)
