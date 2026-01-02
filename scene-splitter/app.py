import streamlit as st
import re
import zipfile
import io
import base64

# ================== PAGE CONFIG ==================
st.set_page_config(page_title="Scene / Prompt Splitter", layout="centered")

# ================== SET BACKGROUND FROM LOCAL ==================
def set_bg_from_local(image_path):
    with open(image_path, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image:
                linear-gradient(rgba(0,0,0,0.65), rgba(0,0,0,0.65)),
                url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        h1, h2, h3, p, label {{
            color: #ffffff !important;
        }}

        .stButton button, .stDownloadButton button {{
            background: linear-gradient(90deg, #ff8a00, #ff3d00);
            color: white;
            border-radius: 12px;
            font-weight: 600;
            padding: 0.6em 1.2em;
            border: none;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ======= LOAD BACKGROUND =======
set_bg_from_local("93177f6eb9834c29794a9b63b2.jpg")

# ================== UI ==================
st.title("Scene / Prompt Splitter")
st.write("Upload file txt → tự động chuẩn hóa & chia scene / prompt")

uploaded_file = st.file_uploader(
    "Upload file .txt",
    type=["txt"]
)

# ================== LOGIC ==================
if uploaded_file:
    content = uploaded_file.read().decode("utf-8", errors="ignore")
    content = re.sub(r'[\u200B-\u200D\uFEFF]', '', content)

    pattern = r'(?=^[^\S\r\n]*[^\w\n\r]*(?:cảnh|scene|prompt)\s+\d+(?:\s*[–—-])?)'
    scenes = re.split(pattern, content, flags=re.MULTILINE | re.IGNORECASE)

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        count = 0
        for scene in scenes:
            scene = scene.strip()
            if not scene:
                continue
            zipf.writestr(f"scene_{count:02d}.txt", scene)
            count += 1

    st.success(f"Đã tách {count} scene / prompt")

    st.download_button(
        label="Tải file ZIP",
        data=zip_buffer.getvalue(),
        file_name="scenes.zip",
        mime="application/zip"
    )



