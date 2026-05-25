import streamlit as st
import datetime
import base64
import os
import json
import urllib.parse
from PIL import Image

# ══════════════════════════════════════════════════════════════════════════════
# 1. INITIALIZATION & UTILITIES
# ══════════════════════════════════════════════════════════════════════════════
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Ensure directories exist
os.makedirs(os.path.join(BASE_DIR, "zdjecia"), exist_ok=True)

# Emojis/SVGs for navigation
SVG_HOME = """<svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>"""
SVG_EDIT = """<svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"></path><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path></svg>"""
SVG_CHECK = """<svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>"""
SVG_SETTINGS = """<svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>"""
SVG_USER = """<svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>"""
SVG_ADD_DATA = """<svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path><rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect><line x1="12" y1="11" x2="12" y2="17"></line><line x1="9" y1="14" x2="15" y2="14"></line></svg>"""
SVG_DAY = """<svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="2" width="14" height="20" rx="2" ry="2"></rect><line x1="12" y1="18" x2="12.01" y2="18"></line></svg>"""
SVG_WEEK = """<svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>"""

# ══════════════════════════════════════════════════════════════════════════════
# 2. PWA SETUP & FAVICON
# ══════════════════════════════════════════════════════════════════════════════

ICON_DIR = os.path.join(BASE_DIR, "App Icon")
if not os.path.exists(ICON_DIR):
    os.makedirs(ICON_DIR, exist_ok=True)

icon_src = os.path.join(ICON_DIR, "icon_192.png")
icon_512_path = os.path.join(ICON_DIR, "icon_512.png")
icon_fav_path = os.path.join(BASE_DIR, "zdjecia", "icon.png")

# If icon_192.png exists, use it; otherwise generate a fallback MS icon
if not os.path.exists(icon_src):
    try:
        from PIL import Image, ImageDraw, ImageFont
        img = Image.new('RGBA', (192, 192), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse([8, 8, 184, 184], outline='#006089', width=6)
        try:
            font = ImageFont.truetype("arial.ttf", 75)
        except IOError:
            font = ImageFont.load_default()
        try:
            left, top, right, bottom = draw.textbbox((0, 0), "MS", font=font)
            w = right - left; h = bottom - top
        except AttributeError:
            w, h = draw.textsize("MS", font=font)
        x = (192 - w) // 2; y = (192 - h) // 2 - 5
        draw.text((x, y), "MS", fill='#006089', font=font)
        img.save(icon_src, 'PNG')
        print(f"Generated fallback MS icon at {icon_src}")
    except Exception as e:
        print(f"Error generating icon: {e}")

# Open icon_192.png and create 512x512 version
try:
    img_pil = Image.open(icon_src)
    if img_pil.size != (192, 192):
        img_pil = img_pil.resize((192, 192), Image.LANCZOS)
        img_pil.save(icon_src, 'PNG')

    img_512 = img_pil.resize((512, 512), Image.LANCZOS)
    img_512.save(icon_512_path, 'PNG')

    img_pil.save(icon_fav_path, 'PNG')
except Exception as e:
    print(f"Icon processing error: {e}")
    # Last resort: create blank icon
    img = Image.new('RGBA', (192, 192), (0, 0, 0, 0))
    img.save(icon_fav_path, 'PNG')
    img.resize((512, 512), Image.LANCZOS).save(icon_512_path, 'PNG')
    img.save(icon_src, 'PNG')

# Load icon bytes and base64
with open(icon_src, "rb") as f:
    icon_bytes_192 = f.read()
    ICON_B64 = base64.b64encode(icon_bytes_192).decode()
with open(icon_512_path, "rb") as f:
    icon_bytes_512 = f.read()
    ICON_B64_512 = base64.b64encode(icon_bytes_512).decode()

# Initialize Streamlit Page Config
st.set_page_config(
    page_title="Szkielet MS",
    page_icon=os.path.join(BASE_DIR, "zdjecia", "icon.png"),
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Wstrzyknięcie meta/link tagów PWA przez st.markdown (wykrywane przez mobilne Safari)
st.markdown(f"""
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="default">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-title" content="Szkielet MS">
    <meta name="theme-color" content="#006089">
    <link rel="apple-touch-icon" href="data:image/png;base64,{ICON_B64}">
    <link rel="apple-touch-icon-precomposed" href="data:image/png;base64,{ICON_B64}">
""", unsafe_allow_html=True)

# ── Wstrzykiwanie PWA tagów do GŁÓWNEGO dokumentu (parent) przez JS ──
# To jest niezbędne na Streamlit Cloud, gdzie nie ma dostępu do plików instalacyjnych Streamlita.
# Wszystko (ikona, manifest, meta) idzie przez JS do parent.document.head.

PWA_MANIFEST = {
    "name": "Szkielet MS",
    "short_name": "Szkielet",
    "start_url": ".",
    "display": "standalone",
    "background_color": "#F2F7FA",
    "theme_color": "#006089",
    "icons": [
        {"src": f"data:image/png;base64,{ICON_B64}", "sizes": "192x192", "type": "image/png"},
        {"src": f"data:image/png;base64,{ICON_B64_512}", "sizes": "512x512", "type": "image/png"}
    ]
}

PWA_MANIFEST_JSON = json.dumps(PWA_MANIFEST)

PWA_SW_JS = """self.addEventListener('install', (e) => { e.waitUntil(self.skipWaiting()); });
self.addEventListener('activate', (e) => { e.waitUntil(self.clients.claim()); });
self.addEventListener('fetch', (e) => {
  e.respondWith(fetch(e.request).catch(() => new Response('', { status: 408 })));
});"""

st.components.v1.html(f"""
<script>
(function() {{
    var pdoc = window.parent.document;
    if (!pdoc) return;
    
    var iconB64 = 'data:image/png;base64,{ICON_B64}';
    
    // --- Meta tags ---
    var metas = [
        ['apple-mobile-web-app-capable', 'yes'],
        ['apple-mobile-web-app-status-bar-style', 'default'],
        ['mobile-web-app-capable', 'yes'],
        ['apple-mobile-web-app-title', 'Szkielet MS'],
        ['theme-color', '#006089']
    ];
    metas.forEach(function(m) {{
        var el = pdoc.querySelector('meta[name="' + m[0] + '"]');
        if (!el) {{ el = pdoc.createElement('meta'); el.name = m[0]; pdoc.head.appendChild(el); }}
        el.content = m[1];
    }});
    
    // --- Apple touch icons ---
    var setLink = function(rel, href, extra) {{
        var el = pdoc.querySelector('link[rel="' + rel + '"]');
        if (!el) {{ el = pdoc.createElement('link'); el.rel = rel; pdoc.head.appendChild(el); }}
        el.href = href;
        if (extra) {{ for (var k in extra) el.setAttribute(k, extra[k]); }}
    }};
    setLink('apple-touch-icon', iconB64);
    setLink('apple-touch-icon-precomposed', iconB64);
    setLink('icon', iconB64, {{type:'image/png'}});
    setLink('shortcut icon', iconB64, {{type:'image/png'}});
    
    // --- Manifest as Blob URL ---
    var manifestJson = '{PWA_MANIFEST_JSON}';
    var blob = new Blob([manifestJson], {{type: 'application/json'}});
    var manifestUrl = URL.createObjectURL(blob);
    setLink('manifest', manifestUrl);
    
    // --- Service Worker (tylko jeśli /sw.js istnieje) ---
    fetch('/sw.js').then(function(r) {{
        if (r.ok && 'serviceWorker' in navigator) {{
            navigator.serviceWorker.register('/sw.js');
        }}
    }}).catch(function(){{}});
}})();
</script>
""", height=0)

# Dynamiczne wstrzyknięcie SW i manifestu jako trasy Starlette (działa po rozgrzaniu serwera)
def inject_pwa_routes():
    try:
        import gc
        from streamlit.web.server.server import Server
        from starlette.responses import Response

        servers = [obj for obj in gc.get_objects() if isinstance(obj, Server)]
        if not servers:
            return
        server = servers[0]
        starlette_server = getattr(server, "_starlette_server", None)
        if not starlette_server:
            return
        app = getattr(starlette_server, "app", None) or getattr(starlette_server, "_server", None)
        if not app:
            app = starlette_server
        if hasattr(app, "routes"):
            existing = [r.path for r in app.routes if hasattr(r, "path")]
            for route_path, content_type, content in [
                ("/sw.js", "application/javascript", PWA_SW_JS),
                ("/manifest.json", "application/json", json.dumps(PWA_MANIFEST)),
                ("/favicon.png", "image/png", icon_bytes_192),
                ("/favicon.ico", "image/x-icon", icon_bytes_192),
                ("/apple-touch-icon.png", "image/png", icon_bytes_192),
                ("/apple-touch-icon-precomposed.png", "image/png", icon_bytes_192),
            ]:
                if route_path not in existing:
                    @app.route(route_path)
                    async def route(request, ct=content_type, c=content):
                        return Response(content=c, media_type=ct)
                    existing.append(route_path)
    except Exception:
        pass

inject_pwa_routes()

# ══════════════════════════════════════════════════════════════════════════════
# 3. CONSOLIDATED PREMIUM CSS DESIGN SYSTEM
# ══════════════════════════════════════════════════════════════════════════════
def inject_custom_css():
    st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&display=swap" rel="stylesheet">
<style>
    html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMainViewContainer"], [data-testid="stHeader"] {
        background: #F2F7FA !important;
        background-color: #F2F7FA !important;
        color: #1B2B3A;
        font-family: 'Nunito', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    [data-testid="stSidebar"] { display: none; }
    header { visibility: hidden; height: 0px !important; }
    footer { display: none !important; visibility: hidden !important; }
    #MainMenu { display: none !important; }
    [data-testid="stToolbar"] { display: none !important; }
    [data-testid="stDecoration"] { display: none !important; }
    [data-testid="stStatusWidget"] { display: none !important; }
    [data-testid="stFooter"] { display: none !important; }
    [data-testid="stSidebarNav"] { display: none !important; }
    .stDeployButton { display: none !important; }
    div:has(> a[href*="streamlit.io/cloud"]) { display: none !important; }
    a[href*="streamlit.io/cloud"] { display: none !important; }
    [data-testid="stActionButton"] { display: none !important; }

    .block-container {
        padding-top: 1.5rem !important;
        max-width: 98% !important;
        padding-bottom: 5rem !important;
    }

    .mobile-nav-item-icon svg,
    .ios-action-icon svg {
        width: 100%;
        height: 100%;
        display: block;
    }

    div[data-testid="stTextInput"]:has(input[aria-label="js_data_exchange"]),
    div[data-testid="stTextInput"]:has(input[id*="js_data_input"]) {
        position: absolute !important;
        left: -9999px !important;
        opacity: 0 !important;
        pointer-events: none !important;
    }

    .main-layout {
        display: flex;
        gap: 24px;
        overflow: visible !important;
    }

    .tile-link {
        text-decoration: none !important;
        display: block;
        position: relative;
        border-radius: 20px;
        overflow: hidden;
        background: #ffffff;
        border: 1px solid rgba(0, 0, 0, 0.06);
        margin-bottom: 12px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100px;
        cursor: pointer;
    }
    .tile-link:hover {
        transform: translateX(5px);
        border-color: #006089;
        background: #f8fafc;
    }
    .tile-bg-icon-container {
        position: absolute;
        top: 50%;
        right: 20px;
        transform: translateY(-50%);
        z-index: 1;
        opacity: 0.12;
        transition: all 0.3s ease;
        color: #006089;
    }
    .tile-link:hover .tile-bg-icon-container {
        opacity: 0.3;
        transform: translateY(-50%) scale(1.15);
    }
    .tile-content {
        position: relative;
        z-index: 3;
        padding: 15px 20px;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .tile-label {
        color: #006089;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 4px;
    }
    .tile-title {
        font-size: 18px;
        font-weight: 700;
        color: #1B2B3A;
        margin-bottom: 2px;
    }
    .tile-desc {
        font-size: 11px;
        color: #6B7B8D;
        line-height: 1.3;
    }

    .control-panel-card {
        background: #ffffff;
        border: 1px solid rgba(0, 96, 137, 0.15);
        border-radius: 24px;
        padding: 20px;
        margin-bottom: 25px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .header-section {
        background: #ffffff;
        border: 1px solid rgba(0, 0, 0, 0.05);
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .page-title {
        font-size: 24px;
        font-weight: 800;
        color: #1B2B3A;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .content-card {
        background: #ffffff;
        border: 1px solid rgba(0, 0, 0, 0.04);
        border-radius: 20px;
        padding: 24px;
        margin-bottom: 20px;
    }

    .ios-top-bar-wrapper {
        display: none;
        flex-direction: column;
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 9999;
        width: 100%;
        background: #ffffff !important;
        border-bottom: 1px solid rgba(0, 96, 137, 0.2);
        padding-top: env(safe-area-inset-top, 0px);
    }
    .ios-nav-bar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 16px;
        height: 56px;
        gap: 10px;
    }
    .ios-hamburger {
        width: 38px;
        height: 38px;
        border-radius: 50%;
        background: rgba(0, 0, 0, 0.04);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 5px;
        cursor: pointer;
        flex-shrink: 0;
        transition: background 0.2s ease;
        border: 1px solid rgba(0,0,0,0.06);
    }
    .ios-hamburger:active { background: rgba(0, 96, 137, 0.1); }
    .ios-hamburger span {
        display: block;
        width: 16px;
        height: 2px;
        background: #1B2B3A;
        border-radius: 2px;
        transition: all 0.25s ease;
    }
    .ios-hamburger.open span:nth-child(1) { transform: rotate(45deg) translate(5px, 5px); }
    .ios-hamburger.open span:nth-child(2) { opacity: 0; width: 0; }
    .ios-hamburger.open span:nth-child(3) { transform: rotate(-45deg) translate(5px, -5px); }

    .ios-nav-center {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        flex: 1;
        text-align: center;
        min-width: 0;
    }
    .ios-nav-title {
        font-size: 16px;
        font-weight: 800;
        color: #006089;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        line-height: 1.1;
        white-space: nowrap;
    }
    .ios-nav-subtitle {
        font-size: 10px;
        color: #6B7B8D;
        font-weight: 500;
        letter-spacing: 0.3px;
        margin-top: 1px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 180px;
    }
    .ios-avatar {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background: linear-gradient(135deg, #006089 0%, #003D5C 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        font-weight: 900;
        color: #ffffff;
        flex-shrink: 0;
        cursor: pointer;
        box-shadow: 0 0 12px rgba(0, 96, 137, 0.25);
        border: 1.5px solid rgba(0, 96, 137, 0.3);
    }
    .ios-avatar:active { box-shadow: 0 0 20px rgba(0, 96, 137, 0.5); }

    .ios-bottom-bar-wrapper {
        display: none;
    }
    .ios-action-btn {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background: transparent !important;
        border: none !important;
        color: #6B7B8D;
        cursor: pointer;
        transition: all 0.2s ease;
        flex: 0 1 100px;
        margin: 0 15px;
        gap: 3px;
        user-select: none;
    }
    .ios-action-btn:active { transform: scale(0.92); }
    .ios-action-btn.active {
        color: #006089 !important;
    }
    .ios-action-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 20px;
        height: 20px;
    }
    .ios-action-text {
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 0.5px;
    }

    .mobile-nav-dropdown {
        display: none;
        background: rgba(255, 255, 255, 0.98);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-bottom: 1px solid rgba(0, 96, 137, 0.15);
        padding: 8px 12px 12px 12px;
        flex-direction: column;
        gap: 6px;
        z-index: 9998;
    }
    .mobile-nav-item {
        padding: 13px 18px;
        background: rgba(0,0,0,0.02);
        border-radius: 14px;
        color: #1B2B3A;
        text-decoration: none;
        font-weight: 700;
        font-size: 15px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: background 0.15s ease;
        border: 1px solid rgba(0,0,0,0.04);
    }
    .mobile-nav-item:hover { background: rgba(0, 96, 137, 0.06); color: #006089; }
    .mobile-nav-item:active { background: rgba(0, 96, 137, 0.12); }
    .mobile-nav-item-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 18px;
        height: 18px;
        margin-right: 10px;
        vertical-align: middle;
        color: #6B7B8D;
    }
    .mobile-nav-item:hover .mobile-nav-item-icon { color: #006089; }
    .mobile-nav-item-arrow { color: #aaa; font-size: 12px; }

    .desktop-only { display: block; }
    .mobile-only { display: none; }

    @media (min-width: 1001px) {
        .mobile-sidebar-content { display: block !important; }
    }

    @media (max-width: 1000px) {
        .ios-top-bar-wrapper { display: flex; }
        .mobile-sidebar-content { display: none !important; }
        .mobile-nav-dropdown { display: flex; }

        .desktop-only { display: none !important; }
        .mobile-only { display: block !important; }

        .block-container {
            padding-top: calc(56px + env(safe-area-inset-top, 0px)) !important;
            padding-left: 10px !important;
            padding-right: 10px !important;
        }
        header[data-testid="stHeader"] { display: none !important; }

        .ios-bottom-bar-wrapper {
            display: flex;
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            z-index: 9999;
            background: rgba(255, 255, 255, 0.97);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-top: 1px solid rgba(0,0,0,0.08);
            padding: 10px 0 calc(10px + env(safe-area-inset-bottom, 12px)) 0;
            justify-content: center;
            align-items: center;
            box-shadow: 0 -4px 15px rgba(0,0,0,0.08);
        }
    }

    div[data-testid="stForm"] {
        border: 1px solid rgba(0, 0, 0, 0.06) !important;
        background: #ffffff !important;
        border-radius: 20px !important;
        padding: 20px !important;
    }

    .stSelectbox div[data-baseweb="select"] {
        background-color: #ffffff !important;
        border: 1px solid rgba(0, 0, 0, 0.1) !important;
        border-radius: 12px !important;
    }

    .stDateInput div[data-baseweb="input"] {
        background-color: #ffffff !important;
        border: 1px solid rgba(0, 0, 0, 0.1) !important;
        border-radius: 12px !important;
    }
</style>
""", unsafe_allow_html=True)

# Run CSS Injection
inject_custom_css()

# ══════════════════════════════════════════════════════════════════════════════
# 4. GENERIC DATA & SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════

SAMPLE_ITEMS = ["Element A", "Element B", "Element C", "Element D"]
SAMPLE_CATEGORIES = {
    "Kategoria 1": ["Podkategoria A1", "Podkategoria A2", "Podkategoria A3"],
    "Kategoria 2": ["Podkategoria B1", "Podkategoria B2"],
    "Kategoria 3": ["Podkategoria C1", "Podkategoria C2", "Podkategoria C3"],
}

if "page" not in st.session_state:
    st.session_state.page = "home"
if "mobile_menu" not in st.session_state:
    st.session_state.mobile_menu = False
if "last_js_data" not in st.session_state:
    st.session_state.last_js_data = ""
if "selected_item" not in st.session_state:
    st.session_state.selected_item = SAMPLE_ITEMS[0]
if "selected_category" not in st.session_state:
    st.session_state.selected_category = list(SAMPLE_CATEGORIES.keys())[0]

# ══════════════════════════════════════════════════════════════════════════════
# 5. ACTION PROCESSOR
# ══════════════════════════════════════════════════════════════════════════════

# Hidden text input representing the communications bridge from JS to Python
js_data = st.text_input("js_data_exchange", key="js_data_input", label_visibility="collapsed")

if js_data and js_data != st.session_state.last_js_data:
    st.session_state.last_js_data = js_data
    try:
        # Parse query string parameters passed from JavaScript click handler
        parts = {k: urllib.parse.unquote(v) for k, v in [p.split('=') for p in js_data.split('&')]}
        action = parts.get('action')
        
        if action == "nav":
            st.session_state.page = parts.get('page', 'home')
            st.session_state.mobile_menu = False # close menu on navigate
            st.rerun()
        elif action == "toggle_menu":
            st.session_state.mobile_menu = not st.session_state.mobile_menu
            st.rerun()
        elif action == "v_edit":
            st.session_state.page = "settings"
            st.rerun()
    except Exception as e:
        print(f"Action error: {e}")

# Helper for rendering Bento Menu Tiles on Desktop
def render_bento_tile(label, title, desc, page_name, icon_svg):
    is_active = st.session_state.page == page_name
    active_border = "border-color: #006089; background: #f0f7fa;" if is_active else ""
    tile_html = f"""
    <div class="tile-link" style="{active_border}" data-action="action=nav&page={page_name}">
        <div class="tile-bg-icon-container">{icon_svg}</div>
        <div class="tile-content">
            <div class="tile-label">{label}</div>
            <div class="tile-title">{title}</div>
            <div class="tile-desc">{desc}</div>
        </div>
    </div>
    """
    st.markdown(tile_html, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 6. HEADER & MOBILE BARS GENERATION
# ══════════════════════════════════════════════════════════════════════════════

today_label = datetime.date.today().strftime("%d.%m.%Y")
week_num = datetime.date.today().isocalendar()[1]
ios_hbg_open = "open" if st.session_state.mobile_menu else ""

st.markdown(f"""
<div class="ios-top-bar-wrapper">
  <div class="ios-nav-bar">
    <div class="ios-hamburger {ios_hbg_open}" data-action="action=toggle_menu">
      <span class="hbr"></span>
      <span class="hbr"></span>
      <span class="hbr"></span>
    </div>
    <div class="ios-nav-center">
      <div class="ios-nav-title">Szkielet MS</div>
      <div class="ios-nav-subtitle">{today_label}</div>
    </div>
    <div class="ios-avatar" data-action="action=nav&page=settings">MS</div>
  </div>
</div>

<div class="ios-bottom-bar-wrapper">
  <div class="ios-action-btn {"active" if st.session_state.page == "home" else ""}" data-action="action=nav&page=home">
    <span class="ios-action-icon">{SVG_HOME}</span>
    <span class="ios-action-text">HOME</span>
  </div>
  <div class="ios-action-btn {"active" if st.session_state.page == "form" else ""}" data-action="action=nav&page=form">
    <span class="ios-action-icon">{SVG_ADD_DATA}</span>
    <span class="ios-action-text">FORMULARZ</span>
  </div>
  <div class="ios-action-btn {"active" if st.session_state.page == "settings" else ""}" data-action="action=nav&page=settings">
    <span class="ios-action-icon">{SVG_SETTINGS}</span>
    <span class="ios-action-text">USTAWIENIA</span>
  </div>
</div>
""", unsafe_allow_html=True)

if st.session_state.mobile_menu:
    st.markdown(f"""
    <div class="mobile-nav-dropdown">
        <a class="mobile-nav-item" data-action="action=nav&page=home">
            <span><span class="mobile-nav-item-icon">{SVG_HOME}</span> STRONA GŁÓWNA</span>
            <span class="mobile-nav-item-arrow">›</span>
        </a>
        <a class="mobile-nav-item" data-action="action=nav&page=form">
            <span><span class="mobile-nav-item-icon">{SVG_ADD_DATA}</span> FORMULARZ</span>
            <span class="mobile-nav-item-arrow">›</span>
        </a>
        <a class="mobile-nav-item" data-action="action=nav&page=settings">
            <span><span class="mobile-nav-item-icon">{SVG_SETTINGS}</span> USTAWIENIA</span>
            <span class="mobile-nav-item-arrow">›</span>
        </a>
        <div style="text-align: center; color: #6B7B8D; font-size: 11px; padding: 15px 0 5px 0; border-top: 1px solid rgba(0,0,0,0.05); margin-top: 10px;">Szkielet MS v1.0</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-layout">', unsafe_allow_html=True)
col_side, col_main = st.columns([1, 4])

with col_side:
    control_panel_html = f"""
    <div class="control-panel-card desktop-only">
        <div>
            <div class="tile-label">PANEL DOWODZENIA</div>
            <div style="font-size: 22px; font-weight: 800; color: #1B2B3A; margin-top: 10px;">Witaj, MS!</div>
            <div style="font-size: 13px; color: #6B7B8D; margin-top: 5px;">{today_label}</div>
        </div>
    </div>
    """
    st.markdown(control_panel_html, unsafe_allow_html=True)
    
    st.markdown('<div class="mobile-sidebar-content">', unsafe_allow_html=True)
    render_bento_tile("START", "Strona Główna", "Widok startowy aplikacji", "home", SVG_HOME)
    render_bento_tile("DANE", "Formularz", "Przykładowy formularz", "form", SVG_ADD_DATA)
    render_bento_tile("KONFIGURACJA", "Ustawienia", "Konfiguracja szkieletu", "settings", SVG_SETTINGS)
    st.markdown('</div>', unsafe_allow_html=True)

with col_main:
    if st.session_state.page == "home":
        st.markdown(f'<div class="header-section"><div class="page-title">{SVG_HOME} Strona Główna</div></div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="content-card">
            <h3>Witaj w szkielecie aplikacji!</h3>
            <p style="color: #6B7B8D; margin-top: 8px;">
                Ten szkielet stanowi bazę do budowy nowych aplikacji Streamlit 
                z gotowym responsywnym interfejsem (mobile + desktop).
            </p>
            <div style="margin-top: 20px; display: flex; gap: 12px; flex-wrap: wrap;">
                <div style="background: #F2F7FA; border-radius: 14px; padding: 16px; flex: 1; min-width: 140px;">
                    <div style="font-size: 24px; font-weight: 800; color: #006089;">3</div>
                    <div style="font-size: 12px; color: #6B7B8D; margin-top: 4px;">Podstrony</div>
                </div>
                <div style="background: #F2F7FA; border-radius: 14px; padding: 16px; flex: 1; min-width: 140px;">
                    <div style="font-size: 24px; font-weight: 800; color: #006089;">iOS</div>
                    <div style="font-size: 12px; color: #6B7B8D; margin-top: 4px;">Top & Bottom Bar</div>
                </div>
                <div style="background: #F2F7FA; border-radius: 14px; padding: 16px; flex: 1; min-width: 140px;">
                    <div style="font-size: 24px; font-weight: 800; color: #006089;">PWA</div>
                    <div style="font-size: 12px; color: #6B7B8D; margin-top: 4px;">Gotowe do instalacji</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    elif st.session_state.page == "form":
        st.markdown(f'<div class="header-section"><div class="page-title">{SVG_ADD_DATA} Formularz</div></div>', unsafe_allow_html=True)
        
        col_a, col_b = st.columns(2)
        with col_a:
            selected = st.selectbox("Wybierz opcję", SAMPLE_ITEMS, key="selected_item")
        with col_b:
            cat = st.selectbox("Wybierz kategorię", list(SAMPLE_CATEGORIES.keys()), key="selected_category")
        
        sub = SAMPLE_CATEGORIES.get(cat, [])
        if sub:
            picked = st.selectbox("Podkategoria", sub)
        
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        col_1, col_2 = st.columns(2)
        with col_1:
            st.button("WYCZYŚĆ", key="btn_clear", use_container_width=True)
        with col_2:
            if st.button("ZAPISZ", key="btn_save", type="primary", use_container_width=True):
                st.success("Przykładowy zapis — dane do podpięcia w przyszłości.")
        
    elif st.session_state.page == "settings":
        st.markdown(f'<div class="header-section"><div class="page-title">{SVG_SETTINGS} Ustawienia</div></div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="content-card">
            <h3>Konfiguracja szkieletu</h3>
            <p style="color: #6B7B8D; margin-top: 8px;">Miejsce na przyszłe ustawienia aplikacji.</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 7. JS BRIDGE / EVENT LISTENERS
# ══════════════════════════════════════════════════════════════════════════════
st.components.v1.html(f"""
<script>
// Action Bridge: focus hidden input and dispatch change event back to Streamlit
window.parent.sendActionToStreamlit = function(actionStr) {{
    const parentWin = window.parent;
    const parentDoc = parentWin.document;
    const inputs = parentDoc.querySelectorAll('input');
    let target = null;
    inputs.forEach(i => {{ if(i.getAttribute('aria-label') === 'js_data_exchange') target = i; }});
    if(target) {{
        target.focus();
        const setter = Object.getOwnPropertyDescriptor(parentWin.HTMLInputElement.prototype, 'value').set;
        setter.call(target, actionStr + '&ts=' + Date.now());
        target.dispatchEvent(new parentWin.Event('input', {{ bubbles: true }}));
        target.dispatchEvent(new parentWin.Event('change', {{ bubbles: true }}));
        target.blur();
    }}
}};

// Click Handler: listen to clicks on data-action attribute
const doc = document;
window.parent.trainerClickHandler = (e) => {{
    let el = e.target;
    while (el && el !== doc.body) {{
        if (el.hasAttribute('data-action')) {{
            e.preventDefault();
            e.stopPropagation();
            let actionStr = el.getAttribute('data-action');
            if (window.parent.sendActionToStreamlit) {{
                window.parent.sendActionToStreamlit(actionStr);
            }}
            return;
        }}
        el = el.parentElement;
    }}
}};

// Clean up stale listener and bind click handler to window frame
if (window.parent.trainerClickHandlerBound) {{
    doc.body.removeEventListener('click', window.parent.trainerClickHandler);
}}
doc.body.addEventListener('click', window.parent.trainerClickHandler);
window.parent.trainerClickHandlerBound = true;

// Diagnostic flag
doc.body.setAttribute('data-bridge-active', 'true');
</script>
""", height=0)

# Agresywne ukrywanie elementów Streamlit (Made with, toolbar, itp.)
hide_html = ("""
<script>
(function() {
    var docs = [];
    try { docs.push(window.top.document); } catch(e) {}
    try { docs.push(window.parent.document); } catch(e) {}
    
    try {
        var tdoc = window.top.document;

        var hideStyle = tdoc.createElement('style');
        hideStyle.textContent = 'footer,#MainMenu,[data-testid="stToolbar"],[data-testid="stDecoration"],[data-testid="stStatusWidget"],[data-testid="stFooter"],[data-testid="stSidebarNav"],.stDeployButton,[data-testid="stActionButton"],a[href*="streamlit.io/cloud"],a[href*="streamlit.io"]{display:none!important}';
        tdoc.head.appendChild(hideStyle);

        var iconB64 = 'data:image/png;base64,__ICON__';
        ['apple-touch-icon', 'apple-touch-icon-precomposed', 'icon', 'shortcut icon'].forEach(function(rel) {
            var link = tdoc.createElement('link');
            link.rel = rel;
            link.href = iconB64;
            if (rel === 'icon' || rel === 'shortcut icon') link.type = 'image/png';
            tdoc.head.appendChild(link);
        });
        [['apple-mobile-web-app-capable', 'yes'],
         ['apple-mobile-web-app-status-bar-style', 'default'],
         ['apple-mobile-web-app-title', 'Szkielet MS'],
         ['theme-color', '#006089']].forEach(function(m) {
            var meta = tdoc.createElement('meta');
            meta.name = m[0];
            meta.content = m[1];
            tdoc.head.appendChild(meta);
        });
    } catch(e) {}
    
    setInterval(function() {
        docs.forEach(function(d) {
            try {
                [
                    'footer', '#MainMenu',
                    '[data-testid="stToolbar"]', '[data-testid="stDecoration"]',
                    '[data-testid="stStatusWidget"]', '[data-testid="stFooter"]',
                    '[data-testid="stSidebarNav"]', '.stDeployButton',
                    '[data-testid="stActionButton"]', 'header[data-testid="stHeader"]',
                    'a[href*="streamlit.io/cloud"]', 'a[href*="streamlit.io"]'
                ].forEach(function(sel) {
                    d.querySelectorAll(sel).forEach(function(el) {
                        el.style.setProperty('display', 'none', 'important');
                    });
                });
            } catch(e) {}
        });
    }, 3000);
})();
</script>
""").replace('__ICON__', ICON_B64)

st.components.v1.html(hide_html, height=0)
