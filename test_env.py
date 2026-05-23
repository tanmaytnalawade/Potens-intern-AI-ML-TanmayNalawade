from dotenv import load_dotenv
import os


load_dotenv()

api_key = os.getenv(
    "GROQ_API_KEY"
)

if api_key:

    print("\nGROQ API KEY LOADED SUCCESSFULLY!\n")

    print(
        api_key[:10] + "..."
    )

else:

    print(
        "\nAPI KEY NOT FOUND\n"
    )