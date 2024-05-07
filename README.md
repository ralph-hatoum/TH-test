# Take home test

Starting the server :
```
uvicorn main:app --port 8000 --reload
````
If any requirements are missing, use : 
````
pip install -r requirements.txt
````

Running unit tests :
````
python unit_tests.py
````
Running integration tests :
````
python integration_tests.py
````
Once the server is started, a documentation is available :
````
localhost:8000/docs
````

# Assumptions made

## Decrypt endpoint
Any field in the payload that can be decrypted, will be. All fields will be returned as strings. This means any strings that fit the following regex : 
````
^[-A-Za-z0-9+/]*={0,3}$
````
will be decrypted. If you have fields that fit this regex in plaintext, it is recommended to add some recognizable prefix or suffix to the data to avoid having unwanted decryption, but this is left to the user, according to how your business logic works.

## Sign endpoint
Upon signing, the payload is decrypted, so the previous limitation applies.