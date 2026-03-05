def analyze_text(text):

    text = text.lower()

    clauses = {
        "Data Collection Disclosure": ["collect", "data", "information"],
        "User Consent Clause": ["consent", "permission", "agree"],
        "Purpose Limitation": ["purpose", "use", "service"],
        "Data Retention Policy": ["retain", "store", "retention"],
        "User Data Deletion Rights": ["delete", "remove", "erase"]
    }

    detected = []

    for clause, keywords in clauses.items():

        for word in keywords:
            if word in text:
                detected.append(clause)
                break

    return detected