from fastapi import FastAPI, Request, HTTPException, Response
import encrypt_decrypt
import sign_verify
from pydantic import BaseModel
from fastapi.openapi.utils import get_openapi
import json

app = FastAPI()

@app.post("/encrypt")
async def encrypt(request: Request):
    """
    Handler for POST requests on /encrypt. 
    This endpoint expects a json payload, and will return a payload with
    the same fields, but with encrypted values.
    """
    try:
        payload = await request.json()
        return encrypt_decrypt.encrypt_dict(payload)
    except Exception as exc:
        raise HTTPException(status_code=400, detail="bad request; expecting json payload") from exc

@app.post("/decrypt")
async def decrypt(request: Request):
    """
    Handler for POST requests on /decrypt.
    This endpint expects a json payload, and will return a payload with
    the same fields, but with decrypted values, if decryption is possible.
    Limitations : if a plaintext string happens to fit what an encrypted string
    looks like, it will be decrypted. 
    For example, with base64, any string that fits the regex ^[-A-Za-z0-9+/]*={0,3}$
    will be decrypted.
    Also, all elements returned in the decrypted payload will be returned as strings.
    """
    try:
        payload = await request.json()
        return encrypt_decrypt.decrypt_dict(payload)
    except Exception as exc:
        raise HTTPException(status_code=400, detail="bad request; expecting json payload") from exc

@app.post("/sign")
async def sign(request: Request):
    """
    Handler for POST requests on /sign.
    Important : the decrypt function is called on the payload before signing,
    so similar limitations apply : if a plaintext string happens to fit what an encrypted string
    looks like, it will be decrypted. 
    For example, with base64, any string that fits the regex ^[-A-Za-z0-9+/]*={0,3}$
    will be decrypted.
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
    If there are other fields, the request will still be processed and the
    unexpected fields will be ignored.
    """
    signature: str
    data: dict

@app.post("/verify")
async def verify(request: Request):
    """
    Handler for POST requests on /verify
    The payload needs to have a signature field and a data field. If these are
    not provided, the request will not be processed.
    Succesful signature will return a 204 status code, other cases will be a 400.
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
    
with open("openapi.json", "r") as f:
    custom_openapi = f.read()

def custom_openapi_schema():
    return json.loads(custom_openapi)

app.openapi = custom_openapi_schema