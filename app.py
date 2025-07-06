from flask import Flask, request, jsonify
import re

app = Flask(__name__)

@app.route('/extract-jd', methods=['POST'])
def extract_jd():
    try:
        data = request.get_json()
        text = data.get("emailText", "")

        # Flexible pattern to match "Label : value" or "Label value"
        def extract(label):
            pattern = rf"{label}\s*:?\s*(.+)"
            match = re.search(pattern, text, re.IGNORECASE)
            return match.group(1).strip() if match else ""

        result = {
            "JobTitle": extract("Job Title"),
            "Experience": extract("Experience"),
            "Skills": extract("Skills"),
            "Location": extract("Location"),
            "Duration": extract("Duration"),
            "Client": extract("Client")
        }

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render sets this dynamically
    app.run(host="0.0.0.0", port=port)
