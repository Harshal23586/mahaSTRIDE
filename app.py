import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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
    .storage-status {
        font-size: 0.8rem;
        padding: 0.2rem 0.5rem;
        border-radius: 5px;
        display: inline-block;
    }
    .storage-connected {
        background-color: #d4edda;
        color: #155724;
    }
    .weekend-badge {
        background-color: #f8d7da;
        color: #721c24;
        padding: 0.2rem 0.5rem;
        border-radius: 5px;
        font-size: 0.8rem;
        display: inline-block;
    }
    .working-day-badge {
        background-color: #d4edda;
        color: #155724;
        padding: 0.2rem 0.5rem;
        border-radius: 5px;
        font-size: 0.8rem;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# User credentials
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

# University to Data Analyst mapping
UNIVERSITY_ANALYST_MAPPING = {
    "MU": "dataanalyst@mahastride.com",
    "SSPU": "dataanalyst@mahastride.com",
    "COEP": "dataanalyst@mahastride.com",
    "AU": "dataanalyst@mahastride.com",
    "NU": "dataanalyst@mahastride.com",
    "KBCNMU": "dataanalyst@mahastride.com",
    "BAMU": "dataanalyst@mahastride.com",
}

# Task schedule (50 working days)
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

# Project start date - May 18, 2026 (Monday)
PROJECT_START_DATE = datetime(2026, 5, 18)

def get_working_date(working_day_number):
    """
    Convert working day number (1-50) to actual calendar date
    Skipping Saturdays and Sundays
    """
    current_date = PROJECT_START_DATE
    working_days_counted = 0
    
    while working_days_counted < working_day_number:
        # Skip Saturday (5) and Sunday (6)
        if current_date.weekday() < 5:  # Monday=0, Tuesday=1, Wednesday=2, Thursday=3, Friday=4
            working_days_counted += 1
            if working_days_counted == working_day_number:
                return current_date
        current_date += timedelta(days=1)
    
    return current_date

def get_current_working_day():
    """Get current working day number based on actual date"""
    today = datetime.now()
    
    if today < PROJECT_START_DATE:
        return 0
    
    current_date = PROJECT_START_DATE
    working_days_counted = 0
    
    while current_date <= today:
        if current_date.weekday() < 5:  # Monday to Friday
            working_days_counted += 1
        current_date += timedelta(days=1)
    
    return min(working_days_counted, 50)

def get_calendar_date_range():
    """Get start and end calendar dates for the project"""
    start_date = PROJECT_START_DATE
    end_date = get_working_date(50)
    return start_date, end_date

def is_weekend(date):
    """Check if a date is weekend (Saturday or Sunday)"""
    return date.weekday() >= 5  # 5=Saturday, 6=Sunday

# Calculate project end date
PROJECT_END_DATE = get_working_date(50)
TOTAL_CALENDAR_DAYS = (PROJECT_END_DATE - PROJECT_START_DATE).days + 1

# Data file path
DATA_FILE = "progress_data.json"

def hash_password(password):
    return sha256(password.encode()).hexdigest()

def authenticate_user(email, password):
    if email in USERS:
        if USERS[email]["password"] == hash_password(password):
            return True, USERS[email]["role"], USERS[email]["name"]
    return False, None, None

def create_initial_data():
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

def load_data():
    """Load data from persistent JSON file"""
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
                if all(uni_code in data for uni_code in UNIVERSITIES.keys()):
                    return data
                else:
                    return create_initial_data()
        else:
            return create_initial_data()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return create_initial_data()

def save_data(data):
    """Save data to persistent JSON file"""
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Error saving data: {e}")
        return False

def update_task_status(university_code, day, status, remarks="", updated_by=""):
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
    data = load_data()
    if university_code not in data:
        return pd.DataFrame()
    
    records = []
    for day in range(1, 51):
        task_data = data[university_code].get(str(day), {})
        framework, task_name = TASK_SCHEDULE.get(day, ("Unknown", "Unknown"))
        status = task_data.get("status", "pending")
        due_date = get_working_date(day)
        
        records.append({
            "Day": day,
            "Working Day": day,
            "Framework": framework,
            "Task": task_name,
            "Status": status.upper(),
            "Status_Code": status,
            "Due Date": due_date.strftime("%Y-%m-%d"),
            "Day of Week": due_date.strftime("%A"),
            "Remarks": task_data.get("remarks", ""),
            "Last Updated": task_data.get("updated_at", "")[:10] if task_data.get("updated_at") else "",
            "Updated By": task_data.get("updated_by", "")
        })
    return pd.DataFrame(records)

def get_summary_stats():
    data = load_data()
    stats = []
    
    for uni_code, uni_info in UNIVERSITIES.items():
        uni_data = data.get(uni_code, {})
        total = 50
        completed = sum(1 for d in uni_data.values() if d.get("status") == "completed")
        in_progress = sum(1 for d in uni_data.values() if d.get("status") == "in_progress")
        pending = total - completed - in_progress
        
        current_working_day = get_current_working_day()
        expected_completion = (current_working_day / total * 100) if current_working_day > 0 else 0
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
                "Percentage": round(percentage, 1),
                "Due Date": f"Days {days[0]}-{days[-1]}"
            })
    
    return pd.DataFrame(records)

def create_admin_dashboard():
    """Create comprehensive admin dashboard with all visualizations"""
    
    # Project header
    st.markdown('<div class="admin-card"><h2>📊 Admin Dashboard</h2><p>Complete Project Analytics & Insights</p></div>', unsafe_allow_html=True)
    
    # Show storage status
    st.markdown('<span class="storage-status storage-connected">✅ Persistent Storage Active - Data is saved between sessions</span>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Project timeline info
    current_working_day = get_current_working_day()
    start_date, end_date = get_calendar_date_range()
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Working Day", f"{current_working_day}/50")
    with col2:
        st.metric("Start Date", start_date.strftime("%Y-%m-%d"))
    with col3:
        st.metric("End Date", end_date.strftime("%Y-%m-%d"))
    with col4:
        days_left = 50 - current_working_day if current_working_day > 0 else 50
        st.metric("Working Days Left", days_left)
    with col5:
        st.metric("Total Duration", f"{TOTAL_CALENDAR_DAYS} calendar days")
    
    st.info(f"📅 **Working Schedule:** Monday to Friday only. Weekends (Saturday & Sunday) are automatically skipped.")
    
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
    
    # Timeline Heatmap
    st.subheader("📅 Project Timeline Heatmap")
    
    data = load_data()
    heatmap_data = []
    for uni_code, uni_info in UNIVERSITIES.items():
        uni_data = data.get(uni_code, {})
        for day in range(1, 51):
            task_data = uni_data.get(str(day), {})
            status = task_data.get("status", "pending")
            status_value = 2 if status == "completed" else 1 if status == "in_progress" else 0
            due_date = get_working_date(day)
            heatmap_data.append({
                "University": uni_info["name"],
                "Working Day": day,
                "Calendar Date": due_date.strftime("%Y-%m-%d"),
                "Status": status_value
            })
    
    heatmap_df = pd.DataFrame(heatmap_data)
    pivot_data = heatmap_df.pivot(index="University", columns="Working Day", values="Status")
    
    fig = px.imshow(
        pivot_data,
        color_continuous_scale=["red", "yellow", "green"],
        aspect="auto",
        title="Project Progress Heatmap (Red=Pending, Yellow=In Progress, Green=Completed)",
        labels=dict(x="Working Day", y="University", color="Status")
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Performance Analytics
    st.subheader("📈 Performance Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig1 = px.bar(
            summary_df, 
            x="University", 
            y="Completion %", 
            color="Completion %",
            color_continuous_scale="Viridis",
            title="Completion % by University",
            text="Completion %",
            height=400
        )
        fig1.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        framework_df = get_framework_progress()
        if not framework_df.empty:
            framework_avg = framework_df.groupby("Framework")["Percentage"].mean().reset_index()
            fig2 = px.bar(
                framework_avg, 
                x="Framework", 
                y="Percentage", 
                color="Percentage",
                color_continuous_scale="Plasma",
                title="Average Framework Completion",
                text="Percentage",
                height=400
            )
            fig2.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            st.plotly_chart(fig2, use_container_width=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        status_counts = {
            "Completed": summary_df["Completed"].sum(),
            "In Progress": summary_df["In Progress"].sum(),
            "Pending": summary_df["Pending"].sum()
        }
        fig3 = px.pie(
            values=list(status_counts.values()), 
            names=list(status_counts.keys()),
            title="Overall Task Status Distribution",
            color_discrete_sequence=["#90EE90", "#FFD700", "#FFB6C1"],
            hole=0.3,
            height=400
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    with col4:
        daily_progress = []
        for day in range(1, 51):
            completed = sum(1 for uni_data in data.values() if uni_data.get(str(day), {}).get("status") == "completed")
            daily_progress.append({"Working Day": day, "Completed": completed})
        daily_df = pd.DataFrame(daily_progress)
        
        fig4 = px.line(
            daily_df, 
            x="Working Day", 
            y="Completed", 
            markers=True,
            title="Daily Tasks Completed Across All Universities",
            height=400
        )
        fig4.update_traces(line=dict(color='green', width=3), marker=dict(size=8))
        st.plotly_chart(fig4, use_container_width=True)
    
    # Cumulative Progress Chart
    st.subheader("📈 Cumulative Progress Over Time")
    
    cumulative_data = []
    for day in range(1, 51):
        day_completed = sum(1 for uni_data in data.values() if uni_data.get(str(day), {}).get("status") == "completed")
        cumulative_data.append({"Working Day": day, "Completed": day_completed})
    
    cum_df = pd.DataFrame(cumulative_data)
    cum_df["Cumulative_Total"] = cum_df["Completed"].cumsum()
    
    fig5 = go.Figure()
    fig5.add_trace(go.Scatter(
        x=cum_df["Working Day"],
        y=cum_df["Cumulative_Total"],
        mode='lines+markers',
        name='Cumulative Tasks Completed',
        fill='tozeroy',
        line=dict(color='#1e3c72', width=3)
    ))
    fig5.update_layout(
        title="Cumulative Tasks Completed Across All Universities",
        xaxis_title="Working Day",
        yaxis_title="Total Tasks Completed",
        height=400
    )
    st.plotly_chart(fig5, use_container_width=True)
    
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
        pivot_framework = pivot_framework.fillna(0)
        
        fig6 = px.imshow(
            pivot_framework,
            text_auto=True,
            aspect="auto",
            color_continuous_scale="Viridis",
            title="Framework Completion Matrix (%)",
            labels=dict(x="Framework", y="University", color="Percentage")
        )
        fig6.update_layout(height=400)
        st.plotly_chart(fig6, use_container_width=True)
        
        st.subheader("Framework Comparison Chart")
        fig7 = px.bar(
            framework_detail, 
            x="University", 
            y="Percentage", 
            color="Framework",
            barmode="group",
            title="Framework Completion by University",
            text="Percentage",
            height=500
        )
        fig7.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        st.plotly_chart(fig7, use_container_width=True)
    
    # Recent Activity
    st.subheader("🔄 Recent Activity Log")
    recent_updates = []
    for uni_code, uni_data in data.items():
        for day_str, task_data in uni_data.items():
            if task_data.get("updated_at"):
                due_date = get_working_date(int(day_str))
                recent_updates.append({
                    "University": UNIVERSITIES[uni_code]["name"],
                    "Working Day": day_str,
                    "Calendar Date": due_date.strftime("%Y-%m-%d"),
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
    
    assigned_universities = [code for code, email in UNIVERSITY_ANALYST_MAPPING.items() if email == user_email]
    
    if not assigned_universities:
        st.warning("No universities assigned to you. Please contact admin.")
        return
    
    selected_uni_code = st.selectbox(
        "Select University", 
        assigned_universities,
        format_func=lambda x: UNIVERSITIES[x]["name"]
    )
    
    if selected_uni_code:
        uni_info = UNIVERSITIES[selected_uni_code]
        st.info(f"**Coordinators:** {uni_info['coordinators']}")
        
        df = get_university_progress(selected_uni_code)
        
        if not df.empty:
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
            
            st.subheader("📚 Framework Progress")
            framework_df = get_framework_progress(selected_uni_code)
            if not framework_df.empty:
                cols = st.columns(4)
                for idx, (_, row) in enumerate(framework_df.iterrows()):
                    with cols[idx]:
                        st.metric(row["Framework"], f"{row['Percentage']:.1f}%", f"{row['Completed']}/{row['Total']}")
            
            st.markdown("---")
            st.subheader("✏️ Update Task Status")
            
            pending_tasks = df[df["Status_Code"].isin(["pending", "in_progress"])]
            
            if not pending_tasks.empty:
                selected_day = st.selectbox(
                    "Select Task to Update",
                    pending_tasks["Day"].tolist(),
                    format_func=lambda x: f"Working Day {x}: {pending_tasks[pending_tasks['Day']==x]['Task'].iloc[0]} (Due: {pending_tasks[pending_tasks['Day']==x]['Due Date'].iloc[0]} - {pending_tasks[pending_tasks['Day']==x]['Day of Week'].iloc[0]})"
                )
                
                task_data = pending_tasks[pending_tasks["Day"] == selected_day].iloc[0]
                
                col1, col2 = st.columns(2)
                with col1:
                    st.info(f"**Framework:** {task_data['Framework']}\n\n**Current Status:** {task_data['Status']}")
                with col2:
                    due_date_obj = datetime.strptime(task_data['Due Date'], "%Y-%m-%d")
                    if is_weekend(due_date_obj):
                        st.error(f"⚠️ **Due Date:** {task_data['Due Date']} ({task_data['Day of Week']}) - Weekend!")
                    else:
                        st.warning(f"**Due Date:** {task_data['Due Date']} ({task_data['Day of Week']})")
                
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
            
            with st.expander("📋 View All Tasks"):
                display_df = df[["Working Day", "Framework", "Task", "Status", "Due Date", "Day of Week", "Remarks"]]
                st.dataframe(display_df, use_container_width=True)

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
    for key in ["authenticated", "user_email", "user_role", "user_name"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

def main():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    
    if not st.session_state["authenticated"]:
        login_page()
        return
    
    user_role = st.session_state["user_role"]
    user_name = st.session_state["user_name"]
    user_email = st.session_state["user_email"]
    
    with st.sidebar:
        st.title("📊 mahaSTRIDE")
        st.markdown(f"**Welcome, {user_name}**")
        st.markdown(f"*Role: {'Admin' if user_role == 'admin' else 'Data Analyst'}*")
        st.markdown("---")
        
        # Show working day info
        current_working_day = get_current_working_day()
        st.markdown(f"**Current Working Day:** {current_working_day}/50")
        
        if current_working_day > 0:
            next_due_date = get_working_date(current_working_day + 1) if current_working_day < 50 else None
            if next_due_date:
                st.markdown(f"**Next Due Date:** {next_due_date.strftime('%Y-%m-%d')} ({next_due_date.strftime('%A')})")
        
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
                pivot_df = pivot_df.fillna(0)
                
                st.subheader("📊 Framework Completion Matrix (%)")
                st.dataframe(pivot_df, use_container_width=True)
                
                st.subheader("📊 Framework Comparison Chart")
                fig = px.bar(
                    framework_df, 
                    x="University", 
                    y="Percentage", 
                    color="Framework",
                    barmode="group",
                    title="Framework Completion by University",
                    text="Percentage",
                    height=500
                )
                fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                st.plotly_chart(fig, use_container_width=True)
                
                st.subheader("📊 Framework Completion Heatmap")
                fig2 = px.imshow(
                    pivot_df,
                    text_auto=True,
                    aspect="auto",
                    color_continuous_scale="Viridis",
                    title="Framework Completion Heatmap (%)"
                )
                fig2.update_layout(height=500)
                st.plotly_chart(fig2, use_container_width=True)
                
                col1, col2, col3 = st.columns(3)
                framework_avg = framework_df.groupby("Framework")["Percentage"].mean()
                with col1:
                    st.metric("Best Framework", framework_avg.idxmax(), f"{framework_avg.max():.1f}%")
                with col2:
                    st.metric("Needs Improvement", framework_avg.idxmin(), f"{framework_avg.min():.1f}%")
                with col3:
                    st.metric("Overall Average", f"{framework_avg.mean():.1f}%")
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
            end_date = get_working_date(50)
            st.markdown(f"""
            ### mahaSTRIDE Project Tracker
            
            **Project Duration:** 50 Working Days  
            **Working Schedule:** Monday to Friday (Weekends skipped)  
            **Start Date:** {PROJECT_START_DATE.strftime('%A, %B %d, %Y')}  
            **End Date:** {end_date.strftime('%A, %B %d, %Y')}  
            **Total Calendar Days:** {(end_date - PROJECT_START_DATE).days + 1} days  
            **Universities:** 7 Participating Universities  
            
            ### Working Day Calculation:
            - Working days are Monday through Friday
            - Saturdays and Sundays are automatically skipped
            - Day 1 = {PROJECT_START_DATE.strftime('%A, %B %d, %Y')}
            - Day 50 = {end_date.strftime('%A, %B %d, %Y')}
            
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
    
    else:
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
                    display_df = df[["Working Day", "Framework", "Task", "Status", "Due Date", "Day of Week", "Remarks"]]
                    st.dataframe(display_df, use_container_width=True)
        else:
            st.title("ℹ️ About")
            end_date = get_working_date(50)
            st.markdown(f"""
            ### mahaSTRIDE Project Tracker - Data Analyst Portal
            
            **Your Role:** Update and track progress for assigned universities
            
            **Working Schedule:** Monday to Friday (Weekends skipped)  
            **Project Timeline:** {PROJECT_START_DATE.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}  
            **Working Days:** 50 days (Monday-Friday only)
            
            ### Your Responsibilities:
            - Update task status regularly on working days
            - Add remarks for completed/in-progress tasks
            - Ensure timely completion of tasks
            - Maintain accurate progress records
            
            **Note:** Weekends (Saturday & Sunday) are automatically skipped in the schedule.
            
            ### Access Credentials:
            - **Email:** dataanalyst@mahastride.com
            - **Password:** Data@2026
            """)

if __name__ == "__main__":
    if not os.path.exists(DATA_FILE):
        save_data(create_initial_data())
    
    main()
