import sys
from akwaaba.agent import Agent


def run_cli(user_id: str = "default"):
    agent = Agent(user_id=user_id)

    print(" Akwaaba! Welcome to Akwaaba AI — your Ghana Travel Intelligence Agent.")
    print("Ask about destinations, culture, language, itineraries, budgets, and more.")
    print("Type /quit to exit, /new to start a new session.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not user_input:
            continue
        if user_input.lower() in ("/quit", "/exit"):
            break
        if user_input.lower() == "/new":
            agent = Agent(user_id=user_id)
            print("New session started.\n")
            continue

        try:
            response = agent.chat(user_input)
            print(f"\nAkwaaba AI: {response}\n")
        except Exception as e:
            print(f"\nError: {e}\n")


def main():
    user_id = "default"
    if len(sys.argv) > 1:
        user_id = sys.argv[1]
    run_cli(user_id)


if __name__ == "__main__":
    main()
