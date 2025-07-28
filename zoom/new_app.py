import streamlit as st
from crew import run_summary_agent
import os

st.set_page_config(page_title='Zoom Transcript Summarizer')
st.title("Zoom Transcript Summarizer")


DIR = 'uploads'
os.makedirs(DIR,exist_ok=True)

upload_file = st.file_uploader("Upload your Zoom transcript", type=['txt'])


if upload_file:
    # Save to local
    save_file = os.path.join(DIR,upload_file.name)

    with open(save_file,'wb') as f:
        f.write(upload_file.read())

    st.success("Transcript uploaded successfully!")
    
    
    with open(save_file, 'r', encoding='utf-8') as f:
        preview_text = f.read()[:2000]
    st.text_area("Transcript Preview:", preview_text, height=200)

    if st.button("Summarize Zoom Call"):
        with st.spinner("Running agents to summarize the meeting..."):
            summary = run_summary_agent(save_file)
        
        
        summary_markdown = summary['final_output']

        st.markdown(summary_markdown)
    
