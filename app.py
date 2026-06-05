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
    page_title="MahaSTRIDE - Advanced Project Management System",
    page_icon="📊",
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
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        margin: 0;
    }
    .metric-label {
        font-size: 0.8rem;
        opacity: 0.9;
        margin: 0;
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
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
        border-left: 4px solid #28a745;
    }
    .achievement-badge {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 0.5rem;
        border-radius: 20px;
        text-align: center;
        font-size: 0.8rem;
    }
    .leaderboard-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .notification-badge {
        background-color: #dc3545;
        color: white;
        border-radius: 50%;
        padding: 0.2rem 0.5rem;
        font-size: 0.7rem;
        margin-left: 0.5rem;
    }
    .filter-bar {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# COMPLETE USER CREDENTIALS
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
DAILY_TASKS_FILE = "daily_tasks_data.json"
TASK_COMPLETION_FILE = "task_completion_data.json"
COMMENTS_FILE = "task_comments.json"
ACHIEVEMENTS_FILE = "achievements.json"
ACTIVITY_LOG_FILE = "activity_log.json"

# ============================================================
# TASK GENERATION (Same as before - keeping it concise)
# ============================================================

def get_complete_daily_tasks():
    """Generate unique daily tasks for every working day"""
    all_tasks = {}
    
    # June 2026 tasks (detailed)
    june_tasks = {
        "2026-06-08": {"task": "Conduct faculty interviews at Mumbai University", "sub_tasks": ["Interview 5 faculty members", "Document research activities", "Record publication details"], "deliverable": "Faculty Interview Report", "category": "Data Collection", "priority": "High"},
        "2026-06-09": {"task": "Analyze research output metrics for all universities", "sub_tasks": ["Calculate h-index", "Measure citation impact", "Identify top researchers"], "deliverable": "Research Metrics Analysis", "category": "Analysis", "priority": "High"},
        "2026-06-10": {"task": "Evaluate library and lab infrastructure", "sub_tasks": ["Visit central library", "Assess lab equipment", "Check digital resources"], "deliverable": "Infrastructure Assessment", "category": "Assessment", "priority": "Medium"},
        "2026-06-11": {"task": "Assess international collaboration status", "sub_tasks": ["Review MoUs", "Document joint projects", "List visiting faculty"], "deliverable": "Collaboration Report", "category": "Assessment", "priority": "Medium"},
        "2026-06-12": {"task": "Compile all assessment findings", "sub_tasks": ["Consolidate data", "Create dashboards", "Prepare summary"], "deliverable": "Assessment Report", "category": "Analysis", "priority": "High"},
    }
    
    # Add more months as needed...
    all_tasks.update(june_tasks)
    
    # Generate future months
    current_date = datetime(2026, 6, 15)
    end_date = datetime(2028, 4, 28)
    
    task_templates = [
        "Data validation and quality check", "Prepare monthly progress report",
        "Conduct stakeholder meeting", "Update dashboard metrics",
        "Research output analysis", "Training session for staff",
        "Coordinate with university leadership", "Document best practices",
        "Review and approve deliverables", "Plan next week activities"
    ]
    
    while current_date <= end_date:
        if current_date.weekday() < 5:
            date_str = current_date.strftime("%Y-%m-%d")
            template = task_templates[hash(date_str) % len(task_templates)]
            all_tasks[date_str] = {
                "task": template,
                "sub_tasks": [f"Complete {template.lower()}", "Document progress", "Update tracker"],
                "deliverable": f"{template} Report",
                "category": "General",
                "priority": "Medium"
            }
        current_date += timedelta(days=1)
    
    return all_tasks

def load_tasks():
    if os.path.exists(DAILY_TASKS_FILE):
        with open(DAILY_TASKS_FILE, 'r') as f:
            return json.load(f)
    tasks = get_complete_daily_tasks()
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

def load_comments():
    if os.path.exists(COMMENTS_FILE):
        with open(COMMENTS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_comments(comments):
    with open(COMMENTS_FILE, 'w') as f:
        json.dump(comments, f, indent=2)

def load_achievements():
    if os.path.exists(ACHIEVEMENTS_FILE):
        with open(ACHIEVEMENTS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_achievements(achievements):
    with open(ACHIEVEMENTS_FILE, 'w') as f:
        json.dump(achievements, f, indent=2)

def load_activity_log():
    if os.path.exists(ACTIVITY_LOG_FILE):
        with open(ACTIVITY_LOG_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_activity_log(log):
    with open(ACTIVITY_LOG_FILE, 'w') as f:
        json.dump(log, f, indent=2)

def log_activity(email, action, details):
    log = load_activity_log()
    if email not in log:
        log[email] = []
    log[email].append({
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "details": details
    })
    save_activity_log(log)

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
    return len(completed_dates)

def get_user_tasks(email):
    user = USERS.get(email, {})
    all_tasks = load_tasks()
    completions = load_completions()
    user_completions = completions.get(email, {})
    comments = load_comments()
    
    user_tasks = []
    for date_str, task_info in all_tasks.items():
        if user.get("role") == "data_analyst":
            is_completed = date_str in user_completions
            completion_info = user_completions.get(date_str, {})
            task_comments = comments.get(email, {}).get(date_str, [])
            
            user_tasks.append({
                "date": date_str,
                "task": task_info.get("task", ""),
                "sub_tasks": task_info.get("sub_tasks", []),
                "deliverable": task_info.get("deliverable", ""),
                "category": task_info.get("category", ""),
                "priority": task_info.get("priority", "Medium"),
                "status": "Completed" if is_completed else "Pending",
                "completed_at": completion_info.get("completed_at", ""),
                "remarks": completion_info.get("remarks", ""),
                "comments": task_comments
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
    log_activity(email, "task_completed", f"Completed task on {date_str}")
    
    # Check and award achievements
    check_and_award_achievements(email)
    
    return True

def add_comment(email, date_str, comment):
    comments = load_comments()
    if email not in comments:
        comments[email] = {}
    if date_str not in comments[email]:
        comments[email][date_str] = []
    
    comments[email][date_str].append({
        "comment": comment,
        "timestamp": datetime.now().isoformat(),
        "user": USERS.get(email, {}).get("name", email)
    })
    save_comments(comments)
    log_activity(email, "added_comment", f"Added comment on {date_str}")
    return True

def check_and_award_achievements(email):
    achievements = load_achievements()
    if email not in achievements:
        achievements[email] = {"badges": [], "points": 0}
    
    user_tasks = get_user_tasks(email)
    completed_count = sum(1 for t in user_tasks if t["status"] == "Completed" and t["date"] > "2026-06-05")
    
    # Award badges based on milestones
    if completed_count >= 10 and "First Milestone" not in achievements[email]["badges"]:
        achievements[email]["badges"].append("First Milestone")
        achievements[email]["points"] += 100
    if completed_count >= 50 and "Dedicated Worker" not in achievements[email]["badges"]:
        achievements[email]["badges"].append("Dedicated Worker")
        achievements[email]["points"] += 500
    if completed_count >= 100 and "Task Master" not in achievements[email]["badges"]:
        achievements[email]["badges"].append("Task Master")
        achievements[email]["points"] += 1000
    
    save_achievements(achievements)

def get_all_analysts_progress():
    all_tasks = load_tasks()
    completions = load_completions()
    total_tasks = len(all_tasks)
    achievements = load_achievements()
    
    progress_data = []
    for email, user in USERS.items():
        if user.get("role") == "data_analyst":
            user_completions = completions.get(email, {})
            completed = len(user_completions)
            user_achievements = achievements.get(email, {"badges": [], "points": 0})
            
            # Calculate streak
            user_tasks = get_user_tasks(email)
            streak = calculate_streak(user_tasks)
            
            progress_data.append({
                "name": user["name"],
                "team": user.get("team", "N/A"),
                "avatar": user.get("avatar", "👤"),
                "completed": completed,
                "total": total_tasks,
                "progress": round((completed / total_tasks * 100), 1),
                "badges": len(user_achievements["badges"]),
                "points": user_achievements["points"],
                "streak": streak
            })
    
    return pd.DataFrame(progress_data).sort_values("progress", ascending=False)

def calculate_streak(user_tasks):
    """Calculate current completion streak"""
    streak = 0
    today = datetime.now().date()
    current_date = today
    
    while True:
        date_str = current_date.strftime("%Y-%m-%d")
        task = next((t for t in user_tasks if t["date"] == date_str), None)
        if task and task["status"] == "Completed":
            streak += 1
            current_date -= timedelta(days=1)
        else:
            break
    
    return streak

def get_team_summary():
    progress_df = get_all_analysts_progress()
    team_summary = progress_df.groupby("team").agg({
        "completed": "sum",
        "total": "first",
        "points": "sum",
        "streak": "mean"
    }).reset_index()
    team_summary["progress"] = round((team_summary["completed"] / team_summary["total"] * 100), 1)
    team_summary["streak"] = team_summary["streak"].round(1)
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
        .badge {{ display: inline-block; background-color: #28a745; color: white; padding: 2px 8px; border-radius: 12px; font-size: 9pt; }}
    </style>
</head>
<body>
<div class="header">
    <h2>Maharashtra Institution for Transformation (MITRA)</h2>
    <h3>Monthly Progress Report - {month_name} {year}</h3>
</div>

<div class="section-title">1. Executive Summary</div>
<table>
    <tr><th>Metric</th><th>Value</th></tr>
    <tr><td>Total Working Days</div><td>{len(load_tasks())}</div></tr>
    <tr><td>Total Task Completions</div><td>{sum(len(c) for c in load_completions().values())}</div></tr>
    <tr><td>Active Team Members</div><td>{len(progress_df)}</div></tr>
</table>

<div class="section-title">2. Team Performance Summary</div>
<table>
    <tr><th>Rank</th><th>Team Member</th><th>Team</th><th>Completed</th><th>Progress</th><th>Points</th><th>Streak</th></tr>
    {''.join([f'<tr><td>{i+1}</td><td>{row["name"]}</td><td>{row["team"]}</td><td>{row["completed"]}</td><td>{row["progress"]}%</td><td>{row["points"]}</td><td>{row["streak"]} days</td></tr>' for i, (_, row) in enumerate(progress_df.iterrows())])}
</table>

<div class="section-title">3. Team-wise Summary</div>
<table>
    <tr><th>Team</th><th>Tasks Completed</th><th>Progress</th><th>Total Points</th></tr>
    {''.join([f'<tr><td>{row["team"]}</td><td>{row["completed"]}</td><td>{row["progress"]}%</td><td>{row["points"]}</td></tr>' for _, row in team_summary.iterrows()])}
</table>

<div class="section-title">4. Top Achievers</div>
<table>
    <tr><th>Rank</th><th>Team Member</th><th>Badges Earned</th><th>Points</th></tr>
    {''.join([f'<tr><td>{i+1}</td><td>{row["name"]}</td><td>{row["badges"]}</td><td>{row["points"]}</td></tr>' for i, (_, row) in enumerate(progress_df.head(5).iterrows())])}
</table>

<div class="footer">Generated on {datetime.now().strftime('%d-%b-%Y %H:%M:%S')}</div>
</body>
</html>"""
    
    return html

def generate_csv_report():
    progress_df = get_all_analysts_progress()
    return progress_df.to_csv(index=False).encode('utf-8')

def get_download_link(html, filename):
    b64 = base64.b64encode(html.encode()).decode()
    return f'<a href="data:text/html;base64,{b64}" download="{filename}" style="background:#28a745;color:white;padding:10px 20px;text-decoration:none;border-radius:5px;margin:5px;display:inline-block;">📥 Download {filename}</a>'

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
# DATA ANALYST DASHBOARD (Enhanced)
# ============================================================

def data_analyst_dashboard(email, user):
    st.markdown(f"## 📝 {user.get('avatar')} My Tasks - {user.get('name')}")
    st.markdown(f"**Team:** {user.get('team', 'N/A')}")
    st.markdown("**Working Hours:** 10:00 AM - 6:00 PM (Monday to Friday)")
    
    user_tasks = get_user_tasks(email)
    achievements = load_achievements().get(email, {"badges": [], "points": 0})
    
    # Stats row
    pending_tasks = [t for t in user_tasks if t["date"] > "2026-06-05" and t["status"] == "Pending"]
    completed_tasks = [t for t in user_tasks if t["date"] > "2026-06-05" and t["status"] == "Completed"]
    initial_completed = [t for t in user_tasks if t["date"] <= "2026-06-05"]
    streak = calculate_streak(user_tasks)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("📅 Total Tasks", len(user_tasks))
    with col2:
        st.metric("✅ Completed", len(completed_tasks))
    with col3:
        st.metric("⏳ Pending", len(pending_tasks))
    with col4:
        st.metric("🔥 Streak", f"{streak} days")
    with col5:
        st.metric("🏆 Points", achievements["points"])
    
    # Achievements section
    if achievements["badges"]:
        st.markdown("### 🎖️ Your Achievements")
        cols = st.columns(min(len(achievements["badges"]), 4))
        for idx, badge in enumerate(achievements["badges"]):
            with cols[idx % 4]:
                st.markdown(f'<div class="achievement-badge">🏅 {badge}</div>', unsafe_allow_html=True)
        st.markdown("---")
    
    # Today's task with enhanced UI
    today = datetime.now().strftime("%Y-%m-%d")
    today_task = next((t for t in user_tasks if t["date"] == today and t["date"] > "2026-06-05"), None)
    
    if today_task:
        st.subheader("📌 Today's Task")
        priority_class = "task-high-priority" if today_task["priority"] == "High" else "task-pending"
        
        if today_task["status"] == "Completed":
            st.markdown(f"""
            <div class="task-card task-completed">
                ✅ <strong>COMPLETED</strong><br>
                <strong>Task:</strong> {today_task['task']}<br>
                <strong>Deliverable:</strong> {today_task['deliverable']}<br>
                <strong>Completed at:</strong> {today_task.get('completed_at', 'N/A')[:16]}
            </div>
            """, unsafe_allow_html=True)
        else:
            with st.form(key="complete_today_task"):
                st.markdown(f"""
                <div class="task-card {priority_class}">
                    <strong>⏳ TASK TO COMPLETE</strong><br>
                    <strong>Task:</strong> {today_task['task']}<br>
                    <strong>Deliverable:</strong> {today_task['deliverable']}<br>
                    <strong>Priority:</strong> {today_task['priority']}
                </div>
                """, unsafe_allow_html=True)
                
                if today_task.get('sub_tasks'):
                    st.markdown("**📋 Sub-tasks:**")
                    for stask in today_task['sub_tasks']:
                        st.checkbox(stask, key=f"subtask_{stask}")
                    st.markdown("---")
                
                col1, col2 = st.columns(2)
                with col1:
                    start_time = st.time_input("Start Time", value=datetime.strptime("10:00", "%H:%M").time())
                with col2:
                    end_time = st.time_input("End Time", value=datetime.strptime("18:00", "%H:%M").time())
                
                work_hours = f"{start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}"
                remarks = st.text_area("📝 Work Accomplished", height=100, 
                                       placeholder="Describe what you accomplished today...")
                
                col1, col2 = st.columns(2)
                with col1:
                    submitted = st.form_submit_button("✅ MARK AS COMPLETE", use_container_width=True, type="primary")
                with col2:
                    comment = st.text_input("💬 Add a comment (optional)")
                    if comment:
                        add_comment(email, today, comment)
                        st.success("Comment added!")
                
                if submitted:
                    if remarks:
                        if mark_task_complete(email, today_task["date"], remarks, work_hours):
                            st.success("🎉 Task completed! Great work!")
                            st.balloons()
                            time.sleep(1)
                            st.rerun()
                    else:
                        st.error("Please describe your work")
    
    # Search and filter
    st.markdown("---")
    st.subheader("🔍 Search & Filter Tasks")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        search_term = st.text_input("Search by task name", "")
    with col2:
        filter_status = st.selectbox("Filter by status", ["All", "Pending", "Completed"])
    with col3:
        filter_priority = st.selectbox("Filter by priority", ["All", "High", "Medium", "Low"])
    
    # Display filtered tasks
    filtered_tasks = [t for t in user_tasks if t["date"] > "2026-06-05"]
    
    if search_term:
        filtered_tasks = [t for t in filtered_tasks if search_term.lower() in t["task"].lower()]
    if filter_status != "All":
        filtered_tasks = [t for t in filtered_tasks if t["status"] == filter_status]
    if filter_priority != "All":
        filtered_tasks = [t for t in filtered_tasks if t["priority"] == filter_priority]
    
    st.markdown(f"**Showing {len(filtered_tasks)} tasks**")
    
    for task in filtered_tasks[:20]:
        status_icon = "✅" if task["status"] == "Completed" else "⏳"
        priority_color = "🔴" if task["priority"] == "High" else "🟡" if task["priority"] == "Medium" else "🟢"
        st.markdown(f"{status_icon} **{task['date']}** - {priority_color} {task['task'][:80]}")

# ============================================================
# ADMIN DASHBOARD (Enhanced)
# ============================================================

def admin_dashboard():
    st.markdown("## 📊 Admin Dashboard")
    
    all_tasks = load_tasks()
    completions = load_completions()
    progress_df = get_all_analysts_progress()
    team_summary = get_team_summary()
    activity_log = load_activity_log()
    
    # Key metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown(f"""<div class="stat-card"><div class="metric-value">{len(all_tasks)}</div><div class="metric-label">Total Working Days</div></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="stat-card"><div class="metric-value">{len([d for d in all_tasks.keys() if d <= "2026-06-05"])}</div><div class="metric-label">Initial Completed</div></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class="stat-card"><div class="metric-value">{len([u for u in USERS.values() if u.get("role") == "data_analyst"])}</div><div class="metric-label">Team Members</div></div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""<div class="stat-card"><div class="metric-value">{sum(len(c) for c in completions.values())}</div><div class="metric-label">Total Completions</div></div>""", unsafe_allow_html=True)
    with col5:
        st.markdown(f"""<div class="stat-card"><div class="metric-value">{progress_df['points'].sum() if not progress_df.empty else 0}</div><div class="metric-label">Total Points</div></div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Tabs for different views
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Team Performance", "🏆 Leaderboard", "📈 Analytics", "📄 Reports", "📋 Activity Log"])
    
    with tab1:
        st.subheader("👥 Team Progress Dashboard")
        
        fig = px.bar(progress_df, x="name", y="progress", color="team", 
                     text="progress", title="Team Member Progress (%)", height=500)
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Team-wise Summary")
        st.dataframe(team_summary, use_container_width=True, hide_index=True)
        
        st.subheader("Detailed Performance")
        st.dataframe(progress_df[["name", "team", "completed", "progress", "points", "streak"]], 
                    use_container_width=True, hide_index=True)
    
    with tab2:
        st.subheader("🏆 Top Performers Leaderboard")
        
        for idx, (_, row) in enumerate(progress_df.head(10).iterrows()):
            medal = "🥇" if idx == 0 else "🥈" if idx == 1 else "🥉" if idx == 2 else f"{idx+1}."
            st.markdown(f"""
            <div class="leaderboard-card">
                <strong>{medal} {row['name']}</strong> - {row['team']}<br>
                📊 Progress: {row['progress']}% | ✅ Completed: {row['completed']} | 🏆 Points: {row['points']} | 🔥 Streak: {row['streak']} days
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        st.subheader("📈 Advanced Analytics")
        
        col1, col2 = st.columns(2)
        with col1:
            # Progress distribution
            fig = px.histogram(progress_df, x="progress", nbins=20, title="Team Progress Distribution")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Team comparison
            fig = px.pie(team_summary, values="completed", names="team", title="Tasks by Team")
            st.plotly_chart(fig, use_container_width=True)
        
        # Points vs Progress scatter
        fig = px.scatter(progress_df, x="progress", y="points", size="streak", 
                         color="team", text="name", title="Points vs Progress Analysis")
        fig.update_traces(textposition="top center")
        st.plotly_chart(fig, use_container_width=True)
        
        # Streak heatmap
        streak_data = progress_df[["name", "streak"]].set_index("name")
        fig = px.imshow([streak_data["streak"].values], 
                        x=streak_data.index, 
                        y=["Streak Days"],
                        title="Streak Heatmap", color_continuous_scale="Greens")
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.subheader("📄 Generate Reports")
        
        col1, col2 = st.columns(2)
        with col1:
            report_year = st.selectbox("Year", [2026, 2027, 2028])
            report_month = st.selectbox("Month", range(1, 13), 
                                        format_func=lambda x: ["Jan","Feb","Mar","Apr","May","Jun",
                                                              "Jul","Aug","Sep","Oct","Nov","Dec"][x-1])
            if st.button("Generate HTML Report", use_container_width=True):
                html = generate_mpr_html(report_year, report_month)
                st.markdown(get_download_link(html, f"MPR_{report_year}_{report_month}.html"), unsafe_allow_html=True)
        
        with col2:
            if st.button("📊 Export CSV Report", use_container_width=True):
                csv = generate_csv_report()
                st.download_button("Download CSV", csv, f"team_performance_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")
    
    with tab5:
        st.subheader("📋 User Activity Log")
        
        all_activities = []
        for email, activities in activity_log.items():
            user = USERS.get(email, {})
            for act in activities:
                all_activities.append({
                    "User": user.get("name", email),
                    "Action": act["action"],
                    "Time": act["timestamp"][:16],
                    "Details": act["details"]
                })
        
        if all_activities:
            df_activities = pd.DataFrame(all_activities).sort_values("Time", ascending=False)
            st.dataframe(df_activities, use_container_width=True, hide_index=True)
        else:
            st.info("No activities logged yet")

def project_lead_dashboard():
    st.markdown("## 👨‍💼 Project Lead Dashboard")
    st.markdown("**Dr. Harshal Kotwal** - ICARE Project Director")
    
    all_tasks = load_tasks()
    progress_df = get_all_analysts_progress()
    team_summary = get_team_summary()
    
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
    
    tab1, tab2, tab3 = st.tabs(["📊 Performance", "🏆 Leaderboard", "📄 Reports"])
    
    with tab1:
        fig = px.bar(progress_df, x="name", y="progress", color="team", 
                     text="progress", title="Team Member Progress (%)", height=450)
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(progress_df[["name", "team", "completed", "progress", "points", "streak"]], 
                    use_container_width=True, hide_index=True)
    
    with tab2:
        for idx, (_, row) in enumerate(progress_df.head(5).iterrows()):
            medal = "🥇" if idx == 0 else "🥈" if idx == 1 else "🥉" if idx == 2 else f"{idx+1}."
            st.markdown(f"""
            <div class="leaderboard-card">
                <strong>{medal} {row['name']}</strong> - {row['team']}<br>
                ✅ Completed: {row['completed']} | 📊 Progress: {row['progress']}% | 🔥 Streak: {row['streak']} days
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            report_year = st.selectbox("Year", [2026, 2027, 2028])
            report_month = st.selectbox("Month", range(1, 13), 
                                        format_func=lambda x: ["Jan","Feb","Mar","Apr","May","Jun",
                                                              "Jul","Aug","Sep","Oct","Nov","Dec"][x-1])
            if st.button("Generate Report"):
                html = generate_mpr_html(report_year, report_month)
                st.markdown(get_download_link(html, f"MPR_{report_year}_{report_month}.html"), unsafe_allow_html=True)
        
        with col2:
            if st.button("Export CSV"):
                csv = generate_csv_report()
                st.download_button("Download CSV", csv, f"performance_report.csv", "text/csv")

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
            <h1>📊 MahaSTRIDE Advanced Project Management System</h1>
            <p>Complete 24-Month Task Management | Gamification | Analytics | Reports</p>
            <p>Monday to Friday | 10:00 AM - 6:00 PM</p>
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
    
    with st.sidebar:
        st.markdown(f"## {user_info.get('avatar', '📋')} MahaSTRIDE")
        st.markdown(f"**Welcome, {user_info.get('name')}**")
        if role == "data_analyst":
            st.markdown(f"*Team: {user_info.get('team', 'N/A')}*")
        st.markdown(f"*Role: {role.upper()}*")
        st.markdown("---")
        
        if role == "admin":
            nav_options = ["📊 Dashboard", "📈 Analytics", "📄 Reports"]
        elif role == "project_lead":
            nav_options = ["📊 Dashboard", "📈 Analytics", "📄 Reports"]
        else:
            nav_options = ["📝 My Tasks", "🏆 Achievements", "📊 Analytics"]
        
        selected_nav = st.radio("Navigation", nav_options, label_visibility="collapsed")
        
        st.markdown("---")
        st.markdown("ℹ️ **Working Hours:** 10 AM - 6 PM")
        st.markdown("📅 **Working Days:** Monday to Friday")
        st.markdown("✅ **May 4 - June 5, 2026:** COMPLETED")
        
        # Show streak in sidebar for data analysts
        if role == "data_analyst":
            user_tasks = get_user_tasks(email)
            streak = calculate_streak(user_tasks)
            st.markdown(f"🔥 **Current Streak:** {streak} days")
            
            achievements = load_achievements().get(email, {})
            if achievements.get("badges"):
                st.markdown(f"🏅 **Badges:** {len(achievements['badges'])}")
        
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()
    
    if role == "admin":
        if selected_nav == "📊 Dashboard":
            admin_dashboard()
        elif selected_nav == "📈 Analytics":
            st.markdown("## 📈 Advanced Analytics")
            progress_df = get_all_analysts_progress()
            
            col1, col2 = st.columns(2)
            with col1:
                fig = px.box(progress_df, x="team", y="progress", title="Progress Distribution by Team")
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                fig = px.scatter(progress_df, x="streak", y="progress", size="points", 
                                 color="team", text="name", title="Streak vs Progress")
                fig.update_traces(textposition="top center")
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown("## 📄 Reports")
            col1, col2 = st.columns(2)
            with col1:
                report_year = st.selectbox("Year", [2026, 2027, 2028])
                report_month = st.selectbox("Month", range(1, 13), 
                                            format_func=lambda x: ["Jan","Feb","Mar","Apr","May","Jun",
                                                                  "Jul","Aug","Sep","Oct","Nov","Dec"][x-1])
                if st.button("Generate Report"):
                    html = generate_mpr_html(report_year, report_month)
                    st.markdown(get_download_link(html, f"MPR_{report_year}_{report_month}.html"), unsafe_allow_html=True)
    
    elif role == "project_lead":
        if selected_nav == "📊 Dashboard":
            project_lead_dashboard()
        elif selected_nav == "📈 Analytics":
            st.markdown("## 📈 Performance Analytics")
            progress_df = get_all_analysts_progress()
            
            fig = px.line(progress_df.sort_values("progress"), x="name", y="progress", 
                         title="Team Progress Trend", markers=True)
            st.plotly_chart(fig, use_container_width=True)
            
            st.dataframe(progress_df[["name", "team", "completed", "progress", "streak"]], 
                        use_container_width=True, hide_index=True)
        else:
            st.markdown("## 📄 Reports")
            col1, col2 = st.columns(2)
            with col1:
                report_year = st.selectbox("Year", [2026, 2027, 2028])
                report_month = st.selectbox("Month", range(1, 13), 
                                            format_func=lambda x: ["Jan","Feb","Mar","Apr","May","Jun",
                                                                  "Jul","Aug","Sep","Oct","Nov","Dec"][x-1])
                if st.button("Generate Report"):
                    html = generate_mpr_html(report_year, report_month)
                    st.markdown(get_download_link(html, f"MPR_{report_year}_{report_month}.html"), unsafe_allow_html=True)
    
    else:
        if selected_nav == "📝 My Tasks":
            data_analyst_dashboard(email, user_info)
        elif selected_nav == "🏆 Achievements":
            st.markdown("## 🏆 My Achievements & Rewards")
            achievements = load_achievements().get(email, {"badges": [], "points": 0})
            user_tasks = get_user_tasks(email)
            completed = sum(1 for t in user_tasks if t["status"] == "Completed" and t["date"] > "2026-06-05")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("🏅 Points Earned", achievements["points"])
            with col2:
                st.metric("✅ Tasks Completed", completed)
            with col3:
                streak = calculate_streak(user_tasks)
                st.metric("🔥 Current Streak", f"{streak} days")
            
            if achievements["badges"]:
                st.markdown("### 🎖️ Badges Earned")
                cols = st.columns(min(len(achievements["badges"]), 4))
                for idx, badge in enumerate(achievements["badges"]):
                    with cols[idx % 4]:
                        st.markdown(f'<div class="achievement-badge">🏅 {badge}</div>', unsafe_allow_html=True)
            else:
                st.info("Complete more tasks to earn badges!")
            
            # Next milestones
            st.markdown("### 🎯 Next Milestones")
            if completed < 10:
                st.progress(completed/10)
                st.caption(f"{completed}/10 tasks - Next: First Milestone badge (100 points)")
            elif completed < 50:
                st.progress(completed/50)
                st.caption(f"{completed}/50 tasks - Next: Dedicated Worker badge (500 points)")
            else:
                st.progress(min(completed/100, 1))
                st.caption(f"{completed}/100 tasks - Next: Task Master badge (1000 points)")
        else:
            st.markdown("## 📊 My Analytics")
            user_tasks = get_user_tasks(email)
            
            # Monthly completion chart
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
                df_monthly = pd.DataFrame([
                    {"Month": k, "Completed": v["completed"], "Total": v["total"]}
                    for k, v in monthly_data.items()
                ])
                fig = px.bar(df_monthly, x="Month", y="Completed", title="Monthly Completion", text="Total")
                st.plotly_chart(fig, use_container_width=True)
                
                # Category breakdown
                category_data = {}
                for task in user_tasks:
                    if task["date"] > "2026-06-05" and task["status"] == "Completed":
                        cat = task["category"]
                        category_data[cat] = category_data.get(cat, 0) + 1
                
                if category_data:
                    fig = px.pie(values=list(category_data.values()), names=list(category_data.keys()), 
                                 title="Completed Tasks by Category")
                    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
