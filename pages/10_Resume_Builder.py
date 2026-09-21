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

st.markdown("""
<style>
#MainMenu,footer,header,[data-testid="stToolbar"],[data-testid="stSidebarNav"],
[data-testid="stSidebar"],[data-testid="collapsedControl"],section[data-testid="stSidebar"],
.stDeployButton,[class*="viewerBadge"],[class*="toolbar"]
{display:none!important;visibility:hidden!important;}
html,body{margin:0!important;padding:0!important;}
.block-container{padding:0!important;max-width:100%!important;}
div[data-testid="stButton"] button{font-weight:700!important;border-radius:10px!important;}
div[data-testid="stButton"] button[kind="primary"]{background:#333F63!important;border:1px solid rgba(255,255,240,0.18)!important;}
html,body,.stApp{color:#FFFFF0!important;}
div[data-testid="stButton"] button[kind="primary"]{background:#333F63!important;color:#FFFFF0!important;border:1px solid rgba(255,255,240,0.18)!important;box-shadow:none!important;}
.form-section-card{
    background:rgba(0,0,0,0.24);
    border:1px solid rgba(255,255,240,0.14);
    border-radius:16px;
    padding:1.4rem;
    margin-bottom:1.5rem;
}
.section-badge{
    display:inline-flex;align-items:center;gap:0.4rem;
    font-size:0.8rem;font-weight:800;padding:0.25rem 0.65rem;border-radius:8px;
    background:rgba(255,255,240,0.08);color:#FFFFF0;margin-bottom:0.8rem;
}
</style>
""", unsafe_allow_html=True)

show_navbar("Resume Builder")

if is_light:
    st.markdown("""
    <style>
    html,body,.stApp,.page-body,.block-container{
        background:#fdf7e4!important;
        color:#000000!important;
    }
    .form-section-card{
        background:#fdf7e4!important;
        border:1px solid #bbab8c!important;
        color:#000000!important;
    }
    div[data-testid="stMarkdownContainer"],
    div[data-testid="stMarkdownContainer"] *,
    label,p,h1,h2,h3,h4,h5,h6,span,strong{
        color:#000000!important;
    }
    div[data-testid="stTextInput"] input,
    div[data-testid="stTextArea"] textarea,
    div[data-testid="stNumberInput"] input,
    div[data-testid="stSelectbox"] > div > div,
    div[data-testid="stMultiSelect"] > div > div{
        background:#fdf7e4!important;
        background-color:#fdf7e4!important;
        border-color:#bbab8c!important;
        color:#000000!important;
        box-shadow:none!important;
    }
    div[data-testid="stButton"] button,
    div[data-testid="stDownloadButton"] button{
        background:#bbab8c!important;
        background-color:#bbab8c!important;
        border:1px solid #bbab8c!important;
        color:#000000!important;
        box-shadow:none!important;
    }
    div[data-testid="stAlert"]{
        background:#fdf7e4!important;
        border:1px solid #bbab8c!important;
        color:#000000!important;
    }
    .stTabs [data-baseweb="tab-list"]{
        background:#fdf7e4!important;
        border:1px solid #bbab8c!important;
    }
    .stTabs [aria-selected="true"]{
        background:#bbab8c!important;
        color:#000000!important;
    }
    </style>
    """, unsafe_allow_html=True)

# ── Session state init ────────────────────────────────────────────────────────
if "selected_template" not in st.session_state or not st.session_state.selected_template:
    st.session_state.selected_template = "Classic"
if "num_skills" not in st.session_state:
    st.session_state.num_skills = 3

TEMPLATE_META = {
    "Classic": {
        "icon": "📄", "accent": "#000000" if is_light else "#cbd5e1",
        "desc": "Black & white, centered name. Traditional & ATS-tested.",
        "tags": ["Traditional", "ATS-Safe", "Classic Serif"],
    },
    "Modern": {
        "icon": "✨", "accent": "#3b82f6" if is_light else "#60a5fa",
        "desc": "Indigo header band with structured modern typography.",
        "tags": ["Popular", "Tech", "Structured"],
    },
    "Minimal": {
        "icon": "🎯", "accent": "#059669" if is_light else "#34d399",
        "desc": "Clean emerald accents, generous whitespace, sleek lines.",
        "tags": ["Clean", "Minimalist", "Readable"],
    },
    "Creative": {
        "icon": "🎨", "accent": "#7c3aed" if is_light else "#a78bfa",
        "desc": "Purple header, standout section labels and skill tags.",
        "tags": ["Bold", "Creative", "Modern"],
    },
}

def _render_template_card(tmpl: str, meta: dict, is_sel: bool) -> str:
    accent = meta["accent"]
    border_col = accent if is_sel else ("#bbab8c" if is_light else "rgba(255,255,240,0.18)")
    bg_col = "#fdf7e4" if is_light else "rgba(0,0,0,0.28)"
    text_col = "#000000" if is_light else "#FFFFF0"
    badge_html = f'<span style="background:{accent};color:#000 if {is_light} else #fff;padding:2px 8px;border-radius:12px;font-size:0.68rem;font-weight:800;">SELECTED</span>' if is_sel else ''

    if tmpl == "Classic":
        mini_header = f'<div style="text-align:center;font-weight:800;font-size:0.86rem;letter-spacing:1px;color:{text_col};margin-bottom:2px;">JOHN SMITH</div><div style="text-align:center;font-size:0.6rem;opacity:0.65;margin-bottom:6px;">john@email.com • +91 9876543210 • Mumbai</div><div style="height:1.5px;background:{accent};margin-bottom:6px;"></div>'
    elif tmpl == "Modern":
        mini_header = f'<div style="background:{accent};color:#fff;padding:6px 8px;border-radius:6px;margin-bottom:6px;"><div style="font-weight:800;font-size:0.84rem;">JOHN SMITH</div><div style="font-size:0.6rem;opacity:0.9;">Software Engineer • Mumbai</div></div>'
    elif tmpl == "Minimal":
        mini_header = f'<div style="border-left:3px solid {accent};padding-left:6px;margin-bottom:6px;"><div style="font-weight:800;font-size:0.84rem;color:{accent};">John Smith</div><div style="font-size:0.6rem;opacity:0.65;">john@email.com | +91 9876543210</div></div>'
    else:
        mini_header = f'<div style="background:linear-gradient(135deg,{accent},#333F63);color:#fff;padding:6px 8px;border-radius:6px;margin-bottom:6px;"><div style="font-weight:800;font-size:0.84rem;">JOHN SMITH</div><div style="font-size:0.6rem;opacity:0.85;">Full Stack Developer</div></div>'

    mini_body = f"""
    <div style="font-size:0.63rem;line-height:1.35;opacity:0.85;color:{text_col};">
      <div style="font-weight:800;color:{accent};margin-top:4px;font-size:0.66rem;">EXPERIENCE</div>
      <div><strong>Software Engineer</strong> — Tech Corp</div>
      <div style="font-size:0.58rem;opacity:0.75;">• Developed APIs and increased throughput</div>
      <div style="font-weight:800;color:{accent};margin-top:4px;font-size:0.66rem;">EDUCATION</div>
      <div><strong>B.Tech CS</strong> — Univ (2020-2024)</div>
      <div style="font-weight:800;color:{accent};margin-top:4px;font-size:0.66rem;">SKILLS</div>
      <div style="font-size:0.58rem;">Python, React, SQL, Git, Docker</div>
    </div>
    """

    tags_html = " ".join([f'<span style="display:inline-block;background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.12);border-radius:4px;padding:1px 6px;font-size:0.62rem;margin:2px;opacity:0.85;">{tag}</span>' for tag in meta["tags"]])

    shadow_css = f'0 0 16px {accent}44' if is_sel else 'none'
    return f"""
    <div style="background:{bg_col};border:2px solid {border_col};border-radius:14px;padding:12px;min-height:250px;display:flex;flex-direction:column;justify-content:space-between;box-shadow:{shadow_css};margin-bottom:8px;">
      <div>
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
          <span style="font-weight:800;font-size:0.88rem;color:{accent};">{meta['icon']} {tmpl}</span>
          {badge_html}
        </div>
        {mini_header}
        {mini_body}
      </div>
      <div style="margin-top:8px;border-top:1px solid rgba(255,255,255,0.08);padding-top:6px;">
        {tags_html}
      </div>
    </div>
    """

st.markdown("## 📝 Resume Builder")
st.caption("Choose an ATS-optimized template, enter your details, and instantly generate your professional PDF resume.")
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

st.markdown(f"""
<div style="background:rgba(51,63,99,0.35);border:1px solid rgba(255,255,240,0.18);border-radius:12px;padding:0.75rem 1.2rem;margin:1.2rem 0 1.5rem;display:flex;align-items:center;justify-content:space-between;">
    <div>
        <strong style="font-size:1rem;color:#FFFFF0;">{meta['icon']} Selected Template: {selected_template}</strong>
        <p style="font-size:0.82rem;margin:0.2rem 0 0;opacity:0.75;">{meta['desc']}</p>
    </div>
    <span style="background:{meta['accent']};color:#fff;padding:0.25rem 0.75rem;border-radius:8px;font-size:0.75rem;font-weight:800;">ACTIVE</span>
</div>
""", unsafe_allow_html=True)

# ── 2. Resume Details Form ───────────────────────────────────────────────────
st.markdown("### ✍️ 2. Fill In Your Details")

# Personal Information
with st.container():
    st.markdown('<div class="section-badge">👤 Personal Information</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        name  = st.text_input("Full Name *", value=db_user.get("name", ""), placeholder="e.g. John Doe")
        email = st.text_input("Email *", value=st.session_state.email, placeholder="e.g. john@example.com")
    with c2:
        phone    = st.text_input("Phone Number", placeholder="e.g. +91 9876543210")
        linkedin = st.text_input("LinkedIn Profile", placeholder="e.g. linkedin.com/in/johndoe")
    with c3:
        github   = st.text_input("GitHub Profile", placeholder="e.g. github.com/johndoe")
        location = st.text_input("Location", placeholder="e.g. Mumbai, India")

    summary = st.text_area(
        "Professional Summary",
        height=85,
        placeholder="Results-driven Software Engineer with experience building scalable web applications, REST APIs, and data solutions..."
    )

st.markdown("---")

# Skills
with st.container():
    st.markdown('<div class="section-badge">🧠 Technical & Soft Skills</div>', unsafe_allow_html=True)
    st.caption("Organize skills by category (e.g. Languages, Frameworks, Tools, Databases).")

    # Initialize default skill category from profile if empty
    user_skills = db_user.get("skills", [])
    if user_skills and "scat_0" not in st.session_state:
        st.session_state["scat_0"] = "Technical Skills"
        st.session_state["sval_0"] = ", ".join(user_skills)

    skills_data = {}
    for i in range(st.session_state.num_skills):
        s1, s2, s3, s4 = st.columns([1.5, 3.5, 1.3, 0.6])
        with s1:
            cat = st.text_input(f"Category {i+1}", key=f"scat_{i}", placeholder="e.g. Languages")
        with s2:
            val = st.text_input("Skills (comma-separated)", key=f"sval_{i}", placeholder="e.g. Python, SQL, Java")
        with s3:
            level = st.selectbox("Proficiency", ["Basic", "Intermediate", "Expert"], key=f"slvl_{i}", index=1)
        with s4:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🗑️", key=f"sdel_{i}", help="Delete this row"):
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

st.markdown("---")

# Education
with st.container():
    st.markdown('<div class="section-badge">🎓 Education *</div>', unsafe_allow_html=True)
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

st.markdown("---")

# Work Experience
with st.container():
    st.markdown('<div class="section-badge">💼 Work Experience (Optional)</div>', unsafe_allow_html=True)
    num_exp = st.number_input("Number of Experience Entries (0 for freshers)", min_value=0, max_value=5, value=0, key="num_exp")
    experience = []
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

st.markdown("---")

# Projects
with st.container():
    st.markdown('<div class="section-badge">🛠️ Projects</div>', unsafe_allow_html=True)
    num_proj = st.number_input("Number of Projects", min_value=0, max_value=5, value=1, key="num_proj")
    projects = []
    for i in range(int(num_proj)):
        st.markdown(f"**Project #{i+1}**")
        p1, p2 = st.columns([1.5, 1.5])
        with p1: ptitle = st.text_input("Project Title *", key=f"ptitle_{i}", placeholder="e.g. Skill Gap Analyzer")
        with p2: plink  = st.text_input("Live Demo / GitHub Link", key=f"plink_{i}", placeholder="e.g. github.com/user/project")
        ptech = st.text_input("Technologies Used", key=f"ptech_{i}", placeholder="e.g. Python, Streamlit, PostgreSQL")
        pdesc = st.text_area(
            "Project Summary & Impact", key=f"pdesc_{i}", height=70,
            placeholder="• Built a full-stack career platform analyzing skill gaps\n• Integrated automated ATS scoring algorithm"
        )
        if ptitle.strip():
            projects.append({
                "title": ptitle.strip(), "description": pdesc.strip(),
                "tech": [t.strip() for t in ptech.split(",") if t.strip()], "link": plink.strip(),
            })

st.markdown("---")

# Certifications
with st.container():
    st.markdown('<div class="section-badge">🏆 Certifications (Optional)</div>', unsafe_allow_html=True)
    certs_raw = st.text_area(
        "Enter Certifications (one per line)", height=75,
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
                    
                    c_dl, _ = st.columns([1.5, 2.5])
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
