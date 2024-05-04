from fastapi import FastAPI, Request, HTTPException
import encrypt_decrypt
import sign_verify

app = FastAPI()

@app.post("/encrypt")
async def encrypt(request: Request):
    payload = await request.json()
    return encrypt_decrypt.encrypt_dict(payload)

@app.post("/decrypt")
async def decrypt(request: Request):
    payload = await request.json()
    return encrypt_decrypt.decrypt_dict(payload)

@app.post("/sign")
async def sign(request: Request):
    payload = await request.json()
    signature = sign_verify.sign(payload)
    return {"signature":signature}

@app.post("/verify")
async def verify(request: Request):
    payload = await request.json()
    valid = sign_verify.verify(payload)
    if not valid:
        raise HTTPException(status_code=400, detail="Signature invalid")
    else:
        return None