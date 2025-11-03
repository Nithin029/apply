import streamlit as st
import json
from datetime import datetime
from apply import ATSApplicationCreator
import base64
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="ATS Job Application Portal",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        height: 3em;
        background: linear-gradient(to right, #667eea, #764ba2);
        color: white;
        border: none;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    .job-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 10px 0;
        transition: all 0.3s ease;
    }
    .job-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.2);
    }
    .ats-card {
        background: white;
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin: 15px 0;
        text-align: center;
        transition: all 0.3s ease;
        border: 2px solid transparent;
    }
    .ats-card:hover {
        border: 2px solid #667eea;
        transform: scale(1.05);
    }
    .header-text {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3em;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
    }
    .success-box {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 20px 0;
    }
    .info-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 0.9em;
        display: inline-block;
        margin: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'selected_ats' not in st.session_state:
    st.session_state.selected_ats = None
if 'selected_job' not in st.session_state:
    st.session_state.selected_job = None
if 'view' not in st.session_state:
    st.session_state.view = 'ats_list'


# Load jobs data from environment or config
@st.cache_data
def load_jobs_data():
    return {
        "bamboohr_ats": {
            "integration_id": "mg_d8SfAvVUwjyJHrffzeAnAC",
            "name": "BambooHR ATS",
            "icon": "🏢",
            "color": "#4CAF50",
            "jobs": [
                {
                    "id": "15",
                    "title": "IT Security Engineer",
                    "status": "OPEN",
                    "location": "Mayfair, London, City of, United Kingdom",
                    "department": "IT",
                    "created_at": "2026-03-08T20:20:12Z",
                    "stages": [{"id": "1", "text": "New"}],
                    "questions": []
                },
                {
                    "id": "18",
                    "title": "Videographer",
                    "status": "DRAFT",
                    "location": "Lindon, Utah, United States",
                    "department": "Marketing",
                    "created_at": "2025-11-02T09:51:07Z",
                    "stages": [{"id": "1", "text": "New"}],
                    "questions": []
                },
                {
                    "id": "20",
                    "title": "Software Engineer",
                    "status": "OPEN",
                    "location": "Sydney, New South Wales, Australia",
                    "department": "Product",
                    "created_at": "2026-03-08T20:22:25Z",
                    "stages": [{"id": "1", "text": "New"}],
                    "questions": []
                },
                {
                    "id": "22",
                    "title": "Financial Analyst",
                    "status": "OPEN",
                    "location": "Salt Lake City, Utah, United States",
                    "department": "Finance",
                    "created_at": "2026-03-08T20:21:18Z",
                    "stages": [{"id": "1", "text": "New"}],
                    "questions": []
                }
            ]
        },
        "workable": {
            "integration_id": "mg_bdP3JP31kh2jnCGTJGr1er",
            "name": "Workable",
            "icon": "⚙️",
            "color": "#FF9800",
            "jobs": [
                {
                    "id": "2CA2D5B257",
                    "title": "Registered Nurse",
                    "status": "OPEN",
                    "location": "Hyderabad, Telangana, India",
                    "department": "Healthcare",
                    "created_at": "2025-10-24T08:28:11Z",
                    "description": "Nurse Works Near is excited to announce a new opportunity for dedicated and skilled Registered Nurses to join our dynamic staffing and recruiting team. As a leading provider in healthcare staffing solutions, we are committed to matching talented nurses with facilities and institutions that require their expertise.",
                    "salary_range": "₹400,000 - ₹600,000",
                    "stages": [{"id": "applied", "text": "Applied"}],
                    "questions": [
                        {
                            "id": "a36ea9",
                            "title": "Are you a veteran?",
                            "type": "YES_NO",
                            "required": True
                        }
                    ]
                }
            ]
        },
        "recruitee": {
            "integration_id": "mg_X3rFfTRfRdTGT9p6IG6rEO",
            "name": "Recruitee",
            "icon": "🎯",
            "color": "#2196F3",
            "jobs": [
                {
                    "id": "2321420",
                    "title": "Senior Marketer (Sample)",
                    "status": "OPEN",
                    "location": "Remote",
                    "department": "Marketing",
                    "created_at": None,
                    "stages": [{"id": "1", "text": "Applied"}],
                    "questions": []
                },
                {
                    "id": "2321421",
                    "title": "Recruiter (Sample)",
                    "status": "NOT_SPECIFIED",
                    "location": "Remote",
                    "department": "HR",
                    "created_at": None,
                    "stages": [{"id": "1", "text": "Applied"}],
                    "questions": []
                }
            ]
        },
        "breezy": {
            "integration_id": "mg_YZ2dllr3UzefyrQ7E1QPqS",
            "name": "Breezy HR",
            "icon": "🌊",
            "color": "#00BCD4",
            "jobs": []
        },
        "zoho_recruit": {
            "integration_id": "mg_CuzaQl6YbvvFrvC9xP5gk6",
            "name": "Zoho Recruit",
            "icon": "🔷",
            "color": "#9C27B0",
            "jobs": []
        }
    }


# Get API Key from environment
API_KEY = os.getenv('KNIT_API_KEY', 'YOUR_API_KEY')

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/briefcase.png", width=80)
    st.title("ATS Portal")
    st.markdown("---")

    # Show API key status without exposing it
    if API_KEY and API_KEY != 'YOUR_API_KEY':
        st.success("🔑 API Key Loaded")
    else:
        st.error("⚠️ API Key Not Found")
        st.caption("Set KNIT_API_KEY in .env file")

    st.markdown("---")
    st.markdown("### 📊 Quick Stats")
    jobs_data = load_jobs_data()
    total_jobs = sum(len(ats['jobs']) for ats in jobs_data.values())
    total_ats = len(jobs_data)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("ATS Platforms", total_ats)
    with col2:
        st.metric("Total Jobs", total_jobs)

    st.markdown("---")
    st.markdown("### 🎨 Theme")
    st.write("Gradient Purple Theme")

# Main content
jobs_data = load_jobs_data()

# View: ATS List
if st.session_state.view == 'ats_list':
    st.markdown('<p class="header-text">🚀 Choose Your ATS Platform</p>', unsafe_allow_html=True)
    st.markdown("### Discover opportunities across multiple platforms")

    cols = st.columns(3)

    for idx, (ats_key, ats_info) in enumerate(jobs_data.items()):
        with cols[idx % 3]:
            job_count = len(ats_info['jobs'])

            st.markdown(f"""
                <div class="ats-card">
                    <h1>{ats_info['icon']}</h1>
                    <h3>{ats_info['name']}</h3>
                    <p><strong>{job_count}</strong> Jobs Available</p>
                </div>
            """, unsafe_allow_html=True)

            if st.button(f"Explore Jobs →", key=f"view_{ats_key}"):
                st.session_state.selected_ats = ats_key
                st.session_state.view = 'job_list'
                st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)

# View: Job List
elif st.session_state.view == 'job_list':
    ats_key = st.session_state.selected_ats
    ats_info = jobs_data[ats_key]

    col1, col2 = st.columns([1, 11])
    with col1:
        if st.button("← Back"):
            st.session_state.view = 'ats_list'
            st.session_state.selected_ats = None
            st.rerun()

    st.markdown(f'<p class="header-text">{ats_info["icon"]} {ats_info["name"]}</p>', unsafe_allow_html=True)
    st.markdown(f"### 💼 {len(ats_info['jobs'])} Open Positions")
    st.markdown("---")

    if len(ats_info['jobs']) == 0:
        st.info("🔍 No jobs available for this ATS platform at the moment. Check back later!")
    else:
        for job in ats_info['jobs']:
            st.markdown(f"""
                <div class="job-card">
                    <h2>💼 {job['title']}</h2>
                </div>
            """, unsafe_allow_html=True)

            col1, col2, col3 = st.columns([2, 2, 1])

            with col1:
                if job.get('department'):
                    st.markdown(f'<span class="info-badge">🏢 {job["department"]}</span>', unsafe_allow_html=True)
                st.markdown(f'<span class="info-badge">📍 {job["location"]}</span>', unsafe_allow_html=True)

            with col2:
                status_color = "🟢" if job['status'] == "OPEN" else "🟡"
                st.markdown(f'<span class="info-badge">{status_color} {job["status"]}</span>', unsafe_allow_html=True)

            with col3:
                if st.button("Apply Now →", key=f"apply_{job['id']}", use_container_width=True):
                    st.session_state.selected_job = job
                    st.session_state.view = 'application_form'
                    st.rerun()

            # Only show description if it exists and is not None/empty
            if job.get('description') and job['description'].strip():
                with st.expander("📄 View Job Description"):
                    st.write(job['description'])

            # Only show salary if it exists
            if job.get('salary_range'):
                st.markdown(f"**💰 Salary Range:** {job['salary_range']}")

            st.markdown("---")

# View: Application Form
elif st.session_state.view == 'application_form':
    ats_key = st.session_state.selected_ats
    ats_info = jobs_data[ats_key]
    job = st.session_state.selected_job

    col1, col2 = st.columns([1, 11])
    with col1:
        if st.button("← Back"):
            st.session_state.view = 'job_list'
            st.session_state.selected_job = None
            st.rerun()

    st.markdown(f'<p class="header-text">📝 Application Form</p>', unsafe_allow_html=True)
    st.markdown(f"### Applying for: **{job['title']}** at {ats_info['name']}")
    st.markdown("---")

    with st.form("application_form"):
        # Personal Information
        st.markdown("### 👤 Personal Information")
        col1, col2 = st.columns(2)

        with col1:
            first_name = st.text_input("First Name *", placeholder="John", help="Required field")
            email = st.text_input("Email Address *", placeholder="john@example.com", help="Required field")
            title = st.text_input("Current Job Title", placeholder="Software Engineer")

        with col2:
            last_name = st.text_input("Last Name *", placeholder="Doe", help="Required field")
            phone = st.text_input("Phone Number *", placeholder="+1-999-999-9999", help="Required field")
            company = st.text_input("Current Company", placeholder="Tech Corp Inc.")

        st.markdown("---")

        # Education
        st.markdown("### 🎓 Education (Optional)")
        col1, col2 = st.columns(2)
        with col1:
            degree = st.text_input("Degree", placeholder="Bachelor of Science")
            major = st.text_input("Major/Field of Study", placeholder="Computer Science")
        with col2:
            institute = st.text_input("Institute/University", placeholder="Massachusetts Institute of Technology")
            currently_pursuing = st.checkbox("📚 Currently Pursuing")

        st.markdown("---")

        # Address
        st.markdown("### 🏠 Address Information (Optional)")
        col1, col2 = st.columns(2)
        with col1:
            address_line1 = st.text_input("Address Line 1", placeholder="123 Main Street, Apt 4B")
            city = st.text_input("City", placeholder="New York")
            country = st.selectbox("Country",
                                   ["", "United States", "India", "United Kingdom", "Canada", "Australia", "Other"])
        with col2:
            st.write("")  # Spacer
            state = st.text_input("State/Province", placeholder="New York")
            zip_code = st.text_input("Zip/Postal Code", placeholder="10001")

        st.markdown("---")

        # Documents Section
        st.markdown("### 📎 Documents")
        st.info("💡 Upload your resume and cover letter in PDF or DOC format (Max 10MB each)")

        col1, col2 = st.columns(2)
        with col1:
            resume = st.file_uploader(
                "Upload Resume/CV *",
                type=['pdf', 'doc', 'docx'],
                help="Required - PDF or DOC format, max 10MB"
            )
            if resume:
                st.success(f"✅ {resume.name} uploaded ({resume.size / 1024:.1f} KB)")

        with col2:
            cover_letter = st.file_uploader(
                "Upload Cover Letter (Optional)",
                type=['pdf', 'doc', 'docx'],
                help="Optional - PDF or DOC format, max 10MB"
            )
            if cover_letter:
                st.success(f"✅ {cover_letter.name} uploaded ({cover_letter.size / 1024:.1f} KB)")

        st.markdown("---")

        # Additional Questions
        answers = []
        if job.get('questions') and len(job['questions']) > 0:
            st.markdown("### ❓ Additional Questions")
            st.info("Please answer the following questions from the employer")

            for idx, question in enumerate(job['questions'], 1):
                required_mark = "🔴" if question.get('required') else "⚪"
                st.markdown(f"**{idx}. {question['title']}** {required_mark}")

                if question['type'] == 'YES_NO':
                    answer = st.radio(
                        f"Select your answer",
                        options=["Yes", "No"],
                        key=f"q_{question['id']}",
                        horizontal=True
                    )
                    answers.append({
                        "id": question['id'],
                        "question": question['title'],
                        "answer": answer,
                        "type": question['type'],
                        "multipleChoiceAnswers": [answer]
                    })
                elif question['type'] == 'TEXT':
                    answer = st.text_area(
                        f"Your answer",
                        key=f"q_{question['id']}",
                        placeholder="Type your answer here...",
                        height=100
                    )
                    answers.append({
                        "id": question['id'],
                        "question": question['title'],
                        "answer": answer,
                        "type": question['type']
                    })

                st.markdown("<br>", unsafe_allow_html=True)

            st.markdown("---")

        # Submit Button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button(
                "🚀 Submit Application",
                use_container_width=True,
                type="primary"
            )

        if submit_button:
            # Validation
            errors = []
            if not first_name:
                errors.append("First Name is required")
            if not last_name:
                errors.append("Last Name is required")
            if not email:
                errors.append("Email is required")
            if not phone:
                errors.append("Phone Number is required")
            if not resume:
                errors.append("Resume/CV is required")

            if errors:
                st.error("❌ Please fix the following errors:")
                for error in errors:
                    st.error(f"  • {error}")
            else:
                try:
                    # Convert resume to base64
                    resume_data = None
                    cover_letter_data = None

                    if resume:
                        resume_bytes = resume.read()
                        resume_data = {
                            "filename": resume.name,
                            "content": base64.b64encode(resume_bytes).decode('utf-8'),
                            "content_type": resume.type
                        }

                    if cover_letter:
                        cover_letter_bytes = cover_letter.read()
                        cover_letter_data = {
                            "filename": cover_letter.name,
                            "content": base64.b64encode(cover_letter_bytes).decode('utf-8'),
                            "content_type": cover_letter.type
                        }

                    # Initialize ATS creator
                    creator = ATSApplicationCreator(API_KEY)

                    # Get initial stage ID
                    initial_stage_id = job['stages'][0]['id'] if job.get('stages') and len(job['stages']) > 0 else "1"

                    # Prepare application data
                    application_data = {
                        "first_name": first_name,
                        "last_name": last_name,
                        "email": email,
                        "phone": phone,
                        "title": title if title else None,
                        "company": company if company else None,
                        "degree": degree if degree else None,
                        "major": major if major else None,
                        "institute": institute if institute else None,
                        "currently_pursuing": currently_pursuing,
                        "address_line1": address_line1 if address_line1 else None,
                        "city": city if city else None,
                        "state": state if state else None,
                        "country": country if country else None,
                        "zip_code": zip_code if zip_code else None,
                        "answers": answers if answers else None
                    }

                    # Show spinner while submitting
                    with st.spinner('🔄 Submitting your application...'):
                        # Create application
                        result = creator.create_application(
                            ats_name=ats_key,
                            job_id=job['id'],
                            initial_stage_id=initial_stage_id,
                            **application_data
                        )

                    # Show result
                    if result.get('success') == 'true' or result.get('success') == True:
                        st.markdown("""
                            <div class="success-box">
                                <h1>🎉 Success!</h1>
                                <h3>Your application has been submitted successfully!</h3>
                                <p>We'll review your application and get back to you soon.</p>
                                <p style="margin-top: 15px;">Click the <strong>← Back</strong> button above to apply for more jobs.</p>
                            </div>
                        """, unsafe_allow_html=True)

                        if result.get('data'):
                            with st.expander("📋 View Application Details"):
                                st.json(result['data'])
                    else:
                        st.error(f"❌ Application submission failed!")
                        st.error(f"**Error:** {result.get('error', 'Unknown error occurred')}")
                        with st.expander("🔍 View Full Error Response"):
                            st.json(result)

                except FileNotFoundError:
                    st.error("❌ Configuration file 'ats_config.json' not found. Please create it first.")
                except Exception as e:
                    st.error(f"❌ An unexpected error occurred: {str(e)}")
                    with st.expander("🔍 View Error Details"):
                        st.exception(e)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: white; padding: 20px;'>
        <p>💼 ATS Job Application Portal | Built with Streamlit</p>
        <p>🔒 Your data is secure and encrypted</p>
    </div>
""", unsafe_allow_html=True)