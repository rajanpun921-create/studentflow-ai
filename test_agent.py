
from agent import ask_agent

print("AI Student Assistant")
print("--------------------")

while True:

    question = input("\nAsk your AI assistant: ").strip()

    if question.lower() == "exit":
        print("Goodbye!")
        break

    if not question:
        continue

    try:

        answer = ask_agent(question)

        print("\nAI Assistant:")
        print(answer)

    except Exception as error:

        print("AI request failed.")
        print(error)
