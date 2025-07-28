# 🧠 Zoom Transcript Summarizer

A smart multi-agent AI app that converts raw Zoom or video call transcripts into structured, ready-to-use meeting summaries in JSON format. Built using CrewAI, LangChain, Pydantic, and Streamlit, powered by OpenRouter's DeepSeek R1 LLM

---

## 🚀 Features

✅ Upload `.txt` transcripts (Zoom/Meet/Teams)  
✅ Extracts clean, human-readable summaries  
✅ Outputs structured JSON matching a defined schema  
✅ Uses two intelligent agents:
- 📌 `Transcript Interpreter` — summarizes key meeting points
- 📌 `JSON Structurer` — converts into clean JSON for downstream use

✅ Built with:
- [Streamlit](https://streamlit.io/)
- [CrewAI](https://github.com/joaomdmoura/crewAI)
- [OpenRouter (DeepSeek R1)](https://openrouter.ai/)
- [LangChain](https://www.langchain.com/)
- [Pydantic](https://docs.pydantic.dev/)

---

## 📂 Output JSON Schema

```json
{
  "date": "YYYY-MM-DD",
  "time": "10:00 AM",
  "attendees": ["Name1", "Name2"],
  "project": "Project Title",
  "agenda": ["Item 1", "Item 2"],
  "key_discussions": ["Discussion point 1", "Discussion point 2"],
  "decisions_made": ["Decision 1", "Decision 2"],
  "action_items": 

https://github.com/user-attachments/assets/537639ba-47d5-425a-ac56-19bef5a7c4ac

[
    {
      "task": "Task description",
      "owner": "Person responsible",
      "due_date": "YYYY-MM-DD"
    }
  ]
}
