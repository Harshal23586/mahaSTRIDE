import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import calendar

# Page configuration
st.set_page_config(
    page_title="MahaSTRIDE - Project Plan of Action Dashboard",
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
    .phase-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        transition: transform 0.3s;
    }
    .phase-card:hover {
        transform: translateY(-5px);
    }
    .milestone-card {
        background: white;
        border-left: 4px solid #28a745;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .deliverable-card {
        background: white;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .university-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #2a5298;
    }
    .stat-card {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
    .timeline-node {
        position: relative;
        padding: 0.5rem 0;
        padding-left: 1.5rem;
        border-left: 2px solid #2a5298;
        margin-left: 1rem;
    }
    .timeline-node::before {
        content: "●";
        position: absolute;
        left: -0.6rem;
        color: #2a5298;
        font-size: 1.2rem;
    }
    .war-room-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# PROJECT DATA
# ============================================================

PROJECT_NAME = "MahaSTRIDE - Maharashtra Strengthening Institutional Capabilities in Districts for Enabling Growth"
CONTRACT_VALUE = "₹4,44,41,888"
START_DATE = datetime(2026, 5, 5)
END_DATE = datetime(2028, 5, 6)
DURATION_MONTHS = 24

# Universities Data
UNIVERSITIES = {
    "MU": {
        "name": "Mumbai University",
        "location": "Mumbai",
        "vice_chancellor": "Dr. Ravindra Kulkarni",
        "nodal_officer": "Dr. Varsha Kelkar Mane",
        "contact": "+91-22-26543000",
        "email": "vc@mu.ac.in",
        "coordinators": ["Sneha Kashitkar", "Sagar Teli"],
        "established": "1857",
        "students": "7,50,000+",
        "rank": "NIRF 2025: 65"
    },
    "SSPU": {
        "name": "Savitribai Phule Pune University",
        "location": "Pune",
        "vice_chancellor": "Dr. Suresh Gosavi",
        "nodal_officer": "Prof. Vinayak Joshi",
        "contact": "+91-20-25696061",
        "email": "vc@unipune.ac.in",
        "coordinators": ["Jagan Sridhar"],
        "established": "1949",
        "students": "6,00,000+",
        "rank": "NIRF 2025: 12"
    },
    "COEP": {
        "name": "COEP Technological University",
        "location": "Pune",
        "vice_chancellor": "Dr. B. K. Mishra",
        "nodal_officer": "Dr. Uttam Chaskar",
        "contact": "+91-20-25507000",
        "email": "director@coep.ac.in",
        "coordinators": ["Vaibhav Ambekar"],
        "established": "1854",
        "students": "5,000+",
        "rank": "NIRF Engineering: 45"
    },
    "KBCNMU": {
        "name": "Kavayitri Bahinabai Chaudhari North Maharashtra University",
        "location": "Jalgaon",
        "vice_chancellor": "Dr. R. P. Swami",
        "nodal_officer": "Prof. Sameer Narkhede",
        "contact": "+91-257-2257457",
        "email": "vc@nmu.ac.in",
        "coordinators": ["Nitish Kumbhar"],
        "established": "1990",
        "students": "2,00,000+",
        "rank": "NIRF 2025: 101-150"
    },
    "BAMU": {
        "name": "Dr. Babasaheb Ambedkar Marathwada University",
        "location": "Chhatrapati Sambhajinagar",
        "vice_chancellor": "Dr. Pramod Yeole",
        "nodal_officer": "Prof. G. D. Khedkar",
        "contact": "+91-240-2403111",
        "email": "vc@bamu.ac.in",
        "coordinators": ["Atharav Paturkar"],
        "established": "1958",
        "students": "3,00,000+",
        "rank": "NIRF 2025: 101-150"
    },
    "NU": {
        "name": "Rashtrasant Tukadoji Maharaj Nagpur University",
        "location": "Nagpur",
        "vice_chancellor": "Dr. Subhash Chaudhari",
        "nodal_officer": "Prof. Nandkishor Karade",
        "contact": "+91-712-2500511",
        "email": "vc@nagpuruniversity.ac.in",
        "coordinators": ["Anjali Singh"],
        "established": "1923",
        "students": "4,00,000+",
        "rank": "NIRF 2025: 81"
    },
    "AU": {
        "name": "Sant Gadge Baba Amravati University",
        "location": "Amravati",
        "vice_chancellor": "Dr. Milind Baride",
        "nodal_officer": "Dr. A. B. Naik",
        "contact": "+91-721-2662379",
        "email": "vc@sgbau.ac.in",
        "coordinators": ["Prathamesh Babhulkar"],
        "established": "1983",
        "students": "2,50,000+",
        "rank": "NIRF 2025: 101-150"
    },
    "MITRA": {
        "name": "MITRA - State Data Authority",
        "location": "Mumbai",
        "ceo": "Shri. Aman Mittal",
        "nodal_officer": "Dr. Harshal Kotwal",
        "contact": "+91-22-69979440",
        "email": "pmu.mahastride@mahamitra.org",
        "coordinators": ["Shubham Singh"],
        "established": "2024",
        "students": "N/A",
        "rank": "N/A"
    }
}

# Project Phases
PHASES = {
    "Phase 1: Foundation (Months 1-3)": {
        "months": "May 2026 - July 2026",
        "color": "#1e3c72",
        "key_activities": [
            "Project Kick-off and Team Mobilization",
            "SANGAM Orientation & Training (May 4-6)",
            "University Onboarding & Data Source Mapping",
            "NIRF Data Collection across all 7 universities",
            "Stakeholder Consultation & Review Meetings",
            "Inception Report & GRDAU Framework Development",
            "Diagnostic Assessments completion",
            "GRDAU Establishment in all universities"
        ],
        "deliverables": [
            "Inception Report and Deployment Plan",
            "Diagnostic Assessment Reports (7 universities)",
            "GRDAUs Established and Operationalized",
            "SWOT Analysis Reports"
        ]
    },
    "Phase 2: Planning (Months 4-6)": {
        "months": "August 2026 - October 2026",
        "color": "#2a5298",
        "key_activities": [
            "Institutional Development Plans (IDPs) development",
            "Stakeholder review and feedback incorporation",
            "Data portal architecture design",
            "Dashboard requirements gathering",
            "Dashboard prototype development",
            "Milestone 1: Sustainable Data Systems establishment"
        ],
        "deliverables": [
            "Institutional Development Plans (IDPs) - 7",
            "Portal Design Document",
            "Dashboard Mockups",
            "Milestone 1 Report"
        ]
    },
    "Phase 3: Implementation (Months 7-12)": {
        "months": "November 2026 - April 2027",
        "color": "#28a745",
        "key_activities": [
            "Data Portal MVP Deployment",
            "Training Needs Assessment",
            "Capacity Building Programs (First round)",
            "Performance Dashboards Launch",
            "Data Validation and Quality Improvement",
            "Research Output Enhancement Initiatives",
            "Milestone 2: IDP Execution Monitoring"
        ],
        "deliverables": [
            "Data Portal Live",
            "Training Completion Report",
            "Dashboard Deployment Report",
            "Research Enhancement Plan"
        ]
    },
    "Phase 4: Enhancement (Months 13-18)": {
        "months": "May 2027 - October 2027",
        "color": "#17a2b8",
        "key_activities": [
            "Advanced Training Programs",
            "International Collaboration Development",
            "Global Ranking Submissions (QS, THE, US News)",
            "Employer Perception Enhancement",
            "Academic Reputation Building",
            "Milestone 3: Capacity Building Participation"
        ],
        "deliverables": [
            "Advanced Training Report",
            "Ranking Submission Packages",
            "Industry Connect Report",
            "Milestone 3 Report"
        ]
    },
    "Phase 5: Finalization (Months 19-24)": {
        "months": "November 2027 - April 2028",
        "color": "#fd7e14",
        "key_activities": [
            "Final Global Ranking Submissions",
            "Sustainability Planning",
            "Knowledge Transfer and Handover",
            "Final Evaluation",
            "Project Closure Activities"
        ],
        "deliverables": [
            "Final Closure Report",
            "Sustainability Plan",
            "Knowledge Transfer Report",
            "Milestone 6 & 7 Reports"
        ]
    }
}

# Milestones (Performance-Linked)
MILESTONES = [
    {"id": 1, "name": "Establishment of Sustainable Data & Quality Systems", "weight": "10%", "target": "Sep 30, 2026", "status": "upcoming"},
    {"id": 2, "name": "Institutional Development Plans and Execution Monitoring", "weight": "10%", "target": "Oct 31, 2026", "status": "upcoming"},
    {"id": 3, "name": "Capacity Building Participation (60% of IQAC faculty)", "weight": "10%", "target": "Dec 31, 2026", "status": "upcoming"},
    {"id": 4, "name": "Minimum 10% Improvement in Performance Indicators", "weight": "15%", "target": "Jun 30, 2027", "status": "upcoming"},
    {"id": 5, "name": "Minimum 20% Improvement in Performance Indicators", "weight": "25%", "target": "Dec 31, 2027", "status": "upcoming"},
    {"id": 6, "name": "Enhanced Global Rankings Participation (10 colleges)", "weight": "20%", "target": "Feb 29, 2028", "status": "upcoming"},
    {"id": 7, "name": "Final Evaluation and Reporting", "weight": "10%", "target": "Apr 30, 2028", "status": "upcoming"}
]

# Contract Deliverables
CONTRACT_DELIVERABLES = [
    {"deliverable": "Inception Report and Deployment Plan", "due_days": 30, "due_date": "Jun 5, 2026", "status": "completed", "actual_date": "May 26, 2026"},
    {"deliverable": "Diagnostic Assessment Reports (Institution-wise)", "due_days": 60, "due_date": "Jul 5, 2026", "status": "in_progress", "actual_date": None},
    {"deliverable": "Institutional Development Plans (IDPs)", "due_days": 100, "due_date": "Aug 14, 2026", "status": "pending", "actual_date": None},
    {"deliverable": "GRDAUs Established and Operationalized", "due_days": 60, "due_date": "Jul 5, 2026", "status": "in_progress", "actual_date": None},
    {"deliverable": "Mid-term Progress Report", "due_days": 180, "due_date": "Nov 2, 2026", "status": "pending", "actual_date": None},
    {"deliverable": "Dashboard Reports and Analytics", "due_days": "Monthly", "due_date": "Monthly from day 60", "status": "pending", "actual_date": None},
    {"deliverable": "Final Closure Report and Recommendations", "due_days": "End of 24 months", "due_date": "May 6, 2028", "status": "pending", "actual_date": None}
]

# Working Days Calculation
def get_working_days_count(start, end):
    count = 0
    current = start
    while current <= end:
        if current.weekday() < 5:
            count += 1
        current += timedelta(days=1)
    return count

total_working_days = get_working_days_count(START_DATE, END_DATE)
completed_working_days = get_working_days_count(START_DATE, datetime(2026, 5, 31))

# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

with st.sidebar:
    st.markdown("## 🎯 MahaSTRIDE")
    st.markdown("---")
    
    nav_options = {
        "🏠 Project Overview": "overview",
        "📊 Dashboard": "dashboard",
        "📅 24-Month Plan": "plan",
        "🏫 Universities & Team": "universities",
        "🎯 Milestones": "milestones",
        "📋 Deliverables": "deliverables",
        "🏛️ War Room & GRDAU": "warroom",
        "📈 KPIs & Outcomes": "kpis",
        "📁 Documents": "documents"
    }
    
    selected_nav = st.radio("Navigation", list(nav_options.keys()), label_visibility="collapsed")
    selected_key = nav_options[selected_nav]
    
    st.markdown("---")
    st.markdown("### ℹ️ Project Info")
    st.markdown(f"**Start Date:** {START_DATE.strftime('%d %b %Y')}")
    st.markdown(f"**End Date:** {END_DATE.strftime('%d %b %Y')}")
    st.markdown(f"**Duration:** 24 months")
    st.markdown(f"**Working Days:** {total_working_days}")
    st.markdown(f"**Universities:** 7")
    st.markdown(f"**Data Analysts:** 10")
    
    st.markdown("---")
    st.markdown("### ✅ May 2026 Status")
    st.markdown("- SANGAM Training: ✅ Completed")
    st.markdown("- University Onboarding: ✅ Completed")
    st.markdown("- NIRF Data Collection: ✅ Completed")
    st.markdown("- Inception Report: ✅ Submitted")
    st.markdown("- May MPR: ✅ Submitted")
    
    st.markdown("---")
    st.markdown("### 📞 Contact")
    st.markdown("**PMU MahaSTRIDE**")
    st.markdown("📧 pmu.mahastride@mahamitra.org")
    st.markdown("📞 022-69979440")
    st.markdown("📍 5th Floor, Nirmal Building, Nariman Point, Mumbai-400021")

# ============================================================
# MAIN CONTENT
# ============================================================

st.markdown(f"""
<div class="main-header">
    <h1>🎯 {PROJECT_NAME}</h1>
    <p>World Bank Loan No: IBRD 9737-IN | RFP Ref: IN-MITRA(PMU)-PforR-Edu-QCBS</p>
    <p>Consultant: Indian Centre for Academic Rankings & Excellence - ICARE Pvt. Ltd.</p>
    <p>Client: Maharashtra Institution for Transformation (MITRA) - State Data Authority</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# 1. PROJECT OVERVIEW
# ============================================================
if selected_key == "overview":
    st.header("📋 Project Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <h2>24</h2>
            <p>Months Duration</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <h2>7</h2>
            <p>Universities</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <h2>{total_working_days}</h2>
            <p>Working Days</p>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <h2>10</h2>
            <p>Data Analysts</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.subheader("🎯 Project Objective")
    st.markdown("""
    The MahaSTRIDE project aims to establish a structured and sustainable system for systematic data collation, 
    advanced analytics, and performance monitoring across selected State Universities in Maharashtra. The initiative 
    seeks to:
    
    - **Retain top student talent and financial resources** within Maharashtra
    - **Enhance institutional visibility** in global rankings (QS, THE, US News)
    - **Support the State's contribution to Viksit Bharat** by leveraging its demographic advantage
    - **Address the fundamental need for a rigorous, metrics‑based approach** - collecting and analysing performance 
      data to identify gaps, devise targeted interventions, and elevate Maharashtra's public universities to meet 
      and exceed national and global benchmarks
    """)
    
    st.markdown("---")
    
    st.subheader("🏗️ Key Components")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### 1. Data Framework Development
        - Comprehensive data framework aligned with global ranking parameters
        - Integration with NIRF, NAAC, QS, THE, US News metrics
        
        ### 2. Digital Infrastructure
        - Data portal for upload and submission
        - Customized analytical tools and dashboards
        - Integration with international ranking portals
        
        ### 3. GRDAU Establishment
        - Dedicated Global Ranking Data Analytics Units in each university
        - Trained personnel for data governance
        """)
    
    with col2:
        st.markdown("""
        ### 4. Capacity Building
        - Structured training programmes for faculty and staff
        - Focus on research quality, international collaboration, OBE
        
        ### 5. Performance Monitoring
        - Real-time tracking dashboards
        - Quality enhancement initiatives
        - Progress toward ranking goals
        
        ### 6. Sustainability
        - Transparent data repositories on university websites
        - Institutionalized quality improvement culture
        """)
    
    st.markdown("---")
    
    st.subheader("📊 Key Metrics to Track")
    
    metrics_data = {
        "Metric": [
            "Teaching, Learning & Resources (TLR)",
            "Research and Professional Practice (RP)",
            "Graduation Outcomes (GO)",
            "Outreach and Inclusivity (OI)",
            "Academic Reputation",
            "Employer Perception",
            "Citations per Faculty"
        ],
        "Weightage": [
            "NIRF Parameter",
            "NIRF Parameter",
            "NIRF Parameter",
            "NIRF Parameter",
            "30% (QS)",
            "15% (QS)",
            "20% (QS)"
        ],
        "Target": [
            "Improve by 20%",
            "Increase publications & citations",
            "Enhance placement rate",
            "Increase diversity metrics",
            "Top 500 globally",
            "Improve by 30%",
            "Increase by 25%"
        ]
    }
    
    st.dataframe(pd.DataFrame(metrics_data), use_container_width=True, hide_index=True)

# ============================================================
# 2. DASHBOARD
# ============================================================
elif selected_key == "dashboard":
    st.header("📊 Project Dashboard")
    
    # Overall Progress
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        progress_pct = (completed_working_days / total_working_days * 100)
        st.markdown(f"""
        <div class="stat-card">
            <h2>{progress_pct:.1f}%</h2>
            <p>Overall Progress</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        completed_deliverables = sum(1 for d in CONTRACT_DELIVERABLES if d["status"] == "completed")
        st.markdown(f"""
        <div class="stat-card">
            <h2>{completed_deliverables}/{len(CONTRACT_DELIVERABLES)}</h2>
            <p>Deliverables Completed</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        completed_milestones = sum(1 for m in MILESTONES if m["status"] == "completed")
        st.markdown(f"""
        <div class="stat-card">
            <h2>{completed_milestones}/{len(MILESTONES)}</h2>
            <p>Milestones Achieved</p>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <h2>{completed_working_days}</h2>
            <p>Working Days Completed</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Phase-wise Progress
    st.subheader("📈 Phase-wise Progress")
    
    phase_data = []
    for phase_name, phase_info in PHASES.items():
        phase_data.append({
            "Phase": phase_name,
            "Duration": phase_info["months"],
            "Color": phase_info["color"]
        })
    
    fig = go.Figure()
    for i, phase in enumerate(phase_data):
        fig.add_trace(go.Bar(
            x=[phase["Phase"]],
            y=[1],
            name=phase["Phase"],
            marker_color=phase["Color"],
            text=phase["Duration"],
            textposition="inside",
            orientation='v'
        ))
    
    fig.update_layout(
        title="Project Phases Timeline",
        showlegend=False,
        height=400,
        yaxis=dict(showticklabels=False, title=""),
        xaxis=dict(title="")
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Current Status
    st.subheader("✅ Current Status (May 2026 - Completed)")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### Completed Activities
        - ✅ SANGAM Orientation & Training (May 4-6 at Trident Board Room)
        - ✅ University Onboarding & Data Source Mapping
        - ✅ NIRF Data Collection (Student, Faculty, Research, Placement, Finance)
        - ✅ Stakeholder Consultation & Review Meetings
        - ✅ Inception Report & GRDAU Framework Development
        - ✅ May MPR Preparation & Finalization
        """)
    
    with col2:
        st.markdown("""
        ### Next Milestones
        - 📍 Diagnostic Assessment Reports (Due: July 5, 2026)
        - 📍 GRDAUs Establishment (Due: July 5, 2026)
        - 📍 Institutional Development Plans (Due: August 14, 2026)
        - 📍 Milestone 1: Sustainable Data Systems (Due: Sep 30, 2026)
        """)
    
    st.markdown("---")
    
    # Team Attendance Summary (May 2026)
    st.subheader("👥 Team Attendance - May 2026")
    
    attendance_data = {
        "Name": ["Dr. Harshal Kotwal", "Shubham Singh", "Sneha Kashitkar", "Sagar Teli", "Jagan Sridhar", 
                "Vaibhav Ambekar", "Prathamesh Babhulkar", "Anjali Singh", "Nitish Kumbhar", "Atharav Paturkar"],
        "Role": ["Project Lead", "Data Analytics Specialist", "Institutional Coordinator", "Institutional Coordinator",
                "Institutional Coordinator", "Institutional Coordinator", "Institutional Coordinator", 
                "Institutional Coordinator", "Institutional Coordinator", "Institutional Coordinator"],
        "University": ["ICARE", "MITRA", "Mumbai University", "Mumbai University", "SPPU Pune", 
                      "COEP Pune", "Amravati University", "Nagpur University", "KBCNMU Jalgaon", "BAMU Aurangabad"],
        "Present Days": [19, 19, 19, 19, 19, 19, 19, 19, 19, 19],
        "Absent": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "Holidays": [12, 12, 12, 12, 12, 12, 12, 12, 12, 12]
    }
    
    df_attendance = pd.DataFrame(attendance_data)
    st.dataframe(df_attendance, use_container_width=True, hide_index=True)

# ============================================================
# 3. 24-MONTH PLAN
# ============================================================
elif selected_key == "plan":
    st.header("📅 24-Month Project Plan")
    st.markdown("May 2026 - April 2028 | Monday to Friday | 10:00 AM - 6:00 PM")
    st.markdown("---")
    
    # Phase selector
    phase_tabs = st.tabs(list(PHASES.keys()))
    
    for tab, (phase_name, phase_info) in zip(phase_tabs, PHASES.items()):
        with tab:
            st.markdown(f"""
            <div class="phase-card" style="background: linear-gradient(135deg, {phase_info['color']} 0%, {phase_info['color']}cc 100%);">
                <h2>{phase_name}</h2>
                <p><strong>Duration:</strong> {phase_info['months']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 🎯 Key Activities")
                for activity in phase_info["key_activities"]:
                    st.markdown(f"- {activity}")
            
            with col2:
                st.markdown("### 📦 Deliverables")
                for deliverable in phase_info["deliverables"]:
                    st.markdown(f"- {deliverable}")
            
            st.markdown("---")
    
    # Detailed Month-wise Plan
    st.subheader("📆 Month-wise Detailed Plan")
    
    month_plan = [
        ("May 2026", "✅ COMPLETED", "SANGAM Training, University Onboarding, NIRF Data Collection, Inception Report"),
        ("June 2026", "🔄 In Progress", "Diagnostic Assessments, GRDAU Training, Data Validation"),
        ("July 2026", "⏳ Upcoming", "Gap Analysis, SWOT Reports, GRDAU Establishment, Phase 1 Completion"),
        ("August 2026", "⏳ Upcoming", "IDP Development, Strategic Plan Collection, Portal Design"),
        ("September 2026", "⏳ Upcoming", "Dashboard Development, Milestone 1, User Testing"),
        ("October 2026", "⏳ Upcoming", "Milestone 2, Mid-Term Review, Portal Deployment"),
        ("November 2026", "⏳ Upcoming", "Portal MVP, Training Needs Assessment"),
        ("December 2026", "⏳ Upcoming", "Milestone 3, Training Programs, Year-End Review"),
        ("January 2027", "⏳ Upcoming", "Data Quality, Research Enhancement"),
        ("February 2027", "⏳ Upcoming", "International Collaboration, OBE Implementation"),
        ("March 2027", "⏳ Upcoming", "Accreditation, Quality Assurance"),
        ("April 2027", "⏳ Upcoming", "Milestone 4 (10% Improvement), Year 1 Report"),
        ("May 2027", "⏳ Upcoming", "Year 2 Kickoff, Advanced Analytics"),
        ("June 2027", "⏳ Upcoming", "Global Ranking Preparation (QS, THE, US News)"),
        ("July 2027", "⏳ Upcoming", "Advanced Training, Research Support"),
        ("August 2027", "⏳ Upcoming", "Employer Perception, Industry Connect"),
        ("September 2027", "⏳ Upcoming", "Milestone 5 (20% Improvement)"),
        ("October 2027", "⏳ Upcoming", "Academic Reputation Building"),
        ("November 2027", "⏳ Upcoming", "Final Ranking Submissions, Milestone 6"),
        ("December 2027", "⏳ Upcoming", "Sustainability Planning"),
        ("January 2028", "⏳ Upcoming", "Final Evaluation Preparation"),
        ("February 2028", "⏳ Upcoming", "Final Client Presentation, Milestone 7"),
        ("March 2028", "⏳ Upcoming", "Project Closure, Knowledge Transfer"),
        ("April 2028", "⏳ Upcoming", "Contract Completion, Final Submission")
    ]
    
    for month, status, activities in month_plan:
        if "COMPLETED" in status:
            st.markdown(f"### ✅ {month} - {status}")
        elif "In Progress" in status:
            st.markdown(f"### 🔄 {month} - {status}")
        else:
            st.markdown(f"### ⏳ {month} - {status}")
        st.markdown(f"*Activities:* {activities}")
        st.markdown("---")

# ============================================================
# 4. UNIVERSITIES & TEAM
# ============================================================
elif selected_key == "universities":
    st.header("🏫 Universities & Team Structure")
    
    st.subheader("📋 Participating Universities")
    
    for code, uni in UNIVERSITIES.items():
        with st.expander(f"🏛️ {uni['name']} ({code})"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                **📍 Location:** {uni['location']}<br>
                **👨‍🎓 Vice Chancellor:** {uni.get('vice_chancellor', 'N/A')}<br>
                **👤 Nodal Officer:** {uni.get('nodal_officer', 'N/A')}<br>
                **📞 Contact:** {uni.get('contact', 'N/A')}<br>
                **📧 Email:** {uni.get('email', 'N/A')}
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                **📅 Established:** {uni.get('established', 'N/A')}<br>
                **👥 Students:** {uni.get('students', 'N/A')}<br>
                **📊 NIRF Rank:** {uni.get('rank', 'N/A')}<br>
                **👥 Coordinators:** {', '.join(uni.get('coordinators', []))}
                """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.subheader("👥 Project Team Structure")
    
    team_data = {
        "Role": ["Project Director", "Project Lead", "Data Analytics Specialist", "Statistician & Program Designer",
                "Institutional Coordinator (MU)", "Institutional Coordinator (MU)", "Institutional Coordinator (SSPU)",
                "Institutional Coordinator (COEP)", "Institutional Coordinator (AU)", "Institutional Coordinator (NU)",
                "Institutional Coordinator (KBCNMU)", "Institutional Coordinator (BAMU)"],
        "Name": ["Shri. Aman Mittal", "Dr. Harshal Kotwal", "Shubham Singh", "Sagar Teli",
                "Sneha Kashitkar", "Sagar Teli", "Jagan Sridhar", "Vaibhav Ambekar", "Prathamesh Babhulkar",
                "Anjali Singh", "Nitish Kumbhar", "Atharav Paturkar"],
        "Organization": ["MITRA", "ICARE", "MITRA", "Mumbai University", "Mumbai University", "Mumbai University",
                        "SPPU Pune", "COEP Pune", "Amravati University", "Nagpur University", "KBCNMU Jalgaon", "BAMU Aurangabad"],
        "Contact": ["pmu.mahastride@mahamitra.org", "projectlead@mahastride.com", "shubham@mitra.gov.in", 
                   "sagar@mu.edu", "sneha@mu.edu", "sagar@mu.edu", "jagan@sspu.edu", "vaibhav@coep.edu",
                   "pratham@au.edu", "anjali@nu.edu", "nitish@kbcnmu.edu", "atharv@bamu.edu"]
    }
    
    df_team = pd.DataFrame(team_data)
    st.dataframe(df_team, use_container_width=True, hide_index=True)

# ============================================================
# 5. MILESTONES
# ============================================================
elif selected_key == "milestones":
    st.header("🎯 Performance-Linked Milestones")
    st.markdown("30% of contract value is linked to milestone achievement")
    
    st.markdown("---")
    
    # Milestone progress visualization
    fig = go.Figure(data=[go.Pie(
        labels=[m["name"] for m in MILESTONES],
        values=[int(m["weight"].replace("%", "")) for m in MILESTONES],
        hole=0.4,
        marker_colors=['#1e3c72', '#2a5298', '#28a745', '#ffc107', '#fd7e14', '#dc3545', '#17a2b8']
    )])
    fig.update_layout(title="Milestone Weightage Distribution", height=450)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    for milestone in MILESTONES:
        if milestone["status"] == "completed":
            icon = "✅"
            color = "#d4edda"
        elif milestone["status"] == "in_progress":
            icon = "🔄"
            color = "#fff3cd"
        else:
            icon = "⏳"
            color = "#f8f9fa"
        
        st.markdown(f"""
        <div style="background-color:{color}; padding:1rem; margin:0.5rem 0; border-radius:8px;">
            <strong>{icon} Milestone {milestone['id']}: {milestone['name']}</strong><br>
            📅 Target Date: {milestone['target']} | 📊 Weight: {milestone['weight']}
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.subheader("📊 Expected Outcomes")
    
    outcomes = {
        "Enhanced Global Rankings Participation": "Successful participation of institutions on minimum two global ranking platforms",
        "Minimum 20% Improvement": "Validation of comparative data between baseline and endline diagnostics",
        "Establishment of Sustainable Data & Quality Systems": "Certification of GRDAU readiness and dashboard deployment",
        "Institutional Development Plans": "Finalization and institutional sign-off of all IDPs",
        "Capacity Building Participation": "Minimum 60% participation of IQAC faculty and staff",
        "Final Evaluation": "Approval of final report and satisfactory project closure"
    }
    
    for outcome, metric in outcomes.items():
        st.markdown(f"**🏆 {outcome}**")
        st.markdown(f"📊 {metric}")
        st.markdown("---")

# ============================================================
# 6. DELIVERABLES
# ============================================================
elif selected_key == "deliverables":
    st.header("📋 Contract Deliverables Tracker")
    
    completed = sum(1 for d in CONTRACT_DELIVERABLES if d["status"] == "completed")
    in_progress = sum(1 for d in CONTRACT_DELIVERABLES if d["status"] == "in_progress")
    pending = sum(1 for d in CONTRACT_DELIVERABLES if d["status"] == "pending")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("✅ Completed", completed)
    with col2:
        st.metric("🔄 In Progress", in_progress)
    with col3:
        st.metric("⏳ Pending", pending)
    
    st.markdown("---")
    
    for deliverable in CONTRACT_DELIVERABLES:
        if deliverable["status"] == "completed":
            icon = "✅"
            color = "#d4edda"
        elif deliverable["status"] == "in_progress":
            icon = "🔄"
            color = "#fff3cd"
        else:
            icon = "⏳"
            color = "#f8f9fa"
        
        actual_text = f"<br>✅ Actual Submission: {deliverable['actual_date']}" if deliverable.get('actual_date') else ""
        
        st.markdown(f"""
        <div style="background-color:{color}; padding:1rem; margin:0.5rem 0; border-radius:8px;">
            <strong>{icon} {deliverable['deliverable']}</strong><br>
            📅 Due: {deliverable['due_date']}<br>
            📊 Status: {deliverable['status'].upper()}
            {actual_text}
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# 7. WAR ROOM & GRDAU
# ============================================================
elif selected_key == "warroom":
    st.header("🏛️ War Room & GRDAU Setup")
    
    st.markdown("""
    <div class="war-room-card">
        <h2>🎯 Project War Room - MITRA, Mumbai</h2>
        <p><strong>Location:</strong> 5th Floor, Nirmal Building, Nariman Point, Mumbai-400021</p>
        <p><strong>Purpose:</strong> Central command center for project monitoring, coordination, and decision-making</p>
        <p><strong>Facilities:</strong> Real-time dashboards, video conferencing, data visualization tools</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.subheader("🏫 Global Ranking Data Analytics Units (GRDAUs)")
    
    st.markdown("""
    Each participating university will establish a dedicated GRDAU with the following:
    
    - **Staffing:** Multidisciplinary personnel including data analysts, statisticians, and research coordinators
    - **Responsibilities:**
        - Implementing Institutional Development Plans (IDPs)
        - Monitoring institutional performance
        - Coordinating training and capacity building
        - Acting as nodal points for engagement with global and national ranking agencies
    - **Infrastructure:** Computers, software for data analysis, dashboard access
    """)
    
    st.markdown("---")
    
    st.subheader("📍 GRDAU Locations")
    
    grdau_data = []
    for code, uni in UNIVERSITIES.items():
        if code != "MITRA":
            grdau_data.append({
                "University": uni["name"],
                "Location": uni["location"],
                "Coordinator": ", ".join(uni["coordinators"]),
                "Status": "Setup in Progress"
            })
    
    st.dataframe(pd.DataFrame(grdau_data), use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    st.subheader("📋 GRDAU Operational Framework")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### Key Responsibilities
        - **Data Collection:** Systematic collection of NIRF/ranking parameters
        - **Data Validation:** Quality checks and verification
        - **Reporting:** Monthly Progress Reports
        - **Analysis:** Performance gap analysis
        - **Training:** Capacity building for faculty
        """)
    
    with col2:
        st.markdown("""
        ### KPIs for GRDAU
        - Data completeness rate: >95%
        - On-time MPR submission: 100%
        - Training participation: >60%
        - Dashboard usage: Monthly active users
        - Ranking improvement: Year-on-year
        """)

# ============================================================
# 8. KPIs & OUTCOMES
# ============================================================
elif selected_key == "kpis":
    st.header("📈 KPIs & Expected Outcomes")
    
    st.subheader("🎯 Key Performance Indicators")
    
    kpi_data = {
        "KPI": [
            "NIRF Score Improvement",
            "Research Publication Growth",
            "Citation Impact Increase",
            "Placement Rate Improvement",
            "Faculty-Student Ratio",
            "International Collaboration",
            "Global Ranking Participation",
            "GRDAU Operational Status"
        ],
        "Baseline (2025)": [
            "Current NIRF scores",
            "Current publication count",
            "Current citation count",
            "Current placement %",
            "Current ratio",
            "Current MoUs",
            "0 universities",
            "Not established"
        ],
        "Target (2028)": [
            "20% improvement",
            "50% increase",
            "25% increase",
            "30% improvement",
            "1:15 target",
            "10+ new MoUs",
            "10+ colleges",
            "Fully operational"
        ],
        "Responsible": [
            "GRDAU + IQAC",
            "Research Cell",
            "Research Cell",
            "Placement Cell",
            "Administration",
            "International Office",
            "GRDAU",
            "GRDAU"
        ]
    }
    
    df_kpi = pd.DataFrame(kpi_data)
    st.dataframe(df_kpi, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    st.subheader("🏆 Expected Outcomes (Performance-Linked)")
    
    outcomes_data = {
        "Outcome": [
            "Enhanced Global Rankings Participation",
            "Minimum 20% Improvement in Performance Indicators",
            "Establishment of Sustainable Data & Quality Systems",
            "Institutional Development Plans and Execution",
            "Capacity Building Participation",
            "Final Evaluation and Reporting"
        ],
        "Success Criteria": [
            "Participation in 2+ global ranking platforms",
            "Validation of comparative baseline-endline data",
            "GRDAU readiness + dashboard deployment",
            "Institutional sign-off of all IDPs",
            "60% IQAC faculty participation",
            "Approval of final report"
        ]
    }
    
    df_outcomes = pd.DataFrame(outcomes_data)
    st.dataframe(df_outcomes, use_container_width=True, hide_index=True)

# ============================================================
# 9. DOCUMENTS
# ============================================================
elif selected_key == "documents":
    st.header("📁 Reference Documents")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📄 Contract Documents
        - Draft Contract with ICARE
        - Terms & Conditions of Contract
        - Terms of Reference (ToR)
        - Consultant's Technical Proposal
        
        ### 📋 SOP Documents
        - SOP for Payment Processing
        - Attendance Tracking Guidelines
        - MPR Submission Guidelines
        """)
    
    with col2:
        st.markdown("""
        ### 📊 Reports
        - Consolidated MPR - May 2026
        - Work Order (ICARE)
        - RFP Reference Documents
        
        ### 🏛️ Government Orders
        - Planning Department GRs
        - State Steering Committee Minutes
        - Administrative Approvals
        """)
    
    st.markdown("---")
    
    st.subheader("📎 Key Document Links")
    
    st.markdown("""
    | Document | Description | Status |
    |----------|-------------|--------|
    | Contract Agreement | Signed contract between MITRA and ICARE | ✅ Executed |
    | Work Order | Issued to ICARE Pvt. Ltd. | ✅ Issued |
    | Performance Bank Guarantee | 5% of contract value | ⏳ Pending Submission |
    | Inception Report | Submitted on May 26, 2026 | ✅ Submitted |
    | May MPR | Submitted on May 29, 2026 | ✅ Submitted |
    | Diagnostic Reports | Due July 5, 2026 | 🔄 In Progress |
    """)

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #666; font-size: 0.8rem;">
    <p>© 2026-2028 Maharashtra Institution for Transformation (MITRA) | MahaSTRIDE Project | World Bank Loan No: IBRD 9737-IN</p>
    <p>Consultant: ICARE Pvt. Ltd. | Duration: 24 months (May 2026 - April 2028) | Working Days: Monday to Friday | Hours: 10:00 - 18:00</p>
    <p>Last Updated: {datetime.now().strftime('%d %B %Y, %H:%M:%S')}</p>
</div>
""", unsafe_allow_html=True)
