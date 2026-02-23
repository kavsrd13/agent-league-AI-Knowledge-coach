# AI Knowledge Coach

A minimal, polished AI-powered web app to help users quickly learn any topic with structured summaries, key insights, interview questions, and a mini quiz. Built for the Microsoft Agents League – Creative Apps track.

## Features
- Enter any topic and instantly generate:
  - Structured summary
  - 5 key insights
  - 3 interview questions
  - 5-question knowledge check quiz (MCQs)
- Download results as a clean PDF
- Modern, minimal UI (Streamlit)
- Uses Azure OpenAI Service
- Modular, production-style codebase

## Folder Structure
```

├── app.py              # Main Streamlit UI
├── ai_engine.py        # Azure OpenAI calls and prompt logic
├── pdf_generator.py    # PDF export logic
├── utils.py            # Utilities (prompt templates, parsing, errors)
├── requirements.txt    # Python dependencies
├── .env.example        # Example environment variables
└── README.md           # Project overview & instructions
```

## Architecture
- **Streamlit** for UI and user interaction
- **Azure OpenAI Service** for AI content generation
- **fpdf** for PDF export
- **Modular Python files** for maintainability
- **Environment variables** for API keys and endpoint

## Setup Instructions
1. Clone this repo or copy the folder.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your Azure OpenAI credentials as environment variables:
   - On Windows:
     ```powershell
     $env:AZURE_OPENAI_ENDPOINT="https://demofoundry214354.cognitiveservices.azure.com/"
     $env:AZURE_OPENAI_KEY="<your-api-key>"
     $env:AZURE_OPENAI_DEPLOYMENT="gpt-4.1"
     $env:AZURE_OPENAI_API_VERSION="2024-12-01-preview"
     ```
   - Or enter them in the sidebar at runtime.
4. Run the app:
   ```bash
   streamlit run app.py
   ```

## How GitHub Copilot Was Used
This project was built with significant help from GitHub Copilot:
- Generating modular Python code for each file
- Suggesting prompt templates and error handling
- Creating Streamlit UI layout and PDF formatting
- Writing README and requirements
- Improving code clarity and structure

Copilot accelerated development, provided best practices, and helped ensure a clean, production-ready result.

---

**Enjoy learning with AI Knowledge Coach!**
