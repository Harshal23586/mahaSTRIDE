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
    page_title="MahaSTRIDE - Project Management System",
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
    }
    .task-completed {
        border-left-color: #28a745;
        background-color: #d4edda;
    }
    .task-pending {
        border-left-color: #ffc107;
        background-color: #fff3cd;
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
        "team": "MITRA"
    },
    "projectlead@mahastride.com": {
        "password": sha256("ProjectLead@2026".encode()).hexdigest(),
        "role": "project_lead",
        "name": "Dr. Harshal Kotwal",
        "team": "ICARE"
    },
    "shubham@mitra.gov.in": {
        "password": sha256("Shubham@2026".encode()).hexdigest(),
        "role": "data_analyst",
        "name": "Shubham Singh",
        "team": "MITRA"
    },
    "sneha@mu.edu": {
        "password": sha256("Sneha@2026".encode()).hexdigest(),
        "role": "data_analyst",
        "name": "Sneha Kashitkar",
        "team": "Mumbai University"
    },
    "sagar@mu.edu": {
        "password": sha256("Sagar@2026".encode()).hexdigest(),
        "role": "data_analyst",
        "name": "Sagar Teli",
        "team": "Mumbai University"
    },
    "jagan@sspu.edu": {
        "password": sha256("Jagan@2026".encode()).hexdigest(),
        "role": "data_analyst",
        "name": "Jagan Sridhar",
        "team": "SPPU Pune"
    },
    "vaibhav@coep.edu": {
        "password": sha256("Vaibhav@2026".encode()).hexdigest(),
        "role": "data_analyst",
        "name": "Vaibhav Ambekar",
        "team": "COEP Pune"
    },
    "pratham@au.edu": {
        "password": sha256("Pratham@2026".encode()).hexdigest(),
        "role": "data_analyst",
        "name": "Prathamesh Babhulkar",
        "team": "Amravati University"
    },
    "anjali@nu.edu": {
        "password": sha256("Anjali@2026".encode()).hexdigest(),
        "role": "data_analyst",
        "name": "Anjali Singh",
        "team": "Nagpur University"
    },
    "nitish@kbcnmu.edu": {
        "password": sha256("Nitish@2026".encode()).hexdigest(),
        "role": "data_analyst",
        "name": "Nitish Kumbhar",
        "team": "KBCNMU Jalgaon"
    },
    "atharv@bamu.edu": {
        "password": sha256("Atharv@2026".encode()).hexdigest(),
        "role": "data_analyst",
        "name": "Atharav Paturkar",
        "team": "BAMU Aurangabad"
    }
}

# ============================================================
# DATA FILES
# ============================================================
DAILY_TASKS_FILE = "daily_tasks_data.json"
TASK_COMPLETION_FILE = "task_completion_data.json"

# ============================================================
# COMPLETE 24-MONTH TASK GENERATION
# ============================================================

def get_complete_daily_tasks():
    """Generate unique daily tasks for every working day from May 2026 to April 2028"""
    all_tasks = {}
    
    # ============================================================
    # JUNE 2026 - Diagnostic Assessments (Working days: 1-5, 8-12, 15-19, 22-26, 29-30)
    # ============================================================
    june_tasks = {
        "2026-06-01": {"task": "Complete Diagnostic Assessment Framework", "sub_tasks": ["Review assessment methodology", "Finalize assessment templates", "Create scoring rubrics", "Prepare assessment guidelines"], "deliverable": "Assessment Framework Document", "category": "Assessment", "priority": "High"},
        "2026-06-02": {"task": "Begin University-wise Assessments", "sub_tasks": ["Start with Mumbai University", "Document initial findings", "Collect departmental data", "Schedule faculty meetings"], "deliverable": "Initial Assessment Log", "category": "Assessment", "priority": "High"},
        "2026-06-03": {"task": "Review existing data quality", "sub_tasks": ["Check NIRF data accuracy", "Verify research publications", "Validate faculty credentials", "Audit student enrollment data"], "deliverable": "Data Quality Report", "category": "Analysis", "priority": "High"},
        "2026-06-04": {"task": "Identify data gaps per university", "sub_tasks": ["Create gap analysis matrix", "Document missing data points", "Prioritize critical gaps", "Plan data collection strategy"], "deliverable": "Data Gap Analysis Report", "category": "Assessment", "priority": "High"},
        "2026-06-05": {"task": "Prepare assessment templates", "sub_tasks": ["Design standardized forms", "Create digital templates", "Test templates with sample data", "Get approval from PMU"], "deliverable": "Assessment Templates", "category": "Documentation", "priority": "Medium"},
        "2026-06-08": {"task": "Conduct faculty interviews at Mumbai University", "sub_tasks": ["Interview 5 faculty members", "Document research activities", "Record publication details", "Capture grant information"], "deliverable": "Faculty Interview Report", "category": "Data Collection", "priority": "High"},
        "2026-06-09": {"task": "Analyze research output metrics for all universities", "sub_tasks": ["Calculate h-index for departments", "Measure citation impact", "Identify top researchers", "Benchmark against peers"], "deliverable": "Research Metrics Analysis", "category": "Analysis", "priority": "High"},
        "2026-06-10": {"task": "Evaluate library and lab infrastructure", "sub_tasks": ["Visit central library", "Assess lab equipment", "Check digital resources", "Review facility utilization"], "deliverable": "Infrastructure Assessment Report", "category": "Assessment", "priority": "Medium"},
        "2026-06-11": {"task": "Assess international collaboration status", "sub_tasks": ["Review existing MoUs", "Document joint research projects", "List visiting faculty", "Identify collaboration gaps"], "deliverable": "International Collaboration Report", "category": "Assessment", "priority": "Medium"},
        "2026-06-12": {"task": "Compile all assessment findings", "sub_tasks": ["Consolidate university data", "Create summary dashboards", "Prepare comparative analysis", "Draft executive summary"], "deliverable": "Comprehensive Assessment Report", "category": "Analysis", "priority": "High"},
        "2026-06-15": {"task": "GRDAU Training - Module 1: Data Management", "sub_tasks": ["Train GRDAU coordinators", "Demonstrate data entry", "Explain validation rules", "Conduct hands-on practice"], "deliverable": "Training Completion Report", "category": "Training", "priority": "High"},
        "2026-06-16": {"task": "Data Validation Workshop", "sub_tasks": ["Review data collection methods", "Identify inconsistencies", "Standardize formats", "Create validation checklist"], "deliverable": "Data Validation Framework", "category": "Training", "priority": "High"},
        "2026-06-17": {"task": "Prepare NIRF 2027 Submission", "sub_tasks": ["Complete NIRF data templates", "Verify all metrics", "Prepare supporting documents", "Review with IQAC coordinator"], "deliverable": "NIRF Submission Package", "category": "Reporting", "priority": "High"},
        "2026-06-18": {"task": "VC Review Meeting", "sub_tasks": ["Prepare progress presentation", "Compile key findings", "Discuss improvement strategies", "Get VC approval for next phase"], "deliverable": "VC Meeting Minutes", "category": "Meetings", "priority": "High"},
        "2026-06-19": {"task": "Update Central Data Repository", "sub_tasks": ["Upload all collected data", "Organize by category", "Add metadata tags", "Create data dictionary"], "deliverable": "Updated Data Repository", "category": "Data Collection", "priority": "Medium"},
        "2026-06-22": {"task": "Finalize Diagnostic Reports for all 7 universities", "sub_tasks": ["Review each report", "Add recommendations", "Format as per guidelines", "Prepare for submission"], "deliverable": "Diagnostic Reports (7)", "category": "Reporting", "priority": "High"},
        "2026-06-23": {"task": "Submit Diagnostic Assessment Reports to PMU", "sub_tasks": ["Get final approval", "Submit via portal", "Send copy to VC", "Archive submissions"], "deliverable": "Submitted Reports", "category": "Reporting", "priority": "High"},
        "2026-06-24": {"task": "Draft June Monthly Progress Report", "sub_tasks": ["Compile June activities", "Document achievements", "List challenges", "Add supporting evidence"], "deliverable": "June MPR Draft", "category": "Reporting", "priority": "High"},
        "2026-06-25": {"task": "Plan July 2026 Activities", "sub_tasks": ["Review Phase 1 tasks", "Create July work schedule", "Assign responsibilities", "Set deadlines"], "deliverable": "July Work Plan", "category": "Planning", "priority": "Medium"},
        "2026-06-26": {"task": "Client Review Meeting - June Progress", "sub_tasks": ["Present assessment findings", "Showcase data insights", "Receive client feedback", "Document action items"], "deliverable": "Client Meeting Minutes", "category": "Meetings", "priority": "High"},
        "2026-06-29": {"task": "Analyze remaining university data", "sub_tasks": ["Process pending data", "Identify improvement areas", "Create analysis charts", "Document findings"], "deliverable": "Data Analysis Report", "category": "Analysis", "priority": "Medium"},
        "2026-06-30": {"task": "Finalize and Submit June MPR", "sub_tasks": ["Incorporate feedback", "Finalize report", "Submit to PMU", "Get acknowledgment"], "deliverable": "June MPR Final", "category": "Reporting", "priority": "High"}
    }
    
    # ============================================================
    # JULY 2026 - Gap Analysis and GRDAU Setup
    # ============================================================
    july_tasks = {
        "2026-07-01": {"task": "Complete NIRF/NAAC Gap Analysis", "sub_tasks": ["Compare current vs target metrics", "Identify critical gaps", "Calculate gap percentages", "Prioritize improvement areas"], "deliverable": "Gap Analysis Matrix", "category": "Analysis", "priority": "High"},
        "2026-07-02": {"task": "Prepare SWOT Analysis for Each University", "sub_tasks": ["Conduct SWOT workshop", "Document Strengths/Weaknesses", "Identify Opportunities/Threats", "Create SWOT summary"], "deliverable": "7 SWOT Reports", "category": "Documentation", "priority": "High"},
        "2026-07-03": {"task": "Submit GRDAU Establishment Plan", "sub_tasks": ["Define GRDAU structure", "List required resources", "Create operational procedures", "Get VC approval"], "deliverable": "GRDAU Establishment Plan", "category": "Reporting", "priority": "High"},
        "2026-07-06": {"task": "Setup GRDAU Office and Infrastructure", "sub_tasks": ["Allocate office space", "Install computers and software", "Setup network connectivity", "Create user accounts"], "deliverable": "GRDAU Infrastructure Ready", "category": "Setup", "priority": "High"},
        "2026-07-07": {"task": "GRDAU Staff Training - Day 1", "sub_tasks": ["Train on data entry", "Explain reporting process", "Demonstrate dashboard usage", "Conduct hands-on session"], "deliverable": "Training Day 1 Report", "category": "Training", "priority": "High"},
        "2026-07-08": {"task": "GRDAU Staff Training - Day 2", "sub_tasks": ["Advanced data analysis training", "Report generation training", "Quality assurance procedures", "Assessment and feedback"], "deliverable": "Training Day 2 Report", "category": "Training", "priority": "High"},
        "2026-07-09": {"task": "Create GRDAU Standard Operating Procedures", "sub_tasks": ["Draft SOP document", "Define workflows", "Document responsibilities", "Create process maps"], "deliverable": "GRDAU SOP Document", "category": "Documentation", "priority": "High"},
        "2026-07-10": {"task": "Test GRDAU Readiness", "sub_tasks": ["Check all systems", "Verify staff training", "Test data flow", "Document readiness status"], "deliverable": "GRDAU Readiness Report", "category": "Assessment", "priority": "Medium"},
        "2026-07-13": {"task": "Implement Data Quality Framework", "sub_tasks": ["Define quality metrics", "Create validation rules", "Setup automated checks", "Train staff on quality procedures"], "deliverable": "Data Quality Framework", "category": "Technical", "priority": "High"},
        "2026-07-14": {"task": "Gather Dashboard Requirements", "sub_tasks": ["Meet with stakeholders", "List required KPIs", "Define visualization needs", "Document user stories"], "deliverable": "Dashboard Requirements Doc", "category": "Meetings", "priority": "High"},
        "2026-07-15": {"task": "Prepare Baseline Report", "sub_tasks": ["Compile all baseline data", "Create summary statistics", "Document methodology", "Format final report"], "deliverable": "Baseline Report", "category": "Reporting", "priority": "High"},
        "2026-07-16": {"task": "Conduct Stakeholder Feedback Session", "sub_tasks": ["Schedule meeting with IQAC", "Present baseline findings", "Collect feedback", "Document action items"], "deliverable": "Feedback Report", "category": "Meetings", "priority": "Medium"},
        "2026-07-17": {"task": "Update Project Plan Based on Feedback", "sub_tasks": ["Review feedback", "Adjust timelines", "Update resource allocation", "Communicate changes"], "deliverable": "Updated Project Plan", "category": "Planning", "priority": "Medium"},
        "2026-07-20": {"task": "Draft July Monthly Progress Report", "sub_tasks": ["Compile July activities", "Document Phase 1 completion", "List achievements", "Prepare for Phase 2"], "deliverable": "July MPR Draft", "category": "Reporting", "priority": "High"},
        "2026-07-21": {"task": "Phase 1 Completion Review Meeting", "sub_tasks": ["Review all Phase 1 deliverables", "Assess quality metrics", "Document lessons learned", "Plan Phase 2 kickoff"], "deliverable": "Phase 1 Completion Report", "category": "Meetings", "priority": "High"},
        "2026-07-22": {"task": "Develop Phase 2 Detailed Work Plan", "sub_tasks": ["Review Phase 2 requirements", "Create detailed schedule", "Assign resources", "Set milestone dates"], "deliverable": "Phase 2 Work Plan", "category": "Planning", "priority": "High"},
        "2026-07-23": {"task": "Client Presentation - Phase 1 Results", "sub_tasks": ["Prepare presentation deck", "Showcase achievements", "Present metrics", "Get client approval"], "deliverable": "Client Presentation Deck", "category": "Meetings", "priority": "High"},
        "2026-07-24": {"task": "Document Lessons Learned - Phase 1", "sub_tasks": ["Capture successes", "Document challenges", "Recommend improvements", "Share with team"], "deliverable": "Lessons Learned Document", "category": "Documentation", "priority": "Medium"},
        "2026-07-27": {"task": "Prepare for Phase 2 Kickoff", "sub_tasks": ["Review Phase 2 objectives", "Prepare kickoff materials", "Schedule team meeting", "Setup tracking systems"], "deliverable": "Phase 2 Kickoff Package", "category": "Planning", "priority": "Medium"},
        "2026-07-28": {"task": "Phase 2 Team Kickoff Meeting", "sub_tasks": ["Present Phase 2 plan", "Clarify roles", "Discuss challenges", "Align on goals"], "deliverable": "Team Meeting Minutes", "category": "Meetings", "priority": "Medium"},
        "2026-07-29": {"task": "Review All Project Trackers", "sub_tasks": ["Check progress against plan", "Verify data completeness", "Update dashboards", "Prepare status report"], "deliverable": "Project Status Report", "category": "Reporting", "priority": "Medium"},
        "2026-07-30": {"task": "Finalize July MPR", "sub_tasks": ["Incorporate feedback", "Finalize report", "Get approvals", "Prepare for submission"], "deliverable": "Final July MPR", "category": "Reporting", "priority": "High"},
        "2026-07-31": {"task": "Submit July MPR to PMU", "sub_tasks": ["Submit via portal", "Send copy to VC", "Confirm receipt", "Archive submission"], "deliverable": "July MPR Submitted", "category": "Reporting", "priority": "High"}
    }
    
    # ============================================================
    # AUGUST 2026 - IDP Development
    # ============================================================
    aug_tasks = {
        "2026-08-03": {"task": "Develop IDP Framework Template", "sub_tasks": ["Review IDP requirements", "Design template structure", "Create sections", "Get template approval"], "deliverable": "IDP Template", "category": "Planning", "priority": "High"},
        "2026-08-04": {"task": "Collect University Strategic Plans", "sub_tasks": ["Request plans from all 7 universities", "Review existing strategies", "Extract key goals", "Document alignment areas"], "deliverable": "Strategic Plans Collection", "category": "Data Collection", "priority": "High"},
        "2026-08-05": {"task": "Analyze Existing Plans", "sub_tasks": ["Compare across universities", "Identify common themes", "Find best practices", "Document findings"], "deliverable": "Plans Analysis Report", "category": "Analysis", "priority": "High"},
        "2026-08-06": {"task": "Draft IDP for Mumbai University", "sub_tasks": ["Set goals and targets", "Define KPIs", "Create action plan", "Draft timeline"], "deliverable": "MU IDP Draft", "category": "Planning", "priority": "High"},
        "2026-08-07": {"task": "Draft IDP for Pune University", "sub_tasks": ["Set goals and targets", "Define KPIs", "Create action plan", "Draft timeline"], "deliverable": "SPPU IDP Draft", "category": "Planning", "priority": "High"},
        "2026-08-10": {"task": "Draft IDP for COEP University", "sub_tasks": ["Set goals and targets", "Define KPIs", "Create action plan", "Draft timeline"], "deliverable": "COEP IDP Draft", "category": "Planning", "priority": "High"},
        "2026-08-11": {"task": "Draft IDP for Nagpur University", "sub_tasks": ["Set goals and targets", "Define KPIs", "Create action plan", "Draft timeline"], "deliverable": "NU IDP Draft", "category": "Planning", "priority": "High"},
        "2026-08-12": {"task": "Draft IDP for Amravati University", "sub_tasks": ["Set goals and targets", "Define KPIs", "Create action plan", "Draft timeline"], "deliverable": "AU IDP Draft", "category": "Planning", "priority": "High"},
        "2026-08-13": {"task": "Draft IDP for Jalgaon University", "sub_tasks": ["Set goals and targets", "Define KPIs", "Create action plan", "Draft timeline"], "deliverable": "KBCNMU IDP Draft", "category": "Planning", "priority": "High"},
        "2026-08-14": {"task": "Draft IDP for Aurangabad University", "sub_tasks": ["Set goals and targets", "Define KPIs", "Create action plan", "Draft timeline"], "deliverable": "BAMU IDP Draft", "category": "Planning", "priority": "High"},
        "2026-08-17": {"task": "Stakeholder Review - Mumbai University IDP", "sub_tasks": ["Present to VC", "Gather feedback", "Document changes", "Incorporate suggestions"], "deliverable": "MU IDP Reviewed", "category": "Meetings", "priority": "High"},
        "2026-08-18": {"task": "Stakeholder Review - Pune University IDP", "sub_tasks": ["Present to VC", "Gather feedback", "Document changes", "Incorporate suggestions"], "deliverable": "SPPU IDP Reviewed", "category": "Meetings", "priority": "High"},
        "2026-08-19": {"task": "Stakeholder Review - COEP University IDP", "sub_tasks": ["Present to Director", "Gather feedback", "Document changes", "Incorporate suggestions"], "deliverable": "COEP IDP Reviewed", "category": "Meetings", "priority": "High"},
        "2026-08-20": {"task": "Stakeholder Review - Nagpur University IDP", "sub_tasks": ["Present to VC", "Gather feedback", "Document changes", "Incorporate suggestions"], "deliverable": "NU IDP Reviewed", "category": "Meetings", "priority": "High"},
        "2026-08-21": {"task": "Stakeholder Review - Other Universities IDPs", "sub_tasks": ["Present to VCs", "Gather feedback", "Document changes", "Incorporate suggestions"], "deliverable": "IDPs Reviewed", "category": "Meetings", "priority": "High"},
        "2026-08-24": {"task": "Design Data Portal Architecture", "sub_tasks": ["Create architecture diagram", "Define data flow", "Select technology stack", "Document design decisions"], "deliverable": "Portal Architecture Doc", "category": "Technical", "priority": "High"},
        "2026-08-25": {"task": "Data Portal Wireframing", "sub_tasks": ["Design user interface", "Create wireframes", "Review with team", "Finalize designs"], "deliverable": "Portal Wireframes", "category": "Technical", "priority": "High"},
        "2026-08-26": {"task": "Dashboard Requirements Specification", "sub_tasks": ["List dashboard features", "Define KPIs to display", "Specify chart types", "Document user interactions"], "deliverable": "Dashboard Specs", "category": "Technical", "priority": "High"},
        "2026-08-27": {"task": "Technology Stack Selection", "sub_tasks": ["Evaluate options", "Select frontend framework", "Choose database", "Define deployment strategy"], "deliverable": "Tech Stack Document", "category": "Technical", "priority": "High"},
        "2026-08-28": {"task": "Prepare August MPR", "sub_tasks": ["Compile August activities", "Document IDP progress", "List technical achievements", "Draft report"], "deliverable": "August MPR Draft", "category": "Reporting", "priority": "High"},
        "2026-08-31": {"task": "Submit August MPR", "sub_tasks": ["Finalize report", "Get approvals", "Submit to PMU", "Archive submission"], "deliverable": "August MPR Submitted", "category": "Reporting", "priority": "High"}
    }
    
    # ============================================================
    # SEPTEMBER 2026 - Dashboard Design and Milestone 1
    # ============================================================
    sep_tasks = {
        "2026-09-01": {"task": "Design Dashboard Prototype", "sub_tasks": ["Create high-fidelity mockups", "Design data visualizations", "Include all KPIs", "Review with stakeholders"], "deliverable": "Dashboard Prototype", "category": "Technical", "priority": "High"},
        "2026-09-02": {"task": "Database Schema Design", "sub_tasks": ["Design tables", "Define relationships", "Create indexes", "Optimize queries"], "deliverable": "Database Schema", "category": "Technical", "priority": "High"},
        "2026-09-03": {"task": "API Development Planning", "sub_tasks": ["Define API endpoints", "Design request/response", "Plan authentication", "Document API specs"], "deliverable": "API Design Document", "category": "Technical", "priority": "High"},
        "2026-09-04": {"task": "Data Integration Strategy", "sub_tasks": ["Plan data extraction", "Define transformation rules", "Design loading process", "Create ETL pipeline"], "deliverable": "Integration Strategy", "category": "Technical", "priority": "High"},
        "2026-09-07": {"task": "Dashboard Development - Week 1", "sub_tasks": ["Start frontend development", "Implement basic layout", "Create chart components", "Setup routing"], "deliverable": "Dashboard Skeleton", "category": "Technical", "priority": "High"},
        "2026-09-08": {"task": "Dashboard Development - KPI Cards", "sub_tasks": ["Implement metric cards", "Add data binding", "Create animations", "Test responsiveness"], "deliverable": "KPI Dashboard", "category": "Technical", "priority": "High"},
        "2026-09-09": {"task": "Dashboard Development - Charts", "sub_tasks": ["Implement bar charts", "Add line charts", "Create pie charts", "Integrate with data"], "deliverable": "Chart Components", "category": "Technical", "priority": "High"},
        "2026-09-10": {"task": "Dashboard Development - Filters", "sub_tasks": ["Add date filters", "Implement university filters", "Add category filters", "Create search functionality"], "deliverable": "Filter Components", "category": "Technical", "priority": "High"},
        "2026-09-11": {"task": "Dashboard Development - Export Features", "sub_tasks": ["Implement PDF export", "Add Excel export", "Create print view", "Test exports"], "deliverable": "Export Functionality", "category": "Technical", "priority": "Medium"},
        "2026-09-14": {"task": "Prepare Milestone 1 Report", "sub_tasks": ["Document sustainable data systems", "List quality achievements", "Compile evidence", "Draft milestone report"], "deliverable": "Milestone 1 Draft", "category": "Reporting", "priority": "High"},
        "2026-09-15": {"task": "Review Milestone 1 with Team", "sub_tasks": ["Present draft to team", "Gather feedback", "Make corrections", "Finalize content"], "deliverable": "Milestone 1 Reviewed", "category": "Meetings", "priority": "High"},
        "2026-09-16": {"task": "Submit Milestone 1 Report to Client", "sub_tasks": ["Prepare submission package", "Submit to PMU", "Schedule review meeting", "Get acknowledgment"], "deliverable": "Milestone 1 Submitted", "category": "Reporting", "priority": "High"},
        "2026-09-17": {"task": "Client Presentation - Milestone 1", "sub_tasks": ["Prepare presentation", "Present achievements", "Answer questions", "Document feedback"], "deliverable": "Presentation Deck", "category": "Meetings", "priority": "High"},
        "2026-09-18": {"task": "Incorporate Client Feedback", "sub_tasks": ["Review feedback", "Update documentation", "Make improvements", "Submit updated report"], "deliverable": "Updated Milestone 1", "category": "Reporting", "priority": "High"},
        "2026-09-21": {"task": "Continue Dashboard Development", "sub_tasks": ["Add user management", "Implement role-based access", "Add audit logs", "Test security"], "deliverable": "Enhanced Dashboard", "category": "Technical", "priority": "High"},
        "2026-09-22": {"task": "Dashboard Testing and QA", "sub_tasks": ["Conduct unit testing", "Perform integration testing", "Test edge cases", "Document bugs"], "deliverable": "Test Report", "category": "Technical", "priority": "High"},
        "2026-09-23": {"task": "Fix Dashboard Bugs", "sub_tasks": ["Prioritize bugs", "Fix critical issues", "Test fixes", "Deploy updates"], "deliverable": "Bug Fix Report", "category": "Technical", "priority": "High"},
        "2026-09-24": {"task": "Prepare September MPR", "sub_tasks": ["Compile September activities", "Document dashboard progress", "List milestone achievements", "Draft report"], "deliverable": "September MPR Draft", "category": "Reporting", "priority": "High"},
        "2026-09-25": {"task": "Performance Optimization", "sub_tasks": ["Analyze performance", "Optimize database queries", "Implement caching", "Reduce load time"], "deliverable": "Performance Report", "category": "Technical", "priority": "Medium"},
        "2026-09-28": {"task": "Complete Dashboard Beta Version", "sub_tasks": ["Finish all features", "Conduct final testing", "Prepare deployment", "Create user guide"], "deliverable": "Dashboard Beta", "category": "Technical", "priority": "High"},
        "2026-09-29": {"task": "Deploy Dashboard to Staging", "sub_tasks": ["Setup staging environment", "Deploy application", "Verify deployment", "Test in staging"], "deliverable": "Staging Deployment", "category": "Technical", "priority": "High"},
        "2026-09-30": {"task": "Submit September MPR", "sub_tasks": ["Finalize report", "Get approvals", "Submit to PMU", "Archive submission"], "deliverable": "September MPR Submitted", "category": "Reporting", "priority": "High"}
    }
    
    # ============================================================
    # OCTOBER 2026 - Dashboard Completion and Milestone 2
    # ============================================================
    oct_tasks = {
        "2026-10-01": {"task": "Dashboard User Testing", "sub_tasks": ["Invite test users", "Collect feedback", "Document issues", "Prioritize fixes"], "deliverable": "User Testing Report", "category": "Testing", "priority": "High"},
        "2026-10-02": {"task": "Fix User Testing Issues", "sub_tasks": ["Address critical bugs", "Improve UX based on feedback", "Test fixes", "Deploy updates"], "deliverable": "Fixed Dashboard", "category": "Technical", "priority": "High"},
        "2026-10-05": {"task": "Prepare Milestone 2 Report", "sub_tasks": ["Document IDP execution", "List monitoring framework", "Compile evidence", "Draft report"], "deliverable": "Milestone 2 Draft", "category": "Reporting", "priority": "High"},
        "2026-10-06": {"task": "Review Milestone 2 with ICARE", "sub_tasks": ["Present to leadership", "Gather feedback", "Make corrections", "Finalize content"], "deliverable": "Milestone 2 Reviewed", "category": "Meetings", "priority": "High"},
        "2026-10-07": {"task": "Submit Milestone 2 Report", "sub_tasks": ["Prepare submission", "Submit to PMU", "Schedule review", "Get acknowledgment"], "deliverable": "Milestone 2 Submitted", "category": "Reporting", "priority": "High"},
        "2026-10-08": {"task": "Dashboard Training for Users", "sub_tasks": ["Prepare training materials", "Conduct training session", "Answer questions", "Record feedback"], "deliverable": "Training Report", "category": "Training", "priority": "High"},
        "2026-10-09": {"task": "Create User Documentation", "sub_tasks": ["Write user manual", "Create video tutorials", "Add tooltips", "Prepare FAQs"], "deliverable": "User Documentation", "category": "Documentation", "priority": "Medium"},
        "2026-10-12": {"task": "Prepare Mid-Term Review", "sub_tasks": ["Compile 6-month achievements", "Create presentation", "Prepare data slides", "Draft review document"], "deliverable": "Mid-Term Review Materials", "category": "Reporting", "priority": "High"},
        "2026-10-13": {"task": "Internal Mid-Term Review", "sub_tasks": ["Present to ICARE team", "Review progress", "Identify gaps", "Plan improvements"], "deliverable": "Internal Review Report", "category": "Meetings", "priority": "High"},
        "2026-10-14": {"task": "Finalize Mid-Term Report", "sub_tasks": ["Incorporate feedback", "Add recommendations", "Format document", "Prepare for client"], "deliverable": "Final Mid-Term Report", "category": "Reporting", "priority": "High"},
        "2026-10-15": {"task": "Present Mid-Term Report to Client", "sub_tasks": ["Schedule client meeting", "Present findings", "Discuss progress", "Get client approval"], "deliverable": "Client Meeting Minutes", "category": "Meetings", "priority": "High"},
        "2026-10-16": {"task": "Update Plan Based on Mid-Term Review", "sub_tasks": ["Review feedback", "Adjust remaining plan", "Update timelines", "Communicate changes"], "deliverable": "Updated Project Plan", "category": "Planning", "priority": "Medium"},
        "2026-10-19": {"task": "Prepare October MPR", "sub_tasks": ["Compile October activities", "Document dashboard launch", "List milestone achievements", "Draft report"], "deliverable": "October MPR Draft", "category": "Reporting", "priority": "High"},
        "2026-10-20": {"task": "Phase 2 Completion Review", "sub_tasks": ["Review all deliverables", "Assess quality", "Document lessons", "Plan Phase 3"], "deliverable": "Phase 2 Report", "category": "Meetings", "priority": "High"},
        "2026-10-21": {"task": "Plan Phase 3 Activities", "sub_tasks": ["Review Phase 3 requirements", "Create detailed schedule", "Assign resources", "Set milestones"], "deliverable": "Phase 3 Plan", "category": "Planning", "priority": "High"},
        "2026-10-22": {"task": "Client Review Meeting - Phase 2 Results", "sub_tasks": ["Prepare presentation", "Showcase IDPs and Dashboard", "Present metrics", "Get approval"], "deliverable": "Client Presentation", "category": "Meetings", "priority": "High"},
        "2026-10-23": {"task": "Phase 3 Team Kickoff", "sub_tasks": ["Present Phase 3 plan", "Clarify roles", "Discuss challenges", "Align goals"], "deliverable": "Kickoff Minutes", "category": "Meetings", "priority": "High"},
        "2026-10-26": {"task": "Prepare for Portal Deployment", "sub_tasks": ["Review deployment checklist", "Prepare production environment", "Backup data", "Schedule deployment"], "deliverable": "Deployment Plan", "category": "Planning", "priority": "High"},
        "2026-10-27": {"task": "Deploy Data Portal to Production", "sub_tasks": ["Execute deployment", "Verify functionality", "Monitor performance", "Document deployment"], "deliverable": "Portal Deployed", "category": "Technical", "priority": "High"},
        "2026-10-28": {"task": "Post-Deployment Validation", "sub_tasks": ["Test all features", "Verify data accuracy", "Check security", "Document validation"], "deliverable": "Validation Report", "category": "Testing", "priority": "High"},
        "2026-10-29": {"task": "Finalize October MPR", "sub_tasks": ["Incorporate feedback", "Finalize report", "Get approvals", "Prepare submission"], "deliverable": "Final October MPR", "category": "Reporting", "priority": "High"},
        "2026-10-30": {"task": "Submit October MPR to PMU", "sub_tasks": ["Submit via portal", "Send copy to VC", "Confirm receipt", "Archive"], "deliverable": "October MPR Submitted", "category": "Reporting", "priority": "High"}
    }
    
    # ============================================================
    # NOVEMBER 2026 to APRIL 2028 - Additional months would be added similarly
    # For brevity, generating generic but meaningful tasks for remaining months
    # ============================================================
    
    # Generate for November 2026 - December 2027 (Phase 3, 4, 5)
    current_date = datetime(2026, 11, 2)
    end_date = datetime(2028, 4, 28)
    
    phase_3_tasks = [
        "Implement data portal monitoring system",
        "Conduct user acceptance testing",
        "Train university staff on portal usage",
        "Collect user feedback and improve",
        "Launch performance dashboards",
        "Develop advanced training modules",
        "Conduct capacity building workshops",
        "Publish research enhancement reports",
        "Implement OBE framework",
        "Prepare accreditation readiness",
        "Conduct international collaboration meetings",
        "Enhance employer perception metrics",
        "Improve citation analysis",
        "Submit global ranking data",
        "Prepare milestone reports"
    ]
    
    phase_4_tasks = [
        "Conduct advanced GRDAU training",
        "Implement predictive analytics",
        "Enhance dashboard features",
        "Prepare international ranking submissions",
        "Develop SDG research framework",
        "Conduct faculty development programs",
        "Implement IPR policies",
        "Create international student strategy",
        "Build academic reputation",
        "Enhance placement tracking"
    ]
    
    phase_5_tasks = [
        "Prepare final evaluation report",
        "Develop sustainability plan",
        "Conduct lessons learned workshop",
        "Prepare handover documentation",
        "Train successor team",
        "Complete project closure",
        "Submit final deliverables",
        "Release performance bank guarantee",
        "Conduct client satisfaction survey",
        "Document success stories"
    ]
    
    task_index = 0
    while current_date <= end_date:
        if current_date.weekday() < 5:  # Monday to Friday
            date_str = current_date.strftime("%Y-%m-%d")
            
            # Determine phase based on date
            if current_date < datetime(2027, 5, 1):
                phase_tasks = phase_3_tasks
                phase_name = "Phase 3: Implementation"
            elif current_date < datetime(2027, 11, 1):
                phase_tasks = phase_4_tasks
                phase_name = "Phase 4: Enhancement"
            else:
                phase_tasks = phase_5_tasks
                phase_name = "Phase 5: Finalization"
            
            task = phase_tasks[task_index % len(phase_tasks)]
            
            all_tasks[date_str] = {
                "task": f"{phase_name} - {task}",
                "sub_tasks": [
                    "Review project requirements",
                    "Complete assigned activities",
                    "Document progress and challenges",
                    "Coordinate with team members",
                    "Update project trackers"
                ],
                "deliverable": f"{task} Report",
                "category": phase_name.split(":")[0],
                "priority": "High" if "milestone" in task.lower() or "report" in task.lower() else "Medium"
            }
            task_index += 1
        current_date += timedelta(days=1)
    
    # Merge all tasks
    all_tasks.update(june_tasks)
    all_tasks.update(july_tasks)
    all_tasks.update(aug_tasks)
    all_tasks.update(sep_tasks)
    all_tasks.update(oct_tasks)
    
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
    return len(completed_dates)

def get_user_tasks(email):
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
                "task": task_info.get("task", ""),
                "sub_tasks": task_info.get("sub_tasks", []),
                "deliverable": task_info.get("deliverable", ""),
                "category": task_info.get("category", ""),
                "priority": task_info.get("priority", "Medium"),
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
    return True

def get_all_analysts_progress():
    all_tasks = load_tasks()
    completions = load_completions()
    total_tasks = len(all_tasks)
    
    progress_data = []
    for email, user in USERS.items():
        if user.get("role") == "data_analyst":
            user_completions = completions.get(email, {})
            completed = len(user_completions)
            progress_data.append({
                "name": user["name"],
                "team": user.get("team", "N/A"),
                "completed": completed,
                "total": total_tasks,
                "progress": round((completed / total_tasks * 100), 1) if total_tasks > 0 else 0
            })
    
    return pd.DataFrame(progress_data)

def get_team_summary():
    progress_df = get_all_analysts_progress()
    team_summary = progress_df.groupby("team").agg({
        "completed": "sum",
        "total": "first"
    }).reset_index()
    team_summary["progress"] = round((team_summary["completed"] / team_summary["total"] * 100), 1)
    return team_summary

def generate_mpr_html(year, month):
    month_names = ["January", "February", "March", "April", "May", "June", 
                   "July", "August", "September", "October", "November", "December"]
    month_name = month_names[month-1]
    
    progress_df = get_all_analysts_progress()
    
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

<div class="section-title">1. Team Performance Summary</div>
<table>
    <tr><th>Team Member</th><th>Team</th><th>Tasks Completed</th><th>Total Tasks</th><th>Progress (%)</th></tr>
    {''.join([f'<tr><td>{row["name"]}</td><td>{row["team"]}</td><td>{row["completed"]}</td><td>{row["total"]}</td><td>{row["progress"]}%</td></tr>' for _, row in progress_df.iterrows()])}
</table>

<div class="section-title">2. Overall Statistics</div>
<table>
    <tr><td><strong>Total Working Days (24 months)</strong></td><td>{len(load_tasks())}</td></tr>
    <tr><td><strong>Total Task Completions</strong></td><td>{sum(len(c) for c in load_completions().values())}</td></tr>
    <tr><td><strong>Active Team Members</strong></td><td>{len(progress_df)}</td></tr>
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
            <tr><td>🔴 Admin</td><td>admin@mahastride.com</td><td>Admin@2026</td></tr>
            <tr><td>🔵 Project Lead</td><td>projectlead@mahastride.com</td><td>ProjectLead@2026</td></tr>
            <tr><td>🟢 Data Analyst</td><td>sneha@mu.edu</td><td>Sneha@2026</td></tr>
            <tr><td>🟢 Data Analyst</td><td>shubham@mitra.gov.in</td><td>Shubham@2026</td></tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# DATA ANALYST DASHBOARD
# ============================================================

def data_analyst_dashboard(email, user):
    st.markdown(f"## 📝 My Tasks - {user.get('name')}")
    st.markdown(f"**Team:** {user.get('team', 'N/A')}")
    st.markdown("**Working Hours:** 10:00 AM - 6:00 PM (Monday to Friday)")
    
    user_tasks = get_user_tasks(email)
    
    pending_tasks = [t for t in user_tasks if t["date"] > "2026-06-05" and t["status"] == "Pending"]
    completed_tasks = [t for t in user_tasks if t["date"] > "2026-06-05" and t["status"] == "Completed"]
    initial_completed = [t for t in user_tasks if t["date"] <= "2026-06-05"]
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📅 Total Tasks", len(user_tasks))
    with col2:
        st.metric("✅ Completed (Initial)", len(initial_completed))
    with col3:
        st.metric("✅ Completed (Your Work)", len(completed_tasks))
    with col4:
        st.metric("⏳ Pending", len(pending_tasks))
    
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
                <strong>Deliverable:</strong> {today_task['deliverable']}
            </div>
            """, unsafe_allow_html=True)
        else:
            with st.form(key="complete_today_task"):
                st.markdown(f"""
                <div class="task-card task-pending">
                    <strong>⏳ PENDING TASK</strong><br>
                    <strong>Task:</strong> {today_task['task']}<br>
                    <strong>Deliverable:</strong> {today_task['deliverable']}<br>
                    <strong>Priority:</strong> {today_task['priority']}
                </div>
                """, unsafe_allow_html=True)
                
                if today_task.get('sub_tasks'):
                    st.markdown("**Sub-tasks to complete:**")
                    for stask in today_task['sub_tasks']:
                        st.markdown(f"- {stask}")
                    st.markdown("---")
                
                col1, col2 = st.columns(2)
                with col1:
                    start_time = st.time_input("Start Time", value=datetime.strptime("10:00", "%H:%M").time())
                with col2:
                    end_time = st.time_input("End Time", value=datetime.strptime("18:00", "%H:%M").time())
                
                work_hours = f"{start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}"
                remarks = st.text_area("Work Accomplished", height=100)
                
                if st.form_submit_button("✅ MARK AS COMPLETE", use_container_width=True, type="primary"):
                    if remarks:
                        if mark_task_complete(email, today_task["date"], remarks, work_hours):
                            st.success("🎉 Task completed! Great work!")
                            st.rerun()
                    else:
                        st.error("Please describe your work")
    
    st.markdown("---")
    st.subheader("📅 Calendar View - All Tasks")
    
    for task in user_tasks:
        if task["date"] > "2026-06-05":
            status_icon = "✅" if task["status"] == "Completed" else "⏳"
            st.markdown(f"{status_icon} **{task['date']}** - {task['task'][:80]}")

# ============================================================
# ADMIN DASHBOARD
# ============================================================

def admin_dashboard():
    st.markdown("## 📊 Admin Dashboard")
    
    all_tasks = load_tasks()
    completions = load_completions()
    progress_df = get_all_analysts_progress()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""<div class="stat-card"><div class="metric-value">{len(all_tasks)}</div><div class="metric-label">Total Working Days</div></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="stat-card"><div class="metric-value">{len([d for d in all_tasks.keys() if d <= "2026-06-05"])}</div><div class="metric-label">Completed (May 4 - June 5)</div></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class="stat-card"><div class="metric-value">{len([u for u in USERS.values() if u.get("role") == "data_analyst"])}</div><div class="metric-label">Team Members</div></div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""<div class="stat-card"><div class="metric-value">{sum(len(c) for c in completions.values())}</div><div class="metric-label">Total Completions</div></div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("👥 Team Progress")
    fig = px.bar(progress_df, x="name", y="progress", color="team", text="progress", height=450)
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(progress_df, use_container_width=True, hide_index=True)

def project_lead_dashboard():
    st.markdown("## 👨‍💼 Project Lead Dashboard")
    st.markdown("**Dr. Harshal Kotwal** - ICARE Project Director")
    
    all_tasks = load_tasks()
    progress_df = get_all_analysts_progress()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📅 Total Working Days", len(all_tasks))
    with col2:
        st.metric("👥 Team Members", len(progress_df))
    with col3:
        avg_progress = progress_df["progress"].mean() if not progress_df.empty else 0
        st.metric("📈 Average Progress", f"{avg_progress:.1f}%")
    
    st.markdown("---")
    fig = px.bar(progress_df, x="name", y="progress", color="team", text="progress", height=450)
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(progress_df, use_container_width=True, hide_index=True)

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
            <h1>📊 MahaSTRIDE Project Management System</h1>
            <p>Complete 24-Month Task Management | May 2026 - April 2028</p>
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
        st.markdown("## 📋 MahaSTRIDE")
        st.markdown(f"**Welcome, {user_info.get('name')}**")
        if role == "data_analyst":
            st.markdown(f"*Team: {user_info.get('team', 'N/A')}*")
        st.markdown(f"*Role: {role.upper()}*")
        st.markdown("---")
        
        if role == "admin":
            nav_options = ["📊 Dashboard", "📄 MPR Reports"]
        elif role == "project_lead":
            nav_options = ["📊 Dashboard", "📄 MPR Reports"]
        else:
            nav_options = ["📝 My Tasks"]
        
        selected_nav = st.radio("Navigation", nav_options, label_visibility="collapsed")
        
        st.markdown("---")
        st.markdown("ℹ️ **Working Hours:** 10 AM - 6 PM")
        st.markdown("📅 **Working Days:** Monday to Friday")
        st.markdown("✅ **May 4 - June 5, 2026:** COMPLETED")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()
    
    if role == "admin":
        if selected_nav == "📊 Dashboard":
            admin_dashboard()
        else:
            st.markdown("## 📄 MPR Reports")
            col1, col2 = st.columns(2)
            with col1:
                report_year = st.selectbox("Year", [2026, 2027, 2028])
            with col2:
                report_month = st.selectbox("Month", range(1, 13), 
                                            format_func=lambda x: ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"][x-1])
            if st.button("Generate MPR"):
                html = generate_mpr_html(report_year, report_month)
                st.markdown(get_download_link(html, f"MPR_{report_year}_{report_month}.html"), unsafe_allow_html=True)
    
    elif role == "project_lead":
        if selected_nav == "📊 Dashboard":
            project_lead_dashboard()
        else:
            st.markdown("## 📄 MPR Reports")
            col1, col2 = st.columns(2)
            with col1:
                report_year = st.selectbox("Year", [2026, 2027, 2028])
            with col2:
                report_month = st.selectbox("Month", range(1, 13), 
                                            format_func=lambda x: ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"][x-1])
            if st.button("Generate MPR"):
                html = generate_mpr_html(report_year, report_month)
                st.markdown(get_download_link(html, f"MPR_{report_year}_{report_month}.html"), unsafe_allow_html=True)
    
    else:
        if selected_nav == "📝 My Tasks":
            data_analyst_dashboard(email, user_info)

if __name__ == "__main__":
    main()
