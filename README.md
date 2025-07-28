# 📊 Zoom Transcript Summarizer

A smart multi-agent AI app that converts raw Zoom, Meet, or Teams transcripts into **structured, human-readable meeting summaries** in Markdown format. Built using **CrewAI**, **LangChain**, **Streamlit**, and powered by **DeepSeek R1 via OpenRouter**.

---

## 🚀 Features

✅ Upload `.txt` transcripts from Zoom, Google Meet, Microsoft Teams, etc.  
✅ Extracts clean, concise meeting summaries with key sections  
✅ Outputs **Markdown summaries** formatted with **emojis and tables**  
✅ Uses **two intelligent agents** for accurate processing:

| Agent Name              | Function                                                   |
|-------------------------|------------------------------------------------------------|
| 🧠 Transcript Interpreter | Parses messy transcripts into structured bullet summaries  |
| ✍️ Markdown Formatter     | Converts bullet summaries into polished Markdown output    |

✅ Built with:
- [Streamlit](https://streamlit.io/)
- [CrewAI](https://www.crewai.io/)
- [OpenRouter](https://openrouter.ai/) (DeepSeek R1)
- [LangChain](https://www.langchain.com/)
- [Pydantic](https://docs.pydantic.dev/)

---

## 📂 Example Output

```markdown
# 📝 Meeting Summary
- 📅 **Date**: 2025-07-28
- ⏰ **Time**: 10:00 AM
- 📌 **Project**: AI Zoom Summarizer
- 👥 **Attendees**: Alice, Bob, Charlie

## 📋 Agenda
- Discuss Zoom AI summary
- Deployment plan

## 💬 Key Discussions
- Token usage optimization
- Markdown formatting improvements

## ✅ Decisions Made
- Use DeepSeek for transcript processing
- Automate JSON to Markdown conversion

## 📌 Action Items
| Task                        | Owner   | Due Date     |
|----------------------------|---------|--------------|
| Refactor summarizer logic  | Alice   | 2025-08-01   |
| Add download option in UI  | Charlie | 2025-08-02   |
