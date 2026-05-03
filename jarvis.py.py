import streamlit as st
import json
import os
import re
from datetime import datetime, date, timedelta
import plotly.graph_objects as go

st.set_page_config(page_title="JARVIS · Dhruv", page_icon="⚡", layout="wide", initial_sidebar_state="expanded")

CHALLENGE_START = date(2026, 5, 4)
CHALLENGE_DAYS = 56
DATA_FILE = "jarvis_data.json"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=DM+Mono:wght@400;500&family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,700;1,9..144,300;1,9..144,400&display=swap');
html,body,.stApp{background:#141414!important;color:#c8c3bc}
.main{background:#141414!important}
.block-container{padding:2rem 2.5rem 4rem 2.5rem!important;max-width:1300px!important}
#MainMenu,footer,header,.stDeployButton,[data-testid="stToolbar"],.stDecoration{display:none!important;visibility:hidden!important}
*{font-family:'DM Mono',monospace}
h1,h2,h3,h4{font-family:'Fraunces',serif!important;color:#f0ece4!important}
[data-testid="stSidebar"]{background:#0f0f0f!important;border-right:1px solid #1e1e1e!important;min-width:230px!important}
[data-testid="stSidebarContent"]{padding:2rem 1.4rem!important}
.sidebar-title{font-family:'Fraunces',serif;font-size:1.5rem;font-weight:300;color:#f0ece4!important;letter-spacing:-.5px;line-height:1.1;margin-bottom:4px}
.sidebar-sub{font-size:.55rem;letter-spacing:2.5px;color:#2e2e2e!important;margin-bottom:20px}
[data-testid="stSidebar"] .stRadio label{font-size:.65rem!important;letter-spacing:1.5px!important;color:#3a3a3a!important;padding:9px 0!important;cursor:pointer!important;text-transform:uppercase!important;border-bottom:1px solid #161616!important;display:block!important}
[data-testid="stSidebar"] .stRadio label:hover{color:#E63946!important}
[data-testid="stSidebar"] .stRadio{gap:0!important}
[data-testid="stSidebar"] .stRadio div[role="radio"]{display:none!important}
.j-card{background:#1c1c1c;border:1px solid #242424;border-radius:12px;padding:18px 20px;margin-bottom:10px}
.j-card-red{border-left:3px solid #E63946!important}
.j-card-blue{border-left:3px solid #1D7FE8!important}
.j-card-green{border-left:3px solid #22c55e!important}
.j-card-amber{border-left:3px solid #f59e0b!important}
.obt-card{background:#E63946;border-radius:14px;padding:24px 26px;margin:0 0 16px 0;position:relative;overflow:hidden}
.obt-card::after{content:'';position:absolute;right:-40px;top:-40px;width:160px;height:160px;border-radius:50%;background:rgba(255,255,255,.06)}
.obt-label{font-size:.58rem;letter-spacing:2.5px;color:rgba(255,255,255,.6);margin-bottom:10px}
.obt-text{font-family:'Fraunces',serif;font-size:1.8rem;font-weight:300;color:#fff;line-height:1.2}
.sec{font-size:.58rem;letter-spacing:2.5px;color:#323232;text-transform:uppercase;margin:20px 0 10px}
.sec-red{color:#E63946!important}.sec-blue{color:#1D7FE8!important}.sec-green{color:#22c55e!important}.sec-amber{color:#f59e0b!important}
.task-row{display:flex;align-items:center;gap:12px;padding:10px 0;border-bottom:1px solid #202020;font-size:.82rem;color:#aaa}
.task-row:last-child{border-bottom:none}
.task-done{color:#2e2e2e;text-decoration:line-through}
.chk-done{display:inline-flex;width:19px;height:19px;background:#22c55e;border-radius:4px;align-items:center;justify-content:center;font-size:11px;color:#000;font-weight:700;flex-shrink:0}
.chk-open{display:inline-block;width:19px;height:19px;border:2px solid #282828;border-radius:4px;flex-shrink:0}
.alive-row{display:flex;justify-content:space-between;align-items:center;padding:14px 18px;background:#1c1c1c;border:1px solid #242424;border-radius:10px;margin-bottom:8px}
.alive-label{font-size:.85rem;color:#ddd9d2;font-weight:500}
.alive-sub{font-size:.62rem;color:#383838;margin-top:3px;letter-spacing:.5px}
.s-pill{font-size:.55rem;letter-spacing:1.2px;padding:3px 9px;border-radius:4px;font-weight:500;text-transform:uppercase;flex-shrink:0}
.quote{border-left:3px solid #E63946;padding-left:16px;font-family:'Cormorant Garamond',serif;font-style:italic;font-size:1.05rem;color:#484848;line-height:1.65;margin:16px 0}
.stat-card{background:#1c1c1c;border:1px solid #242424;border-radius:12px;padding:16px 18px}
.stat-lbl{font-size:.58rem;letter-spacing:2px;color:#323232;margin-bottom:6px}
.stat-num{font-family:'Fraunces',serif;font-size:2.2rem;font-weight:300;color:#f0ece4;line-height:1}
.prog-wrap{background:#202020;border-radius:99px;height:4px;margin:8px 0 4px}
.prog-fill{border-radius:99px;height:4px;background:linear-gradient(90deg,#E63946,#1D7FE8)}
.win-item{display:flex;gap:10px;align-items:flex-start;padding:9px 0;font-size:.8rem;color:#888;border-bottom:1px solid #202020}
.win-item:last-child{border-bottom:none}
.habit-row{display:flex;justify-content:space-between;align-items:center;padding:12px 0;border-bottom:1px solid #202020}
.habit-row:last-child{border-bottom:none}
.habit-name{font-size:.82rem;color:#aaa}
.h-dots{display:flex;gap:5px}
.h-dot{width:9px;height:9px;border-radius:50%}
.goal-track{background:#1c1c1c;border-radius:10px;padding:14px 16px;margin-bottom:8px}
.goal-track-lbl{font-size:.82rem;color:#c8c3bc;margin-bottom:8px}
.goal-track-sub{font-size:.62rem;color:#323232;margin-top:6px;letter-spacing:1px}
.log-detail{font-size:.75rem;color:#484848;line-height:1.9}
.log-detail span{color:#888}
.blk-lbl{font-size:.58rem;color:#1D7FE8;letter-spacing:1.5px;margin:10px 0 6px}
.stTextArea textarea{background:#1c1c1c!important;border:1px solid #242424!important;border-radius:10px!important;color:#c8c3bc!important;font-family:'DM Mono',monospace!important;font-size:.78rem!important}
.stTextArea textarea:focus{border-color:#E63946!important;box-shadow:none!important}
.stButton button{background:#E63946!important;color:white!important;border:none!important;border-radius:8px!important;font-family:'DM Mono',monospace!important;font-size:.65rem!important;letter-spacing:1.5px!important;width:100%!important;padding:12px!important}
.streamlit-expanderHeader{background:#1c1c1c!important;border:1px solid #242424!important;border-radius:10px!important;color:#c8c3bc!important;font-size:.78rem!important;font-family:'DM Mono',monospace!important}
.streamlit-expanderContent{background:#181818!important;border:1px solid #242424!important;border-top:none!important}
hr{border-color:#1e1e1e!important;margin:20px 0!important}
</style>
""", unsafe_allow_html=True)

# ── DEFAULTS ─────────────────────────────────────────────
DEFAULT_ALIVE = [
    {"icon":"💼","label":"Job applications","sub":"active · target: 3/week","status":"active"},
    {"icon":"🏥","label":"Doctor appointment","sub":"this week · no date set","status":"pending"},
    {"icon":"🏋️","label":"Gym","sub":"goal: 3× per week","status":"flagged"},
    {"icon":"🥦","label":"Groceries","sub":"pending · salt especially","status":"pending"},
    {"icon":"🇩🇪","label":"German study","sub":"B2 goal · targeting daily","status":"flagged"},
]
DEFAULT_HABITS = [
    {"name":"Gym","days":[0,0,0,0,0,0,0]},
    {"name":"Job apps","days":[0,0,0,0,0,0,0]},
    {"name":"Morning dump","days":[0,0,0,0,0,0,0]},
]
ALIVE_ICONS = {"job":("💼","Job applications"),"doctor":("🏥","Doctor appointment"),"gym":("🏋️","Gym"),"groceries":("🥦","Groceries"),"german":("🇩🇪","German study"),"portfolio":("🗂️","Portfolio")}

# ── DATA ─────────────────────────────────────────────────
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE,'r') as f:
            return json.load(f)
    return {
        "chats":[],"alive":DEFAULT_ALIVE,
        "weekly_goals":["Apply to 3 Business Analyst roles in Berlin","Go to gym at least 2×"],
        "week_theme":"Applications",
        "weekly_wins":["Start here — paste your first morning block"],
        "weekly_slipping":[],
        "habits":DEFAULT_HABITS,
        "settings":{"challenge_start":"2026-05-04","name":"Dhruv","week_range":"May 4 — May 10"}
    }

def save_data(d):
    with open(DATA_FILE,'w') as f:
        json.dump(d,f,indent=2)

# ── PARSER — captures ALL dashboard fields ────────────────
def parse_log_block(text):
    result = {}
    lines = text.strip().split('\n')

    # Header — chat num, block num, session type
    m = re.search(r'CHAT\s+(\d+).*?BLOCK\s+([\d.]+).*?(MORNING|EVENING|UPDATE)', text, re.IGNORECASE)
    if m:
        result['chat_num'] = int(m.group(1))
        result['block_num'] = m.group(2)
        result['session_type'] = m.group(3).upper()

    # Simple key:value fields
    field_map = {
        'Date:': 'date',
        'Energy:': 'energy',
        'One Big Thing:': 'obt',
        'Must:': 'must',
        'Should:': 'should',
        'Can:': 'can',
        'Carried forward:': 'carried',
        'Week goal:': 'week_goal',
        'Parked:': 'parked',
        'One line:': 'one_line',
        'Week theme:': 'week_theme',
        'Week range:': 'week_range',
        'Alive updates:': 'alive_updates',
        'Habits:': 'habits_update',
        'Wins:': 'wins_update',
        'Slipping:': 'slipping_update',
        'Proof created today:': 'proof_today',
        'Job metrics:': 'job_metrics',
        'Tomorrow first move:': 'tomorrow_move',
    }
    for line in lines:
        line = line.strip()
        if not line or line.startswith('==='): continue
        for prefix, key in field_map.items():
            if line.startswith(prefix):
                result[key] = line.replace(prefix, '').strip()
                break

    return result

def apply_block_to_data(data, parsed):
    """Apply all parsed fields to the main data store"""

    # Week theme
    if parsed.get('week_theme') and parsed['week_theme'].upper() != 'NONE':
        data['week_theme'] = parsed['week_theme']

    # Week range
    if parsed.get('week_range') and parsed['week_range'].upper() != 'NONE':
        data.setdefault('settings', {})['week_range'] = parsed['week_range']

    # Alive updates — format: "Job apps:active · Doctor:pending · Gym:flagged"
    if parsed.get('alive_updates') and parsed['alive_updates'].upper() != 'NONE':
        updates = [u.strip() for u in parsed['alive_updates'].split('·')]
        for update in updates:
            if ':' in update:
                label_part, status = update.rsplit(':', 1)
                label_part = label_part.strip().lower()
                status = status.strip().lower()
                # Match to existing alive items
                for item in data.get('alive', []):
                    if any(kw in item['label'].lower() for kw in label_part.split()):
                        item['status'] = status
                        break

    # Habits update — format: "Gym:0 · Job apps:1 · Morning dump:1"
    if parsed.get('habits_update') and parsed['habits_update'].upper() != 'NONE':
        updates = [u.strip() for u in parsed['habits_update'].split('·')]
        today_weekday = date.today().weekday()  # 0=Mon, 6=Sun
        for update in updates:
            if ':' in update:
                habit_name, val = update.rsplit(':', 1)
                habit_name = habit_name.strip()
                try:
                    val = int(val.strip())
                    for habit in data.get('habits', []):
                        if habit_name.lower() in habit['name'].lower():
                            # Ensure 7 days exist
                            while len(habit['days']) < 7:
                                habit['days'].append(0)
                            habit['days'][today_weekday] = val
                            break
                except:
                    pass

    # Weekly wins — format: "win1 | win2 | win3"
    if parsed.get('wins_update') and parsed['wins_update'].upper() != 'NONE':
        wins = [w.strip() for w in parsed['wins_update'].split('|') if w.strip()]
        if wins:
            data['weekly_wins'] = wins

    # Weekly slipping — format: "item1 | item2"
    if parsed.get('slipping_update') and parsed['slipping_update'].upper() != 'NONE':
        slipping = [s.strip() for s in parsed['slipping_update'].split('|') if s.strip()]
        if slipping:
            data['weekly_slipping'] = slipping

    return data

def get_challenge_day():
    return max(0, min((date.today() - CHALLENGE_START).days + 1, CHALLENGE_DAYS))

def get_day_color(chat):
    if not chat: return '#1c1c1c'
    must = chat.get('must', '')
    if not must: return '#1D7FE8'
    items = must.split('·')
    done = sum(1 for i in items if '✓' in i)
    total = len(items)
    if total == 0: return '#1c1c1c'
    r = done / total
    return '#22c55e' if r >= 0.8 else '#f59e0b' if r >= 0.5 else '#E63946'

def render_tasks(items_str, color):
    if not items_str or items_str.upper() == 'NONE':
        return '<div style="font-size:.75rem;color:#2a2a2a;padding:8px 0">Nothing here</div>'
    html = ''
    for item in [i.strip() for i in items_str.split('·')]:
        done = '✓' in item
        text = item.replace('✓','').replace('✗','').strip()
        chk = '<span class="chk-done">✓</span>' if done else f'<span class="chk-open" style="border-color:{color}35"></span>'
        html += f'<div class="task-row">{chk}<span class="{"task-done" if done else ""}">{text}</span></div>'
    return html

SC = {
    'active': ('#1D7FE8','#1D7FE810','#1D7FE825'),
    'pending': ('#f59e0b','#f59e0b10','#f59e0b25'),
    'flagged': ('#E63946','#E6394610','#E6394625'),
    'done':    ('#22c55e','#22c55e10','#22c55e25'),
}

# ── LOAD ─────────────────────────────────────────────────
data = load_data()
chats = data.get('chats', [])
latest = chats[-1] if chats else None
challenge_day = get_challenge_day()
days_left = CHALLENGE_DAYS - challenge_day

# ── SIDEBAR ───────────────────────────────────────────────
with st.sidebar:
    name = data.get('settings', {}).get('name', 'Dhruv')
    st.markdown(f'<div class="sidebar-sub">{date.today().strftime("%A · %B %d").upper()}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sidebar-title">JARVIS<br><span style="color:#E63946">{name}</span></div>', unsafe_allow_html=True)
    pct_done = int(challenge_day / CHALLENGE_DAYS * 100)
    st.markdown(f'''
    <div style="margin:16px 0;padding:14px 16px;background:#1a1a1a;border-radius:10px;border:1px solid #1e1e1e">
        <div style="font-size:.55rem;letter-spacing:2px;color:#2a2a2a;margin-bottom:4px">8-WEEK CHALLENGE</div>
        <div style="font-family:Fraunces,serif;font-size:2rem;font-weight:300;color:#E63946;line-height:1">Day {challenge_day}</div>
        <div style="font-size:.55rem;color:#2a2a2a;letter-spacing:1px;margin-top:4px">{days_left} DAYS REMAINING</div>
        <div style="background:#1e1e1e;border-radius:99px;height:3px;margin-top:10px">
            <div style="background:#E63946;border-radius:99px;height:3px;width:{pct_done}%"></div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    page = st.radio('NAV', [
        '⌂  Home', '✓  Tasks', '◎  Whats Alive',
        '↗  Weekly', '▦  Challenge', '📖  Journey Log', '＋  Update',
    ], label_visibility='collapsed')

    cn = chats[-1].get('chat_num', len(chats)) if chats else 0
    st.markdown(f'''
    <div style="margin-top:24px;padding:12px 14px;background:#1a1a1a;border:1px solid #1e1e1e;border-radius:10px;display:flex;justify-content:space-between;align-items:center">
        <div style="font-size:.55rem;color:#2a2a2a;letter-spacing:1.5px">CHAT</div>
        <div style="font-family:Fraunces,serif;font-size:1.4rem;font-weight:300;color:#E63946">{str(cn).zfill(3)}</div>
    </div>
    ''', unsafe_allow_html=True)

# ═══════════════════════════════════════════════
# HOME
# ═══════════════════════════════════════════════
if '⌂' in page:
    c1, c2 = st.columns([3, 2])
    with c1:
        st.markdown(f'<div style="font-size:.58rem;letter-spacing:2.5px;color:#2a2a2a;margin-bottom:8px">{date.today().strftime("%A · %B %d · %Y").upper()}</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="font-family:Fraunces,serif;font-size:2.8rem;font-weight:300;color:#f0ece4;line-height:1;margin-bottom:20px">Hey,<br>{name}.</div>', unsafe_allow_html=True)
        obt = latest.get('obt', 'Start your first morning session') if latest else 'Start your first morning session'
        st.markdown(f'<div class="obt-card"><div class="obt-label">⚡ ONE BIG THING TODAY</div><div class="obt-text">{obt}</div></div>', unsafe_allow_html=True)
        quote = latest.get('one_line', 'Tomorrow is Day 1. Show up.') if latest else 'Tomorrow is Day 1. Show up.'
        st.markdown(f'<div class="quote">"{quote}"</div>', unsafe_allow_html=True)
        if latest:
            st.markdown('<div class="sec sec-red">🔴 MUST DO</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="j-card j-card-red">{render_tasks(latest.get("must",""), "#E63946")}</div>', unsafe_allow_html=True)
        if latest and latest.get('carried','').upper() not in ['','NONE']:
            st.markdown('<div class="sec sec-amber">↩ CARRIED FORWARD</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="j-card j-card-amber"><div style="font-size:.82rem;color:#aaa">{latest.get("carried")}</div></div>', unsafe_allow_html=True)

        # Proof + Tomorrow
        proof = latest.get('proof_today','') if latest else ''
        tomorrow = latest.get('tomorrow_move','') if latest else ''
        if proof and proof.upper() != 'NONE':
            st.markdown('<div class="sec sec-green">✓ PROOF TODAY</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="j-card j-card-green"><div style="font-size:.82rem;color:#aaa">{proof}</div></div>', unsafe_allow_html=True)
        if tomorrow and tomorrow.upper() != 'NONE':
            st.markdown('<div class="sec sec-blue">→ TOMORROW\'S FIRST MOVE</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="j-card j-card-blue"><div style="font-size:.82rem;color:#aaa">{tomorrow}</div></div>', unsafe_allow_html=True)

    with c2:
        done_c = total_c = 0
        if latest:
            for f in ['must','should','can']:
                v = latest.get(f,'')
                if v and v.upper() != 'NONE':
                    items = v.split('·')
                    total_c += len(items)
                    done_c += sum(1 for i in items if '✓' in i)
        wg = latest.get('week_goal','') if latest else ''
        pm = re.search(r'(\d+)/(\d+)', wg)
        wd, wt = (pm.group(1), pm.group(2)) if pm else ('0','3')
        pct = int(done_c/total_c*100) if total_c > 0 else 0

        a, b = st.columns(2)
        with a:
            st.markdown(f'<div class="stat-card"><div class="stat-lbl">TASKS DONE</div><div class="stat-num">{done_c}<span style="font-size:1rem;color:#2a2a2a">/{total_c}</span></div><div class="prog-wrap"><div class="prog-fill" style="width:{pct}%"></div></div></div>', unsafe_allow_html=True)
        with b:
            st.markdown(f'<div class="stat-card"><div class="stat-lbl">WEEK GOAL</div><div class="stat-num" style="color:#1D7FE8">{wd}<span style="font-size:1rem;color:#2a2a2a">/{wt}</span></div><div style="font-size:.6rem;color:#2a2a2a;margin-top:4px;letter-spacing:1px">APPLICATIONS</div></div>', unsafe_allow_html=True)

        st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
        a2, b2 = st.columns(2)
        with a2:
            st.markdown(f'<div class="stat-card"><div class="stat-lbl">SESSIONS</div><div class="stat-num" style="color:#E63946">{len(chats)}</div></div>', unsafe_allow_html=True)
        with b2:
            st.markdown(f'<div class="stat-card"><div class="stat-lbl">DAY</div><div class="stat-num" style="color:#f59e0b">{challenge_day}</div></div>', unsafe_allow_html=True)

        # Energy indicator
        energy = latest.get('energy', 'unknown') if latest else 'unknown'
        energy_color = {'low':'#E63946','medium':'#f59e0b','high':'#22c55e','unknown':'#333'}.get(energy.lower(),'#333')
        energy_bar = {'low':33,'medium':66,'high':100,'unknown':0}.get(energy.lower(),0)
        st.markdown(f'''
        <div class="j-card" style="margin-top:10px">
            <div class="stat-lbl">ENERGY TODAY</div>
            <div style="display:flex;align-items:center;gap:10px;margin-top:6px">
                <div style="font-size:.85rem;color:{energy_color};text-transform:uppercase;letter-spacing:1px">{energy}</div>
                <div style="flex:1;background:#202020;border-radius:99px;height:4px">
                    <div style="background:{energy_color};border-radius:99px;height:4px;width:{energy_bar}%"></div>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

        # Job metrics
        metrics = latest.get('job_metrics','') if latest else ''
        if metrics and metrics.upper() not in ['','NONE','UNKNOWN']:
            st.markdown('<div class="sec">📊 JOB METRICS</div>', unsafe_allow_html=True)
            metric_parts = [m.strip() for m in metrics.split('·')]
            metric_html = ''.join([f'<div style="display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid #202020;font-size:.75rem"><span style="color:#555">{p.split(":")[0].strip() if ":" in p else p}</span><span style="color:#aaa">{p.split(":")[1].strip() if ":" in p else "—"}</span></div>' for p in metric_parts if p])
            st.markdown(f'<div class="j-card">{metric_html}</div>', unsafe_allow_html=True)

        st.markdown('<div class="sec">◎ OPEN LOOPS</div>', unsafe_allow_html=True)
        for item in data.get('alive', [])[:4]:
            sc, sbg, sborder = SC.get(item['status'], ('#666','#66610','#66625'))
            st.markdown(f'<div class="alive-row" style="border-left:3px solid {sc}"><div style="display:flex;gap:10px;align-items:center"><span style="font-size:1.1rem">{item["icon"]}</span><div><div class="alive-label" style="font-size:.8rem">{item["label"]}</div><div class="alive-sub">{item["sub"]}</div></div></div><span class="s-pill" style="background:{sbg};color:{sc};border:1px solid {sborder}">{item["status"].upper()}</span></div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════
# TASKS
# ═══════════════════════════════════════════════
elif '✓' in page:
    st.markdown('<div style="font-family:Fraunces,serif;font-size:2rem;font-weight:300;color:#f0ece4;margin-bottom:4px">Today\'s Tasks</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size:.58rem;letter-spacing:2px;color:#2a2a2a;margin-bottom:20px">{date.today().strftime("%A · %B %d").upper()}</div>', unsafe_allow_html=True)

    if not latest:
        st.markdown('<div class="j-card" style="text-align:center;padding:50px"><div style="font-family:Fraunces,serif;font-size:1.3rem;color:#1e1e1e">No tasks yet — paste your morning block first</div></div>', unsafe_allow_html=True)
    else:
        done_c = total_c = 0
        for f in ['must','should','can']:
            v = latest.get(f,'')
            if v and v.upper() != 'NONE':
                items = v.split('·')
                total_c += len(items)
                done_c += sum(1 for i in items if '✓' in i)
        pct = int(done_c/total_c*100) if total_c > 0 else 0
        st.markdown(f'<div style="font-size:.65rem;color:#2a2a2a;letter-spacing:1px;margin-bottom:6px">{done_c} OF {total_c} DONE · {pct}%</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="prog-wrap"><div class="prog-fill" style="width:{pct}%"></div></div>', unsafe_allow_html=True)
        st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            if latest.get('must'):
                st.markdown('<div class="sec sec-red">🔴 MUST DO</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="j-card j-card-red">{render_tasks(latest.get("must",""), "#E63946")}</div>', unsafe_allow_html=True)
            if latest.get('can'):
                st.markdown('<div class="sec sec-green">🟢 CAN DO</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="j-card j-card-green">{render_tasks(latest.get("can",""), "#22c55e")}</div>', unsafe_allow_html=True)
        with c2:
            if latest.get('should'):
                st.markdown('<div class="sec sec-blue">🔵 SHOULD DO</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="j-card j-card-blue">{render_tasks(latest.get("should",""), "#1D7FE8")}</div>', unsafe_allow_html=True)
            if latest.get('carried','').upper() not in ['','NONE']:
                st.markdown('<div class="sec sec-amber">↩ CARRIED FORWARD</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="j-card j-card-amber"><div style="font-size:.82rem;color:#aaa">{latest.get("carried")}</div></div>', unsafe_allow_html=True)
            if latest.get('parked','').upper() not in ['','NONE']:
                st.markdown('<div class="sec">🅿 PARKED</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="j-card"><div style="font-size:.82rem;color:#aaa">{latest.get("parked")}</div></div>', unsafe_allow_html=True)

        st.markdown('<hr>', unsafe_allow_html=True)
        st.markdown('<div class="j-card j-card-amber"><div style="font-size:.58rem;color:#f59e0b;letter-spacing:2px;margin-bottom:8px">🌙 EVENING CHECK-IN</div><div style="font-size:.8rem;color:#555;line-height:1.7">Finish your Claude chat. Type FINISH. Paste the block in the Update section.</div></div>', unsafe_allow_html=True)

        proof = latest.get('proof_today','')
        tomorrow = latest.get('tomorrow_move','')
        if proof and proof.upper() != 'NONE':
            st.markdown('<div class="sec sec-green">✓ PROOF CREATED TODAY</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="j-card j-card-green"><div style="font-size:.82rem;color:#aaa">{proof}</div></div>', unsafe_allow_html=True)
        if tomorrow and tomorrow.upper() != 'NONE':
            st.markdown('<div class="sec sec-blue">→ TOMORROW\'S FIRST MOVE</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="j-card j-card-blue"><div style="font-size:.82rem;color:#aaa">{tomorrow}</div></div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════
# WHAT'S ALIVE
# ═══════════════════════════════════════════════
elif 'Alive' in page or '◎' in page:
    st.markdown('<div style="font-family:Fraunces,serif;font-size:2rem;font-weight:300;color:#f0ece4;margin-bottom:4px">What\'s Alive</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:.58rem;letter-spacing:2px;color:#2a2a2a;margin-bottom:20px">EVERYTHING OPEN IN YOUR LIFE RIGHT NOW</div>', unsafe_allow_html=True)
    for item in data.get('alive', []):
        sc, sbg, sborder = SC.get(item['status'], ('#666','#66610','#66625'))
        st.markdown(f'<div class="alive-row" style="border-left:4px solid {sc}"><div style="display:flex;gap:14px;align-items:center"><span style="font-size:1.5rem">{item["icon"]}</span><div><div class="alive-label">{item["label"]}</div><div class="alive-sub">{item["sub"]}</div></div></div><span class="s-pill" style="background:{sbg};color:{sc};border:1px solid {sborder}">{item["status"].upper()}</span></div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════
# WEEKLY
# ═══════════════════════════════════════════════
elif '↗' in page:
    wr = data.get('settings', {}).get('week_range', 'May 4 — May 10')
    st.markdown(f'<div style="font-family:Fraunces,serif;font-size:2rem;font-weight:300;color:#f0ece4;margin-bottom:4px">This Week</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size:.58rem;letter-spacing:2px;color:#2a2a2a;margin-bottom:20px">{wr.upper()} · 2026</div>', unsafe_allow_html=True)

    c1, c2 = st.columns([1, 2])
    with c1:
        theme = data.get('week_theme', 'Applications')
        st.markdown(f'<div class="j-card" style="text-align:center;padding:24px;border-color:#E6394620"><div style="font-size:.58rem;letter-spacing:2.5px;color:#E63946;margin-bottom:10px">FOCUS THEME</div><div style="font-family:Fraunces,serif;font-size:3rem;font-weight:300;color:#f0ece4;line-height:1">{theme}</div></div>', unsafe_allow_html=True)

        st.markdown('<div class="sec sec-green">🏆 WINS</div>', unsafe_allow_html=True)
        wins = ''.join([f'<div class="win-item"><span style="color:#22c55e">✓</span>{w}</div>' for w in data.get('weekly_wins',[])])
        st.markdown(f'<div class="j-card j-card-green">{wins if wins else "<div style=\'font-size:.75rem;color:#2a2a2a;padding:8px 0\'>No wins logged yet</div>"}</div>', unsafe_allow_html=True)

        slipping = data.get('weekly_slipping', [])
        if slipping:
            st.markdown('<div class="sec sec-red">↩ SLIPPING</div>', unsafe_allow_html=True)
            slip = ''.join([f'<div class="win-item"><span style="color:#E63946">↩</span>{w}</div>' for w in slipping])
            st.markdown(f'<div class="j-card j-card-red">{slip}</div>', unsafe_allow_html=True)

        # Weekly job metrics from latest block
        if latest and latest.get('job_metrics','').upper() not in ['','NONE','UNKNOWN']:
            st.markdown('<div class="sec">📊 JOB METRICS THIS WEEK</div>', unsafe_allow_html=True)
            metric_parts = [m.strip() for m in latest.get('job_metrics','').split('·')]
            metric_html = ''.join([f'<div style="display:flex;justify-content:space-between;padding:7px 0;border-bottom:1px solid #202020;font-size:.78rem"><span style="color:#555">{p.split(":")[0].strip() if ":" in p else p}</span><span style="color:#aaa;font-weight:700">{p.split(":")[1].strip() if ":" in p else "—"}</span></div>' for p in metric_parts if p])
            st.markdown(f'<div class="j-card">{metric_html}</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="sec">WEEKLY GOALS</div>', unsafe_allow_html=True)
        wg = latest.get('week_goal','') if latest else ''
        pm = re.search(r'(\d+)/(\d+)', wg)
        wd, wt = (int(pm.group(1)), int(pm.group(2))) if pm else (0, 3)
        for i, goal in enumerate(data.get('weekly_goals',[])):
            p = wd/wt if i == 0 and wt > 0 else 0
            st.markdown(f'<div class="goal-track"><div class="goal-track-lbl">{goal}</div><div class="prog-wrap"><div class="prog-fill" style="width:{int(p*100)}%"></div></div><div class="goal-track-sub">{wd if i==0 else 0} OF {wt if i==0 else 2} · {days_left} DAYS LEFT</div></div>', unsafe_allow_html=True)

        st.markdown('<div class="sec">DAILY SNAPSHOT</div>', unsafe_allow_html=True)
        day_map = {}
        for chat in chats:
            try:
                d = datetime.strptime(chat.get('date',''), '%A, %B %d %Y').date()
                day_map[d] = chat
            except: pass
        week_start = date.today() - timedelta(days=date.today().weekday())
        dots = ''.join([f'<div style="text-align:center"><div style="font-size:.55rem;color:#2a2a2a;margin-bottom:6px">{["M","T","W","T","F","S","S"][i]}</div><div style="width:12px;height:12px;border-radius:50%;background:{get_day_color(day_map.get(week_start+timedelta(days=i)))};margin:0 auto"></div></div>' for i in range(7)])
        st.markdown(f'<div class="j-card"><div style="display:grid;grid-template-columns:repeat(7,1fr);gap:8px">{dots}</div></div>', unsafe_allow_html=True)

        st.markdown('<div class="sec">HABITS</div>', unsafe_allow_html=True)
        habit_rows = []
        for h in data.get('habits', []):
            dot_html = ''.join([f'<div class="h-dot" style="background:{"#22c55e" if d else "#202020"}"></div>' for d in h["days"]])
            habit_rows.append(f'<div class="habit-row"><div class="habit-name">{h["name"]}</div><div class="h-dots">{dot_html}</div></div>')
        st.markdown(f'<div class="j-card">{"".join(habit_rows)}</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════
# CHALLENGE
# ═══════════════════════════════════════════════
elif '▦' in page:
    st.markdown('<div style="font-family:Fraunces,serif;font-size:2rem;font-weight:300;color:#f0ece4;margin-bottom:4px">8-Week Challenge</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:.58rem;letter-spacing:2px;color:#2a2a2a;margin-bottom:20px">MAY 4 — JUN 28 · 2026 · 56 DAYS</div>', unsafe_allow_html=True)

    a, b, c, d2 = st.columns(4)
    for col, lbl, val, color in [(a,'CURRENT DAY',challenge_day,'#E63946'),(b,'DAYS LEFT',days_left,'#1D7FE8'),(c,'SESSIONS',len(chats),'#22c55e'),(d2,'COMPLETE',f'{int(challenge_day/CHALLENGE_DAYS*100)}%','#f59e0b')]:
        with col:
            st.markdown(f'<div class="stat-card"><div class="stat-lbl">{lbl}</div><div class="stat-num" style="color:{color}">{val}</div></div>', unsafe_allow_html=True)

    st.markdown('<div style="height:16px"></div>', unsafe_allow_html=True)

    day_map = {}
    for chat in chats:
        try:
            d3 = datetime.strptime(chat.get('date',''), '%A, %B %d %Y').date()
            day_map[d3] = chat
        except: pass

    grid = '<div style="display:grid;grid-template-columns:repeat(8,1fr);gap:6px;margin-bottom:8px">'
    for w in range(1, 9):
        grid += f'<div style="font-size:.52rem;color:#252525;letter-spacing:1px;text-align:center;padding-bottom:6px">WK{w}</div>'
    for dn in range(1, CHALLENGE_DAYS + 1):
        dd = CHALLENGE_START + timedelta(days=dn-1)
        is_today = dd == date.today()
        is_future = dd > date.today()
        cd = day_map.get(dd)
        if is_future:   bg,border,op = '#161616','1px solid #1e1e1e','0.3'
        elif is_today:  bg,border,op = '#1D7FE8','2px solid #1D7FE8','1'
        elif cd:        bg,border,op = get_day_color(cd),'none','1'
        else:           bg,border,op = '#1e1212','1px solid #241818','0.8'
        grid += f'<div title="Day {dn} · {dd.strftime("%b %d")}" style="aspect-ratio:1;background:{bg};border:{border};border-radius:5px;opacity:{op}"></div>'
    grid += '</div>'
    legend = ''.join([f'<div style="display:flex;align-items:center;gap:5px"><div style="width:8px;height:8px;background:{c};border-radius:2px"></div><span style="font-size:.55rem;color:#2a2a2a;letter-spacing:1px">{l}</span></div>' for c,l in [('#22c55e','STRONG'),('#f59e0b','PARTIAL'),('#E63946','MISSED'),('#1D7FE8','TODAY'),('#161616','AHEAD')]])
    st.markdown(f'<div class="j-card">{grid}<div style="display:flex;gap:20px;margin-top:8px">{legend}</div></div>', unsafe_allow_html=True)

    if len(chats) > 0:
        st.markdown('<div class="sec">COMPLETION OVER TIME</div>', unsafe_allow_html=True)
        xs, ys = [], []
        for chat in chats:
            try:
                d4 = datetime.strptime(chat.get('date',''), '%A, %B %d %Y').date()
                dn = (d4 - CHALLENGE_START).days + 1
                must = chat.get('must','')
                if must and must.upper() != 'NONE':
                    items = must.split('·')
                    done = sum(1 for i in items if '✓' in i)
                    total = len(items)
                    if total > 0:
                        xs.append(dn)
                        ys.append(int(done/total*100))
            except: pass
        if xs:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=xs, y=ys, mode='lines+markers', line=dict(color='#E63946',width=2), marker=dict(color='#E63946',size=6), fill='tozeroy', fillcolor='rgba(230,57,70,0.05)'))
            fig.update_layout(height=180, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=0,r=0,t=0,b=0), xaxis=dict(showgrid=False,color='#2a2a2a',title='Day',tickfont=dict(size=9,color='#2a2a2a')), yaxis=dict(showgrid=True,gridcolor='#1e1e1e',color='#2a2a2a',title='% Done',tickfont=dict(size=9,color='#2a2a2a'),range=[0,110]), showlegend=False)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar':False})

# ═══════════════════════════════════════════════
# JOURNEY LOG
# ═══════════════════════════════════════════════
elif '📖' in page:
    st.markdown('<div style="font-family:Fraunces,serif;font-size:2rem;font-weight:300;color:#f0ece4;margin-bottom:4px">Journey Log</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size:.58rem;letter-spacing:2px;color:#2a2a2a;margin-bottom:20px">{len(chats)} SESSIONS · YOUR COMPLETE RECORD</div>', unsafe_allow_html=True)

    if not chats:
        st.markdown('<div class="j-card" style="text-align:center;padding:60px"><div style="font-family:Fraunces,serif;font-size:1.5rem;color:#1e1e1e;font-style:italic">Your story starts tomorrow.</div><div style="font-size:.6rem;color:#1a1a1a;margin-top:10px;letter-spacing:1.5px">CHAT 001 · DAY 1 · MAY 4 2026</div></div>', unsafe_allow_html=True)
    else:
        for chat in reversed(chats):
            cn2 = str(chat.get('chat_num','?')).zfill(3)
            cd2 = chat.get('date','Unknown date')
            cs = chat.get('one_line','')
            with st.expander(f"Chat {cn2}  ·  {cd2}", expanded=False):
                st.markdown(f'<div style="font-family:Cormorant Garamond,serif;font-style:italic;font-size:.95rem;color:#444;margin-bottom:12px">"{cs}"</div>', unsafe_allow_html=True)
                energy_c = {'low':'#E63946','medium':'#f59e0b','high':'#22c55e','unknown':'#333'}.get(chat.get('energy','unknown').lower(),'#333')
                st.markdown(f'<div class="log-detail"><b style="color:#555">Energy:</b> <span style="color:{energy_c}">{chat.get("energy","—")}</span><br><b style="color:#555">OBT:</b> <span>{chat.get("obt","—")}</span><br><b style="color:#555">Must:</b> <span>{chat.get("must","—")}</span><br><b style="color:#555">Should:</b> <span>{chat.get("should","—")}</span><br><b style="color:#555">Can:</b> <span>{chat.get("can","—")}</span><br><b style="color:#555">Carried:</b> <span>{chat.get("carried","NONE")}</span><br><b style="color:#555">Week:</b> <span>{chat.get("week_goal","—")}</span><br><b style="color:#555">Proof:</b> <span>{chat.get("proof_today","NONE")}</span><br><b style="color:#555">Job metrics:</b> <span>{chat.get("job_metrics","—")}</span><br><b style="color:#555">Tomorrow:</b> <span>{chat.get("tomorrow_move","—")}</span><br><b style="color:#555">Parked:</b> <span>{chat.get("parked","NONE")}</span></div>', unsafe_allow_html=True)
                for block in chat.get('blocks',[]):
                    bn = block.get('block_num','')
                    bt = block.get('session_type','')
                    bd = block.get('data',{})
                    if bn:
                        st.markdown(f'<div style="margin-top:12px;padding-top:12px;border-top:1px solid #1e1e1e"><div class="blk-lbl">BLOCK {bn} · {bt}</div><div class="log-detail">OBT: <span>{bd.get("obt","—")}</span><br>Must: <span>{bd.get("must","—")}</span><br>Carried: <span>{bd.get("carried","NONE")}</span></div></div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════
# UPDATE
# ═══════════════════════════════════════════════
elif '＋' in page:
    st.markdown('<div style="font-family:Fraunces,serif;font-size:2rem;font-weight:300;color:#f0ece4;margin-bottom:4px">Update Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:.58rem;letter-spacing:2px;color:#2a2a2a;margin-bottom:20px">PASTE YOUR LOG BLOCK FROM CLAUDE · ONE PASTE UPDATES EVERYTHING</div>', unsafe_allow_html=True)

    c1, c2 = st.columns([2, 1])
    with c1:
        log_input = st.text_area('', height=340,
            placeholder="""=== CHAT 002 · BLOCK 2.0 · MORNING ===
Date: Monday, May 4 2026
Energy: medium
One Big Thing: Apply to Capgemini Invent ✗
Must: Apply to 1 job ✗ · Breakfast ✓ · Work ✓
Should: Buy groceries ✗ · Doctor appointment ✗
Can: Gym ✗
Carried forward: Gym · Doctor appointment
Week goal: Apply to 3 BA roles → 0/3 done
Parked: NONE
One line: Day 1. Showed up.
Week theme: Applications
Week range: May 4 — May 10
Alive updates: Job apps:active · Doctor:pending · Gym:flagged
Habits: Gym:0 · Job apps:0 · Morning dump:1
Wins: First morning dump done
Slipping: NONE
Proof created today: NONE
Job metrics: Applications:0 · CVs tailored:0 · Recruiters:0 · Follow-ups:0 · Interviews:0
Tomorrow first move: Open Capgemini post and tailor first 3 CV bullets
=== END BLOCK ===""",
            label_visibility='collapsed'
        )
        if st.button('UPDATE DASHBOARD →'):
            if log_input.strip():
                parsed = parse_log_block(log_input)
                if parsed and 'obt' in parsed:
                    parsed['logged_at'] = datetime.now().isoformat()
                    parsed['raw'] = log_input

                    # Apply all the new fields to global data
                    data = apply_block_to_data(data, parsed)

                    # Add/update chat entry
                    cn3 = parsed.get('chat_num', len(chats) + 1)
                    idx = next((i for i, c in enumerate(chats) if c.get('chat_num') == cn3), None)
                    # Clean copy for storing inside blocks — avoids circular reference
                    clean = {k: v for k, v in parsed.items() if k != 'blocks'}

                    if idx is not None:
                        chats[idx].update(clean)
                        if 'blocks' not in chats[idx]: chats[idx]['blocks'] = []
                        chats[idx]['blocks'].append({'block_num': clean.get('block_num',''), 'session_type': clean.get('session_type',''), 'data': clean})
                    else:
                        clean['blocks'] = [{'block_num': clean.get('block_num','1.0'), 'session_type': clean.get('session_type','MORNING'), 'data': clean}]
                        chats.append(clean)

                    data['chats'] = chats
                    save_data(data)
                    st.success('✓ All sections updated — tasks, alive, weekly, habits, challenge tracker, log')
                    st.rerun()
                else:
                    st.error('Could not parse — check format matches the template on the right.')
            else:
                st.warning('Paste a log block first.')

    with c2:
        st.markdown('''
        <div class="j-card" style="border-color:#1D7FE820">
            <div style="font-size:.58rem;color:#1D7FE8;letter-spacing:2px;margin-bottom:12px">HOW IT WORKS</div>
            <div style="font-size:.75rem;color:#444;line-height:1.9">
                1. End your Claude chat<br>
                2. Type <span style="color:#E63946">FINISH</span><br>
                3. Copy the block Claude generates<br>
                4. Paste it here<br>
                5. Hit update<br><br>
                <span style="color:#282828">Every section updates from one paste — tasks, alive, weekly, habits, challenge tracker, log.</span>
            </div>
        </div>
        ''', unsafe_allow_html=True)

        st.markdown('''
        <div class="j-card j-card-amber" style="margin-top:10px">
            <div style="font-size:.58rem;color:#f59e0b;letter-spacing:2px;margin-bottom:10px">FULL BLOCK FORMAT v6</div>
            <div style="font-size:.62rem;color:#3a3a3a;line-height:2;font-family:monospace">
                === CHAT [N] · BLOCK [X.Y] ===<br>
                Date: Weekday, Mon DD YYYY<br>
                Energy: low/medium/high<br>
                One Big Thing: ... ✓/✗<br>
                Must: item ✓ · item ✗<br>
                Should: item ✓ · item ✗<br>
                Can: item ✗<br>
                Carried forward: ...<br>
                Week goal: goal → X/Y done<br>
                Parked: ...<br>
                One line: ...<br>
                <span style="color:#555">Week theme: word</span><br>
                <span style="color:#555">Week range: May 4 — May 10</span><br>
                <span style="color:#555">Alive updates: Job apps:active</span><br>
                <span style="color:#555">Habits: Gym:0 · Job apps:1 · Morning dump:1</span><br>
                <span style="color:#555">Wins: win1 | win2</span><br>
                <span style="color:#555">Slipping: item1 | item2</span><br>
                <span style="color:#1D7FE8">Proof created today: ...</span><br>
                <span style="color:#1D7FE8">Job metrics: Apps:X · CVs:X · ...</span><br>
                <span style="color:#1D7FE8">Tomorrow first move: ...</span><br>
                === END BLOCK ===
            </div>
        </div>
        ''', unsafe_allow_html=True)
