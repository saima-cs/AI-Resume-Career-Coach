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
# CUSTOM CSS — HIGH CONTRAST BLUE & WHITE THEME
# ============================================================

st.markdown(
    """
    <style>

    /* ======================================================
       MAIN APP
       ====================================================== */

    .stApp {
        background-color: #F5F9FF;
    }

    .main .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }


    /* ======================================================
       SIDEBAR
       ====================================================== */

    section[data-testid="stSidebar"] {
        background-color: #0B1F3A;
    }

    section[data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }

    section[data-testid="stSidebar"] hr {
        border-color: #31527D;
    }


    /* ======================================================
       HERO
       ====================================================== */

    .hero {
        background: linear-gradient(
            135deg,
            #0B1F3A 0%,
            #123E73 50%,
            #1769AA 100%
        );

        color: white;

        padding: 3rem;

        border-radius: 24px;

        margin-bottom: 30px;

        box-shadow:
            0 12px 35px rgba(11, 31, 58, 0.25);
    }

    .hero-badge {
        display: inline-block;

        background-color: #FFFFFF;

        color: #0B4F8A;

        padding: 7px 14px;

        border-radius: 50px;

        font-size: 0.85rem;

        font-weight: 800;

        margin-bottom: 18px;
    }

    .hero h1 {
        color: #FFFFFF;

        font-size: 3.1rem;

        font-weight: 800;

        line-height: 1.15;

        margin-bottom: 15px;
    }

    .hero p {
        color: #E8F3FF;

        font-size: 1.15rem;

        line-height: 1.7;

        max-width: 900px;
    }


    /* ======================================================
       SECTION TITLES
       ====================================================== */

    .section-title {
        color: #0B3A68;

        font-size: 1.9rem;

        font-weight: 800;

        margin-top: 10px;

        margin-bottom: 5px;
    }

    .section-subtitle {
        color: #4B6380;

        font-size: 1rem;

        margin-bottom: 25px;
    }


    /* ======================================================
       FEATURE CARDS
       ====================================================== */

    .feature-card {
        background-color: #FFFFFF;

        border: 2px solid #D7E7F7;

        border-radius: 18px;

        padding: 1.5rem;

        min-height: 190px;

        margin-bottom: 20px;

        box-shadow:
            0 6px 20px rgba(11, 63, 105, 0.08);
    }

    .feature-card:hover {
        border-color: #2589D9;

        box-shadow:
            0 10px 28px rgba(11, 63, 105, 0.15);
    }

    .feature-icon {
        font-size: 2.2rem;

        margin-bottom: 10px;
    }

    .feature-card h3 {
        color: #0B4F8A;

        font-size: 1.25rem;

        margin-bottom: 10px;
    }

    .feature-card p {
        color: #455A70;

        line-height: 1.6;
    }


    /* ======================================================
       INFORMATION CARDS
       ====================================================== */

    .info-card {
        background-color: #EAF4FF;

        border: 2px solid #B8D8F5;

        border-radius: 18px;

        padding: 1.4rem;

        margin: 20px 0;
    }

    .info-card h3 {
        color: #0B4F8A;
    }

    .info-card p {
        color: #334E68;
    }


    /* ======================================================
       PROJECT / ROADMAP CARDS
       ====================================================== */

    .project-card {
        background-color: #FFFFFF;

        border: 2px solid #D7E7F7;

        border-radius: 18px;

        padding: 1.5rem;

        margin-bottom: 20px;

        box-shadow:
            0 6px 20px rgba(11, 63, 105, 0.08);
    }

    .roadmap-card {
        background-color: #FFFFFF;

        border-left: 6px solid #1769AA;

        border-top: 1px solid #D7E7F7;

        border-right: 1px solid #D7E7F7;

        border-bottom: 1px solid #D7E7F7;

        border-radius: 15px;

        padding: 1.5rem;

        margin-bottom: 20px;
    }


    /* ======================================================
       METRICS
       ====================================================== */

    [data-testid="stMetric"] {
        background-color: #FFFFFF;

        border: 2px solid #D7E7F7;

        border-radius: 18px;

        padding: 1.2rem;

        box-shadow:
            0 6px 20px rgba(11, 63, 105, 0.08);
    }

    [data-testid="stMetricLabel"] {
        color: #49647E !important;
    }

    [data-testid="stMetricValue"] {
        color: #0B4F8A !important;
        font-weight: 800;
    }


    /* ======================================================
       BUTTONS
       ====================================================== */

    .stButton > button {
        background-color: #1769AA;

        color: #FFFFFF;

        border: none;

        border-radius: 10px;

        font-weight: 700;

        min-height: 45px;

        padding: 0.6rem 1.2rem;
    }

    .stButton > button:hover {
        background-color: #0B4F8A;

        color: #FFFFFF;

        border: none;
    }


    /* ======================================================
       INPUT BOXES
       ====================================================== */

    div[data-baseweb="input"] > div {
        background-color: #FFFFFF !important;

        border: 1px solid #AFC9E2 !important;

        border-radius: 10px !important;
    }

    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;

        border: 1px solid #AFC9E2 !important;

        border-radius: 10px !important;
    }

    textarea {
        background-color: #FFFFFF !important;

        border: 1px solid #AFC9E2 !important;

        border-radius: 10px !important;
    }


    /* ======================================================
       FILE UPLOADER
       ====================================================== */

    [data-testid="stFileUploader"] {
        background-color: #FFFFFF;

        border: 2px dashed #2589D9;

        border-radius: 18px;

        padding: 20px;

        box-shadow:
            0 6px 20px rgba(37, 137, 217, 0.10);
    }


    /* ======================================================
       PROGRESS BAR
       ====================================================== */

    [data-testid="stProgressBar"] {
        margin-top: 8px;

        margin-bottom: 15px;
    }


    /* ======================================================
       TABS
       ====================================================== */

    button[data-baseweb="tab"] {
        color: #24415F !important;

        font-weight: 700;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #1769AA !important;
    }


    /* ======================================================
       FOOTER
       ====================================================== */

    .footer {
        text-align: center;

        color: #60758A;

        padding: 25px;

        font-size: 0.9rem;
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
    "target_role": "AI Engineer",
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

        st.error(
            "🔐 Groq API key is not configured. "
            "Please add GROQ_API_KEY in Streamlit Secrets."
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
8. Never encourage lying.
9. Give practical advice.
10. Use professional formatting.
11. Make recommendations realistic for a Computer Science student.
12. Prioritize actionable recommendations.
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

        error_text = str(error)

        st.error(
            "⚠️ The Groq AI request failed."
        )

        if (
            "401" in error_text
            or "authentication" in error_text.lower()
        ):

            st.warning(
                "🔑 Your Groq API key may be invalid or expired."
            )

        elif "429" in error_text:

            st.warning(
                "⏳ Groq rate limit or usage limit reached."
            )

        elif "model" in error_text.lower():

            st.warning(
                "🤖 There may be an issue with the selected Groq model."
            )

        else:

            st.warning(
                "Please check your Streamlit Secrets and Groq configuration."
            )

        return None


# ============================================================
# PDF EXTRACTION
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

        reader = PdfReader(
            BytesIO(file_bytes)
        )

        if len(reader.pages) == 0:

            return None, (
                "The PDF does not contain any pages."
            )

        max_pages = 25

        pages = reader.pages[:max_pages]

        extracted_text = []

        for page in pages:

            try:

                text = page.extract_text() or ""

                extracted_text.append(text)

            except Exception:

                extracted_text.append("")

        text = "\n".join(
            extracted_text
        ).strip()

        if not text:

            return None, (
                "No readable text was found. "
                "This may be a scanned or image-only PDF."
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

        pattern = (
            rf"{re.escape(label)}"
            rf"\s*[:\-]?\s*"
            rf"(\d{{1,3}})"
        )

        match = re.search(
            pattern,
            text,
            re.IGNORECASE,
        )

        if match:

            score = int(
                match.group(1)
            )

            return min(
                max(score, 0),
                100,
            )

    return 0


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            text-align:center;
            padding:10px 0 20px 0;
        ">

            <div style="
                font-size:3rem;
            ">
                🤖
            </div>

            <h2>
                AI Career Coach
            </h2>

            <p>
                Your AI-powered career companion
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    if st.session_state.resume_text:

        st.success(
            "✅ Resume Loaded"
        )

        word_count = len(
            st.session_state.resume_text.split()
        )

        st.metric(
            "Resume Words",
            word_count,
        )

    else:

        st.info(
            "📄 Upload a resume to begin."
        )

    st.divider()

    st.subheader(
        "🎯 Target Career"
    )

    role = st.selectbox(

        "Choose your target role",

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

        index=0,
    )

    if role != "Other":

        st.session_state.target_role = role

    else:

        custom_role = st.text_input(
            "Enter your target role",
            value=st.session_state.target_role,
        )

        if custom_role.strip():

            st.session_state.target_role = custom_role

    st.divider()

    st.caption(
        "🔒 Uploaded resumes are processed temporarily "
        "and are not permanently stored by this application."
    )


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero">

        <div class="hero-badge">
            ✨ AI-POWERED CAREER INTELLIGENCE
        </div>

        <h1>
            AI Resume & Career Coach 🤖
        </h1>

        <p>
            Analyze your resume, improve your professional profile,
            discover your skill gaps, build a personalized roadmap,
            create stronger portfolio projects, and prepare for interviews.
        </p>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# TABS
# ============================================================

tabs = st.tabs(
    [
        "🏠 Home",
        "📄 Resume",
        "🤖 AI Analysis",
        "✍️ Improver",
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

    st.markdown(
        '<div class="section-title">Welcome to your AI Career Hub 👋</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-subtitle">Analyze • Improve • Learn • Build • Prepare</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
            <div class="feature-card">

                <div class="feature-icon">
                    📄
                </div>

                <h3>
                    Resume Intelligence
                </h3>

                <p>
                    Analyze resume quality, ATS compatibility,
                    missing sections, keywords and content issues.
                </p>

            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:

        st.markdown(
            """
            <div class="feature-card">

                <div class="feature-icon">
                    🧠
                </div>

                <h3>
                    Skill Gap Analysis
                </h3>

                <p>
                    Discover technical and professional skills
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

                <div class="feature-icon">
                    🚀
                </div>

                <h3>
                    Career Roadmap
                </h3>

                <p>
                    Build a personalized learning roadmap
                    based on your current skills.
                </p>

            </div>
            """,
            unsafe_allow_html=True,
        )

    col4, col5, col6 = st.columns(3)

    with col4:

        st.markdown(
            """
            <div class="feature-card">

                <div class="feature-icon">
                    💼
                </div>

                <h3>
                    Career Match
                </h3>

                <p>
                    Compare your profile with your desired
                    career and identify missing skills.
                </p>

            </div>
            """,
            unsafe_allow_html=True,
        )

    with col5:

        st.markdown(
            """
            <div class="feature-card">

                <div class="feature-icon">
                    🚀
                </div>

                <h3>
                    Portfolio Projects
                </h3>

                <p>
                    Discover practical projects that can
                    strengthen your GitHub portfolio.
                </p>

            </div>
            """,
            unsafe_allow_html=True,
        )

    with col6:

        st.markdown(
            """
            <div class="feature-card">

                <div class="feature-icon">
                    🎤
                </div>

                <h3>
                    Interview Coach
                </h3>

                <p>
                    Practice technical, HR, behavioral and
                    project-based interview questions.
                </p>

            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="info-card">

            <h3>
                🚀 Start Your Career Analysis
            </h3>

            <p>
                Upload your PDF resume, choose your target career
                and start your personalized AI analysis.
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.resume_text:

        st.success(
            "✅ Your resume is ready. Go to AI Analysis to begin."
        )

    else:

        st.info(
            "📄 Start by uploading your resume from the Resume tab."
        )


# ============================================================
# RESUME UPLOAD
# ============================================================

with tabs[1]:

    st.markdown(
        '<div class="section-title">📄 Resume Center</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-subtitle">Upload your PDF resume and extract its content for AI analysis.</div>',
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(

        "📤 Upload Resume PDF",

        type=["pdf"],

        help="Maximum recommended size: 10 MB.",
    )

    if uploaded_file:

        with st.spinner(
            "🔍 Extracting resume information..."
        ):

            resume_text, error = extract_resume_text(
                uploaded_file
            )

        if error:

            st.error(error)

        else:

            st.session_state.resume_text = resume_text

            st.success(
                "🎉 Resume extracted successfully!"
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "📝 Words",
                    len(resume_text.split()),
                )

            with col2:

                st.metric(
                    "🔤 Characters",
                    len(resume_text),
                )

            with col3:

                reader = PdfReader(
                    BytesIO(
                        uploaded_file.getvalue()
                    )
                )

                st.metric(
                    "📄 Pages",
                    min(len(reader.pages), 25),
                )

            st.divider()

            st.subheader(
                "👀 Resume Preview"
            )

            st.text_area(

                "Extracted Resume Text",

                resume_text[:5000],

                height=350,

                disabled=True,
            )

            if len(resume_text) > 5000:

                st.caption(
                    "Preview limited to the first 5,000 characters."
                )

            st.info(
                "🔒 Your resume is processed temporarily "
                "and is not permanently stored by this application."
            )


# ============================================================
# AI RESUME ANALYSIS
# ============================================================

with tabs[2]:

    st.markdown(
        '<div class="section-title">🤖 AI Resume Analysis</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-subtitle">Get a professional AI-powered review of your resume.</div>',
        unsafe_allow_html=True,
    )

    if not st.session_state.resume_text:

        st.warning(
            "📄 Please upload a resume first."
        )

    else:

        if st.button(
            "🚀 Run Complete Resume Analysis",
            type="primary",
            use_container_width=True,
        ):

            prompt = f"""
Analyze the following resume as a professional ATS resume reviewer.

RESUME:
{st.session_state.resume_text[:30000]}

Provide:

# Overall Resume Score

Overall Resume Score: [0-100]

# ATS Friendliness

ATS Score: [0-100]

# Strengths

Identify the strongest aspects.

# Weaknesses

Identify important weaknesses.

# Missing Sections

Identify missing or weak resume sections.

# Formatting and Content Issues

Identify ATS and professional writing problems.

# Missing Keywords

Recommend useful keywords.

# Recommended Skills

Clearly separate current skills from recommended skills.

# Professional Summary Improvement

Explain how the professional summary can be improved.

# Priority Improvements

Give the top 5 improvements.

Do not invent qualifications, jobs, degrees,
certifications, projects or achievements.
"""

            with st.spinner(
                "🧠 AI is analyzing your resume..."
            ):

                result = ask_groq(
                    prompt,
                    max_tokens=4500,
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

            st.divider()

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "📄 Resume Score",
                    f"{st.session_state.resume_score}/100",
                )

                st.progress(
                    st.session_state.resume_score / 100
                )

            with col2:

                st.metric(
                    "🎯 ATS Score",
                    f"{st.session_state.ats_score}/100",
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

    st.markdown(
        '<div class="section-title">✍️ AI Resume Improver</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-subtitle">Improve your resume content without inventing information.</div>',
        unsafe_allow_html=True,
    )

    if not st.session_state.resume_text:

        st.warning(
            "📄 Please upload a resume first."
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

            "📝 Original Section",

            height=200,

            placeholder=(
                "Paste your current resume section here..."
            ),
        )

        target_role = st.text_input(

            "🎯 Target Role",

            value=st.session_state.target_role,
        )

        if st.button(
            "✨ Improve This Section",
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
                    "✍️ Improving your resume..."
                ):

                    improved = ask_groq(
                        prompt,
                        max_tokens=1800,
                    )

                if improved:

                    col1, col2 = st.columns(2)

                    with col1:

                        st.subheader(
                            "📌 Original"
                        )

                        st.text_area(
                            "Original Version",
                            original,
                            height=300,
                            disabled=True,
                        )

                    with col2:

                        st.subheader(
                            "✨ AI Improved"
                        )

                        st.text_area(
                            "Improved Version",
                            improved,
                            height=300,
                        )


# ============================================================
# CAREER MATCH
# ============================================================

with tabs[4]:

    st.markdown(
        '<div class="section-title">💼 Career Match</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-subtitle">See how closely your profile matches your target career.</div>',
        unsafe_allow_html=True,
    )

    if not st.session_state.resume_text:

        st.warning(
            "📄 Please upload a resume first."
        )

    else:

        target_role = st.text_input(

            "🎯 Target Job Role",

            value=st.session_state.target_role,

            placeholder="Example: Generative AI Engineer",
        )

        st.session_state.target_role = target_role

        if st.button(
            "🎯 Analyze Career Match",
            type="primary",
            use_container_width=True,
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

Never claim that the user already has a skill
unless the resume provides evidence.
"""

                with st.spinner(
                    "🔍 Calculating career match..."
                ):

                    result = ask_groq(
                        prompt,
                        max_tokens=4000,
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

            st.divider()

            st.metric(
                "🎯 Career Match",
                f"{st.session_state.career_match}/100",
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

    st.markdown(
        '<div class="section-title">🧠 Skill Gap Analyzer</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-subtitle">Discover what you know and what you should learn next.</div>',
        unsafe_allow_html=True,
    )

    if not st.session_state.resume_text:

        st.warning(
            "📄 Please upload a resume first."
        )

    else:

        role = st.text_input(

            "🎯 Career Target",

            value=st.session_state.target_role,

            placeholder="Example: Machine Learning Engineer",

            key="skill_gap_role",
        )

        if st.button(
            "🧠 Analyze Skill Gap",
            type="primary",
            use_container_width=True,
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
                    "🧠 Analyzing your skill gap..."
                ):

                    result = ask_groq(
                        prompt,
                        max_tokens=4000,
                    )

                if result:

                    st.session_state.skill_gap_result = result

        if st.session_state.skill_gap_result:

            st.divider()

            st.markdown(
                st.session_state.skill_gap_result
            )


# ============================================================
# PERSONALIZED ROADMAP
# ============================================================

with tabs[6]:

    st.markdown(
        '<div class="section-title">📚 Personalized Career Roadmap</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-subtitle">Create a structured learning and portfolio plan.</div>',
        unsafe_allow_html=True,
    )

    if not st.session_state.resume_text:

        st.warning(
            "📄 Please upload a resume first."
        )

    else:

        role = st.text_input(

            "🎯 Target Career",

            value=st.session_state.target_role,

            key="roadmap_role",
        )

        duration = st.selectbox(

            "⏱️ Roadmap Duration",

            [
                "3 Months",
                "6 Months",
                "9 Months",
                "12 Months",
            ],
        )

        if st.button(
            "🚀 Generate Career Roadmap",
            type="primary",
            use_container_width=True,
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

For every month provide:

- Main learning goals
- Technical skills
- Tools
- Practice tasks
- Portfolio milestone
- Suggested outcome

Customize everything according to the resume.

Do not assume skills that are not demonstrated.
"""

            with st.spinner(
                "📚 Creating your personalized roadmap..."
            ):

                result = ask_groq(
                    prompt,
                    max_tokens=4500,
                )

            if result:

                st.session_state.roadmap_result = result

        if st.session_state.roadmap_result:

            st.divider()

            st.markdown(
                st.session_state.roadmap_result
            )


# ============================================================
# PROJECT RECOMMENDATIONS
# ============================================================

with tabs[7]:

    st.markdown(
        '<div class="section-title">🚀 Portfolio Project Recommendations</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-subtitle">Find realistic projects that strengthen your technical portfolio.</div>',
        unsafe_allow_html=True,
    )

    if not st.session_state.resume_text:

        st.warning(
            "📄 Please upload a resume first."
        )

    else:

        role = st.text_input(

            "🎯 Target Career",

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
            "🚀 Recommend Projects",
            type="primary",
            use_container_width=True,
        ):

            prompt = f"""
Recommend {number_of_projects} strong portfolio projects.

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
                "🚀 Generating project recommendations..."
            ):

                result = ask_groq(
                    prompt,
                    max_tokens=4500,
                )

            if result:

                st.session_state.projects_result = result

        if st.session_state.projects_result:

            st.divider()

            st.markdown(
                st.session_state.projects_result
            )


# ============================================================
# INTERVIEW COACH
# ============================================================

with tabs[8]:

    st.markdown(
        '<div class="section-title">🎤 AI Interview Coach</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-subtitle">Practice interviews and receive structured AI feedback.</div>',
        unsafe_allow_html=True,
    )

    if not st.session_state.resume_text:

        st.warning(
            "📄 Please upload a resume first."
        )

    else:

        role = st.text_input(

            "🎯 Interview Role",

            value=st.session_state.target_role,

            key="interview_role",
        )

        interview_type = st.multiselect(

            "Question Types",

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
            "🎤 Generate Interview Questions",
            type="primary",
            use_container_width=True,
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
that appears in the resume.

Do not invent projects or experience.
"""

            with st.spinner(
                "🎤 Preparing interview questions..."
            ):

                result = ask_groq(
                    prompt,
                    max_tokens=4000,
                )

            if result:

                st.session_state.interview_questions = result

        if st.session_state.interview_questions:

            st.divider()

            st.subheader(
                "❓ Interview Questions"
            )

            st.markdown(
                st.session_state.interview_questions
            )

            st.divider()

            st.subheader(
                "📝 Practice Your Answer"
            )

            selected_question = st.text_input(

                "Interview Question",

                placeholder=(
                    "Paste an interview question here..."
                ),
            )

            answer = st.text_area(

                "Your Answer",

                height=220,

                placeholder=(
                    "Write your answer honestly..."
                ),
            )

            if st.button(
                "✨ Get AI Feedback",
                type="primary",
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
                        "🧠 Reviewing your answer..."
                    ):

                        feedback = ask_groq(
                            prompt,
                            max_tokens=2500,
                        )

                    if feedback:

                        st.session_state.interview_feedback = feedback

            if st.session_state.interview_feedback:

                st.divider()

                st.subheader(
                    "💡 AI Feedback"
                )

                st.markdown(
                    st.session_state.interview_feedback
                )


# ============================================================
# DASHBOARD
# ============================================================

with tabs[9]:

    st.markdown(
        '<div class="section-title">📊 Career Dashboard</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-subtitle">Track your current career-readiness progress.</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "📄 Resume Score",
            f"{st.session_state.resume_score}/100",
        )

    with col2:

        st.metric(
            "🎯 ATS Score",
            f"{st.session_state.ats_score}/100",
        )

    with col3:

        st.metric(
            "💼 Career Match",
            f"{st.session_state.career_match}/100",
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
        "🚀 Career Readiness"
    )

    if readiness == 0:

        st.info(
            "Upload your resume and run the analyses "
            "to calculate your career readiness."
        )

    else:

        st.metric(
            "Career Readiness Score",
            f"{readiness}/100",
        )

        st.progress(
            readiness / 100
        )

        if readiness >= 80:

            st.success(
                "🌟 Strong career readiness! "
                "Continue building projects and preparing for interviews."
            )

        elif readiness >= 60:

            st.info(
                "👍 Good foundation. Focus on skill gaps "
                "and portfolio improvements."
            )

        elif readiness >= 40:

            st.warning(
                "📚 Continue developing your core skills "
                "and strengthening your resume."
            )

        else:

            st.warning(
                "🌱 Focus on foundational skills, projects "
                "and resume quality."
            )

    st.divider()

    st.subheader(
        "📋 Career Summary"
    )

    summary_col1, summary_col2 = st.columns(2)

    with summary_col1:

        st.write(
            f"**🎯 Target Career:** "
            f"{st.session_state.target_role or 'Not selected'}"
        )

        st.write(
            f"**📄 Resume Uploaded:** "
            f"{'Yes ✅' if st.session_state.resume_text else 'No ❌'}"
        )

    with summary_col2:

        st.write(
            f"**🤖 Resume Analysis:** "
            f"{'Completed ✅' if st.session_state.analysis else 'Not completed ⏳'}"
        )

        st.write(
            f"**💼 Career Match:** "
            f"{'Completed ✅' if st.session_state.career_match_result else 'Not completed ⏳'}"
        )

    st.divider()

    st.subheader(
        "✨ Your Career Journey"
    )

    journey_col1, journey_col2, journey_col3, journey_col4 = st.columns(4)

    with journey_col1:

        st.markdown(
            """
            <div class="feature-card"
                 style="min-height:120px;text-align:center;">

                <div class="feature-icon">
                    01
                </div>

                <h3>
                    Analyze
                </h3>

            </div>
            """,
            unsafe_allow_html=True,
        )

    with journey_col2:

        st.markdown(
            """
            <div class="feature-card"
                 style="min-height:120px;text-align:center;">

                <div class="feature-icon">
                    02
                </div>

                <h3>
                    Improve
                </h3>

            </div>
            """,
            unsafe_allow_html=True,
        )

    with journey_col3:

        st.markdown(
            """
            <div class="feature-card"
                 style="min-height:120px;text-align:center;">

                <div class="feature-icon">
                    03
                </div>

                <h3>
                    Learn & Build
                </h3>

            </div>
            """,
            unsafe_allow_html=True,
        )

    with journey_col4:

        st.markdown(
            """
            <div class="feature-card"
                 style="min-height:120px;text-align:center;">

                <div class="feature-icon">
                    04
                </div>

                <h3>
                    Prepare
                </h3>

            </div>
            """,
            unsafe_allow_html=True,
        )

    st.caption(
        "AI recommendations are informational and should be reviewed "
        "before being used in applications."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <div class="footer">

        🤖 <b>AI Resume & Career Coach</b>

        <br><br>

        Built with Python • Streamlit • Groq AI • pypdf

        <br>

        Analyze • Improve • Learn • Build • Prepare 🚀

    </div>
    """,
    unsafe_allow_html=True,
)
    
