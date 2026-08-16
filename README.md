# 🤖 Multi-Tool AI Agent Assistant

An interactive AI Agent built with **LangChain (ReAct framework)**, **Groq (Llama 3.3)**, and **Streamlit**. The agent can autonomously choose between custom mathematical tools and external live API tools to solve multi-step user inquiries.

---

## 🚀 Features

*   **Autonomous Decision Making**: Uses the ReAct (Reasoning and Acting) framework to chain logical thoughts, tools, and observations.
*   **Custom Math Tools**: Built-in Python tool execution for complex operations like calculating squares.
*   **Live Weather Integration**: Dynamically connects with the WeatherStack API to retrieve current weather, humidity, and UV indexes for any global city.
*   **Modern Chat UI**: Implements a highly intuitive Streamlit chat interface that securely buffers session interactions and displays real-time execution status trackers.
*   **LangSmith Observability**: Built-in support to pull public standard prompt templates and log agent trace execution paths.

---

## 🛠️ Tech Stack

*   **Frontend UI**: [Streamlit](https://streamlit.io/)
*   **Agent Framework**: [LangChain](https://www.langchain.com/)
*   **LLM Engine**: [Groq Cloud (Llama-3.3-70b-versatile)](https://groq.com/)
*   **Data API**: [WeatherStack API](https://weatherstack.com/)
*   **Observability**: [LangSmith Hub](https://smith.langchain.com/)

---

## 📋 Prerequisites

Before running the application, make sure you have:
1. Python installed (v3.9 or higher recommended).
2. A **Groq API Key** (Get one from the [Groq Console](https://console.groq.com/)).
3. A **WeatherStack Access Key** (Get a free tier key from [WeatherStack](https://weatherstack.com/)).

---

## 🔧 Installation & Setup

Follow these steps to set up the project locally:

### 1. Clone or Create Project Files
Create a new directory and save the code file as `app.py`.

### 2. Install Required Dependencies
Run the following command to install all necessary Python packages:
```bash
pip install streamlit langchain langchain-groq langsmith python-dotenv requests
```

### 3. Configure Environment Variables
Create a file named `.env` in the root directory of your project and populate it with your active API keys:

```env
GROQ_API_KEY="your_groq_api_key_here"
WEATHER_API_KEY="your_weatherstack_api_key_here"

# Optional: Configuration if you want to track executions in LangSmith
LANGCHAIN_TRACING_V2="true"
LANGCHAIN_API_KEY="your_langsmith_api_key_here"
```

---

## 💻 Running the Application

Launch the Streamlit server from your terminal or command prompt:

```bash
streamlit run app.py
```

Once running, your local web browser will automatically open to `http://localhost:8501`.

---

## 💡 Example Queries to Try

You can test the agent's capability to process simple and complex multi-step reasoning chains with prompts like:

*   *"What is the square of 45?"*
*   *"Check the weather in Paris."*
*   *"What is the capital of India and how is the weather there right now?"* *(Requires the agent to parse two separate tasks, run an inner thought loop, and fetch the API data sequentially).*