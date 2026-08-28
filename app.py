import io
import streamlit as st
from PIL import Image
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# --- PAGE CONFIG & SESSION STATE ---
st.set_page_config(
    page_title="TECH-OPS || CYBER COMMAND VAULT",
    page_icon="🛰️",
    layout="centered"
)

if "page" not in st.session_state:
    st.session_state.page = "home"

def set_page(page_name):
    st.session_state.page = page_name


# --- FIXED TECH-OPS CSS ---
TECHOPS_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700;800&family=Chakra+Petch:wght@600;700;800&display=swap');

/* Tactical Command Background */
.stApp {
    background-color: #070a12;
    background-image: radial-gradient(rgba(245, 158, 11, 0.08) 1px, transparent 1px);
    background-size: 24px 24px;
    color: #f8fafc;
    font-family: 'JetBrains Mono', monospace;
}

/* Tech-Ops Header */
.techops-title {
    font-family: 'Chakra Petch', sans-serif;
    font-size: 2.7rem;
    font-weight: 800;
    text-align: center;
    color: #f59e0b;
    text-shadow: 0 0 25px rgba(245, 158, 11, 0.45);
    letter-spacing: 3px;
    margin-bottom: 2px;
    text-transform: uppercase;
}

.techops-subtitle {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    text-align: center;
    color: #94a3b8;
    letter-spacing: 2px;
    margin-bottom: 25px;
    text-transform: uppercase;
}

/* Telemetry Badges */
.ops-badge {
    display: inline-block;
    padding: 3px 8px;
    font-size: 0.72rem;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700;
    border-radius: 3px;
    background: rgba(245, 158, 11, 0.08);
    border: 1px solid rgba(245, 158, 11, 0.4);
    color: #f59e0b;
    margin: 2px;
    letter-spacing: 1px;
}

/* Tactical Container Cards */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: #0d121f !important;
    border: 1px solid #1e293b !important;
    border-radius: 4px !important;
    padding: 16px !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.6) !important;
    transition: all 0.2s ease !important;
}
[data-testid="stVerticalBlockBorderWrapper"]:hover {
    border-color: #f59e0b !important;
    box-shadow: 0 0 15px rgba(245, 158, 11, 0.2) !important;
}

/* Card Titles */
.card-title-amber {
    font-family: 'Chakra Petch', sans-serif;
    font-size: 1.25rem;
    font-weight: 700;
    color: #f59e0b;
    margin-bottom: 6px;
    letter-spacing: 0.5px;
}
.card-title-cyan {
    font-family: 'Chakra Petch', sans-serif;
    font-size: 1.25rem;
    font-weight: 700;
    color: #38bdf8;
    margin-bottom: 6px;
    letter-spacing: 0.5px;
}
.card-desc {
    font-family: 'JetBrains Mono', monospace;
    color: #94a3b8;
    font-size: 0.82rem;
    line-height: 1.5;
    min-height: 65px;
}

/* Form Labels */
label[data-testid="stWidgetLabel"] p, label, .stWidgetLabel {
    color: #f59e0b !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.88rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.5px !important;
    margin-bottom: 6px !important;
}

/* ========================================================
   FIXED FILE UPLOADER & BUTTON
   ======================================================== */
[data-testid="stFileUploaderDropzone"] {
    background-color: #0d121f !important;
    border: 1.5px dashed #f59e0b !important;
    border-radius: 4px !important;
}

/* Upload Button Color Fix */
[data-testid="stFileUploaderDropzone"] button {
    background-color: #1e293b !important;
    color: #f59e0b !important;
    border: 1px solid #f59e0b !important;
    border-radius: 4px !important;
}
[data-testid="stFileUploaderDropzone"] button:hover {
    background-color: #f59e0b !important;
    color: #070a12 !important;
}
[data-testid="stFileUploaderDropzone"] button svg {
    fill: #f59e0b !important;
}
[data-testid="stFileUploaderDropzone"] button:hover svg {
    fill: #070a12 !important;
}

/* Helper Text ("200MB per file...") Fix */
[data-testid="stFileUploaderDropzoneInstructions"] div,
[data-testid="stFileUploaderDropzoneInstructions"] span,
[data-testid="stFileUploaderDropzoneInstructions"] small,
[data-testid="stFileUploaderDropzone"] small {
    color: #e2e8f0 !important;
    opacity: 0.95 !important;
}

/* Inputs & Textareas */
div[data-baseweb="textarea"] textarea,
div[data-baseweb="input"] input,
.stTextArea textarea,
.stTextInput input {
    background-color: #0d121f !important;
    color: #ffffff !important;
    border: 1px solid #283347 !important;
    border-radius: 4px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.9rem !important;
}

div[data-baseweb="textarea"] textarea:focus,
div[data-baseweb="input"] input:focus,
.stTextArea textarea:focus,
.stTextInput input:focus {
    border-color: #f59e0b !important;
    box-shadow: 0 0 10px rgba(245, 158, 11, 0.3) !important;
}

::placeholder {
    color: #64748b !important;
}

/* Primary Button (Tactical Amber) */
div[data-testid="stButton"] > button[kind="primary"] {
    background-color: #f59e0b !important;
    color: #000000 !important;
    font-family: 'Chakra Petch', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 1px !important;
    border: none !important;
    border-radius: 3px !important;
    box-shadow: 0 0 15px rgba(245, 158, 11, 0.35) !important;
    transition: all 0.2s ease !important;
    margin-top: 10px !important;
}
div[data-testid="stButton"] > button[kind="primary"]:hover {
    background-color: #d97706 !important;
    box-shadow: 0 0 25px rgba(245, 158, 11, 0.65) !important;
}

/* Secondary Button (Tactical Cyan) */
div[data-testid="stButton"] > button[kind="secondary"] {
    background-color: #38bdf8 !important;
    color: #000000 !important;
    font-family: 'Chakra Petch', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 1px !important;
    border: none !important;
    border-radius: 3px !important;
    box-shadow: 0 0 15px rgba(56, 189, 248, 0.35) !important;
    transition: all 0.2s ease !important;
    margin-top: 10px !important;
}
div[data-testid="stButton"] > button[kind="secondary"]:hover {
    background-color: #0284c7 !important;
    box-shadow: 0 0 25px rgba(56, 189, 248, 0.65) !important;
}

/* Captions */
.stCaption {
    color: #64748b !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.8rem !important;
}
</style>
"""
st.markdown(TECHOPS_CSS, unsafe_allow_html=True)


# --- 1. CRYPTOGRAPHY ENGINE ---

def derive_key(passphrase: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
    )
    return base64.urlsafe_b64encode(kdf.derive(passphrase.encode()))

def encrypt_message(plaintext: str, passphrase: str) -> bytes:
    salt = b"techops_salt_16b"
    key = derive_key(passphrase, salt)
    fernet = Fernet(key)
    return fernet.encrypt(plaintext.encode('utf-8'))

def decrypt_message(ciphertext: bytes, passphrase: str) -> str:
    salt = b"techops_salt_16b"
    key = derive_key(passphrase, salt)
    fernet = Fernet(key)
    return fernet.decrypt(ciphertext).decode('utf-8')


# --- 2. STEGANOGRAPHY ENGINE (LSB) ---

DELIMITER = b"<<<END_TECHOPS_VAULT>>>"

def hide_data_in_image(cover_image: Image.Image, secret_bytes: bytes) -> Image.Image:
    img = cover_image.convert('RGB')
    payload = secret_bytes + DELIMITER
    bits = ''.join(f"{byte:08b}" for byte in payload)
    
    pixels = list(img.getdata())
    max_bits = len(pixels) * 3
    if len(bits) > max_bits:
        raise ValueError(f"[BUFFER OVERFLOW] Max capacity: {max_bits//8} bytes, Payload: {len(payload)} bytes.")
    
    new_pixels = []
    bit_idx = 0
    total_bits = len(bits)
    
    for pixel in pixels:
        r, g, b = pixel
        if bit_idx < total_bits:
            r = (r & ~1) | int(bits[bit_idx]); bit_idx += 1
        if bit_idx < total_bits:
            g = (g & ~1) | int(bits[bit_idx]); bit_idx += 1
        if bit_idx < total_bits:
            b = (b & ~1) | int(bits[bit_idx]); bit_idx += 1
        new_pixels.append((r, g, b))
        
    stego_img = Image.new(img.mode, img.size)
    stego_img.putdata(new_pixels)
    return stego_img

def extract_data_from_image(stego_image: Image.Image) -> bytes:
    img = stego_image.convert('RGB')
    pixels = list(img.getdata())
    bits = [str(channel & 1) for pixel in pixels for channel in pixel]
    bit_string = ''.join(bits)
    all_bytes = bytearray()
    delimiter_len = len(DELIMITER)
    
    for i in range(0, len(bit_string), 8):
        byte_bits = bit_string[i:i+8]
        if len(byte_bits) < 8:
            break
        all_bytes.append(int(byte_bits, 2))
        if all_bytes.endswith(DELIMITER):
            return bytes(all_bytes[:-delimiter_len])
            
    raise ValueError("[AUTH BREACH] No valid signature or encrypted payload detected.")


# --- 3. VIEWS & NAVIGATION ---

# =======================================================
# VIEW 1: TECH-OPS COMMAND VAULT
# =======================================================
if st.session_state.page == "home":
    st.markdown("<h1 class='techops-title'>🛰️ TECH-OPS COMMAND 🛰️</h1>", unsafe_allow_html=True)
    st.markdown("<p class='techops-subtitle'>[ TACTICAL CYBER DEFENSE & COVERT DATA EXFILTRATION ]</p>", unsafe_allow_html=True)
    
    st.markdown(
        """
        <div style='text-align: center; margin-bottom: 25px;'>
            <span class='ops-badge'>STATUS: ARMED</span>
            <span class='ops-badge'>CIPHER: AES-256</span>
            <span class='ops-badge'>KDF: PBKDF2-SHA256</span>
            <span class='ops-badge'>CARRIER: LSB-PIXEL</span>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container(border=True):
            st.markdown("<div class='card-title-amber'>|| ENCRYPT & CLOAK ||</div>", unsafe_allow_html=True)
            st.markdown("<div class='card-desc'>Encrypt classified payload with AES-256 and inject into carrier image bitplanes.</div>", unsafe_allow_html=True)
            if st.button("INITIALIZE ENCRYPTION ➔", type="primary", use_container_width=True):
                set_page("encrypt")
                st.rerun()

    with col2:
        with st.container(border=True):
            st.markdown("<div class='card-title-cyan'>|| EXTRACT & UNVEIL || </div>", unsafe_allow_html=True)
            st.markdown("<div class='card-desc'>Extract concealed bitstream from carrier image and restore original classified data.</div>", unsafe_allow_html=True)
            if st.button("INITIALIZE DECRYPTOR ➔", type="secondary", use_container_width=True):
                set_page("decrypt")
                st.rerun()

    st.markdown("<br><hr style='border-color: #1e293b;'>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #475569; font-size: 0.75rem;'>TECH-OPS SECURITY CONSOLE v3.0 • VTU MINI-PROJECT</p>", unsafe_allow_html=True)


# =======================================================
# VIEW 2: ENCRYPT & CLOAK PAGE
# =======================================================
elif st.session_state.page == "encrypt":
    col_back, col_title = st.columns([1, 4])
    with col_back:
        if st.button("← HOME", use_container_width=True):
            set_page("home")
            st.rerun()
    with col_title:
        st.markdown("<h3 style='color: #f59e0b; margin:0; font-family: Chakra Petch;'>|| ENCRYPTION & PIXEL CLOAK || </h3>", unsafe_allow_html=True)
        
    st.markdown("<hr style='border-color: #1e293b;'>", unsafe_allow_html=True)
    
    cover_file = st.file_uploader("1. SELECT COVER CARRIER (PNG Recommended)", type=["png", "jpg", "jpeg"], key="enc_cover")
    secret_text = st.text_area("2. ENTER CLASSIFIED PAYLOAD:", placeholder="Type or paste confidential data here...")
    passphrase = st.text_input("3. ENTER SECURITY PASSPHRASE:", type="password", key="enc_pass")
    
    if st.button("EXECUTE ENCRYPT & CLOAK ⚡", type="primary", use_container_width=True):
        if not cover_file or not secret_text or not passphrase:
            st.error("[ERROR] Carrier Image, Secret Text, and Passphrase required.")
        else:
            try:
                cover_img = Image.open(cover_file)
                
                # Step 1: Encrypt Plaintext -> Ciphertext
                ciphertext = encrypt_message(secret_text, passphrase)
                
                # Step 2: Hide Ciphertext in Image
                stego_img = hide_data_in_image(cover_img, ciphertext)
                
                st.success("✅ [OPERATIONAL SUCCESS] Payload encrypted with AES-256 and cloaked into image bitplanes.")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.caption("Cover Carrier (Original)")
                    st.image(cover_img, use_container_width=True)
                with col2:
                    st.caption("Stego Carrier (Cloaked Payload)")
                    st.image(stego_img, use_container_width=True)
                    
                # Download PNG
                buf = io.BytesIO()
                stego_img.save(buf, format="PNG")
                st.download_button(
                    label="⬇️ DOWNLOAD STEGO CARRIER (PNG)",
                    data=buf.getvalue(),
                    file_name="techops_cloaked.png",
                    mime="image/png",
                    use_container_width=True
                )
                
                with st.expander("🔍 [HEX] VIEW RAW CIPHERTEXT"):
                    st.code(ciphertext.decode(), language="text")
                    
            except Exception as e:
                st.error(f"[EXECUTION FAULT] {e}")


# =======================================================
# VIEW 3: EXTRACT & DECRYPT PAGE
# =======================================================
elif st.session_state.page == "decrypt":
    col_back, col_title = st.columns([1, 4])
    with col_back:
        if st.button("← HOME", use_container_width=True):
            set_page("home")
            st.rerun()
    with col_title:
        st.markdown("<h3 style='color: #38bdf8; margin:0; font-family: Chakra Petch;'>|| EXTRACTION & DECRYPTION || </h3>", unsafe_allow_html=True)
        
    st.markdown("<hr style='border-color: #1e293b;'>", unsafe_allow_html=True)
    
    stego_file = st.file_uploader("1. SELECT STEGO CARRIER (PNG)", type=["png"], key="dec_stego")
    passphrase_extract = st.text_input("2. ENTER SECURITY PASSPHRASE:", type="password", key="dec_pass")
    
    if st.button("EXECUTE EXTRACT & DECRYPT ⚡", type="secondary", use_container_width=True):
        if not stego_file or not passphrase_extract:
            st.error("[ERROR] Stego Carrier and Passphrase required.")
        else:
            try:
                stego_img = Image.open(stego_file)
                
                # Step 1: Extract Ciphertext
                extracted_ciphertext = extract_data_from_image(stego_img)
                
                # Step 2: Decrypt Ciphertext -> Plaintext
                decrypted_plaintext = decrypt_message(extracted_ciphertext, passphrase_extract)
                
                st.success("🎉 [UNVEILED] Authentication tag verified. Plaintext recovered!")
                
                st.markdown("### 📝 RECOVERED CLASSIFIED DATA:")
                st.info(decrypted_plaintext)
                
                with st.expander("🔍 [HEX] EXTRACTED CIPHERTEXT"):
                    st.code(extracted_ciphertext.decode(), language="text")
                    
            except Exception as e:
                st.error("❌ [AUTH REJECTED] Passphrase mismatch or corrupted bitplanes.")