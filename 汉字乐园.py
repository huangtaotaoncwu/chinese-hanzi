# 入口文件：使用 st.navigation 单入口，侧栏仅在此绘制，切换页面时侧栏不再由各页重画，避免左侧菜单刷新
import streamlit as st

st.set_page_config(page_title="汉字乐园", page_icon="🏠", layout="wide")

# 全局样式（首帧即注入，与 theme 一致）
st.markdown(
    """
<style>
    .stApp, [data-testid="stAppViewContainer"], main { background-color: #f0f2f6 !important; }
    [data-testid="stStatusWidget"] { visibility: hidden !important; height: 0 !important; overflow: hidden !important; }
    .block-container { animation: stPageFadeIn 0.2s ease-out; }
    @keyframes stPageFadeIn { from { opacity: 0; } to { opacity: 1; } }
    footer { visibility: hidden; }
    [data-testid="stSidebarNav"] span { font-weight: 500; font-size: 1.125rem !important; }
    [data-testid="stSidebarNav"] li { padding: 8px 0; }
</style>
""",
    unsafe_allow_html=True,
)

# 侧栏仅在此入口绘制一次，各子页不再输出侧栏，避免切换时侧栏重绘
st.sidebar.header("🏠 汉字乐园")
st.sidebar.caption("从上方菜单切换功能")

# 多页导航：由框架统一渲染菜单，切换时只更新主内容区
nav_pages = [
    st.Page("pages/0_🏠_首页.py", title="首页", icon="🏠", default=True),
    st.Page("pages/1_📜_源.py", title="源", icon="📜"),
    st.Page("pages/2_🎮_玩.py", title="玩", icon="🎮"),
    st.Page("pages/3_📚_学.py", title="学", icon="📚"),
    st.Page("pages/4_✏️_练.py", title="练", icon="✏️"),
]
pg = st.navigation(nav_pages)
pg.run()
