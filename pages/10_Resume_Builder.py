import streamlit as st
import sys, os
import base64

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.auth import require_login, get_user
from utils.resume_builder import build_resume_pdf, validate_resume_data
from components.navbar import show_navbar

st.set_page_config(page_title="Resume Builder · SkillGap", page_icon="📝", layout="wide", initial_sidebar_state="collapsed")
require_login()

db_user = get_user(st.session_state.email)
theme = db_user.get("theme", "dark")
is_light = theme == "light"

# ── Helper to prevent Markdown from treating indented HTML as code blocks ───
def _clean_html(html_str: str) -> str:
    return "".join(line.strip() for line in html_str.splitlines() if line.strip())

# ── Base Styles ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
#MainMenu,footer,header,[data-testid="stToolbar"],[data-testid="stSidebarNav"],
[data-testid="stSidebar"],[data-testid="collapsedControl"],section[data-testid="stSidebar"],
.stDeployButton,[class*="viewerBadge"],[class*="toolbar"]
{display:none!important;visibility:hidden!important;}

html,body{margin:0!important;padding:0!important;}

.block-container {
    padding-top: 0 !important;
    padding-bottom: 3.5rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    max-width: 1240px !important;
    margin: 0 auto !important;
}

div[data-testid="stHorizontalBlock"]:first-of-type {
    margin-left: -2rem !important;
    margin-right: -2rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}

div[data-testid="stButton"] button {
    font-weight: 700 !important;
    border-radius: 10px !important;
}

div[data-testid="stButton"] button[kind="primary"],
div[data-testid="stDownloadButton"] button[kind="primary"] {
    background: #333F63 !important;
    color: #FFFFF0 !important;
    border: 1px solid rgba(255,255,240,0.22) !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.25) !important;
}

div[data-testid="stButton"] button[kind="primary"]:hover,
div[data-testid="stDownloadButton"] button[kind="primary"]:hover {
    filter: brightness(1.15);
}

.rb-card {
    background: rgba(0, 0, 0, 0.24);
    border: 1px solid rgba(255, 255, 240, 0.14);
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.6rem;
}

.rb-section-header {
    display: flex;
    align-items: center;
    gap: 0.65rem;
    margin-bottom: 1.1rem;
}

.rb-section-icon {
    font-size: 1.35rem;
}

.rb-section-title {
    font-size: 1.05rem;
    font-weight: 800;
    letter-spacing: 0.2px;
}

.rb-section-sub {
    font-size: 0.78rem;
    opacity: 0.7;
    margin-top: 1px;
}

.rb-badge {
    color: #ffffff !important;
    padding: 3px 9px !important;
    border-radius: 12px !important;
    font-size: 0.68rem !important;
    font-weight: 800 !important;
    letter-spacing: 0.5px !important;
    display: inline-block !important;
    box-shadow: 0 2px 6px rgba(0,0,0,0.2) !important;
}

div[data-testid="stMarkdownContainer"] .rb-badge,
div[data-testid="stMarkdownContainer"] span.rb-badge {
    color: #ffffff !important;
}

.rb-header-banner {
    padding: 6px 8px;
    border-radius: 6px;
    margin-bottom: 6px;
}
div[data-testid="stMarkdownContainer"] .rb-header-banner,
div[data-testid="stMarkdownContainer"] .rb-header-banner div,
div[data-testid="stMarkdownContainer"] .rb-header-banner * {
    color: #ffffff !important;
}

@media (max-width: 900px) {
    .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    div[data-testid="stHorizontalBlock"]:first-of-type {
        margin-left: -1rem !important;
        margin-right: -1rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
}
</style>
""", unsafe_allow_html=True)

show_navbar("Resume Builder")

# ── Light mode overrides ─────────────────────────────────────────────────────
if is_light:
    st.markdown("""
    <style>
    html,body,.stApp,.page-body,.block-container {
        background: #fdf7e4 !important;
        color: #000000 !important;
    }
    .rb-card {
        background: #ffffff !important;
        border: 1.5px solid #bbab8c !important;
        color: #000000 !important;
        box-shadow: 0 4px 14px rgba(187, 171, 140, 0.15) !important;
    }
    div[data-testid="stMarkdownContainer"] p,
    div[data-testid="stMarkdownContainer"] h1,
    div[data-testid="stMarkdownContainer"] h2,
    div[data-testid="stMarkdownContainer"] h3,
    div[data-testid="stMarkdownContainer"] span,
    div[data-testid="stMarkdownContainer"] strong,
    label, p, h1, h2, h3, h4, h5, h6, span, strong {
        color: #000000 !important;
    }
    div[data-testid="stTextInput"] input,
    div[data-testid="stTextArea"] textarea,
    div[data-testid="stNumberInput"] input,
    div[data-testid="stSelectbox"] > div > div {
        background: #fdf7e4 !important;
        border: 1px solid #bbab8c !important;
        color: #000000 !important;
    }
    div[data-testid="stButton"] button:not([kind="primary"]) {
        background: #fdf7e4 !important;
        border: 1px solid #bbab8c !important;
        color: #000000 !important;
    }
    div[data-testid="stButton"] button[kind="primary"],
    div[data-testid="stDownloadButton"] button[kind="primary"] {
        background: #bbab8c !important;
        border: 1px solid #a49374 !important;
        color: #000000 !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        background: #fdf7e4 !important;
        border: 1px solid #bbab8c !important;
    }
    .stTabs [aria-selected="true"] {
        background: #bbab8c !important;
        color: #000000 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ── Session State Initialization ─────────────────────────────────────────────
if "selected_template" not in st.session_state or not st.session_state.selected_template:
    st.session_state.selected_template = "Classic"
if "num_skills" not in st.session_state:
    st.session_state.num_skills = 3

TEMPLATE_META = {
    "Classic": {
        "icon": "📄",
        "accent": "#1e293b" if is_light else "#e2e8f0",
        "desc": "Traditional ATS-tested black & white design with clean dividers.",
        "tags": ["Traditional", "ATS-Safe", "Classic"],
    },
    "Modern": {
        "icon": "✨",
        "accent": "#2563eb" if is_light else "#60a5fa",
        "desc": "Bold colored header band with structured contemporary typography.",
        "tags": ["Tech", "Structured", "Modern"],
    },
    "Minimal": {
        "icon": "🎯",
        "accent": "#059669" if is_light else "#34d399",
        "desc": "Clean emerald accents with generous whitespace and high readability.",
        "tags": ["Clean", "Minimalist", "Readable"],
    },
    "Creative": {
        "icon": "🎨",
        "accent": "#7c3aed" if is_light else "#a78bfa",
        "desc": "Vibrant gradient header with distinctive section labels and skills.",
        "tags": ["Bold", "Creative", "Portfolio"],
    },
}

def _render_template_card(tmpl: str, meta: dict, is_sel: bool) -> str:
    accent = meta["accent"]
    border_col = accent if is_sel else ("#bbab8c" if is_light else "rgba(255,255,240,0.18)")
    bg_col = "#ffffff" if is_light else "rgba(0,0,0,0.30)"
    text_col = "#000000" if is_light else "#FFFFF0"
    badge_html = f'<span class="rb-badge" style="background:{accent};color:#fefefe!important;">SELECTED</span>' if is_sel else ''

    if tmpl == "Classic":
        mini_header = (
            f'<div style="text-align:center;font-weight:800;font-size:0.86rem;letter-spacing:1px;color:{text_col};margin-bottom:2px;">JOHN SMITH</div>'
            f'<div style="text-align:center;font-size:0.6rem;opacity:0.75;margin-bottom:6px;color:{text_col};">john@email.com • +91 9876543210 • Mumbai</div>'
            f'<div style="height:2px;background:{accent};margin-bottom:6px;"></div>'
        )
    elif tmpl == "Modern":
        mini_header = (
            f'<div class="rb-header-banner" style="background:{accent};">'
            f'<div style="font-weight:800;font-size:0.84rem;">JOHN SMITH</div>'
            f'<div style="font-size:0.6rem;opacity:0.92;">Software Engineer • Mumbai</div>'
            f'</div>'
        )
    elif tmpl == "Minimal":
        mini_header = (
            f'<div style="border-left:3px solid {accent};padding-left:6px;margin-bottom:6px;">'
            f'<div style="font-weight:800;font-size:0.84rem;color:{accent};">John Smith</div>'
            f'<div style="font-size:0.6rem;opacity:0.75;color:{text_col};">john@email.com | +91 9876543210</div>'
            f'</div>'
        )
    else:
        mini_header = (
            f'<div class="rb-header-banner" style="background:linear-gradient(135deg,{accent},#333F63);">'
            f'<div style="font-weight:800;font-size:0.84rem;">JOHN SMITH</div>'
            f'<div style="font-size:0.6rem;opacity:0.9;">Full Stack Developer</div>'
            f'</div>'
        )

    mini_body = (
        f'<div style="font-size:0.63rem;line-height:1.35;opacity:0.88;color:{text_col};">'
        f'<div style="font-weight:800;color:{accent};margin-top:4px;font-size:0.66rem;letter-spacing:0.5px;">EXPERIENCE</div>'
        f'<div><strong>Software Engineer</strong> — Tech Corp</div>'
        f'<div style="font-size:0.58rem;opacity:0.75;">• Developed APIs and increased throughput</div>'
        f'<div style="font-weight:800;color:{accent};margin-top:4px;font-size:0.66rem;letter-spacing:0.5px;">EDUCATION</div>'
        f'<div><strong>B.Tech CS</strong> — Univ (2020-2024)</div>'
        f'<div style="font-weight:800;color:{accent};margin-top:4px;font-size:0.66rem;letter-spacing:0.5px;">SKILLS</div>'
        f'<div style="font-size:0.58rem;">Python, React, SQL, Git, Docker</div>'
        f'</div>'
    )

    tag_bg = "#f3eee3" if is_light else "rgba(255,255,255,0.08)"
    tag_border = "#bbab8c" if is_light else "rgba(255,255,255,0.14)"
    tag_text = "#000000" if is_light else "#FFFFF0"
    tags_html = "".join([
        f'<span style="display:inline-block;background:{tag_bg};border:1px solid {tag_border};border-radius:4px;padding:1px 6px;font-size:0.62rem;margin:2px;color:{tag_text};font-weight:600;">{tag}</span>'
        for tag in meta["tags"]
    ])

    shadow_css = f'0 0 16px {accent}44' if is_sel else ('0 2px 8px rgba(0,0,0,0.06)' if is_light else 'none')
    card_html = (
        f'<div style="background:{bg_col};border:2px solid {border_col};border-radius:14px;padding:12px;min-height:260px;display:flex;flex-direction:column;justify-content:space-between;box-shadow:{shadow_css};margin-bottom:8px;">'
        f'<div>'
        f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">'
        f'<span style="font-weight:800;font-size:0.88rem;color:{accent};">{meta["icon"]} {tmpl}</span>'
        f'{badge_html}'
        f'</div>'
        f'{mini_header}'
        f'{mini_body}'
        f'</div>'
        f'<div style="margin-top:8px;border-top:1px solid {border_col};padding-top:6px;">'
        f'{tags_html}'
        f'</div>'
        f'</div>'
    )
    return _clean_html(card_html)


# ── Page Header ───────────────────────────────────────────────────────────────
st.markdown("## 📝 Resume Builder")
st.caption("Choose an ATS-optimized template, customize your information, and download a high-impact PDF resume.")
st.markdown("")

# ── 1. Choose Template ────────────────────────────────────────────────────────
st.markdown("### 🎨 1. Choose Your Template")
cols = st.columns(4, gap="small")
for col, (tmpl, meta) in zip(cols, TEMPLATE_META.items()):
    with col:
        is_sel = st.session_state.selected_template == tmpl
        st.markdown(_render_template_card(tmpl, meta, is_sel), unsafe_allow_html=True)
        btn_label = "✅ Selected" if is_sel else f"Select {tmpl}"
        btn_type  = "primary" if is_sel else "secondary"
        if st.button(btn_label, key=f"tmpl_{tmpl}", use_container_width=True, type=btn_type):
            st.session_state.selected_template = tmpl
            st.rerun()

selected_template = st.session_state.selected_template
meta = TEMPLATE_META[selected_template]

active_bg = "#ffffff" if is_light else "rgba(51,63,99,0.35)"
active_border = "#bbab8c" if is_light else "rgba(255,255,240,0.18)"
banner_text = "#000000" if is_light else "#FFFFF0"

banner_html = (
    f'<div style="background:{active_bg};border:1.5px solid {active_border};border-radius:12px;padding:0.85rem 1.25rem;margin:1.2rem 0 1.8rem;display:flex;align-items:center;justify-content:space-between;box-shadow:0 2px 10px rgba(0,0,0,0.06);">'
    f'<div>'
    f'<strong style="font-size:1.02rem;color:{banner_text};">{meta["icon"]} Active Template: {selected_template}</strong>'
    f'<p style="font-size:0.83rem;margin:0.25rem 0 0;color:{banner_text};opacity:0.75;">{meta["desc"]}</p>'
    f'</div>'
    f'<span class="rb-badge" style="background:{meta["accent"]};font-size:0.75rem;padding:4px 10px;color:#fefefe!important;">ACTIVE</span>'
    f'</div>'
)
st.markdown(_clean_html(banner_html), unsafe_allow_html=True)

# ── 2. Resume Details Form ───────────────────────────────────────────────────
st.markdown("### ✍️ 2. Fill In Your Details")

# Personal Information
with st.container():
    st.markdown(_clean_html("""
    <div class="rb-card">
        <div class="rb-section-header">
            <span class="rb-section-icon">👤</span>
            <div>
                <div class="rb-section-title">Personal Information</div>
                <div class="rb-section-sub">Contact information and professional headline</div>
            </div>
        </div>
    </div>
    """), unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        name  = st.text_input("Full Name *", value=db_user.get("name", ""), placeholder="e.g. John Doe")
        phone = st.text_input("Phone Number", value=db_user.get("phone", ""), placeholder="e.g. +91 9876543210")
        linkedin = st.text_input("LinkedIn Profile", value=db_user.get("linkedin", ""), placeholder="e.g. linkedin.com/in/johndoe")
    with c2:
        email = st.text_input("Email *", value=st.session_state.email, placeholder="e.g. john@example.com")
        location = st.text_input("Location", value=db_user.get("location", ""), placeholder="e.g. Mumbai, India")
        github = st.text_input("GitHub Profile", value=db_user.get("github", ""), placeholder="e.g. github.com/johndoe")

    summary = st.text_area(
        "Professional Summary",
        height=90,
        placeholder="Results-driven Software Engineer with experience building scalable web applications, REST APIs, and data solutions..."
    )

st.markdown("")

# Skills
with st.container():
    st.markdown(_clean_html("""
    <div class="rb-card">
        <div class="rb-section-header">
            <span class="rb-section-icon">🧠</span>
            <div>
                <div class="rb-section-title">Technical & Soft Skills</div>
                <div class="rb-section-sub">Categorize skills (e.g. Languages, Frameworks, Databases, Tools)</div>
            </div>
        </div>
    </div>
    """), unsafe_allow_html=True)

    # Initialize default skill category from profile if empty
    user_skills = db_user.get("skills", [])
    if user_skills and "scat_0" not in st.session_state:
        st.session_state["scat_0"] = "Technical Skills"
        st.session_state["sval_0"] = ", ".join(user_skills)

    skills_data = {}
    for i in range(st.session_state.num_skills):
        s1, s2, s3, s4 = st.columns([1.5, 3.4, 1.2, 0.5])
        with s1:
            cat = st.text_input(f"Category {i+1}", key=f"scat_{i}", placeholder="e.g. Languages")
        with s2:
            val = st.text_input("Skills (comma-separated)", key=f"sval_{i}", placeholder="e.g. Python, SQL, Java")
        with s3:
            level = st.selectbox("Proficiency", ["Basic", "Intermediate", "Expert"], key=f"slvl_{i}", index=1)
        with s4:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🗑️", key=f"sdel_{i}", help="Delete row"):
                st.session_state.num_skills = max(1, st.session_state.num_skills - 1)
                st.rerun()

        if cat.strip() and val.strip():
            skills_data[cat.strip()] = {
                "skills": [s.strip() for s in val.split(",") if s.strip()],
                "level": level
            }

    if st.button("➕ Add Skill Category"):
        st.session_state.num_skills += 1
        st.rerun()

st.markdown("")

# Education
with st.container():
    st.markdown(_clean_html("""
    <div class="rb-card">
        <div class="rb-section-header">
            <span class="rb-section-icon">🎓</span>
            <div>
                <div class="rb-section-title">Education *</div>
                <div class="rb-section-sub">Academic degrees, universities, and graduation details</div>
            </div>
        </div>
    </div>
    """), unsafe_allow_html=True)

    num_edu = st.number_input("Number of Education Entries", min_value=1, max_value=4, value=1, key="num_edu")
    education = []
    for i in range(int(num_edu)):
        st.markdown(f"**Education #{i+1}**")
        e1, e2, e3, e4 = st.columns([1.5, 1.8, 1.0, 0.8])
        with e1: deg  = st.text_input("Degree / Program *", key=f"deg_{i}", placeholder="e.g. B.Tech Computer Science")
        with e2: inst = st.text_input("Institution / University *", key=f"inst_{i}", placeholder="e.g. ABC University")
        with e3: yr   = st.text_input("Year / Duration", key=f"yr_{i}", placeholder="e.g. 2020 – 2024")
        with e4: gpa  = st.text_input("GPA / Grade", key=f"gpa_{i}", placeholder="e.g. 8.5 / 10")
        if deg.strip():
            education.append({"degree": deg.strip(), "institution": inst.strip(), "year": yr.strip(), "gpa": gpa.strip()})

st.markdown("")

# Work Experience
with st.container():
    st.markdown(_clean_html("""
    <div class="rb-card">
        <div class="rb-section-header">
            <span class="rb-section-icon">💼</span>
            <div>
                <div class="rb-section-title">Work Experience (Optional)</div>
                <div class="rb-section-sub">Full-time, part-time, or internships (set 0 for freshers)</div>
            </div>
        </div>
    </div>
    """), unsafe_allow_html=True)

    num_exp = st.number_input("Number of Experience Entries", min_value=0, max_value=5, value=0, key="num_exp")
    experience = []
    if num_exp == 0:
        st.caption("ℹ️ No work experience added yet. Set the number above to 1 or more to add job or internship details.")
    for i in range(int(num_exp)):
        st.markdown(f"**Experience #{i+1}**")
        x1, x2, x3 = st.columns(3)
        with x1: title = st.text_input("Job Title *", key=f"jtitle_{i}", placeholder="e.g. Software Engineer")
        with x2: comp  = st.text_input("Company *", key=f"jcomp_{i}", placeholder="e.g. Google")
        with x3: dur   = st.text_input("Duration", key=f"jdur_{i}", placeholder="e.g. Jun 2022 – Present")
        resp = st.text_area(
            "Responsibilities / Key Achievements (one bullet per line)",
            key=f"jresp_{i}", height=80,
            placeholder="• Designed and deployed scalable RESTful APIs\n• Reduced database query response times by 35%"
        )
        if title.strip():
            experience.append({
                "title": title.strip(), "company": comp.strip(), "duration": dur.strip(),
                "responsibilities": [r.lstrip("•-– ").strip() for r in resp.splitlines() if r.strip()],
            })

st.markdown("")

# Projects
with st.container():
    st.markdown(_clean_html("""
    <div class="rb-card">
        <div class="rb-section-header">
            <span class="rb-section-icon">🛠️</span>
            <div>
                <div class="rb-section-title">Projects</div>
                <div class="rb-section-sub">Key academic, personal, or professional projects</div>
            </div>
        </div>
    </div>
    """), unsafe_allow_html=True)

    num_proj = st.number_input("Number of Projects", min_value=0, max_value=5, value=1, key="num_proj")
    projects = []
    for i in range(int(num_proj)):
        st.markdown(f"**Project #{i+1}**")
        p1, p2 = st.columns(2)
        with p1: ptitle = st.text_input("Project Title *", key=f"ptitle_{i}", placeholder="e.g. Skill Gap Analyzer")
        with p2: plink  = st.text_input("Live Demo / GitHub Link", key=f"plink_{i}", placeholder="e.g. github.com/user/project")
        ptech = st.text_input("Technologies Used", key=f"ptech_{i}", placeholder="e.g. Python, Streamlit, PostgreSQL")
        pdesc = st.text_area(
            "Project Summary & Impact", key=f"pdesc_{i}", height=70,
            placeholder="• Built a career platform analyzing skill gaps\n• Integrated automated ATS scoring algorithm"
        )
        if ptitle.strip():
            projects.append({
                "title": ptitle.strip(), "description": pdesc.strip(),
                "tech": [t.strip() for t in ptech.split(",") if t.strip()], "link": plink.strip(),
            })

st.markdown("")

# Certifications
with st.container():
    st.markdown(_clean_html("""
    <div class="rb-card">
        <div class="rb-section-header">
            <span class="rb-section-icon">🏆</span>
            <div>
                <div class="rb-section-title">Certifications (Optional)</div>
                <div class="rb-section-sub">Licenses, credentials, and honors (one per line)</div>
            </div>
        </div>
    </div>
    """), unsafe_allow_html=True)

    certs_raw = st.text_area(
        "Certifications List", height=75,
        placeholder="AWS Certified Solutions Architect (2024)\nOracle Certified Associate, Java SE 8"
    )
    certifications = [line.strip() for line in certs_raw.splitlines() if line.strip()]

st.markdown("---")

# ── 3. Assemble and Download ──────────────────────────────────────────────────
st.markdown("### 🚀 3. Generate Your Resume")

resume_data = {
    "name": name, "email": email, "phone": phone,
    "linkedin": linkedin, "github": github, "location": location,
    "summary": summary, "skills": skills_data,
    "experience": experience, "education": education,
    "projects": projects, "certifications": certifications,
}

b1, b2 = st.columns([1.5, 1.5])
with b1:
    generate_clicked = st.button("📄 Generate & Download Resume", type="primary", use_container_width=True)
with b2:
    preview_clicked  = st.button("👁️ Preview All 4 Templates", use_container_width=True)

if generate_clicked or preview_clicked:
    errors = validate_resume_data(resume_data)
    if errors:
        for e in errors:
            st.error(f"❌ {e}")
    else:
        if generate_clicked:
            with st.spinner(f"Building your {selected_template} resume..."):
                try:
                    pdf = build_resume_pdf(resume_data, template=selected_template)
                    clean_filename = f"{name.strip().replace(' ', '_')}_{selected_template}_resume.pdf" if name.strip() else f"{selected_template}_resume.pdf"
                    
                    st.success(f"🎉 **{selected_template} Resume Generated Successfully!** Click below to download:")
                    
                    c_dl, _ = st.columns([1.8, 2.2])
                    with c_dl:
                        st.download_button(
                            label=f"⬇️ Download {selected_template} Resume (PDF)",
                            data=pdf,
                            file_name=clean_filename,
                            mime="application/pdf",
                            type="primary",
                            use_container_width=True,
                        )
                    
                    with st.expander("👁️ View Embedded PDF Preview", expanded=True):
                        b64 = base64.b64encode(pdf).decode("ascii")
                        st.markdown(
                            f'<iframe src="data:application/pdf;base64,{b64}#toolbar=0" '
                            f'width="100%" height="750px" '
                            f'style="border:1px solid rgba(255,255,240,0.2);border-radius:12px;background:#ffffff;">'
                            f'</iframe>',
                            unsafe_allow_html=True,
                        )
                except Exception as exc:
                    st.error(f"Error generating PDF: {exc}")

        if preview_clicked:
            st.markdown("---")
            st.markdown("### 👁️ Preview All 4 Templates with Your Data")
            st.caption("Explore how your resume looks across different templates and download your favorite.")
            templates_list = ["Classic", "Modern", "Minimal", "Creative"]
            icons = {t: TEMPLATE_META[t]["icon"] for t in templates_list}
            
            with st.spinner("Generating previews for all 4 templates..."):
                pdfs = {}
                for tmpl in templates_list:
                    try:
                        pdfs[tmpl] = build_resume_pdf(resume_data, template=tmpl)
                    except Exception as exc:
                        st.error(f"Could not build {tmpl}: {exc}")

            tabs = st.tabs([f"{icons[t]} {t}" for t in templates_list])
            for tab, tmpl in zip(tabs, templates_list):
                with tab:
                    if tmpl in pdfs:
                        pdf_data = pdfs[tmpl]
                        clean_fn = f"{name.strip().replace(' ', '_')}_{tmpl}_resume.pdf" if name.strip() else f"{tmpl}_resume.pdf"
                        
                        st.download_button(
                            label=f"⬇️ Download {tmpl} Template (PDF)",
                            data=pdf_data,
                            file_name=clean_fn,
                            mime="application/pdf",
                            key=f"dl_tab_{tmpl}",
                            use_container_width=True,
                        )
                        b64_tab = base64.b64encode(pdf_data).decode("ascii")
                        st.markdown(
                            f'<iframe src="data:application/pdf;base64,{b64_tab}#toolbar=0" '
                            f'width="100%" height="700px" '
                            f'style="border:1px solid rgba(255,255,240,0.2);border-radius:12px;background:#ffffff;margin-top:10px;">'
                            f'</iframe>',
                            unsafe_allow_html=True,
                        )
