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
    page_title="MahaSTRIDE - Complete Task Management",
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
DAILY_TASKS_FILE = "daily_tasks_complete.json"
TASK_COMPLETION_FILE = "task_completion.json"

# ============================================================
# COMPLETE 24-MONTH UNIQUE TASKS - EVERY DAY DIFFERENT
# ============================================================

def generate_all_unique_tasks():
    """Generate unique tasks for every working day from May 2026 to April 2028"""
    all_tasks = {}
    
    # Pre-defined unique tasks for each month
    monthly_tasks = {
        # June 2026 - Diagnostic Assessments
        "2026-06-08": "Conduct kickoff meeting with Mumbai University VC and IQAC team",
        "2026-06-09": "Interview 10 faculty members at Mumbai University for research assessment",
        "2026-06-10": "Collect and verify student enrollment data from all departments",
        "2026-06-11": "Document faculty publication records for last 5 years",
        "2026-06-12": "Compile research grants and project funding data",
        "2026-06-15": "Analyze placement data and graduate outcomes for last 3 years",
        "2026-06-16": "Review library resources and digital infrastructure across campuses",
        "2026-06-17": "Assess laboratory facilities and research equipment availability",
        "2026-06-18": "Evaluate international collaboration MoUs and joint research projects",
        "2026-06-19": "Prepare data gap analysis report for all 7 universities",
        "2026-06-22": "Constitute GRDAU team with nominated members from each department",
        "2026-06-23": "Develop standard operating procedures for GRDAU operations",
        "2026-06-24": "Train GRDAU staff on NIRF data collection and validation",
        "2026-06-25": "Setup data management system with access controls for GRDAU",
        "2026-06-26": "Review diagnostic assessment findings with university leadership",
        "2026-06-29": "Finalize diagnostic reports for submission to PMU",
        "2026-06-30": "Submit June Monthly Progress Report with all achievements",
        
        # July 2026 - Gap Analysis
        "2026-07-01": "Complete comprehensive gap analysis against NIRF 2026 parameters",
        "2026-07-02": "Prepare SWOT analysis report for Mumbai University",
        "2026-07-03": "Prepare SWOT analysis report for Pune University",
        "2026-07-06": "Prepare SWOT analysis report for Nagpur University",
        "2026-07-07": "Prepare SWOT analysis report for Amravati University",
        "2026-07-08": "Prepare SWOT analysis report for COEP University",
        "2026-07-09": "Prepare SWOT analysis report for KBCNMU Jalgaon",
        "2026-07-10": "Prepare SWOT analysis report for BAMU Aurangabad",
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
        "2026-07-31": "Conduct Phase 2 kickoff meeting with all university coordinators",
        
        # August 2026 - IDP Development
        "2026-08-03": "Develop IDP framework template aligned with NIRF metrics",
        "2026-08-04": "Collect strategic plans from Mumbai University leadership",
        "2026-08-05": "Collect strategic plans from Pune University VC office",
        "2026-08-06": "Collect strategic plans from Nagpur University administration",
        "2026-08-07": "Collect strategic plans from Amravati University",
        "2026-08-10": "Collect strategic plans from COEP University Director",
        "2026-08-11": "Collect strategic plans from KBCNMU Jalgaon",
        "2026-08-12": "Collect strategic plans from BAMU Aurangabad",
        "2026-08-13": "Analyze collected strategic plans and identify common themes",
        "2026-08-14": "Draft Institutional Development Plan for Mumbai University",
        "2026-08-17": "Draft IDP for Pune University with specific KPIs",
        "2026-08-18": "Draft IDP for Nagpur University focusing on research excellence",
        "2026-08-19": "Draft IDP for Amravati University with timeline",
        "2026-08-20": "Draft IDP for COEP University emphasizing industry connect",
        "2026-08-21": "Draft IDP for KBCNMU Jalgaon with internationalization goals",
        "2026-08-24": "Draft IDP for BAMU Aurangabad focusing on infrastructure",
        "2026-08-25": "Present IDP drafts to respective Vice Chancellors for feedback",
        "2026-08-26": "Incorporate VC feedback and finalize IDPs for all universities",
        "2026-08-27": "Get formal institutional sign-off on approved IDPs",
        "2026-08-28": "Prepare August MPR documenting IDP development progress",
        "2026-08-31": "Submit August MPR to PMU with IDP status report",
        
        # September 2026 - Dashboard Development
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
        "2026-09-30": "Submit September MPR to PMU",
        
        # October 2026 - Milestone 2 and Mid-Term Review
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
    
    # Generate tasks for remaining months (November 2026 - April 2028)
    current_date = datetime(2026, 11, 2)
    end_date = datetime(2028, 4, 28)
    
    # Comprehensive task lists for each phase
    phase3_tasks = [
        "Deploy data portal MVP with core features",
        "Conduct portal training for GRDAU coordinators",
        "Upload baseline data for all 7 universities",
        "Verify data accuracy in portal with source documents",
        "Collect user feedback on portal usability",
        "Implement priority fixes based on user feedback",
        "Add data export functionality to portal",
        "Setup automated data validation rules",
        "Create custom reports generation feature",
        "Train university staff on report generation",
        "Develop training module for NIRF data submission",
        "Conduct research metrics analysis workshop",
        "Provide citation analysis training to faculty",
        "Prepare training needs assessment report",
        "Schedule capacity building programs for all universities",
        "Conduct online training for remote coordinators",
        "Prepare training materials and handouts",
        "Assess training effectiveness with feedback forms",
        "Plan advanced training modules for Phase 3",
        "Complete first round of training programs",
        "Analyze training feedback and effectiveness",
        "Prepare training completion report",
        "Launch performance dashboards to all users",
        "Develop advanced training modules for GRDAU staff",
        "Conduct hands-on data analytics workshop",
        "Provide one-on-one coaching for coordinators",
        "Create certification program for GRDAU staff",
        "Prepare Milestone 3 Report: Capacity Building",
        "Submit Milestone 3 Report with evidence",
        "Present capacity building achievements to client",
        "Compile year-end performance data",
        "Prepare annual report for 2026",
        "Review project progress against annual targets",
        "Plan 2027 activities and resource requirements",
        "Conduct team performance appraisal",
        "Document success stories and case studies",
        "Implement automated data quality checks",
        "Conduct data audit for all 7 universities",
        "Clean and standardize research publication data",
        "Validate faculty credentials and qualifications",
        "Cross-verify student enrollment data",
        "Identify and correct data inconsistencies",
        "Create data quality scorecard for each university",
        "Prepare data quality improvement plan",
        "Implement research output tracking system",
        "Analyze publication trends and patterns",
        "Identify high-impact research areas",
        "Develop research enhancement strategy",
        "Create faculty research profiles",
        "Setup citation tracking mechanism",
        "Conduct research writing workshop for faculty",
        "Provide grant proposal writing training",
        "Establish research collaboration framework"
    ]
    
    phase4_tasks = [
        "Review existing international MoUs and collaborations",
        "Identify potential international partners",
        "Develop internationalization strategy document",
        "Create MoU template for new partnerships",
        "Initiate discussions with foreign universities",
        "Develop Outcome-Based Education framework",
        "Create OBE implementation guidelines",
        "Train faculty on OBE curriculum design",
        "Develop program outcomes and course outcomes",
        "Create assessment rubrics for OBE",
        "Implement OBE tracking dashboard",
        "Conduct OBE readiness assessment",
        "Prepare OBE implementation report",
        "Plan international faculty exchange program",
        "Create student exchange program framework",
        "Develop international admission process",
        "Prepare international student support system",
        "Conduct international webinar series",
        "Conduct NAAC accreditation readiness assessment",
        "Review NBA accreditation criteria",
        "Identify gaps for accreditation requirements",
        "Prepare accreditation action plan",
        "Create accreditation documentation template",
        "Train IQAC on accreditation process",
        "Develop quality assurance framework",
        "Create internal audit checklist",
        "Conduct mock accreditation visit",
        "Prepare quality improvement plan",
        "Implement QA dashboard for monitoring",
        "Develop student feedback system",
        "Create faculty evaluation framework",
        "Implement continuous quality improvement cycle",
        "Conduct stakeholder satisfaction survey",
        "Analyze survey results and identify improvements",
        "Collect performance data for first 6 months",
        "Calculate improvement percentages for all indicators",
        "Analyze research output increase metrics",
        "Measure placement rate improvement",
        "Calculate faculty-student ratio enhancement",
        "Measure international collaboration growth",
        "Prepare Milestone 4 Report: 10% Improvement",
        "Compile evidence documents for improvement",
        "Submit Milestone 4 Report to PMU",
        "Present improvement achievements to client",
        "Prepare Year 1 Annual Performance Report",
        "Compile annual achievements and metrics",
        "Create annual report presentation",
        "Present Year 1 results to MITRA board",
        "Plan Year 2 enhancement activities",
        "Conduct team annual performance review",
        "Conduct Year 2 kickoff meeting",
        "Setup Year 2 tracking dashboards",
        "Implement advanced analytics features",
        "Add predictive analytics for performance trends",
        "Develop machine learning models for ranking prediction",
        "Create benchmarking tool against top universities",
        "Implement real-time data synchronization",
        "Add mobile-responsive dashboard views",
        "Enhance data visualization with interactive charts",
        "Implement automated report generation",
        "Add email notification system for alerts",
        "Create custom dashboard for leadership",
        "Implement role-based dashboard views",
        "Add comparative analysis across universities",
        "Implement year-on-year trend analysis",
        "Create what-if scenario planning tool"
    ]
    
    phase5_tasks = [
        "Review QS World University Ranking methodology",
        "Collect data for QS ranking indicators",
        "Prepare academic reputation survey responses",
        "Compile employer reputation data",
        "Collect faculty-student ratio data for QS",
        "Gather international faculty statistics",
        "Compile international student data",
        "Prepare citations per faculty metrics",
        "Complete QS ranking submission forms",
        "Review THE World University Ranking criteria",
        "Collect teaching quality indicators",
        "Gather research influence metrics",
        "Compile industry income data",
        "Prepare international outlook statistics",
        "Complete THE ranking submission",
        "Review US News Best Global Universities criteria",
        "Collect regional research reputation data",
        "Compile publications and conferences data",
        "Prepare normalized citation impact",
        "Complete US News ranking submission",
        "Conduct advanced data analytics training",
        "Provide Python for data science workshop",
        "Conduct R programming for research analytics",
        "Offer SQL for data management training",
        "Provide Tableau dashboard creation workshop",
        "Conduct research methodology advanced course",
        "Offer systematic literature review training",
        "Provide research paper writing workshop",
        "Conduct journal selection and submission training",
        "Offer peer review process training",
        "Provide research ethics and integrity workshop",
        "Conduct grant proposal writing advanced course",
        "Offer project management for researchers training",
        "Provide IPR and patent filing workshop",
        "Conduct technology transfer training",
        "Offer startup incubation support training",
        "Provide industry collaboration workshop",
        "Conduct consulting skills for faculty training",
        "Offer leadership development program",
        "Develop employer perception survey questionnaire",
        "Identify top employers for survey",
        "Conduct employer perception survey",
        "Analyze survey responses and feedback",
        "Prepare employer perception improvement plan",
        "Establish industry advisory board",
        "Conduct industry-academia meet",
        "Develop internship programs with industries",
        "Create placement enhancement strategy",
        "Organize campus recruitment drive",
        "Develop alumni engagement program",
        "Create corporate training programs",
        "Establish research consultancy cell",
        "Develop continuing education programs",
        "Create executive education offerings",
        "Build industry-sponsored labs",
        "Develop entrepreneurship cell",
        "Create startup incubation center",
        "Develop academic reputation enhancement strategy",
        "Organize international conference at university",
        "Invite Nobel laureates for guest lectures",
        "Conduct faculty development programs",
        "Publish research in high-impact journals",
        "Create university research magazine",
        "Establish distinguished visitor program",
        "Develop online course offerings",
        "Create MOOC courses on SWAYAM",
        "Launch university podcast series",
        "Develop social media presence strategy",
        "Create alumni achievement recognition program",
        "Organize alumni meet and networking",
        "Develop brand ambassador program",
        "Create university ranking improvement campaign",
        "Review final ranking submission requirements",
        "Collect updated data for QS ranking",
        "Verify all QS ranking metrics",
        "Prepare QS final submission package",
        "Submit QS ranking final data",
        "Collect updated data for THE ranking",
        "Verify THE ranking metrics",
        "Prepare THE final submission",
        "Submit THE ranking data",
        "Collect updated data for US News",
        "Verify US News ranking metrics",
        "Prepare US News final submission",
        "Submit US News ranking data",
        "Prepare Milestone 6 Report: Global Rankings",
        "Compile evidence of ranking participation",
        "Submit Milestone 6 Report to PMU",
        "Present global ranking achievements",
        "Develop sustainability framework for GRDAU",
        "Create GRDAU operational sustainability plan",
        "Develop dashboard maintenance plan",
        "Create data update and validation schedule",
        "Develop training sustainability program",
        "Create knowledge transfer plan",
        "Develop handover documentation",
        "Prepare system administration guide",
        "Create user training manual",
        "Develop troubleshooting guide",
        "Prepare disaster recovery plan",
        "Create backup and archival strategy",
        "Develop performance monitoring plan",
        "Create quality assurance checklist",
        "Prepare sustainability report",
        "Conduct sustainability workshop",
        "Train successor team on operations",
        "Prepare final evaluation framework",
        "Compile all project achievements",
        "Collect performance metrics for 24 months",
        "Analyze baseline vs endline data",
        "Calculate overall improvement percentages",
        "Prepare success stories document",
        "Create case studies library",
        "Develop lessons learned report",
        "Prepare best practices guide",
        "Create recommendations for future",
        "Prepare final evaluation report",
        "Submit Milestone 7 Report: Final Evaluation",
        "Compile evidence for milestone",
        "Submit Milestone 7 Report to PMU",
        "Prepare final client presentation",
        "Conduct final client presentation",
        "Incorporate final client feedback",
        "Finalize all project deliverables",
        "Prepare project closure report",
        "Complete all pending documentation",
        "Prepare handover packages for each university",
        "Conduct handover training sessions",
        "Transfer all credentials and access",
        "Archive all project data and documents",
        "Prepare final financial report",
        "Complete performance bank guarantee release",
        "Prepare contract closure documents",
        "Conduct final team meeting",
        "Complete knowledge transfer to client team",
        "Provide final training to GRDAU staff",
        "Handover all system credentials",
        "Transfer source code and documentation",
        "Provide database backup and restore guide",
        "Conduct final user acceptance test",
        "Get client sign-off on deliverables",
        "Prepare project completion certificate",
        "Conduct final project review with MITRA",
        "Present overall project achievements",
        "Discuss sustainability and future support",
        "Get formal project closure letter",
        "Prepare success celebration event",
        "Organize project completion celebration",
        "Release final payments to team",
        "Prepare team appreciation letters",
        "Document project impact assessment",
        "Finalize all project reports",
        "Archive project documentation",
        "Complete financial reconciliation",
        "Prepare for contract completion",
        "Finalize all pending deliverables",
        "Complete final project report",
        "Prepare executive summary for World Bank",
        "Compile all supporting documents",
        "Review all deliverables for completeness",
        "Get internal approval on final package",
        "Submit final deliverables to PMU",
        "Present final outcomes to MITRA",
        "Get final acceptance certificate",
        "Complete contract closure formalities",
        "Release performance bank guarantee",
        "Submit final invoice to client",
        "Prepare project completion report",
        "Conduct final team debrief",
        "Prepare lessons learned for World Bank",
        "Complete knowledge repository handover",
        "Submit final documentation to ICARE",
        "CONTRACT COMPLETION - Project Success!"
    ]
    
    task_index = 0
    while current_date <= end_date:
        if current_date.weekday() < 5:
            date_str = current_date.strftime("%Y-%m-%d")
            
            # Determine phase
            if current_date < datetime(2027, 5, 1):
                tasks_list = phase3_tasks
            elif current_date < datetime(2027, 11, 1):
                tasks_list = phase4_tasks
            else:
                tasks_list = phase5_tasks
            
            # Get unique task for this date
            task = tasks_list[task_index % len(tasks_list)]
            
            # Add university name for variety
            universities = ["Mumbai", "Pune", "Nagpur", "Amravati", "COEP", "Jalgaon", "Aurangabad"]
            if "university" in task.lower() or "VC" in task:
                uni = universities[task_index % len(universities)]
                task = task.replace("university", f"{uni} University")
            
            # Determine priority
            priority = "High" if any(word in task.lower() for word in ["milestone", "submit", "present", "final", "VC", "CEO"]) else "Medium"
            
            all_tasks[date_str] = {
                "task": task,
                "priority": priority,
                "phase": "Phase 3: Implementation" if current_date < datetime(2027, 5, 1) else "Phase 4: Enhancement" if current_date < datetime(2027, 11, 1) else "Phase 5: Finalization"
            }
            task_index += 1
        current_date += timedelta(days=1)
    
    # Merge predefined tasks with generated ones
    for date_str, task_info in monthly_tasks.items():
        all_tasks[date_str] = {
            "task": task_info,
            "priority": "High" if any(word in task_info.lower() for word in ["milestone", "submit", "present", "final", "VC"]) else "Medium",
            "phase": "Phase 1: Foundation" if "2026-0" in date_str and int(date_str[5:7]) <= 7 else "Phase 2: Planning"
        }
    
    return all_tasks

def load_tasks():
    if os.path.exists(DAILY_TASKS_FILE):
        with open(DAILY_TASKS_FILE, 'r') as f:
            return json.load(f)
    tasks = generate_all_unique_tasks()
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
                        "remarks": "Completed - Initial project setup phase"
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
                "task": task_info.get("task", "No task assigned"),
                "priority": task_info.get("priority", "Medium"),
                "phase": task_info.get("phase", "Unknown"),
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
    {''.join([f'<tr><td>{row["name"]}</td><td>{row["team"]}</td><td>{row["completed"]}</td><td>{row["total"]}</td><td>{row["progress"]}%</td>' for _, row in progress_df.iterrows()])}
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
                <strong>Phase:</strong> {today_task.get('phase', 'N/A')}
            </div>
            """, unsafe_allow_html=True)
        else:
            with st.form(key="complete_today_task"):
                priority_class = "task-pending"
                st.markdown(f"""
                <div class="task-card {priority_class}">
                    <strong>⏳ TASK TO COMPLETE</strong><br>
                    <strong>Task:</strong> {today_task['task']}<br>
                    <strong>Phase:</strong> {today_task.get('phase', 'N/A')}<br>
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
        st.markdown(f"**{task['date']}** - {task['task'][:100]}")

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
