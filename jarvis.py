import streamlit as st
import json
import os
import re
from datetime import datetime, date, timedelta
import plotly.graph_objects as go
import plotly.express as px

# ── PAGE CONFIG ──────────────────────────────────────────
st.set_page_config(
    page_title="JARVIS · Dhruv",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── CONSTANTS ────────────────────────────────────────────
CHALLENGE_START = date(2026, 5, 4)
CHALLENGE_DAYS = 56
DATA_FILE = "jarvis_data.json"

# ── STYLES ───────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400;1,600&family=DM+Mono:wght@400;500&family=Fraunces:ital,wght@0,300;0,400;0,700;1,300;1,400&display=swap');

* { font-family: 'DM Mono', monospace; }

.main { background: #0c0c0c; }
.stApp { background: #0c0c0c; }

/* Hide streamlit defaults */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
[data-testid="stToolbar"] { display: none; }
.stDecoration { display: none; }

/* Main container */
.block-container {
    padding: 2rem 2rem 4rem 2rem !important;
    max-width: 1400px !important;
}

/* Typography */
h1, h2, h3 { font-family: 'Fraunces', serif !important; }

.jarvis-title {
    font-family: 'Fraunces', serif;
    font-size: 3.5rem;
    font-weight: 300;
    color: #f0ece4;
    letter-spacing: -1px;
    line-height: 1;
}

.jarvis-sub {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 3px;
    color: #444;
    text-transform: uppercase;
    margin-top: 4px;
}

/* Chat number */
.chat-badge {
    font-family: 'Fraunces', serif;
    font-size: 2.5rem;
    font-weight: 700;
    color: #E63946;
    line-height: 1;
}

/* Cards */
.j-card {
    background: #111;
    border: 1px solid #1e1e1e;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 12px;
}

.j-card-red { border-left: 3px solid #E63946; }
.j-card-blue { border-left: 3px solid #1D7FE8; }
.j-card-green { border-left: 3px solid #22c55e; }
.j-card-amber { border-left: 3px solid #f59e0b; }

/* Section labels */
.sec-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 2.5px;
    color: #444;
    text-transform: uppercase;
    margin-bottom: 10px;
    margin-top: 24px;
}

.sec-label-red { color: #E63946 !important; }
.sec-label-blue { color: #1D7FE8 !important; }
.sec-label-green { color: #22c55e !important; }
.sec-label-amber { color: #f59e0b !important; }

/* OBT card */
.obt-card {
    background: #E63946;
    border-radius: 14px;
    padding: 22px 24px;
    margin: 16px 0;
    position: relative;
    overflow: hidden;
}

.obt-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 2.5px;
    color: rgba(255,255,255,0.65);
    margin-bottom: 8px;
}

.obt-text {
    font-family: 'Fraunces', serif;
    font-size: 1.6rem;
    font-weight: 400;
    color: #fff;
    line-height: 1.2;
}

.obt-reminder {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    color: rgba(255,255,255,0.55);
    margin-top: 10px;
    letter-spacing: 1px;
}

/* Task items */
.task-row {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 0;
    border-bottom: 1px solid #1a1a1a;
    font-size: 0.85rem;
    color: #ccc;
}

.task-row:last-child { border-bottom: none; }

.task-done {
    color: #444;
    text-decoration: line-through;
}

.check-done {
    display: inline-block;
    width: 18px; height: 18px;
    background: #22c55e;
    border-radius: 4px;
    text-align: center;
    line-height: 18px;
    font-size: 11px;
    flex-shrink: 0;
}

.check-open {
    display: inline-block;
    width: 18px; height: 18px;
    border: 2px solid #333;
    border-radius: 4px;
    flex-shrink: 0;
}

/* Alive items */
.alive-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 14px 16px;
    background: #111;
    border: 1px solid #1e1e1e;
    border-radius: 10px;
    margin-bottom: 8px;
}

.status-pill {
    font-family: 'DM Mono', monospace;
    font-size: 0.55rem;
    letter-spacing: 1.2px;
    padding: 3px 9px;
    border-radius: 4px;
    font-weight: 500;
    text-transform: uppercase;
}

/* Quote */
.daily-quote {
    border-left: 3px solid #E63946;
    padding-left: 16px;
    font-family: 'Cormorant Garamond', serif;
    font-style: italic;
    font-size: 1.1rem;
    color: #555;
    line-height: 1.6;
    margin: 16px 0;
}

/* Log cards */
.log-card {
    background: #0f0f0f;
    border: 1px solid #1e1e1e;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 10px;
}

.log-chat-num {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    color: #E63946;
    letter-spacing: 2px;
    margin-bottom: 4px;
}

.log-date {
    font-family: 'Fraunces', serif;
    font-size: 1rem;
    color: #f0ece4;
}

.log-summary {
    font-size: 0.75rem;
    color: #444;
    margin-top: 4px;
}

.log-block-label {
    font-size: 0.6rem;
    color: #1D7FE8;
    letter-spacing: 1.5px;
    margin: 10px 0 6px;
}

.log-detail {
    font-size: 0.75rem;
    color: #666;
    line-height: 1.8;
}

.log-detail span { color: #aaa; }

/* Stat cards */
.stat-num {
    font-family: 'Fraunces', serif;
    font-size: 2.2rem;
    font-weight: 300;
    color: #f0ece4;
    line-height: 1;
}

.stat-label-sm {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 2px;
    color: #444;
    margin-bottom: 6px;
}

/* Day tracker grid */
.day-grid {
    display: grid;
    grid-template-columns: repeat(8, 1fr);
    gap: 6px;
    margin-top: 12px;
}

.day-cell {
    aspect-ratio: 1;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.55rem;
    font-family: 'DM Mono', monospace;
    cursor: default;
}

/* Input area */
.stTextArea textarea {
    background: #111 !important;
    border: 1px solid #222 !important;
    border-radius: 10px !important;
    color: #f0ece4 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.8rem !important;
}

.stButton button {
    background: #E63946 !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 1.5px !important;
    padding: 10px 20px !important;
    width: 100% !important;
}

/* Divider */
hr { border-color: #1e1e1e !important; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0a0a0a !important;
    border-right: 1px solid #1e1e1e !important;
}
</style>
""", unsafe_allow_html=True)

# ── DATA MANAGEMENT ──────────────────────────────────────
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {
        "chats": [],
        "alive": [
            {"icon": "💼", "label": "Job applications", "sub": "active · target: 3/week", "status": "active"},
            {"icon": "🏥", "label": "Doctor appointment", "sub": "this week · no date set", "status": "pending"},
            {"icon": "🏋️", "label": "Gym", "sub": "goal: 3× per week", "status": "flagged"},
            {"icon": "🥦", "label": "Groceries", "sub": "pending · salt especially", "status": "pending"},
            {"icon": "🇩🇪", "label": "German study", "sub": "B2 goal · targeting daily", "status": "flagged"},
        ],
        "weekly_goals": ["Apply to 3 Business Analyst roles in Berlin"],
        "week_theme": "Applications",
        "settings": {
            "challenge_start": str(CHALLENGE_START),
            "name": "Dhruv"
        }
    }

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def parse_log_block(text):
    """Parse the log block generated by Claude into structured data"""
    result = {}
    lines = text.strip().split('\n')

    for line in lines:
        line = line.strip()
        if not line or line.startswith('==='):
            continue

        if line.startswith('Date:'):
            result['date'] = line.replace('Date:', '').strip()
        elif line.startswith('One Big Thing:'):
            result['obt'] = line.replace('One Big Thing:', '').strip()
        elif line.startswith('Must:'):
            result['must'] = line.replace('Must:', '').strip()
        elif line.startswith('Should:'):
            result['should'] = line.replace('Should:', '').strip()
        elif line.startswith('Can:'):
            result['can'] = line.replace('Can:', '').strip()
        elif line.startswith('Carried forward:'):
            result['carried'] = line.replace('Carried forward:', '').strip()
        elif line.startswith('Week goal:'):
            result['week_goal'] = line.replace('Week goal:', '').strip()
        elif line.startswith('Parked:'):
            result['parked'] = line.replace('Parked:', '').strip()
        elif line.startswith('One line:'):
            result['one_line'] = line.replace('One line:', '').strip()

    # Extract chat and block numbers from header
    header_match = re.search(r'CHAT\s+(\d+).*BLOCK\s+([\d.]+).*?(MORNING|EVENING|UPDATE)', text, re.IGNORECASE)
    if header_match:
        result['chat_num'] = int(header_match.group(1))
        result['block_num'] = header_match.group(2)
        result['session_type'] = header_match.group(3).upper()

    return result

def get_challenge_day():
    today = date.today()
    delta = (today - CHALLENGE_START).days + 1
    return max(0, min(delta, CHALLENGE_DAYS))

def get_day_color(day_data):
    if not day_data:
        return '#1a1a1a'
    # Based on completion
    if 'must' in day_data:
        must_items = day_data['must'].split('·')
        done = sum(1 for i in must_items if '✓' in i)
        total = len(must_items)
        if total == 0:
            return '#1a1a1a'
        ratio = done / total
        if ratio >= 0.8:
            return '#22c55e'
        elif ratio >= 0.5:
            return '#f59e0b'
        else:
            return '#E63946'
    return '#1D7FE8'

# ── LOAD DATA ─────────────────────────────────────────────
data = load_data()
chats = data.get('chats', [])
latest = chats[-1] if chats else None

# ── HEADER ───────────────────────────────────────────────
col_title, col_chat, col_date = st.columns([3, 1, 2])

with col_title:
    name = data.get('settings', {}).get('name', 'Dhruv')
    today_str = date.today().strftime('%A · %b %d · %Y').upper()
    st.markdown(f'<div class="jarvis-sub">{today_str}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="jarvis-title">Hey,<br>{name}.</div>', unsafe_allow_html=True)

with col_chat:
    chat_num = len(chats) + 1 if not chats else chats[-1].get('chat_num', len(chats))
    st.markdown(f'<div class="jarvis-sub">CHAT</div><div class="chat-badge">{str(chat_num).zfill(3)}</div>', unsafe_allow_html=True)

with col_date:
    challenge_day = get_challenge_day()
    days_left = CHALLENGE_DAYS - challenge_day
    st.markdown(f'''
    <div style="text-align:right;padding-top:8px">
        <div class="jarvis-sub">8-WEEK CHALLENGE</div>
        <div style="font-family:'Fraunces',serif;font-size:2rem;font-weight:300;color:#f0ece4;line-height:1">
            Day {challenge_day}<span style="font-size:1rem;color:#444">/{CHALLENGE_DAYS}</span>
        </div>
        <div class="jarvis-sub" style="margin-top:4px">{days_left} DAYS REMAINING</div>
    </div>
    ''', unsafe_allow_html=True)

st.markdown('<hr>', unsafe_allow_html=True)

# ── MAIN LAYOUT ───────────────────────────────────────────
left, mid, right = st.columns([2, 2, 1.5])

# ════════════════════════════════════════
# LEFT COLUMN — Today + Tasks
# ════════════════════════════════════════
with left:

    # OBT
    obt = latest.get('obt', 'No plan yet — paste your morning block') if latest else 'Start your first morning session'
    reminder = ''
    if latest and 'must' in latest:
        # Try to extract time from obt
        time_match = re.search(r'\d{1,2}[:\-]\d{2}|\d{1,2}\s*[AP]M', obt, re.IGNORECASE)
        if time_match:
            reminder = f'⏰ REMINDER · {time_match.group()}'

    st.markdown(f'''
    <div class="obt-card">
        <div class="obt-label">⚡ ONE BIG THING TODAY</div>
        <div class="obt-text">{obt}</div>
        {'<div class="obt-reminder">' + reminder + '</div>' if reminder else ''}
    </div>
    ''', unsafe_allow_html=True)

    # Daily quote
    quote = latest.get('one_line', 'Your story starts tomorrow.') if latest else 'Your story starts tomorrow.'
    st.markdown(f'<div class="daily-quote">"{quote}"</div>', unsafe_allow_html=True)

    # Tasks
    if latest:
        def render_tasks(items_str, color):
            if not items_str or items_str == 'NONE':
                return ''
            items = [i.strip() for i in items_str.split('·')]
            html = ''
            for item in items:
                done = '✓' in item
                text = item.replace('✓', '').replace('✗', '').strip()
                check = '<span class="check-done">✓</span>' if done else f'<span class="check-open" style="border-color:{color}"></span>'
                cls = 'task-done' if done else ''
                html += f'<div class="task-row">{check}<span class="{cls}">{text}</span></div>'
            return html

        st.markdown('<div class="sec-label sec-label-red">🔴 MUST DO</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="j-card j-card-red">{render_tasks(latest.get("must",""), "#E63946")}</div>', unsafe_allow_html=True)

        if latest.get('should') and latest.get('should') != 'NONE':
            st.markdown('<div class="sec-label sec-label-blue">🔵 SHOULD DO</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="j-card j-card-blue">{render_tasks(latest.get("should",""), "#1D7FE8")}</div>', unsafe_allow_html=True)

        if latest.get('can') and latest.get('can') != 'NONE':
            st.markdown('<div class="sec-label sec-label-green">🟢 CAN DO</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="j-card j-card-green">{render_tasks(latest.get("can",""), "#22c55e")}</div>', unsafe_allow_html=True)

        if latest.get('carried') and latest.get('carried') != 'NONE':
            st.markdown('<div class="sec-label sec-label-amber">↩ CARRIED FORWARD</div>', unsafe_allow_html=True)
            st.markdown(f'''
            <div class="j-card j-card-amber">
                <div style="font-size:0.8rem;color:#ccc">{latest.get("carried")}</div>
            </div>
            ''', unsafe_allow_html=True)
    else:
        st.markdown('''
        <div class="j-card" style="text-align:center;padding:40px">
            <div style="font-family:'Fraunces',serif;font-size:1.2rem;color:#333">No data yet</div>
            <div style="font-size:0.7rem;color:#333;margin-top:8px;letter-spacing:1px">PASTE YOUR FIRST MORNING BLOCK →</div>
        </div>
        ''', unsafe_allow_html=True)

# ════════════════════════════════════════
# MIDDLE COLUMN — Stats + Weekly + Alive
# ════════════════════════════════════════
with mid:

    # Stats row
    s1, s2, s3 = st.columns(3)

    with s1:
        # Count tasks done
        done_count = 0
        total_count = 0
        if latest:
            for field in ['must', 'should', 'can']:
                val = latest.get(field, '')
                if val and val != 'NONE':
                    items = val.split('·')
                    total_count += len(items)
                    done_count += sum(1 for i in items if '✓' in i)
        st.markdown(f'''
        <div class="j-card" style="padding:16px">
            <div class="stat-label-sm">TASKS DONE</div>
            <div class="stat-num">{done_count}<span style="font-size:1rem;color:#333">/{total_count}</span></div>
        </div>
        ''', unsafe_allow_html=True)

    with s2:
        # Week goal progress
        week_goal = latest.get('week_goal', '') if latest else ''
        prog_match = re.search(r'(\d+)/(\d+)', week_goal)
        if prog_match:
            wdone, wtotal = prog_match.group(1), prog_match.group(2)
        else:
            wdone, wtotal = '0', '3'
        st.markdown(f'''
        <div class="j-card" style="padding:16px">
            <div class="stat-label-sm">WEEK GOAL</div>
            <div class="stat-num" style="color:#1D7FE8">{wdone}<span style="font-size:1rem;color:#333">/{wtotal}</span></div>
        </div>
        ''', unsafe_allow_html=True)

    with s3:
        st.markdown(f'''
        <div class="j-card" style="padding:16px">
            <div class="stat-label-sm">CHATS LOGGED</div>
            <div class="stat-num" style="color:#E63946">{len(chats)}</div>
        </div>
        ''', unsafe_allow_html=True)

    # Progress bar
    if total_count > 0:
        pct = done_count / total_count
        fig = go.Figure(go.Bar(
            x=[pct], y=[''],
            orientation='h',
            marker=dict(color='#E63946'),
            width=0.4
        ))
        fig.add_trace(go.Bar(
            x=[1-pct], y=[''],
            orientation='h',
            marker=dict(color='#1a1a1a'),
            width=0.4
        ))
        fig.update_layout(
            barmode='stack',
            height=40,
            margin=dict(l=0,r=0,t=0,b=0),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            xaxis=dict(visible=False, range=[0,1]),
            yaxis=dict(visible=False),
            bargap=0
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # 8-week tracker
    st.markdown('<div class="sec-label">8-WEEK CHALLENGE · MAY 4 — JUN 28</div>', unsafe_allow_html=True)

    # Build day grid
    day_map = {}
    for chat in chats:
        if 'date' in chat:
            try:
                d = datetime.strptime(chat['date'], '%A, %B %d %Y').date()
                day_map[d] = chat
            except:
                pass

    cols_per_row = 8
    weeks = 7
    grid_html = '<div style="display:grid;grid-template-columns:repeat(8,1fr);gap:5px;margin-top:12px">'

    # Week labels
    for w in range(1, 9):
        grid_html += f'<div style="font-size:0.55rem;color:#333;letter-spacing:1px;text-align:center;padding-bottom:4px">WK{w}</div>'

    for day_num in range(1, CHALLENGE_DAYS + 1):
        day_date = CHALLENGE_START + timedelta(days=day_num - 1)
        day_data = day_map.get(day_date)
        is_today = day_date == date.today()
        is_future = day_date > date.today()
        is_past = day_date < date.today()

        if is_future:
            color = '#141414'
            border = '1px solid #1a1a1a'
            opacity = '0.4'
        elif is_today:
            color = '#1D7FE8'
            border = '2px solid #1D7FE8'
            opacity = '1'
        elif day_data:
            color = get_day_color(day_data)
            border = 'none'
            opacity = '1'
        else:
            color = '#E63946'
            border = '1px solid #2a1a1a'
            opacity = '0.6'

        tooltip = f"Day {day_num} · {day_date.strftime('%b %d')}"
        grid_html += f'<div title="{tooltip}" style="aspect-ratio:1;background:{color};border:{border};border-radius:5px;opacity:{opacity}"></div>'

    grid_html += '</div>'

    # Legend
    grid_html += '''
    <div style="display:flex;gap:16px;margin-top:10px">
        <div style="display:flex;align-items:center;gap:5px">
            <div style="width:8px;height:8px;background:#22c55e;border-radius:2px"></div>
            <span style="font-size:0.6rem;color:#444;letter-spacing:1px">STRONG</span>
        </div>
        <div style="display:flex;align-items:center;gap:5px">
            <div style="width:8px;height:8px;background:#f59e0b;border-radius:2px"></div>
            <span style="font-size:0.6rem;color:#444;letter-spacing:1px">PARTIAL</span>
        </div>
        <div style="display:flex;align-items:center;gap:5px">
            <div style="width:8px;height:8px;background:#E63946;border-radius:2px"></div>
            <span style="font-size:0.6rem;color:#444;letter-spacing:1px">MISSED</span>
        </div>
        <div style="display:flex;align-items:center;gap:5px">
            <div style="width:8px;height:8px;background:#1D7FE8;border-radius:2px"></div>
            <span style="font-size:0.6rem;color:#444;letter-spacing:1px">TODAY</span>
        </div>
    </div>
    '''
    st.markdown(grid_html, unsafe_allow_html=True)

    # What's Alive
    st.markdown('<div class="sec-label">◎ WHAT\'S ALIVE</div>', unsafe_allow_html=True)

    status_colors = {
        'active': ('#1D7FE8', '#1D7FE818', '#1D7FE830'),
        'pending': ('#f59e0b', '#f59e0b18', '#f59e0b30'),
        'flagged': ('#E63946', '#E6394618', '#E6394630'),
        'done': ('#22c55e', '#22c55e18', '#22c55e30'),
    }

    for item in data.get('alive', []):
        sc, sbg, sborder = status_colors.get(item['status'], ('#666', '#66618', '#66630'))
        st.markdown(f'''
        <div class="alive-row" style="border-left:3px solid {sc}">
            <div style="display:flex;gap:12px;align-items:center">
                <span style="font-size:1.3rem">{item["icon"]}</span>
                <div>
                    <div style="font-size:0.85rem;color:#f0ece4;font-weight:500">{item["label"]}</div>
                    <div style="font-size:0.65rem;color:#444;margin-top:2px;letter-spacing:0.5px">{item["sub"]}</div>
                </div>
            </div>
            <span class="status-pill" style="background:{sbg};color:{sc};border:1px solid {sborder}">{item["status"].upper()}</span>
        </div>
        ''', unsafe_allow_html=True)

# ════════════════════════════════════════
# RIGHT COLUMN — Log input + Journey log
# ════════════════════════════════════════
with right:

    st.markdown('<div class="sec-label sec-label-red">⚡ PASTE LOG BLOCK</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.65rem;color:#333;margin-bottom:10px;letter-spacing:0.5px">Copy the block Claude generates at end of chat and paste below</div>', unsafe_allow_html=True)

    log_input = st.text_area(
        "",
        height=200,
        placeholder="=== CHAT 002 · BLOCK 2.0 · MORNING ===\nDate: Monday, May 4 2026\nOne Big Thing: ...\nMust: ...\n...\n=== END BLOCK ===",
        label_visibility="collapsed"
    )

    if st.button("UPDATE DASHBOARD →"):
        if log_input.strip():
            parsed = parse_log_block(log_input)
            if parsed:
                # Add timestamp
                parsed['logged_at'] = datetime.now().isoformat()
                parsed['raw'] = log_input

                # Check if updating existing chat or adding new block
                chat_num_new = parsed.get('chat_num', len(chats) + 1)
                existing_idx = next((i for i, c in enumerate(chats) if c.get('chat_num') == chat_num_new), None)

                if existing_idx is not None:
                    # Update existing chat with new block
                    chats[existing_idx].update(parsed)
                    # Keep blocks history
                    if 'blocks' not in chats[existing_idx]:
                        chats[existing_idx]['blocks'] = []
                    chats[existing_idx]['blocks'].append({
                        'block_num': parsed.get('block_num', ''),
                        'session_type': parsed.get('session_type', ''),
                        'data': parsed
                    })
                else:
                    parsed['blocks'] = [{
                        'block_num': parsed.get('block_num', '1.0'),
                        'session_type': parsed.get('session_type', 'MORNING'),
                        'data': parsed
                    }]
                    chats.append(parsed)

                data['chats'] = chats
                save_data(data)
                st.success("✓ Dashboard updated")
                st.rerun()
            else:
                st.error("Couldn't parse that block. Check the format.")
        else:
            st.warning("Paste a log block first.")

    st.markdown('<hr>', unsafe_allow_html=True)

    # Journey Log
    st.markdown('<div class="sec-label">📖 JOURNEY LOG</div>', unsafe_allow_html=True)

    if not chats:
        st.markdown('''
        <div class="log-card" style="text-align:center;padding:30px">
            <div style="font-family:'Fraunces',serif;font-size:1rem;color:#2a2a2a">Your log starts here</div>
            <div style="font-size:0.65rem;color:#222;margin-top:6px;letter-spacing:1px">CHAT 001 WILL APPEAR AFTER FIRST PASTE</div>
        </div>
        ''', unsafe_allow_html=True)
    else:
        for chat in reversed(chats):
            chat_n = str(chat.get('chat_num', '?')).zfill(3)
            chat_date = chat.get('date', 'Unknown date')
            chat_summary = chat.get('one_line', '')
            chat_obt = chat.get('obt', '')

            blocks_html = ''
            for block in chat.get('blocks', []):
                bn = block.get('block_num', '')
                bt = block.get('session_type', '')
                bd = block.get('data', {})
                blocks_html += f'''
                <div style="margin-top:10px;padding-top:10px;border-top:1px solid #1a1a1a">
                    <div class="log-block-label">BLOCK {bn} · {bt}</div>
                    <div class="log-detail">
                        OBT: <span>{bd.get("obt","—")}</span><br>
                        Must: <span>{bd.get("must","—")}</span><br>
                        Carried: <span>{bd.get("carried","NONE")}</span>
                    </div>
                </div>
                '''

            with st.expander(f"Chat {chat_n} · {chat_date}", expanded=False):
                st.markdown(f'''
                <div>
                    <div style="font-size:0.75rem;color:#666;font-style:italic;margin-bottom:8px">"{chat_summary}"</div>
                    <div class="log-detail">
                        <b style="color:#aaa">OBT:</b> <span>{chat_obt}</span><br>
                        <b style="color:#aaa">Must:</b> <span>{chat.get("must","—")}</span><br>
                        <b style="color:#aaa">Should:</b> <span>{chat.get("should","—")}</span><br>
                        <b style="color:#aaa">Carried:</b> <span>{chat.get("carried","NONE")}</span><br>
                        <b style="color:#aaa">Week:</b> <span>{chat.get("week_goal","—")}</span>
                    </div>
                    {blocks_html}
                </div>
                ''', unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────
st.markdown('<hr>', unsafe_allow_html=True)
footer_cols = st.columns(4)
with footer_cols[0]:
    st.markdown('<div style="font-size:0.6rem;color:#222;letter-spacing:1.5px">JARVIS · DHRUV KUMAR</div>', unsafe_allow_html=True)
with footer_cols[1]:
    st.markdown(f'<div style="font-size:0.6rem;color:#222;letter-spacing:1.5px">CHALLENGE: DAY {challenge_day} OF {CHALLENGE_DAYS}</div>', unsafe_allow_html=True)
with footer_cols[2]:
    st.markdown(f'<div style="font-size:0.6rem;color:#222;letter-spacing:1.5px">CHATS LOGGED: {len(chats)}</div>', unsafe_allow_html=True)
with footer_cols[3]:
    st.markdown('<div style="font-size:0.6rem;color:#222;letter-spacing:1.5px;text-align:right">BERLIN · 2026</div>', unsafe_allow_html=True)
