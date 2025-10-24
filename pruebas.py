import os
from dotenv import load_dotenv

test =load_dotenv()

print(os.getenv("GMAIL_PASS_APP"))