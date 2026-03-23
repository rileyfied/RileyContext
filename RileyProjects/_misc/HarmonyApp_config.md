import os  
import shutil  
from pathlib import Path  
from fastapi import FastAPI, File, UploadFile, HTTPException  
from fastapi.responses import FileResponse  
from fastapi.middleware.cors import CORSMiddleware  
from spleeter.separator import Separator

\# \--- CONFIGURATION \---  
\# This is where we receive uploads and store the split files  
UPLOAD\_DIR \= Path("uploads")  
OUTPUT\_DIR \= Path("separated\_audio")

\# Create these folders if they don't exist  
UPLOAD\_DIR.mkdir(exist\_ok=True)  
OUTPUT\_DIR.mkdir(exist\_ok=True)

\# Initialize the App  
app \= FastAPI()

\# Allow your React app to talk to this server (CORS Security)  
app.add\_middleware(  
    CORSMiddleware,  
    allow\_origins=\["\*"\],   
    allow\_credentials=True,  
    allow\_methods=\["\*"\],  
    allow\_headers=\["\*"\],  
)

\# Initialize the AI Brain (Spleeter)  
\# This downloads the AI model the first time you run it.  
print("Initializing AI Model... this might take a minute...")  
separator \= Separator('spleeter:4stems')  
print("AI Model Ready.")

@app.get("/")  
def read\_root():  
    return {"status": "online", "message": "HarmonyHelper AI Brain is Ready"}

@app.post("/split-audio")  
async def split\_audio(file: UploadFile \= File(...)):  
    try:  
        \# 1\. Save the uploaded file  
        file\_location \= UPLOAD\_DIR / file.filename  
        with open(file\_location, "wb") as buffer:  
            shutil.copyfileobj(file.file, buffer)  
              
        print(f"Received file: {file.filename}. Starting separation...")

        \# 2\. Run the AI Separation  
        separator.separate\_to\_file(str(file\_location), str(OUTPUT\_DIR))  
          
        \# 3\. Construct the download links  
        song\_name \= file\_location.stem \# filename without extension  
        result\_path \= OUTPUT\_DIR / song\_name  
          
        print(f"Separation complete. Results at: {result\_path}")

        return {  
            "status": "success",  
            "song\_name": song\_name,  
            "stems": {  
                "soprano": f"/files/{song\_name}/vocals.wav", \# Mapping Vocals \-\> Soprano  
                "alto": f"/files/{song\_name}/other.wav",     \# Mapping Other \-\> Alto  
                "tenor": f"/files/{song\_name}/drums.wav",    \# Mapping Drums \-\> Tenor  
                "bass": f"/files/{song\_name}/bass.wav"       \# Mapping Bass \-\> Bass  
            }  
        }

    except Exception as e:  
        print(f"Error: {e}")  
        raise HTTPException(status\_code=500, detail=str(e))

@app.get("/files/{song\_name}/{stem\_name}")  
async def get\_audio\_file(song\_name: str, stem\_name: str):  
    file\_path \= OUTPUT\_DIR / song\_name / stem\_name  
    if file\_path.exists():  
        return FileResponse(file\_path)  
    return HTTPException(status\_code=404, detail="Stem not found")  
