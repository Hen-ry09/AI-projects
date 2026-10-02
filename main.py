from model import chat
from prompt import build_system_prompt
from retriever import Retriever


def main():
    system_prompt = build_system_prompt()
    retriever = Retriever()

    if system_prompt:
        print(f"Loaded guidelines ({len(system_prompt)} chars)")
    else:
        print("No system prompt found.")

    while True:
        try:
            user_input = input("\nYou: ")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if user_input.lower() in ("exit", "quit"):
            print("Goodbye!")
            break

        context = retriever.retrieve_text(user_input)
        rag_prompt = f"Relevant information:\n{context}\n\nQuestion: {user_input}"
        response = chat(rag_prompt, system_prompt=system_prompt)
        print(f"\nBot: {response}")


if __name__ == "__main__":
    main()
