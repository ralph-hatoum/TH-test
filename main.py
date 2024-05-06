from fastapi import FastAPI, Request, HTTPException, Response
import encrypt_decrypt
import sign_verify
from pydantic import BaseModel, ValidationError

app = FastAPI()

@app.post("/encrypt")
async def encrypt(request: Request):
    """
    Handler for POST requests on /encrypt
    """
    try:
        payload = await request.json()
        return encrypt_decrypt.encrypt_dict(payload)
    except Exception as exc:
        raise HTTPException(status_code=400, detail="bad request; expecting json payload") from exc

@app.post("/decrypt")
async def decrypt(request: Request):
    """
    Handler for POST requests on /decrypt
    """
    try:
        payload = await request.json()
        return encrypt_decrypt.decrypt_dict(payload)
    except Exception as exc:
        raise HTTPException(status_code=400, detail="bad request; expecting json payload") from exc

@app.post("/sign")
async def sign(request: Request):
    """
    Handler for POST requests on /sign
    """
    try:
        payload = await request.json()
        signature = sign_verify.sign(payload)
        return {"signature":signature}
    except Exception as exc:
            raise HTTPException(status_code=400, detail="bad request") from exc

class VerifyPayload(BaseModel):
    """
    The payload on a POST on /verify needs to contain a signature field and a data field.
    If there are other fields, the request will still be 
    """
    signature: str
    data: dict

@app.post("/verify")
async def verify(request: Request):
    """
    Handler for POST requests on /verify
    """
    try:
        payload = await request.json()
        payload = VerifyPayload(**payload)
    except:
        raise HTTPException(status_code=400, detail="bad request")
    valid = sign_verify.verify(payload)
    if not valid:
        raise HTTPException(status_code=400, detail="Signature invalid")
    else:
        return Response(status_code=204)

    
# GENERAL TODO :   MAKE A SWAGGER DOC MAYBE