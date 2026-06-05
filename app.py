import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os
from hashlib import sha256
import base64
import time
import random

# Page configuration
st.set_page_config(
    page_title="MahaSTRIDE - Enterprise Task Management",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Theme state
if "theme" not in st.session_state:
    st.session_state.theme = "light"

# Custom CSS with theme support
def get_theme_css():
    if st.session_state.theme == "dark":
        return """
        <style>
            .main-header { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); color: white; }
            .stat-card { background: linear-gradient(135deg, #0f3460 0%, #16213e 100%); color: white; }
            .task-card { background: #1a1a2e; border-left-color: #e94560; color: white; }
            .task-completed { background: #0a3d2f; border-left-color: #00ff88; }
            .task-pending { background: #3d2f0a; border-left-color: #ffaa00; }
            .leaderboard-card { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); color: white; }
            .credentials-box { background: #1a1a2e; border-color: #e94560; color: white; }
            .stMarkdown, .stMetric, .stDataFrame { color: white; }
            .stApp { background-color: #0f0f1a; }
        </style>
        """
    else:
        return """
        <style>
            .main-header { background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: white; }
            .stat-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
            .task-card { background: white; border-left-color: #2a5298; }
            .task-completed { background: #d4edda; border-left-color: #28a745; }
            .task-pending { background: #fff3cd; border-left-color: #ffc107; }
            .leaderboard-card { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
            .credentials-box { background: #f8f9fa; border-color: #2a5298; }
        </style>
        """

st.markdown(get_theme_css(), unsafe_allow_html=True)

# Theme toggle button
col_theme1, col_theme2 = st.columns([6, 1])
with col_theme2:
    if st.button("🌓" if st.session_state.theme == "light" else "☀️"):
        st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"
        st.rerun()

# ============================================================
# USER CREDENTIALS
# ============================================================
USERS = {
    "admin@mahastride.com": {
        "password": sha256("Admin@2026".encode()).hexdigest(),
        "role": "admin",
        "name": "Administrator",
        "team": "MITRA",
        "avatar": "👨‍💼"
    },
    "projectlead@mahastride.com": {
        "password": sha256("ProjectLead@2026".encode()).hexdigest(),
        "role": "project_lead",
        "name": "Dr. Harshal Kotwal",
        "team": "ICARE",
        "avatar": "👨‍🔬"
    },
    "sneha@mu.edu": {
        "password": sha256("Sneha@2026".encode()).hexdigest(),
        "role": "data_analyst",
        "name": "Sneha Kashitkar",
        "team": "Mumbai University",
        "avatar": "👩‍🎓"
    },
    "shubham@mitra.gov.in": {
        "password": sha256("Shubham@2026".encode()).hexdigest(),
        "role": "data_analyst",
        "name": "Shubham Singh",
        "team": "MITRA",
        "avatar": "👨‍💻"
    },
    "sagar@mu.edu": {
        "password": sha256("Sagar@2026".encode()).hexdigest(),
        "role": "data_analyst",
        "name": "Sagar Teli",
        "team": "Mumbai University",
        "avatar": "👨‍🎓"
    },
    "jagan@sspu.edu": {
        "password": sha256("Jagan@2026".encode()).hexdigest(),
        "role": "data_analyst",
        "name": "Jagan Sridhar",
        "team": "SPPU Pune",
        "avatar": "👨‍🏫"
    },
    "vaibhav@coep.edu": {
        "password": sha256("Vaibhav@2026".encode()).hexdigest(),
        "role": "data_analyst",
        "name": "Vaibhav Ambekar",
        "team": "COEP Pune",
        "avatar": "👨‍🔧"
    },
    "pratham@au.edu": {
        "password": sha256("Pratham@2026".encode()).hexdigest(),
        "role": "data_analyst",
        "name": "Prathamesh Babhulkar",
        "team": "Amravati University",
        "avatar": "👨‍🎓"
    },
    "anjali@nu.edu": {
        "password": sha256("Anjali@2026".encode()).hexdigest(),
        "role": "data_analyst",
        "name": "Anjali Singh",
        "team": "Nagpur University",
        "avatar": "👩‍🎓"
    },
    "nitish@kbcnmu.edu": {
        "password": sha256("Nitish@2026".encode()).hexdigest(),
        "role": "data_analyst",
        "name": "Nitish Kumbhar",
        "team": "KBCNMU Jalgaon",
        "avatar": "👨‍🎓"
    },
    "atharv@bamu.edu": {
        "password": sha256("Atharv@2026".encode()).hexdigest(),
        "role": "data_analyst",
        "name": "Atharav Paturkar",
        "team": "BAMU Aurangabad",
        "avatar": "👨‍🎓"
    }
}

# ============================================================
# DATA FILES
# ============================================================
DAILY_TASKS_FILE = "daily_tasks_complete.json"
TASK_COMPLETION_FILE = "task_completion.json"
ACHIEVEMENTS_FILE = "achievements.json"
NOTIFICATIONS_FILE = "notifications.json"
AUDIT_LOG_FILE = "audit_log.json"

# ============================================================
# AUDIT LOG FUNCTION
# ============================================================

def log_audit(email, action, details):
    """Log user actions for admin audit"""
    audit_log = load_audit_log()
    audit_log.append({
        "timestamp": datetime.now().isoformat(),
        "user": email,
        "user_name": USERS.get(email, {}).get("name", email),
        "action": action,
        "details": details
    })
    # Keep only last 500 entries
    if len(audit_log) > 500:
        audit_log = audit_log[-500:]
    save_audit_log(audit_log)

def load_audit_log():
    if os.path.exists(AUDIT_LOG_FILE):
        with open(AUDIT_LOG_FILE, 'r') as f:
            return json.load(f)
    return []

def save_audit_log(log):
    with open(AUDIT_LOG_FILE, 'w') as f:
        json.dump(log, f, indent=2)

# ============================================================
# MOTIVATIONAL QUOTES
# ============================================================

MOTIVATIONAL_QUOTES = [
    ("🌟", "The secret of getting ahead is getting started.", "Mark Twain"),
    ("💪", "Your limitation—it’s only your imagination.", "Unknown"),
    ("🎯", "Push yourself, because no one else is going to do it for you.", "Unknown"),
    ("🏆", "Great things never come from comfort zones.", "Unknown"),
    ("🚀", "Dream it. Wish it. Do it.", "Unknown"),
    ("⭐", "Success doesn’t just find you. You have to go out and get it.", "Unknown"),
    ("📈", "The harder you work for something, the greater you’ll feel when you achieve it.", "Unknown"),
    ("💡", "Dream bigger. Do bigger.", "Unknown"),
    ("🔥", "Don’t stop when you’re tired. Stop when you’re done.", "Unknown"),
    ("🎉", "Wake up with determination. Go to bed with satisfaction.", "Unknown")
]

def get_motivational_quote():
    icon, quote, author = random.choice(MOTIVATIONAL_QUOTES)
    return f"{icon} *\"{quote}\"* — {author}"

# ============================================================
# TASK FUNCTIONS
# ============================================================

def generate_all_unique_tasks():
    """Generate unique tasks for every working day from May 2026 to April 2028"""
    all_tasks = {}
    
    # Pre-defined unique tasks
    monthly_tasks = {
        "2026-06-08": "Conduct kickoff meeting with Mumbai University VC and IQAC team",
        "2026-06-09": "Interview 10 faculty members at Mumbai University for research assessment",
        "2026-06-10": "Collect and verify student enrollment data from all departments",
        "2026-06-11": "Document faculty publication records for last 5 years",
        "2026-06-12": "Compile research grants and project funding data",
        "2026-06-15": "Analyze placement data and graduate outcomes for last 3 years",
        "2026-06-16": "Review library resources and digital infrastructure across campuses",
        "2026-06-17": "Assess laboratory facilities and research equipment availability",
        "2026-06-18": "Evaluate international collaboration MoUs and joint research projects",
        "2026-06-19": "Prepare data gap analysis report for all 7 universities",
        "2026-06-22": "Constitute GRDAU team with nominated members from each department",
        "2026-06-23": "Develop standard operating procedures for GRDAU operations",
        "2026-06-24": "Train GRDAU staff on NIRF data collection and validation",
        "2026-06-25": "Setup data management system with access controls for GRDAU",
        "2026-06-26": "Review diagnostic assessment findings with university leadership",
        "2026-06-29": "Finalize diagnostic reports for submission to PMU",
        "2026-06-30": "Submit June Monthly Progress Report with all achievements",
        "2026-07-01": "Complete comprehensive gap analysis against NIRF 2026 parameters",
        "2026-07-02": "Prepare SWOT analysis report for Mumbai University",
        "2026-07-03": "Prepare SWOT analysis report for Pune University",
        "2026-07-06": "Prepare SWOT analysis report for Nagpur University",
        "2026-07-07": "Prepare SWOT analysis report for Amravati University",
        "2026-07-08": "Prepare SWOT analysis report for COEP University",
        "2026-07-09": "Prepare SWOT analysis report for KBCNMU Jalgaon",
        "2026-07-10": "Prepare SWOT analysis report for BAMU Aurangabad",
        "2026-07-13": "Finalize GRDAU establishment plan and submit for approval",
        "2026-07-14": "Setup GRDAU office with required hardware and software",
        "2026-07-15": "Conduct data entry training for newly appointed GRDAU staff",
        "2026-07-16": "Create data validation protocols and quality checklists",
        "2026-07-17": "Develop dashboard requirements document with stakeholder inputs",
        "2026-07-20": "Design baseline report template for Phase 1 completion",
        "2026-07-21": "Compile all Phase 1 deliverables and prepare completion report",
        "2026-07-22": "Present Phase 1 findings to MITRA steering committee",
        "2026-07-23": "Document lessons learned and best practices from Phase 1",
        "2026-07-24": "Plan Phase 2 activities with detailed work breakdown structure",
        "2026-07-27": "Prepare July Monthly Progress Report with Phase 1 summary",
        "2026-07-28": "Submit July MPR and Phase 1 completion report to PMU",
        "2026-07-29": "Review and incorporate client feedback on Phase 1 deliverables",
        "2026-07-30": "Finalize Phase 2 work plan and resource allocation",
        "2026-07-31": "Conduct Phase 2 kickoff meeting with all university coordinators",
        "2026-08-03": "Develop IDP framework template aligned with NIRF metrics",
        "2026-08-04": "Collect strategic plans from Mumbai University leadership",
        "2026-08-05": "Collect strategic plans from Pune University VC office",
        "2026-08-06": "Collect strategic plans from Nagpur University administration",
        "2026-08-07": "Collect strategic plans from Amravati University",
        "2026-08-10": "Collect strategic plans from COEP University Director",
        "2026-08-11": "Collect strategic plans from KBCNMU Jalgaon",
        "2026-08-12": "Collect strategic plans from BAMU Aurangabad",
        "2026-08-13": "Analyze collected strategic plans and identify common themes",
        "2026-08-14": "Draft Institutional Development Plan for Mumbai University",
        "2026-08-17": "Draft IDP for Pune University with specific KPIs",
        "2026-08-18": "Draft IDP for Nagpur University focusing on research excellence",
        "2026-08-19": "Draft IDP for Amravati University with timeline",
        "2026-08-20": "Draft IDP for COEP University emphasizing industry connect",
        "2026-08-21": "Draft IDP for KBCNMU Jalgaon with internationalization goals",
        "2026-08-24": "Draft IDP for BAMU Aurangabad focusing on infrastructure",
        "2026-08-25": "Present IDP drafts to respective Vice Chancellors for feedback",
        "2026-08-26": "Incorporate VC feedback and finalize IDPs for all universities",
        "2026-08-27": "Get formal institutional sign-off on approved IDPs",
        "2026-08-28": "Prepare August MPR documenting IDP development progress",
        "2026-08-31": "Submit August MPR to PMU with IDP status report",
    }
    
    # Generate tasks for remaining months
    current_date = datetime(2026, 9, 1)
    end_date = datetime(2028, 4, 28)
    
    phase_tasks = [
        "Design data portal architecture", "Create dashboard wireframes", "Develop backend APIs",
        "Implement user authentication", "Build KPI dashboard", "Integrate research charts",
        "Add faculty-student ratio analytics", "Implement financial tracking", "Develop placement dashboard",
        "Create international metrics", "Add citation analysis", "Implement infrastructure dashboard",
        "Prepare Milestone Report", "Submit to PMU for review", "Conduct user testing",
        "Fix bugs and optimize", "Deploy to staging", "Complete beta testing",
        "Conduct training for administrators", "Create user manual", "Prepare Mid-Term Review",
        "Deploy to production", "Monitor performance", "Setup analytics tracking",
        "Create backup procedures", "Plan Phase 3 activities", "Develop Phase 3 schedule"
    ]
    
    task_index = 0
    while current_date <= end_date:
        if current_date.weekday() < 5:
            date_str = current_date.strftime("%Y-%m-%d")
            task = phase_tasks[task_index % len(phase_tasks)]
            priority = "High" if any(w in task.lower() for w in ["milestone", "submit", "present", "final"]) else "Medium"
            all_tasks[date_str] = {"task": task, "priority": priority, "phase": "Implementation"}
            task_index += 1
        current_date += timedelta(days=1)
    
    for date_str, task_info in monthly_tasks.items():
        all_tasks[date_str] = {"task": task_info, "priority": "High", "phase": "Foundation"}
    
    return all_tasks

def load_tasks():
    if os.path.exists(DAILY_TASKS_FILE):
        with open(DAILY_TASKS_FILE, 'r') as f:
            return json.load(f)
    tasks = generate_all_unique_tasks()
    with open(DAILY_TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)
    return tasks

def load_completions():
    if os.path.exists(TASK_COMPLETION_FILE):
        with open(TASK_COMPLETION_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_completions(completions):
    with open(TASK_COMPLETION_FILE, 'w') as f:
        json.dump(completions, f, indent=2)

def load_achievements():
    if os.path.exists(ACHIEVEMENTS_FILE):
        with open(ACHIEVEMENTS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_achievements(achievements):
    with open(ACHIEVEMENTS_FILE, 'w') as f:
        json.dump(achievements, f, indent=2)

def load_notifications():
    if os.path.exists(NOTIFICATIONS_FILE):
        with open(NOTIFICATIONS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_notifications(notifications):
    with open(NOTIFICATIONS_FILE, 'w') as f:
        json.dump(notifications, f, indent=2)

def add_notification(email, title, message):
    notifications = load_notifications()
    if email not in notifications:
        notifications[email] = []
    notifications[email].append({
        "id": len(notifications[email]) + 1,
        "title": title,
        "message": message,
        "timestamp": datetime.now().isoformat(),
        "read": False
    })
    save_notifications(notifications)

def initialize_completed_tasks():
    completions = load_completions()
    all_tasks = load_tasks()
    
    completed_dates = []
    start_date = datetime(2026, 5, 4)
    end_date = datetime(2026, 6, 5)
    current = start_date
    while current <= end_date:
        if current.weekday() < 5:
            date_str = current.strftime("%Y-%m-%d")
            if date_str in all_tasks:
                completed_dates.append(date_str)
        current += timedelta(days=1)
    
    for email, user in USERS.items():
        if user.get("role") == "data_analyst":
            if email not in completions:
                completions[email] = {}
            for date_str in completed_dates:
                if date_str not in completions[email]:
                    completions[email][date_str] = {
                        "completed_at": datetime(2026, 6, 5, 17, 0, 0).isoformat(),
                        "remarks": "Completed - Initial project setup phase"
                    }
    
    save_completions(completions)
    
    achievements = load_achievements()
    for email, user in USERS.items():
        if user.get("role") == "data_analyst" and email not in achievements:
            achievements[email] = {"points": 0, "badges": []}
    save_achievements(achievements)
    
    return len(completed_dates)

def get_user_tasks(email):
    user = USERS.get(email, {})
    all_tasks = load_tasks()
    completions = load_completions()
    user_completions = completions.get(email, {})
    
    user_tasks = []
    for date_str, task_info in all_tasks.items():
        if user.get("role") == "data_analyst":
            is_completed = date_str in user_completions
            completion_info = user_completions.get(date_str, {})
            user_tasks.append({
                "date": date_str,
                "task": task_info.get("task", "No task assigned"),
                "priority": task_info.get("priority", "Medium"),
                "phase": task_info.get("phase", "Unknown"),
                "status": "Completed" if is_completed else "Pending",
                "completed_at": completion_info.get("completed_at", ""),
                "remarks": completion_info.get("remarks", "")
            })
    return sorted(user_tasks, key=lambda x: x["date"])

def mark_task_complete(email, date_str, remarks, work_hours):
    completions = load_completions()
    if email not in completions:
        completions[email] = {}
    
    completions[email][date_str] = {
        "completed_at": datetime.now().isoformat(),
        "remarks": remarks,
        "work_hours": work_hours
    }
    save_completions(completions)
    
    user_tasks = get_user_tasks(email)
    completed_count = sum(1 for t in user_tasks if t["status"] == "Completed" and t["date"] > "2026-06-05")
    
    achievements = load_achievements()
    if email not in achievements:
        achievements[email] = {"points": 0, "badges": []}
    
    new_badges = []
    if completed_count >= 5 and "Rising Star" not in achievements[email]["badges"]:
        new_badges.append("Rising Star")
        add_notification(email, "🏅 Badge Earned!", "You earned the 'Rising Star' badge!")
    if completed_count >= 15 and "Dedicated Worker" not in achievements[email]["badges"]:
        new_badges.append("Dedicated Worker")
        add_notification(email, "🏅 Badge Earned!", "You earned the 'Dedicated Worker' badge!")
    if completed_count >= 30 and "Task Master" not in achievements[email]["badges"]:
        new_badges.append("Task Master")
        add_notification(email, "🏅 Badge Earned!", "You earned the 'Task Master' badge!")
    
    achievements[email]["badges"].extend(new_badges)
    achievements[email]["points"] = completed_count * 10
    save_achievements(achievements)
    
    add_notification(email, "✅ Task Completed", f"Completed task on {date_str}")
    log_audit(email, "task_completed", f"Completed task on {date_str}")
    
    return True

def get_all_analysts_progress():
    all_tasks = load_tasks()
    completions = load_completions()
    achievements = load_achievements()
    total_tasks = len(all_tasks)
    
    progress_data = []
    for email, user in USERS.items():
        if user.get("role") == "data_analyst":
            user_completions = completions.get(email, {})
            completed = len(user_completions)
            user_achievements = achievements.get(email, {"points": 0, "badges": []})
            progress_data.append({
                "name": user["name"],
                "team": user.get("team", "N/A"),
                "avatar": user.get("avatar", "👤"),
                "completed": completed,
                "total": total_tasks,
                "progress": round((completed / total_tasks * 100), 1),
                "points": user_achievements.get("points", 0),
                "badges": len(user_achievements.get("badges", []))
            })
    return pd.DataFrame(progress_data).sort_values("progress", ascending=False)

def generate_mpr_html(year, month):
    month_names = ["January", "February", "March", "April", "May", "June", 
                   "July", "August", "September", "October", "November", "December"]
    month_name = month_names[month-1]
    progress_df = get_all_analysts_progress()
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Monthly Progress Report - {month_name} {year}</title>
    <style>
        body {{ font-family: 'Times New Roman', serif; margin: 0.7in; font-size: 11pt; }}
        .header {{ text-align: center; margin-bottom: 20px; }}
        .report-title {{ font-size: 14pt; font-weight: bold; text-align: center; margin: 15px 0; }}
        .section-title {{ font-size: 12pt; font-weight: bold; margin-top: 15px; margin-bottom: 8px; background-color: #f0f0f0; padding: 5px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
        th, td {{ border: 1px solid #000; padding: 6px; vertical-align: top; }}
        th {{ background-color: #e8e8e8; font-weight: bold; text-align: center; }}
        .footer {{ text-align: center; font-size: 9pt; font-style: italic; margin-top: 30px; }}
    </style>
</head>
<body>
<div class="header">
    <h2>Maharashtra Institution for Transformation (MITRA)</h2>
    <h3>Monthly Progress Report - {month_name} {year}</h3>
</div>

<div class="section-title">1. Team Performance Summary</div>
<table>
    <tr><th>Rank</th><th>Team Member</th><th>Team</th><th>Tasks Completed</th><th>Progress</th><th>Points</th><th>Badges</th></tr>
    {''.join([f'<tr><td>{i+1}</td><td>{row["name"]}</td><td>{row["team"]}</td><td>{row["completed"]}</td><td>{row["progress"]}%</td><td>{row["points"]}</td><td>{row["badges"]}</td></tr>' for i, (_, row) in enumerate(progress_df.head(10).iterrows())])}
</table>

<div class="section-title">2. Overall Statistics</div>
<table>
    <tr><td><strong>Total Working Days (24 months)</strong></td><td>{len(load_tasks())}</td></tr>
    <tr><td><strong>Total Task Completions</strong></td><td>{sum(len(c) for c in load_completions().values())}</td></tr>
    <tr><td><strong>Active Team Members</strong></td><td>{len(progress_df)}</td></tr>
</table>

<div class="footer">Generated on {datetime.now().strftime('%d-%b-%Y %H:%M:%S')}</div>
</body>
</html>"""
    return html

def get_download_link(html, filename):
    b64 = base64.b64encode(html.encode()).decode()
    return f'<a href="data:text/html;base64,{b64}" download="{filename}" style="background:#28a745;color:white;padding:10px 20px;text-decoration:none;border-radius:5px;">📥 Download {filename}</a>'

def show_credentials():
    st.markdown("""
    <div class="credentials-box">
        <h4>🔐 Login Credentials</h4>
        <p><strong>Password for all accounts:</strong> <code>Name@2026</code> (e.g., Admin@2026, Sneha@2026)</p>
        <table style="width:100%; font-size:12px;">
            <tr><th>Role</th><th>Email</th><th>Password</th></tr>
            <td>🔴 Admin</div><td>admin@mahastride.com</div><td>Admin@2026</div></tr>
            <td>🔵 Project Lead</div><td>projectlead@mahastride.com</div><td>ProjectLead@2026</div></tr>
            <td>🟢 Data Analyst</div><td>sneha@mu.edu</div><td>Sneha@2026</div></tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# DATA ANALYST DASHBOARD
# ============================================================

def data_analyst_dashboard(email, user):
    st.markdown(f"## {user.get('avatar', '📝')} My Tasks - {user.get('name')}")
    st.markdown(f"**Team:** {user.get('team', 'N/A')}")
    
    # Real-time clock
    current_time = datetime.now().strftime("%I:%M %p")
    current_date = datetime.now().strftime("%A, %B %d, %Y")
    st.markdown(f"<div style='text-align: center; padding: 10px; background: #e8f4f8; border-radius: 10px; margin-bottom: 10px;'>📅 {current_date} | 🕐 {current_time} | Working Hours: 10:00 AM - 6:00 PM</div>", unsafe_allow_html=True)
    
    # Motivational quote
    st.info(get_motivational_quote())
    
    user_tasks = get_user_tasks(email)
    achievements = load_achievements().get(email, {"points": 0, "badges": []})
    
    pending_tasks = [t for t in user_tasks if t["date"] > "2026-06-05" and t["status"] == "Pending"]
    completed_tasks = [t for t in user_tasks if t["date"] > "2026-06-05" and t["status"] == "Completed"]
    initial_completed = [t for t in user_tasks if t["date"] <= "2026-06-05"]
    
    # Weekly summary
    today = datetime.now()
    week_start = today - timedelta(days=today.weekday())
    week_tasks = [t for t in user_tasks if t["date"] > "2026-06-05" and datetime.strptime(t["date"], "%Y-%m-%d") >= week_start and datetime.strptime(t["date"], "%Y-%m-%d") <= today]
    week_completed = sum(1 for t in week_tasks if t["status"] == "Completed")
    week_total = len(week_tasks)
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        st.metric("📅 Total", len(user_tasks))
    with col2:
        st.metric("✅ Initial", len(initial_completed))
    with col3:
        st.metric("✅ Your Work", len(completed_tasks))
    with col4:
        st.metric("⏳ Pending", len(pending_tasks))
    with col5:
        st.metric("🏆 Points", achievements.get("points", 0))
    with col6:
        st.metric("📅 This Week", f"{week_completed}/{week_total}")
    
    if achievements.get("badges"):
        st.markdown("### 🎖️ Your Badges")
        cols = st.columns(len(achievements["badges"]))
        for idx, badge in enumerate(achievements["badges"]):
            with cols[idx]:
                st.markdown(f'<div class="achievement-badge">🏅 {badge}</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Today's task with complete button
    today = datetime.now().strftime("%Y-%m-%d")
    today_task = next((t for t in user_tasks if t["date"] == today and t["date"] > "2026-06-05"), None)
    
    if today_task:
        st.subheader("📌 Today's Task")
        if today_task["status"] == "Completed":
            st.markdown(f"""
            <div class="task-card task-completed">
                ✅ <strong>COMPLETED</strong><br>
                <strong>Task:</strong> {today_task['task']}<br>
                <strong>Phase:</strong> {today_task.get('phase', 'N/A')}<br>
                <strong>Completed:</strong> {today_task.get('completed_at', 'N/A')[:16] if today_task.get('completed_at') else 'N/A'}
            </div>
            """, unsafe_allow_html=True)
        else:
            with st.form(key="complete_today_task"):
                priority_badge = "🔴 HIGH" if today_task["priority"] == "High" else "🟡 MEDIUM" if today_task["priority"] == "Medium" else "🟢 LOW"
                st.markdown(f"""
                <div class="task-card task-pending">
                    <strong>⏳ PENDING - {priority_badge}</strong><br>
                    <strong>Task:</strong> {today_task['task']}<br>
                    <strong>Phase:</strong> {today_task.get('phase', 'N/A')}
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    start_time = st.time_input("Start Time", value=datetime.strptime("10:00", "%H:%M").time())
                with col2:
                    end_time = st.time_input("End Time", value=datetime.strptime("18:00", "%H:%M").time())
                
                work_hours = f"{start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}"
                remarks = st.text_area("📝 Work Accomplished", height=100)
                
                if st.form_submit_button("✅ MARK AS COMPLETE", use_container_width=True, type="primary"):
                    if remarks:
                        if mark_task_complete(email, today_task["date"], remarks, work_hours):
                            st.success("🎉 Task completed! Great work!")
                            st.balloons()
                            time.sleep(1)
                            st.rerun()
                    else:
                        st.error("Please describe your work")
    
    st.markdown("---")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📅 Pending Tasks", "📊 My Progress", "🏆 Leaderboard", "🔔 Notifications"])
    
    with tab1:
        st.subheader(f"Pending Tasks ({len(pending_tasks)})")
        if pending_tasks:
            for task in pending_tasks[:20]:
                priority_badge = "🔴" if task["priority"] == "High" else "🟡" if task["priority"] == "Medium" else "🟢"
                with st.expander(f"{priority_badge} 📅 {task['date']} - {task['task'][:80]}..."):
                    st.markdown(f"""
                    **Task:** {task['task']}<br>
                    **Phase:** {task.get('phase', 'N/A')}<br>
                    **Priority:** {task['priority']}
                    """, unsafe_allow_html=True)
                    
                    with st.form(key=f"complete_pending_{task['date']}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            task_start = st.time_input("Start Time", value=datetime.strptime("10:00", "%H:%M").time(), key=f"start_{task['date']}")
                        with col2:
                            task_end = st.time_input("End Time", value=datetime.strptime("18:00", "%H:%M").time(), key=f"end_{task['date']}")
                        
                        task_hours = f"{task_start.strftime('%H:%M')} - {task_end.strftime('%H:%M')}"
                        task_remarks = st.text_area("Work Accomplished", height=80, key=f"remarks_{task['date']}")
                        
                        if st.form_submit_button(f"✅ Complete Task for {task['date']}", use_container_width=True):
                            if task_remarks:
                                if mark_task_complete(email, task["date"], task_remarks, task_hours):
                                    st.success(f"✅ Task for {task['date']} completed!")
                                    st.rerun()
                            else:
                                st.error("Please describe your work")
        else:
            st.success("🎉 All tasks completed! Great job!")
    
    with tab2:
        st.subheader("My Progress")
        total_future = len(pending_tasks) + len(completed_tasks)
        progress_pct = (len(completed_tasks) / total_future * 100) if total_future > 0 else 0
        st.progress(progress_pct / 100)
        st.caption(f"{len(completed_tasks)}/{total_future} tasks completed ({progress_pct:.1f}%)")
        
        monthly_data = {}
        for task in user_tasks:
            if task["date"] > "2026-06-05":
                month_key = task["date"][:7]
                if month_key not in monthly_data:
                    monthly_data[month_key] = {"total": 0, "completed": 0}
                monthly_data[month_key]["total"] += 1
                if task["status"] == "Completed":
                    monthly_data[month_key]["completed"] += 1
        
        if monthly_data:
            df_monthly = pd.DataFrame([{"Month": k, "Completed": v["completed"], "Total": v["total"]} for k, v in monthly_data.items()])
            fig = px.bar(df_monthly, x="Month", y="Completed", title="Monthly Task Completion", text="Total")
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Team Leaderboard")
        progress_df = get_all_analysts_progress()
        for idx, (_, row) in enumerate(progress_df.head(10).iterrows()):
            medal = "🥇" if idx == 0 else "🥈" if idx == 1 else "🥉" if idx == 2 else f"{idx+1}."
            st.markdown(f"""
            <div class="leaderboard-card">
                <strong>{medal} {row['avatar']} {row['name']}</strong> ({row['team']})<br>
                📊 Progress: {row['progress']}% | ✅ Completed: {row['completed']} | 🏆 Points: {row['points']} | 🎖️ Badges: {row['badges']}
            </div>
            """, unsafe_allow_html=True)
    
    with tab4:
        st.subheader("Notifications")
        notifications = load_notifications().get(email, [])
        if notifications:
            for notif in reversed(notifications[-10:]):
                st.info(f"**{notif['title']}**\n\n{notif['message']}\n\n*{notif['timestamp'][:16]}*")
        else:
            st.info("No notifications yet")

# ============================================================
# ADMIN DASHBOARD
# ============================================================

def admin_dashboard():
    st.markdown("## 📊 Admin Dashboard")
    
    all_tasks = load_tasks()
    completions = load_completions()
    progress_df = get_all_analysts_progress()
    audit_log = load_audit_log()
    
    total_users = len([u for u in USERS.values() if u.get("role") == "data_analyst"])
    total_completions = sum(len(c) for c in completions.values())
    avg_completion = total_completions / total_users if total_users > 0 else 0
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown(f"""<div class="stat-card"><div class="metric-value">{len(all_tasks)}</div><div class="metric-label">Total Working Days</div></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="stat-card"><div class="metric-value">{len([d for d in all_tasks.keys() if d <= "2026-06-05"])}</div><div class="metric-label">Initial Completed</div></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class="stat-card"><div class="metric-value">{total_users}</div><div class="metric-label">Team Members</div></div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""<div class="stat-card"><div class="metric-value">{total_completions}</div><div class="metric-label">Total Completions</div></div>""", unsafe_allow_html=True)
    with col5:
        st.markdown(f"""<div class="stat-card"><div class="metric-value">{avg_completion:.1f}</div><div class="metric-label">Avg/User</div></div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Team Progress", "🏆 Leaderboard", "📄 Reports", "📋 Audit Log", "⚙️ System"])
    
    with tab1:
        fig = px.bar(progress_df, x="name", y="progress", color="team", text="progress", height=450)
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(progress_df, use_container_width=True, hide_index=True)
    
    with tab2:
        for idx, (_, row) in enumerate(progress_df.head(10).iterrows()):
            medal = "🥇" if idx == 0 else "🥈" if idx == 1 else "🥉" if idx == 2 else f"{idx+1}."
            st.markdown(f"""
            <div class="leaderboard-card">
                <strong>{medal} {row['avatar']} {row['name']}</strong> - {row['team']}<br>
                📊 Progress: {row['progress']}% | ✅ Completed: {row['completed']} | 🏆 Points: {row['points']} | 🎖️ Badges: {row['badges']}
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            report_year = st.selectbox("Year", [2026, 2027, 2028])
        with col2:
            report_month = st.selectbox("Month", range(1, 13), format_func=lambda x: ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"][x-1])
        if st.button("Generate Report"):
            html = generate_mpr_html(report_year, report_month)
            st.markdown(get_download_link(html, f"MPR_{report_year}_{report_month}.html"), unsafe_allow_html=True)
    
    with tab4:
        st.subheader("Audit Log - User Activity History")
        if audit_log:
            df_audit = pd.DataFrame(audit_log[-50:])
            st.dataframe(df_audit, use_container_width=True, hide_index=True)
            if st.button("Clear Audit Log", use_container_width=True):
                save_audit_log([])
                st.success("Audit log cleared!")
                st.rerun()
        else:
            st.info("No audit logs available")
    
    with tab5:
        st.subheader("System Settings")
        st.info("📁 Data files are stored locally. Backups are recommended.")
        if st.button("🔄 Force Data Reset", use_container_width=True):
            for f in [DAILY_TASKS_FILE, TASK_COMPLETION_FILE, ACHIEVEMENTS_FILE, NOTIFICATIONS_FILE]:
                if os.path.exists(f):
                    os.remove(f)
            st.success("Data reset successfully! Please refresh.")
        st.warning("⚠️ This will reset all user progress. Use with caution.")

def project_lead_dashboard():
    st.markdown("## 👨‍💼 Project Lead Dashboard")
    st.markdown("**Dr. Harshal Kotwal** - ICARE Project Director")
    
    all_tasks = load_tasks()
    progress_df = get_all_analysts_progress()
    
    milestones = [
        {"name": "Milestone 1: Data Systems", "due": "Sep 30, 2026", "status": "pending"},
        {"name": "Milestone 2: IDP Execution", "due": "Oct 31, 2026", "status": "pending"},
        {"name": "Milestone 3: Capacity Building", "due": "Dec 31, 2026", "status": "pending"},
        {"name": "Milestone 4: 10% Improvement", "due": "Jun 30, 2027", "status": "pending"},
        {"name": "Milestone 5: 20% Improvement", "due": "Dec 31, 2027", "status": "pending"},
        {"name": "Milestone 6: Global Rankings", "due": "Feb 29, 2028", "status": "pending"},
        {"name": "Milestone 7: Final Evaluation", "due": "Apr 30, 2028", "status": "pending"}
    ]
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📅 Total Working Days", len(all_tasks))
    with col2:
        st.metric("👥 Team Members", len(progress_df))
    with col3:
        avg_progress = progress_df["progress"].mean() if not progress_df.empty else 0
        st.metric("📈 Avg Progress", f"{avg_progress:.1f}%")
    with col4:
        total_points = progress_df["points"].sum() if not progress_df.empty else 0
        st.metric("🏆 Total Points", total_points)
    
    st.markdown("---")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Team Performance", "🏆 Leaderboard", "🎯 Milestones", "📄 Reports"])
    
    with tab1:
        fig = px.bar(progress_df, x="name", y="progress", color="team", text="progress", height=450)
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(progress_df[["name", "team", "completed", "progress", "points"]], use_container_width=True, hide_index=True)
    
    with tab2:
        for idx, (_, row) in enumerate(progress_df.head(5).iterrows()):
            medal = "🥇" if idx == 0 else "🥈" if idx == 1 else "🥉" if idx == 2 else f"{idx+1}."
            st.markdown(f"""
            <div class="leaderboard-card">
                <strong>{medal} {row['name']}</strong> - {row['team']}<br>
                ✅ Completed: {row['completed']} | 📊 Progress: {row['progress']}% | 🏆 Points: {row['points']}
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        st.subheader("Project Milestones")
        for milestone in milestones:
            status_icon = "⏳" if milestone["status"] == "pending" else "✅"
            st.markdown(f"""
            <div class="task-card">
                <strong>{status_icon} {milestone['name']}</strong><br>
                📅 Due: {milestone['due']}
            </div>
            """, unsafe_allow_html=True)
    
    with tab4:
        col1, col2 = st.columns(2)
        with col1:
            report_year = st.selectbox("Year", [2026, 2027, 2028])
        with col2:
            report_month = st.selectbox("Month", range(1, 13), format_func=lambda x: ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"][x-1])
        if st.button("Generate Report"):
            html = generate_mpr_html(report_year, report_month)
            st.markdown(get_download_link(html, f"MPR_{report_year}_{report_month}.html"), unsafe_allow_html=True)

# ============================================================
# MAIN APP
# ============================================================

def main():
    load_tasks()
    initialize_completed_tasks()
    
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        st.markdown("""
        <div class="main-header">
            <h1>📋 MahaSTRIDE Enterprise Task Management System</h1>
            <p>24-Month Detailed Task Plan | May 2026 - April 2028</p>
            <p>Monday to Friday | 10:00 AM - 6:00 PM</p>
            <p>✅ May 4 to June 5, 2026: COMPLETED | June 8, 2026 onwards: PENDING</p>
            <p>✨ New: Dark Mode | Task Timer | Achievements | Real-time Clock</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("### 🔐 Login")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            
            if st.button("Login", use_container_width=True):
                if email in USERS:
                    hashed_input = sha256(password.encode()).hexdigest()
                    if USERS[email]["password"] == hashed_input:
                        st.session_state.authenticated = True
                        st.session_state.user_email = email
                        st.session_state.user_info = USERS[email]
                        log_audit(email, "login", "User logged in")
                        st.rerun()
                    else:
                        st.error("Invalid password")
                else:
                    st.error("Email not found")
            
            show_credentials()
        return
    
    user_info = st.session_state.user_info
    email = st.session_state.user_email
    role = user_info.get("role", "data_analyst")
    
    with st.sidebar:
        st.markdown(f"## {user_info.get('avatar', '📋')} MahaSTRIDE")
        st.markdown(f"**Welcome, {user_info.get('name')}**")
        if role == "data_analyst":
            st.markdown(f"*Team: {user_info.get('team', 'N/A')}*")
        st.markdown(f"*Role: {role.upper()}*")
        st.markdown("---")
        
        if role == "admin":
            nav_options = ["📊 Dashboard", "📄 Reports"]
        elif role == "project_lead":
            nav_options = ["📊 Dashboard", "📄 Reports"]
        else:
            nav_options = ["📝 My Tasks", "🏆 Achievements", "🔔 Notifications"]
        
        selected_nav = st.radio("Navigation", nav_options, label_visibility="collapsed")
        
        st.markdown("---")
        st.markdown("ℹ️ **Information**")
        st.markdown("🕐 **Hours:** 10 AM - 6 PM")
        st.markdown("📅 **Days:** Monday to Friday")
        st.markdown("✅ **May 4 - June 5, 2026:** COMPLETED")
        
        if role == "data_analyst":
            user_tasks = get_user_tasks(email)
            completed = sum(1 for t in user_tasks if t["status"] == "Completed" and t["date"] > "2026-06-05")
            total = len([t for t in user_tasks if t["date"] > "2026-06-05"])
            if total > 0:
                st.markdown("---")
                st.markdown("**Your Progress**")
                st.progress(completed/total)
                st.caption(f"{completed}/{total} tasks completed")
        
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            log_audit(email, "logout", "User logged out")
            st.session_state.authenticated = False
            st.rerun()
    
    if role == "admin":
        if selected_nav == "📊 Dashboard":
            admin_dashboard()
        else:
            st.markdown("## 📄 Reports")
            col1, col2 = st.columns(2)
            with col1:
                report_year = st.selectbox("Year", [2026, 2027, 2028])
            with col2:
                report_month = st.selectbox("Month", range(1, 13), format_func=lambda x: ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"][x-1])
            if st.button("Generate Report"):
                html = generate_mpr_html(report_year, report_month)
                st.markdown(get_download_link(html, f"MPR_{report_year}_{report_month}.html"), unsafe_allow_html=True)
    
    elif role == "project_lead":
        if selected_nav == "📊 Dashboard":
            project_lead_dashboard()
        else:
            st.markdown("## 📄 Reports")
            col1, col2 = st.columns(2)
            with col1:
                report_year = st.selectbox("Year", [2026, 2027, 2028])
            with col2:
                report_month = st.selectbox("Month", range(1, 13), format_func=lambda x: ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"][x-1])
            if st.button("Generate Report"):
                html = generate_mpr_html(report_year, report_month)
                st.markdown(get_download_link(html, f"MPR_{report_year}_{report_month}.html"), unsafe_allow_html=True)
    
    else:
        if selected_nav == "📝 My Tasks":
            data_analyst_dashboard(email, user_info)
        elif selected_nav == "🏆 Achievements":
            st.markdown(f"## 🏆 My Achievements - {user_info.get('name')}")
            achievements = load_achievements().get(email, {"points": 0, "badges": []})
            user_tasks = get_user_tasks(email)
            completed = sum(1 for t in user_tasks if t["status"] == "Completed" and t["date"] > "2026-06-05")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("🏅 Points Earned", achievements.get("points", 0))
            with col2:
                st.metric("✅ Tasks Completed", completed)
            with col3:
                st.metric("🎖️ Badges Earned", len(achievements.get("badges", [])))
            
            if achievements.get("badges"):
                st.markdown("### 🎖️ Your Badges")
                for badge in achievements["badges"]:
                    st.markdown(f'<div class="achievement-badge">🏅 {badge}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f"## 🔔 Notifications - {user_info.get('name')}")
            notifications = load_notifications().get(email, [])
            if notifications:
                for notif in reversed(notifications):
                    st.info(f"**{notif['title']}**\n\n{notif['message']}\n\n*{notif['timestamp'][:16]}*")
            else:
                st.info("No notifications yet")

if __name__ == "__main__":
    main()
