import streamlit as st
import json
import random
import re

from data.dict import WORD_TO_LEARN

st.set_page_config(page_title="拼音与汉字", page_icon="✏️", layout="wide")

# 隐藏部分默认元素，保留侧边栏
st.markdown(
    """
<style>
    /* 与 theme 一致，避免左侧菜单切换时整页白屏闪烁 */
    .stApp, [data-testid="stAppViewContainer"], main { background-color: #f0f2f6 !important; }
    [data-testid="stStatusWidget"] { visibility: hidden !important; height: 0 !important; overflow: hidden !important; }
    .block-container { animation: stPageFadeIn 0.2s ease-out; }
    @keyframes stPageFadeIn { from { opacity: 0; } to { opacity: 1; } }
    .block-container { padding-top: 0.35rem; padding-bottom: 0; max-width: 100%; }
    footer { visibility: hidden; }
    [data-testid="stSidebarNav"] span { font-weight: 500; font-size: 1.125rem !important; }
    [data-testid="stSidebarNav"] li { padding: 8px 0; }
</style>
""",
    unsafe_allow_html=True,
)

# 侧栏由入口 汉字乐园.py 统一绘制，本页不再输出侧栏，避免切换时侧栏刷新

# ========== 拼音与汉字练习 HTML 模板（内联，不依赖 static 文件） ==========
HANZI_PINYIN_HTML = r"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>拼音与汉字</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Helvetica Neue', Arial, sans-serif; background: transparent; margin-top: 6px; }
    .g-wrap { width: 100%; min-height: 720px; position: relative; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 16px; overflow: visible; display: flex; flex-direction: column; padding-top: 16px; }
    .g-start { position: absolute; inset: 0; z-index: 900; display: flex; flex-direction: column; align-items: center; justify-content: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 16px; }
    .g-start h2 { font-size: 48px; color: #fff; margin-bottom: 16px; }
    .g-start p { font-size: 18px; color: rgba(255, 255, 255, 0.8); text-align: center; line-height: 1.8; margin-bottom: 36px; }
    .g-start-btn { padding: 16px 56px; font-size: 22px; font-weight: 700; background: linear-gradient(135deg, #ffd54f, #ffb300); color: #333; border: none; border-radius: 30px; cursor: pointer; box-shadow: 0 8px 28px rgba(255, 213, 79, 0.5); transition: all .3s; }
    .g-start-btn:hover { transform: translateY(-3px) scale(1.04); box-shadow: 0 12px 36px rgba(255, 213, 79, 0.7); }
    .g-topbar { display: flex; justify-content: space-between; align-items: center; padding: 18px 24px 14px; flex-shrink: 0; margin-top: 4px; }
    .g-topbar-item { display: flex; align-items: center; gap: 8px; background: rgba(255, 255, 255, 0.18); backdrop-filter: blur(6px); padding: 8px 18px; border-radius: 20px; color: #fff; font-weight: 700; font-size: 15px; }
    .g-topbar-item .num { color: #ffd54f; font-size: 15px; margin-left: 4px; }
    .g-end-btn { background: rgba(255, 80, 80, 0.7); backdrop-filter: blur(6px); border: none; color: #fff; padding: 10px 24px; border-radius: 20px; font-weight: 700; font-size: 15px; cursor: pointer; transition: all .2s; }
    .g-end-btn:hover { background: rgba(255, 60, 60, 0.9); }
    .g-next-btn { background: rgba(76, 175, 80, 0.85); backdrop-filter: blur(6px); border: none; color: #fff; padding: 10px 24px; border-radius: 20px; font-weight: 700; font-size: 15px; cursor: pointer; transition: all .2s; margin-left: 10px; text-decoration: none; display: inline-block; }
    .g-next-btn:hover { background: rgba(56, 142, 60, 0.95); color: #fff; }
    .g-topbar-btns { display: flex; align-items: center; gap: 0; }
    .g-modal-close-btn { margin-top: 18px; padding: 10px 24px; background: #f5f5f5; border: 1px solid #ddd; border-radius: 20px; font-size: 15px; font-weight: 600; color: #555; cursor: pointer; transition: all .2s; }
    .g-modal-close-btn:hover { background: #eee; color: #333; }
    .g-progress { margin: 0 24px 20px; height: 6px; background: rgba(255, 255, 255, 0.2); border-radius: 4px; overflow: hidden; flex-shrink: 0; }
    .g-progress-bar { height: 100%; background: linear-gradient(90deg, #ffd54f, #ffb300); border-radius: 4px; transition: width .5s ease; width: 0%; }
    .g-body { flex: 1; display: flex; flex-direction: column; gap: 24px; padding: 0 24px 24px; align-items: center; justify-content: center; min-height: 0; }
    .g-sentence-card { background: #fff; border-radius: 16px; padding: 36px 40px; text-align: center; font-size: 24px; color: #333; line-height: 2.4; box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08); flex-shrink: 0; width: 100%; max-width: 700px; margin: 0 auto; position: relative; }
    .g-sentence-text { display: inline; }
    .g-speak-btn { display: inline-flex; align-items: center; justify-content: center; width: 38px; height: 38px; border-radius: 50%; border: none; cursor: pointer; background: linear-gradient(135deg, #ff9a9e, #fecfef); color: #e53935; font-size: 20px; box-shadow: 0 3px 12px rgba(255, 107, 107, 0.3); transition: all .2s; vertical-align: middle; margin-left: 12px; flex-shrink: 0; }
    .g-speak-btn:hover { transform: scale(1.15); box-shadow: 0 5px 18px rgba(255, 107, 107, 0.45); }
    .g-speak-btn:active { transform: scale(0.95); }
    .py-target { color: #ff6d00; font-weight: 800; font-size: 28px; background: rgba(255, 109, 0, 0.1); padding: 2px 6px; border-radius: 6px; border-bottom: 3px solid #ff6d00; }
    .py-blank { display: inline-block; min-width: 64px; border: 2px dashed #764ba2; color: #764ba2; font-weight: 700; font-size: 17px; margin: 0 6px; padding: 4px 10px; transition: all .3s; border-radius: 8px; background: rgba(118, 75, 162, 0.06); vertical-align: middle; }
    .py-blank.filled { border-style: solid; border-color: #4CAF50; color: #4CAF50; background: rgba(76, 175, 80, 0.1); animation: blankPop .4s ease; }
    .py-blank.wrong { border-color: #f44336; color: #f44336; background: rgba(244, 67, 54, 0.08); animation: blankShake .5s ease; }
    @keyframes blankPop { 0% { transform: scale(1) } 50% { transform: scale(1.15) } 100% { transform: scale(1) } }
    @keyframes blankShake { 0%,100% { transform: translateX(0) } 20% { transform: translateX(-6px) } 40% { transform: translateX(6px) } 60% { transform: translateX(-4px) } 80% { transform: translateX(4px) } }
    .g-choices-card { width: 100%; max-width: 700px; margin: 0 auto; background: rgba(255, 255, 255, 0.12); backdrop-filter: blur(6px); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 16px; padding: 20px 24px; }
    .g-choices-label { color: rgba(255, 255, 255, 0.7); font-size: 13px; font-weight: 600; text-align: center; margin-bottom: 14px; letter-spacing: 1px; }
    .g-choices { display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; }
    .g-choice { padding: 12px 28px; border-radius: 14px; font-size: 18px; font-weight: 700; color: #fff; cursor: pointer; box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12); transition: all .2s; user-select: none; border: 2px solid rgba(255, 255, 255, 0.15); }
    .g-choice:hover { transform: translateY(-3px) scale(1.04); box-shadow: 0 8px 24px rgba(0, 0, 0, 0.18); }
    .g-choice:active { transform: scale(0.96); }
    .g-choice.disabled { opacity: 0.35; pointer-events: none; transform: none; }
    .g-hint { text-align: center; color: rgba(255, 255, 255, 0.7); font-size: 14px; margin-top: auto; padding-top: 8px; }
    .g-feedback { position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 80px; z-index: 9999; pointer-events: none; animation: fbPop .8s ease forwards; }
    @keyframes fbPop { 0% { opacity: 0; transform: translate(-50%, -50%) scale(0) } 30% { opacity: 1; transform: translate(-50%, -50%) scale(1.3) } 60% { transform: translate(-50%, -50%) scale(1) } 100% { opacity: 0; transform: translate(-50%, -70%) scale(.8) } }
    .g-modal-overlay { position: fixed; inset: 0; background: rgba(0, 0, 0, 0.55); display: flex; align-items: center; justify-content: center; z-index: 9998; animation: gFadeIn .3s ease; }
    @keyframes gFadeIn { from { opacity: 0 } to { opacity: 1 } }
    .g-modal { background: #fff; padding: 36px 44px; border-radius: 20px; text-align: center; min-width: 320px; max-width: 420px; box-shadow: 0 24px 60px rgba(0, 0, 0, 0.3); animation: gModalIn .4s cubic-bezier(.34, 1.56, .64, 1); }
    @keyframes gModalIn { from { opacity: 0; transform: scale(.8) } to { opacity: 1; transform: scale(1) } }
    .g-modal h3 { font-size: 28px; font-weight: 700; margin-bottom: 16px; }
    .g-modal .g-stats { margin: 16px 0; padding: 16px; background: #f8f9fa; border-radius: 14px; }
    .g-modal .g-stat-row { display: flex; justify-content: space-between; align-items: center; padding: 8px 0; font-size: 16px; }
    .g-modal .g-stat-row .sl { color: #888; }
    .g-modal .g-stat-row .sv { font-weight: 700; color: #333; font-size: 18px; }
    .g-mbtn { margin-top: 8px; padding: 12px 28px; border: none; border-radius: 24px; cursor: pointer; font-size: 16px; font-weight: 600; transition: all .2s; }
    .g-mbtn:hover { transform: translateY(-2px); }
    .g-mbtn-ok { background: linear-gradient(135deg, #4CAF50, #45a049); color: #fff; box-shadow: 0 4px 16px rgba(76, 175, 80, 0.35); }
    .particle { position: fixed; pointer-events: none; z-index: 9999; }
    @keyframes particleFly { 0% { opacity: 1; transform: translate(0, 0) rotate(0deg) scale(1) } 100% { opacity: 0; transform: translate(var(--tx), var(--ty)) rotate(var(--rot)) scale(.4) } }
    @keyframes confFall { 0% { transform: translateY(0) rotate(0deg); opacity: 1 } 100% { transform: translateY(100vh) rotate(720deg); opacity: .7 } }
  </style>
</head>
<body>
  <div class="g-wrap" id="g-wrap">
    <div class="g-start" id="g-start">
      <h2>✏️ 拼音与汉字</h2>
      <p>阅读句子，选择正确的拼音填入空白<br>✅ 正确 +10分 &nbsp; ❌ 错误 -5分<br>每轮共 10 个句子</p>
      <button class="g-start-btn" onclick="gStart()">开始练习</button>
    </div>
    <div class="g-topbar" id="g-topbar" style="visibility:hidden;">
      <div class="g-topbar-item">⏱️ <span id="g-timer">00:00</span></div>
      <div class="g-topbar-item">🏆 <span class="num" id="g-score">0</span></div>
      <div class="g-topbar-item">📝 <span id="g-idx">0</span>/<span id="g-total">10</span></div>
      <button class="g-end-btn" onclick="gEnd()">🛑 结束</button>
    </div>
    <div class="g-progress" id="g-progress" style="visibility:hidden;">
      <div class="g-progress-bar" id="g-pbar"></div>
    </div>
    <div class="g-body" id="g-body" style="visibility:hidden;">
      <div class="g-sentence-card">
        <span class="g-sentence-text" id="g-sentence"></span>
        <button class="g-speak-btn" id="g-speak-btn" onclick="speakCurrent()" title="朗读句子">🔊</button>
      </div>
      <div class="g-choices-card">
        <div class="g-choices-label">👇 选择正确的拼音</div>
        <div class="g-choices" id="g-choices"></div>
      </div>
    </div>
  </div>
  <div id="g-modal-holder"></div>
  <script>
    function continuePractice() {
      try { window.top.location.reload(); } catch (e) { try { window.parent.location.reload(); } catch (e2) { window.location.reload(); } }
    }
    const SDATA = /* DATA_START */ {"exercises": [], "total": 0, "autoStart": false, "mode": "sentence"} /* DATA_END */;
    const exercises = SDATA.exercises;
    const totalEx = SDATA.total;
    let gStartTime = null, gTimerIv = null, gStarted = false;
    let gIdx = 0, gScore = 0, gOk = 0, gFail = 0, gBusy = false;
    let currentText = '';
    const GRADS = ['linear-gradient(135deg,#667eea,#764ba2)','linear-gradient(135deg,#f093fb,#f5576c)','linear-gradient(135deg,#4facfe,#00f2fe)','linear-gradient(135deg,#43e97b,#38f9d7)','linear-gradient(135deg,#fa709a,#fee140)'];
    function fmt(ms) { const s = Math.floor(ms / 1000), m = Math.floor(s / 60); return m.toString().padStart(2, '0') + ':' + (s % 60).toString().padStart(2, '0'); }
    function tick() { if (gStartTime) document.getElementById('g-timer').innerText = fmt(Date.now() - gStartTime); }
    function stopTimer() { if (gTimerIv) { clearInterval(gTimerIv); gTimerIv = null; } return gStartTime ? Date.now() - gStartTime : 0; }
    let _ac = null;
    function ac() { if (!_ac) _ac = new (window.AudioContext || window.webkitAudioContext)(); return _ac; }
    function sndOk() { const c = ac(), n = c.currentTime;[523.25, 659.25, 783.99, 1046.5].forEach((f, i) => { const o = c.createOscillator(), g = c.createGain(); o.connect(g); g.connect(c.destination); o.type = 'sine'; o.frequency.setValueAtTime(f, n + i * .12); g.gain.setValueAtTime(0, n + i * .12); g.gain.linearRampToValueAtTime(.3, n + i * .12 + .02); g.gain.exponentialRampToValueAtTime(.001, n + i * .12 + .3); o.start(n + i * .12); o.stop(n + i * .12 + .35); }); }
    function sndFail() { const c = ac(), n = c.currentTime, o = c.createOscillator(), g = c.createGain(); o.connect(g); g.connect(c.destination); o.type = 'sine'; o.frequency.setValueAtTime(440, n); o.frequency.exponentialRampToValueAtTime(220, n + .8); g.gain.setValueAtTime(0, n); g.gain.linearRampToValueAtTime(.2, n + .05); g.gain.exponentialRampToValueAtTime(.001, n + 1); o.start(n); o.stop(n + 1.2); }
    function sndWin() { const c = ac();[523.25, 659.25, 783.99, 1046.5].forEach((f, i) => { const o = c.createOscillator(), g = c.createGain(); o.connect(g); g.connect(c.destination); o.type = 'sine'; o.frequency.setValueAtTime(f, c.currentTime + i * .15); g.gain.setValueAtTime(0, c.currentTime + i * .15); g.gain.linearRampToValueAtTime(.3, c.currentTime + i * .15 + .02); g.gain.exponentialRampToValueAtTime(.01, c.currentTime + i * .15 + .2); o.start(c.currentTime + i * .15); o.stop(c.currentTime + i * .15 + .3); }); }
    function showFB(emoji) { const d = document.createElement('div'); d.className = 'g-feedback'; d.innerText = emoji; document.body.appendChild(d); setTimeout(function(){ d.remove(); }, 900); }
    function speakCurrent() {
      if (!currentText) return;
      if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
        var u = new SpeechSynthesisUtterance(currentText);
        u.lang = 'zh-CN'; u.rate = 0.8; u.pitch = 1;
        var voices = window.speechSynthesis.getVoices();
        var zh = voices.find(function(v){ return v.lang.indexOf('zh') >= 0; });
        if (zh) u.voice = zh;
        window.speechSynthesis.speak(u);
      }
    }
    if ('speechSynthesis' in window) { window.speechSynthesis.getVoices(); window.speechSynthesis.onvoiceschanged = function(){ window.speechSynthesis.getVoices(); }; }
    function explode(x, y) { var cols = ['#ff5252', '#ffb74d', '#ffd54f', '#4db6ac', '#81c784', '#9575cd', '#f06292']; for (var i = 0; i < 30; i++) { (function(ii){ setTimeout(function(){ var p = document.createElement('div'); p.className = 'particle'; var s = 6 + Math.random() * 8; p.style.cssText = 'width:'+s+'px;height:'+s+'px;border-radius:'+(s/2)+'px;background:'+cols[Math.floor(Math.random()*cols.length)]+';left:'+(x-4+Math.random()*8)+'px;top:'+(y-4+Math.random()*8)+'px;'; var a = Math.random()*Math.PI*2, sp = 60+Math.random()*200; p.style.setProperty('--tx', Math.cos(a)*sp+'px'); p.style.setProperty('--ty', Math.sin(a)*sp+'px'); p.style.setProperty('--rot', (Math.random()*720-360)+'deg'); p.style.animation = 'particleFly 1s cubic-bezier(.15,.8,.3,1) forwards'; document.body.appendChild(p); setTimeout(function(){ p.remove(); }, 1200); }, Math.random()*150); })(i); } }
    function confetti() { var cols = ['#ff5252','#ffb74d','#ffd54f','#4db6ac','#81c784','#9575cd','#f06292','#29b6f6']; for (var i = 0; i < 120; i++) { (function(ii){ setTimeout(function(){ var c = document.createElement('div'); var w = 4+Math.random()*6, h = 16+Math.random()*20; c.style.cssText = 'position:fixed;width:'+w+'px;height:'+h+'px;background:'+cols[Math.floor(Math.random()*cols.length)]+';left:'+Math.random()*100+'vw;top:-30px;border-radius:2px;pointer-events:none;z-index:10000;transform:rotate('+(Math.random()*360)+'deg);animation:confFall '+(3+Math.random()*2)+'s linear forwards;'; document.body.appendChild(c); setTimeout(function(){ c.remove(); }, 5500); }, Math.random()*600); })(i); } }
    function gStart() {
      if (gStarted) return; gStarted = true;
      var ov = document.getElementById('g-start');
      ov.style.transition = 'opacity .3s'; ov.style.opacity = '0'; setTimeout(function(){ ov.style.display = 'none'; }, 300);
      document.getElementById('g-topbar').style.visibility = 'visible';
      document.getElementById('g-progress').style.visibility = 'visible';
      document.getElementById('g-body').style.visibility = 'visible';
      document.getElementById('g-total').innerText = totalEx;
      gStartTime = Date.now(); gTimerIv = setInterval(tick, 200);
      gIdx = 0; gScore = 0; gOk = 0; gFail = 0;
      render();
    }
    function render() {
      if (gIdx >= totalEx) { finish(); return; }
      gBusy = false;
      var ex = exercises[gIdx];
      currentText = ex.text || '';
      document.getElementById('g-sentence').innerHTML = ex.html;
      document.getElementById('g-idx').innerText = gIdx + 1;
      document.getElementById('g-pbar').style.width = (gIdx / totalEx * 100) + '%';
      var box = document.getElementById('g-choices'); box.innerHTML = '';
      ex.candidates.forEach(function(c, i) {
        var btn = document.createElement('div'); btn.className = 'g-choice'; btn.style.background = GRADS[i % GRADS.length]; btn.innerText = c;
        btn.onclick = function(){ pick(c, btn); }; box.appendChild(btn);
      });
    }
    function pick(chosen, btnEl) {
      if (gBusy) return; gBusy = true;
      var ex = exercises[gIdx], blank = document.querySelector('.py-blank');
      if (!blank) { gBusy = false; return; }
      if (chosen === ex.answer) {
        blank.innerText = chosen; blank.classList.add('filled'); sndOk();
        var r = blank.getBoundingClientRect(); explode(r.left + r.width/2, r.top + r.height/2); showFB('🎉');
        gScore += 10; gOk++; document.getElementById('g-score').innerText = gScore;
        document.querySelectorAll('.g-choice').forEach(function(c){ c.classList.add('disabled'); });
        setTimeout(function(){ gIdx++; render(); }, 1000);
      } else {
        blank.classList.add('wrong'); btnEl.classList.add('disabled'); sndFail(); showFB('❌');
        gScore = Math.max(0, gScore - 5); gFail++; document.getElementById('g-score').innerText = gScore;
        setTimeout(function(){ blank.classList.remove('wrong'); gBusy = false; }, 700);
      }
    }
    function finish() { var el = stopTimer(), ts = fmt(el); sndWin(); confetti(); document.getElementById('g-pbar').style.width = '100%'; setTimeout(function(){ modal(true, ts); }, 1200); }
    function gEnd() { if (!gStarted) return; var el = stopTimer(), ts = fmt(el); modal(false, ts); }
    function closeModal() { var ho = document.getElementById('g-modal-holder'); if (ho && ho.lastChild) ho.removeChild(ho.lastChild); }
    function modal(win, ts) {
      var ho = document.getElementById('g-modal-holder');
      var ov = document.createElement('div');
      ov.className = 'g-modal-overlay';
      ov.innerHTML = '<div class="g-modal"><h3>' + (win ? '🎉 练习完成！' : '🎉 练习结束') + '</h3><div class="g-stats"><div class="g-stat-row"><span class="sl">⏱️ 用时</span><span class="sv">' + ts + '</span></div><div class="g-stat-row"><span class="sl">🏆 得分</span><span class="sv">' + gScore + '</span></div><div class="g-stat-row"><span class="sl">✅ 正确</span><span class="sv">' + gOk + '</span></div><div class="g-stat-row"><span class="sl">❌ 错误</span><span class="sv">' + gFail + '</span></div>' + (!win ? '<div class="g-stat-row"><span class="sl">📊 进度</span><span class="sv">' + gIdx + ' / ' + totalEx + '</span></div>' : '') + '</div><button type="button" class="g-mbtn g-mbtn-ok" onclick="continuePractice()" style="margin-top:18px;">继续练习</button></div>';
      ov.onclick = function(e){ if (e.target === ov) closeModal(); };
      ov.querySelector('.g-modal').onclick = function(e){ e.stopPropagation(); };
      ho.appendChild(ov);
    }
    if (SDATA.autoStart) { setTimeout(function(){ gStart(); }, 100); }
  </script>
</body>
</html>
"""


def show_find_pinyin():
    sentence_pool = []
    for item in WORD_TO_LEARN:
        for s in item.get("sentence", []):
            sentence_pool.append(s)
    random.shuffle(sentence_pool)

    all_toned_pinyins = set()
    for s_item in WORD_TO_LEARN:
        for s in s_item.get("sentence", []):
            for m in re.finditer(r"\(([^)]+)\)", s):
                all_toned_pinyins.add(m.group(1).strip())
    all_toned_pinyins = list(all_toned_pinyins)

    sentence_exercises = []
    needed = 10
    for s in sentence_pool:
        if len(sentence_exercises) >= needed:
            break
        m = re.search(r"\(([^)]+)\)", s)
        if not m:
            continue
        tone_py = m.group(1).strip()
        target_pattern = r"([\u4e00-\u9fff])\s*\(" + re.escape(tone_py) + r"\)"
        display_html = re.sub(
            target_pattern,
            r'<span class="py-target">\1</span> <span class="py-blank" data-answer="'
            + tone_py
            + r'">?</span>',
            s,
            count=1,
        )
        if "py-blank" not in display_html:
            display_html = s.replace(
                "(" + tone_py + ")",
                '<span class="py-blank" data-answer="' + tone_py + '">?</span>',
            )
        display_html = re.sub(r"\s*\([^)]+\)", "", display_html)
        candidates = [tone_py]
        tries = 0
        while len(candidates) < 5 and tries < 200:
            cand = random.choice(all_toned_pinyins)
            if cand not in candidates:
                candidates.append(cand)
            tries += 1
        random.shuffle(candidates)
        plain_text = re.sub(r"\s*\([^)]+\)", "", s)
        sentence_exercises.append(
            {
                "html": display_html,
                "answer": tone_py,
                "candidates": candidates,
                "text": plain_text,
            }
        )

    while len(sentence_exercises) < needed:
        sentence_exercises.append(sentence_exercises[-1])

    data_json = json.dumps(
        {
            "exercises": sentence_exercises,
            "total": len(sentence_exercises),
            "autoStart": False,
            "mode": "sentence",
        },
        ensure_ascii=False,
    )

    html_content = re.sub(
        r"/\*\s*DATA_START\s\*/[\s\S]*?/\*\s*DATA_END\s\*/",
        data_json,
        HANZI_PINYIN_HTML,
        count=1,
    )
    import streamlit.components.v1 as components

    components.html(html_content, height=850, scrolling=False)


show_find_pinyin()
