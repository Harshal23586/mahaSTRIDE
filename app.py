import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import json

# Page configuration must be the first Streamlit command
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
    .status-box {
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #e0e0e0;
    }
    .warning {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
    .success-card {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        border-radius: 5px;
    }
    .info-card {
        background-color: #d1ecf1;
        border-left: 4px solid #17a2b8;
        padding: 1rem;
        border-radius: 5px;
    }
    .stButton > button {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Task schedule definition
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

# University data
UNIVERSITIES = {
    "MU": {"name": "Mumbai University", "coordinators": "Ms Sneha, Shubham"},
    "SSPU": {"name": "SSPU Pune", "coordinators": "Mr Jagan"},
    "COEP": {"name": "COEP Tech University", "coordinators": "Mr Vaibhav"},
    "AU": {"name": "Amravati University", "coordinators": "Mr Pratham"},
    "NU": {"name": "Nagpur University", "coordinators": "Ms Anjali"},
    "KBCNMU": {"name": "KBCNMU Jalgaon University", "coordinators": "Mr Nitish"},
    "BAMU": {"name": "BAMU University Aurangabad", "coordinators": "Mr Atharv"},
}

# Data management functions
def load_data():
    """Load progress data from JSON file"""
    if os.path.exists("progress_data.json"):
        with open("progress_data.json", "r") as f:
            return json.load(f)
    else:
        # Initialize empty progress data
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
    with open("progress_data.json", "w") as f:
        json.dump(data, f, indent=2)

def update_task_status(university_code, day, status, remarks=""):
    """Update task status for a specific university and day"""
    data = load_data()
    if university_code in data and str(day) in data[university_code]:
        data[university_code][str(day)]["status"] = status
        data[university_code][str(day)]["remarks"] = remarks
        data[university_code][str(day)]["updated_at"] = datetime.now().isoformat()
        save_data(data)
        return True
    return False

def get_university_progress(university_code):
    """Get progress DataFrame for a specific university"""
    data = load_data()
    if university_code not in data:
        return pd.DataFrame()
    
    records = []
    for day in range(1, 51):
        task_data = data[university_code].get(str(day), {})
        framework, task_name = TASK_SCHEDULE.get(day, ("Unknown", "Unknown Task"))
        records.append({
            "day": day,
            "framework": framework,
            "task_name": task_name,
            "status": task_data.get("status", "pending"),
            "remarks": task_data.get("remarks", ""),
            "updated_at": task_data.get("updated_at", "")
        })
    
    return pd.DataFrame(records)

def get_summary_stats():
    """Get summary statistics for all universities"""
    data = load_data()
    stats = []
    
    for uni_code, uni_info in UNIVERSITIES.items():
        uni_data = data.get(uni_code, {})
        total = 50
        completed = sum(1 for day_data in uni_data.values() if day_data.get("status") == "completed")
        in_progress = sum(1 for day_data in uni_data.values() if day_data.get("status") == "in_progress")
        pending = total - completed - in_progress
        
        stats.append({
            "University": uni_info["name"],
            "Code": uni_code,
            "Coordinators": uni_info["coordinators"],
            "Total Tasks": total,
            "Completed": completed,
            "In Progress": in_progress,
            "Pending": pending,
            "Completion %": round((completed / total * 100), 2) if total > 0 else 0
        })
    
    return pd.DataFrame(stats)

def get_framework_wise_progress(university_code=None):
    """Get framework-wise progress"""
    data = load_data()
    frameworks = ["SAMARTH", "NEP", "AEGIS", "IKS"]
    framework_days = {
        "SAMARTH": list(range(1, 26)),
        "NEP": list(range(26, 36)),
        "AEGIS": list(range(36, 43)),
        "IKS": list(range(43, 51))
    }
    
    records = []
    universities_to_process = [university_code] if university_code else list(UNIVERSITIES.keys())
    
    for uni_code in universities_to_process:
        if uni_code not in data:
            continue
        
        uni_name = UNIVERSITIES[uni_code]["name"]
        uni_data = data[uni_code]
        
        for framework in frameworks:
            days = framework_days[framework]
            total = len(days)
            completed = sum(1 for day in days if uni_data.get(str(day), {}).get("status") == "completed")
            
            records.append({
                "framework": framework,
                "university": uni_name,
                "university_code": uni_code,
                "total_tasks": total,
                "completed": completed,
                "completion_percentage": round((completed / total * 100), 2) if total > 0 else 0
            })
    
    return pd.DataFrame(records)

# Initialize data on first run
if not os.path.exists("progress_data.json"):
    load_data()  # This creates the initial data

# Project timeline
project_start_date = datetime(2024, 11, 1)
current_day = min((datetime.now() - project_start_date).days + 1, 50)
if current_day < 1:
    current_day = 1

# Sidebar navigation
with st.sidebar:
    st.title("📊 mahaSTRIDE")
    st.markdown("---")
    
    page = st.radio(
        "Navigation",
        ["Dashboard", "University Progress", "Task Updates", "Framework Analysis", "Reports", "About"]
    )
    
    st.markdown("---")
    
    # Project timeline info
    st.markdown("### 📅 Timeline")
    st.progress(current_day / 50)
    st.write(f"**Day:** {current_day} / 50")
    st.write(f"**Progress:** {(current_day/50*100):.1f}%")
    
    st.markdown("---")
    
    # Overall progress
    summary = get_summary_stats()
    if not summary.empty:
        total_completed = summary['Completed'].sum()
        total_tasks = summary['Total Tasks'].sum()
        overall_progress = (total_completed / total_tasks * 100) if total_tasks > 0 else 0
        st.metric("Overall Progress", f"{overall_progress:.1f}%")

# Main content
if page == "Dashboard":
    st.markdown('<div class="main-header"><h1>🏠 mahaSTRIDE Dashboard</h1><p>Project Progress Tracking System</p></div>', unsafe_allow_html=True)
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    summary = get_summary_stats()
    if not summary.empty:
        total_tasks = summary['Total Tasks'].sum()
        total_completed = summary['Completed'].sum()
        overall_completion = (total_completed / total_tasks * 100) if total_tasks > 0 else 0
        
        with col1:
            st.metric("📋 Total Tasks", f"{total_tasks}")
        with col2:
            st.metric("✅ Completed Tasks", f"{total_completed}")
        with col3:
            st.metric("📊 Completion Rate", f"{overall_completion:.1f}%")
        with col4:
            st.metric("🏛️ Universities", "7")
    
    st.markdown("---")
    
    # University Progress Overview
    st.subheader("📈 University-wise Progress")
    
    if not summary.empty:
        # Create bar chart
        chart_data = summary[['University', 'Completion %']].copy()
        st.bar_chart(chart_data.set_index('University'))
        
        # Detailed table
        with st.expander("View Detailed Statistics"):
            st.dataframe(summary, use_container_width=True)
    
    # Current Day Tasks
    st.markdown("---")
    st.subheader("📅 Today's Tasks")
    
    if current_day <= 50:
        framework, task = TASK_SCHEDULE[current_day]
        st.info(f"**Day {current_day} - {framework} Framework**\n\n**Task:** {task}")
    else:
        st.success("🎉 Project Completed! Congratulations to all teams!")

elif page == "University Progress":
    st.title("🏛️ University Progress Tracking")
    st.markdown("---")
    
    selected_university = st.selectbox("Select University", list(UNIVERSITIES.keys()), format_func=lambda x: UNIVERSITIES[x]["name"])
    
    if selected_university:
        uni_info = UNIVERSITIES[selected_university]
        st.info(f"**Coordinators:** {uni_info['coordinators']}")
        
        progress_df = get_university_progress(selected_university)
        
        if not progress_df.empty:
            # Summary metrics
            total = len(progress_df)
            completed = len(progress_df[progress_df['status'] == 'completed'])
            in_progress = len(progress_df[progress_df['status'] == 'in_progress'])
            pending = total - completed - in_progress
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Tasks", total)
            with col2:
                st.metric("Completed", completed)
            with col3:
                st.metric("In Progress", in_progress)
            with col4:
                st.metric("Pending", pending)
            
            # Progress gauge
            completion_rate = (completed / total * 100) if total > 0 else 0
            st.progress(completion_rate / 100)
            st.caption(f"Overall Progress: {completion_rate:.1f}%")
            
            # Detailed table
            st.subheader("Task-wise Progress")
            
            # Color coding function
            def color_status(val):
                colors = {
                    'completed': 'background-color: #90EE90',
                    'in_progress': 'background-color: #FFD700',
                    'pending': 'background-color: #FFB6C1'
                }
                return colors.get(val, '')
            
            styled_df = progress_df.style.applymap(color_status, subset=['status'])
            st.dataframe(styled_df, use_container_width=True, height=400)

elif page == "Task Updates":
    st.title("✅ Task Status Updates")
    st.markdown("---")
    
    st.warning("⚠️ Coordinator Access Only - Update task status for your university")
    
    university_code = st.selectbox("Select Your University", list(UNIVERSITIES.keys()), format_func=lambda x: UNIVERSITIES[x]["name"])
    
    if university_code:
        progress_df = get_university_progress(university_code)
        
        if not progress_df.empty:
            pending_tasks = progress_df[progress_df['status'].isin(['pending', 'in_progress'])]
            
            if not pending_tasks.empty:
                st.subheader("Update Task Status")
                
                # Create task options
                task_options = {row['day']: f"Day {row['day']}: {row['task_name']} ({row['framework']})" for _, row in pending_tasks.iterrows()}
                selected_day = st.selectbox("Select Task", options=list(task_options.keys()), format_func=lambda x: task_options[x])
                
                task_details = pending_tasks[pending_tasks['day'] == selected_day].iloc[0]
                
                col1, col2 = st.columns(2)
                with col1:
                    st.info(f"**Framework:** {task_details['framework']}\n\n**Task:** {task_details['task_name']}")
                with col2:
                    st.warning(f"**Current Status:** {task_details['status'].upper()}")
                
                new_status = st.radio("Update Status", ['in_progress', 'completed'], format_func=lambda x: "🔄 In Progress" if x == 'in_progress' else "✅ Completed")
                remarks = st.text_area("Remarks (optional)")
                
                if st.button("Update Status", type="primary"):
                    if update_task_status(university_code, selected_day, new_status, remarks):
                        st.success(f"✅ Task status updated to {new_status}!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to update status")
            else:
                st.success("🎉 All tasks completed for your university!")

elif page == "Framework Analysis":
    st.title("📚 Framework-wise Analysis")
    st.markdown("---")
    
    frameworks = ["SAMARTH", "NEP", "AEGIS", "IKS"]
    selected_framework = st.selectbox("Select Framework", frameworks)
    
    framework_progress = get_framework_wise_progress()
    
    if not framework_progress.empty:
        filtered_data = framework_progress[framework_progress['framework'] == selected_framework]
        
        if not filtered_data.empty:
            # Create bar chart
            chart_data = filtered_data.set_index('university')['completion_percentage']
            st.bar_chart(chart_data)
            
            # Statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Average Completion", f"{filtered_data['completion_percentage'].mean():.1f}%")
            with col2:
                st.metric("Highest Completion", f"{filtered_data['completion_percentage'].max():.1f}%")
            with col3:
                st.metric("Lowest Completion", f"{filtered_data['completion_percentage'].min():.1f}%")
            
            # Detailed table
            st.subheader("Detailed Breakdown")
            st.dataframe(filtered_data[['university', 'total_tasks', 'completed', 'completion_percentage']].sort_values('completion_percentage', ascending=False), use_container_width=True)
            
            # List tasks
            framework_days = {
                "SAMARTH": (1, 25),
                "NEP": (26, 35),
                "AEGIS": (36, 42),
                "IKS": (43, 50)
            }
            
            if selected_framework in framework_days:
                start_day, end_day = framework_days[selected_framework]
                with st.expander(f"View Tasks in {selected_framework} Framework"):
                    for day in range(start_day, end_day + 1):
                        _, task = TASK_SCHEDULE[day]
                        st.write(f"**Day {day}:** {task}")

elif page == "Reports":
    st.title("📊 Reports & Analytics")
    st.markdown("---")
    
    report_type = st.selectbox("Select Report Type", ["Overall Progress", "University Comparison", "Export Data"])
    
    if report_type == "Overall Progress":
        st.subheader("Overall Project Status")
        
        summary = get_summary_stats()
        if not summary.empty:
            total_completed = summary['Completed'].sum()
            total_tasks = summary['Total Tasks'].sum()
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Tasks", total_tasks)
            with col2:
                st.metric("Total Completed", total_completed)
            
            # Completion by framework
            framework_progress = get_framework_wise_progress()
            if not framework_progress.empty:
                framework_summary = framework_progress.groupby('framework')['completion_percentage'].mean().reset_index()
                st.subheader("Framework-wise Average Completion")
                st.bar_chart(framework_summary.set_index('framework'))
    
    elif report_type == "University Comparison":
        st.subheader("University Performance Comparison")
        
        summary = get_summary_stats()
        if not summary.empty:
            st.dataframe(summary[['University', 'Completion %', 'Completed', 'In Progress', 'Pending']].sort_values('Completion %', ascending=False), use_container_width=True)
    
    elif report_type == "Export Data":
        st.subheader("Export Project Data")
        
        export_type = st.radio("Select Export Type", ["Summary Report", "All Universities Data"])
        
        if export_type == "Summary Report":
            if st.button("Generate Summary Report"):
                summary = get_summary_stats()
                st.dataframe(summary, use_container_width=True)
                
                # Download button
                csv = summary.to_csv(index=False)
                st.download_button("Download CSV", data=csv, file_name="mahastride_summary.csv", mime="text/csv")
        else:
            if st.button("Export All Data"):
                all_data = []
                for uni_code in UNIVERSITIES.keys():
                    df = get_university_progress(uni_code)
                    df['university'] = UNIVERSITIES[uni_code]['name']
                    all_data.append(df)
                
                if all_data:
                    combined_df = pd.concat(all_data, ignore_index=True)
                    csv = combined_df.to_csv(index=False)
                    st.download_button("Download CSV", data=csv, file_name="all_universities_data.csv", mime="text/csv")

elif page == "About":
    st.title("ℹ️ About mahaSTRIDE Tracker")
    st.markdown("---")
    
    st.markdown("""
    ### 🎯 Project Overview
    
    **mahaSTRIDE** is a comprehensive 10-week (50-day) project involving 7 universities across Maharashtra.
    
    ### 📚 Frameworks
    
    - **SAMARTH Framework** (Days 1-25): Core implementation
    - **NEP Framework** (Days 26-35): National Education Policy alignment
    - **AEGIS Framework** (Days 36-42): Security and governance
    - **IKS Framework** (Days 43-50): Indian Knowledge Systems
    
    ### 🏛️ Participating Universities
    
    1. **Mumbai University** - Ms Sneha, Shubham
    2. **SSPU Pune** - Mr Jagan
    3. **COEP Tech University** - Mr Vaibhav
    4. **Amravati University** - Mr Pratham
    5. **Nagpur University** - Ms Anjali
    6. **KBCNMU Jalgaon University** - Mr Nitish
    7. **BAMU University Aurangabad** - Mr Atharv
    
    ### 👨‍💻 Developer
    
    Developed for **Dr. Harshal** to track and manage project progress effectively.
    
    ### 📊 Features
    
    - Real-time progress tracking
    - University-wise analytics
    - Framework performance metrics
    - Data export capabilities
    - Interactive visualizations
    """)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>© 2024 mahaSTRIDE Project Tracker | Developed for Dr. Harshal</p>", unsafe_allow_html=True)
