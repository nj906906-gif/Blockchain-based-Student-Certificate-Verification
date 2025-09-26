import streamlit as st
from blockchain import Blockchain
import time

st.set_page_config(page_title="Certificate Verification", layout="centered")
st.title("🎓 Blockchain-Based Certificate Verification")

# Initialize blockchain in session state
if "chain" not in st.session_state:
    st.session_state.chain = Blockchain()

chain = st.session_state.chain

tab1, tab2 = st.tabs(["📜 Issue Certificate", "🔍 Verify Certificate"])

with tab1:
    st.subheader("Issue New Certificate")
    name = st.text_input("Student Name")
    degree = st.text_input("Degree")
    year = st.text_input("Year of Graduation")
    issuer = st.text_input("Issuing Authority")

    if st.button("Issue Certificate"):
        if name and degree and year and issuer:
            cert_data = {
                "name": name,
                "degree": degree,
                "year": year,
                "issuer": issuer
            }
            last = chain.get_last_block()
            block = chain.create_block(cert_data, last['hash'])
            st.success("✅ Certificate Issued and Block Created")
            st.code(block['hash'], language='text')
        else:
            st.error("Please fill all fields.")

    st.markdown("### 🔗 Blockchain Ledger")
    for block in reversed(chain.chain):
        cert = block['certificate']
        st.markdown(f"""
        **Block {block['index']}**
        - Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(block['timestamp']))}
        - Name: {cert if isinstance(cert, str) else cert.get('name', '')}
        - Degree: {cert.get('degree', '') if isinstance(cert, dict) else ''}
        - Year: {cert.get('year', '') if isinstance(cert, dict) else ''}
        - Issuer: {cert.get('issuer', '') if isinstance(cert, dict) else ''}
        - Hash: `{block['hash']}`
        - Previous Hash: `{block['previous_hash']}`
        """)

with tab2:
    st.subheader("Verify Certificate")
    cert_hash = st.text_input("Enter Certificate Hash")

    if st.button("Verify"):
        if chain.verify_certificate(cert_hash):
            st.success("✅ Certificate is valid and exists on blockchain.")
        else:
            st.error("❌ Certificate not found or invalid.")

if st.button("Validate Blockchain Integrity"):
    if chain.is_valid():
        st.success("✅ Blockchain is valid and tamper-proof.")
    else:
        st.error("❌ Blockchain integrity compromised!")
