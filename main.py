from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# 1️⃣ Define the chat template with history placeholder
chat_prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content="You are a helpful assistant."),
    MessagesPlaceholder(variable_name="chat_history"),  # This is where history is injected
    HumanMessage(content="{question}")  # User's current input
])

# 2️⃣ Initialize chat history
chat_history = []

# 3️⃣ User asks the first question
user_question = "What is the capital of France?"
chat_history.append(HumanMessage(content=user_question))  # Store user input

# 4️⃣ Generate first AI response
formatted_messages = chat_prompt.invoke({
    "chat_history": chat_history,  # Insert full history
    "question": user_question,  # New question
})
ai_response = AIMessage(content="The capital of France is Paris.")
chat_history.append(ai_response)  # Store AI response

# 🟢 First cycle complete, `chat_history` now has a record of the first conversation

# 5️⃣ User asks a follow-up question
user_question_2 = "What is its population?"
chat_history.append(HumanMessage(content=user_question_2))  # Store user input

# 6️⃣ Generate second AI response (history is automatically included)
formatted_messages = chat_prompt.invoke({
    "chat_history": chat_history,  # Now includes previous Q&A
    "question": user_question_2,  # New question
})
ai_response_2 = AIMessage(content="The population of France is around 67 million.")
chat_history.append(ai_response_2)  # Store AI response

# 🟢 Second cycle complete, history has grown, and AI will retain context

user_question_3 = "What is its currency?"
chat_history.append(HumanMessage(content=user_question_3))

formatted_messages = chat_prompt.invoke({
    "chat_history": chat_history,
    "question": user_question_3,
})

ai_response_3 = AIMessage(content="The currency of France is Euros.")
chat_history.append(ai_response_3)

print(chat_history)

