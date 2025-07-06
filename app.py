from fastapi import FastAPI, Request
from pydantic import BaseModel
from bs4 import BeautifulSoup

app = FastAPI()

class HTMLRequest(BaseModel):
    html: str

@app.post("/convert")
async def convert_html(request: HTMLRequest):
    soup = BeautifulSoup(request.html, "html.parser")
    text = soup.get_text(separator="\n").strip()
    
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    data = {
        "jobTitle": lines[0] if len(lines) > 0 else "",
        "experience": "",
        "location": "",
        "skills": "",
        "duration": ""
    }

    for line in lines:
        if line.lower().startswith("experience"):
            data["experience"] = line.replace("Experience:", "").strip()
        elif line.lower().startswith("location"):
            data["location"] = line.replace("Location:", "").strip()
        elif line.lower().startswith("skills"):
            data["skills"] = line.replace("Skills:", "").strip()
        elif line.lower().startswith("duration"):
            data["duration"] = line.replace("Duration:", "").strip()

    return data
