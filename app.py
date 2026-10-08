# Konfigurasi Halaman
st.set_page_config(page_title="Youtube Niche AI", page_icon="💪")
‎st.title("📈 AI Analisa Niche YouTube")
‎st.caption("Agen AI khusus untuk mencari niche YouTube dengan RPM tinggi & persaingan rendah.")
‎
‎# --- PENTING: Ganti URL di bawah ini dengan URL Webhook dari n8n kamu ---
‎N8N_WEBHOOK_URL = "https://n8n-j0rtdedyllcf.jkt2.sumopod.my.id/webhook-test/2dd390bf-a190-40a6-9e68-6b56ef760f06
‎
‎# Inisialisasi memori chat agar percakapan tidak hilang
‎if "messages" not in st.session_state:
‎    st.session_state.messages = [{"role": "assistant", "content": "Halo! Niche YouTube apa yang ingin kita analisa hari ini?"}]
‎
‎# Menampilkan histori chat sebelumnya
‎for msg in st.session_state.messages:
‎    with st.chat_message(msg["role"]):
‎        st.markdown(msg["content"])
‎
‎# Kolom tempat kamu mengetik prompt/chat
‎if prompt := st.chat_input("Ketik niche yang ingin dianalisa (misal: 'Keuangan' atau 'Teknologi')..."):
‎    
‎    # 1. Tampilkan pesan dari kamu
‎    st.session_state.messages.append({"role": "user", "content": prompt})
‎    with st.chat_message("user"):
‎        st.markdown(prompt)
‎
‎    # 2. Tampilkan pesan dari AI (sambil loading)
‎    with st.chat_message("assistant"):
‎        with st.spinner("Menggali data YouTube & menganalisa niche... ⏳"):
‎            try:
‎                # Mengirim chat kamu ke n8n
‎                payload = {"chat_input": prompt}
‎                response = requests.post(N8N_WEBHOOK_URL, json=payload)
‎                
‎                # Menerima balasan dari n8n
‎                if response.status_code == 200:
‎                    # Mengambil teks balasan dari n8n
‎                    ai_reply = response.text 
‎                else:
‎                    ai_reply = f"Maaf, gagal terhubung ke n8n. (Error: {response.status_code})"
‎            except Exception as e:
‎                ai_reply = f"Terjadi kesalahan sistem: {e}"
‎            
‎            # Menampilkan jawaban
‎            st.markdown(ai_reply)
‎            
‎    # 3. Simpan jawaban AI ke memori chat
‎    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
‎
