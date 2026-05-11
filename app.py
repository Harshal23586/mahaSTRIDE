import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

from database import DatabaseManager
from models import TaskStatus, ProjectTimeline, TASK_SCHEDULE

# Load environment variables
load_dotenv()

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
        background-color: #1E3A8A;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .status-box {
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    .metric-card {
        background-color: #F3F4F6;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
    .warning {
        background-color: #FEF3C7;
        border-left: 4px solid #F59E0B;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize database
@st.cache_resource
def init_db():
    db = DatabaseManager()
    db.initialize_data()
    return db

db = init_db()

# Initialize project timeline (assuming project starts today)
# In production, you might want to set a fixed start date
project_start_date = datetime(2024, 1, 1)  # Adjust this date as needed
timeline = ProjectTimeline(start_date=project_start_date)

# Sidebar navigation
st.sidebar.title("📊 mahaSTRIDE Tracker")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "University Progress", "Task Updates", "Framework Analysis", "Reports"]
)

st.sidebar.markdown("---")
st.sidebar.info(
    """
    **Project Timeline:** 50 Days  
    **Current Day:** {}  
    **Project Status:** {}  
    """.format(
        timeline.get_current_day(),
        "Ongoing" if timeline.get_current_day() <= timeline.total_days else "Completed"
    )
)

# Main content
if page == "Dashboard":
    st.title("🏠 mahaSTRIDE Project Dashboard")
    st.markdown("---")
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    summary_stats = db.get_summary_stats()
    
    with col1:
        total_tasks = summary_stats['Total Tasks'].sum() if not summary_stats.empty else 0
        st.metric("Total Tasks", f"{total_tasks}")
    
    with col2:
        total_completed = summary_stats['Completed'].sum() if not summary_stats.empty else 0
        st.metric("Tasks Completed", f"{total_completed}")
    
    with col3:
        overall_completion = (total_completed / total_tasks * 100) if total_tasks > 0 else 0
        st.metric("Overall Completion", f"{overall_completion:.1f}%")
    
    with col4:
        active_universities = len(summary_stats) if not summary_stats.empty else 0
        st.metric("Active Universities", f"{active_universities}")
    
    st.markdown("---")
    
    # University Progress Overview
    st.subheader("📈 University-wise Progress")
    
    if not summary_stats.empty:
        fig = px.bar(
            summary_stats,
            x='University',
            y='Completion %',
            color='Completion %',
            color_continuous_scale='Viridis',
            title="Completion Percentage by University",
            text='Completion %'
        )
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed table
        with st.expander("View Detailed Statistics"):
            st.dataframe(summary_stats, use_container_width=True)
    else:
        st.warning("No data available")
    
    # Current Day Tasks
    st.markdown("---")
    st.subheader("📅 Today's Tasks")
    current_day = timeline.get_current_day()
    
    if current_day <= timeline.total_days:
        current_framework, current_task = TASK_SCHEDULE[current_day]
        
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**Day {current_day}**")
            st.write(f"**Framework:** {current_framework}")
            st.write(f"**Task:** {current_task}")
        
        with col2:
            st.warning(f"**Project Deadline:** {timeline.get_date_for_day(timeline.total_days).strftime('%Y-%m-%d')}")
            st.write(f"**Days Remaining:** {timeline.total_days - current_day}")
    else:
        st.success("🎉 Project Completed! Congratulations to all teams!")
    
    # Alerts for delayed tasks
    st.markdown("---")
    st.subheader("⚠️ Attention Required")
    
    # You can add logic here to show universities behind schedule

elif page == "University Progress":
    st.title("🏛️ University-wise Progress Tracking")
    st.markdown("---")
    
    # University selector
    universities_data = db.get_all_universities_progress()
    university_names = list(universities_data.keys())
    
    selected_university = st.selectbox("Select University", university_names)
    
    if selected_university:
        uni_data = universities_data[selected_university]
        
        # University header
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**University Code:** {uni_data['code']}")
        with col2:
            st.info(f"**Coordinators:** {uni_data['coordinators']}")
        
        progress_df = uni_data['progress']
        
        if not progress_df.empty:
            # Summary metrics
            total = len(progress_df)
            completed = len(progress_df[progress_df['status'] == TaskStatus.COMPLETED.value])
            in_progress = len(progress_df[progress_df['status'] == TaskStatus.IN_PROGRESS.value])
            pending = len(progress_df[progress_df['status'] == TaskStatus.PENDING.value])
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Tasks", total)
            with col2:
                st.metric("Completed", completed, delta=f"{(completed/total*100):.1f}%")
            with col3:
                st.metric("In Progress", in_progress)
            with col4:
                st.metric("Pending", pending)
            
            # Progress gauge
            completion_rate = (completed / total * 100) if total > 0 else 0
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=completion_rate,
                title={'text': "Overall Progress"},
                domain={'x': [0, 1], 'y': [0, 1]},
                gauge={'axis': {'range': [None, 100]},
                      'bar': {'color': "darkblue"},
                      'steps': [
                          {'range': [0, 33], 'color': "lightgray"},
                          {'range': [33, 66], 'color': "gray"}],
                      'threshold': {'line': {'color': "red", 'width': 4},
                                   'thickness': 0.75, 'value': 90}}))
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
            
            # Detailed progress table
            st.subheader("Task-wise Progress")
            
            # Color coding for status
            def color_status(val):
                colors = {
                    TaskStatus.COMPLETED.value: 'background-color: #90EE90',
                    TaskStatus.IN_PROGRESS.value: 'background-color: #FFD700',
                    TaskStatus.PENDING.value: 'background-color: #FFB6C1'
                }
                return colors.get(val, '')
            
            styled_df = progress_df.style.applymap(color_status, subset=['status'])
            st.dataframe(styled_df, use_container_width=True, height=400)

elif page == "Task Updates":
    st.title("✅ Task Status Updates")
    st.markdown("---")
    
    st.warning("This section is for coordinators to update task status")
    
    # Authentication placeholder (you should implement proper authentication)
    university_code = st.selectbox(
        "Select Your University",
        ["MU", "SSPU", "COEP", "AU", "NU", "KBCNMU", "BAMU"]
    )
    
    # Get current progress to show pending tasks
    uni_progress = db.get_university_progress(university_code)
    
    if not uni_progress.empty:
        pending_tasks = uni_progress[uni_progress['status'].isin([TaskStatus.PENDING.value, TaskStatus.IN_PROGRESS.value])]
        
        if not pending_tasks.empty:
            st.subheader("Update Task Status")
            
            # Task selection
            selected_day = st.selectbox(
                "Select Task Day",
                pending_tasks['day'].tolist(),
                format_func=lambda x: f"Day {x}: {pending_tasks[pending_tasks['day']==x]['task_name'].iloc[0]}"
            )
            
            # Get task details
            task_details = pending_tasks[pending_tasks['day'] == selected_day].iloc[0]
            
            st.write(f"**Framework:** {task_details['framework']}")
            st.write(f"**Task:** {task_details['task_name']}")
            
            # Status update
            new_status = st.selectbox(
                "Update Status",
                [TaskStatus.IN_PROGRESS.value, TaskStatus.COMPLETED.value]
            )
            
            remarks = st.text_area("Remarks (optional)")
            
            if st.button("Update Status", type="primary"):
                success = db.update_task_status(university_code, selected_day, new_status, remarks)
                if success:
                    st.success(f"✅ Task status updated to {new_status}")
                    st.rerun()
                else:
                    st.error("Failed to update status")
        else:
            st.success("🎉 All tasks completed for your university!")
    else:
        st.error("No data found for your university")

elif page == "Framework Analysis":
    st.title("📚 Framework-wise Analysis")
    st.markdown("---")
    
    # Framework selector
    frameworks = ["SAMARTH", "NEP", "AEGIS", "IKS"]
    selected_framework = st.selectbox("Select Framework", frameworks)
    
    # Get framework-wise progress
    framework_progress = db.get_framework_wise_progress()
    
    if not framework_progress.empty:
        # Filter for selected framework
        filtered_data = framework_progress[framework_progress['framework'] == selected_framework]
        
        # Bar chart
        fig = px.bar(
            filtered_data,
            x='university',
            y='completion_percentage',
            color='completion_percentage',
            color_continuous_scale='Blues',
            title=f"{selected_framework} Framework - University-wise Completion",
            text='completion_percentage'
        )
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed table
        st.subheader("Framework Details")
        
        # Get tasks for the framework
        framework_tasks = {day: (fw, task) for day, (fw, task) in TASK_SCHEDULE.items() if fw == selected_framework}
        
        st.write(f"**Total Tasks in {selected_framework}:** {len(framework_tasks)}")
        st.write(f"**Days:** Day {min(framework_tasks.keys())} to Day {max(framework_tasks.keys())}")
        
        with st.expander("View All Tasks"):
            for day, (_, task) in framework_tasks.items():
                st.write(f"Day {day}: {task}")

elif page == "Reports":
    st.title("📊 Reports & Analytics")
    st.markdown("---")
    
    report_type = st.selectbox(
        "Select Report Type",
        ["Overall Progress Report", "University Comparison", "Task Completion Timeline", "Export Data"]
    )
    
    if report_type == "Overall Progress Report":
        st.subheader("Overall Project Status")
        
        summary = db.get_summary_stats()
        if not summary.empty:
            # Summary statistics
            total_completed = summary['Completed'].sum()
            total_tasks = summary['Total Tasks'].sum()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Tasks Across All Universities", total_tasks)
            with col2:
                st.metric("Total Completed Tasks", total_completed)
            with col3:
                st.metric("Overall Completion Rate", f"{(total_completed/total_tasks*100):.1f}%")
            
            # Completion heatmap
            pivot_data = []
            for uni in summary['University']:
                uni_progress = db.get_university_progress(
                    summary[summary['University'] == uni]['Code'].iloc[0]
                )
                for _, row in uni_progress.iterrows():
                    pivot_data.append({
                        'University': uni,
                        'Day': row['day'],
                        'Status': row['status']
                    })
            
            if pivot_data:
                heatmap_df = pd.DataFrame(pivot_data)
                status_order = ['completed', 'in_progress', 'pending']
                heatmap_df['Status_Num'] = heatmap_df['Status'].map({s: i for i, s in enumerate(status_order)})
                
                fig = px.density_heatmap(
                    heatmap_df,
                    x='Day',
                    y='University',
                    z='Status_Num',
                    title="Project Progress Heatmap",
                    color_continuous_scale=['red', 'yellow', 'green'],
                    labels={'Status_Num': 'Progress (0=Pending, 1=In Progress, 2=Completed)'}
                )
                st.plotly_chart(fig, use_container_width=True)
    
    elif report_type == "University Comparison":
        st.subheader("University Performance Comparison")
        
        summary = db.get_summary_stats()
        if not summary.empty:
            # Radar chart for comparison
            fig = go.Figure()
            
            for _, uni in summary.iterrows():
                fig.add_trace(go.Scatterpolar(
                    r=[uni['Completion %'], uni['Completed'], uni['In Progress']],
                    theta=['Completion %', 'Completed Tasks', 'In Progress'],
                    fill='toself',
                    name=uni['University']
                ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100]
                    )),
                showlegend=True,
                title="University Performance Radar Chart"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Comparison table
            st.dataframe(summary.sort_values('Completion %', ascending=False), use_container_width=True)
    
    elif report_type == "Task Completion Timeline":
        st.subheader("Task Completion Timeline Analysis")
        
        # Show progress over days
        all_data = []
        universities_data = db.get_all_universities_progress()
        
        for uni_name, uni_data in universities_data.items():
            progress_df = uni_data['progress']
            for _, row in progress_df.iterrows():
                if row['status'] == TaskStatus.COMPLETED.value:
                    all_data.append({
                        'University': uni_name,
                        'Day': row['day'],
                        'Task': row['task_name']
                    })
        
        if all_data:
            timeline_df = pd.DataFrame(all_data)
            completion_by_day = timeline_df.groupby('Day').size().reset_index(name='Completed Tasks')
            
            fig = px.line(
                completion_by_day,
                x='Day',
                y='Completed Tasks',
                title="Tasks Completed Over Time",
                markers=True
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    elif report_type == "Export Data":
        st.subheader("Export Project Data")
        
        # Export options
        export_type = st.selectbox("Select data to export", ["All Universities", "Single University"])
        
        if export_type == "Single University":
            uni_name = st.selectbox("Select University", list(db.get_all_universities_progress().keys()))
            if st.button("Export to CSV"):
                uni_data = db.get_university_progress(
                    db.get_all_universities_progress()[uni_name]['code']
                )
                csv = uni_data.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"{uni_name}_progress.csv",
                    mime="text/csv"
                )
        else:
            if st.button("Export Summary to CSV"):
                summary = db.get_summary_stats()
                csv = summary.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="mahastride_summary.csv",
                    mime="text/csv"
                )

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>mahaSTRIDE Project Tracker | Developed for Dr. Harshal</div>",
    unsafe_allow_html=True
)
