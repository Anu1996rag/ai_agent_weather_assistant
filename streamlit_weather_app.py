import os
import requests
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_classic.agents import create_react_agent, AgentExecutor
from langsmith import Client

# 1. Page Configuration
st.set_page_config(page_title="AI Agent - Weather Assistant", page_icon="🤖", layout="centered")
st.title("🤖 AI Agent - Weather Assistant")
st.caption("Ask me to calculate squares or check the live weather anywhere!")

# 2. Environment Setup & Initialization
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# Initialize LangSmith Client if configured
client = Client()


# 3. Define Tools
@tool
def calculate_square(num) -> int:
    """ Multiplies the given number by itself """
    return int(num) * int(num)

@tool
def get_weather_data(city: str):
    """
    Fetch current weather for given city
    :param city:
    :return:
    """
    if not WEATHER_API_KEY:
        return "Weather API Key is missing"

    url = f"https://api.weatherstack.com/current?access_key={WEATHER_API_KEY}&query={city}"
    try:
        resp = requests.get(url)
        data = resp.json()

        if "current" not in data:
            return f"Unable to fetch current weather for {city}"

        return (
            f"City : {city}\n"
            f"Temperature : {data['current']['temperature']}°C\n"
            f"Weather : {data['current']['weather_descriptions'][0] if isinstance(data['current']['weather_descriptions'], list) else data['current']['weather_descriptions']}\n"
            f"Humidity : {data['current']['humidity']}%\n"
            f"UV Index: {data['current']['uv_index']}"
        )
    except Exception as e:
        return f"Error fetching weather data: {str(e)}"

# 4. Agent Setup (Cached to prevent reloading on every click)
@st.cache_resource
def get_agent_executor():
    tools = [calculate_square, get_weather_data]

    # Fallback default ReAct prompt structure if LangSmith client is not active/configured
    if client:
        prompt = client.pull_prompt("hwchase17/react", dangerously_pull_public_prompt=True)
    else:
        from langchain_core.prompts import PromptTemplate
        template = """Answer the following questions as best you can. You have access to the following tools:

                    {tools}
                    
                    Use the following format:
                    
                    Question: the input question you must answer
                    Thought: you should always think about what to do
                    Action: the action to take, should be one of [{tool_names}]
                    Action Input: the input to the action
                    Observation: the result of the action
                    ... (this Thought/Action/Action Input/Observation can repeat N times)
                    Thought: I now know the final answer
                    Final Answer: the final answer to the original input question
                    
                    Begin!
                    
                    Question: {input}
                    Thought:{agent_scratchpad}
                """
        prompt = PromptTemplate.from_template(template)

    llm = ChatGroq(
        model="groq/compound-mini",
        api_key=groq_api_key,
        max_tokens=500
    )

    agent = create_react_agent(tools=tools, prompt=prompt, llm=llm)
    return AgentExecutor(agent=agent, tools=tools, verbose=False)

# Validate API keys before proceeding
if not groq_api_key:
    st.error("Missing `GROQ_API_KEY`")
    st.stop()

agent_exec = get_agent_executor()

# 5. Maintain Chat History in Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. User Input and Execution Loop
if user_input := st.chat_input("What is the capital of India and how is the weather there?"):

    # Display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate and display agent response
    with st.chat_message("assistant"):
        status_placeholder = st.empty()

        # Visual loader while the multi-step agent thinks and runs tools
        with status_placeholder.status("🤖 Agent is thinking and executing tools...", expanded=True) as status:
            try:
                response = agent_exec.invoke({"input": user_input})
                output_text = response["output"]
                status.update(label="Execution complete!", state="complete", expanded=False)
            except Exception as e:
                output_text = f"An error occurred: {str(e)}"
                status.update(label="Execution failed.", state="error", expanded=True)

        # Clear the status banner and show clean markdown output
        status_placeholder.empty()
        st.markdown(output_text)
        st.session_state.messages.append({"role": "assistant", "content": output_text})
