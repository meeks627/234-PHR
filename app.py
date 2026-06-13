import streamlit as st
import time
import random
from datetime import datetime, date

st.set_page_config(page_title="MediVault PHR Pro", page_icon="🏥", layout="wide")

st.markdown("""
<style>
.stApp { background: #ffffff; }
h1, h2, h3 { color: #000000; font-weight: 700; }
.stMarkdown p, .stMarkdown li, .stMarkdown span { color: #000000; }
.stMarkdown strong { color: #000000; font-weight: 700; }
.stMarkdown em { color: #1565C0; }
.stMarkdown code { color: #d63384 !important; background: #f5f5f5 !important; }
a { color: #1565C0; font-weight: 500; }
.st-dv { border-color: #e0e0e0 !important; }

.card {
    background: #f8f9fa; border-radius: 12px; padding: 1.3rem; margin-bottom: 1rem;
    border: 1px solid #e0e0e0; box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.card h3, .card p, .card li, .card span, .card strong { color: #000000 !important; }

.card-white {
    background: #ffffff; border-radius: 12px; padding: 1.3rem; margin-bottom: 1rem;
    border: 1px solid #e0e0e0; box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.card-white h3 { color: #000000 !important; font-weight: 700; }
.card-white p, .card-white li, .card-white span { color: #000000 !important; }
.card-white strong { color: #000000 !important; font-weight: 700; }
.card-white .stMetric { background: #f5f5f5; border: 1px solid #e0e0e0; }
.card-white [data-testid="stMetricValue"] { color: #000000 !important; font-weight: 800; }
.card-white [data-testid="stMetricLabel"] p { color: #333333 !important; }

section[data-testid="stSidebar"] { background: #f0f2f6; border-right: 1px solid #d0d0d0; }
section[data-testid="stSidebar"] .stMarkdown p { color: #000000; }
section[data-testid="stSidebar"] .stMarkdown strong { color: #000000; font-weight: 700; }
section[data-testid="stSidebar"] hr { border-color: #d0d0d0; }
section[data-testid="stSidebar"] .stButton button {
    background: #e0e0e0; color: #000000; border: 1px solid #ccc; border-radius: 8px;
}
section[data-testid="stSidebar"] .stTextInput input {
    background: #ffffff; color: #000000; border: 1px solid #ccc; border-radius: 8px;
}
section[data-testid="stSidebar"] .stTextInput input::placeholder { color: #999; }

.stButton button { border-radius: 8px; font-weight: 500; }
button[kind="primary"] {
    background: #1565C0 !important; border: none !important; font-weight: 600 !important; color: white !important;
}
.stButton button:not([kind="primary"]) {
    background: #e0e0e0; color: #000000; border: 1px solid #ccc;
}

.stTextInput input, .stTextArea textarea, .stDateInput input {
    background: #ffffff !important; color: #000000 !important;
    border: 1px solid #ccc !important; border-radius: 8px !important;
}
.stTextInput input::placeholder, .stTextArea textarea::placeholder { color: #999 !important; }
.stTextInput input:focus, .stTextArea textarea:focus { border-color: #1565C0 !important; }
[data-testid="stChatInput"] textarea, [data-testid="stChatInput"] input {
    color: #000000 !important; background: #ffffff !important; border: 1px solid #ccc !important;
}

.stAlert { border-left-width: 4px !important; }
.stSuccess { border-left-color: #4caf50 !important; }
.stError { border-left-color: #f44336 !important; }

.stMetric { background: #f5f5f5; border-radius: 8px; padding: 0.8rem; border: 1px solid #e0e0e0; }
[data-testid="stMetricValue"] { color: #000000 !important; font-weight: 800; }
[data-testid="stMetricLabel"] p { color: #333 !important; font-weight: 600 !important; }

.badge-green {
    display: inline-block; background: #e8f5e9; color: #2e7d32;
    padding: 0.2rem 0.7rem; border-radius: 12px; font-size: 0.78rem;
    font-weight: 700; border: 1px solid #4caf50;
}
.badge-red {
    display: inline-block; background: #fce4ec; color: #c62828;
    padding: 0.2rem 0.7rem; border-radius: 12px; font-size: 0.78rem;
    font-weight: 700; border: 1px solid #e53935;
}
.badge-blue {
    display: inline-block; background: #e3f2fd; color: #1565C0;
    padding: 0.2rem 0.7rem; border-radius: 12px; font-size: 0.78rem;
    font-weight: 700; border: 1px solid #42a5f5;
}

.search-container {
    background: #f8f9fa; border-radius: 12px; padding: 1.5rem 2rem;
    margin: 1rem 0; border: 1px solid #e0e0e0; text-align: center;
}
.search-title { color: #1565C0; font-size: 0.85rem; margin-bottom: 0.5rem; letter-spacing: 1.5px; text-transform: uppercase; font-weight: 700; }
.search-container .stTextInput input { background: #ffffff !important; border-color: #1565C0 !important; }

.section-label {
    color: #1565C0; font-size: 0.78rem; text-transform: uppercase;
    letter-spacing: 1.5px; margin-bottom: 0.75rem; font-weight: 700;
}
.stAlert p { font-weight: 500; color: #000000 !important; }
.emoji { font-size: 1.5em !important; }
h1 .emoji { font-size: 2rem !important; }
.badge-green, .badge-red, .badge-blue { font-size: 0.9rem !important; }
</style>
""", unsafe_allow_html=True)

# ── GEMINI SETUP ──
import google.generativeai as genai

GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
if "gemini_api_key" not in st.session_state:
    st.session_state.gemini_api_key = GEMINI_API_KEY

# ── DATABASES ──
PATIENTS = {
    "MH-001": {
        "patient_id": "MH-001", "name": "Amina Yusuf", "age": 29, "gender": "Female",
        "blood_group": "O+", "allergies": ["Penicillin"],
        "conditions": ["Asthma", "Pregnancy (3rd trimester)"],
        "medications": ["Salbutamol", "Iron supplements"],
        "medical_history": [
            {"hospital": "Lagos University Teaching Hospital", "date": "2026-01-15",
             "diagnosis": "Hypertensive urgency",
             "notes": "Presented with elevated BP 160/100 and headache. Started on Amlodipine 5mg daily. Advised salt restriction and bed rest.",
             "medications_prescribed": ["Amlodipine 5mg"], "doctor": "Dr. Adebayo", "department": "Cardiology"},
            {"hospital": "General Hospital Abuja", "date": "2026-03-10",
             "diagnosis": "Antenatal checkup — 28 weeks",
             "notes": "BP stable at 128/84. Fetal heart rate normal. Iron supplements continued.",
             "medications_prescribed": ["Iron supplements"], "doctor": "Dr. Ngozi", "department": "OB/GYN"},
            {"hospital": "Lagos University Teaching Hospital", "date": "2026-04-20",
             "diagnosis": "Mild asthma exacerbation",
             "notes": "Wheezing and SOB for 2 days. Salbutamol increased. Prednisolone 40mg prescribed.",
             "medications_prescribed": ["Prednisolone 40mg", "Salbutamol PRN"], "doctor": "Dr. Adebayo", "department": "Respiratory"},
            {"hospital": "General Hospital Abuja", "date": "2026-06-05",
             "diagnosis": "Antenatal checkup — 34 weeks",
             "notes": "BP 130/86. Mild pedal edema. Urinalysis negative. Delivery planning discussed.",
             "medications_prescribed": ["Salbutamol", "Iron supplements"], "doctor": "Dr. Ngozi", "department": "OB/GYN"}
        ],
        "emergency_contact": "Husband - 08012345678", "nin_linked": "YES", "pin": "1234"
    },
    "MH-002": {
        "patient_id": "MH-002", "name": "John Okafor", "age": 45, "gender": "Male",
        "blood_group": "A+", "allergies": [],
        "conditions": ["Type 2 Diabetes"],
        "medications": ["Metformin"],
        "medical_history": [
            {"hospital": "Lagos University Teaching Hospital", "date": "2025-02-03",
             "diagnosis": "New-onset Type 2 Diabetes",
             "notes": "FBG 11.2 mmol/L, HbA1c 8.5%. Started Metformin 500mg bid.",
             "medications_prescribed": ["Metformin 500mg"], "doctor": "Dr. Okafor", "department": "Endocrinology"},
            {"hospital": "General Hospital Abuja", "date": "2025-08-12",
             "diagnosis": "Diabetes follow-up",
             "notes": "HbA1c improved to 7.2%. Metformin increased to 850mg bid.",
             "medications_prescribed": ["Metformin 850mg"], "doctor": "Dr. Eze", "department": "Endocrinology"},
            {"hospital": "Lagos University Teaching Hospital", "date": "2026-01-20",
             "diagnosis": "Hyperglycemic episode",
             "notes": "Glucose 18.5 mmol/L. Managed with IV fluids and insulin. Admitted 2 days.",
             "medications_prescribed": ["Metformin 1g", "Insulin (temporary)"], "doctor": "Dr. Adebayo", "department": "Emergency"},
            {"hospital": "General Hospital Abuja", "date": "2026-05-15",
             "diagnosis": "Routine diabetes review",
             "notes": "HbA1c 6.9%. BP 128/82. No complications detected.",
             "medications_prescribed": ["Metformin 1g"], "doctor": "Dr. Eze", "department": "Endocrinology"}
        ],
        "emergency_contact": "Wife - 08098765432", "nin_linked": "YES", "pin": "1234"
    },
    "MH-003": {
        "patient_id": "MH-003", "name": "Fatima Bello", "age": 60, "gender": "Female",
        "blood_group": "B+", "allergies": ["Aspirin"],
        "conditions": ["Hypertension", "Stroke history"],
        "medications": ["Amlodipine"],
        "medical_history": [
            {"hospital": "Lagos University Teaching Hospital", "date": "2022-03-22",
             "diagnosis": "Acute ischemic stroke",
             "notes": "Left-sided weakness. CT: small MCA infarct. Thrombolysis given. Admitted 5 days.",
             "medications_prescribed": ["Aspirin 75mg", "Amlodipine 5mg", "Atorvastatin 20mg"], "doctor": "Dr. Adebayo", "department": "Neurology"},
            {"hospital": "General Hospital Abuja", "date": "2023-09-10",
             "diagnosis": "Post-stroke follow-up",
             "notes": "Modified Rankin 1. Aspirin stopped — switched to Clopidogrel.",
             "medications_prescribed": ["Clopidogrel 75mg", "Amlodipine 5mg", "Atorvastatin 20mg"], "doctor": "Dr. Ngozi", "department": "Neurology"},
            {"hospital": "Lagos University Teaching Hospital", "date": "2024-01-05",
             "diagnosis": "Hypertension review",
             "notes": "BP 142/88. Amlodipine increased to 10mg.",
             "medications_prescribed": ["Amlodipine 10mg", "Clopidogrel 75mg", "Atorvastatin 20mg"], "doctor": "Dr. Adebayo", "department": "Cardiology"},
            {"hospital": "General Hospital Abuja", "date": "2026-04-30",
             "diagnosis": "Routine BP check",
             "notes": "BP 130/82. Patient well. Continue current regimen.",
             "medications_prescribed": ["Amlodipine 10mg", "Clopidogrel 75mg", "Atorvastatin 20mg"], "doctor": "Dr. Eze", "department": "General Medicine"}
        ],
        "emergency_contact": "Son - 08055512345", "nin_linked": "NO", "pin": "1234"
    },
    "MH-004": {
        "patient_id": "MH-004", "name": "David Ijeoma", "age": 12, "gender": "Male",
        "blood_group": "O-", "allergies": ["Peanut allergy"],
        "conditions": ["Severe asthma"],
        "medications": ["Ventolin inhaler"],
        "medical_history": [
            {"hospital": "Lagos University Teaching Hospital", "date": "2025-03-05",
             "diagnosis": "Acute severe asthma",
             "notes": "SpO2 88%. Nebulized Salbutamol + Ipratropium. Admitted 3 days.",
             "medications_prescribed": ["Nebulized Salbutamol", "Beclometasone inhaler"], "doctor": "Dr. Okoro", "department": "Pediatrics"},
            {"hospital": "General Hospital Abuja", "date": "2025-07-14",
             "diagnosis": "Asthma follow-up",
             "notes": "Peak flow 65%. Ventolin 2-3x/week. Inhaler technique reviewed.",
             "medications_prescribed": ["Beclometasone inhaler", "Ventolin PRN"], "doctor": "Dr. Ngozi", "department": "Pediatrics"},
            {"hospital": "Lagos University Teaching Hospital", "date": "2025-12-01",
             "diagnosis": "Anaphylaxis — peanut",
             "notes": "Epinephrine given at school. Observed 6h. Epi-pen prescribed.",
             "medications_prescribed": ["Epinephrine auto-injector", "Cetirizine"], "doctor": "Dr. Okoro", "department": "Emergency"},
            {"hospital": "General Hospital Abuja", "date": "2026-02-20",
             "diagnosis": "Asthma review — well controlled",
             "notes": "Peak flow 82%. Ventolin <2x/week. Action plan updated.",
             "medications_prescribed": ["Beclometasone inhaler", "Ventolin PRN"], "doctor": "Dr. Eze", "department": "Pediatrics"}
        ],
        "emergency_contact": "Mother - 08044467890", "nin_linked": "YES", "pin": "1234"
    }
}

HOSPITALS = {
    "HOSP-001": {"name": "Lagos University Teaching Hospital", "admin_pin": "0000"},
    "HOSP-002": {"name": "Abuja General Hospital", "admin_pin": "0000"}
}

# ── SESSION STATE ──
for key, val in {
    "hosp_auth": False, "hosp_code": "", "hospital_target": None,
    "hosp_access_granted": False, "active_patient": None,
    "chat_history": [], "summary": None, "edit_mode": False,
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ── HELPERS ──
def get_patient(pid):
    return PATIENTS.get(pid)

def auth_hospital(code, pin):
    h = HOSPITALS.get(code)
    return h and h["admin_pin"] == pin

def update_patient(pid, updates):
    if pid in PATIENTS:
        for k, v in updates.items():
            PATIENTS[pid][k] = v
        return True
    return False

def add_history_entry(pid, entry):
    if pid in PATIENTS:
        PATIENTS[pid]["medical_history"].append(entry)
        return True
    return False

def format_history_for_prompt(history):
    if not history:
        return "No records."
    lines = []
    for i, v in enumerate(history, 1):
        lines.append(f"Visit {i}: {v['date']} — {v['hospital']}")
        lines.append(f"  Diagnosis: {v['diagnosis']}")
        lines.append(f"  Notes: {v['notes']}")
        if v.get('medications_prescribed'):
            lines.append(f"  Meds: {', '.join(v['medications_prescribed'])}")
        lines.append("")
    return "\n".join(lines)

def gemini_available():
    return bool(st.session_state.get("gemini_api_key", ""))

def call_gemini(prompt):
    try:
        genai.configure(api_key=st.session_state.gemini_api_key)
        model = genai.GenerativeModel("gemini-2.0-flash")
        resp = model.generate_content(prompt)
        return resp.text
    except Exception:
        return None

def chatbot_respond(patient, query):
    if gemini_available():
        ctx = (
            f"You are a clinical AI assistant. Answer concisely using only the data provided.\n\n"
            f"PATIENT: {patient['name']}, {patient['age']}yo, {patient['gender']}\n"
            f"Blood: {patient['blood_group']} | Allergies: {', '.join(patient['allergies'])}\n"
            f"Conditions: {', '.join(patient['conditions'])} | Meds: {', '.join(patient['medications'])}\n\n"
            f"HISTORY:\n{format_history_for_prompt(patient.get('medical_history', []))}\n\n"
            f"QUESTION: {query}\n\nAnswer concisely referencing specific data."
        )
        r = call_gemini(ctx)
        if r:
            return r

    q = query.lower()
    if "summarize" in q and ("visit" in q or "history" in q):
        h = patient.get("medical_history", [])
        if not h:
            return "No records."
        parts = ["**📋 All Visits**"]
        for v in reversed(h):
            parts.append(f"**{v['date']}** — {v['hospital']}: {v['diagnosis']}")
        return "\n\n".join(parts)
    if "timeline" in q:
        h = patient.get("medical_history", [])
        return "**Timeline:**\n" + "\n".join(f"• {v['date']} — {v['diagnosis']}" for v in h) if h else "None"
    if "allerg" in q:
        a = patient.get("allergies", [])
        return f"**Allergies:** {', '.join(a) if a else 'None known'}"
    if "medication" in q or "drug" in q or "prescri" in q:
        m = patient.get("medications", [])
        return f"**Current Meds:** {', '.join(m) if m else 'None'}"
    if "condition" in q or "chronic" in q or "diagnos" in q:
        c = patient.get("conditions", [])
        return f"**Conditions:** {', '.join(c) if c else 'None'}"
    if "risk" in q:
        parts = [f"• {c}" for c in patient.get("conditions", [])]
        for a in patient.get("allergies", []):
            parts.append(f"• Allergy: {a}")
        h = patient.get("medical_history", [])
        if h:
            parts.append(f"• {len(h)} prior visits")
        return "**Risk Factors:**\n" + ("\n".join(parts) if parts else "None")
    if "emergency" in q:
        parts = [f"• {c}" for c in patient.get("conditions", [])]
        for a in patient.get("allergies", []):
            parts.append(f"• Allergy risk: {a}")
        return "**Emergency Concerns:**\n" + ("\n".join(parts) if parts else "None")
    if "history" in q or "past" in q:
        h = patient.get("medical_history", [])
        if not h:
            return "No records."
        return f"**Most Recent:** {h[-1]['date']} — {h[-1]['hospital']}: {h[-1]['diagnosis']}"
    if "blood" in q or "group" in q:
        return f"**Blood Group:** {patient['blood_group']}"
    if "contact" in q:
        return f"**Emergency Contact:** {patient.get('emergency_contact', 'N/A')}"
    return (f"**{patient['name']}** ({patient['age']}yo, {patient['blood_group']}) | "
            f"Conditions: {', '.join(patient.get('conditions', ['None']))}")

def generate_summary(p):
    if gemini_available():
        prompt = (
            f"Generate a structured clinical summary with sections: "
            f"## Clinical Summary, ### Key Conditions, ### Treatment Timeline, "
            f"### Risk Factors, ### Medication Warnings, ### Emergency Alerts.\n\n"
            f"Patient: {p['name']}, {p['age']}yo, {p['gender']}, Blood {p['blood_group']}\n"
            f"Allergies: {', '.join(p['allergies'])}\n"
            f"Conditions: {', '.join(p['conditions'])}\n"
            f"Current Meds: {', '.join(p['medications'])}\n\n"
            f"Medical History:\n{format_history_for_prompt(p.get('medical_history', []))}\n"
            f"NIN: {p['nin_linked']}"
        )
        r = call_gemini(prompt)
        if r:
            return r
    h = p.get("medical_history", [])
    lines = [
        "## 🏥 Clinical Summary",
        f"**Patient:** {p['name']} ({p['age']}y, {p['gender']}) — Blood {p['blood_group']}",
        f"**NIN:** {'✅ Linked' if p['nin_linked']=='YES' else '❌ Not linked'}",
        "",
        "### Key Conditions",
    ]
    for c in p['conditions']:
        lines.append(f"- {c}")
    lines.extend(["", "### Treatment Timeline"])
    for v in h:
        lines.append(f"- **{v['date']}** — {v['hospital']}: {v['diagnosis']}")
    lines.extend(["", "### Risk Factors"])
    for c in p['conditions']:
        lines.append(f"- {c}")
    for a in p.get('allergies', []):
        lines.append(f"- Allergy: {a}")
    lines.extend(["", "### Medication Warnings"])
    for m in p.get('medications', []):
        lines.append(f"- {m}")
    lines.extend(["", "### Emergency Alerts"])
    kw = {'asthma', 'diabetes', 'hypertension', 'stroke', 'pregnancy', 'anaphylaxis', 'allerg'}
    for a in p.get('allergies', []):
        lines.append(f"- ⚠️ {a}")
    for c in p['conditions']:
        if any(k in c.lower() for k in kw):
            lines.append(f"- 🚨 {c}")
    lines.extend(["", "---", f"*Generated by MediVault PHR · {datetime.now().strftime('%Y-%m-%d %H:%M')}*"])
    return "\n".join(lines)

# ── RENDER ──
def render_patient_record(p):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='card-white'>", unsafe_allow_html=True)
        st.markdown("### Personal Information")
        st.markdown(f"**Name:** {p['name']}")
        st.markdown(f"**ID:** `{p['patient_id']}`")
        st.markdown(f"**Age:** {p['age']}  |  **Gender:** {p['gender']}")
        st.markdown(f"**Blood Group:** `{p['blood_group']}`")
        nin = p.get('nin_linked', 'NO')
        b = f"<span class='badge-green'>YES</span>" if nin == 'YES' else f"<span class='badge-red'>NO</span>"
        st.markdown(f"**NIN:** {b}", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='card-white'>", unsafe_allow_html=True)
        st.markdown("### Medical Status")
        st.markdown(f"**Allergies:** {', '.join(p['allergies']) if p['allergies'] else 'None'}")
        st.markdown("**Conditions:**")
        for c in p['conditions']:
            st.markdown(f"- {c}")
        st.markdown("**Current Meds:**")
        for m in p['medications']:
            st.markdown(f"- {m}")
        st.markdown("</div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='card-white'>", unsafe_allow_html=True)
        st.markdown("### Emergency Contact")
        st.markdown(f"**Contact:** {p['emergency_contact']}")
        st.markdown("</div>", unsafe_allow_html=True)

def render_medical_history(history):
    st.markdown("<div class='card-white'>", unsafe_allow_html=True)
    st.markdown("### Medical History")
    if not history:
        st.info("No records.")
    else:
        st.markdown(f"*{len(history)} visit(s)*")
        for entry in reversed(history):
            st.markdown(f"""
<div style='padding:0.8rem;margin-bottom:0.5rem;background:#f8f9fa;border-radius:8px;border-left:3px solid #1565C0;'>
    <div style='display:flex;justify-content:space-between;'>
        <strong>{entry['hospital']}</strong>
        <span style='color:#666;font-size:0.85rem;'>{entry['date']}</span>
    </div>
    <div style='color:#666;font-size:0.85rem;'>{entry.get('department','')} &middot; {entry.get('doctor','N/A')}</div>
    <div><strong>DX:</strong> {entry['diagnosis']}</div>
    <div>{entry['notes']}</div>
""", unsafe_allow_html=True)
            if entry.get("medications_prescribed"):
                st.markdown(f"**Meds:** {', '.join(entry['medications_prescribed'])}")
            st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

def render_edit_form(p):
    st.markdown("<div class='card-white'>", unsafe_allow_html=True)
    st.markdown("### Edit Medical Record")
    tabs = st.tabs(["Conditions & Meds", "Add New Visit"])
    with tabs[0]:
        nc = st.text_area("Conditions (one per line)", value="\n".join(p.get("conditions", [])), key="ec")
        na = st.text_area("Allergies (one per line)", value="\n".join(p.get("allergies", [])), key="ea")
        nm = st.text_area("Medications (one per line)", value="\n".join(p.get("medications", [])), key="em")
        if st.button("Save", type="primary", key="save_med"):
            update_patient(p['patient_id'], {
                "conditions": [x.strip() for x in nc.split("\n") if x.strip()],
                "allergies": [x.strip() for x in na.split("\n") if x.strip()],
                "medications": [x.strip() for x in nm.split("\n") if x.strip()]
            })
            st.success("Saved!")
            st.rerun()
    with tabs[1]:
        vh = st.text_input("Hospital", placeholder="e.g. LUTH", key="evh")
        vd = st.date_input("Date", key="evd")
        vdx = st.text_input("Diagnosis", key="evdx")
        vn = st.text_area("Notes", key="evn")
        vm = st.text_input("Medications (comma-sep)", key="evm")
        vdr = st.text_input("Doctor", key="evdr")
        if st.button("Add Visit", type="primary", key="save_visit"):
            if vh and vdx:
                add_history_entry(p['patient_id'], {
                    "hospital": vh, "date": str(vd),
                    "diagnosis": vdx, "notes": vn or "No notes.",
                    "medications_prescribed": [x.strip() for x in vm.split(",") if x.strip()],
                    "doctor": vdr or "Unknown", "department": "General"
                })
                st.success("Visit added!")
                st.rerun()
            else:
                st.error("Hospital and Diagnosis required.")
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════
# UI
# ══════════════════════════════════════════

# ── SIDEBAR ──
with st.sidebar:
    st.markdown("<div style='text-align:center;padding:0.5rem 0;'>"
                "<h2 style='color:#000000;margin:0;border:none;'>🏥 MediVault PHR</h2>"
                "<p style='color:#333333;font-size:0.8rem;margin:0;'>Hospital Access Portal</p></div>",
                unsafe_allow_html=True)
    st.divider()

    if not st.session_state.hosp_auth:
        st.markdown("#### 🔐 Hospital Login")
        hc = st.text_input("Hospital Code", placeholder="e.g. HOSP-001", key="side_hc", label_visibility="collapsed")
        hp = st.text_input("PIN", type="password", placeholder="0000", key="side_hp", label_visibility="collapsed")
        if st.button("🔑 Authenticate", use_container_width=True, key="side_auth"):
            if auth_hospital(hc, hp):
                st.session_state.hosp_auth = True
                st.session_state.hosp_code = hc
                st.rerun()
            else:
                st.error("❌ Invalid credentials")
    else:
        hname = HOSPITALS.get(st.session_state.hosp_code, {}).get("name", "")
        st.markdown(f"<span class='badge-green'>✅ {hname}</span>", unsafe_allow_html=True)
        with st.expander("🔑 Change PIN"):
            cur = st.text_input("Current PIN", type="password", key="chg_cur")
            new1 = st.text_input("New PIN", type="password", key="chg_new1")
            new2 = st.text_input("Confirm PIN", type="password", key="chg_new2")
            if st.button("Update PIN", use_container_width=True, key="chg_btn"):
                h = HOSPITALS.get(st.session_state.hosp_code)
                if h and cur == h["admin_pin"] and new1 == new2 and len(new1) >= 4:
                    h["admin_pin"] = new1
                    st.success("✅ PIN updated")
                elif not h or cur != h["admin_pin"]:
                    st.error("❌ Current PIN incorrect")
                elif new1 != new2:
                    st.error("❌ New PINs don't match")
                else:
                    st.error("❌ PIN must be at least 4 characters")
        if st.button("🚪 Logout", use_container_width=True, key="side_logout"):
            for k in ["hosp_auth", "hosp_code", "hospital_target", "hosp_access_granted",
                       "active_patient", "chat_history", "summary"]:
                st.session_state[k] = False if isinstance(st.session_state.get(k), bool) else ("" if isinstance(st.session_state.get(k), str) else None if k != "chat_history" else [])
            st.rerun()

    st.divider()
    ai_status = "✅ AI Connected" if st.session_state.gemini_api_key else "⚡ Mock AI Active"
    ai_badge = "badge-green" if st.session_state.gemini_api_key else "badge-blue"
    st.markdown(f"<span class='{ai_badge}'>{ai_status}</span>", unsafe_allow_html=True)

    st.markdown("**Hospital PIN:** `0000`")
    st.caption("v2.0 · 234Hackathon 2026")

# ── MAIN ──
st.markdown("""
<div style='display:flex;justify-content:space-between;align-items:center;padding:0.2rem 0 0 0;'>
    <div>
        <h1 style='color:#000000;margin:0;font-size:1.6rem;border:none;'>🏥 MediVault PHR Pro</h1>
        <p style='color:#333333;margin:0;font-size:0.85rem;'>Portable Health Record · Hospital Access Only</p>
    </div>
</div>
""", unsafe_allow_html=True)
st.divider()

if not st.session_state.hosp_auth:
    st.markdown("<div style='text-align:center;padding:3rem 1rem;'>"
                "<div style='font-size:4rem;margin-bottom:1rem;'>🏥</div>"
                "<h2 style='color:#000000;'>Welcome to MediVault PHR</h2>"
                "<p style='color:#333333;max-width:500px;margin:0 auto 1.5rem auto;'>"
                "Authorized hospital staff can access patient records securely. "
                "Authenticate via the sidebar to begin.</p>"
                "<p style='color:#666666;font-size:0.85rem;'>Demo: HOSP-001 / PIN: 0000</p>"
                "</div>", unsafe_allow_html=True)
else:
    # ── SEARCH ──
    st.markdown("<div class='search-container'>"
                "<div class='search-title'>🔍 Patient Search</div>",
                unsafe_allow_html=True)
    scol1, scol2 = st.columns([4, 1])
    with scol1:
        search_pid = st.text_input("", placeholder="Enter Patient ID (e.g. MH-001, MH-002...)",
                                   key="main_search", label_visibility="collapsed")
    with scol2:
        if st.button("🔍 Find Patient", use_container_width=True, key="main_find"):
            p = get_patient(search_pid)
            if p:
                st.session_state.hospital_target = p
                st.session_state.hosp_access_granted = False
            else:
                st.error("Patient not found")
                st.session_state.hospital_target = None
    st.markdown("<div style='text-align:center;margin:0.5rem 0;'>"
                "<span style='color:#999;font-size:0.8rem;'>or scan fingerprint</span></div>",
                unsafe_allow_html=True)
    if st.button("🖐️ Tap Fingerprint", use_container_width=True, key="fp_scan"):
        pid = random.choice(list(PATIENTS.keys()))
        p = PATIENTS[pid]
        st.session_state.hospital_target = p
        st.session_state.hosp_access_granted = False
        st.info(f"Fingerprint matched — {p['name']}")
    st.markdown("</div>", unsafe_allow_html=True)

    # ── RECORD ──
    if st.session_state.hospital_target:
        p = st.session_state.hospital_target

        if not st.session_state.hosp_access_granted:
            c1, c2 = st.columns([1, 1])
            with c1:
                if st.button("📋 Request Access", use_container_width=True, key="req_access"):
                    st.info("⏳ Request sent to patient...")
            with c2:
                if st.button("✅ Simulate Patient Approval", type="primary", use_container_width=True, key="approve"):
                    st.session_state.hosp_access_granted = True
                    st.session_state.active_patient = p
                    st.rerun()
        else:
            st.success("Access approved")
            render_patient_record(p)
            render_medical_history(p.get("medical_history", []))

            st.markdown("---")
            with st.expander("Edit Medical Record"):
                render_edit_form(p)

            st.markdown("---")
            st.markdown("<div class='section-label'>AI Clinical Assistant</div>", unsafe_allow_html=True)

            aicol1, aicol2 = st.columns([1, 1])

            with aicol1:
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.markdown("#### Chat")
                suggestions = [
                    "Does this patient have allergies?",
                    "What are the chronic conditions?",
                    "Summarize all hospital visits",
                    "What medications is the patient on?"
                ]
                for i, s in enumerate(suggestions):
                    if st.button(s, key=f"ai_sug_{i}", use_container_width=True):
                        resp = chatbot_respond(p, s)
                        st.session_state.chat_history.append({"role": "user", "content": s})
                        st.session_state.chat_history.append({"role": "assistant", "content": resp})
                        st.rerun()
                chat_container = st.container(height=240)
                with chat_container:
                    if not st.session_state.chat_history:
                        st.caption("No messages yet.")
                    for msg in st.session_state.chat_history:
                        with st.chat_message(msg["role"]):
                            st.markdown(msg["content"])
                user_q = st.chat_input("Ask about this patient...")
                if user_q:
                    resp = chatbot_respond(p, user_q)
                    st.session_state.chat_history.append({"role": "user", "content": user_q})
                    st.session_state.chat_history.append({"role": "assistant", "content": resp})
                    st.rerun()
                if st.session_state.chat_history:
                    if st.button("Clear", key="clear_chat"):
                        st.session_state.chat_history = []
                        st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

            with aicol2:
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.markdown("#### Clinical Summary")
                if st.button("Generate Summary", type="primary", use_container_width=True, key="gen_summary"):
                    with st.spinner("Generating..."):
                        time.sleep(0.3)
                        st.session_state.summary = generate_summary(p)
                if st.session_state.summary:
                    with st.container(border=True):
                        st.markdown(st.session_state.summary)
                st.markdown("</div>", unsafe_allow_html=True)
