from modules.pdf_generator import generate_daily_pdf

# Dummy Data with Realistic Keys (from config.py)
ai_report = {
    "⚖️ International Law": "According to <https://jurist.org/news/2024/05/venezuela-amnesty|Jurist News>, *Venezuela's imminent amnesty bill* set to activate within a week...",
    "🌍 International Relations": "1. *Canada's Supreme Court* has recently established a groundbreaking exception to solicitor-client privilege...",
    "🇵🇰 National & Political (Pakistan)": "As the federal government seeks consensus on sweeping judicial reforms...",
    "💻 Tech & Innovation": "The European Commission faces mounting pressure to invoke the Digital Services Act..."
}

learning_item = {
    "title": "Quantum Encryption",
    "content": "Post-quantum cryptography (PQC) refers to cryptographic algorithms (usually public-key algorithms) that are thought to be secure against a cryptanalytic attack by a quantum computer. As quantum computers become more powerful, current encryption standards like RSA will become vulnerable."
}

print("Generating Test PDF...")
path = generate_daily_pdf(ai_report, learning_item)
if path:
    print(f"Success! PDF at: {path}")
else:
    print("Failed to generate PDF.")
