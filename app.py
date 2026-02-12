import os
import base64
from datetime import date
from pathlib import Path
import streamlit as st

# ------------------ Customize ------------------
HIS_NAME = "Darling~"        # 改成你先生的英文名/昵称
YOUR_NAME = "Vivienne"      # 你的名字
BIRTHDAY = date(2026, 2, 9) # 改生日 (YYYY, M, D)

TITLE = f"Happy Birthday, {HIS_NAME} 🎂"

MESSAGE_TOP = "A quiet birthday note for you."
MESSAGE_BODY = (
    "Happy Birthday.\n"
    "Happy Birthday.\n\n"
    "THappy Birthday.\n"
    "Happy Birthday.\n\n"
    "Happy Birthday.\n"
    "And Happy Birthday."
)
MESSAGE_BOTTOM = (
    "May this year be gentle with you.\n"
    "May you feel loved in ways that are simple, real, and lasting."
)
SIGNATURE = f"— {YOUR_NAME}"

PHOTO_DIR = "photos"
BGM_PATH = "assets/bgm.mp3"   # 把音乐放这里
# ------------------------------------------------


def file_to_data_uri(filepath: str, mime: str) -> str:
    p = Path(filepath)
    if not p.exists():
        return ""
    data = p.read_bytes()
    b64 = base64.b64encode(data).decode("utf-8")
    return f"data:{mime};base64,{b64}"


def list_photos(folder: str):
    paths = []
    if os.path.isdir(folder):
        for fn in os.listdir(folder):
            if fn.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                paths.append(os.path.join(folder, fn))
    return sorted(paths)


st.set_page_config(page_title=TITLE, page_icon="🎂", layout="centered")

photos = list_photos(PHOTO_DIR)
if len(photos) < 1:
    st.error("No photos found. Put at least 1 image into the 'photos/' folder.")
    st.stop()

# 取前三张做轮播（不足三张就循环使用）
p1 = photos[0] if len(photos) >= 1 else photos[0]
p2 = photos[1] if len(photos) >= 2 else photos[0]
p3 = photos[2] if len(photos) >= 3 else photos[0]

img1 = file_to_data_uri(p1, "image/jpeg")
img2 = file_to_data_uri(p2, "image/jpeg")
img3 = file_to_data_uri(p3, "image/jpeg")

bgm_uri = file_to_data_uri(BGM_PATH, "audio/mpeg")

today = date.today()
days = (BIRTHDAY - today).days
if days > 0:
    countdown = f"{days} days to go"
elif days == 0:
    countdown = "Today."
else:
    countdown = f"{-days} days since"

# ---- UI Controls (minimal & not “flashy”) ----
st.markdown("### ")
# colA, colB = st.columns([1, 1])
# with colA:
#    music_on = st.toggle("Play music", value=False)
# with colB:
#     sparkle_on = st.toggle("Sparkles", value=True)

# ---- Paper-card + Sparkles + Slideshow + Audio (HTML/CSS/JS) ----
# 暖色纸质背景 + 轻微纹理（用 CSS 渐变模拟）
# 星光：纯 CSS 小点 + 闪烁动画
# 轮播：JS 每 3.5 秒切换背景图
# 音乐：audio 标签，toggle 控制播放

music_on = True     
sparkle_on = True

html = f"""
<div class="stage">
  <div class="paper">
    <div class="countdown">{countdown}</div>

    <div class="photo-frame" id="photoFrame">
      <div class="photo-overlay"></div>
    </div>

    <div class="content">
      <div class="title">{TITLE}</div>
      <div class="subtitle">{MESSAGE_TOP}</div>

      <div class="text">{MESSAGE_BODY.replace("\n", "<br>")}</div>
      <div class="text bottom">{MESSAGE_BOTTOM.replace("\n", "<br>")}</div>

      <div class="sig">{SIGNATURE}</div>
    </div>
  </div>

  <div class="sparkles" id="sparkles"></div>

  <audio id="bgm" loop>
    {"<source src='" + bgm_uri + "' type='audio/mpeg' />" if bgm_uri else ""}
  </audio>
</div>

<style>
  :root {{
    --paper: #fbf3e6;
    --ink: rgba(25, 20, 16, 0.88);
    --muted: rgba(25, 20, 16, 0.55);
    --shadow: rgba(0,0,0,0.10);
  }}

  body {{
    background: radial-gradient(1200px 600px at 50% 10%, #fff7ee 0%, #f6efe6 40%, #efe6da 100%) !important;
  }}

  .stage {{
    position: relative;
    width: 100%;
    display: flex;
    justify-content: center;
    padding: 18px 0 40px 0;
  }}

  .paper {{
    position: relative;
    width: min(760px, 92vw);
    border-radius: 22px;
    padding: 18px 18px 26px 18px;
    box-shadow: 0 18px 55px var(--shadow);
    border: 1px solid rgba(0,0,0,0.06);

    /* paper texture */
    background:
      radial-gradient(1000px 600px at 20% 10%, rgba(255,255,255,0.75) 0%, rgba(255,255,255,0.0) 55%),
      radial-gradient(900px 540px at 80% 30%, rgba(255,255,255,0.55) 0%, rgba(255,255,255,0.0) 60%),
      linear-gradient(180deg, #fff7ef 0%, var(--paper) 35%, #f7eddc 100%);
    overflow: hidden;
  }}

  .countdown {{
    font-size: 12px;
    color: var(--muted);
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin: 2px 4px 10px 6px;
  }}

  .photo-frame {{
    position: relative;
    width: 100%;
    height: 360px;
    border-radius: 18px;
    overflow: hidden;
    background-size: cover;
    background-position: center;
    filter: saturate(1.02) contrast(1.02);
    box-shadow: 0 12px 32px rgba(0,0,0,0.10);
  }}

  /* soft vignette + warm tint */
  .photo-overlay {{
    position: absolute;
    inset: 0;
    background:
      radial-gradient(900px 500px at 50% 20%, rgba(255,245,230,0.25) 0%, rgba(0,0,0,0.18) 80%),
      linear-gradient(180deg, rgba(255,235,210,0.10) 0%, rgba(0,0,0,0.12) 100%);
    pointer-events: none;
  }}

  .content {{
    padding: 18px 10px 0 10px;
  }}

  .title {{
    font-size: 32px;
    font-weight: 750;
    color: var(--ink);
    margin: 6px 0 6px 0;
    line-height: 1.12;
  }}

  .subtitle {{
    font-size: 14px;
    color: var(--muted);
    margin-bottom: 14px;
    letter-spacing: 0.02em;
  }}

  .text {{
    font-size: 16px;
    line-height: 1.85;
    color: var(--ink);
    white-space: normal;
  }}

  .text.bottom {{
    margin-top: 12px;
  }}

  .sig {{
    margin-top: 14px;
    font-size: 16px;
    color: rgba(25, 20, 16, 0.75);
  }}

  /* Sparkles layer */
  .sparkles {{
    position: absolute;
    inset: 0;
    pointer-events: none;
    opacity: {"1" if sparkle_on else "0"};
    transition: opacity 0.6s ease;
  }}

  .sparkle {{
    position: absolute;
    width: 2px;
    height: 2px;
    border-radius: 999px;
    background: rgba(255,255,255,0.9);
    box-shadow: 0 0 10px rgba(255,255,255,0.9);
    animation: twinkle var(--dur) ease-in-out infinite;
    opacity: 0.0;
  }}

  @keyframes twinkle {{
    0%   {{ opacity: 0.0; transform: scale(0.8); }}
    45%  {{ opacity: 0.9; transform: scale(1.4); }}
    100% {{ opacity: 0.0; transform: scale(0.8); }}
  }}

  @media (max-width: 520px) {{
    .paper {{
      width: 94vw !important;
      padding: 14px 12px 18px 12px !important;
      border-radius: 18px !important;
    }}

    .photo-frame {{
      height: 240px !important;
      border-radius: 14px !important;
    }}

    .title {{
      font-size: 24px !important;
    }}

    .text {{
      font-size: 14px !important;
      line-height: 1.75 !important;
    }}
  }}
  
  .stage {{ min-height: 1800px; }}
  .paper {{ display: block; }}

</style>

<script>
  const photos = ["{img1}", "{img2}", "{img3}"].filter(Boolean);
  const frame = document.getElementById("photoFrame");
  let i = 0;

  function setPhoto(idx) {{
    if (!photos.length) return;
    frame.style.backgroundImage = `url('${{photos[idx]}}')`;
  }}

  setPhoto(i);
  setInterval(() => {{
    i = (i + 1) % photos.length;
    setPhoto(i);
  }}, 2000);

  // Sparkles: generate stars
  const sparkleLayer = document.getElementById("sparkles");
  sparkleLayer.innerHTML = "";
  const N = 70;
  for (let k = 0; k < N; k++) {{
    const s = document.createElement("div");
    s.className = "sparkle";
    const x = Math.random() * 100;
    const y = Math.random() * 100;
    const dur = (2.2 + Math.random() * 3.2).toFixed(2) + "s";
    const delay = (Math.random() * 3.0).toFixed(2) + "s";
    s.style.left = x + "%";
    s.style.top = y + "%";
    s.style.setProperty("--dur", dur);
    s.style.animationDelay = delay;
    sparkleLayer.appendChild(s);
  }}

  // Music control
  const audio = document.getElementById("bgm");
  const shouldPlay = {str(music_on).lower()};
  if (audio && shouldPlay) {{
    // Many browsers block autoplay without a user gesture.
    // Streamlit toggle counts as user interaction; try play and ignore errors.
    audio.volume = 0.6;
    audio.play().catch(() => {{}});
  }} else if (audio) {{
    audio.pause();
  }}
</script>
"""

st.components.v1.html(html, height=2200, scrolling=True)


# Small note if no music file
if not Path(BGM_PATH).exists():
    st.caption("Tip: Put your background music at assets/bgm.mp3 (optional).")
