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
</style>
""", unsafe_allow_html=True)

# ============================================================
# COMPLETE USER CREDENTIALS - ALL 11 DATA ANALYSTS
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
ACHIEVEMENTS_FILE = "achievements_data.json"

# ============================================================
# TASK GENERATION FUNCTIONS
# ============================================================

def generate_tasks_for_date(date):
    """Generate a unique task for a specific date"""
    date_str = date.strftime("%Y-%m-%d")
    month = date.month
    year = date.year
    
    # Task templates organized by month
    task_templates = {
        (2026, 6): [
            "Conduct kickoff meeting with university VC and IQAC team",
            "Interview faculty members for research assessment",
            "Collect student enrollment and demographic data",
            "Document faculty publication records and citations",
            "Compile research grants and funded projects data",
            "Analyze placement statistics and graduate outcomes",
            "Review library resources and digital infrastructure",
            "Assess laboratory facilities and equipment availability",
            "Evaluate international collaboration MoUs",
            "Prepare comprehensive data gap analysis report"
        ],
        (2026, 7): [
            "Constitute GRDAU team with nominated members",
            "Develop standard operating procedures for GRDAU",
            "Train GRDAU staff on NIRF data collection",
            "Setup data management system with access controls",
            "Review diagnostic findings with university leadership",
            "Finalize diagnostic reports for PMU submission",
            "Complete gap analysis against NIRF parameters",
            "Prepare SWOT analysis report",
            "Finalize GRDAU establishment plan",
            "Setup GRDAU office with hardware and software"
        ],
        (2026, 8): [
            "Develop IDP framework aligned with NIRF metrics",
            "Collect strategic plans from university leadership",
            "Analyze collected strategic plans for common themes",
            "Draft Institutional Development Plan with KPIs",
            "Present IDP draft to VC for feedback",
            "Incorporate VC feedback and finalize IDP",
            "Get institutional sign-off on approved IDP",
            "Design data portal architecture and schema",
            "Create dashboard wireframes and mockups",
            "Setup development environment and version control"
        ],
        (2026, 9): [
            "Develop backend APIs for data integration",
            "Implement user authentication and role-based access",
            "Build KPI dashboard with metric cards",
            "Integrate research output visualization charts",
            "Add faculty-student ratio analytics dashboard",
            "Implement financial resource utilization tracking",
            "Develop placement and graduate outcomes dashboard",
            "Create international collaboration metrics",
            "Add citation analysis and publication impact",
            "Implement infrastructure assessment dashboard"
        ],
        (2026, 10): [
            "Prepare Milestone Report with evidence",
            "Submit milestone report to PMU for review",
            "Conduct user acceptance testing with coordinators",
            "Fix bugs and optimize dashboard performance",
            "Deploy dashboard beta version to staging",
            "Complete dashboard beta testing with all universities",
            "Finalize dashboard based on user feedback",
            "Conduct dashboard training for administrators",
            "Create comprehensive user manual and tutorials",
            "Prepare Mid-Term Review presentation"
        ]
    }
    
    # Default template for other months
    if (year, month) in task_templates:
        templates = task_templates[(year, month)]
    else:
        templates = [
            f"Continue {['data analysis', 'report preparation', 'stakeholder coordination', 'dashboard enhancement', 'training delivery'][date.day % 5]} activities",
            f"Complete {['milestone', 'progress report', 'data validation', 'quality check', 'documentation'][date.day % 5]} tasks",
            f"Coordinate with {['VC office', 'IQAC', 'GRDAU team', 'department heads', 'IT team'][date.day % 5]}",
            f"Prepare {['monthly report', 'presentation', 'dashboard update', 'data summary', 'status update'][date.day % 5]}"
        ]
    
    # Select task based on day of month
    task_index = (date.day - 1) % len(templates)
    task = templates[task_index]
    
    # Add phase indicator
    if year == 2026 and month <= 7:
        phase = "Phase 1: Foundation"
    elif year == 2026 and month <= 10:
        phase = "Phase 2: Planning"
    elif year == 2026 or (year == 2027 and month <= 4):
        phase = "Phase 3: Implementation"
    elif year == 2027 and month <= 10:
        phase = "Phase 4: Enhancement"
    else:
        phase = "Phase 5: Finalization"
    
    # Determine priority
    priority = "High" if any(word in task.lower() for word in ["milestone", "submit", "present", "final", "vc", "ceo"]) else "Medium"
    
    return {
        "task": task,
        "priority": priority,
        "phase": phase
    }

def get_all_working_dates():
    """Get all working dates from May 4, 2026 to April 28, 2028"""
    dates = []
    start_date = datetime(2026, 5, 4)
    end_date = datetime(2028, 4, 28)
    
    current = start_date
    while current <= end_date:
        if current.weekday() < 5:  # Monday to Friday
            dates.append(current)
        current += timedelta(days=1)
    return dates

def load_tasks():
    if os.path.exists(DAILY_TASKS_FILE):
        with open(DAILY_TASKS_FILE, 'r') as f:
            return json.load(f)
    
    # Generate tasks for all working days
    tasks = {}
    for date in get_all_working_dates():
        date_str = date.strftime("%Y-%m-%d")
        tasks[date_str] = generate_tasks_for_date(date)
    
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

def initialize_completed_tasks():
    """Mark May 4 to June 5, 2026 as completed for all data analysts"""
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
                        "remarks": "Completed - Initial project setup phase (May 4 to June 5, 2026)"
                    }
    
    save_completions(completions)
    
    # Initialize achievements
    achievements = load_achievements()
    for email, user in USERS.items():
        if user.get("role") == "data_analyst" and email not in achievements:
            achievements[email] = {"badges": [], "points": 0}
    save_achievements(achievements)
    
    return len(completed_dates)

def get_user_tasks(email):
    """Get tasks for a specific user"""
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
    
    # Update achievements
    achievements = load_achievements()
    if email not in achievements:
        achievements[email] = {"badges": [], "points": 0}
    
    user_tasks = get_user_tasks(email)
    completed_count = sum(1 for t in user_tasks if t["status"] == "Completed" and t["date"] > "2026-06-05")
    
    achievements[email]["points"] = completed_count * 10
    
    # Award badges
    new_badges = []
    if completed_count >= 5 and "Rising Star" not in achievements[email]["badges"]:
        new_badges.append("Rising Star")
    if completed_count >= 15 and "Dedicated Worker" not in achievements[email]["badges"]:
        new_badges.append("Dedicated Worker")
    if completed_count >= 30 and "Task Master" not in achievements[email]["badges"]:
        new_badges.append("Task Master")
    if completed_count >= 50 and "Elite Performer" not in achievements[email]["badges"]:
        new_badges.append("Elite Performer")
    
    achievements[email]["badges"].extend(new_badges)
    save_achievements(achievements)
    
    return True

def get_all_analysts_progress():
    """Get progress for all data analysts"""
    all_tasks = load_tasks()
    completions = load_completions()
    achievements = load_achievements()
    total_tasks = len(all_tasks)
    future_tasks = len([d for d in all_tasks.keys() if d > "2026-06-05"])
    
    progress_data = []
    for email, user in USERS.items():
        if user.get("role") == "data_analyst":
            user_completions = completions.get(email, {})
            completed_future = sum(1 for d in user_completions.keys() if d > "2026-06-05")
            completed_total = len(user_completions)
            user_achievements = achievements.get(email, {"badges": [], "points": 0})
            
            progress_data.append({
                "name": user["name"],
                "team": user.get("team", "N/A"),
                "avatar": user.get("avatar", "👤"),
                "completed_total": completed_total,
                "completed_future": completed_future,
                "total_future": future_tasks,
                "total_all": total_tasks,
                "progress_future": round((completed_future / future_tasks * 100), 1) if future_tasks > 0 else 0,
                "progress_overall": round((completed_total / total_tasks * 100), 1),
                "points": user_achievements.get("points", 0),
                "badges": len(user_achievements.get("badges", []))
            })
    
    return pd.DataFrame(progress_data).sort_values("progress_future", ascending=False)

def get_team_summary():
    progress_df = get_all_analysts_progress()
    if progress_df.empty:
        return pd.DataFrame()
    team_summary = progress_df.groupby("team").agg({
        "completed_future": "sum",
        "total_future": "first",
        "points": "sum"
    }).reset_index()
    team_summary["progress"] = round((team_summary["completed_future"] / team_summary["total_future"] * 100), 1)
    return team_summary

def generate_mpr_html(year, month):
    month_names = ["January", "February", "March", "April", "May", "June", 
                   "July", "August", "September", "October", "November", "December"]
    month_name = month_names[month-1]
    
    progress_df = get_all_analysts_progress()
    team_summary = get_team_summary()
    all_tasks = load_tasks()
    
    # Get tasks for this month
    month_tasks = {d: t for d, t in all_tasks.items() if datetime.strptime(d, "%Y-%m-%d").year == year and datetime.strptime(d, "%Y-%m-%d").month == month}
    
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

<div class="section-title">1. Executive Summary</div>
<table>
    <tr><th>Metric</th><th>Value</th></tr>
    <tr><td>Reporting Period</td><td>{month_name} {year}</td></tr>
    <tr><td>Working Days in Month</td><td>{len(month_tasks)}</td></tr>
    <tr><td>Total Working Days (Project)</td><td>{len(all_tasks)}</td></tr>
    <tr><td>Active Team Members</td><td>{len(progress_df)}</td></tr>
</table>

<div class="section-title">2. Team Performance Summary</div>
<table>
    <tr><th>Rank</th><th>Team Member</th><th>Team</th><th>Tasks Completed</th><th>Progress</th><th>Points</th><th>Badges</th></tr>
    {''.join([f'<tr><td>{i+1}</td><td>{row["name"]}</td><td>{row["team"]}</td><td>{row["completed_future"]}</td><td>{row["progress_future"]}%</td><td>{row["points"]}</td><td>{row["badges"]}</td></tr>' for i, (_, row) in enumerate(progress_df.head(10).iterrows())])}
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
            <tr><td style="background:#dc3545;color:white;">Admin</td><td>admin@mahastride.com</td><td>Admin@2026</td></tr>
            <tr><td style="background:#17a2b8;color:white;">Project Lead</td><td>projectlead@mahastride.com</td><td>ProjectLead@2026</td></tr>
            <tr><td style="background:#28a745;color:white;">Data Analyst</td><td>sneha@mu.edu</td><td>Sneha@2026</td></tr>
            <tr><td style="background:#28a745;color:white;">Data Analyst</td><td>shubham@mitra.gov.in</td><td>Shubham@2026</td></tr>
        </table>
        <p style="margin-top:10px;"><small>Other data analysts: sagar@mu.edu, jagan@sspu.edu, vaibhav@coep.edu, pratham@au.edu, anjali@nu.edu, nitish@kbcnmu.edu, atharv@bamu.edu (Password: Name@2026)</small></p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# DATA ANALYST DASHBOARD
# ============================================================

def data_analyst_dashboard(email, user):
    st.markdown(f"## {user.get('avatar', '📝')} My Tasks - {user.get('name')}")
    st.markdown(f"**Team:** {user.get('team', 'N/A')}")
    st.markdown("**Working Hours:** 10:00 AM - 6:00 PM (Monday to Friday)")
    
    user_tasks = get_user_tasks(email)
    achievements = load_achievements().get(email, {"badges": [], "points": 0})
    
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
        cols = st.columns(min(len(achievements["badges"]), 5))
        for idx, badge in enumerate(achievements["badges"]):
            with cols[idx % 5]:
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
                <strong>Phase:</strong> {today_task.get('phase', 'N/A')}<br>
                <strong>Completed:</strong> {today_task.get('completed_at', 'N/A')[:16] if today_task.get('completed_at') else 'N/A'}
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
                remarks = st.text_area("📝 Work Accomplished", height=100, 
                                      placeholder="Describe what you accomplished today...")
                
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
    tab1, tab2, tab3 = st.tabs(["📅 Upcoming Tasks", "📊 My Progress", "🏆 Leaderboard"])
    
    with tab1:
        st.subheader("Upcoming Tasks (Next 20)")
        for task in pending_tasks[:20]:
            priority_icon = "🔴" if task["priority"] == "High" else "🟡"
            st.markdown(f"{priority_icon} **{task['date']}** - {task['task'][:100]}")
    
    with tab2:
        st.subheader("My Progress")
        
        # Progress gauge
        total_future = len(pending_tasks) + len(completed_tasks)
        progress_pct = (len(completed_tasks) / total_future * 100) if total_future > 0 else 0
        st.progress(progress_pct / 100)
        st.caption(f"{len(completed_tasks)}/{total_future} tasks completed ({progress_pct:.1f}%)")
        
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
                📊 Progress: {row['progress_future']}% | ✅ Completed: {row['completed_future']} | 🏆 Points: {row['points']} | 🎖️ Badges: {row['badges']}
            </div>
            """, unsafe_allow_html=True)

# ============================================================
# ADMIN DASHBOARD
# ============================================================

def admin_dashboard():
    st.markdown("## 📊 Admin Dashboard")
    
    all_tasks = load_tasks()
    completions = load_completions()
    progress_df = get_all_analysts_progress()
    team_summary = get_team_summary()
    
    # Key metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown(f"""<div class="stat-card"><div class="metric-value">{len(all_tasks)}</div><div class="metric-label">Total Working Days</div></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="stat-card"><div class="metric-value">{len([d for d in all_tasks.keys() if d <= "2026-06-05"])}</div><div class="metric-label">Initial Completed</div></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class="stat-card"><div class="metric-value">{len([u for u in USERS.values() if u.get("role") == "data_analyst"])}</div><div class="metric-label">Team Members</div></div>""", unsafe_allow_html=True)
    with col4:
        total_completions = sum(len(c) for c in completions.values())
        st.markdown(f"""<div class="stat-card"><div class="metric-value">{total_completions}</div><div class="metric-label">Total Completions</div></div>""", unsafe_allow_html=True)
    with col5:
        total_points = progress_df["points"].sum() if not progress_df.empty else 0
        st.markdown(f"""<div class="stat-card"><div class="metric-value">{total_points}</div><div class="metric-label">Total Points</div></div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Team Performance", "🏆 Leaderboard", "📄 Reports", "📈 Analytics"])
    
    with tab1:
        st.subheader("Team Progress Dashboard")
        
        if not progress_df.empty:
            fig = px.bar(progress_df, x="name", y="progress_future", color="team", 
                         text="progress_future", title="Team Progress (%) - Tasks from June 8 onwards", height=500)
            fig.update_traces(textposition="outside")
            st.plotly_chart(fig, use_container_width=True)
        
        if not team_summary.empty:
            st.subheader("Team-wise Summary")
            st.dataframe(team_summary, use_container_width=True, hide_index=True)
        
        st.subheader("Detailed Performance")
        if not progress_df.empty:
            st.dataframe(progress_df[["name", "team", "completed_future", "total_future", "progress_future", "points", "badges"]], 
                        use_container_width=True, hide_index=True)
    
    with tab2:
        st.subheader("🏆 Top Performers Leaderboard")
        if not progress_df.empty:
            for idx, (_, row) in enumerate(progress_df.head(10).iterrows()):
                medal = "🥇" if idx == 0 else "🥈" if idx == 1 else "🥉" if idx == 2 else f"{idx+1}."
                st.markdown(f"""
                <div class="leaderboard-card">
                    <strong>{medal} {row['avatar']} {row['name']}</strong> - {row['team']}<br>
                    📊 Progress: {row['progress_future']}% | ✅ Completed: {row['completed_future']} | 🏆 Points: {row['points']} | 🎖️ Badges: {row['badges']}
                </div>
                """, unsafe_allow_html=True)
    
    with tab3:
        st.subheader("Generate Monthly Progress Report")
        col1, col2 = st.columns(2)
        with col1:
            report_year = st.selectbox("Year", [2026, 2027, 2028])
        with col2:
            report_month = st.selectbox("Month", range(1, 13), 
                                        format_func=lambda x: ["Jan","Feb","Mar","Apr","May","Jun",
                                                              "Jul","Aug","Sep","Oct","Nov","Dec"][x-1])
        if st.button("Generate HTML Report", use_container_width=True):
            html = generate_mpr_html(report_year, report_month)
            st.markdown(get_download_link(html, f"MPR_{report_year}_{report_month}.html"), unsafe_allow_html=True)
    
    with tab4:
        st.subheader("Advanced Analytics")
        
        if not progress_df.empty:
            col1, col2 = st.columns(2)
            with col1:
                fig = px.histogram(progress_df, x="progress_future", nbins=20, title="Team Progress Distribution")
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                fig = px.scatter(progress_df, x="progress_future", y="points", size="badges", 
                                 color="team", text="name", title="Points vs Progress")
                st.plotly_chart(fig, use_container_width=True)

def project_lead_dashboard():
    st.markdown("## 👨‍💼 Project Lead Dashboard")
    st.markdown("**Dr. Harshal Kotwal** - ICARE Project Director")
    
    progress_df = get_all_analysts_progress()
    team_summary = get_team_summary()
    all_tasks = load_tasks()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📅 Total Working Days", len(all_tasks))
    with col2:
        st.metric("👥 Team Members", len(progress_df))
    with col3:
        avg_progress = progress_df["progress_future"].mean() if not progress_df.empty else 0
        st.metric("📈 Avg Team Progress", f"{avg_progress:.1f}%")
    with col4:
        total_points = progress_df["points"].sum() if not progress_df.empty else 0
        st.metric("🏆 Total Points", total_points)
    
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["📊 Team Performance", "🏆 Leaderboard", "📄 Reports"])
    
    with tab1:
        if not progress_df.empty:
            fig = px.bar(progress_df, x="name", y="progress_future", color="team", 
                         text="progress_future", title="Team Progress (%)", height=450)
            fig.update_traces(textposition="outside")
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(progress_df[["name", "team", "completed_future", "progress_future", "points"]], 
                        use_container_width=True, hide_index=True)
    
    with tab2:
        if not progress_df.empty:
            for idx, (_, row) in enumerate(progress_df.head(5).iterrows()):
                medal = "🥇" if idx == 0 else "🥈" if idx == 1 else "🥉" if idx == 2 else f"{idx+1}."
                st.markdown(f"""
                <div class="leaderboard-card">
                    <strong>{medal} {row['name']}</strong> - {row['team']}<br>
                    ✅ Completed: {row['completed_future']} | 📊 Progress: {row['progress_future']}% | 🏆 Points: {row['points']}
                </div>
                """, unsafe_allow_html=True)
    
    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            report_year = st.selectbox("Year", [2026, 2027, 2028])
        with col2:
            report_month = st.selectbox("Month", range(1, 13), 
                                        format_func=lambda x: ["Jan","Feb","Mar","Apr","May","Jun",
                                                              "Jul","Aug","Sep","Oct","Nov","Dec"][x-1])
        if st.button("Generate Report"):
            html = generate_mpr_html(report_year, report_month)
            st.markdown(get_download_link(html, f"MPR_{report_year}_{report_month}.html"), unsafe_allow_html=True)

# ============================================================
# MAIN APP
# ============================================================

def main():
    # Initialize data
    load_tasks()
    initialize_completed_tasks()
    
    # Authentication
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        st.markdown("""
        <div class="main-header">
            <h1>🎯 MahaSTRIDE Enterprise Project Management System</h1>
            <p>24-Month Detailed Task Plan | May 2026 - April 2028</p>
            <p>Monday to Friday | 10:00 AM - 6:00 PM</p>
            <p>✅ May 4 to June 5, 2026: COMPLETED | June 8, 2026 onwards: PENDING</p>
            <p>👥 11 Team Members | 📋 500+ Unique Tasks | 🏆 Gamification | 📊 Analytics</p>
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
    
    # Sidebar
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
            nav_options = ["📝 My Tasks"]
        
        selected_nav = st.radio("Navigation", nav_options, label_visibility="collapsed")
        
        st.markdown("---")
        st.markdown("ℹ️ **Information**")
        st.markdown("🕐 **Hours:** 10 AM - 6 PM")
        st.markdown("📅 **Days:** Monday to Friday")
        st.markdown("✅ **May 4 - June 5:** COMPLETED")
        
        # Show user stats in sidebar for data analysts
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
            st.session_state.authenticated = False
            st.rerun()
    
    # Main content
    if role == "admin":
        if selected_nav == "📊 Dashboard":
            admin_dashboard()
        else:
            st.markdown("## 📄 Reports")
            col1, col2 = st.columns(2)
            with col1:
                report_year = st.selectbox("Year", [2026, 2027, 2028])
            with col2:
                report_month = st.selectbox("Month", range(1, 13), 
                                            format_func=lambda x: ["Jan","Feb","Mar","Apr","May","Jun",
                                                                  "Jul","Aug","Sep","Oct","Nov","Dec"][x-1])
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
                report_month = st.selectbox("Month", range(1, 13), 
                                            format_func=lambda x: ["Jan","Feb","Mar","Apr","May","Jun",
                                                                  "Jul","Aug","Sep","Oct","Nov","Dec"][x-1])
            if st.button("Generate Report"):
                html = generate_mpr_html(report_year, report_month)
                st.markdown(get_download_link(html, f"MPR_{report_year}_{report_month}.html"), unsafe_allow_html=True)
    
    else:
        if selected_nav == "📝 My Tasks":
            data_analyst_dashboard(email, user_info)

if __name__ == "__main__":
    main()
