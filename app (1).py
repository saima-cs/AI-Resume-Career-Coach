
import re
from io import BytesIO

import streamlit as st
from pypdf import PdfReader
from groq import Groq


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Resume & Career Coach",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .hero {
        padding: 2rem;
        border-radius: 20px;
        background: linear-gradient(
            135deg,
            #111827,
            #1e3a8a,
            #312e81
        );
        color: white;
        margin-bottom: 25px;
    }

    .hero h1 {
        font-size: 3rem;
        margin-bottom: 10px;
    }

    .hero p {
        font-size: 1.15rem;
    }

    .feature-card {
        padding: 1.3rem;
        border-radius: 15px;
        border: 1px solid #e5e7eb;
        background: white;
        min-height: 160px;
        margin-bottom: 15px;
    }

    .project-card {
        padding: 1.2rem;
        border-radius: 15px;
        border: 1px solid #e5e7eb;
        background: white;
        margin-bottom: 15px;
    }

    .roadmap-card {
        padding: 1.2rem;
        border-radius: 15px;
        border-left: 5px solid #4f46e5;
        background: white;
        margin-bottom: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "resume_text": "",
    "analysis": "",
    "resume_score": 0,
    "ats_score": 0,
    "career_match": 0,
    "career_match_result": "",
    "skill_gap_result": "",
    "roadmap_result": "",
    "projects_result": "",
    "interview_questions": "",
    "interview_feedback": "",
    "target_role": "",
}

for key, value in defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# GROQ CONFIGURATION
# ============================================================

MODEL_NAME = "llama-3.3-70b-versatile"


@st.cache_resource
def get_groq_client():

    try:

        api_key = st.secrets["GROQ_API_KEY"]

        if not api_key:
            return None

        return Groq(api_key=api_key)

    except Exception:

        return None


def ask_groq(prompt, max_tokens=3500):

    client = get_groq_client()

    if client is None:

        st.warning(
            "Groq API key is not configured. "
            "Please add GROQ_API_KEY in Streamlit Cloud Secrets."
        )

        return None

    system_prompt = """
    You are an expert AI Resume and Career Coach.

    Your responsibilities include:

    - Resume analysis
    - ATS optimization
    - Career planning
    - Skill gap analysis
    - Portfolio recommendations
    - Interview preparation

    IMPORTANT RULES:

    1. Never invent qualifications.
    2. Never invent degrees.
    3. Never invent jobs.
    4. Never invent internships.
    5. Never invent certifications.
    6. Never invent achievements.
    7. Clearly distinguish existing skills from recommended skills.
    8. Do not encourage lying during interviews.
    9. Give practical advice.
    10. Use professional formatting.
    """

    try:

        response = client.chat.completions.create(

            model=MODEL_NAME,

            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],

            temperature=0.3,
            max_tokens=max_tokens,
        )

        return response.choices[0].message.content

    except Exception as error:

        st.error(
            "The AI request could not be completed. "
            "Please check your Groq API configuration."
        )

        return None


# ============================================================
# PDF RESUME EXTRACTION
# ============================================================

def extract_resume_text(uploaded_file):

    try:

        file_bytes = uploaded_file.getvalue()

        if not file_bytes:

            return None, "The uploaded PDF is empty."

        max_size = 10 * 1024 * 1024

        if len(file_bytes) > max_size:

            return None, (
                "The PDF is larger than 10 MB. "
                "Please upload a smaller resume."
            )

        reader = PdfReader(BytesIO(file_bytes))

        if len(reader.pages) == 0:

            return None, "The PDF does not contain any pages."

        max_pages = 25

        pages = reader.pages[:max_pages]

        extracted_text = []

        for page in pages:

            try:

                text = page.extract_text() or ""

                extracted_text.append(text)

            except Exception:

                extracted_text.append("")

        text = "\n".join(extracted_text).strip()

        if not text:

            return None, (
                "No readable text was found. "
                "This may be a scanned/image-only PDF."
            )

        if len(text) < 50:

            return None, (
                "Very little text was extracted. "
                "Please upload a text-based PDF resume."
            )

        return text[:30000], None

    except Exception:

        return None, (
            "The PDF could not be processed. "
            "Please check that it is a valid PDF."
        )


# ============================================================
# SCORE EXTRACTION
# ============================================================

def extract_score(text, labels):

    if not text:
        return 0

    for label in labels:

        pattern = rf"{re.escape(label)}\s*[:\-]?\s*(\d{{1,3}})"

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            score = int(match.group(1))

            return min(max(score, 0), 100)

    return 0


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🤖 AI Career Coach")

    st.write(
        """
        Analyze → Improve → Learn → Build → Prepare
        """
    )

    st.divider()

    if st.session_state.resume_text:

        st.success("Resume loaded")

        word_count = len(
            st.session_state.resume_text.split()
        )

        st.metric(
            "Resume Words",
            word_count
        )

    else:

        st.info(
            "Upload a resume to begin."
        )

    st.divider()

    st.subheader("Target Career")

    role = st.selectbox(

        "Choose a target role",

        [
            "AI Engineer",
            "Machine Learning Engineer",
            "Python Developer",
            "Data Scientist",
            "Software Engineer",
            "Generative AI Engineer",
            "Data Analyst",
            "Other",
        ],
    )

    if role != "Other":

        st.session_state.target_role = role

    st.divider()

    st.caption(
        "Uploaded resumes are processed temporarily "
        "and are not permanently stored by this application."
    )


# ============================================================
# HERO SECTION
# ============================================================

st.markdown(

    """
    <div class="hero">

        <h1>
        AI Resume & Career Coach 🤖📄💼
        </h1>

        <p>
        Analyze your resume. Discover your skill gaps.
        Build your career roadmap.
        </p>

    </div>
    """,

    unsafe_allow_html=True,
)


# ============================================================
# APPLICATION TABS
# ============================================================

tabs = st.tabs(

    [
        "🏠 Home",
        "📄 Resume",
        "🤖 AI Analysis",
        "✍️ Resume Improver",
        "💼 Career Match",
        "🧠 Skill Gap",
        "📚 Roadmap",
        "🚀 Projects",
        "🎤 Interview",
        "📊 Dashboard",
    ]
)


# ============================================================
# HOME
# ============================================================

with tabs[0]:

    st.header(
        "Welcome to AI Resume & Career Coach"
    )

    st.write(
        """
        AI Resume & Career Coach is an AI-powered career
        assistant designed to help students and early-career
        professionals analyze their resumes, discover skill
        gaps, improve resume content and prepare for their
        target careers.
        """
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
            <div class="feature-card">

            <h3>📄 Resume Intelligence</h3>

            <p>
            Analyze resume quality, ATS compatibility,
            missing sections and keywords.
            </p>

            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:

        st.markdown(
            """
            <div class="feature-card">

            <h3>🧠 Skill Gap Analysis</h3>

            <p>
            Identify technical and soft skills
            required for your target career.
            </p>

            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:

        st.markdown(
            """
            <div class="feature-card">

            <h3>🚀 Career Roadmap</h3>

            <p>
            Build a personalized learning roadmap
            based on your existing skills.
            </p>

            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()

    st.subheader(
        "Start Career Analysis 🚀"
    )

    if not st.session_state.resume_text:

        st.info(
            "Go to the 📄 Resume tab and upload your PDF resume."
        )

    else:

        st.success(
            "Your resume is ready for analysis."
        )


# ============================================================
# RESUME UPLOAD
# ============================================================

with tabs[1]:

    st.header(
        "📄 Resume Upload"
    )

    st.write(
        """
        Upload your resume as a PDF.
        The application will extract the text
        for AI analysis.
        """
    )

    uploaded_file = st.file_uploader(

        "Upload Resume PDF",

        type=["pdf"],

        help="Maximum recommended size: 10 MB.",
    )

    if uploaded_file:

        with st.spinner(
            "Extracting resume text..."
        ):

            resume_text, error = extract_resume_text(
                uploaded_file
            )

        if error:

            st.error(error)

        else:

            st.session_state.resume_text = resume_text

            st.success(
                "Resume extracted successfully! ✅"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Words",
                    len(resume_text.split())
                )

            with col2:

                st.metric(
                    "Characters",
                    len(resume_text)
                )

            st.subheader(
                "Resume Preview"
            )

            st.text_area(

                "Extracted Resume Text",

                resume_text[:3000],

                height=300,

                disabled=True,
            )

            if len(resume_text) > 3000:

                st.caption(
                    "Preview limited to the first 3,000 characters."
                )

            st.info(
                "The application does not permanently save "
                "your uploaded resume."
            )


# ============================================================
# AI RESUME ANALYSIS
# ============================================================

with tabs[2]:

    st.header(
        "🤖 AI Resume Analysis"
    )

    if not st.session_state.resume_text:

        st.warning(
            "Please upload a resume first."
        )

    else:

        st.write(
            "Analyze your resume using AI."
        )

        if st.button(
            "Run Complete Resume Analysis",
            type="primary",
        ):

            prompt = f"""

            Analyze the following resume as a professional
            ATS resume reviewer.

            RESUME:

            {st.session_state.resume_text[:30000]}

            Provide the following sections:

            # Overall Resume Score

            Overall Resume Score: [0-100]

            # ATS Friendliness

            ATS Score: [0-100]

            # Strengths

            Identify the strongest aspects.

            # Weaknesses

            Identify important weaknesses.

            # Missing Sections

            Identify missing resume sections.

            # Formatting and Content Issues

            Identify ATS and professional writing problems.

            # Missing Keywords

            Recommend useful keywords.

            # Recommended Skills

            Separate current skills from recommended skills.

            # Professional Summary Improvement

            Explain how the professional summary can be improved.

            # Priority Improvements

            Give the top 5 improvements.

            Do not invent qualifications or experience.

            """

            with st.spinner(
                "AI is analyzing your resume..."
            ):

                result = ask_groq(
                    prompt,
                    max_tokens=4500
                )

            if result:

                st.session_state.analysis = result

                st.session_state.resume_score = extract_score(

                    result,

                    [
                        "Overall Resume Score",
                        "Resume Score",
                    ],
                )

                st.session_state.ats_score = extract_score(

                    result,

                    [
                        "ATS Score",
                        "ATS Friendliness",
                    ],
                )

        if st.session_state.analysis:

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Resume Score",
                    f"{st.session_state.resume_score}/100"
                )

                st.progress(
                    st.session_state.resume_score / 100
                )

            with col2:

                st.metric(
                    "ATS Score",
                    f"{st.session_state.ats_score}/100"
                )

                st.progress(
                    st.session_state.ats_score / 100
                )

            st.divider()

            st.markdown(
                st.session_state.analysis
            )


# ============================================================
# RESUME IMPROVER
# ============================================================

with tabs[3]:

    st.header(
        "✍️ AI Resume Improver"
    )

    if not st.session_state.resume_text:

        st.warning(
            "Please upload a resume first."
        )

    else:

        section = st.selectbox(

            "Choose a resume section",

            [
                "Professional Summary",
                "Career Objective",
                "Skills",
                "Projects",
                "Experience",
                "Education",
            ],
        )

        original = st.text_area(

            "Paste your original section",

            height=180,

            placeholder=(
                "Paste your current resume section here..."
            ),
        )

        target_role = st.text_input(

            "Target role",

            value=st.session_state.target_role,

            placeholder="Example: AI Engineer",
        )

        if st.button(
            "Improve This Section",
            type="primary",
        ):

            if not original.strip():

                st.warning(
                    "Please enter the original section."
                )

            else:

                prompt = f"""

                Improve this resume section.

                SECTION:
                {section}

                TARGET ROLE:
                {target_role}

                ORIGINAL:

                {original}

                Requirements:

                - Make it professional.
                - Make it ATS-friendly.
                - Improve clarity.
                - Keep it concise.
                - Preserve factual information.
                - Do not invent jobs.
                - Do not invent degrees.
                - Do not invent certifications.
                - Do not invent achievements.
                - Do not invent technologies.
                - Return only the improved version.

                """

                with st.spinner(
                    "Improving your resume..."
                ):

                    improved = ask_groq(
                        prompt,
                        max_tokens=1800
                    )

                if improved:

                    col1, col2 = st.columns(2)

                    with col1:

                        st.subheader(
                            "Original Version"
                        )

                        st.text_area(
                            "Original",
                            original,
                            height=280,
                            disabled=True,
                        )

                    with col2:

                        st.subheader(
                            "Improved Version"
                        )

                        st.text_area(
                            "AI Improved",
                            improved,
                            height=280,
                        )


# ============================================================
# CAREER MATCH
# ============================================================

with tabs[4]:

    st.header(
        "💼 Career Match"
    )

    if not st.session_state.resume_text:

        st.warning(
            "Please upload a resume first."
        )

    else:

        target_role = st.text_input(

            "Target job role",

            value=st.session_state.target_role,

            placeholder="Example: Generative AI Engineer",
        )

        st.session_state.target_role = target_role

        if st.button(
            "Analyze Career Match",
            type="primary",
        ):

            if not target_role.strip():

                st.warning(
                    "Please enter a target job role."
                )

            else:

                prompt = f"""

                Compare this resume against the target career.

                TARGET ROLE:
                {target_role}

                RESUME:

                {st.session_state.resume_text[:30000]}

                Provide:

                # Job Match

                Job Match Percentage: [0-100]

                # Matching Skills

                List skills demonstrated in the resume.

                # Missing Skills

                List important missing skills.

                # Recommended Technologies

                Recommend technologies to learn.

                # Recommended Projects

                Recommend relevant portfolio projects.

                # Recommended Certifications

                Recommend useful certification categories.

                # Skills Priority

                Create a priority list.

                Never claim that the user already has
                a skill unless the resume provides evidence.

                """

                with st.spinner(
                    "Calculating career match..."
                ):

                    result = ask_groq(
                        prompt,
                        max_tokens=4000
                    )

                if result:

                    st.session_state.career_match_result = result

                    st.session_state.career_match = extract_score(

                        result,

                        [
                            "Job Match Percentage",
                            "Job Match",
                            "Career Match",
                        ],
                    )

        if st.session_state.career_match_result:

            st.metric(
                "Career Match",
                f"{st.session_state.career_match}/100"
            )

            st.progress(
                st.session_state.career_match / 100
            )

            st.divider()

            st.markdown(
                st.session_state.career_match_result
            )


# ============================================================
# SKILL GAP ANALYZER
# ============================================================

with tabs[5]:

    st.header(
        "🧠 Skill Gap Analyzer"
    )

    if not st.session_state.resume_text:

        st.warning(
            "Please upload a resume first."
        )

    else:

        role = st.text_input(

            "Career target",

            value=st.session_state.target_role,

            placeholder="Example: Machine Learning Engineer",
            key="skill_gap_role",
        )

        if st.button(
            "Analyze Skill Gap",
            type="primary",
        ):

            if not role.strip():

                st.warning(
                    "Enter a target career first."
                )

            else:

                prompt = f"""

                Analyze the skill gap between this resume
                and the target career.

                TARGET CAREER:
                {role}

                RESUME:
                {st.session_state.resume_text[:30000]}

                Create:

                # Current Skills

                Skills already demonstrated.

                # Missing Technical Skills

                Important technical skills missing.

                # Missing Soft Skills

                Important professional skills.

                # Beginner Skills

                Skills to learn at beginner level.

                # Intermediate Skills

                Skills to learn at intermediate level.

                # Advanced Skills

                Advanced skills to learn later.

                # Skill Priority

                Rank skills by importance.

                Do not claim that missing skills already exist.

                """

                with st.spinner(
                    "Analyzing your skill gap..."
                ):

                    result = ask_groq(
                        prompt,
                        max_tokens=4000
                    )

                if result:

                    st.session_state.skill_gap_result = result

        if st.session_state.skill_gap_result:

            st.markdown(
                st.session_state.skill_gap_result
            )


# ============================================================
# PERSONALIZED ROADMAP
# ============================================================

with tabs[6]:

    st.header(
        "📚 Personalized Career Roadmap"
    )

    if not st.session_state.resume_text:

        st.warning(
            "Please upload a resume first."
        )

    else:

        role = st.text_input(

            "Target career for roadmap",

            value=st.session_state.target_role,

            key="roadmap_role",
        )

        duration = st.selectbox(

            "Roadmap duration",

            [
                "3 Months",
                "6 Months",
                "9 Months",
                "12 Months",
            ],
        )

        if st.button(
            "Generate Career Roadmap",
            type="primary",
        ):

            prompt = f"""

            Create a personalized career roadmap.

            TARGET CAREER:
            {role}

            DURATION:
            {duration}

            RESUME:

            {st.session_state.resume_text[:30000]}

            Existing skills must be considered.

            Create a structured roadmap.

            For every month provide:

            - Main learning goals
            - Technical skills
            - Tools
            - Practice tasks
            - Portfolio milestone
            - Suggested outcome

            Example:

            Month 1:
            Python
            Git/GitHub
            Basic SQL

            Month 2:
            Machine Learning
            Data handling

            Month 3:
            Generative AI
            LLM APIs
            RAG

            Customize everything according to the resume.

            Do not assume skills that are not demonstrated.

            """

            with st.spinner(
                "Creating your personalized roadmap..."
            ):

                result = ask_groq(
                    prompt,
                    max_tokens=4500
                )

            if result:

                st.session_state.roadmap_result = result

        if st.session_state.roadmap_result:

            st.markdown(
                st.session_state.roadmap_result
            )


# ============================================================
# PROJECT RECOMMENDATIONS
# ============================================================

with tabs[7]:

    st.header(
        "🚀 Portfolio Project Recommendations"
    )

    if not st.session_state.resume_text:

        st.warning(
            "Please upload a resume first."
        )

    else:

        role = st.text_input(

            "Target career",

            value=st.session_state.target_role,

            key="projects_role",
        )

        number_of_projects = st.slider(

            "Number of project ideas",

            min_value=3,

            max_value=8,

            value=5,
        )

        if st.button(
            "Recommend Projects",
            type="primary",
        ):

            prompt = f"""

            Recommend {number_of_projects} strong portfolio
            projects for this career.

            TARGET CAREER:
            {role}

            RESUME:

            {st.session_state.resume_text[:30000]}

            For every project provide:

            # Project Title

            Difficulty

            Technologies

            What the project demonstrates

            Why it helps the resume

            Suggested GitHub portfolio value

            Make projects realistic for a Computer Science student.

            Avoid generic projects when possible.

            """

            with st.spinner(
                "Generating project recommendations..."
            ):

                result = ask_groq(
                    prompt,
                    max_tokens=4500
                )

            if result:

                st.session_state.projects_result = result

        if st.session_state.projects_result:

            st.markdown(
                st.session_state.projects_result
            )


# ============================================================
# INTERVIEW COACH
# ============================================================

with tabs[8]:

    st.header(
        "🎤 Interview Coach"
    )

    if not st.session_state.resume_text:

        st.warning(
            "Please upload a resume first."
        )

    else:

        role = st.text_input(

            "Interview role",

            value=st.session_state.target_role,

            key="interview_role",
        )

        interview_type = st.multiselect(

            "Question types",

            [
                "Technical",
                "HR",
                "Behavioral",
                "Project-based",
            ],

            default=[
                "Technical",
                "HR",
                "Behavioral",
                "Project-based",
            ],
        )

        if st.button(
            "Generate Interview Questions",
            type="primary",
        ):

            prompt = f"""

            Create an interview preparation set.

            TARGET ROLE:
            {role}

            RESUME:

            {st.session_state.resume_text[:30000]}

            QUESTION TYPES:
            {", ".join(interview_type)}

            Generate:

            - Technical questions
            - HR questions
            - Behavioral questions
            - Project-based questions

            Personalize questions using only information
            that actually appears in the resume.

            Do not invent projects or experience.

            """

            with st.spinner(
                "Preparing interview questions..."
            ):

                result = ask_groq(
                    prompt,
                    max_tokens=4000
                )

            if result:

                st.session_state.interview_questions = result

        if st.session_state.interview_questions:

            st.subheader(
                "Interview Questions"
            )

            st.markdown(
                st.session_state.interview_questions
            )

            st.divider()

            st.subheader(
                "Practice Your Answer"
            )

            selected_question = st.text_input(
                "Question",
                placeholder="Paste an interview question here..."
            )

            answer = st.text_area(
                "Your answer",
                height=200,
                placeholder="Write your answer honestly..."
            )

            if st.button(
                "Get AI Feedback"
            ):

                if not selected_question.strip():

                    st.warning(
                        "Enter an interview question."
                    )

                elif not answer.strip():

                    st.warning(
                        "Enter your answer."
                    )

                else:

                    prompt = f"""

                    Evaluate this interview answer.

                    QUESTION:
                    {selected_question}

                    ANSWER:
                    {answer}

                    Provide:

                    # Feedback

                    # Missing Points

                    # Better Answer Structure

                    # Improvement Suggestions

                    Do not create false experience
                    or encourage the candidate to lie.

                    """

                    with st.spinner(
                        "Reviewing your answer..."
                    ):

                        feedback = ask_groq(
                            prompt,
                            max_tokens=2500
                        )

                    if feedback:

                        st.session_state.interview_feedback = feedback

            if st.session_state.interview_feedback:

                st.subheader(
                    "AI Feedback"
                )

                st.markdown(
                    st.session_state.interview_feedback
                )


# ============================================================
# CAREER DASHBOARD
# ============================================================

with tabs[9]:

    st.header(
        "📊 Career Dashboard"
    )

    st.write(
        "Your current career-readiness overview."
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Resume Score",
            f"{st.session_state.resume_score}/100"
        )

    with col2:

        st.metric(
            "ATS Score",
            f"{st.session_state.ats_score}/100"
        )

    with col3:

        st.metric(
            "Career Match",
            f"{st.session_state.career_match}/100"
        )

    st.divider()

    overall_scores = [
        st.session_state.resume_score,
        st.session_state.ats_score,
        st.session_state.career_match,
    ]

    valid_scores = [
        score
        for score in overall_scores
        if score > 0
    ]

    if valid_scores:

        readiness = int(
            sum(valid_scores) / len(valid_scores)
        )

    else:

        readiness = 0

    st.subheader(
        "Career Readiness"
    )

    if readiness == 0:

        st.info(
            "Upload your resume and run the analyses "
            "to calculate your career readiness."
        )

    else:

        st.metric(
            "Career Readiness Score",
            f"{readiness}/100"
        )

        st.progress(
            readiness / 100
        )

        if readiness >= 80:

            st.success(
                "Strong career readiness. Continue building "
                "projects and preparing for interviews."
            )

        elif readiness >= 60:

            st.info(
                "Good foundation. Focus on the identified "
                "skill gaps and portfolio improvements."
            )

        elif readiness >= 40:

            st.warning(
                "Develop your core skills and strengthen "
                "your resume before applying widely."
            )

        else:

            st.warning(
                "Focus on building foundational skills, "
                "projects and resume quality."
            )

    st.divider()

    st.subheader(
        "Career Summary"
    )

    summary_col1, summary_col2 = st.columns(2)

    with summary_col1:

        st.write(
            f"**Target Career:** "
            f"{st.session_state.target_role or 'Not selected'}"
        )

        st.write(
            f"**Resume Uploaded:** "
            f"{'Yes' if st.session_state.resume_text else 'No'}"
        )

    with summary_col2:

        st.write(
            f"**Resume Analysis:** "
            f"{'Completed' if st.session_state.analysis else 'Not completed'}"
        )

        st.write(
            f"**Career Match:** "
            f"{'Completed' if st.session_state.career_match_result else 'Not completed'}"
        )

    st.divider()

    st.caption(
        "AI recommendations are informational and should be reviewed "
        "by the user before being used in applications."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "AI Resume & Career Coach 🤖 | "
    "Built with Python, Streamlit, Groq API and pypdf"
)
