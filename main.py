from fastapi import FastAPI, UploadFile, File, HTTPException
from pathlib import Path
import shutil
from services.gen_ai_llm import generate_response

app = FastAPI()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.get("/")
def read_root():
    return {"message": "FastAPI app running with Poetry & Docker"}


@app.post("/bank-statement-analysis")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")

    file_path = UPLOAD_DIR / file.filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    print(file_path)

    # return {
    #     "filename": file.filename,
    #     "content_type": file.content_type,
    #     "saved_to": str(file_path),
    #     "path": file_path
    # }

    # this will give json or dict as output
    response = generate_response(filepath=str(file_path))

    # Safety check
    if not isinstance(response, dict):
        raise HTTPException(status_code=500, detail="Invalid model response")


    if response.get("is_bank_statement") is False:
        return {
            "is_bank_statement": False,
            "message": "Given file is not a bank statement"
        }


    return {
        "is_bank_statement": True,
        "bank_details": {
            "bank_name": response.get("bank_name"),
            "account_name": response.get("account_name"),
            "CIF_ID": response.get("CIF_ID"),
            "IFSC": response.get("IFSC"),
            "statement_period": response.get("statement_period"),
        },
        "transactions": response.get("transactions", []),
        "analysis": response.get("analysis"),
        "costing":response.get("costing")
    }