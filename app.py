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
    page_title="MahaSTRIDE - Complete Task Management System",
    page_icon="📋",
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
</style>
""", unsafe_allow_html=True)

# ============================================================
# USER CREDENTIALS
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
    "sneha@mu.edu": {
        "password": sha256("Sneha@2026".encode()).hexdigest(),
        "role": "data_analyst",
        "name": "Sneha Kashitkar",
        "team": "Mumbai University"
    },
    "shubham@mitra.gov.in": {
        "password": sha256("Shubham@2026".encode()).hexdigest(),
        "role": "data_analyst",
        "name": "Shubham Singh",
        "team": "MITRA"
    }
}

# ============================================================
# DATA FILES
# ============================================================
DAILY_TASKS_FILE = "complete_daily_tasks.json"
TASK_COMPLETION_FILE = "task_completion.json"

# ============================================================
# COMPLETE 24-MONTH UNIQUE TASKS DATABASE
# ============================================================

def get_all_unique_tasks():
    """Return a dictionary with unique tasks for every working day"""
    
    all_tasks = {}
    
    # ============================================================
    # JUNE 2026 - Week by week detailed tasks
    # ============================================================
    
    # Week 1: June 1-5 (Already completed - included for reference)
    june_week1 = {
        "2026-06-02": "Design Diagnostic Assessment framework and methodology",
        "2026-06-03": "Create assessment rubrics for NIRF parameters",
        "2026-06-04": "Prepare university-wise data collection templates",
        "2026-06-05": "Finalize assessment tools and get PMU approval"
    }
    
    # Week 2: June 8-12
    june_week2 = {
        "2026-06-08": "Conduct kickoff meeting with Mumbai University VC and IQAC team",
        "2026-06-09": "Interview 10 faculty members at Mumbai University for research assessment",
        "2026-06-10": "Collect and verify student enrollment data from all departments",
        "2026-06-11": "Document faculty publication records for last 5 years",
        "2026-06-12": "Compile research grants and project funding data"
    }
    
    # Week 3: June 15-19
    june_week3 = {
        "2026-06-15": "Analyze placement data and graduate outcomes for last 3 years",
        "2026-06-16": "Review library resources and digital infrastructure across campuses",
        "2026-06-17": "Assess laboratory facilities and research equipment availability",
        "2026-06-18": "Evaluate international collaboration MoUs and joint research projects",
        "2026-06-19": "Prepare data gap analysis report for all 7 universities"
    }
    
    # Week 4: June 22-26
    june_week4 = {
        "2026-06-22": "Constitute GRDAU team with nominated members from each department",
        "2026-06-23": "Develop standard operating procedures for GRDAU operations",
        "2026-06-24": "Train GRDAU staff on NIRF data collection and validation",
        "2026-06-25": "Setup data management system with access controls for GRDAU",
        "2026-06-26": "Review diagnostic assessment findings with university leadership"
    }
    
    # Week 5: June 29-30
    june_week5 = {
        "2026-06-29": "Finalize diagnostic reports for submission to PMU",
        "2026-06-30": "Submit June Monthly Progress Report with all achievements"
    }
    
    # ============================================================
    # JULY 2026 - Gap Analysis and GRDAU Operationalization
    # ============================================================
    july_tasks = {
        "2026-07-01": "Complete comprehensive gap analysis against NIRF 2026 parameters",
        "2026-07-02": "Prepare SWOT analysis report for Mumbai University",
        "2026-07-03": "Prepare SWOT analysis report for Pune University",
        "2026-07-06": "Prepare SWOT analysis report for Nagpur University",
        "2026-07-07": "Prepare SWOT analysis report for Amravati University",
        "2026-07-08": "Prepare SWOT analysis report for COEP University",
        "2026-07-09": "Prepare SWOT analysis report for Jalgaon University",
        "2026-07-10": "Prepare SWOT analysis report for Aurangabad University",
        "2026-07-13": "Finalize GRDAU establishment plan and submit for approval",
        "2026-07-14": "Setup GRDAU office with required hardware and software",
        "2026-07-15": "Conduct data entry training for newly appointed GRDAU staff",
        "2026-07-16": "Create data validation protocols and quality checklists",
        "2026-07-17": "Develop dashboard requirements document with stakeholder inputs",
        "2026-07-20": "Design baseline report template for Phase 1 completion",
        "2026-07-21": "Compile all Phase 1 deliverables and prepare completion report",
        "2026-07-22": "Present Phase 1 findings to MITRA steering committee",
        "2026-07-23": "Document lessons learned and best practices from Phase 1",
        "2026-07-24": "Plan Phase 2 activities with detailed work breakdown structure",
        "2026-07-27": "Prepare July Monthly Progress Report with Phase 1 summary",
        "2026-07-28": "Submit July MPR and Phase 1 completion report to PMU",
        "2026-07-29": "Review and incorporate client feedback on Phase 1 deliverables",
        "2026-07-30": "Finalize Phase 2 work plan and resource allocation",
        "2026-07-31": "Conduct Phase 2 kickoff meeting with all university coordinators"
    }
    
    # ============================================================
    # AUGUST 2026 - IDP Development for All Universities
    # ============================================================
    aug_tasks = {
        "2026-08-03": "Develop IDP framework template aligned with NIRF metrics",
        "2026-08-04": "Collect strategic plans and vision documents from Mumbai University",
        "2026-08-05": "Collect strategic plans from Pune University leadership",
        "2026-08-06": "Collect strategic plans from Nagpur University administration",
        "2026-08-07": "Collect strategic plans from Amravati University",
        "2026-08-10": "Collect strategic plans from COEP University",
        "2026-08-11": "Collect strategic plans from Jalgaon University",
        "2026-08-12": "Collect strategic plans from Aurangabad University",
        "2026-08-13": "Analyze collected strategic plans and identify common themes",
        "2026-08-14": "Draft Institutional Development Plan for Mumbai University",
        "2026-08-17": "Draft IDP for Pune University with specific KPIs",
        "2026-08-18": "Draft IDP for Nagpur University focusing on research excellence",
        "2026-08-19": "Draft IDP for Amravati University with timeline",
        "2026-08-20": "Draft IDP for COEP University emphasizing industry connect",
        "2026-08-21": "Draft IDP for Jalgaon University with internationalization goals",
        "2026-08-24": "Draft IDP for Aurangabad University focusing on infrastructure",
        "2026-08-25": "Present IDP drafts to respective Vice Chancellors for feedback",
        "2026-08-26": "Incorporate VC feedback and finalize IDPs for all universities",
        "2026-08-27": "Get formal institutional sign-off on approved IDPs",
        "2026-08-28": "Prepare August MPR documenting IDP development progress",
        "2026-08-31": "Submit August MPR to PMU with IDP status report"
    }
    
    # ============================================================
    # SEPTEMBER 2026 - Dashboard Design and Development
    # ============================================================
    sep_tasks = {
        "2026-09-01": "Design data portal architecture and database schema",
        "2026-09-02": "Create high-fidelity dashboard wireframes and mockups",
        "2026-09-03": "Setup development environment and version control system",
        "2026-09-04": "Develop backend APIs for data integration",
        "2026-09-07": "Implement user authentication and role-based access control",
        "2026-09-08": "Build KPI dashboard with metric cards for NIRF parameters",
        "2026-09-09": "Integrate research output visualization charts",
        "2026-09-10": "Add faculty-student ratio analytics dashboard",
        "2026-09-11": "Implement financial resource utilization tracking",
        "2026-09-14": "Develop placement and graduate outcomes dashboard",
        "2026-09-15": "Create international collaboration metrics visualization",
        "2026-09-16": "Add citation analysis and publication impact charts",
        "2026-09-17": "Implement infrastructure assessment dashboard",
        "2026-09-18": "Prepare Milestone 1 Report: Sustainable Data Systems",
        "2026-09-21": "Submit Milestone 1 Report to PMU for review",
        "2026-09-22": "Present Milestone 1 achievements to client",
        "2026-09-23": "Incorporate client feedback into dashboard design",
        "2026-09-24": "Conduct user acceptance testing with university coordinators",
        "2026-09-25": "Fix bugs and optimize dashboard performance",
        "2026-09-28": "Deploy dashboard beta version to staging server",
        "2026-09-29": "Prepare September MPR with dashboard development status",
        "2026-09-30": "Submit September MPR to PMU"
    }
    
    # ============================================================
    # OCTOBER 2026 - Milestone 2 and Mid-Term Review
    # ============================================================
    oct_tasks = {
        "2026-10-01": "Complete dashboard beta testing with all universities",
        "2026-10-02": "Finalize dashboard based on user feedback",
        "2026-10-05": "Prepare Milestone 2 Report: IDP Execution Monitoring",
        "2026-10-06": "Submit Milestone 2 Report to PMU with evidence",
        "2026-10-07": "Present IDP monitoring framework to client",
        "2026-10-08": "Conduct dashboard training for university administrators",
        "2026-10-09": "Create comprehensive user manual and video tutorials",
        "2026-10-12": "Compile 6-month achievements for Mid-Term Review",
        "2026-10-13": "Prepare Mid-Term Review presentation for MITRA",
        "2026-10-14": "Conduct internal review with ICARE leadership",
        "2026-10-15": "Present Mid-Term Report to World Bank and MITRA",
        "2026-10-16": "Incorporate mid-term feedback into project plan",
        "2026-10-19": "Prepare October MPR with milestone achievements",
        "2026-10-20": "Deploy data portal to production environment",
        "2026-10-21": "Monitor portal performance and fix issues",
        "2026-10-22": "Setup analytics tracking for portal usage",
        "2026-10-23": "Create backup and disaster recovery procedures",
        "2026-10-26": "Plan Phase 3 implementation activities",
        "2026-10-27": "Develop detailed Phase 3 work schedule",
        "2026-10-28": "Assign Phase 3 responsibilities to team members",
        "2026-10-29": "Conduct Phase 3 team coordination meeting",
        "2026-10-30": "Submit October MPR to PMU"
    }
    
    # ============================================================
    # NOVEMBER 2026 - Portal Deployment and Training
    # ============================================================
    nov_tasks = {
        "2026-11-02": "Deploy data portal MVP with core features",
        "2026-11-03": "Conduct portal training for GRDAU coordinators",
        "2026-11-04": "Upload baseline data for all 7 universities",
        "2026-11-05": "Verify data accuracy in portal with source documents",
        "2026-11-06": "Collect user feedback on portal usability",
        "2026-11-09": "Implement priority fixes based on user feedback",
        "2026-11-10": "Add data export functionality to portal",
        "2026-11-11": "Setup automated data validation rules",
        "2026-11-12": "Create custom reports generation feature",
        "2026-11-13": "Train university staff on report generation",
        "2026-11-16": "Develop training module for NIRF data submission",
        "2026-11-17": "Conduct research metrics analysis workshop",
        "2026-11-18": "Provide citation analysis training to faculty",
        "2026-11-19": "Prepare training needs assessment report",
        "2026-11-20": "Schedule capacity building programs for all universities",
        "2026-11-23": "Conduct online training for remote coordinators",
        "2026-11-24": "Prepare training materials and handouts",
        "2026-11-25": "Assess training effectiveness with feedback forms",
        "2026-11-26": "Plan advanced training modules for Phase 3",
        "2026-11-27": "Prepare November MPR with training status",
        "2026-11-30": "Submit November MPR to PMU"
    }
    
    # ============================================================
    # DECEMBER 2026 - Milestone 3 and Year-End Review
    # ============================================================
    dec_tasks = {
        "2026-12-01": "Complete first round of training programs",
        "2026-12-02": "Analyze training feedback and effectiveness",
        "2026-12-03": "Prepare training completion report",
        "2026-12-04": "Launch performance dashboards to all users",
        "2026-12-07": "Develop advanced training modules for GRDAU staff",
        "2026-12-08": "Conduct hands-on data analytics workshop",
        "2026-12-09": "Provide one-on-one coaching for coordinators",
        "2026-12-10": "Create certification program for GRDAU staff",
        "2026-12-11": "Prepare Milestone 3 Report: Capacity Building",
        "2026-12-14": "Submit Milestone 3 Report with evidence",
        "2026-12-15": "Present capacity building achievements to client",
        "2026-12-16": "Compile year-end performance data",
        "2026-12-17": "Prepare annual report for 2026",
        "2026-12-18": "Review project progress against annual targets",
        "2026-12-21": "Plan 2027 activities and resource requirements",
        "2026-12-22": "Conduct team performance appraisal",
        "2026-12-23": "Document success stories and case studies",
        "2026-12-24": "Prepare December MPR with annual summary",
        "2026-12-28": "Submit December MPR and annual report",
        "2026-12-29": "Conduct client year-end review meeting",
        "2026-12-30": "Plan for Phase 3 enhancement activities",
        "2026-12-31": "Celebrate project achievements with team"
    }
    
    # ============================================================
    # JANUARY 2027 - Data Quality and Research Enhancement
    # ============================================================
    jan_tasks = {
        "2027-01-04": "Implement automated data quality checks in portal",
        "2027-01-05": "Conduct data audit for all 7 universities",
        "2027-01-06": "Clean and standardize research publication data",
        "2027-01-07": "Validate faculty credentials and qualifications",
        "2027-01-08": "Cross-verify student enrollment data",
        "2027-01-11": "Identify and correct data inconsistencies",
        "2027-01-12": "Create data quality scorecard for each university",
        "2027-01-13": "Prepare data quality improvement plan",
        "2027-01-14": "Implement research output tracking system",
        "2027-01-15": "Analyze publication trends and patterns",
        "2027-01-18": "Identify high-impact research areas",
        "2027-01-19": "Develop research enhancement strategy",
        "2027-01-20": "Create faculty research profiles",
        "2027-01-21": "Setup citation tracking mechanism",
        "2027-01-22": "Prepare research enhancement plan document",
        "2027-01-25": "Conduct research writing workshop for faculty",
        "2027-01-26": "Provide grant proposal writing training",
        "2027-01-27": "Establish research collaboration framework",
        "2027-01-28": "Prepare January MPR with research progress",
        "2027-01-29": "Submit January MPR to PMU"
    }
    
    # ============================================================
    # FEBRUARY 2027 - International Collaboration and OBE
    # ============================================================
    feb_tasks = {
        "2027-02-01": "Review existing international MoUs and collaborations",
        "2027-02-02": "Identify potential international partners for collaboration",
        "2027-02-03": "Develop internationalization strategy document",
        "2027-02-04": "Create MoU template for new partnerships",
        "2027-02-05": "Initiate discussions with foreign universities",
        "2027-02-08": "Develop Outcome-Based Education framework",
        "2027-02-09": "Create OBE implementation guidelines",
        "2027-02-10": "Train faculty on OBE curriculum design",
        "2027-02-11": "Develop program outcomes and course outcomes",
        "2027-02-12": "Create assessment rubrics for OBE",
        "2027-02-15": "Implement OBE tracking dashboard",
        "2027-02-16": "Conduct OBE readiness assessment",
        "2027-02-17": "Prepare OBE implementation report",
        "2027-02-18": "Plan international faculty exchange program",
        "2027-02-19": "Create student exchange program framework",
        "2027-02-22": "Develop international admission process",
        "2027-02-23": "Prepare international student support system",
        "2027-02-24": "Conduct international webinar series",
        "2027-02-25": "Prepare February MPR with OBE progress",
        "2027-02-26": "Submit February MPR to PMU"
    }
    
    # ============================================================
    # MARCH 2027 - Accreditation and Quality Assurance
    # ============================================================
    mar_tasks = {
        "2027-03-01": "Conduct NAAC accreditation readiness assessment",
        "2027-03-02": "Review NBA accreditation criteria for programs",
        "2027-03-03": "Identify gaps for accreditation requirements",
        "2027-03-04": "Prepare accreditation action plan",
        "2027-03-05": "Create accreditation documentation template",
        "2027-03-08": "Train IQAC on accreditation process",
        "2027-03-09": "Develop quality assurance framework",
        "2027-03-10": "Create internal audit checklist",
        "2027-03-11": "Conduct mock accreditation visit",
        "2027-03-12": "Prepare quality improvement plan",
        "2027-03-15": "Implement QA dashboard for monitoring",
        "2027-03-16": "Develop student feedback system",
        "2027-03-17": "Create faculty evaluation framework",
        "2027-03-18": "Implement continuous quality improvement cycle",
        "2027-03-19": "Prepare QA implementation report",
        "2027-03-22": "Conduct stakeholder satisfaction survey",
        "2027-03-23": "Analyze survey results and identify improvements",
        "2027-03-24": "Prepare March MPR with QA progress",
        "2027-03-25": "Submit March MPR to PMU",
        "2027-03-26": "Plan Phase 4 enhancement activities"
    }
    
    # ============================================================
    # APRIL 2027 - Milestone 4 (10% Improvement)
    # ============================================================
    apr_tasks = {
        "2027-04-01": "Collect performance data for first 6 months",
        "2027-04-02": "Calculate improvement percentages for all indicators",
        "2027-04-05": "Analyze research output increase metrics",
        "2027-04-06": "Measure placement rate improvement",
        "2027-04-07": "Calculate faculty-student ratio enhancement",
        "2027-04-08": "Measure international collaboration growth",
        "2027-04-09": "Prepare Milestone 4 Report: 10% Improvement",
        "2027-04-12": "Compile evidence documents for improvement",
        "2027-04-13": "Submit Milestone 4 Report to PMU",
        "2027-04-14": "Present improvement achievements to client",
        "2027-04-15": "Prepare Year 1 Annual Performance Report",
        "2027-04-16": "Compile annual achievements and metrics",
        "2027-04-19": "Create annual report presentation",
        "2027-04-20": "Present Year 1 results to MITRA board",
        "2027-04-21": "Plan Year 2 enhancement activities",
        "2027-04-22": "Conduct team annual performance review",
        "2027-04-23": "Prepare April MPR with annual summary",
        "2027-04-26": "Submit April MPR and Annual Report",
        "2027-04-27": "Conduct client annual review meeting",
        "2027-04-28": "Finalize Year 2 work plan and budget",
        "2027-04-29": "Celebrate Year 1 achievements with team",
        "2027-04-30": "Plan Phase 4 kickoff activities"
    }
    
    # ============================================================
    # MAY 2027 - Year 2 Kickoff and Advanced Analytics
    # ============================================================
    may_tasks = {
        "2027-05-03": "Conduct Year 2 kickoff meeting with all stakeholders",
        "2027-05-04": "Present Year 2 goals and targets to team",
        "2027-05-05": "Setup Year 2 tracking dashboards",
        "2027-05-06": "Implement advanced analytics features",
        "2027-05-07": "Add predictive analytics for performance trends",
        "2027-05-10": "Develop machine learning models for ranking prediction",
        "2027-05-11": "Create benchmarking tool against top universities",
        "2027-05-12": "Implement real-time data synchronization",
        "2027-05-13": "Add mobile-responsive dashboard views",
        "2027-05-14": "Enhance data visualization with interactive charts",
        "2027-05-17": "Implement automated report generation",
        "2027-05-18": "Add email notification system for alerts",
        "2027-05-19": "Create custom dashboard for leadership",
        "2027-05-20": "Implement role-based dashboard views",
        "2027-05-23": "Add comparative analysis across universities",
        "2027-05-24": "Implement year-on-year trend analysis",
        "2027-05-25": "Create what-if scenario planning tool",
        "2027-05-26": "Add budget vs actual tracking",
        "2027-05-27": "Prepare May MPR with Year 2 progress",
        "2027-05-28": "Submit May MPR to PMU"
    }
    
    # ============================================================
    # JUNE 2027 - Global Ranking Preparation
    # ============================================================
    jun_tasks = {
        "2027-06-01": "Review QS World University Ranking methodology",
        "2027-06-02": "Collect data for QS ranking indicators",
        "2027-06-03": "Prepare academic reputation survey responses",
        "2027-06-04": "Compile employer reputation data",
        "2027-06-07": "Collect faculty-student ratio data for QS",
        "2027-06-08": "Gather international faculty statistics",
        "2027-06-09": "Compile international student data",
        "2027-06-10": "Prepare citations per faculty metrics",
        "2027-06-11": "Complete QS ranking submission forms",
        "2027-06-14": "Review THE World University Ranking criteria",
        "2027-06-15": "Collect teaching quality indicators",
        "2027-06-16": "Gather research influence metrics",
        "2027-06-17": "Compile industry income data",
        "2027-06-18": "Prepare international outlook statistics",
        "2027-06-21": "Complete THE ranking submission",
        "2027-06-22": "Review US News Best Global Universities criteria",
        "2027-06-23": "Collect regional research reputation data",
        "2027-06-24": "Compile publications and conferences data",
        "2027-06-25": "Prepare normalized citation impact",
        "2027-06-28": "Complete US News ranking submission",
        "2027-06-29": "Prepare June MPR with ranking status",
        "2027-06-30": "Submit June MPR to PMU"
    }
    
    # ============================================================
    # JULY 2027 - Advanced Training and Research Support
    # ============================================================
    jul_tasks = {
        "2027-07-01": "Conduct advanced data analytics training for GRDAU",
        "2027-07-02": "Provide Python for data science workshop",
        "2027-07-05": "Conduct R programming for research analytics",
        "2027-07-06": "Offer SQL for data management training",
        "2027-07-07": "Provide Tableau dashboard creation workshop",
        "2027-07-08": "Conduct research methodology advanced course",
        "2027-07-09": "Offer systematic literature review training",
        "2027-07-12": "Provide research paper writing workshop",
        "2027-07-13": "Conduct journal selection and submission training",
        "2027-07-14": "Offer peer review process training",
        "2027-07-15": "Provide research ethics and integrity workshop",
        "2027-07-16": "Conduct grant proposal writing advanced course",
        "2027-07-19": "Offer project management for researchers training",
        "2027-07-20": "Provide IPR and patent filing workshop",
        "2027-07-21": "Conduct technology transfer training",
        "2027-07-22": "Offer startup incubation support training",
        "2027-07-23": "Provide industry collaboration workshop",
        "2027-07-26": "Conduct consulting skills for faculty training",
        "2027-07-27": "Offer leadership development program",
        "2027-07-28": "Prepare July MPR with training summary",
        "2027-07-29": "Submit July MPR to PMU",
        "2027-07-30": "Plan August enhancement activities"
    }
    
    # ============================================================
    # AUGUST 2027 - Employer Perception and Industry Connect
    # ============================================================
    aug_tasks = {
        "2027-08-02": "Develop employer perception survey questionnaire",
        "2027-08-03": "Identify top employers for survey",
        "2027-08-04": "Conduct employer perception survey",
        "2027-08-05": "Analyze survey responses and feedback",
        "2027-08-06": "Prepare employer perception improvement plan",
        "2027-08-09": "Establish industry advisory board",
        "2027-08-10": "Conduct industry-academia meet",
        "2027-08-11": "Develop internship programs with industries",
        "2027-08-12": "Create placement enhancement strategy",
        "2027-08-13": "Organize campus recruitment drive",
        "2027-08-16": "Develop alumni engagement program",
        "2027-08-17": "Create corporate training programs",
        "2027-08-18": "Establish research consultancy cell",
        "2027-08-19": "Develop continuing education programs",
        "2027-08-20": "Create executive education offerings",
        "2027-08-23": "Build industry-sponsored labs",
        "2027-08-24": "Develop entrepreneurship cell",
        "2027-08-25": "Create startup incubation center",
        "2027-08-26": "Prepare August MPR with industry connect",
        "2027-08-27": "Submit August MPR to PMU",
        "2027-08-30": "Plan September ranking activities",
        "2027-08-31": "Coordinate with ranking agencies"
    }
    
    # ============================================================
    # SEPTEMBER 2027 - Milestone 5 (20% Improvement)
    # ============================================================
    sep_tasks_2027 = {
        "2027-09-01": "Collect performance data for Year 1",
        "2027-09-02": "Calculate 20% improvement metrics",
        "2027-09-03": "Analyze research output growth",
        "2027-09-06": "Measure citation impact increase",
        "2027-09-07": "Calculate placement rate improvement",
        "2027-09-08": "Measure international collaboration growth",
        "2027-09-09": "Calculate faculty quality enhancement",
        "2027-09-10": "Measure infrastructure improvement",
        "2027-09-13": "Prepare Milestone 5 Report: 20% Improvement",
        "2027-09-14": "Compile evidence documents for improvement",
        "2027-09-15": "Submit Milestone 5 Report to PMU",
        "2027-09-16": "Present 20% improvement achievements",
        "2027-09-17": "Prepare success stories documentation",
        "2027-09-20": "Create case studies of improvement",
        "2027-09-21": "Develop best practices guide",
        "2027-09-22": "Prepare knowledge sharing session",
        "2027-09-23": "Conduct webinar on success factors",
        "2027-09-24": "Prepare September MPR with milestone",
        "2027-09-27": "Submit September MPR to PMU",
        "2027-09-28": "Plan Phase 5 finalization activities",
        "2027-09-29": "Review project status against targets",
        "2027-09-30": "Team meeting for final phase planning"
    }
    
    # ============================================================
    # OCTOBER 2027 - Academic Reputation Building
    # ============================================================
    oct_tasks_2027 = {
        "2027-10-01": "Develop academic reputation enhancement strategy",
        "2027-10-04": "Organize international conference at university",
        "2027-10-05": "Invite Nobel laureates for guest lectures",
        "2027-10-06": "Conduct faculty development programs",
        "2027-10-07": "Publish research in high-impact journals",
        "2027-10-08": "Create university research magazine",
        "2027-10-11": "Establish distinguished visitor program",
        "2027-10-12": "Develop online course offerings",
        "2027-10-13": "Create MOOC courses on SWAYAM",
        "2027-10-14": "Launch university podcast series",
        "2027-10-15": "Develop social media presence strategy",
        "2027-10-18": "Create alumni achievement recognition program",
        "2027-10-19": "Organize alumni meet and networking",
        "2027-10-20": "Develop brand ambassador program",
        "2027-10-21": "Create university ranking improvement campaign",
        "2027-10-22": "Prepare October MPR with reputation activities",
        "2027-10-25": "Submit October MPR to PMU",
        "2027-10-26": "Plan final evaluation activities",
        "2027-10-27": "Review sustainability requirements",
        "2027-10-28": "Prepare handover documentation template",
        "2027-10-29": "Conduct team meeting for final phase"
    }
    
    # ============================================================
    # NOVEMBER 2027 - Final Ranking Submissions
    # ============================================================
    nov_tasks_2027 = {
        "2027-11-01": "Review final ranking submission requirements",
        "2027-11-02": "Collect updated data for QS ranking",
        "2027-11-03": "Verify all QS ranking metrics",
        "2027-11-04": "Prepare QS final submission package",
        "2027-11-05": "Submit QS ranking final data",
        "2027-11-08": "Collect updated data for THE ranking",
        "2027-11-09": "Verify THE ranking metrics",
        "2027-11-10": "Prepare THE final submission",
        "2027-11-11": "Submit THE ranking data",
        "2027-11-12": "Collect updated data for US News",
        "2027-11-15": "Verify US News ranking metrics",
        "2027-11-16": "Prepare US News final submission",
        "2027-11-17": "Submit US News ranking data",
        "2027-11-18": "Prepare Milestone 6 Report: Global Rankings",
        "2027-11-19": "Compile evidence of ranking participation",
        "2027-11-22": "Submit Milestone 6 Report to PMU",
        "2027-11-23": "Present global ranking achievements",
        "2027-11-24": "Prepare November MPR with ranking status",
        "2027-11-25": "Submit November MPR to PMU",
        "2027-11-26": "Plan sustainability framework"
    }
    
    # ============================================================
    # DECEMBER 2027 - Sustainability Planning
    # ============================================================
    dec_tasks_2027 = {
        "2027-12-01": "Develop sustainability framework for GRDAU",
        "2027-12-02": "Create GRDAU operational sustainability plan",
        "2027-12-03": "Develop dashboard maintenance plan",
        "2027-12-06": "Create data update and validation schedule",
        "2027-12-07": "Develop training sustainability program",
        "2027-12-08": "Create knowledge transfer plan",
        "2027-12-09": "Develop handover documentation",
        "2027-12-10": "Prepare system administration guide",
        "2027-12-13": "Create user training manual",
        "2027-12-14": "Develop troubleshooting guide",
        "2027-12-15": "Prepare disaster recovery plan",
        "2027-12-16": "Create backup and archival strategy",
        "2027-12-17": "Develop performance monitoring plan",
        "2027-12-20": "Create quality assurance checklist",
        "2027-12-21": "Prepare sustainability report",
        "2027-12-22": "Conduct sustainability workshop",
        "2027-12-23": "Train successor team on operations",
        "2027-12-27": "Prepare December MPR with sustainability",
        "2027-12-28": "Submit December MPR to PMU",
        "2027-12-29": "Plan final evaluation activities",
        "2027-12-30": "Year-end team celebration",
        "2027-12-31": "Finalize 2027 achievements summary"
    }
    
    # ============================================================
    # JANUARY 2028 - Final Evaluation Preparation
    # ============================================================
    jan_tasks_2028 = {
        "2028-01-03": "Prepare final evaluation framework",
        "2028-01-04": "Compile all project achievements",
        "2028-01-05": "Collect performance metrics for 24 months",
        "2028-01-06": "Analyze baseline vs endline data",
        "2028-01-07": "Calculate overall improvement percentages",
        "2028-01-10": "Prepare success stories document",
        "2028-01-11": "Create case studies library",
        "2028-01-12": "Develop lessons learned report",
        "2028-01-13": "Prepare best practices guide",
        "2028-01-14": "Create recommendations for future",
        "2028-01-17": "Prepare final evaluation report draft",
        "2028-01-18": "Review draft with ICARE leadership",
        "2028-01-19": "Incorporate feedback into report",
        "2028-01-20": "Prepare final evaluation presentation",
        "2028-01-21": "Conduct internal review of evaluation",
        "2028-01-24": "Finalize evaluation report",
        "2028-01-25": "Prepare January MPR with evaluation",
        "2028-01-26": "Submit January MPR to PMU",
        "2028-01-27": "Schedule final client presentation",
        "2028-01-28": "Prepare client presentation materials"
    }
    
    # ============================================================
    # FEBRUARY 2028 - Final Client Presentation and Milestone 7
    # ============================================================
    feb_tasks_2028 = {
        "2028-02-01": "Prepare Milestone 7 Report: Final Evaluation",
        "2028-02-02": "Compile evidence for milestone",
        "2028-02-03": "Submit Milestone 7 Report to PMU",
        "2028-02-04": "Prepare final client presentation",
        "2028-02-07": "Conduct final client presentation",
        "2028-02-08": "Incorporate final client feedback",
        "2028-02-09": "Finalize all project deliverables",
        "2028-02-10": "Prepare project closure report",
        "2028-02-11": "Complete all pending documentation",
        "2028-02-14": "Prepare handover packages for each university",
        "2028-02-15": "Conduct handover training sessions",
        "2028-02-16": "Transfer all credentials and access",
        "2028-02-17": "Archive all project data and documents",
        "2028-02-18": "Prepare final financial report",
        "2028-02-21": "Complete performance bank guarantee release",
        "2028-02-22": "Prepare contract closure documents",
        "2028-02-23": "Conduct final team meeting",
        "2028-02-24": "Prepare February MPR with closure",
        "2028-02-25": "Submit February MPR to PMU",
        "2028-02-28": "Plan project celebration event",
        "2028-02-29": "Final milestone review meeting"
    }
    
    # ============================================================
    # MARCH 2028 - Project Closure and Knowledge Transfer
    # ============================================================
    mar_tasks_2028 = {
        "2028-03-01": "Complete knowledge transfer to client team",
        "2028-03-02": "Provide final training to GRDAU staff",
        "2028-03-03": "Handover all system credentials",
        "2028-03-06": "Transfer source code and documentation",
        "2028-03-07": "Provide database backup and restore guide",
        "2028-03-08": "Conduct final user acceptance test",
        "2028-03-09": "Get client sign-off on deliverables",
        "2028-03-10": "Prepare project completion certificate",
        "2028-03-13": "Conduct final project review with MITRA",
        "2028-03-14": "Present overall project achievements",
        "2028-03-15": "Discuss sustainability and future support",
        "2028-03-16": "Get formal project closure letter",
        "2028-03-17": "Prepare success celebration event",
        "2028-03-20": "Organize project completion celebration",
        "2028-03-21": "Release final payments to team",
        "2028-03-22": "Prepare team appreciation letters",
        "2028-03-23": "Document project impact assessment",
        "2028-03-24": "Prepare March MPR with closure status",
        "2028-03-27": "Submit March MPR to PMU",
        "2028-03-28": "Finalize all project reports",
        "2028-03-29": "Archive project documentation",
        "2028-03-30": "Complete financial reconciliation",
        "2028-03-31": "Prepare for contract completion"
    }
    
    # ============================================================
    # APRIL 2028 - Contract Completion and Final Submission
    # ============================================================
    apr_tasks_2028 = {
        "2028-04-03": "Finalize all pending deliverables",
        "2028-04-04": "Complete final project report",
        "2028-04-05": "Prepare executive summary for World Bank",
        "2028-04-06": "Compile all supporting documents",
        "2028-04-07": "Review all deliverables for completeness",
        "2028-04-10": "Get internal approval on final package",
        "2028-04-11": "Submit final deliverables to PMU",
        "2028-04-12": "Present final outcomes to MITRA",
        "2028-04-13": "Get final acceptance certificate",
        "2028-04-14": "Complete contract closure formalities",
        "2028-04-17": "Release performance bank guarantee",
        "2028-04-18": "Submit final invoice to client",
        "2028-04-19": "Prepare project completion report",
        "2028-04-20": "Conduct final team debrief",
        "2028-04-21": "Prepare lessons learned for World Bank",
        "2028-04-24": "Complete knowledge repository handover",
        "2028-04-25": "Submit final documentation to ICARE",
        "2028-04-26": "Prepare April MPR with completion",
        "2028-04-27": "Submit April MPR to PMU",
        "2028-04-28": "CONTRACT COMPLETION - Project Success!"
    }
    
    # ============================================================
    # Merge all tasks into one dictionary
    # ============================================================
    all_tasks.update(june_week1)
    all_tasks.update(june_week2)
    all_tasks.update(june_week3)
    all_tasks.update(june_week4)
    all_tasks.update(june_week5)
    all_tasks.update(july_tasks)
    all_tasks.update(aug_tasks)
    all_tasks.update(sep_tasks)
    all_tasks.update(oct_tasks)
    all_tasks.update(nov_tasks)
    all_tasks.update(dec_tasks)
    all_tasks.update(jan_tasks)
    all_tasks.update(feb_tasks)
    all_tasks.update(mar_tasks)
    all_tasks.update(apr_tasks)
    all_tasks.update(may_tasks)
    all_tasks.update(jun_tasks)
    all_tasks.update(jul_tasks)
    all_tasks.update(aug_tasks)
    all_tasks.update(sep_tasks_2027)
    all_tasks.update(oct_tasks_2027)
    all_tasks.update(nov_tasks_2027)
    all_tasks.update(dec_tasks_2027)
    all_tasks.update(jan_tasks_2028)
    all_tasks.update(feb_tasks_2028)
    all_tasks.update(mar_tasks_2028)
    all_tasks.update(apr_tasks_2028)
    
    return all_tasks

def load_tasks():
    if os.path.exists(DAILY_TASKS_FILE):
        with open(DAILY_TASKS_FILE, 'r') as f:
            return json.load(f)
    tasks = get_all_unique_tasks()
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
    for date_str, task in all_tasks.items():
        if user.get("role") == "data_analyst":
            is_completed = date_str in user_completions
            completion_info = user_completions.get(date_str, {})
            
            # Determine priority based on task content
            priority = "High" if any(word in task.lower() for word in ["milestone", "submit", "present", "final"]) else "Medium"
            
            user_tasks.append({
                "date": date_str,
                "task": task,
                "priority": priority,
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
                "progress": round((completed / total_tasks * 100), 1)
            })
    
    return pd.DataFrame(progress_data)

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
    <tr><td><strong>Total Working Days (24 months)</strong></div><td>{len(load_tasks())}</div></tr>
    <tr><td><strong>Total Task Completions</strong></div><td>{sum(len(c) for c in load_completions().values())}</div></tr>
    <tr><td><strong>Active Team Members</strong></div><td>{len(progress_df)}</div></tr>
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
            <tr><td style="background:#dc3545;color:white;">Admin</div><td>admin@mahastride.com</div><td>Admin@2026</div></tr>
            <tr><td style="background:#17a2b8;color:white;">Project Lead</div><td>projectlead@mahastride.com</div><td>ProjectLead@2026</div></tr>
            <tr><td style="background:#28a745;color:white;">Data Analyst</div><td>sneha@mu.edu</div><td>Sneha@2026</div></tr>
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
        st.metric("⏳ Remaining", len(pending_tasks))
    
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
                <strong>Completed:</strong> {today_task.get('completed_at', 'N/A')[:16]}
            </div>
            """, unsafe_allow_html=True)
        else:
            with st.form(key="complete_today_task"):
                priority_class = "task-pending"
                st.markdown(f"""
                <div class="task-card {priority_class}">
                    <strong>⏳ TASK TO COMPLETE</strong><br>
                    <strong>Task:</strong> {today_task['task']}<br>
                    <strong>Priority:</strong> {today_task['priority']}
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    start_time = st.time_input("Start Time", value=datetime.strptime("10:00", "%H:%M").time())
                with col2:
                    end_time = st.time_input("End Time", value=datetime.strptime("18:00", "%H:%M").time())
                
                work_hours = f"{start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}"
                remarks = st.text_area("📝 Work Accomplished", height=100)
                
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
    st.subheader("📅 Upcoming Tasks (Next 10)")
    
    for task in pending_tasks[:10]:
        priority_icon = "🔴" if task["priority"] == "High" else "🟡"
        st.markdown(f"{priority_icon} **{task['date']}** - {task['task'][:100]}")

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
            <h1>📋 MahaSTRIDE Complete Task Management System</h1>
            <p>24-Month Detailed Task Plan | May 2026 - April 2028</p>
            <p>Monday to Friday | 10:00 AM - 6:00 PM</p>
            <p>✅ May 4 to June 5, 2026: COMPLETED | June 8, 2026 onwards: PENDING</p>
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
            nav_options = ["📊 Dashboard", "📄 Reports"]
        elif role == "project_lead":
            nav_options = ["📊 Dashboard", "📄 Reports"]
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
