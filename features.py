def extract_features(url):
    url = url.strip().lower()

    suspicious_words = [
        "verify", "login", "password",
        "secure", "update", "urgent",
        "account", "confirm"
    ]

    features = {
        "url_length": len(url),
        "has_https": int(url.startswith("https://")),
        "dot_count": url.count("."),
        "hyphen_count": url.count("-"),
        "at_count": url.count("@"),
        "digit_count": sum(c.isdigit() for c in url),
        "slash_count": url.count("/"),
        "question_count": url.count("?"),
        "percent_count": url.count("%"),
        "suspicious_words": sum(
            word in url for word in suspicious_words
        )
    }

    return features


if __name__ == "__main__":
    url = input("Enter a website URL: ")
    print(extract_features(url))
