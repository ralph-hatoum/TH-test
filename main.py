from fastapi import FastAPI, Request, HTTPException
import encrypt_decrypt
import sign_verify

app = FastAPI()

@app.post("/encrypt")
async def encrypt(request: Request):
    request_json = await request.json()
    return encrypt_decrypt.encrypt_dict(request_json)

@app.post("/decrypt")
async def decrypt(request: Request):
    request_json = await request.json()
    return encrypt_decrypt.decrypt_dict(request_json)

@app.post("/sign")
async def sign(request: Request):
    request_json = await request.json()
    signature = sign_verify.sign(request_json)
    return {"signature":signature}

@app.post("/verify")
async def verify(request: Request):
    request_json = await request.json()
    valid = sign_verify.verify(request_json)
    if not valid:
        raise HTTPException(status_code=400, detail="Signature invalid")
    else:
        return None