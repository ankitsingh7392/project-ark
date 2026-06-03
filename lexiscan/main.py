import os
from pathlib import Path

from lexiscan import LexiModel

DATA_PATH = os.getenv("LEXISCAN_DATA_PATH", str(Path(__file__).parent / "data" / "enterprise_tickets.csv"))

model = LexiModel(use_tfidf=True)
model.train(data_path=DATA_PATH, text_column="ticket_text", label_column="department")

# Make a prediction
inputs = [
    # --- Billing (clear but long) ---
    "Hi, I was checking my latest invoice and noticed that I’ve been charged twice for the same subscription this month. I already paid once last week, but now I see another deduction from my account. Can you please look into this and process a refund if this is an error?",

    # --- Billing (ambiguous wording) ---
    "I don’t fully understand my bill. The amount seems higher than usual and I think there might be some extra charges added. Also, I updated my card recently, not sure if that caused any issue. Can you clarify and fix if needed?",

    # --- Technical Support (clear) ---
    "Every time I try to open the app after logging in, it just freezes and then crashes after a few seconds. I tried reinstalling it but the problem still exists. This is really frustrating as I cannot access my account at all.",

    # --- Technical Support (multi-issue: login + billing confusion) ---
    "I was trying to log in today but couldn’t access my account because it says invalid credentials. I reset my password but still no luck. Also, I wanted to check my invoice but now I can't even log in. Please help urgently.",

    # --- Returns (clear) ---
    "I recently purchased an item but it arrived damaged. The screen is cracked and it doesn’t work properly. I would like to return it and get either a replacement or a refund. Please let me know the return process.",

    # --- Returns (mixed with shipping confusion) ---
    "I want to return the product I bought last week because it is not working as expected. However, I haven’t received any return label or instructions yet. Also, I’m not sure if I need to pay for shipping or if it’s covered.",

    # --- Ambiguous (Billing vs Returns → model may fail) ---
    "I returned an item a few days ago but I still haven’t received my money back. I’m not sure if this is a refund issue or something related to the return process. Can you check the status for me?",

    # --- Ambiguous (Technical vs Billing) ---
    "The app is not letting me update my payment method. Every time I try to add a new card, it throws an error. Because of this, I think my payment didn’t go through. Can you fix this?",

    # --- Unknown / Out-of-scope ---
    "Do you offer any discounts for students or seasonal promotions? I am planning to buy soon and wanted to check if there are any ongoing deals.",

    # --- Unknown / General inquiry ---
    "Can you tell me more about your company policies and how long you have been operating? I am just trying to understand your services better before making a purchase.",

    # --- Noisy real-world style (multiple intents → hard case) ---
    "Hi team, I ordered a product last week and it arrived broken, so I want to return it. At the same time, I noticed I was already charged for it and I’m worried about how the refund will be processed. Also, your app keeps crashing when I try to check the return status. This whole experience has been confusing, please assist."
]

for new_ticket in inputs:
    prediction = model.predict(new_ticket)
    print(f"Routing ticket to: {prediction['category']} (Confidence: {prediction['confidence']}%)")
