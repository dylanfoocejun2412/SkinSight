from jamaibase import JamAI, protocol as p

# Initialize JamAI client with your API key and project ID
API_KEY = "jamai_sk_dd6199ad3508babf09fcf71ab8f10e0c549f2d188c9e319b"
PROJECT_ID = "proj_64591c7c611bfa70f12f511d"

# Table IDs for user advice and doctor advice
USER_ADVICE_TABLE_ID = "medical_advice"
DOCTOR_ADVICE_TABLE_ID = "doctor_advice"

# Initialize JamAI client
jamai = JamAI(api_key=API_KEY, project_id=PROJECT_ID)

def generate_user_advice(prediction, confidence):
    """Generate AI advice for users based on prediction and confidence score."""
    try:
        completion = jamai.add_table_rows(
            "action",
            p.RowAddRequest(
                table_id=USER_ADVICE_TABLE_ID,
                data=[{"input": f"The lesion is classified as {prediction} with a confidence level of {confidence:.2f}%."}],
                stream=False
            )
        )

        # Extract the AI-generated advice
        if completion.rows:
            advice = completion.rows[0].columns.get("reply").text
            return advice if advice else "No advice available."
        else:
            return "Failed to get a response from JamAI."

    except Exception as e:
        return f"An error occurred: {str(e)}"

def generate_doctor_advice(prediction, confidence):
    """Generate AI advice for doctors based on prediction and confidence score."""
    try:
        completion = jamai.add_table_rows(
            "action",
            p.RowAddRequest(
                table_id=DOCTOR_ADVICE_TABLE_ID,
                data=[{"input": f"The lesion is classified as {prediction} with a confidence level of {confidence:.2f}%. Please provide detailed recommendations and treatment plans for users."}],
                stream=False
            )
        )

        # Extract the AI-generated doctor advice
        if completion.rows:
            doctor_advice = completion.rows[0].columns.get("doctor_reply").text
            return doctor_advice if doctor_advice else "No advice available for doctors."
        else:
            return "Failed to get a response from JamAI."

    except Exception as e:
        return f"An error occurred: {str(e)}"
