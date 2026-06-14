import streamlit as st
import time
import random
from datetime import datetime, date

st.set_page_config(page_title="medID", page_icon="🆔", layout="wide")

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

.card { background: #f8f9fa; border-radius: 12px; padding: 1.3rem; margin-bottom: 1rem; border: 1px solid #e0e0e0; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
.card h3, .card p, .card li, .card span, .card strong { color: #000000 !important; }

.card-white { background: #ffffff; border-radius: 12px; padding: 1.3rem; margin-bottom: 1rem; border: 1px solid #e0e0e0; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
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
section[data-testid="stSidebar"] .stButton button { background: #e0e0e0; color: #000000; border: 1px solid #ccc; border-radius: 8px; }
section[data-testid="stSidebar"] .stTextInput input { background: #ffffff; color: #000000; border: 1px solid #ccc; border-radius: 8px; }
section[data-testid="stSidebar"] .stTextInput input::placeholder { color: #999; }

.stButton button { border-radius: 8px; font-weight: 500; }
button[kind="primary"] { background: #1565C0 !important; border: none !important; font-weight: 600 !important; color: white !important; }
.stButton button:not([kind="primary"]) { background: #e0e0e0; color: #000000; border: 1px solid #ccc; }

.stTextInput input, .stTextArea textarea, .stDateInput input { background: #ffffff !important; color: #000000 !important; border: 1px solid #ccc !important; border-radius: 8px !important; }
.stTextInput input::placeholder, .stTextArea textarea::placeholder { color: #999 !important; }
.stTextInput input:focus, .stTextArea textarea:focus { border-color: #1565C0 !important; }
[data-testid="stChatInput"] textarea, [data-testid="stChatInput"] input { color: #000000 !important; background: #ffffff !important; border: 1px solid #ccc !important; }

.stAlert { border-left-width: 4px !important; }
.stSuccess { border-left-color: #4caf50 !important; }
.stError { border-left-color: #f44336 !important; }

.stMetric { background: #f5f5f5; border-radius: 8px; padding: 0.8rem; border: 1px solid #e0e0e0; }
[data-testid="stMetricValue"] { color: #000000 !important; font-weight: 800; }
[data-testid="stMetricLabel"] p { color: #333 !important; font-weight: 600 !important; }

.badge-green { display: inline-block; background: #e8f5e9; color: #2e7d32; padding: 0.2rem 0.7rem; border-radius: 12px; font-size: 0.78rem; font-weight: 700; border: 1px solid #4caf50; }
.badge-red { display: inline-block; background: #fce4ec; color: #c62828; padding: 0.2rem 0.7rem; border-radius: 12px; font-size: 0.78rem; font-weight: 700; border: 1px solid #e53935; }
.badge-blue { display: inline-block; background: #e3f2fd; color: #1565C0; padding: 0.2rem 0.7rem; border-radius: 12px; font-size: 0.78rem; font-weight: 700; border: 1px solid #42a5f5; }

.search-container { background: #f8f9fa; border-radius: 12px; padding: 1.5rem 2rem; margin: 1rem 0; border: 1px solid #e0e0e0; text-align: center; }
.search-title { color: #1565C0; font-size: 0.85rem; margin-bottom: 0.5rem; letter-spacing: 1.5px; text-transform: uppercase; font-weight: 700; }
.search-container .stTextInput input { background: #ffffff !important; border-color: #1565C0 !important; }

.section-label { color: #1565C0; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 0.75rem; font-weight: 700; }
.stAlert p { font-weight: 500; color: #000000 !important; }
.emoji { font-size: 1.5em !important; }
h1 .emoji { font-size: 2rem !important; }
.badge-green, .badge-red, .badge-blue { font-size: 0.9rem !important; }
.fp-container { text-align: center; padding: 1rem 0; }
.fp-svg { width: 64px; height: 64px; cursor: pointer; transition: all 0.3s; }
.fp-svg:hover { transform: scale(1.1); }
.fp-svg-idle .fp-outer { stroke: #999; } .fp-svg-idle .fp-inner { fill: #999; }
.fp-svg-scanning .fp-outer { stroke: #1565C0; } .fp-svg-scanning .fp-inner { fill: #1565C0; }
.fp-svg-scanning { animation: fp-pulse 0.8s ease-in-out infinite; }
.fp-svg-success .fp-outer { stroke: #2e7d32; } .fp-svg-success .fp-inner { fill: #2e7d32; }
.fp-svg-fail .fp-outer { stroke: #c62828; } .fp-svg-fail .fp-inner { fill: #c62828; }
@keyframes fp-pulse { 0% { opacity: 0.6; } 50% { opacity: 1; } 100% { opacity: 0.6; } }
.fp-status { font-size: 0.9rem; margin-top: 0.3rem; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# ── GEMINI SETUP ──
import google.generativeai as genai

GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
if "gemini_api_key" not in st.session_state:
    st.session_state.gemini_api_key = GEMINI_API_KEY

# ── DATABASES (session-persisted) ──
if "PATIENTS" not in st.session_state:
    st.session_state.PATIENTS = {
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

if "HOSPITALS" not in st.session_state:
    st.session_state.HOSPITALS = {
        "HOSP-001": {"name": "Lagos University Teaching Hospital", "admin_pin": "0000"},
        "HOSP-002": {"name": "Abuja General Hospital", "admin_pin": "0000"}
    }

# ── SESSION STATE ──
for key, val in {
    "hosp_auth": False, "hosp_code": "", "hospital_target": None,
    "hosp_access_granted": False, "active_patient": None,
    "chat_history": [], "summary": None, "edit_mode": False,
    "fp_status": "idle", "fp_patient": None,
    "access_consent": False, "access_reason": "", "access_doctor": "",
    "reg_success": False,
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ── HELPERS ──
def get_patient(pid):
    return st.session_state.PATIENTS.get(pid)

def auth_hospital(code, pin):
    h = st.session_state.HOSPITALS.get(code)
    return h and h["admin_pin"] == pin

def update_patient(pid, updates):
    if pid in st.session_state.PATIENTS:
        for k, v in updates.items():
            st.session_state.PATIENTS[pid][k] = v
        return True
    return False

def add_history_entry(pid, entry):
    if pid in st.session_state.PATIENTS:
        st.session_state.PATIENTS[pid]["medical_history"].append(entry)
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
            f"Answer the question directly using the patient data below. "
            f"Do NOT repeat the question. Do NOT use phrases like 'Based on the data' or 'According to the records'. "
            f"Just give a short, precise answer.\n\n"
            f"Patient: {patient['name']}, {patient['age']}yo, {patient['gender']}\n"
            f"Blood: {patient['blood_group']} | Allergies: {', '.join(patient['allergies'])}\n"
            f"Conditions: {', '.join(patient['conditions'])} | Meds: {', '.join(patient['medications'])}\n\n"
            f"History:\n{format_history_for_prompt(patient.get('medical_history', []))}\n\n"
            f"Q: {query}\nA:"
        )
        r = call_gemini(ctx)
        if r:
            return r

    q = query.lower()
    if "allerg" in q:
        a = patient.get("allergies", [])
        return f"{', '.join(a) if a else 'No known allergies'}"
    if "medication" in q or "drug" in q or "prescri" in q:
        m = patient.get("medications", [])
        return f"{', '.join(m) if m else 'No current medications'}"
    if "condition" in q or "chronic" in q or "diagnos" in q:
        c = patient.get("conditions", [])
        return f"{', '.join(c) if c else 'No chronic conditions'}"
    if "history" in q or "past" in q or "visit" in q:
        h = patient.get("medical_history", [])
        if not h:
            return "No medical history on record"
        return f"Most recent: {h[-1]['date']} at {h[-1]['hospital']} — {h[-1]['diagnosis']}. Total: {len(h)} visit(s)."
    if "summarize" in q:
        h = patient.get("medical_history", [])
        parts = [f"{v['date']} — {v['hospital']}: {v['diagnosis']}" for v in reversed(h)]
        return "\n".join(parts) if parts else "No records"
    if "risk" in q or "emergency" in q:
        items = list(patient.get("conditions", []))
        items += [f"Allergy: {a}" for a in patient.get("allergies", [])]
        return ", ".join(items) if items else "No significant risks identified"
    if "blood" in q or "group" in q:
        return patient['blood_group']
    if "contact" in q:
        return patient.get('emergency_contact', 'N/A')
    return f"{patient['name']}, {patient['age']}yo, {patient['blood_group']}. Conditions: {', '.join(patient.get('conditions', ['None']))}"

def generate_summary(p):
    if gemini_available():
        prompt = (
            f"You are a doctor's clinical assistant. Generate a VERY BRIEF summary (max 5 bullet points). "
            f"Focus ONLY on: critical conditions, emergency risks, cross-hospital medication conflicts, "
            f"and immediate action items. No greetings, no fluff.\n\n"
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
    alerts = []
    for c in p['conditions']:
        alerts.append(f"🚨 {c}")
    for a in p.get('allergies', []):
        alerts.append(f"⚠️ Allergy: {a}")
    timeline = "\n".join(f"- {v['date']} — {v['hospital']}: {v['diagnosis']}" for v in h[-3:]) if h else "None"
    lines = [
        "### Critical Conditions & Alerts",
        "\n".join(alerts) if alerts else "None",
        "",
        "### Recent Visits (Last 3)",
        timeline,
        "",
        "### Current Medications",
        ", ".join(p['medications']) if p['medications'] else "None",
        "",
        f"**Blood:** {p['blood_group']} | **NIN:** {'Linked' if p['nin_linked']=='YES' else 'Not linked'}",
        "---",
        f"*medID · {datetime.now().strftime('%Y-%m-%d %H:%M')}*"
    ]
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
        st.markdown(f"**NIN Linked:** {b}", unsafe_allow_html=True)
        with st.expander("Link / Unlink NIN"):
            nin_input = st.text_input("NIN Number", placeholder="Enter 11-digit NIN", key=f"nin_{p['patient_id']}")
            if st.button("Link NIN", key=f"link_nin_{p['patient_id']}"):
                st.session_state.PATIENTS[p['patient_id']]['nin_linked'] = "YES"
                st.success("NIN linked!")
                st.rerun()
            if nin == "YES" and st.button("Unlink NIN", key=f"unlink_nin_{p['patient_id']}"):
                st.session_state.PATIENTS[p['patient_id']]['nin_linked'] = "NO"
                st.success("NIN unlinked!")
                st.rerun()
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
    pid = p['patient_id']
    history = st.session_state.PATIENTS[pid].get("medical_history", [])
    hospitals = list(set(v["hospital"] for v in history)) if history else []
    tabs = st.tabs(["Edit / Delete Visit", "Add New Visit"])
    with tabs[0]:
        if not hospitals:
            st.info("No hospital records to edit.")
        else:
            sel_hosp = st.selectbox("Select hospital", hospitals, key="sel_hosp")
            entries = [v for v in history if v["hospital"] == sel_hosp]
            if entries:
                idx = st.selectbox("Select date", range(len(entries)), format_func=lambda i: entries[i]["date"], key="sel_visit_idx")
                entry = entries[idx]
                ed_dx = st.text_input("Diagnosis", value=entry.get("diagnosis", ""), key="ed_dx")
                ed_notes = st.text_area("Notes", value=entry.get("notes", ""), key="ed_notes")
                ed_meds = st.text_input("Medications (comma-sep)", value=", ".join(entry.get("medications_prescribed", [])), key="ed_meds")
                ed_doc = st.text_input("Doctor", value=entry.get("doctor", ""), key="ed_doc")
                col_save, col_del = st.columns([1, 1])
                with col_save:
                    if st.button("Save Changes", type="primary", use_container_width=True, key="save_edit_visit"):
                        hv = st.session_state.PATIENTS[pid]["medical_history"]
                        for i, v in enumerate(hv):
                            if v["hospital"] == sel_hosp and v["date"] == entry["date"]:
                                hv[i]["diagnosis"] = ed_dx
                                hv[i]["notes"] = ed_notes
                                hv[i]["medications_prescribed"] = [x.strip() for x in ed_meds.split(",") if x.strip()]
                                hv[i]["doctor"] = ed_doc
                                break
                        st.success("Visit updated!")
                        st.rerun()
                with col_del:
                    if st.button("Delete Visit", use_container_width=True, key="del_visit"):
                        hv = st.session_state.PATIENTS[pid]["medical_history"]
                        st.session_state.PATIENTS[pid]["medical_history"] = [v for v in hv if not (v["hospital"] == sel_hosp and v["date"] == entry["date"])]
                        st.success("Visit deleted!")
                        st.rerun()
    with tabs[1]:
        vh = st.text_input("Hospital", placeholder="e.g. LUTH", key="evh")
        c1, c2, c3 = st.columns(3)
        with c1:
            vy = st.text_input("Year", placeholder="YYYY", max_chars=4, key="evy")
        with c2:
            vm = st.text_input("Month", placeholder="MM", max_chars=2, key="evmth")
        with c3:
            vd = st.text_input("Day", placeholder="DD", max_chars=2, key="evd")
        vdx = st.text_input("Diagnosis", key="evdx")
        vn = st.text_area("Notes", key="evn")
        vm2 = st.text_input("Medications (comma-sep)", key="evm2")
        vdr = st.text_input("Doctor", key="evdr")
        if st.button("Add Visit", type="primary", key="save_visit"):
            if vh and vdx:
                date_str = f"{vy}/{vm}/{vd}" if vy and vm and vd else "Unknown"
                add_history_entry(pid, {
                    "hospital": vh, "date": date_str,
                    "diagnosis": vdx, "notes": vn or "No notes.",
                    "medications_prescribed": [x.strip() for x in vm2.split(",") if x.strip()],
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
                "<h2 style='color:#000000;margin:0;border:none;'>medID</h2>"
                "<p style='color:#333333;font-size:0.8rem;margin:0;'>Patient Identity Portal</p></div>",
                unsafe_allow_html=True)
    st.divider()

    if not st.session_state.hosp_auth:
        st.markdown("<div style='text-align:center;padding:0.5rem 0;color:#999;font-size:0.85rem;'>Not logged in</div>", unsafe_allow_html=True)
    else:
        hname = st.session_state.HOSPITALS.get(st.session_state.hosp_code, {}).get("name", "")
        st.markdown(f"<span class='badge-green'>✅ {hname}</span>", unsafe_allow_html=True)
        st.markdown(f"**Code:** `{st.session_state.hosp_code}`", unsafe_allow_html=True)
        with st.expander("⚙️ Settings"):
            st.markdown("#### Hospital Info")
            new_name = st.text_input("Hospital Name", value=hname, key="set_hosp_name")
            if st.button("Update Name", use_container_width=True, key="set_save_name"):
                st.session_state.HOSPITALS[st.session_state.hosp_code]["name"] = new_name
                st.success("Name updated!")
                st.rerun()
            st.divider()
            st.markdown("#### Change PIN")
            cur = st.text_input("Current PIN", type="password", placeholder="0000", key="chg_cur")
            new1 = st.text_input("New PIN", type="password", placeholder="New PIN (4+ digits)", key="chg_new1")
            new2 = st.text_input("Confirm PIN", type="password", placeholder="Confirm new PIN", key="chg_new2")
            if st.button("Update PIN", use_container_width=True, key="chg_btn"):
                h = st.session_state.HOSPITALS.get(st.session_state.hosp_code)
                cur_stripped = cur.strip() if cur else ""
                new1_stripped = new1.strip() if new1 else ""
                new2_stripped = new2.strip() if new2 else ""
                if h and cur_stripped == str(h["admin_pin"]).strip() and new1_stripped == new2_stripped and len(new1_stripped) >= 4:
                    h["admin_pin"] = new1_stripped
                    st.success("✅ PIN updated")
                    st.rerun()
                elif not h or cur_stripped != str(h["admin_pin"]).strip():
                    st.error("❌ Current PIN incorrect")
                elif new1_stripped != new2_stripped:
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

# ── MAIN ──
st.markdown("""
<div style='display:flex;justify-content:space-between;align-items:center;padding:0.2rem 0 0 0;'>
    <div>
        <h1 style='color:#000000;margin:0;font-size:1.6rem;border:none;'>medID</h1>
        <p style='color:#333333;margin:0;font-size:0.85rem;'>Patient Identity Portal</p>
    </div>
</div>
""", unsafe_allow_html=True)
st.divider()

if not st.session_state.hosp_auth:
    col_left, col_center, col_right = st.columns([1, 2, 1])
    with col_center:
        st.markdown("<div style='text-align:center;padding:1rem 0 0.5rem 0;'>"
                    "<div style='font-size:3rem;margin-bottom:0.5rem;'>🆔</div>"
                    "<h2 style='color:#000000;margin:0;'>Welcome to medID</h2>"
                    "<p style='color:#333333;margin:0.3rem 0 1rem 0;'>Patient Identity Portal</p>"
                    "</div>", unsafe_allow_html=True)
        auth_tab = st.radio("", ["Login", "Sign Up"], horizontal=True, key="main_auth_tab", label_visibility="collapsed")
        if auth_tab == "Login":
            if st.session_state.get("reg_success"):
                st.success("Hospital registered successfully! You can now log in.")
                st.session_state.reg_success = False
            st.markdown("<div class='card-white'>", unsafe_allow_html=True)
            st.markdown("#### Hospital Login")
            hc = st.text_input("Hospital Code", placeholder="e.g. HOSP-001", key="main_hc")
            hp = st.text_input("PIN", type="password", placeholder="Enter your PIN", key="main_hp")
            if st.button("Authenticate", use_container_width=True, type="primary", key="main_auth"):
                if auth_hospital(hc, hp):
                    st.session_state.hosp_auth = True
                    st.session_state.hosp_code = hc
                    st.rerun()
                else:
                    st.error("Invalid hospital code or PIN")
            st.markdown("<p style='text-align:center;color:#999;font-size:0.85rem;margin-top:0.5rem;'>Demo: HOSP-001 / PIN: 0000</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='card-white'>", unsafe_allow_html=True)
            st.markdown("#### Hospital Sign Up")
            reg_code = st.text_input("Hospital Code", placeholder="e.g. HOSP-003", key="main_reg_code")
            reg_name = st.text_input("Hospital Name", placeholder="e.g. City General Hospital", key="main_reg_name")
            reg_pin = st.text_input("Create PIN", type="password", placeholder="Minimum 4 digits", key="main_reg_pin")
            reg_confirm = st.text_input("Confirm PIN", type="password", placeholder="Re-enter PIN", key="main_reg_confirm")
            if st.button("Register Hospital", use_container_width=True, type="primary", key="main_reg_btn"):
                if not reg_code or not reg_name or not reg_pin:
                    st.error("All fields required")
                elif reg_pin != reg_confirm:
                    st.error("PINs don't match")
                elif len(reg_pin) < 4:
                    st.error("PIN must be at least 4 characters")
                elif reg_code in st.session_state.HOSPITALS:
                    st.error("Hospital code already exists")
                else:
                    st.session_state.HOSPITALS[reg_code] = {"name": reg_name, "admin_pin": reg_pin}
                    st.session_state.main_auth_tab = "Login"
                    st.session_state.reg_success = True
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
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
    fp_state = st.session_state.fp_status
    fp_class = {"idle": "fp-svg-idle", "scanning": "fp-svg-scanning", "success": "fp-svg-success", "fail": "fp-svg-fail"}
    fp_text = {"idle": "Tap to scan", "scanning": "Scanning...", "success": "", "fail": "No match found"}
    fp_text_color = {"idle": "#999", "scanning": "#1565C0", "success": "#2e7d32", "fail": "#c62828"}
    st.markdown(f"""
<div class='fp-container'>
    <svg class='fp-svg {fp_class.get(fp_state, "fp-svg-idle")}' viewBox='0 0 48 48' onclick=''>
        <circle class='fp-outer' cx='24' cy='18' r='10' fill='none' stroke-width='2.5'/>
        <path class='fp-inner' d='M14 38c0-5.5 4.5-10 10-10s10 4.5 10 10M18 32c0-3.3 2.7-6 6-6s6 2.7 6 6M22 28l2 4 4-2' stroke-width='2' fill='none' stroke-linecap='round'/>
        <circle cx='24' cy='18' r='3' fill='currentColor' opacity='0.4'/>
    </svg>
    <div class='fp-status' style='color:{fp_text_color.get(fp_state, "#999")}'>{fp_text.get(fp_state, "")}</div>
</div>""", unsafe_allow_html=True)
    if fp_state == "idle" and st.button("Scan Fingerprint", use_container_width=True, key="fp_btn"):
        st.session_state.fp_status = "scanning"
        st.rerun()
    if fp_state == "scanning":
        with st.spinner(""):
            time.sleep(0.8)
            if random.random() < 0.85:
                pid = random.choice(list(st.session_state.PATIENTS.keys()))
                st.session_state.fp_status = "success"
                st.session_state.fp_patient = pid
            else:
                st.session_state.fp_status = "fail"
            st.rerun()
    if fp_state == "success":
        pid = st.session_state.fp_patient
        p = st.session_state.PATIENTS[pid]
        st.success(f"Matched — {p['name']}")
        if st.button("Continue with this patient", type="primary", use_container_width=True, key="fp_continue"):
            st.session_state.hospital_target = p
            st.session_state.hosp_access_granted = True
            st.session_state.active_patient = p
            st.session_state.fp_status = "idle"
            st.session_state.fp_patient = None
            st.rerun()
    if fp_state == "fail":
        st.error("No fingerprint match found")
        if st.button("Try Again", use_container_width=True, key="fp_retry"):
            st.session_state.fp_status = "idle"
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # ── RECORD ──
    if st.session_state.hospital_target:
        p = st.session_state.hospital_target

        if not st.session_state.hosp_access_granted:
            st.markdown("<div class='card-white'>", unsafe_allow_html=True)
            st.markdown("### Access Requirements")
            consent = st.checkbox("Patient consent obtained", key="access_consent")
            reason = st.selectbox("Reason for access", ["", "Emergency", "Routine Review", "Referral", "Administrative", "Lab Results"], key="access_reason")
            doctor = st.text_input("Attending Doctor", placeholder="Enter doctor's name", key="access_doctor")
            can_proceed = consent and reason and doctor
            col_a, col_b = st.columns([1, 1])
            with col_a:
                if st.button("Request Access", use_container_width=True, key="req_access"):
                    if can_proceed:
                        st.info("Request sent to patient...")
                    else:
                        st.warning("Complete all requirements first")
            with col_b:
                if st.button("Simulate Patient Approval", type="primary", use_container_width=True, key="approve", disabled=not can_proceed):
                    st.session_state.hosp_access_granted = True
                    st.session_state.active_patient = p
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            if st.button("← Back to Search", key="back_to_search"):
                st.session_state.hospital_target = None
                st.session_state.hosp_access_granted = False
                st.session_state.active_patient = None
                st.session_state.chat_history = []
                st.session_state.summary = None
                st.rerun()
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
