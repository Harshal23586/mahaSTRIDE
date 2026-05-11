import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import os
import json
from hashlib import sha256

# Page configuration
st.set_page_config(
    page_title="mahaSTRIDE Project Tracker",
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
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #e0e0e0;
        transition: transform 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .info-card {
        background-color: #d1ecf1;
        border-left: 4px solid #17a2b8;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .success-card {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .warning-card {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .admin-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .stButton > button {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 5px;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .timeline-container {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# User credentials (same for all users of same role)
USERS = {
    "admin@mahastride.com": {
        "password": sha256("Admin@2026".encode()).hexdigest(),
        "role": "admin",
        "name": "Dr. Harshal"
    },
    "dataanalyst@mahastride.com": {
        "password": sha256("Data@2026".encode()).hexdigest(),
        "role": "data_analyst",
        "name": "Data Analyst"
    }
}

# University to Data Analyst mapping (each analyst can edit their respective university)
UNIVERSITY_ANALYST_MAPPING = {
    "MU": "dataanalyst@mahastride.com",
    "SSPU": "dataanalyst@mahastride.com",
    "COEP": "dataanalyst@mahastride.com",
    "AU": "dataanalyst@mahastride.com",
    "NU": "dataanalyst@mahastride.com",
    "KBCNMU": "dataanalyst@mahastride.com",
    "BAMU": "dataanalyst@mahastride.com",
}

# Task schedule
TASK_SCHEDULE = {
    1: ("SAMARTH", "Faculty Roster - Day 1"),
    2: ("SAMARTH", "Faculty Roster - Day 2"),
    3: ("SAMARTH", "Students Documentation - Day 3"),
    4: ("SAMARTH", "Students Documentation - Day 4"),
    5: ("SAMARTH", "Financial Records - Day 5"),
    6: ("SAMARTH", "Financial Records - Day 6"),
    7: ("SAMARTH", "IPR/Patents - Day 7"),
    8: ("SAMARTH", "IPR/Patents - Day 8"),
    9: ("SAMARTH", "Publications - Day 9"),
    10: ("SAMARTH", "Publications - Day 10"),
    11: ("SAMARTH", "PhD Faculties - Day 11"),
    12: ("SAMARTH", "PhD Faculties - Day 12"),
    13: ("SAMARTH", "SAM TLR - Day 13"),
    14: ("SAMARTH", "SAM TLR - Day 14"),
    15: ("SAMARTH", "SAM TLR - Day 15"),
    16: ("SAMARTH", "SAM TLR - Day 16"),
    17: ("SAMARTH", "SAM RP - Day 17"),
    18: ("SAMARTH", "SAM RP - Day 18"),
    19: ("SAMARTH", "SAM RP - Day 19"),
    20: ("SAMARTH", "SAM RP - Day 20"),
    21: ("SAMARTH", "SAM-GO - Day 21"),
    22: ("SAMARTH", "SAM-GO - Day 22"),
    23: ("SAMARTH", "SAM-OI - Day 23"),
    24: ("SAMARTH", "SAM-OI - Day 24"),
    25: ("SAMARTH", "SAM PR - Day 25"),
    26: ("NEP", "NEP CUR - Day 26"),
    27: ("NEP", "NEP CUR - Day 27"),
    28: ("NEP", "NEP-TCH - Day 28"),
    29: ("NEP", "NEP-TCH - Day 29"),
    30: ("NEP", "NEP RES - Day 30"),
    31: ("NEP", "NEP GOV - Day 31"),
    32: ("NEP", "NEP INC - Day 32"),
    33: ("NEP", "NEP OUT - Day 33"),
    34: ("NEP", "NEP-DIG - Day 34"),
    35: ("NEP", "NEP SUS - Day 35"),
    36: ("AEGIS", "AEG-BI - Day 36"),
    37: ("AEGIS", "AEG-BI - Day 37"),
    38: ("AEGIS", "AEG-EDU - Day 38"),
    39: ("AEGIS", "AEG-EDU - Day 39"),
    40: ("AEGIS", "AEG-GRD - Day 40"),
    41: ("AEGIS", "AEG-INC - Day 41"),
    42: ("AEGIS", "AEG-SAF - Day 42"),
    43: ("IKS", "IKS-CUR - Day 43"),
    44: ("IKS", "IKS-CUR - Day 44"),
    45: ("IKS", "IKS-TCH - Day 45"),
    46: ("IKS", "IKS-TCH - Day 46"),
    47: ("IKS", "IKS-RES - Day 47"),
    48: ("IKS", "IKS-GOV - Day 48"),
    49: ("IKS", "IKS-OUT - Day 49"),
    50: ("IKS", "IKS-DIG - Day 50"),
}

# Universities data
UNIVERSITIES = {
    "MU": {"name": "Mumbai University", "coordinators": "Ms Sneha, Shubham"},
    "SSPU": {"name": "SSPU Pune", "coordinators": "Mr Jagan"},
    "COEP": {"name": "COEP Tech University", "coordinators": "Mr Vaibhav"},
    "AU": {"name": "Amravati University", "coordinators": "Mr Pratham"},
    "NU": {"name": "Nagpur University", "coordinators": "Ms Anjali"},
    "KBCNMU": {"name": "KBCNMU Jalgaon University", "coordinators": "Mr Nitish"},
    "BAMU": {"name": "BAMU University Aurangabad", "coordinators": "Mr Atharv"},
}

# Project start date - May 18, 2026
PROJECT_START_DATE = datetime(2026, 5, 18)
PROJECT_END_DATE = PROJECT_START_DATE + timedelta(days=49)

# Data file path
DATA_FILE = "progress_data.json"

def hash_password(password):
    """Hash a password"""
    return sha256(password.encode()).hexdigest()

def authenticate_user(email, password):
    """Authenticate user"""
    if email in USERS:
        if USERS[email]["password"] == hash_password(password):
            return True, USERS[email]["role"], USERS[email]["name"]
    return False, None, None

def load_data():
    """Load progress data from JSON file"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except:
            return create_initial_data()
    else:
        return create_initial_data()

def create_initial_data():
    """Create initial data structure"""
    data = {}
    for uni_code in UNIVERSITIES.keys():
        data[uni_code] = {}
        for day in range(1, 51):
            data[uni_code][str(day)] = {
                "status": "pending",
                "remarks": "",
                "updated_at": None,
                "updated_by": None
            }
    return data

def save_data(data):
    """Save progress data to JSON file"""
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except:
        return False

def update_task_status(university_code, day, status, remarks="", updated_by=""):
    """Update task status"""
    data = load_data()
    if university_code in data and str(day) in data[university_code]:
        data[university_code][str(day)]["status"] = status
        if remarks:
            data[university_code][str(day)]["remarks"] = remarks
        data[university_code][str(day)]["updated_at"] = datetime.now().isoformat()
        data[university_code][str(day)]["updated_by"] = updated_by
        return save_data(data)
    return False

def get_university_progress(university_code):
    """Get progress dataframe for a university"""
    data = load_data()
    if university_code not in data:
        return pd.DataFrame()
    
    records = []
    for day in range(1, 51):
        task_data = data[university_code].get(str(day), {})
        framework, task_name = TASK_SCHEDULE.get(day, ("Unknown", "Unknown"))
        status = task_data.get("status", "pending")
        due_date = PROJECT_START_DATE + timedelta(days=day-1)
        
        records.append({
            "Day": day,
            "Framework": framework,
            "Task": task_name,
            "Status": status.upper(),
            "Status_Code": status,
            "Due Date": due_date.strftime("%Y-%m-%d"),
            "Remarks": task_data.get("remarks", ""),
            "Last Updated": task_data.get("updated_at", "")[:10] if task_data.get("updated_at") else "",
            "Updated By": task_data.get("updated_by", "")
        })
    return pd.DataFrame(records)

def get_summary_stats():
    """Get summary statistics"""
    data = load_data()
    stats = []
    
    for uni_code, uni_info in UNIVERSITIES.items():
        uni_data = data.get(uni_code, {})
        total = 50
        completed = sum(1 for d in uni_data.values() if d.get("status") == "completed")
        in_progress = sum(1 for d in uni_data.values() if d.get("status") == "in_progress")
        pending = total - completed - in_progress
        
        # Calculate on-track status
        current_day = get_current_project_day()
        expected_completion = (current_day / total * 100) if current_day > 0 else 0
        actual_completion = (completed / total * 100) if total > 0 else 0
        is_on_track = actual_completion >= expected_completion - 10
        
        stats.append({
            "University": uni_info["name"],
            "Code": uni_code,
            "Coordinators": uni_info["coordinators"],
            "Completed": completed,
            "In Progress": in_progress,
            "Pending": pending,
            "Completion %": round((completed / total * 100), 1),
            "On Track": "✅ Yes" if is_on_track else "⚠️ Behind"
        })
    
    return pd.DataFrame(stats)

def get_framework_progress(university_code=None):
    """Get framework-wise progress"""
    data = load_data()
    frameworks = {
        "SAMARTH": list(range(1, 26)),
        "NEP": list(range(26, 36)),
        "AEGIS": list(range(36, 43)),
        "IKS": list(range(43, 51))
    }
    
    records = []
    unis_to_process = [university_code] if university_code else list(UNIVERSITIES.keys())
    
    for uni_code in unis_to_process:
        if uni_code not in data:
            continue
        
        uni_name = UNIVERSITIES[uni_code]["name"]
        uni_data = data[uni_code]
        
        for framework, days in frameworks.items():
            total = len(days)
            completed = sum(1 for day in days if uni_data.get(str(day), {}).get("status") == "completed")
            in_progress = sum(1 for day in days if uni_data.get(str(day), {}).get("status") == "in_progress")
            percentage = (completed / total * 100) if total > 0 else 0
            
            records.append({
                "University": uni_name,
                "Framework": framework,
                "Completed": completed,
                "In Progress": in_progress,
                "Total": total,
                "Percentage": round(percentage, 1)
            })
    
    return pd.DataFrame(records)

def get_current_project_day():
    """Get current day of the project"""
    today = datetime.now()
    if today < PROJECT_START_DATE:
        return 0
    days_passed = (today - PROJECT_START_DATE).days
    return min(days_passed + 1, 50)

def create_admin_dashboard():
    """Create comprehensive admin dashboard with all visualizations"""
    
    # Project header
    st.markdown('<div class="admin-card"><h2>📊 Admin Dashboard</h2><p>Complete Project Analytics & Insights</p></div>', unsafe_allow_html=True)
    
    # Project timeline info
    current_day = get_current_project_day()
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Project Day", f"{current_day}/50")
    with col2:
        st.metric("Start Date", PROJECT_START_DATE.strftime("%Y-%m-%d"))
    with col3:
        st.metric("End Date", PROJECT_END_DATE.strftime("%Y-%m-%d"))
    with col4:
        days_left = 50 - current_day if current_day > 0 else 50
        st.metric("Days Remaining", days_left)
    
    st.markdown("---")
    
    # Key Performance Indicators
    st.subheader("🎯 Key Performance Indicators")
    summary_df = get_summary_stats()
    
    if not summary_df.empty:
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            total_completed = summary_df["Completed"].sum()
            st.metric("✅ Total Completed", f"{total_completed}/350", delta=f"{(total_completed/350*100):.1f}%")
        with col2:
            avg_completion = summary_df["Completion %"].mean()
            st.metric("📊 Avg Completion", f"{avg_completion:.1f}%")
        with col3:
            on_track_count = len(summary_df[summary_df["On Track"] == "✅ Yes"])
            st.metric("🏆 On Track", f"{on_track_count}/7")
        with col4:
            total_in_progress = summary_df["In Progress"].sum()
            st.metric("🔄 In Progress", total_in_progress)
        with col5:
            best_uni = summary_df.loc[summary_df["Completion %"].idxmax(), "University"]
            st.metric("🥇 Top Performer", best_uni[:15])
    
    st.markdown("---")
    
    # Timeline Heatmap (fixed version)
    st.subheader("📅 Project Timeline Heatmap")
    
    # Prepare data for heatmap
    data = load_data()
    heatmap_data = []
    for uni_code, uni_info in UNIVERSITIES.items():
        uni_data = data.get(uni_code, {})
        for day in range(1, 51):
            task_data = uni_data.get(str(day), {})
            status = task_data.get("status", "pending")
            status_value = 2 if status == "completed" else 1 if status == "in_progress" else 0
            heatmap_data.append({
                "University": uni_info["name"],
                "Day": day,
                "Status": status_value,
                "Status_Text": status.upper()
            })
    
    heatmap_df = pd.DataFrame(heatmap_data)
    
    # Create pivot table for heatmap
    pivot_data = heatmap_df.pivot(index="University", columns="Day", values="Status")
    
    # Create heatmap using plotly
    fig = px.imshow(
        pivot_data,
        color_continuous_scale=["red", "yellow", "green"],
        aspect="auto",
        title="Project Progress Heatmap (Red=Pending, Yellow=In Progress, Green=Completed)",
        labels=dict(x="Project Day", y="University", color="Status Value")
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Multi-metric charts
    st.subheader("📈 Performance Analytics")
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("Completion % by University", "Framework-wise Progress", "Task Status Distribution", "Daily Progress Trend")
    )
    
    # Chart 1: Completion by University
    fig.add_trace(
        go.Bar(x=summary_df["University"], y=summary_df["Completion %"], marker_color='#1e3c72', text=summary_df["Completion %"], textposition='auto'),
        row=1, col=1
    )
    
    # Chart 2: Framework-wise Progress
    framework_df = get_framework_progress()
    if not framework_df.empty:
        framework_avg = framework_df.groupby("Framework")["Percentage"].mean().reset_index()
        fig.add_trace(
            go.Bar(x=framework_avg["Framework"], y=framework_avg["Percentage"], marker_color='#2a5298', text=framework_avg["Percentage"], textposition='auto'),
            row=1, col=2
        )
    
    # Chart 3: Task Status Distribution (Donut chart)
    status_counts = {
        "Completed": summary_df["Completed"].sum(),
        "In Progress": summary_df["In Progress"].sum(),
        "Pending": summary_df["Pending"].sum()
    }
    fig.add_trace(
        go.Pie(labels=list(status_counts.keys()), values=list(status_counts.values()), hole=0.3),
        row=2, col=1
    )
    
    # Chart 4: Daily Progress Trend
    daily_progress = []
    for day in range(1, 51):
        completed = sum(1 for uni_data in data.values() if uni_data.get(str(day), {}).get("status") == "completed")
        daily_progress.append({"Day": day, "Completed": completed})
    daily_df = pd.DataFrame(daily_progress)
    fig.add_trace(
        go.Scatter(x=daily_df["Day"], y=daily_df["Completed"], mode='lines+markers', name='Daily Completions', line=dict(color='green', width=2)),
        row=2, col=2
    )
    
    fig.update_layout(height=800, showlegend=True)
    fig.update_xaxes(title_text="University", row=1, col=1)
    fig.update_xaxes(title_text="Framework", row=1, col=2)
    fig.update_xaxes(title_text="Day", row=2, col=2)
    fig.update_yaxes(title_text="Completion %", row=1, col=1)
    fig.update_yaxes(title_text="Completion %", row=1, col=2)
    fig.update_yaxes(title_text="Number of Tasks", row=2, col=2)
    st.plotly_chart(fig, use_container_width=True)
    
    # Cumulative Progress Chart
    st.subheader("📈 Cumulative Progress Over Time")
    
    cumulative_data = []
    for day in range(1, 51):
        cumulative_completed = 0
        for uni_code in UNIVERSITIES.keys():
            if uni_data.get(str(day), {}).get("status") == "completed":
                cumulative_completed += 1
        cumulative_data.append({"Day": day, "Cumulative": cumulative_completed})
    
    cum_df = pd.DataFrame(cumulative_data)
    cum_df["Cumulative_Total"] = cum_df["Cumulative"].cumsum()
    
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=cum_df["Day"],
        y=cum_df["Cumulative_Total"],
        mode='lines+markers',
        name='Cumulative Tasks Completed',
        fill='tozeroy',
        line=dict(color='#1e3c72', width=3)
    ))
    fig2.update_layout(
        title="Cumulative Tasks Completed Across All Universities",
        xaxis_title="Project Day",
        yaxis_title="Total Tasks Completed",
        height=400
    )
    st.plotly_chart(fig2, use_container_width=True)
    
    # University Ranking
    st.subheader("🏆 University Rankings")
    ranking_df = summary_df[["University", "Completion %", "Completed", "In Progress", "Pending", "On Track"]].sort_values("Completion %", ascending=False)
    ranking_df.index = range(1, len(ranking_df) + 1)
    st.dataframe(ranking_df, use_container_width=True)
    
    # Framework Analysis
    st.subheader("📚 Detailed Framework Analysis")
    framework_detail = get_framework_progress()
    if not framework_detail.empty:
        pivot_framework = framework_detail.pivot(index="University", columns="Framework", values="Percentage")
        # Apply styling
        styled_pivot = pivot_framework.style.background_gradient(cmap='YlOrRd', axis=None)
        st.dataframe(styled_pivot, use_container_width=True)
    
    # Recent Activity
    st.subheader("🔄 Recent Activity Log")
    recent_updates = []
    for uni_code, uni_data in data.items():
        for day_str, task_data in uni_data.items():
            if task_data.get("updated_at"):
                recent_updates.append({
                    "University": UNIVERSITIES[uni_code]["name"],
                    "Day": day_str,
                    "Task": TASK_SCHEDULE.get(int(day_str), ("", ""))[1],
                    "Status": task_data.get("status", "").upper(),
                    "Updated By": task_data.get("updated_by", ""),
                    "Updated At": task_data["updated_at"]
                })
    
    if recent_updates:
        recent_df = pd.DataFrame(recent_updates).sort_values("Updated At", ascending=False).head(20)
        st.dataframe(recent_df, use_container_width=True)
    else:
        st.info("No updates recorded yet")
    
    # Export Options
    st.subheader("💾 Export Data")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📥 Export Complete Report (CSV)", use_container_width=True):
            all_data = []
            for uni_code in UNIVERSITIES.keys():
                df = get_university_progress(uni_code)
                df["University"] = UNIVERSITIES[uni_code]["name"]
                all_data.append(df)
            if all_data:
                combined = pd.concat(all_data, ignore_index=True)
                csv = combined.to_csv(index=False)
                st.download_button("Download CSV", csv, "complete_mahastride_data.csv", "text/csv")
    with col2:
        if st.button("📊 Export Summary Report (CSV)", use_container_width=True):
            csv = summary_df.to_csv(index=False)
            st.download_button("Download CSV", csv, "summary_report.csv", "text/csv")

def create_data_analyst_dashboard(user_email):
    """Create data analyst dashboard for assigned universities"""
    
    st.markdown('<div class="info-card"><h2>📊 Data Analyst Dashboard</h2><p>Update and track your assigned university progress</p></div>', unsafe_allow_html=True)
    
    # Get universities assigned to this analyst
    assigned_universities = [code for code, email in UNIVERSITY_ANALYST_MAPPING.items() if email == user_email]
    
    if not assigned_universities:
        st.warning("No universities assigned to you. Please contact admin.")
        return
    
    # University selector
    selected_uni_code = st.selectbox(
        "Select University", 
        assigned_universities,
        format_func=lambda x: UNIVERSITIES[x]["name"]
    )
    
    if selected_uni_code:
        uni_info = UNIVERSITIES[selected_uni_code]
        st.info(f"**Coordinators:** {uni_info['coordinators']}")
        
        # Show progress summary
        df = get_university_progress(selected_uni_code)
        
        if not df.empty:
            # Statistics
            col1, col2, col3, col4 = st.columns(4)
            completed = len(df[df["Status"] == "COMPLETED"])
            in_progress = len(df[df["Status"] == "IN PROGRESS"])
            pending = len(df[df["Status"] == "PENDING"])
            
            with col1:
                st.metric("✅ Completed", completed, delta=f"{(completed/50*100):.1f}%")
            with col2:
                st.metric("🔄 In Progress", in_progress)
            with col3:
                st.metric("⏳ Pending", pending)
            with col4:
                st.metric("📊 Progress", f"{(completed/50*100):.1f}%")
            
            st.progress(completed/50)
            
            # Framework breakdown
            st.subheader("📚 Framework Progress")
            framework_df = get_framework_progress(selected_uni_code)
            if not framework_df.empty:
                cols = st.columns(4)
                for idx, (_, row) in enumerate(framework_df.iterrows()):
                    with cols[idx]:
                        st.metric(row["Framework"], f"{row['Percentage']:.1f}%", f"{row['Completed']}/{row['Total']}")
            
            # Task update section
            st.markdown("---")
            st.subheader("✏️ Update Task Status")
            
            pending_tasks = df[df["Status_Code"].isin(["pending", "in_progress"])]
            
            if not pending_tasks.empty:
                selected_day = st.selectbox(
                    "Select Task to Update",
                    pending_tasks["Day"].tolist(),
                    format_func=lambda x: f"Day {x}: {pending_tasks[pending_tasks['Day']==x]['Task'].iloc[0]} (Due: {pending_tasks[pending_tasks['Day']==x]['Due Date'].iloc[0]})"
                )
                
                task_data = pending_tasks[pending_tasks["Day"] == selected_day].iloc[0]
                
                col1, col2 = st.columns(2)
                with col1:
                    st.info(f"**Framework:** {task_data['Framework']}\n\n**Current Status:** {task_data['Status']}")
                with col2:
                    st.warning(f"**Due Date:** {task_data['Due Date']}")
                
                new_status = st.radio(
                    "Update Status To:",
                    ["in_progress", "completed"],
                    format_func=lambda x: "🔄 In Progress" if x == "in_progress" else "✅ Completed"
                )
                
                remarks = st.text_area("Remarks (optional)", placeholder="Add any notes about this task...")
                
                if st.button("🚀 Update Status", type="primary", use_container_width=True):
                    if update_task_status(selected_uni_code, selected_day, new_status, remarks, user_email):
                        st.success(f"✅ Task status updated to {new_status.upper()} successfully!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("❌ Failed to update status")
            else:
                st.success("🎉 Congratulations! All tasks for this university are completed!")
            
            # View all tasks
            with st.expander("📋 View All Tasks"):
                st.dataframe(df[["Day", "Framework", "Task", "Status", "Due Date", "Remarks"]], use_container_width=True)

def login_page():
    """Display login page"""
    st.markdown('<div class="main-header"><h1>🔐 mahaSTRIDE Project Tracker</h1><p>Please login to continue</p></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### Login")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        
        if st.button("Login", type="primary", use_container_width=True):
            if email and password:
                success, role, name = authenticate_user(email, password)
                if success:
                    st.session_state["authenticated"] = True
                    st.session_state["user_email"] = email
                    st.session_state["user_role"] = role
                    st.session_state["user_name"] = name
                    st.rerun()
                else:
                    st.error("Invalid email or password")
            else:
                st.warning("Please enter both email and password")
        
        st.markdown("---")
        st.markdown("""
        **Demo Credentials:**
        - **Admin:** admin@mahastride.com / Admin@2026
        - **Data Analyst:** dataanalyst@mahastride.com / Data@2026
        """)

def logout():
    """Logout user"""
    for key in ["authenticated", "user_email", "user_role", "user_name"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

# Main application
def main():
    # Initialize session state
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    
    # Show login page if not authenticated
    if not st.session_state["authenticated"]:
        login_page()
        return
    
    # Logged in user
    user_role = st.session_state["user_role"]
    user_name = st.session_state["user_name"]
    user_email = st.session_state["user_email"]
    
    # Sidebar with user info
    with st.sidebar:
        st.title("📊 mahaSTRIDE")
        st.markdown(f"**Welcome, {user_name}**")
        st.markdown(f"*Role: {'Admin' if user_role == 'admin' else 'Data Analyst'}*")
        st.markdown("---")
        
        if user_role == "admin":
            menu = st.radio(
                "Navigation",
                ["Admin Dashboard", "University Details", "Framework Analytics", "User Management", "About"]
            )
        else:
            menu = st.radio(
                "Navigation",
                ["My Dashboard", "Update Progress", "View Tasks", "About"]
            )
        
        st.markdown("---")
        
        # Show overall progress in sidebar
        summary_df = get_summary_stats()
        if not summary_df.empty:
            total_completed = summary_df["Completed"].sum()
            total_tasks = 50 * 7
            overall_pct = (total_completed / total_tasks * 100) if total_tasks > 0 else 0
            st.metric("Overall Progress", f"{overall_pct:.1f}%")
            st.progress(overall_pct / 100)
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            logout()
    
    # Main content based on role and menu
    if user_role == "admin":
        if menu == "Admin Dashboard":
            create_admin_dashboard()
        elif menu == "University Details":
            st.title("🏛️ University Details")
            summary_df = get_summary_stats()
            if not summary_df.empty:
                st.dataframe(summary_df, use_container_width=True)
        elif menu == "Framework Analytics":
            st.title("📚 Framework Analytics")
            framework_df = get_framework_progress()
            if not framework_df.empty:
                pivot_df = framework_df.pivot(index="University", columns="Framework", values="Percentage")
                # Fill NaN values with 0
                pivot_df = pivot_df.fillna(0)
                st.dataframe(pivot_df.style.background_gradient(cmap='YlOrRd', axis=None), use_container_width=True)
                
                # Framework comparison chart
                fig = px.bar(framework_df, x="Framework", y="Percentage", color="University", barmode="group", title="Framework Completion by University")
                st.plotly_chart(fig, use_container_width=True)
        elif menu == "User Management":
            st.title("👥 User Management")
            st.info("Current Users:")
            user_df = pd.DataFrame([
                {"Email": email, "Role": info["role"], "Name": info["name"]}
                for email, info in USERS.items()
            ])
            st.dataframe(user_df, use_container_width=True)
        else:
            st.title("ℹ️ About")
            st.markdown(f"""
            ### mahaSTRIDE Project Tracker
            
            **Project Duration:** 50 Days  
            **Timeline:** {PROJECT_START_DATE.strftime('%Y-%m-%d')} to {PROJECT_END_DATE.strftime('%Y-%m-%d')}  
            **Universities:** 7 Participating Universities  
            
            ### Admin Features:
            - Complete project overview dashboard
            - Real-time progress tracking
            - Advanced analytics and visualizations
            - Heatmaps and cumulative charts
            - Export capabilities
            - User management
            
            ### Access Credentials:
            - **Admin:** admin@mahastride.com / Admin@2026
            - **Data Analyst:** dataanalyst@mahastride.com / Data@2026
            """)
    
    else:  # Data Analyst
        if menu == "My Dashboard":
            create_data_analyst_dashboard(user_email)
        elif menu == "Update Progress":
            st.title("✅ Update Progress")
            create_data_analyst_dashboard(user_email)
        elif menu == "View Tasks":
            st.title("📋 View All Tasks")
            assigned_universities = [code for code, email in UNIVERSITY_ANALYST_MAPPING.items() if email == user_email]
            if assigned_universities:
                selected_uni = st.selectbox("Select University", assigned_universities, format_func=lambda x: UNIVERSITIES[x]["name"])
                if selected_uni:
                    df = get_university_progress(selected_uni)
                    st.dataframe(df, use_container_width=True)
        else:
            st.title("ℹ️ About")
            st.markdown(f"""
            ### mahaSTRIDE Project Tracker - Data Analyst Portal
            
            **Your Role:** Update and track progress for assigned universities
            
            **Project Timeline:** {PROJECT_START_DATE.strftime('%Y-%m-%d')} to {PROJECT_END_DATE.strftime('%Y-%m-%d')}
            
            ### Your Responsibilities:
            - Update task status regularly
            - Add remarks for completed/in-progress tasks
            - Ensure timely completion of tasks
            - Maintain accurate progress records
            
            ### Access Credentials:
            - **Email:** dataanalyst@mahastride.com
            - **Password:** Data@2026
            """)

if __name__ == "__main__":
    # Initialize data on first run
    if not os.path.exists(DATA_FILE):
        save_data(create_initial_data())
    
    main()
