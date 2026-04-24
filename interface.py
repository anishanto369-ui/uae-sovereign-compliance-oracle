import streamlit as st
from agent_logic import run_uae_audit

st.set_page_config(page_title="UAE Sovereign Oracle", page_icon="🇦🇪", layout="wide")

# Institutional Sidebar
with st.sidebar:
    st.markdown("### 🇦🇪 Institutional Access")
    st.title("👤 Lead Architect")
    st.write("**Anish Anto** (MBA Finance)")
    st.success("Anthropic Certified AI Architect")
    st.divider()
    st.info("System: Sovereign Oracle v4.0")
    st.info("Sovereign Compliance: ENABLED")
    st.info("PII Redaction: ACTIVE (Law 45)")
    st.info("CBUAE PF Triangulation: ACTIVE")

st.title("🇦🇪 UAE Enterprise Compliance Oracle")
st.markdown("### *Consulting-Grade Regulatory Intelligence & Decision Support*")

query = st.text_area("Regulatory Scenario / Financial Query:", 
                     placeholder="Enter details (e.g. VAT recovery, DMCC transfers, EIDs)...",
                     height=150)

if st.button("🚀 EXECUTE INSTITUTIONAL AUDIT"):
    if query:
        with st.spinner("Analyzing across Sovereign FTA and CBUAE 2026 Data Lakes..."):
            report = run_uae_audit(query)
            st.session_state['report'] = report
            st.session_state['status'] = "🟠 DRAFT: PENDING INSTITUTIONAL VERIFICATION"
    else:
        st.warning("Please provide a query for analysis.")

# Display Report and HITL (Human-in-the-Loop) Verification Logic
if 'report' in st.session_state:
    st.markdown("---")
    st.subheader(f"Status: {st.session_state['status']}")
    
    col1, col2 = st.columns([5, 1])
    with col1:
        st.markdown(st.session_state['report'])
    
    with col2:
        if st.button("✅ VERIFY & SIGN"):
            st.session_state['status'] = "🟢 APPROVED: CERTIFIED AUDIT REPORT"
            st.rerun()
        
        st.download_button("📂 EXPORT VERIFIED MD", 
                           st.session_state['report'], 
                           file_name="UAE_Verified_Audit.md")