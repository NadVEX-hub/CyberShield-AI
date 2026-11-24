print("Welcome to CyberShield AI!")
print("Detect. Protect. Educate.")

url = input("Enter a website URL: ").strip().lower()

risk_score = 0

if not url.startswith("https://"):
    risk_score += 20
    print("Warning: HTTPS is missing.")

if "verify" in url:
    risk_score += 20
    print("Warning: Contains the word verify.")

if len(url) > 75:
    risk_score += 20
    print("Warning: URL is unusually long.")

if "@" in url:
    risk_score += 20
    print("Warning: Contains the @ symbol.")

print("Risk score:", risk_score, "/ 80")

if risk_score >= 60:
    print("Classification: HIGH RISK")
    print("Recommendation: Avoid entering personal information.")

elif risk_score >= 40:
    print("Classification: MEDIUM RISK")
    print("Recommendation: Verify the website before proceeding.")

else:
    print("Classification: LOW RISK")
    print("Recommendation: Stay cautious. Safety is not guaranteed.")




