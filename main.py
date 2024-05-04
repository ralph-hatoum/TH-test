from fastapi import FastAPI, Request
import encrypt_decrypt

app = FastAPI()

@app.post("/encrypt")
async def encrypt(request: Request):
    request_json = await request.json()
    return encrypt_decrypt.encrypt_dict(request_json)

@app.post("/decrypt")
async def decrypt(request: Request):
    request_json = await request.json()
    return encrypt_decrypt.decrypt_dict(request_json)
