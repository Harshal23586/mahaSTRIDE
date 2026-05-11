import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
import json

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
</style>
""", unsafe_allow_html=True)

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

# Data file path
DATA_FILE = "progress_data.json"

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
                "updated_at": None
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

def update_task_status(university_code, day, status, remarks=""):
    """Update task status"""
    data = load_data()
    if university_code in data and str(day) in data[university_code]:
        data[university_code][str(day)]["status"] = status
        if remarks:
            data[university_code][str(day)]["remarks"] = remarks
        data[university_code][str(day)]["updated_at"] = datetime.now().isoformat()
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
        
        records.append({
            "Day": day,
            "Framework": framework,
            "Task": task_name,
            "Status": status.upper(),
            "Remarks": task_data.get("remarks", ""),
            "Last Updated": task_data.get("updated_at", "")[:10] if task_data.get("updated_at") else ""
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
        
        stats.append({
            "University": uni_info["name"],
            "Code": uni_code,
            "Coordinators": uni_info["coordinators"],
            "Completed": completed,
            "In Progress": in_progress,
            "Pending": pending,
            "Completion %": round((completed / total * 100), 1)
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
            percentage = (completed / total * 100) if total > 0 else 0
            
            records.append({
                "University": uni_name,
                "Framework": framework,
                "Completed": completed,
                "Total": total,
                "Percentage": round(percentage, 1)
            })
    
    return pd.DataFrame(records)

# Initialize data on first run
if not os.path.exists(DATA_FILE):
    save_data(create_initial_data())

# Sidebar
with st.sidebar:
    st.title("📊 mahaSTRIDE")
    st.markdown("---")
    
    menu = st.radio(
        "Navigation",
        ["Dashboard", "University Progress", "Update Status", "Framework Analysis", "Reports", "About"]
    )
    
    st.markdown("---")
    
    # Show overall progress
    summary_df = get_summary_stats()
    if not summary_df.empty:
        total_completed = summary_df["Completed"].sum()
        total_tasks = 50 * 7
        overall_pct = (total_completed / total_tasks * 100) if total_tasks > 0 else 0
        st.metric("Overall Progress", f"{overall_pct:.1f}%")
        st.progress(overall_pct / 100)
        
        # Project timeline
        st.markdown("---")
        st.markdown("### 📅 Timeline")
        project_start = datetime(2024, 11, 1)
        current_day = (datetime.now() - project_start).days + 1
        current_day = max(1, min(current_day, 50))
        st.write(f"**Day:** {current_day} / 50")
        st.write(f"**Progress:** {(current_day/50*100):.1f}%")
        st.progress(current_day/50)

# Main content
if menu == "Dashboard":
    st.markdown('<div class="main-header"><h1>🏠 mahaSTRIDE Dashboard</h1><p>Project Progress Tracking System</p></div>', unsafe_allow_html=True)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    if not summary_df.empty:
        with col1:
            st.metric("📋 Total Tasks", "350", help="50 days × 7 universities")
        with col2:
            st.metric("✅ Completed", f"{summary_df['Completed'].sum()}")
        with col3:
            st.metric("📊 Completion", f"{overall_pct:.1f}%")
        with col4:
            st.metric("🏛️ Universities", "7")
    
    st.markdown("---")
    
    # University progress chart
    st.subheader("📈 University Progress")
    if not summary_df.empty:
        chart_data = summary_df.set_index("University")["Completion %"]
        st.bar_chart(chart_data)
        
        with st.expander("📋 View Detailed Statistics"):
            st.dataframe(summary_df, use_container_width=True)
    
    # Today's tasks
    st.markdown("---")
    st.subheader("📅 Today's Schedule")
    project_start = datetime(2024, 11, 1)
    current_day = (datetime.now() - project_start).days + 1
    current_day = max(1, min(current_day, 50))
    
    if current_day <= 50:
        framework, task = TASK_SCHEDULE[current_day]
        st.info(f"**Day {current_day} - {framework} Framework**\n\n📋 **Task:** {task}")

elif menu == "University Progress":
    st.title("🏛️ University Progress")
    st.markdown("---")
    
    selected_uni = st.selectbox("Select University", list(UNIVERSITIES.keys()), format_func=lambda x: UNIVERSITIES[x]["name"])
    
    if selected_uni:
        uni_info = UNIVERSITIES[selected_uni]
        st.info(f"**Coordinators:** {uni_info['coordinators']}")
        
        df = get_university_progress(selected_uni)
        
        if not df.empty:
            # Stats
            col1, col2, col3 = st.columns(3)
            completed = len(df[df["Status"] == "COMPLETED"])
            in_progress = len(df[df["Status"] == "IN PROGRESS"])
            
            with col1:
                st.metric("✅ Completed", completed)
            with col2:
                st.metric("🔄 In Progress", in_progress)
            with col3:
                st.metric("⏳ Pending", 50 - completed - in_progress)
            
            # Progress bar
            st.progress(completed / 50)
            
            # Detailed table
            st.subheader("Task Details")
            st.dataframe(df, use_container_width=True, height=400)

elif menu == "Update Status":
    st.title("✅ Update Task Status")
    st.markdown("---")
    
    st.warning("⚠️ Coordinator Access Only")
    
    selected_uni = st.selectbox("University", list(UNIVERSITIES.keys()), format_func=lambda x: UNIVERSITIES[x]["name"])
    
    if selected_uni:
        df = get_university_progress(selected_uni)
        pending_df = df[df["Status"].isin(["PENDING", "IN PROGRESS"])]
        
        if not pending_df.empty:
            selected_day = st.selectbox(
                "Select Task", 
                pending_df["Day"].tolist(),
                format_func=lambda x: f"Day {x}: {pending_df[pending_df['Day']==x]['Task'].iloc[0]}"
            )
            
            task_data = pending_df[pending_df["Day"] == selected_day].iloc[0]
            st.info(f"**Framework:** {task_data['Framework']}\n\n**Current Status:** {task_data['Status']}")
            
            new_status = st.radio("Update Status", ["in_progress", "completed"], format_func=lambda x: "🔄 In Progress" if x == "in_progress" else "✅ Completed")
            remarks = st.text_area("Remarks")
            
            if st.button("Update", type="primary"):
                if update_task_status(selected_uni, selected_day, new_status, remarks):
                    st.success("✅ Status updated successfully!")
                    st.rerun()
        else:
            st.success("🎉 All tasks completed!")

elif menu == "Framework Analysis":
    st.title("📚 Framework Analysis")
    st.markdown("---")
    
    framework_df = get_framework_progress()
    
    if not framework_df.empty:
        selected_framework = st.selectbox("Select Framework", ["SAMARTH", "NEP", "AEGIS", "IKS"])
        
        filtered_df = framework_df[framework_df["Framework"] == selected_framework]
        
        # Chart
        chart_data = filtered_df.set_index("University")["Percentage"]
        st.bar_chart(chart_data)
        
        # Stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Average", f"{filtered_df['Percentage'].mean():.1f}%")
        with col2:
            st.metric("Highest", f"{filtered_df['Percentage'].max():.1f}%")
        with col3:
            st.metric("Lowest", f"{filtered_df['Percentage'].min():.1f}%")
        
        # Details
        st.subheader("Detailed Breakdown")
        st.dataframe(filtered_df[["University", "Completed", "Total", "Percentage"]].sort_values("Percentage", ascending=False), use_container_width=True)

elif menu == "Reports":
    st.title("📊 Reports")
    st.markdown("---")
    
    report_type = st.selectbox("Report Type", ["Summary Report", "Export Data"])
    
    if report_type == "Summary Report":
        summary_df = get_summary_stats()
        if not summary_df.empty:
            st.dataframe(summary_df, use_container_width=True)
            
            # Download
            csv = summary_df.to_csv(index=False)
            st.download_button("Download CSV", csv, "summary_report.csv", "text/csv")
    
    else:
        if st.button("Export All Data"):
            all_data = []
            for uni_code in UNIVERSITIES.keys():
                df = get_university_progress(uni_code)
                df["University"] = UNIVERSITIES[uni_code]["name"]
                all_data.append(df)
            
            if all_data:
                combined = pd.concat(all_data, ignore_index=True)
                csv = combined.to_csv(index=False)
                st.download_button("Download CSV", csv, "all_data.csv", "text/csv")

else:
    st.title("ℹ️ About")
    st.markdown("---")
    
    st.markdown("""
    ### 🎯 mahaSTRIDE Project Tracker
    
    **Duration:** 10 Weeks (50 Days)  
    **Universities:** 7 Participating Universities  
    **Frameworks:** SAMARTH, NEP, AEGIS, IKS
    
    ### 🏛️ Universities
    
    1. **Mumbai University** - Ms Sneha, Shubham
    2. **SSPU Pune** - Mr Jagan  
    3. **COEP Tech University** - Mr Vaibhav
    4. **Amravati University** - Mr Pratham
    5. **Nagpur University** - Ms Anjali
    6. **KBCNMU Jalgaon University** - Mr Nitish
    7. **BAMU University Aurangabad** - Mr Atharv
    
    ### 👨‍💻 Developer
    
    Developed for **Dr. Harshal**
    """)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>© 2024 mahaSTRIDE Project Tracker | Developed for Dr. Harshal</p>", unsafe_allow_html=True)
