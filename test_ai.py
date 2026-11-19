
from ai_engine import generate_response

print("Testing AI connection...")
print()

try:
    answer = generate_response(
        "Hello! Introduce yourself as an AI student "
        "study assistant in three sentences."
    )

    print("AI connection successful!")
    print()
    print("AI Response:")
    print(answer)

except Exception as error:
    print("AI connection failed.")
    print(error)
