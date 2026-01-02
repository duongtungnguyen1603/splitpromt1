import streamlit as st
import re
import zipfile
import io

st.set_page_config(page_title="Scene / Prompt Splitter", layout="centered")

st.title("Scene / Prompt Splitter")
st.write("Upload file txt → tự động chuẩn hóa & chia scene / prompt")

uploaded_file = st.file_uploader(
    "Upload file .txt",
    type=["txt"]
)

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

    st.success(f"✅ Đã tách {count} scene / prompt")

    st.download_button(
        label="⬇️ Tải file ZIP",
        data=zip_buffer.getvalue(),
        file_name="scenes.zip",
        mime="application/zip"
    )
