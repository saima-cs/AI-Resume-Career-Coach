%%writefile app.py

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
# CUSTOM CSS — TEAL + EMERALD AI THEME
# ============================================================

st.markdown(
    """
    <style>

    /* ---------- GLOBAL ---------- */

    .stApp {
        background:
            radial-gradient(
                circle at top right,
                rgba(20, 184, 166, 0.10),
                transparent 35%
            ),
            linear-gradient(
                135deg,
                #f0fdfa 0%,
                #ecfdf5 45%,
                #f8fafc 100%
            );
    }

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }


    /* ---------- SIDEBAR ---------- */

    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #022c22 0%,
            #064e3b 55%,
            #115e59 100%
        );
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    section[data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.20);
    }


    /* ---------- HERO ---------- */

    .hero {
        position: relative;
        overflow: hidden;
        padding: 3rem;
        border-radius: 28px;
        background:
            radial-gradient(
                circle at 85% 20%,
                rgba(45, 212, 191, 0.35),
                transparent 25%
            ),
            linear-gradient(
                135deg,
                #022c22,
                #065f46,
                #0f766e,
                #0891b2
            );
        color: white;
        margin-bottom: 30px;
        box-shadow:
            0 20px 50px rgba(6, 78, 59, 0.25);
    }

    .hero h1 {
        font-size: 3.2rem;
        line-height: 1.1;
        font-weight: 800;
        margin: 0 0 15px 0;
    }

    .hero p {
        font-size: 1.2rem;
        line-height: 1.7;
        margin: 0;
        max-width: 850px;
        opacity: 0.95;
    }

    .hero-badge {
        display: inline-block;
        padding: 7px 14px;
        margin-bottom: 18px;
        border-radius: 50px;
        background: rgba(255,255,255,0.14);
        border: 1px solid rgba(255,255,255,0.25);
        font-size: 0.9rem;
        font-weight: 600;
    }


    /* ---------- SECTION HEADERS ---------- */

    .section-title {
        font-size: 1.8rem;
        font-weight: 800;
        color: #064e3b;
        margin-top: 10px;
        margin-bottom: 6px;
    }

    .section-subtitle {
        color: #64748b;
        margin-bottom: 25px;
    }


    /* ---------- FEATURE CARDS ---------- */

    .feature-card {
        padding: 1.5rem;
        min-height: 190px;
        border-radius: 22px;
        border: 1px solid #ccfbf1;
        background: rgba(255,255,255,0.90);
        box-shadow:
            0 10px 30px rgba(15,118,110,0.08);
        transition: all 0.25s ease;
        margin-bottom: 18px;
    }

    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow:
            0 16px 35px rgba(15,118,110,0.15);
        border-color: #5eead4;
    }

    .feature-icon {
        font-size: 2rem;
        margin-bottom: 10px;
    }

    .feature-card h3 {
        color: #0f766e;
        margin-bottom: 8px;
    }

    .feature-card p {
        color: #475569;
        line-height: 1.6;
    }


    /* ---------- STAT CARDS ---------- */

    .stat-card {
        padding: 1.3rem;
        border-radius: 20px;
        background: white;
        border: 1px solid #ccfbf1;
        box-shadow:
            0 8px 25px rgba(15,118,110,0.08);
        text-align: center;
        margin-bottom: 15px;
    }

    .stat-number {
        font-size: 2rem;
        font-weight: 800;
        color: #0f766e;
    }

    .stat-label {
        color: #64748b;
        font-size: 0.9rem;
    }


    /* ---------- PROJECT CARDS ---------- */

    .project-card {
        padding: 1.5rem;
        border-radius: 22px;
        border: 1px solid #d1fae5;
        background: white;
        margin-bottom: 20px;
        box-shadow:
            0 8px 25px rgba(16,185,129,0.08);
    }


    /* ---------- ROADMAP CARDS ---------- */

    .roadmap-card {
        padding: 1.5rem;
        border-radius: 20px;
        border-left: 6px solid #0f766e;
        background: white;
        margin-bottom: 20px;
        box-shadow:
            0 8px 25px rgba(15,118,110,0.08);
    }


    /* ---------- INFO BOX ---------- */

    .info-card {
        padding: 1.4rem;
        border-radius: 20px;
        background: linear-gradient(
            135deg,
            #ecfdf5,
            #f0fdfa
        );
        border: 1px solid #99f6e4;
        margin-bottom: 20px;
    }


    /* ---------- BUTTONS ---------- */

    .stButton > button {
        border-radius: 12px !important;
        font-weight: 700 !important;
        min-height: 45px;
        transition: all 0.2s ease !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow:
            0 8px 20px rgba(15,118,110,0.18);
    }


    /* ---------- METRICS ---------- */

    [data-testid="stMetric"] {
        background: white;
        padding: 1.25rem;
        border-radius: 20px;
        border: 1px solid #ccfbf1;
        box-shadow:
            0 7px 22px rgba(15,118,110,0.08);
    }


    /* ---------- FILE UPLOADER ---------- */

    [data-testid="stFileUploader"] {
        background: white;
        border: 2px dashed #14b8a6;
        border-radius: 20px;
        padding: 20px;
        box-shadow:
            0 8px 25px rgba(20,184,166,0.08);
    }


    /* ---------- INPUTS ---------- */

    div[data-baseweb="input"] > div,
    div[data-baseweb="select"] > div,
    textarea {
        border-radius: 12px !important;
    }


    /* ---------- TABS ---------- */

    button[data-baseweb="tab"] {
        font-weight: 600;
    }


    /* ---------- PROGRESS ---------- */

    [data-testid="stProgressBar"] {
        margin-top: 8px;
        margin-bottom: 12px;
    }


    /* ---------- FOOTER ---------- */

    .footer {
        text-align: center;
        padding: 25px;
        color: #64748b;
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

        if not api_key or not api_key.strip():
            return None

        return Groq(api_key=api_key)

    except Exception:
        return None


def ask_groq(prompt, max_tokens=3500):

    client = get_groq_client()

    if client is None:
        st.error(
            "🔐 Groq API key is not available. "
            "Please add GROQ_API_KEY to Streamlit Secrets."
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
8. Never encourage lying during interviews.
9. Give practical advice.
10. Use professional formatting.
11. Be realistic for a Computer Science student.
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

        if "401" in error_text or "authentication" in error_text.lower():
            st.warning(
                "🔑 Your Groq API key may be invalid or expired."
            )

        elif "429" in error_text:
            st.warning(
                "⏳ Groq rate limit or usage limit reached. "
                "Please wait and try again."
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

            score = int(match.group(1))

            return min(max(score, 0), 100)

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
            <div style="font-size:3rem;">🤖</div>
            <h2 style="margin:0;">AI Career Coach</h2>
            <p style="opacity:0.8;">
                Your AI-powered career companion
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    if st.session_state.resume_text:

        st.success("✅ Resume Loaded")

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

    st.subheader("🎯 Target Career")

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

    if role == "Other":

        custom_role = st.text_input(
            "Enter your target role",
            value=st.session_state.target_role,
        )

        if custom_role.strip():
            st.session_state.target_role = custom_role

    st.divider()

    st.markdown(
        """
        <div style="
            padding:12px;
            border-radius:12px;
            background:rgba(255,255,255,0.08);
            font-size:0.85rem;
        ">
        🔒 Your uploaded resume is processed temporarily
        and is not permanently stored by this application.
        </div>
        """,
        unsafe_allow_html=True,
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
# APPLICATION TABS
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
        """
        <div class="section-subtitle">
        One workspace to analyze, improve, learn, build and prepare
        for your future career.
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">📄</div>
                <h3>Resume Intelligence</h3>
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
                <div class="feature-icon">🧠</div>
                <h3>Skill Gap Analysis</h3>
                <p>
                Discover the technical and professional skills
                needed for your target career.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:

        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">🚀</div>
                <h3>Career Roadmap</h3>
                <p>
                Get a personalized learning and portfolio roadmap
                based on your current profile.
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
                <div class="feature-icon">💼</div>
                <h3>Career Match</h3>
                <p>
                Compare your current profile with your desired
                job role and identify missing skills.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col5:

        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">🚀</div>
                <h3>Portfolio Builder</h3>
                <p>
                Discover realistic AI and software projects
                that can strengthen your GitHub portfolio.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col6:

        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">🎤</div>
                <h3>Interview Coach</h3>
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
            <h3>🚀 Start Your Career Analysis</h3>
            <p>
            Upload your PDF resume from the Resume page,
            select your target career and start your personalized analysis.
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
        '<div class="section-subtitle">Upload your PDF resume and let AI extract the information.</div>',
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(
        "📤 Upload Resume PDF",
        type=["pdf"],
        help="Maximum recommended size: 10 MB.",
    )

    if uploaded_file:

        with st.spinner("🔍 Extracting resume information..."):

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
                st.metric(
                    "📄 Pages",
                    min(len(PdfReader(
                        BytesIO(uploaded_file.getvalue())
                    ).pages), 25),
                )

            st.divider()

            st.subheader("👀 Resume Preview")

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
        '<div class="section-subtitle">Get an AI-powered review of your resume.</div>',
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

Provide these sections:

# Overall Resume Score
Overall Resume Score: [0-100]

# ATS Friendliness
ATS Score: [0-100]

# Strengths
Identify the strongest aspects of the resume.

# Weaknesses
Identify important weaknesses.

# Missing Sections
Identify important missing resume sections.

# Formatting and Content Issues
Identify ATS and professional writing problems.

# Missing Keywords
Recommend useful keywords for the target career.

# Recommended Skills
Clearly separate:
- Current skills demonstrated by the resume
- Recommended skills to learn

# Professional Summary Improvement
Explain how the professional summary can be improved.

# Priority Improvements
Give the top 5 improvements in priority order.

Never invent qualifications, experience, education, certifications,
projects or achievements.
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
        '<div class="section-subtitle">Transform your existing content into clearer, ATS-friendly resume language.</div>',
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
            placeholder="Paste your current resume section here...",
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
- Do not add unsupported claims.
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
        '<div class="section-subtitle">Discover how closely your current profile matches your target career.</div>',
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
# SKILL GAP
# ============================================================

with tabs[5]:

    st.markdown(
        '<div class="section-title">🧠 Skill Gap Analyzer</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-subtitle">Understand what you know, what you need and what to learn next.</div>',
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
                    "Enter a career target first."
                )

            else:

                prompt = f"""
Analyze the skill gap between this resume and the target career.

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
Important professional skills missing.

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
        '<div class="section-subtitle">Build a structured learning and portfolio plan around your target career.</div>',
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
        '<div class="section-subtitle">Find practical projects that demonstrate career-relevant skills.</div>',
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
that actually appears in the resume.

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
                placeholder="Paste an interview question here...",
            )

            answer = st.text_area(
                "Your Answer",
                height=220,
                placeholder="Write your answer honestly...",
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
# CAREER DASHBOARD
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
                "👍 Good foundation. Focus on the identified "
                "skill gaps and portfolio improvements."
            )

        elif readiness >= 40:

            st.warning(
                "📚 Keep developing your core skills and "
                "strengthen your resume."
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

        st.markdown(
            f"""
            **🎯 Target Career**

            {st.session_state.target_role or "Not selected"}

            **📄 Resume Uploaded**

            {"✅ Yes" if st.session_state.resume_text else "❌ No"}
            """
        )

    with summary_col2:

        st.markdown(
            f"""
            **🤖 Resume Analysis**

            {"✅ Completed" if st.session_state.analysis else "⏳ Not completed"}

            **💼 Career Match**

            {"✅ Completed" if st.session_state.career_match_result else "⏳ Not completed"}
            """
        )

    st.divider()

    st.subheader(
        "✨ Your Career Journey"
    )

    journey_col1, journey_col2, journey_col3, journey_col4 = st.columns(4)

    with journey_col1:
        st.markdown(
            """
            <div class="stat-card">
                <div class="stat-number">01</div>
                <div class="stat-label">Analyze</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with journey_col2:
        st.markdown(
            """
            <div class="stat-card">
                <div class="stat-number">02</div>
                <div class="stat-label">Improve</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with journey_col3:
        st.markdown(
            """
            <div class="stat-card">
                <div class="stat-number">03</div>
                <div class="stat-label">Learn & Build</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with journey_col4:
        st.markdown(
            """
            <div class="stat-card">
                <div class="stat-number">04</div>
                <div class="stat-label">Prepare</div>
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
        <br>
        Built with Python • Streamlit • Groq AI • pypdf
        <br><br>
        Analyze • Improve • Learn • Build • Prepare 🚀
    </div>
    """,
    unsafe_allow_html=True,
)
