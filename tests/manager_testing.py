from include.groq import call_groq
from include.discord import send_to_discord

commits = [
    "feat: add pagination loop and token bucket",
    "feat: add testing"
]

response = call_groq(commits)

send_to_discord(response)