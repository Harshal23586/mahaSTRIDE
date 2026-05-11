import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
import sys
from typing import Dict, List, Optional

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
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
        background-color: #F3F4F6;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        transition: transform 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .warning {
        background-color: #FEF3C7;
        border-left: 4px solid #F59E0B;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
    .success-card {
        background-color: #D1FAE5;
        border-left: 4px solid #10B981;
        padding: 1rem;
        border-radius: 5px;
    }
    .info-card {
        background-color: #DBEAFE;
        border-left: 4px solid #3B82F6;
        padding: 1rem;
        border-radius: 5px;
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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

# Import database modules with error handling
try:
    from database import DatabaseManager
    from models import TaskStatus, ProjectTimeline, TASK_SCHEDULE, University, Task, TaskProgress
except ImportError as e:
    st.error(f"Error importing modules: {e}")
    st.info("Please make sure all files are in the correct directory structure")
    st.stop()

# Initialize database
@st.cache_resource
def init_db():
    try:
        db = DatabaseManager()
        db.initialize_data()
        return db
    except Exception as e:
        st.error(f"Database initialization error: {e}")
        st.info("Creating new database...")
        # Try to recreate database
        if os.path.exists("mahastride.db"):
            os.remove("mahastride.db")
        db = DatabaseManager()
        db.initialize_data()
        return db

try:
    db = init_db()
except Exception as e:
    st.error(f"Failed to initialize database: {e}")
    st.stop()

# Initialize project timeline
project_start_date = datetime(2024, 11, 1)  # Updated to current date
timeline = ProjectTimeline(start_date=project_start_date)

# Sidebar navigation
with st.sidebar:
    st.image("https://via.placeholder.com/300x100?text=mahaSTRIDE", use_column_width=True)
    st.title("📊 Navigation")
    st.markdown("---")
    
    page = st.radio(
        "Menu",
        ["🏠 Dashboard", "🏛️ University Progress", "✅ Task Updates", "📚 Framework Analysis", "📊 Reports", "ℹ️ About"],
        format_func=lambda x: x.split(' ')[1] if ' ' in x else x
    )
    
    st.markdown("---")
    
    # Project timeline info
    current_day = timeline.get_current_day()
    progress_percentage = (current_day / timeline.total_days * 100) if current_day <= timeline.total_days else 100
    
    st.markdown("### 📅 Project Timeline")
    st.progress(progress_percentage / 100)
    st.write(f"**Day:** {min(current_day, timeline.total_days)} / {timeline.total_days}")
    st.write(f"**Status:** {'🟢 Ongoing' if current_day <= timeline.total_days else '✅ Completed'}")
    
    st.markdown("---")
    
    # Quick stats
    try:
        summary_stats = db.get_summary_stats()
        if not summary_stats.empty:
            total_completed = summary_stats['Completed'].sum()
            total_tasks = summary_stats['Total Tasks'].sum()
            overall_progress = (total_completed / total_tasks * 100) if total_tasks > 0 else 0
            st.markdown("### 📈 Overall Progress")
            st.metric("Completion", f"{overall_progress:.1f}%", delta=f"{overall_progress:.1f}%")
    except:
        pass

# Main content
if page == "🏠 Dashboard":
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    st.title("🏠 mahaSTRIDE Project Dashboard")
    st.markdown("### Tracking Progress Across 7 Universities")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    try:
        summary_stats = db.get_summary_stats()
        
        with col1:
            total_tasks = summary_stats['Total Tasks'].sum() if not summary_stats.empty else 0
            st.markdown(f'''
            <div class="metric-card">
                <h3>📋 Total Tasks</h3>
                <h2>{total_tasks}</h2>
                <small>Across all universities</small>
            </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            total_completed = summary_stats['Completed'].sum() if not summary_stats.empty else 0
            st.markdown(f'''
            <div class="metric-card">
                <h3>✅ Completed</h3>
                <h2>{total_completed}</h2>
                <small>Tasks finished</small>
            </div>
            ''', unsafe_allow_html=True)
        
        with col3:
            overall_completion = (total_completed / total_tasks * 100) if total_tasks > 0 else 0
            st.markdown(f'''
            <div class="metric-card">
                <h3>📊 Completion</h3>
                <h2>{overall_completion:.1f}%</h2>
                <small>Overall progress</small>
            </div>
            ''', unsafe_allow_html=True)
        
        with col4:
            active_universities = len(summary_stats) if not summary_stats.empty else 0
            st.markdown(f'''
            <div class="metric-card">
                <h3>🏛️ Universities</h3>
                <h2>{active_universities}/7</h2>
                <small>Active participants</small>
            </div>
            ''', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error loading metrics: {e}")
    
    st.markdown("---")
    
    # University Progress Overview
    st.subheader("📈 University-wise Progress")
    
    try:
        if not summary_stats.empty:
            # Create interactive bar chart
            fig = px.bar(
                summary_stats,
                x='University',
                y='Completion %',
                color='Completion %',
                color_continuous_scale='Viridis',
                title="<b>Completion Percentage by University</b>",
                text='Completion %',
                height=500
            )
            fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig.update_layout(
                xaxis_title="University",
                yaxis_title="Completion Percentage (%)",
                showlegend=False,
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Detailed table with color coding
            with st.expander("📋 View Detailed Statistics", expanded=False):
                styled_df = summary_stats.style.background_gradient(subset=['Completion %'], cmap='YlOrRd')
                st.dataframe(styled_df, use_container_width=True)
        else:
            st.warning("No data available. Please initialize the database.")
    except Exception as e:
        st.error(f"Error loading university progress: {e}")
    
    # Current Day Tasks
    st.markdown("---")
    st.subheader("📅 Today's Tasks")
    current_day = timeline.get_current_day()
    
    if current_day <= timeline.total_days:
        current_framework, current_task = TASK_SCHEDULE[current_day]
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f'''
            <div class="info-card">
                <h3>🎯 Day {current_day}</h3>
                <p><strong>Framework:</strong> {current_framework}</p>
                <p><strong>Task:</strong> {current_task}</p>
                <p><strong>Due Date:</strong> {timeline.get_date_for_day(current_day).strftime('%Y-%m-%d')}</p>
            </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            days_remaining = timeline.total_days - current_day
            st.markdown(f'''
            <div class="warning">
                <h3>⏰ Timeline</h3>
                <p><strong>Days Remaining:</strong> {days_remaining}</p>
                <p><strong>Project End:</strong> {timeline.get_date_for_day(timeline.total_days).strftime('%Y-%m-%d')}</p>
                <p><strong>Current Progress:</strong> {(current_day/timeline.total_days*100):.1f}%</p>
            </div>
            ''', unsafe_allow_html=True)
    else:
        st.markdown(f'''
        <div class="success-card">
            <h2>🎉 Project Completed!</h2>
            <p>Congratulations to all teams on successfully completing the mahaSTRIDE project!</p>
        </div>
        ''', unsafe_allow_html=True)

elif page == "🏛️ University Progress":
    st.title("🏛️ University-wise Progress Tracking")
    st.markdown("---")
    
    try:
        # University selector
        universities_data = db.get_all_universities_progress()
        university_names = list(universities_data.keys())
        
        if university_names:
            selected_university = st.selectbox("Select University", university_names)
            
            if selected_university:
                uni_data = universities_data[selected_university]
                
                # University header
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f'''
                    <div class="info-card">
                        <h3>🏛️ {selected_university}</h3>
                        <p><strong>Code:</strong> {uni_data['code']}</p>
                    </div>
                    ''', unsafe_allow_html=True)
                with col2:
                    st.markdown(f'''
                    <div class="info-card">
                        <h3>👥 Coordinators</h3>
                        <p>{uni_data['coordinators']}</p>
                    </div>
                    ''', unsafe_allow_html=True)
                
                progress_df = uni_data['progress']
                
                if not progress_df.empty:
                    # Summary metrics
                    total = len(progress_df)
                    completed = len(progress_df[progress_df['status'] == 'completed'])
                    in_progress = len(progress_df[progress_df['status'] == 'in_progress'])
                    pending = len(progress_df[progress_df['status'] == 'pending'])
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("📋 Total Tasks", total)
                    with col2:
                        st.metric("✅ Completed", completed, delta=f"{(completed/total*100):.1f}%")
                    with col3:
                        st.metric("🔄 In Progress", in_progress)
                    with col4:
                        st.metric("⏳ Pending", pending)
                    
                    # Progress gauge
                    completion_rate = (completed / total * 100) if total > 0 else 0
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number+delta",
                        value=completion_rate,
                        title={'text': "Overall Progress", 'font': {'size': 24}},
                        domain={'x': [0, 1], 'y': [0, 1]},
                        gauge={
                            'axis': {'range': [None, 100], 'tickwidth': 1},
                            'bar': {'color': "#667eea"},
                            'steps': [
                                {'range': [0, 33], 'color': "lightgray"},
                                {'range': [33, 66], 'color': "gray"},
                                {'range': [66, 100], 'color': "darkgray"}
                            ],
                            'threshold': {
                                'line': {'color': "red", 'width': 4},
                                'thickness': 0.75,
                                'value': 90
                            }
                        }
                    ))
                    fig.update_layout(height=300, margin=dict(t=0, b=0, l=0, r=0))
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Detailed progress table
                    st.subheader("📋 Task-wise Progress")
                    
                    # Color coding for status
                    def color_status(val):
                        colors = {
                            'completed': 'background-color: #90EE90',
                            'in_progress': 'background-color: #FFD700',
                            'pending': 'background-color: #FFB6C1'
                        }
                        return colors.get(val, '')
                    
                    styled_df = progress_df.style.applymap(color_status, subset=['status'])
                    st.dataframe(styled_df, use_container_width=True, height=400)
        else:
            st.warning("No university data found. Please check database initialization.")
    except Exception as e:
        st.error(f"Error loading university progress: {e}")

elif page == "✅ Task Updates":
    st.title("✅ Task Status Updates")
    st.markdown("---")
    
    st.markdown('<div class="warning">⚠️ This section is for coordinators to update task status</div>', unsafe_allow_html=True)
    
    try:
        # University selection
        university_code = st.selectbox(
            "Select Your University",
            ["MU", "SSPU", "COEP", "AU", "NU", "KBCNMU", "BAMU"],
            format_func=lambda x: {
                "MU": "Mumbai University",
                "SSPU": "SSPU Pune",
                "COEP": "COEP Tech University",
                "AU": "Amravati University",
                "NU": "Nagpur University",
                "KBCNMU": "KBCNMU Jalgaon University",
                "BAMU": "BAMU University Aurangabad"
            }.get(x, x)
        )
        
        # Get current progress
        uni_progress = db.get_university_progress(university_code)
        
        if not uni_progress.empty:
            pending_tasks = uni_progress[uni_progress['status'].isin(['pending', 'in_progress'])]
            
            if not pending_tasks.empty:
                st.subheader("📝 Update Task Status")
                
                # Task selection with better formatting
                task_options = {
                    row['day']: f"Day {row['day']}: {row['task_name']} - {row['framework']}"
                    for _, row in pending_tasks.iterrows()
                }
                
                selected_day = st.selectbox(
                    "Select Task",
                    options=list(task_options.keys()),
                    format_func=lambda x: task_options[x]
                )
                
                # Get task details
                task_details = pending_tasks[pending_tasks['day'] == selected_day].iloc[0]
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f'''
                    <div class="info-card">
                        <p><strong>📚 Framework:</strong> {task_details['framework']}</p>
                        <p><strong>📋 Task:</strong> {task_details['task_name']}</p>
                    </div>
                    ''', unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f'''
                    <div class="warning">
                        <p><strong>Current Status:</strong> {task_details['status'].upper()}</p>
                        <p><strong>Last Updated:</strong> {task_details['updated_at'] if pd.notna(task_details['updated_at']) else 'Never'}</p>
                    </div>
                    ''', unsafe_allow_html=True)
                
                # Status update
                new_status = st.radio(
                    "Update Status",
                    ['in_progress', 'completed'],
                    format_func=lambda x: "🔄 In Progress" if x == 'in_progress' else "✅ Completed"
                )
                
                remarks = st.text_area("📝 Remarks (optional)", placeholder="Add any notes or comments about this task...")
                
                if st.button("🚀 Update Status", type="primary", use_container_width=True):
                    success = db.update_task_status(university_code, selected_day, new_status, remarks)
                    if success:
                        st.success(f"✅ Task status updated to {new_status.upper()} successfully!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("❌ Failed to update status. Please try again.")
            else:
                st.markdown(f'''
                <div class="success-card">
                    <h3>🎉 Congratulations!</h3>
                    <p>All tasks for your university have been completed!</p>
                </div>
                ''', unsafe_allow_html=True)
        else:
            st.error("No data found for your university")
    except Exception as e:
        st.error(f"Error in task updates: {e}")

elif page == "📚 Framework Analysis":
    st.title("📚 Framework-wise Analysis")
    st.markdown("---")
    
    try:
        # Framework selector with icons
        frameworks = {
            "SAMARTH": "📖 SAMARTH Framework (Days 1-25)",
            "NEP": "🎓 NEP Framework (Days 26-35)",
            "AEGIS": "🛡️ AEGIS Framework (Days 36-42)",
            "IKS": "🏛️ IKS Framework (Days 43-50)"
        }
        
        selected_framework = st.selectbox(
            "Select Framework for Analysis",
            list(frameworks.keys()),
            format_func=lambda x: frameworks[x]
        )
        
        # Get framework-wise progress
        framework_progress = db.get_framework_wise_progress()
        
        if not framework_progress.empty:
            # Filter for selected framework
            filtered_data = framework_progress[framework_progress['framework'] == selected_framework]
            
            if not filtered_data.empty:
                # Create bar chart
                fig = px.bar(
                    filtered_data,
                    x='university',
                    y='completion_percentage',
                    color='completion_percentage',
                    color_continuous_scale='Viridis',
                    title=f"<b>{selected_framework} Framework Progress by University</b>",
                    text='completion_percentage',
                    height=500
                )
                fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                fig.update_layout(
                    xaxis_title="University",
                    yaxis_title="Completion Percentage (%)",
                    showlegend=False,
                    hovermode='x unified'
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    avg_completion = filtered_data['completion_percentage'].mean()
                    st.metric("Average Completion", f"{avg_completion:.1f}%")
                with col2:
                    max_completion = filtered_data['completion_percentage'].max()
                    st.metric("Highest Completion", f"{max_completion:.1f}%")
                with col3:
                    min_completion = filtered_data['completion_percentage'].min()
                    st.metric("Lowest Completion", f"{min_completion:.1f}%")
                
                # Detailed table
                st.subheader("📊 Detailed Framework Breakdown")
                st.dataframe(
                    filtered_data[['university', 'total_tasks', 'completed', 'completion_percentage']]
                    .sort_values('completion_percentage', ascending=False),
                    use_container_width=True
                )
                
                # Get tasks for the framework
                framework_tasks = {
                    day: (fw, task) 
                    for day, (fw, task) in TASK_SCHEDULE.items() 
                    if fw == selected_framework
                }
                
                with st.expander(f"📋 View All Tasks in {selected_framework} Framework"):
                    for day in sorted(framework_tasks.keys()):
                        _, task = framework_tasks[day]
                        st.write(f"**Day {day}:** {task}")
            else:
                st.warning(f"No data available for {selected_framework} framework")
        else:
            st.warning("No framework data available")
    except Exception as e:
        st.error(f"Error in framework analysis: {e}")

elif page == "📊 Reports":
    st.title("📊 Reports & Analytics")
    st.markdown("---")
    
    report_type = st.selectbox(
        "Select Report Type",
        ["📈 Overall Progress Report", "📊 University Comparison", "📅 Task Completion Timeline", "💾 Export Data"]
    )
    
    try:
        if report_type == "📈 Overall Progress Report":
            st.subheader("Overall Project Status")
            
            summary = db.get_summary_stats()
            if not summary.empty:
                # Summary statistics
                total_completed = summary['Completed'].sum()
                total_tasks = summary['Total Tasks'].sum()
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("📋 Total Tasks Across All Universities", total_tasks)
                with col2:
                    st.metric("✅ Total Completed Tasks", total_completed)
                with col3:
                    overall_rate = (total_completed/total_tasks*100) if total_tasks > 0 else 0
                    st.metric("📊 Overall Completion Rate", f"{overall_rate:.1f}%")
                
                # Completion heatmap
                st.subheader("📊 Progress Heatmap")
                
                # Prepare data for heatmap
                heatmap_data = []
                for _, uni in summary.iterrows():
                    uni_progress = db.get_university_progress(uni['Code'])
                    for _, row in uni_progress.iterrows():
                        heatmap_data.append({
                            'University': uni['University'],
                            'Day': row['day'],
                            'Status': row['status']
                        })
                
                if heatmap_data:
                    heatmap_df = pd.DataFrame(heatmap_data)
                    status_order = ['completed', 'in_progress', 'pending']
                    heatmap_df['Status_Num'] = heatmap_df['Status'].map({s: i for i, s in enumerate(status_order)})
                    
                    fig = px.density_heatmap(
                        heatmap_df,
                        x='Day',
                        y='University',
                        z='Status_Num',
                        title="Project Progress Heatmap (0=Pending, 1=In Progress, 2=Completed)",
                        color_continuous_scale=['red', 'yellow', 'green'],
                        height=600
                    )
                    st.plotly_chart(fig, use_container_width=True)
        
        elif report_type == "📊 University Comparison":
            st.subheader("University Performance Comparison")
            
            summary = db.get_summary_stats()
            if not summary.empty:
                # Create comparison chart
                fig = px.bar(
                    summary,
                    x='University',
                    y=['Completed', 'In Progress', 'Pending'],
                    title="Task Status Distribution by University",
                    barmode='group',
                    text_auto=True,
                    height=500
                )
                fig.update_layout(
                    xaxis_title="University",
                    yaxis_title="Number of Tasks",
                    legend_title="Status"
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Ranking table
                st.subheader("🏆 University Rankings")
                ranking = summary[['University', 'Completion %', 'Completed', 'Total Tasks']].sort_values('Completion %', ascending=False)
                ranking.index = range(1, len(ranking) + 1)
                st.dataframe(ranking, use_container_width=True)
        
        elif report_type == "📅 Task Completion Timeline":
            st.subheader("Task Completion Timeline Analysis")
            
            # Show progress over days
            all_data = []
            universities_data = db.get_all_universities_progress()
            
            for uni_name, uni_data in universities_data.items():
                progress_df = uni_data['progress']
                for _, row in progress_df.iterrows():
                    if row['status'] == 'completed':
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
                    markers=True,
                    height=500
                )
                fig.update_traces(line=dict(width=3, color='#667eea'), marker=dict(size=8))
                fig.update_layout(
                    xaxis_title="Project Day",
                    yaxis_title="Number of Completed Tasks"
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Cumulative completion
                completion_by_day['Cumulative'] = completion_by_day['Completed Tasks'].cumsum()
                fig2 = px.area(
                    completion_by_day,
                    x='Day',
                    y='Cumulative',
                    title="Cumulative Tasks Completed",
                    height=400
                )
                fig2.update_traces(fill='tozeroy', line=dict(color='#667eea'))
                st.plotly_chart(fig2, use_container_width=True)
        
        elif report_type == "💾 Export Data":
            st.subheader("Export Project Data")
            
            export_type = st.radio("Select data to export", ["All Universities Summary", "Single University Detailed"])
            
            if export_type == "Single University Detailed":
                universities_data = db.get_all_universities_progress()
                uni_name = st.selectbox("Select University", list(universities_data.keys()))
                
                if st.button("📥 Export to CSV", use_container_width=True):
                    uni_data = db.get_university_progress(universities_data[uni_name]['code'])
                    csv = uni_data.to_csv(index=False)
                    st.download_button(
                        label="💾 Download CSV",
                        data=csv,
                        file_name=f"{uni_name.replace(' ', '_')}_progress.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
            else:
                if st.button("📥 Export Summary to CSV", use_container_width=True):
                    summary = db.get_summary_stats()
                    csv = summary.to_csv(index=False)
                    st.download_button(
                        label="💾 Download CSV",
                        data=csv,
                        file_name="mahastride_summary.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
    except Exception as e:
        st.error(f"Error generating reports: {e}")

elif page == "ℹ️ About":
    st.title("ℹ️ About mahaSTRIDE Tracker")
    st.markdown("---")
    
    st.markdown("""
    <div class="main-header">
        <h2>🎯 Project Overview</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📋 Project Details
        
        **Project Name:** mahaSTRIDE  
        **Duration:** 10 Weeks (50 Days)  
        **Universities:** 7 Participating Universities  
        **Frameworks:** 4 Major Frameworks
        
        #### 🎓 Participating Universities
        1. **Mumbai University** - Ms Sneha, Shubham
        2. **SSPU Pune** - Mr Jagan
        3. **COEP Tech University** - Mr Vaibhav
        4. **Amravati University** - Mr Pratham
        5. **Nagpur University** - Ms Anjali
        6. **KBCNMU Jalgaon University** - Mr Nitish
        7. **BAMU University Aurangabad** - Mr Atharv
        """)
    
    with col2:
        st.markdown("""
        ### 📚 Frameworks Timeline
        
        #### SAMARTH Framework (Days 1-25)
        - Faculty Roster, Students, Financial
        - IPR/Patents, Publications
        - PhD Faculties, SAM TLR, SAM RP
        - SAM-GO, SAM-OI, SAM PR
        
        #### NEP Framework (Days 26-35)
        - NEP CUR, NEP-TCH, NEP RES
        - NEP GOV, NEP INC, NEP OUT
        - NEP-DIG, NEP SUS
        
        #### AEGIS Framework (Days 36-42)
        - AEG-BI, AEG-EDU, AEG-GRD
        - AEG-INC, AEG-SAF
        
        #### IKS Framework (Days 43-50)
        - IKS-CUR, IKS-TCH, IKS-RES
        - IKS-GOV, IKS-OUT, IKS-DIG
        """)
    
    st.markdown("---")
    
    st.markdown("""
    <div class="success-card">
        <h3>🚀 Features</h3>
        <ul>
            <li>Real-time progress tracking across 7 universities</li>
            <li>Interactive dashboards with visual analytics</li>
            <li>Framework-wise performance analysis</li>
            <li>Automated report generation</li>
            <li>Data export capabilities</li>
            <li>Mobile-responsive design</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-card">
        <h3>👨‍💻 Developer</h3>
        <p><strong>Developed for:</strong> Dr. Harshal</p>
        <p><strong>Purpose:</strong> Project Management and Progress Tracking</p>
        <p><strong>Version:</strong> 1.0.0</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray; padding: 1rem;'>© 2024 mahaSTRIDE Project Tracker | Developed for Dr. Harshal</div>",
    unsafe_allow_html=True
)
