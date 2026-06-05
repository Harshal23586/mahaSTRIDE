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
import calendar

# Page configuration
st.set_page_config(
    page_title="MahaSTRIDE - Enterprise Project Management",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
    }
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        transition: transform 0.3s;
    }
    .stat-card:hover {
        transform: translateY(-5px);
    }
    .task-card {
        background: white;
        border-left: 4px solid #2a5298;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        transition: all 0.3s;
    }
    .task-card:hover {
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        transform: translateX(5px);
    }
    .task-completed {
        border-left-color: #28a745;
        background-color: #d4edda;
    }
    .task-pending {
        border-left-color: #ffc107;
        background-color: #fff3cd;
    }
    .task-high-priority {
        border-left-color: #dc3545;
        background-color: #f8d7da;
    }
    .credentials-box {
        background-color: #f8f9fa;
        border: 2px solid #2a5298;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .achievement-badge {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        display: inline-block;
        margin: 0.2rem;
    }
    .leaderboard-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .nav-item {
        padding: 0.5rem 1rem;
        margin: 0.2rem 0;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s;
    }
    .nav-item:hover {
        background-color: #e8f4f8;
    }
    .nav-item-active {
        background-color: #2a5298;
        color: white;
    }
    .project-timeline {
        border-left: 2px solid #2a5298;
        padding-left: 1rem;
        margin: 1rem 0;
    }
    .timeline-node {
        position: relative;
        padding: 0.5rem 0;
        padding-left: 1rem;
    }
    .timeline-node::before {
        content: "●";
        position: absolute;
        left: -1.3rem;
        color: #2a5298;
        font-size: 1.2rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# USER CREDENTIALS - Complete List
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
    "shubham@mitra.gov.in": {
        "password": sha256("Shubham@2026".encode()).hexdigest(),
        "role": "data_analyst",
        "name": "Shubham Singh",
        "team": "MITRA",
        "avatar": "👨‍💻"
    },
    "sneha@mu.edu": {
        "password": sha256("Sneha@2026".encode()).hexdigest(),
        "role": "data_analyst",
        "name": "Sneha Kashitkar",
        "team": "Mumbai University",
        "avatar": "👩‍🎓"
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
DOCUMENTS_FILE = "documents.json"

# ============================================================
# TASK GENERATION FUNCTIONS
# ============================================================

def generate_monthly_tasks():
    """Generate unique tasks for each working day"""
    all_tasks = {}
    
    # June 2026
    june_tasks = {
        "2026-06-08": "Conduct kickoff meeting with Mumbai University VC and IQAC team",
        "2026-06-09": "Interview 10 faculty members for research assessment",
        "2026-06-10": "Collect and verify student enrollment data",
        "2026-06-11": "Document faculty publication records for last 5 years",
        "2026-06-12": "Compile research grants and project funding data",
        "2026-06-15": "Analyze placement data and graduate outcomes",
        "2026-06-16": "Review library resources and digital infrastructure",
        "2026-06-17": "Assess laboratory facilities and equipment",
        "2026-06-18": "Evaluate international collaboration MoUs",
        "2026-06-19": "Prepare data gap analysis report",
        "2026-06-22": "Constitute GRDAU team with nominated members",
        "2026-06-23": "Develop standard operating procedures for GRDAU",
        "2026-06-24": "Train GRDAU staff on NIRF data collection",
        "2026-06-25": "Setup data management system with access controls",
        "2026-06-26": "Review diagnostic findings with leadership",
        "2026-06-29": "Finalize diagnostic reports for PMU submission",
        "2026-06-30": "Submit June Monthly Progress Report"
    }
    
    # July 2026
    july_tasks = {
        "2026-07-01": "Complete gap analysis against NIRF parameters",
        "2026-07-02": "Prepare SWOT analysis for Mumbai University",
        "2026-07-03": "Prepare SWOT analysis for Pune University",
        "2026-07-06": "Prepare SWOT analysis for Nagpur University",
        "2026-07-07": "Prepare SWOT analysis for Amravati University",
        "2026-07-08": "Prepare SWOT analysis for COEP University",
        "2026-07-09": "Prepare SWOT analysis for KBCNMU Jalgaon",
        "2026-07-10": "Prepare SWOT analysis for BAMU Aurangabad",
        "2026-07-13": "Finalize GRDAU establishment plan",
        "2026-07-14": "Setup GRDAU office with hardware and software",
        "2026-07-15": "Conduct data entry training for GRDAU staff",
        "2026-07-16": "Create data validation protocols",
        "2026-07-17": "Develop dashboard requirements document",
        "2026-07-20": "Design baseline report template",
        "2026-07-21": "Compile Phase 1 deliverables",
        "2026-07-22": "Present Phase 1 findings to MITRA",
        "2026-07-23": "Document lessons learned from Phase 1",
        "2026-07-24": "Plan Phase 2 activities",
        "2026-07-27": "Prepare July Monthly Progress Report",
        "2026-07-28": "Submit July MPR and Phase 1 report",
        "2026-07-29": "Incorporate client feedback",
        "2026-07-30": "Finalize Phase 2 work plan",
        "2026-07-31": "Conduct Phase 2 kickoff meeting"
    }
    
    # Add all tasks
    for date_str, task in june_tasks.items():
        all_tasks[date_str] = {"task": task, "priority": "High", "phase": "Phase 1"}
    for date_str, task in july_tasks.items():
        all_tasks[date_str] = {"task": task, "priority": "High", "phase": "Phase 1"}
    
    # Generate remaining months (simplified for demo)
    start_date = datetime(2026, 8, 3)
    end_date = datetime(2028, 4, 28)
    
    phases = [
        ("Phase 2: Planning", "IDP Development", ["Develop IDP framework", "Collect strategic plans", "Draft IDP documents", "Review with VCs", "Finalize IDPs"]),
        ("Phase 3: Implementation", "Portal & Dashboard", ["Deploy data portal", "Train GRDAU staff", "Upload baseline data", "Create dashboards", "Test functionality"]),
        ("Phase 4: Enhancement", "Analytics & Rankings", ["Implement analytics", "Prepare ranking data", "Submit to QS/THE", "Enhance dashboards", "Train users"]),
        ("Phase 5: Finalization", "Closure & Handover", ["Prepare final report", "Submit milestone 7", "Handover documentation", "Complete closure", "Celebrate success"])
    ]
    
    task_index = 0
    current_date = start_date
    
    while current_date <= end_date:
        if current_date.weekday() < 5:
            date_str = current_date.strftime("%Y-%m-%d")
            phase_idx = (task_index // 100) % len(phases)
            phase_name, phase_desc, phase_tasks = phases[phase_idx]
            task = phase_tasks[task_index % len(phase_tasks)]
            priority = "High" if "milestone" in task.lower() or "final" in task.lower() else "Medium"
            all_tasks[date_str] = {"task": f"{phase_name} - {task}", "priority": priority, "phase": phase_name}
            task_index += 1
        current_date += timedelta(days=1)
    
    return all_tasks

def load_tasks():
    if os.path.exists(DAILY_TASKS_FILE):
        with open(DAILY_TASKS_FILE, 'r') as f:
            return json.load(f)
    tasks = generate_monthly_tasks()
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
                        "remarks": "Completed - Initial project setup"
                    }
    
    save_completions(completions)
    
    # Initialize achievements
    achievements = load_achievements()
    for email, user in USERS.items():
        if user.get("role") == "data_analyst" and email not in achievements:
            achievements[email] = {"badges": [], "points": 0, "level": 1}
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
                "task": task_info.get("task", "No task"),
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
    
    # Update achievements
    achievements = load_achievements()
    if email not in achievements:
        achievements[email] = {"badges": [], "points": 0, "level": 1}
    
    user_tasks = get_user_tasks(email)
    completed_count = sum(1 for t in user_tasks if t["status"] == "Completed" and t["date"] > "2026-06-05")
    achievements[email]["points"] = completed_count * 10
    
    # Award badges
    if completed_count >= 5 and "Rising Star" not in achievements[email]["badges"]:
        achievements[email]["badges"].append("Rising Star")
        add_notification(email, "🏅 Badge Earned", "You earned the Rising Star badge!")
    if completed_count >= 15 and "Dedicated Worker" not in achievements[email]["badges"]:
        achievements[email]["badges"].append("Dedicated Worker")
        add_notification(email, "🏅 Badge Earned", "You earned the Dedicated Worker badge!")
    if completed_count >= 30 and "Task Master" not in achievements[email]["badges"]:
        achievements[email]["badges"].append("Task Master")
        add_notification(email, "🏅 Badge Earned", "You earned the Task Master badge!")
    
    save_achievements(achievements)
    add_notification(email, "✅ Task Completed", f"Task on {date_str} marked as complete!")
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
            user_achievements = achievements.get(email, {"badges": [], "points": 0})
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

def get_team_summary():
    progress_df = get_all_analysts_progress()
    if progress_df.empty:
        return pd.DataFrame()
    team_summary = progress_df.groupby("team").agg({
        "completed": "sum",
        "total": "first",
        "points": "sum"
    }).reset_index()
    team_summary["progress"] = round((team_summary["completed"] / team_summary["total"] * 100), 1)
    return team_summary

def generate_mpr_html(year, month):
    month_names = ["January", "February", "March", "April", "May", "June", 
                   "July", "August", "September", "October", "November", "December"]
    month_name = month_names[month-1]
    progress_df = get_all_analysts_progress()
    team_summary = get_team_summary()
    
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

<div class="section-title">2. Team-wise Summary</div>
<table>
    <tr><th>Team</th><th>Tasks Completed</th><th>Progress</th><th>Total Points</th></tr>
    {''.join([f'<tr><td>{row["team"]}</td><td>{row["completed"]}</td><td>{row["progress"]}%</td><td>{row["points"]}</td></tr>' for _, row in team_summary.iterrows()])}
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
        <p><strong>Password for all accounts:</strong> <code>Name@2026</code></p>
        <table style="width:100%; font-size:12px;">
            <tr><th>Role</th><th>Email</th><th>Password</th></tr>
            <tr><td>🔴 Admin</td><td>admin@mahastride.com</td><td>Admin@2026</td></tr>
            <tr><td>🔵 Project Lead</td><td>projectlead@mahastride.com</td><td>ProjectLead@2026</td></tr>
            <tr><td>🟢 Data Analyst</td><td>sneha@mu.edu</td><td>Sneha@2026</td></tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# DATA ANALYST DASHBOARD
# ============================================================

def data_analyst_dashboard(email, user):
    st.markdown(f"## {user.get('avatar')} My Tasks - {user.get('name')}")
    st.markdown(f"**Team:** {user.get('team', 'N/A')}")
    st.markdown("**Working Hours:** 10:00 AM - 6:00 PM (Monday to Friday)")
    
    user_tasks = get_user_tasks(email)
    achievements = load_achievements().get(email, {"badges": [], "points": 0})
    notifications = load_notifications().get(email, [])
    
    pending_tasks = [t for t in user_tasks if t["date"] > "2026-06-05" and t["status"] == "Pending"]
    completed_tasks = [t for t in user_tasks if t["date"] > "2026-06-05" and t["status"] == "Completed"]
    initial_completed = [t for t in user_tasks if t["date"] <= "2026-06-05"]
    
    # Stats row
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("📅 Total Tasks", len(user_tasks))
    with col2:
        st.metric("✅ Initial Completed", len(initial_completed))
    with col3:
        st.metric("✅ Your Completed", len(completed_tasks))
    with col4:
        st.metric("⏳ Pending", len(pending_tasks))
    with col5:
        st.metric("🏆 Points", achievements.get("points", 0))
    
    # Badges
    if achievements.get("badges"):
        st.markdown("### 🎖️ Your Badges")
        cols = st.columns(len(achievements["badges"]))
        for idx, badge in enumerate(achievements["badges"]):
            with cols[idx]:
                st.markdown(f'<div class="achievement-badge">🏅 {badge}</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Today's task
    today = datetime.now().strftime("%Y-%m-%d")
    today_task = next((t for t in user_tasks if t["date"] == today and t["date"] > "2026-06-05"), None)
    
    if today_task:
        st.subheader("📌 Today's Task")
        if today_task["status"] == "Completed":
            st.markdown(f"""
            <div class="task-card task-completed">
                ✅ <strong>COMPLETED</strong><br>
                <strong>Task:</strong> {today_task['task']}<br>
                <strong>Phase:</strong> {today_task.get('phase', 'N/A')}
            </div>
            """, unsafe_allow_html=True)
        else:
            with st.form(key="complete_today_task"):
                priority_class = "task-high-priority" if today_task["priority"] == "High" else "task-pending"
                st.markdown(f"""
                <div class="task-card {priority_class}">
                    <strong>⏳ TASK TO COMPLETE TODAY</strong><br>
                    <strong>Task:</strong> {today_task['task']}<br>
                    <strong>Phase:</strong> {today_task.get('phase', 'N/A')}<br>
                    <strong>Priority:</strong> {today_task['priority']}
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
    
    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📅 Upcoming Tasks", "📊 My Progress", "🏆 Leaderboard", "🔔 Notifications"])
    
    with tab1:
        st.subheader("Upcoming Tasks")
        for task in pending_tasks[:15]:
            priority_icon = "🔴" if task["priority"] == "High" else "🟡"
            st.markdown(f"{priority_icon} **{task['date']}** - {task['task'][:100]}")
    
    with tab2:
        st.subheader("My Progress")
        total_future = len(pending_tasks) + len(completed_tasks)
        progress_pct = (len(completed_tasks) / total_future * 100) if total_future > 0 else 0
        st.progress(progress_pct / 100)
        st.caption(f"{len(completed_tasks)}/{total_future} tasks completed ({progress_pct:.1f}%)")
        
        # Monthly chart
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
    team_summary = get_team_summary()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""<div class="stat-card"><div class="metric-value">{len(all_tasks)}</div><div class="metric-label">Total Working Days</div></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="stat-card"><div class="metric-value">{len([d for d in all_tasks.keys() if d <= "2026-06-05"])}</div><div class="metric-label">Initial Completed</div></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class="stat-card"><div class="metric-value">{len([u for u in USERS.values() if u.get("role") == "data_analyst"])}</div><div class="metric-label">Team Members</div></div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""<div class="stat-card"><div class="metric-value">{sum(len(c) for c in completions.values())}</div><div class="metric-label">Total Completions</div></div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Team Performance", "🏆 Leaderboard", "📄 Reports", "📈 Analytics"])
    
    with tab1:
        fig = px.bar(progress_df, x="name", y="progress", color="team", text="progress", height=500)
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(team_summary, use_container_width=True, hide_index=True)
        st.dataframe(progress_df[["name", "team", "completed", "progress", "points", "badges"]], use_container_width=True, hide_index=True)
    
    with tab2:
        for idx, (_, row) in enumerate(progress_df.head(10).iterrows()):
            medal = "🥇" if idx == 0 else "🥈" if idx == 1 else "🥉" if idx == 2 else f"{idx+1}."
            st.markdown(f"""
            <div class="leaderboard-card">
                <strong>{medal} {row['avatar']} {row['name']}</strong> - {row['team']}<br>
                ✅ Completed: {row['completed']} | 📊 Progress: {row['progress']}% | 🏆 Points: {row['points']} | 🎖️ Badges: {row['badges']}
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
        col1, col2 = st.columns(2)
        with col1:
            fig = px.histogram(progress_df, x="progress", nbins=20, title="Progress Distribution")
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.scatter(progress_df, x="progress", y="points", size="badges", color="team", text="name", title="Points vs Progress")
            st.plotly_chart(fig, use_container_width=True)

def project_lead_dashboard():
    st.markdown("## 👨‍💼 Project Lead Dashboard")
    st.markdown("**Dr. Harshal Kotwal** - ICARE Project Director")
    
    progress_df = get_all_analysts_progress()
    all_tasks = load_tasks()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📅 Total Working Days", len(all_tasks))
    with col2:
        st.metric("👥 Team Members", len(progress_df))
    with col3:
        avg_progress = progress_df["progress"].mean() if not progress_df.empty else 0
        st.metric("📈 Average Progress", f"{avg_progress:.1f}%")
    
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["📊 Team Performance", "🏆 Leaderboard", "📄 Reports"])
    
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
            <h1>🎯 MahaSTRIDE Enterprise Project Management</h1>
            <p>24-Month Task Management | Gamification | Analytics | Reports</p>
            <p>Monday to Friday | 10:00 AM - 6:00 PM</p>
            <p>✅ May 4 to June 5, 2026: COMPLETED | June 8, 2026 onwards: PENDING</p>
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
    
    # Sidebar Navigation with expanded options
    with st.sidebar:
        st.markdown(f"## {user_info.get('avatar', '📋')} MahaSTRIDE")
        st.markdown(f"**Welcome, {user_info.get('name')}**")
        if role == "data_analyst":
            st.markdown(f"*Team: {user_info.get('team', 'N/A')}*")
        st.markdown(f"*Role: {role.upper()}*")
        st.markdown("---")
        
        # Main navigation
        if role == "admin":
            nav_options = {
                "📊 Dashboard": "dashboard",
                "👥 Team Management": "team",
                "📄 Reports": "reports",
                "📈 Analytics": "analytics",
                "⚙️ Settings": "settings"
            }
        elif role == "project_lead":
            nav_options = {
                "📊 Dashboard": "dashboard",
                "👥 Team Performance": "team",
                "📄 Reports": "reports",
                "📈 Insights": "insights",
                "📋 Task Overview": "tasks"
            }
        else:
            nav_options = {
                "📝 My Tasks": "mytasks",
                "🏆 Achievements": "achievements",
                "📊 Analytics": "analytics",
                "📅 Calendar": "calendar",
                "🔔 Notifications": "notifications"
            }
        
        selected_nav = st.radio("Navigation", list(nav_options.keys()), label_visibility="collapsed")
        selected_key = nav_options[selected_nav]
        
        st.markdown("---")
        
        # Quick stats for data analyst
        if role == "data_analyst":
            user_tasks = get_user_tasks(email)
            completed = sum(1 for t in user_tasks if t["status"] == "Completed" and t["date"] > "2026-06-05")
            total = len([t for t in user_tasks if t["date"] > "2026-06-05"])
            if total > 0:
                st.markdown("### 📊 Your Stats")
                st.progress(completed/total)
                st.caption(f"Progress: {completed}/{total} ({int(completed/total*100)}%)")
        
        st.markdown("---")
        st.markdown("ℹ️ **Info**")
        st.markdown("🕐 **Hours:** 10 AM - 6 PM")
        st.markdown("📅 **Days:** Monday to Friday")
        st.markdown("✅ **May 4 - June 5:** COMPLETED")
        
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()
    
    # Main content based on role and selection
    if role == "admin":
        if selected_key == "dashboard":
            admin_dashboard()
        elif selected_key == "team":
            st.markdown("## 👥 Team Management")
            progress_df = get_all_analysts_progress()
            st.dataframe(progress_df, use_container_width=True, hide_index=True)
            
            # Add team management features
            st.subheader("Add New Team Member")
            col1, col2 = st.columns(2)
            with col1:
                new_name = st.text_input("Name")
                new_email = st.text_input("Email")
            with col2:
                new_team = st.selectbox("Team", ["MITRA", "Mumbai University", "SPPU Pune", "COEP Pune", "Amravati University", "Nagpur University", "KBCNMU Jalgaon", "BAMU Aurangabad"])
                new_role = st.selectbox("Role", ["data_analyst", "project_lead"])
            if st.button("Add Member"):
                st.success(f"Team member {new_name} added successfully!")
        elif selected_key == "reports":
            st.markdown("## 📄 Reports")
            col1, col2 = st.columns(2)
            with col1:
                report_year = st.selectbox("Year", [2026, 2027, 2028])
            with col2:
                report_month = st.selectbox("Month", range(1, 13), format_func=lambda x: ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"][x-1])
            if st.button("Generate Report"):
                html = generate_mpr_html(report_year, report_month)
                st.markdown(get_download_link(html, f"MPR_{report_year}_{report_month}.html"), unsafe_allow_html=True)
        elif selected_key == "analytics":
            st.markdown("## 📈 Advanced Analytics")
            progress_df = get_all_analysts_progress()
            fig = px.scatter(progress_df, x="progress", y="points", size="badges", color="team", text="name", title="Performance Analysis")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown("## ⚙️ Settings")
            st.info("System settings and configurations")
    
    elif role == "project_lead":
        if selected_key == "dashboard":
            project_lead_dashboard()
        elif selected_key == "team":
            st.markdown("## 👥 Team Performance")
            progress_df = get_all_analysts_progress()
            for _, row in progress_df.iterrows():
                st.markdown(f"**{row['name']}** - {row['team']}")
                st.progress(row['progress']/100)
                st.caption(f"{row['completed']}/{row['total']} tasks completed ({row['progress']}%)")
                st.markdown("---")
        elif selected_key == "reports":
            st.markdown("## 📄 Reports")
            col1, col2 = st.columns(2)
            with col1:
                report_year = st.selectbox("Year", [2026, 2027, 2028])
            with col2:
                report_month = st.selectbox("Month", range(1, 13), format_func=lambda x: ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"][x-1])
            if st.button("Generate Report"):
                html = generate_mpr_html(report_year, report_month)
                st.markdown(get_download_link(html, f"MPR_{report_year}_{report_month}.html"), unsafe_allow_html=True)
        elif selected_key == "insights":
            st.markdown("## 📈 Project Insights")
            progress_df = get_all_analysts_progress()
            avg_progress = progress_df["progress"].mean() if not progress_df.empty else 0
            st.metric("Average Team Progress", f"{avg_progress:.1f}%")
            total_points = progress_df["points"].sum() if not progress_df.empty else 0
            st.metric("Total Team Points", total_points)
        else:
            st.markdown("## 📋 Task Overview")
            all_tasks = load_tasks()
            st.dataframe(pd.DataFrame(list(all_tasks.items()), columns=["Date", "Task Info"]), use_container_width=True)
    
    else:  # data_analyst
        if selected_key == "mytasks":
            data_analyst_dashboard(email, user_info)
        elif selected_key == "achievements":
            st.markdown(f"## 🏆 My Achievements - {user_info.get('name')}")
            achievements = load_achievements().get(email, {"badges": [], "points": 0})
            user_tasks = get_user_tasks(email)
            completed = sum(1 for t in user_tasks if t["status"] == "Completed" and t["date"] > "2026-06-05")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("🏅 Points Earned", achievements.get("points", 0))
            with col2:
                st.metric("✅ Tasks Completed", completed)
            with col3:
                st.metric("🎖️ Badges", len(achievements.get("badges", [])))
            
            if achievements.get("badges"):
                st.markdown("### 🎖️ Your Badges")
                for badge in achievements["badges"]:
                    st.markdown(f'<div class="achievement-badge">🏅 {badge}</div>', unsafe_allow_html=True)
        elif selected_key == "analytics":
            st.markdown(f"## 📊 My Analytics - {user_info.get('name')}")
            user_tasks = get_user_tasks(email)
            future_tasks = [t for t in user_tasks if t["date"] > "2026-06-05"]
            
            # Category distribution
            phase_data = {}
            for task in future_tasks:
                phase = task["phase"]
                if phase not in phase_data:
                    phase_data[phase] = {"total": 0, "completed": 0}
                phase_data[phase]["total"] += 1
                if task["status"] == "Completed":
                    phase_data[phase]["completed"] += 1
            
            if phase_data:
                df_phase = pd.DataFrame([{"Phase": k, "Completed": v["completed"], "Total": v["total"]} for k, v in phase_data.items()])
                fig = px.bar(df_phase, x="Phase", y="Completed", title="Phase-wise Completion", text="Total")
                st.plotly_chart(fig, use_container_width=True)
        elif selected_key == "calendar":
            st.markdown(f"## 📅 Calendar View - {user_info.get('name')}")
            user_tasks = get_user_tasks(email)
            for task in user_tasks:
                if task["date"] > "2026-06-05":
                    status_icon = "✅" if task["status"] == "Completed" else "⏳"
                    st.markdown(f"{status_icon} **{task['date']}** - {task['task'][:80]}")
        else:  # notifications
            st.markdown(f"## 🔔 Notifications - {user_info.get('name')}")
            notifications = load_notifications().get(email, [])
            if notifications:
                for notif in reversed(notifications):
                    st.info(f"**{notif['title']}**\n\n{notif['message']}\n\n*{notif['timestamp'][:16]}*")
            else:
                st.info("No notifications yet")

if __name__ == "__main__":
    main()
