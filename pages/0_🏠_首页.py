# 首页内容（由入口 汉字乐园.py 通过 st.navigation 调用，不再单独渲染侧栏，避免切换时侧栏刷新）
import streamlit as st

st.set_page_config(page_title="汉字乐园", page_icon="🏠", layout="wide")

# 首页标题
st.markdown(
    """
<div style="text-align:center; padding:0px 0 20px;">
    <h1 style="font-size:50px; margin:0; background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">🏠 汉字乐园</h1>
    <p style="font-size:18px; color:#666; margin-top:12px;">让学习汉字变得有趣！</p>
</div>
""",
    unsafe_allow_html=True,
)

# 四个功能卡片样式
st.markdown(
    """
<style>
.feature-card {
    background: linear-gradient(135deg, #f8f9fa, #fff);
    border-radius: 20px;
    padding: 24px;
    margin: 8px 0;
    box-shadow: 0 6px 24px rgba(0,0,0,0.08);
    border: 1px solid #eee;
    transition: transform 0.3s, box-shadow 0.3s;
    text-align: center;
    min-height: 200px;
}
.feature-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 12px 36px rgba(0,0,0,0.15);
}
.feature-icon { font-size: 50px; margin-bottom: 12px; }
.feature-title { font-size: 26px; font-weight: 700; margin: 0 0 10px; color: #333; }
.feature-desc { font-size: 13px; color: #666; line-height: 1.8; }
.origin-card { border-top: 4px solid #d4a574; background: linear-gradient(180deg, rgba(212,165,116,0.08) 0%, #fff 100%); }
.play-card { border-top: 4px solid #667eea; background: linear-gradient(180deg, rgba(102,126,234,0.05) 0%, #fff 100%); }
.learn-card { border-top: 4px solid #11998e; background: linear-gradient(180deg, rgba(17,153,142,0.05) 0%, #fff 100%); }
.practice-card { border-top: 4px solid #f85f73; background: linear-gradient(180deg, rgba(248,95,115,0.05) 0%, #fff 100%); }
</style>
""",
    unsafe_allow_html=True,
)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("""<div class="feature-card origin-card"><div class="feature-icon">📜</div><div class="feature-title">源</div><div class="feature-desc">🏛️ 汉字起源与演变<br>🖼️ 图文并茂展示<br>🎵 古典背景音乐</div></div>""", unsafe_allow_html=True)
    if st.button("📜 汉字起源", key="origin", use_container_width=True):
        st.switch_page("pages/1_📜_源.py")
with col2:
    st.markdown("""<div class="feature-card play-card"><div class="feature-icon">🎮</div><div class="feature-title">玩</div><div class="feature-desc">🎯 汉字消消乐<br>30秒限时挑战<br>连击加分更刺激</div></div>""", unsafe_allow_html=True)
    if st.button("🎮 开始玩", key="play", use_container_width=True):
        st.switch_page("pages/2_🎮_玩.py")
with col3:
    st.markdown("""<div class="feature-card learn-card"><div class="feature-icon">📚</div><div class="feature-title">学</div><div class="feature-desc">✍️ 笔画动画演示<br>🔊 组词例句发音<br>田字格规范书写</div></div>""", unsafe_allow_html=True)
    if st.button("📚 开始学", key="learn", use_container_width=True):
        st.switch_page("pages/3_📚_学.py")
with col4:
    st.markdown("""<div class="feature-card practice-card"><div class="feature-icon">✏️</div><div class="feature-title">练</div><div class="feature-desc">🎈 汉字与拼音<br>📝 找拼音填句子<br>两种模式任你选</div></div>""", unsafe_allow_html=True)
    if st.button("✏️ 开始练", key="practice", use_container_width=True):
        st.switch_page("pages/4_✏️_练.py")

st.markdown("<div style='margin: 30px 0; border-top: 1px solid #eee;'></div>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; padding:10px 20px;">
    <div style="display:flex; justify-content:center; gap:36px; flex-wrap:wrap; margin-bottom:20px;">
        <div style="text-align:center;"><div style="font-size:24px;">📜</div><div style="font-size:13px; color:#d4a574; font-weight:600;">汉字起源</div><div style="font-size:12px; color:#999;">历史演变</div></div>
        <div style="text-align:center;"><div style="font-size:24px;">🎮</div><div style="font-size:13px; color:#667eea; font-weight:600;">玩游戏</div><div style="font-size:12px; color:#999;">限时挑战</div></div>
        <div style="text-align:center;"><div style="font-size:24px;">📚</div><div style="font-size:13px; color:#11998e; font-weight:600;">学汉字</div><div style="font-size:12px; color:#999;">笔画发音</div></div>
        <div style="text-align:center;"><div style="font-size:24px;">✏️</div><div style="font-size:13px; color:#f85f73; font-weight:600;">练拼音</div><div style="font-size:12px; color:#999;">汉字与拼音</div></div>
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown("""<div style="text-align:center; padding:15px 0; color:#aaa; font-size:13px;"><p>👈 也可以从左侧边栏选择功能</p><p style="margin-top:6px;">汉字乐园 - 让每个孩子爱上汉字 ❤️</p></div>""", unsafe_allow_html=True)
