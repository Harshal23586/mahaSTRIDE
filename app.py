import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import calendar
import io
import base64

# Page configuration
st.set_page_config(
    page_title="MahaSTRIDE - Quarterly Project Plan Dashboard",
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
    .assignment-title {
        font-size: 1.1rem;
        font-weight: 500;
        margin: 0.5rem 0;
        padding: 0.5rem;
        background-color: rgba(255,255,255,0.1);
        border-radius: 8px;
        text-align: center;
    }
    .parties-info {
        background: linear-gradient(135deg, #2a5298 0%, #1e3c72 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-top: 1rem;
        font-size: 0.9rem;
        border: 1px solid rgba(255,255,255,0.2);
    }
    .quarter-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        transition: transform 0.3s;
    }
    .quarter-card:hover {
        transform: translateY(-5px);
    }
    .milestone-completed {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
    }
    .milestone-achieved {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
    }
    .milestone-upcoming {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
    }
    .stat-card {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
    .status-ongoing {
        background-color: #fff3cd;
        color: #856404;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        display: inline-block;
    }
    .status-completed {
        background-color: #d4edda;
        color: #155724;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        display: inline-block;
    }
    .war-room-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .party-box {
        background: rgba(255,255,255,0.15);
        border-radius: 8px;
        padding: 0.75rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# PROJECT DATA
# ============================================================

PROJECT_NAME = "MahaSTRIDE - Maharashtra Strengthening Institutional Capabilities in Districts for Enabling Growth"
ASSIGNMENT_TITLE = "Engagement of a Consultancy Firm for Comprehensive Data Collection, Advanced Analytics, and Development of Performance Improvement Framework for Maharashtra State Universities under MahaSTRIDE Operations"

CLIENT_NAME = "Maharashtra Institute for Transformation (MITRA), State Data Authority, Government of Maharashtra"
CONSULTANT_NAME = "Indian Centre for Academic Rankings & Excellence - ICARE Pvt. Ltd."

START_DATE = datetime(2026, 5, 5)
END_DATE = datetime(2028, 5, 6)

# Achieved Milestones
ACHIEVED_MILESTONES = [
    {"milestone": "SANGAM Orientation & Training Completed", "date": "May 4-6, 2026", "status": "achieved"},
    {"milestone": "Inception Report & GRDAU Framework Submitted", "date": "May 26, 2026", "status": "achieved"}
]

# Universities Data with GRDAU Status
UNIVERSITIES = {
    "MU": {
        "name": "Mumbai University",
        "location": "Mumbai",
        "vice_chancellor": "Dr. Ravindra Kulkarni",
        "nodal_officer": "Dr. Varsha Kelkar Mane",
        "contact": "+91-22-26543000",
        "coordinators": ["Sneha Kashitkar", "Sagar Teli"],
        "grdau_status": "Completed",
        "grdau_completion_date": "July 5, 2026"
    },
    "SSPU": {
        "name": "Savitribai Phule Pune University",
        "location": "Pune",
        "vice_chancellor": "Dr. Suresh Gosavi",
        "nodal_officer": "Prof. Vinayak Joshi",
        "contact": "+91-20-25696061",
        "coordinators": ["Jagan Sridhar"],
        "grdau_status": "Completed",
        "grdau_completion_date": "July 5, 2026"
    },
    "COEP": {
        "name": "COEP Technological University",
        "location": "Pune",
        "vice_chancellor": "Dr. B. K. Mishra",
        "nodal_officer": "Dr. Uttam Chaskar",
        "contact": "+91-20-25507000",
        "coordinators": ["Vaibhav Ambekar"],
        "grdau_status": "Completed",
        "grdau_completion_date": "July 5, 2026"
    },
    "KBCNMU": {
        "name": "Kavayitri Bahinabai Chaudhari North Maharashtra University",
        "location": "Jalgaon",
        "vice_chancellor": "Dr. R. P. Swami",
        "nodal_officer": "Prof. Sameer Narkhede",
        "contact": "+91-257-2257457",
        "coordinators": ["Nitish Kumbhar"],
        "grdau_status": "Completed",
        "grdau_completion_date": "July 5, 2026"
    },
    "BAMU": {
        "name": "Dr. Babasaheb Ambedkar Marathwada University",
        "location": "Chhatrapati Sambhajinagar",
        "vice_chancellor": "Dr. Pramod Yeole",
        "nodal_officer": "Prof. G. D. Khedkar",
        "contact": "+91-240-2403111",
        "coordinators": ["Atharav Paturkar"],
        "grdau_status": "Completed",
        "grdau_completion_date": "July 5, 2026"
    },
    "NU": {
        "name": "Rashtrasant Tukadoji Maharaj Nagpur University",
        "location": "Nagpur",
        "vice_chancellor": "Dr. Subhash Chaudhari",
        "nodal_officer": "Prof. Nandkishor Karade",
        "contact": "+91-712-2500511",
        "coordinators": ["Anjali Singh"],
        "grdau_status": "Completed",
        "grdau_completion_date": "July 5, 2026"
    },
    "AU": {
        "name": "Sant Gadge Baba Amravati University",
        "location": "Amravati",
        "vice_chancellor": "Dr. Milind Baride",
        "nodal_officer": "Dr. A. B. Naik",
        "contact": "+91-721-2662379",
        "coordinators": ["Prathamesh Babhulkar"],
        "grdau_status": "Completed",
        "grdau_completion_date": "July 5, 2026"
    },
    "MITRA": {
        "name": "MITRA - State Data Authority",
        "location": "Mumbai",
        "ceo": "Shri. Aman Mittal",
        "nodal_officer": "Dr. Harshal Kotwal",
        "contact": "+91-22-69979440",
        "coordinators": ["Shubham Singh"],
        "grdau_status": "Completed",
        "grdau_completion_date": "July 5, 2026"
    }
}

# ============================================================
# QUARTERLY PLAN
# ============================================================

QUARTERS = {
    "Q1: May - July 2026": {
        "number": 1,
        "months": ["May 2026", "June 2026", "July 2026"],
        "status": "ongoing",
        "key_activities": [
            "✅ SANGAM Orientation & Training (May 4-6 at Trident Board Room)",
            "✅ University Onboarding & Data Source Mapping",
            "✅ NIRF Data Collection (Student, Faculty, Research, Placement, Finance)",
            "✅ Inception Report & GRDAU Framework Development",
            "✅ GRDAU Establishment in all universities (Completed July 5, 2026)",
            "🔄 Diagnostic Assessments across all 7 universities",
            "🔄 Gap Analysis against NIRF/NAAC/Global Rankings",
            "🔄 SWOT Analysis for each university"
        ],
        "deliverables": [
            "✅ Inception Report and Deployment Plan (Submitted May 26, 2026)",
            "✅ GRDAUs Established and Operationalized (Completed July 5, 2026)",
            "🔄 Diagnostic Assessment Reports (7 universities) - Due July 31, 2026",
            "🔄 SWOT Analysis Reports - Due July 31, 2026"
        ],
        "milestones": [
            {"name": "SANGAM Training Completed", "status": "achieved", "date": "May 6, 2026"},
            {"name": "Inception Report Submitted", "status": "achieved", "date": "May 26, 2026"},
            {"name": "GRDAU Establishment Completed", "status": "achieved", "date": "July 5, 2026"},
            {"name": "Diagnostic Reports", "status": "in_progress", "date": "July 31, 2026"},
            {"name": "SWOT Analysis Reports", "status": "in_progress", "date": "July 31, 2026"},
            {"name": "Gap Analysis Report", "status": "in_progress", "date": "July 31, 2026"}
        ],
        "data_collection": "NIRF baseline data collection completed. Diagnostic assessments in progress.",
        "stakeholder_engagement": "VC meetings conducted. IQAC coordination established.",
        "review_mechanism": "Weekly GRDAU meetings. Monthly progress review with MITRA PMU."
    },
    "Q2: August - October 2026": {
        "number": 2,
        "months": ["August 2026", "September 2026", "October 2026"],
        "status": "upcoming",
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
        ],
        "milestones": [
            {"name": "IDPs Draft Completed", "status": "pending", "date": "Aug 31, 2026"},
            {"name": "Portal Design Approved", "status": "pending", "date": "Sep 15, 2026"},
            {"name": "Milestone 1: Sustainable Data & Quality Systems", "status": "pending", "date": "Sep 30, 2026"},
            {"name": "Milestone 2: IDP Execution Monitoring", "status": "pending", "date": "Oct 31, 2026"}
        ],
        "data_collection": "IDP data collection. Dashboard requirements gathering.",
        "stakeholder_engagement": "IDP review meetings with VCs. Dashboard workshops.",
        "review_mechanism": "Bi-weekly IDP review. Monthly progress review."
    },
    "Q3: November 2026 - January 2027": {
        "number": 3,
        "months": ["November 2026", "December 2026", "January 2027"],
        "status": "upcoming",
        "key_activities": [
            "Data Portal MVP Deployment",
            "Training Needs Assessment",
            "Capacity Building Programs (First round)",
            "Performance Dashboards Launch",
            "Data Validation and Quality Improvement",
            "Milestone 3: Capacity Building Participation"
        ],
        "deliverables": [
            "Data Portal Live",
            "Training Completion Report",
            "Dashboard Deployment Report"
        ],
        "milestones": [
            {"name": "Portal MVP Launch", "status": "pending", "date": "Nov 15, 2026"},
            {"name": "Mid-term Progress Report", "status": "pending", "date": "Nov 30, 2026"},
            {"name": "First Training Program", "status": "pending", "date": "Dec 15, 2026"},
            {"name": "Milestone 3: Capacity Building", "status": "pending", "date": "Dec 31, 2026"}
        ],
        "data_collection": "Portal data upload. Training feedback collection.",
        "stakeholder_engagement": "Portal training sessions. Capacity building workshops.",
        "review_mechanism": "Portal usage analytics. Training effectiveness assessment."
    },
    "Q4: February - April 2027": {
        "number": 4,
        "months": ["February 2027", "March 2027", "April 2027"],
        "status": "upcoming",
        "key_activities": [
            "Research Output Enhancement Initiatives",
            "International Collaboration Development",
            "Accreditation Preparedness Assessment",
            "Quality Assurance Framework Implementation"
        ],
        "deliverables": [
            "Research Enhancement Plan",
            "Collaboration Framework",
            "QA Framework Report"
        ],
        "milestones": [
            {"name": "Research Enhancement Plan", "status": "pending", "date": "Feb 28, 2027"},
            {"name": "Year 1 Annual Report", "status": "pending", "date": "Apr 30, 2027"}
        ],
        "data_collection": "Research output data. Collaboration metrics.",
        "stakeholder_engagement": "Research committee meetings. Industry collaboration.",
        "review_mechanism": "Research output tracking. QA dashboard monitoring."
    },
    "Q5: May - July 2027": {
        "number": 5,
        "months": ["May 2027", "June 2027", "July 2027"],
        "status": "upcoming",
        "key_activities": [
            "Year 2 Kickoff and Advanced Analytics",
            "Global Ranking Preparation (QS, THE, US News)",
            "Advanced Training Programs",
            "Milestone 4: 10% Improvement Achievement"
        ],
        "deliverables": [
            "Year 2 Work Plan",
            "Ranking Submission Packages",
            "Advanced Training Report",
            "Milestone 4 Report"
        ],
        "milestones": [
            {"name": "QS Ranking Submission", "status": "pending", "date": "Jun 15, 2027"},
            {"name": "Milestone 4: 10% Improvement", "status": "pending", "date": "Jun 30, 2027"}
        ],
        "data_collection": "Ranking data compilation. Improvement metrics.",
        "stakeholder_engagement": "Ranking preparation workshops. Industry advisory board.",
        "review_mechanism": "Quarterly performance review. Ranking submission tracking."
    },
    "Q6: August - October 2027": {
        "number": 6,
        "months": ["August 2027", "September 2027", "October 2027"],
        "status": "upcoming",
        "key_activities": [
            "Employer Perception Enhancement",
            "Academic Reputation Building",
            "Industry Connect Programs",
            "International Student Enrollment Strategies"
        ],
        "deliverables": [
            "Employer Perception Report",
            "Reputation Strategy Document",
            "Industry Connect Report",
            "Internationalization Plan"
        ],
        "milestones": [
            {"name": "Employer Survey Completion", "status": "pending", "date": "Aug 31, 2027"},
            {"name": "International MoUs Signed", "status": "pending", "date": "Sep 30, 2027"}
        ],
        "data_collection": "Employer survey data. Reputation metrics.",
        "stakeholder_engagement": "Employer meets. International partner meetings.",
        "review_mechanism": "Monthly reputation tracking. Employer feedback analysis."
    },
    "Q7: November 2027 - January 2028": {
        "number": 7,
        "months": ["November 2027", "December 2027", "January 2028"],
        "status": "upcoming",
        "key_activities": [
            "Final Global Ranking Submissions",
            "Sustainability Planning",
            "Knowledge Transfer Preparation",
            "Milestone 5: 20% Improvement",
            "Milestone 6: Global Rankings Participation"
        ],
        "deliverables": [
            "Final Ranking Submissions",
            "Sustainability Plan",
            "Knowledge Transfer Report",
            "Milestone 5 & 6 Reports"
        ],
        "milestones": [
            {"name": "Milestone 5: 20% Improvement", "status": "pending", "date": "Dec 31, 2027"},
            {"name": "Milestone 6: Global Rankings", "status": "pending", "date": "Feb 29, 2028"},
            {"name": "Sustainability Plan", "status": "pending", "date": "Dec 15, 2027"}
        ],
        "data_collection": "20% improvement evidence. Ranking participation data.",
        "stakeholder_engagement": "Sustainability workshop. Handover planning.",
        "review_mechanism": "Final evaluation framework. Sustainability assessment."
    },
    "Q8: February - April 2028": {
        "number": 8,
        "months": ["February 2028", "March 2028", "April 2028"],
        "status": "upcoming",
        "key_activities": [
            "Final Evaluation and Reporting",
            "Project Closure and Knowledge Transfer",
            "Milestone 7: Final Evaluation",
            "Contract Completion"
        ],
        "deliverables": [
            "Final Closure Report",
            "Lessons Learned Report",
            "Knowledge Transfer Documentation",
            "Milestone 7 Report"
        ],
        "milestones": [
            {"name": "Milestone 7: Final Evaluation", "status": "pending", "date": "Apr 30, 2028"},
            {"name": "Project Closure", "status": "pending", "date": "May 6, 2028"}
        ],
        "data_collection": "Final performance metrics. Lessons learned.",
        "stakeholder_engagement": "Final client presentation. Project closure meeting.",
        "review_mechanism": "Final evaluation. Client satisfaction survey."
    }
}

# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

# Initialize session state for navigation if not exists
if 'nav_selection' not in st.session_state:
    st.session_state.nav_selection = "summary"

with st.sidebar:
    st.markdown("## 🎯 MahaSTRIDE")
    st.markdown("---")
    
    # Navigation with callback to update session state
    nav_options = {
        "🏠 Executive Summary": "summary",
        "📊 Quarterly Plan": "quarterly",
        "🏫 Universities & Team": "universities",
        "🏛️ War Room & GRDAU": "warroom",
        "🎯 Milestones Tracker": "milestones",
        "📋 Deliverables": "deliverables",
        "🔄 Review Mechanisms": "review",
        "📁 Documents": "documents",
        "📥 Export Reports": "export"
    }
    
    # Create radio button and store selection
    selected_nav = st.radio(
        "Navigation", 
        list(nav_options.keys()), 
        label_visibility="collapsed",
        key="nav_radio"
    )
    
    # Update session state based on selection
    st.session_state.nav_selection = nav_options[selected_nav]
    
    st.markdown("---")
    st.markdown("### ℹ️ Project Info")
    st.markdown(f"**Start Date:** {START_DATE.strftime('%d %b %Y')}")
    st.markdown(f"**End Date:** {END_DATE.strftime('%d %b %Y')}")
    st.markdown(f"**Duration:** 24 months (8 Quarters)")
    st.markdown(f"**Universities:** 7")
    st.markdown(f"**Data Analysts:** 10")
    
    st.markdown("---")
    st.markdown("### ✅ Achievements")
    for achievement in ACHIEVED_MILESTONES:
        st.markdown(f"- ✅ {achievement['milestone']}")
    
    st.markdown("---")
    st.markdown("### 📞 Contact")
    st.markdown("**PMU MahaSTRIDE**")
    st.markdown("📧 pmu.mahastride@mahamitra.org")
    st.markdown("📞 022-69979440")
    st.markdown("📍 5th Floor, Nirmal Building, Nariman Point, Mumbai-400021")

# ============================================================
# MAIN CONTENT
# ============================================================

# Main Header with Assignment Title and Parties
st.markdown(f"""
<div class="main-header">
    <h1>🎯 {PROJECT_NAME}</h1>
    <div class="assignment-title">
        📋 {ASSIGNMENT_TITLE}
    </div>
    <div class="parties-info">
        <div class="party-box">
            <strong>🏛️ Client:</strong> {CLIENT_NAME}
        </div>
        <div class="party-box">
            <strong>🤝 Consultant:</strong> {CONSULTANT_NAME}
        </div>
        <p style="margin-top:0.5rem; font-size:0.85rem;">World Bank Loan No: IBRD 9737-IN | RFP Ref: IN-MITRA(PMU)-PforR-Edu-QCBS</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# CONTENT RENDERING BASED ON NAVIGATION
# ============================================================

selected_key = st.session_state.nav_selection

# 1. EXECUTIVE SUMMARY
if selected_key == "summary":
    st.header("📋 Executive Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <h2>Q1</h2>
            <p>Phase 1 - Ongoing</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <h2>2</h2>
            <p>Milestones Achieved</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <h2>7</h2>
            <p>GRDAUs Established</p>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <h2>10</h2>
            <p>Team Members</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.subheader("🎯 Current Status")
    st.markdown("""
    <div class="status-ongoing">Q1: May - July 2026 - ONGOING</div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.subheader("✅ Achievements So Far")
    
    for achievement in ACHIEVED_MILESTONES:
        st.markdown(f"""
        <div class="milestone-achieved">
            ✅ <strong>{achievement['milestone']}</strong><br>
            📅 Completed: {achievement['date']}
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.subheader("🏆 GRDAU Establishment Status")
    st.markdown("""
    <div class="milestone-completed">
        ✅ <strong>GRDAUs Established and Operationalized in all 7 universities</strong><br>
        📅 Completed: July 5, 2026
    </div>
    """, unsafe_allow_html=True)

# 2. QUARTERLY PLAN
elif selected_key == "quarterly":
    st.header("📅 8-Quarter Project Plan (May 2026 - April 2028)")
    st.markdown("Working Days: Monday to Friday | Hours: 10:00 AM - 6:00 PM")
    st.markdown("---")
    
    quarter_tabs = st.tabs(list(QUARTERS.keys()))
    
    for tab, (quarter_name, quarter_info) in zip(quarter_tabs, QUARTERS.items()):
        with tab:
            status_display = "🟡 ONGOING" if quarter_info["status"] == "ongoing" else "⚪ UPCOMING"
            st.markdown(f"""
            <div class="quarter-card">
                <h2>{quarter_name}</h2>
                <p><strong>Months:</strong> {', '.join(quarter_info['months'])}</p>
                <p><strong>Status:</strong> {status_display}</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 🎯 Key Activities")
                for activity in quarter_info["key_activities"]:
                    st.markdown(f"- {activity}")
                
                st.markdown("---")
                st.markdown("### 📊 Data Collection Processes")
                st.markdown(quarter_info["data_collection"])
                
                st.markdown("---")
                st.markdown("### 🤝 Stakeholder Engagement")
                st.markdown(quarter_info["stakeholder_engagement"])
            
            with col2:
                st.markdown("### 📦 Deliverables")
                for deliverable in quarter_info["deliverables"]:
                    st.markdown(f"- {deliverable}")
                
                st.markdown("---")
                st.markdown("### 🎯 Milestones")
                for milestone in quarter_info["milestones"]:
                    if milestone["status"] == "achieved":
                        icon = "✅"
                        color = "#d4edda"
                    elif milestone["status"] == "in_progress":
                        icon = "🔄"
                        color = "#fff3cd"
                    else:
                        icon = "⏳"
                        color = "#f8f9fa"
                    st.markdown(f"""
                    <div style="background-color:{color}; padding:0.5rem; margin:0.3rem 0; border-radius:5px;">
                        {icon} <strong>{milestone['name']}</strong><br>
                        📅 Target: {milestone['date']}
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("---")
                st.markdown("### 🔄 Review Mechanism")
                st.markdown(quarter_info["review_mechanism"])
            
            st.markdown("---")

# 3. UNIVERSITIES & TEAM
elif selected_key == "universities":
    st.header("🏫 Universities & Team Structure")
    
    st.subheader("📋 Participating Universities with GRDAU Status")
    
    for code, uni in UNIVERSITIES.items():
        with st.expander(f"🏛️ {uni['name']} ({code})"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                **📍 Location:** {uni['location']}<br>
                **👨‍🎓 Vice Chancellor:** {uni.get('vice_chancellor', uni.get('ceo', 'N/A'))}<br>
                **👤 Nodal Officer:** {uni.get('nodal_officer', 'N/A')}<br>
                **📞 Contact:** {uni.get('contact', 'N/A')}
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                **👥 Coordinators:** {', '.join(uni.get('coordinators', []))}<br>
                **🏛️ GRDAU Status:** <span class="status-completed">✅ {uni['grdau_status']}</span><br>
                **📅 Completion Date:** {uni.get('grdau_completion_date', 'N/A')}
                """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.subheader("👥 Project Team (May 2026 Attendance)")
    
    team_data = {
        "Name": ["Dr. Harshal Kotwal", "Shubham Singh", "Sagar Teli", "Sneha Kashitkar", "Nitish Kumbhar",
                "Anjali Singh", "Vaibhav Ambekar", "Atharav Paturkar", "Prathamesh Babhulkar", "Jagan Sridhar"],
        "Role": ["Project Lead", "Data Analytics Specialist", "Statistician & Program Designer", 
                "Institutional Coordinator", "Institutional Coordinator", "Institutional Coordinator",
                "Institutional Coordinator", "Institutional Coordinator", "Institutional Coordinator", "Institutional Coordinator"],
        "University": ["ICARE", "MITRA", "Mumbai University", "Mumbai University", "KBCNMU Jalgaon",
                      "Nagpur University", "COEP Pune", "BAMU Aurangabad", "Amravati University", "SPPU Pune"]
    }
    
    df_team = pd.DataFrame(team_data)
    st.dataframe(df_team, use_container_width=True, hide_index=True)

# 4. WAR ROOM & GRDAU
elif selected_key == "warroom":
    st.header("🏛️ War Room & GRDAU Setup")
    
    st.markdown("""
    <div class="war-room-card">
        <h2>🎯 Project War Room - MITRA, Mumbai</h2>
        <p><strong>Location:</strong> 5th Floor, Nirmal Building, Nariman Point, Mumbai-400021</p>
        <p><strong>Purpose:</strong> Central command center for project monitoring, coordination, and decision-making</p>
        <p><strong>Facilities:</strong> Real-time dashboards, video conferencing, data visualization tools</p>
        <p><strong>Weekly Meetings:</strong> Every Monday at 11:00 AM</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.subheader("🏫 Global Ranking Data Analytics Units (GRDAUs)")
    
    st.markdown("""
    ### ✅ GRDAU Establishment Status - COMPLETED (July 5, 2026)
    
    All 7 universities have successfully established their GRDAUs.
    """)
    
    st.markdown("---")
    
    st.subheader("📍 GRDAU Establishment Status - ALL COMPLETED")
    
    grdau_data = []
    for code, uni in UNIVERSITIES.items():
        if code != "MITRA":
            grdau_data.append({
                "University": uni["name"],
                "Location": uni["location"],
                "Coordinator": ", ".join(uni["coordinators"]),
                "Status": "✅ Completed",
                "Completion Date": "July 5, 2026"
            })
    
    st.dataframe(pd.DataFrame(grdau_data), use_container_width=True, hide_index=True)

# 5. MILESTONES TRACKER
elif selected_key == "milestones":
    st.header("🎯 Project Milestones Tracker")
    
    st.subheader("✅ Achieved Milestones (2)")
    for achievement in ACHIEVED_MILESTONES:
        st.markdown(f"""
        <div class="milestone-achieved">
            ✅ <strong>{achievement['milestone']}</strong><br>
            📅 Completed: {achievement['date']}
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.subheader("✅ GRDAU Establishment - COMPLETED")
    st.markdown("""
    <div class="milestone-completed">
        ✅ <strong>GRDAUs Established and Operationalized in all 7 universities</strong><br>
        📅 Completed: July 5, 2026
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.subheader("🔄 In Progress Milestones (Q1)")
    
    current_milestones = [
        {"name": "Diagnostic Assessment Reports", "target": "July 31, 2026", "progress": 60},
        {"name": "SWOT Analysis Reports", "target": "July 31, 2026", "progress": 50},
        {"name": "Gap Analysis against NIRF/Global Rankings", "target": "July 31, 2026", "progress": 40}
    ]
    
    for milestone in current_milestones:
        st.markdown(f"**{milestone['name']}** - Target: {milestone['target']}")
        st.progress(milestone['progress']/100)
        st.caption(f"Progress: {milestone['progress']}%")
        st.markdown("---")
    
    st.markdown("---")
    
    st.subheader("⏳ Upcoming Milestones")
    
    upcoming = [
        {"milestone": "Institutional Development Plans (IDPs)", "date": "August 14, 2026", "quarter": "Q2"},
        {"milestone": "Milestone 1: Sustainable Data & Quality Systems", "date": "September 30, 2026", "quarter": "Q2"},
        {"milestone": "Milestone 2: IDP Execution Monitoring", "date": "October 31, 2026", "quarter": "Q2"},
        {"milestone": "Data Portal MVP Deployment", "date": "November 15, 2026", "quarter": "Q3"},
        {"milestone": "Milestone 3: Capacity Building (60% participation)", "date": "December 31, 2026", "quarter": "Q3"}
    ]
    
    for milestone in upcoming:
        st.markdown(f"""
        <div class="milestone-upcoming">
            ⏳ <strong>{milestone['milestone']}</strong><br>
            📅 Target: {milestone['date']} | 📍 Quarter: {milestone['quarter']}
        </div>
        """, unsafe_allow_html=True)

# 6. DELIVERABLES
elif selected_key == "deliverables":
    st.header("📋 Contract Deliverables Status")
    
    deliverables = [
        {"deliverable": "Inception Report and Deployment Plan", "due_date": "Jun 5, 2026", "status": "completed", "actual": "May 26, 2026"},
        {"deliverable": "GRDAUs Established and Operationalized", "due_date": "Jul 5, 2026", "status": "completed", "actual": "July 5, 2026"},
        {"deliverable": "Diagnostic Assessment Reports", "due_date": "Jul 31, 2026", "status": "in_progress", "actual": None},
        {"deliverable": "SWOT Analysis Reports", "due_date": "Jul 31, 2026", "status": "in_progress", "actual": None},
        {"deliverable": "Institutional Development Plans (IDPs)", "due_date": "Aug 14, 2026", "status": "pending", "actual": None},
        {"deliverable": "Mid-term Progress Report", "due_date": "Nov 30, 2026", "status": "pending", "actual": None},
        {"deliverable": "Final Closure Report", "due_date": "May 6, 2028", "status": "pending", "actual": None}
    ]
    
    for deliverable in deliverables:
        if deliverable["status"] == "completed":
            icon = "✅"
            color = "#d4edda"
        elif deliverable["status"] == "in_progress":
            icon = "🔄"
            color = "#fff3cd"
        else:
            icon = "⏳"
            color = "#f8f9fa"
        
        actual_text = f"<br>✅ Actual Submission: {deliverable['actual']}" if deliverable.get('actual') else ""
        
        st.markdown(f"""
        <div style="background-color:{color}; padding:1rem; margin:0.5rem 0; border-radius:8px;">
            <strong>{icon} {deliverable['deliverable']}</strong><br>
            📅 Due: {deliverable['due_date']}<br>
            📊 Status: {deliverable['status'].upper()}
            {actual_text}
        </div>
        """, unsafe_allow_html=True)

# 7. REVIEW MECHANISMS
elif selected_key == "review":
    st.header("🔄 Review & Monitoring Mechanisms")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### Weekly Reviews
        - **GRDAU Weekly Meetings:** Every Monday, 11:00 AM
        - **Data Validation Sessions:** Every Wednesday
        - **Progress Tracking:** Daily dashboard updates
        
        ### Monthly Reviews
        - **Monthly Progress Report (MPR)** submission by 10th
        - **PMU Review Meeting:** Second week of each month
        - **Attendance Verification:** By 9th of each month
        """)
    
    with col2:
        st.markdown("""
        ### Quarterly Reviews
        - **Quarterly Performance Assessment**
        - **Steering Committee Meeting**
        - **Milestone Achievement Evaluation**
        
        ### Annual Reviews
        - **Annual Performance Report**
        - **World Bank Progress Review**
        - **Strategic Planning Session**
        """)
    
    st.markdown("---")
    
    st.subheader("📋 Reporting Structure")
    
    st.markdown("""
    | Level | Responsible | Reports To | Frequency |
    |-------|-------------|------------|-----------|
    | University Level | Institutional Coordinator | Nodal Officer | Daily |
    | University Level | Nodal Officer | VC + PMU | Weekly |
    | PMU Level | Project Director | MITRA CEO | Weekly |
    | Steering Committee | Chairperson | Government | Quarterly |
    | World Bank | MITRA | World Bank | Bi-annually |
    """)

# 8. DOCUMENTS
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
        ### 📊 Submitted Reports
        - ✅ Consolidated MPR - May 2026
        - ✅ Inception Report
        - ✅ Work Order (ICARE)
        
        ### 🏛️ Government Orders
        - Planning Department GRs
        - State Steering Committee Minutes
        - Administrative Approvals
        """)
    
    st.markdown("---")
    
    st.subheader("📎 Key Document Status")
    
    doc_status = {
        "Document": ["Contract Agreement", "Work Order", "Performance Bank Guarantee", "Inception Report", "May MPR", "GRDAU Establishment", "Diagnostic Reports"],
        "Status": ["✅ Executed", "✅ Issued", "⏳ Pending", "✅ Submitted", "✅ Submitted", "✅ Completed", "🔄 In Progress"],
        "Due Date": ["Signed", "Mar 25, 2026", "Within 15 days", "May 26, 2026", "May 29, 2026", "July 5, 2026", "July 31, 2026"]
    }
    
    st.dataframe(pd.DataFrame(doc_status), use_container_width=True, hide_index=True)

# 9. EXPORT REPORTS
elif selected_key == "export":
    st.header("📥 Export Reports")
    st.markdown("Export quarterly reports in Excel format.")
    st.info("ℹ️ This feature is coming soon. Please check back later.")

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #666; font-size: 0.8rem;">
    <p>© 2026-2028 {CLIENT_NAME} | MahaSTRIDE Project | World Bank Loan No: IBRD 9737-IN</p>
    <p>Consultant: {CONSULTANT_NAME} | Duration: 24 months (8 Quarters) | Working Days: Monday to Friday | Hours: 10:00 - 18:00</p>
    <p>Last Updated: {datetime.now().strftime('%d %B %Y, %H:%M:%S')}</p>
</div>
""", unsafe_allow_html=True)
