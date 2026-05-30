import streamlit as st
from google import genai

# 1. SETTING UTAMA HALAMAN WEB (Tampilan Premium)
st.set_page_config(
    page_title="ZettPrompt - Gemini Web App",
    page_icon="🤖",
    layout="centered"
)

# 2. SIDEBAR KIRI (Tempat Input API Key & Pengaturan)
with st.sidebar:
    st.title("⚙️ Pengaturan Web")
    st.subheader("Oleh: Tuan Ragil 😎")
    
    # Input API Key Rahasia milik User
    api_key_input = st.text_input(
        "Masukkan Gemini API Key Tuan:",
        type="password",
        placeholder="AIzaSy..."
    )
    st.markdown("---")
    st.info(
        "💡 **Cara Dapatkan API Key:**\n"
        "Buka Google AI Studio, lalu klik 'Get API Key'. Gratis!"
    )

# 3. KONTEN UTAMA (Tampilan Chat Web)
st.title("🔮 ZettPrompt UI")
st.caption("Prompt Generator & AI Assistant — Tanpa Harus Jago Coding")

# Inisialisasi Memori Chat agar Chat tidak hilang saat web di-refresh
if "messages" not in st.session_state:
    st.session_state.messages = []

# Menampilkan Riwayat Chat di Layar Web
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 4. LOGIKA PENGIRIMAN PESAN
if prompt := st.chat_input("Ask Gemini 3..."):
    # Tampilkan chat user ke layar web
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Cek apakah user sudah memasukkan API Key di sidebar
    if not api_key_input:
        with st.chat_message("assistant"):
            st.error("❌ Tuan Ragil, harap masukkan Gemini API Key di sidebar kiri dulu ya!")
    else:
        # Tembak ke Server Google Gemini menggunakan API Key
        try:
            client = genai.Client(api_key=api_key_input)
            
            with st.chat_message("assistant"):
                # Efek animasi loading mengetik
                with st.spinner("Gemini sedang berpikir..."):
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt,
                    )
                    st.markdown(response.text)
            
            # Simpan balasan Gemini ke memori riwayat chat
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            with st.chat_message("assistant"):
                st.error(f"⚠️ Terjadi Kesalahan Server: {str(e)}")
