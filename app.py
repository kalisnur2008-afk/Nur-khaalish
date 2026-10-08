import streamlit as st
import requests

# 1. Konfigurasi Halaman
st.set_page_config(page_title="Youtube Niche AI", page_icon="💪")
st.title("YouTube Niche Finder AI")
st.caption("Agen AI khusus untuk mencari niche YouTube dengan RPM tinggi & persaingan rendah.")

# 2. Konfigurasi URL Webhook n8n
# PENTING: Karena ini menggunakan '/webhook-test/', n8n kamu harus dalam mode 'Listen'
N8N_WEBHOOK_URL = "https://n8n-j0rtdedy11cf.jkt2.sumopod.my.id/webhook-test/2dd390bf-a190-40a6-9e68-6b56ef760f06"

# 3. Inisialisasi memori chat agar percakapan tidak hilang
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Halo! Niche YouTube apa yang ingin kita analisa hari ini?"}
    ]

# 4. Menampilkan histori chat sebelumnya
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 5. Kolom tempat kamu mengetik prompt/chat
if prompt := st.chat_input("Ketik niche yang ingin dianalisa (misal: 'Keuangan' atau 'Teknologi')..."):

    # Tampilkan pesan dari kamu
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Tampilkan pesan dari AI (sambil loading)
    with st.chat_message("assistant"):
        with st.spinner("Menggali data YouTube & menganalisa niche..."):
            try:
                # Mengirim data payload ke n8n
                # Format JSON ini ({"chatInput": prompt}) harus sesuai dengan yang ditangkap oleh Webhook node di n8n
                payload = {"chatInput": prompt}
                response = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=60)
                
                # Jika sukses diterima server
                if response.status_code == 200:
                    try:
                        # Coba parse sebagai JSON terlebih dahulu
                        data = response.json()
                        
                        # Sesuaikan dengan format output dari n8n kamu
                        if isinstance(data, dict):
                            # Jika n8n membalas dengan {"output": "teks balasan"}, ambil isinya
                            ai_reply = data.get("output", data.get("text", str(data)))
                        elif isinstance(data, list) and len(data) > 0:
                            ai_reply = str(data[0])
                        else:
                            ai_reply = str(data)
                    except ValueError:
                        # Jika n8n hanya membalas text biasa (bukan JSON)
                        ai_reply = response.text
                else:
                    ai_reply = f"⚠️ Server n8n mengembalikan status error: {response.status_code}"
            
            except requests.exceptions.RequestException as e:
                ai_reply = f"⚠️ Terjadi masalah koneksi ke server n8n: {e}"

            # Tampilkan balasan di layar
            st.markdown(ai_reply)
            
    # Simpan balasan AI ke dalam memori sesi
    st.session_state.messages.append({"role": "assistant", "content": ai_reply})

‎ 
