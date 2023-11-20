# Lazarus Forms API Python Library

## Installation
To install
```
pip install lazarus_ai
```
To upgrade
```
pip install lazarus_ai --upgrade
```

## Usage

We recommend storing your Lazarus auth credentials as environment variables.
```
# example .env file
ORG_ID=ORG_ID_HERE
AUTH_KEY=AUTH_KEY_HERE
```

### LazarusAuth
Before using Lazarus Forms or RikAI, you must authenticate using the LazarusAuth class. This auth object will be passed to Forms and RikAI class instantiations.

```
auth = LazarusAuth("ORG_ID_HERE", "AUTH_KEY_HERE")
```


### Forms
Upload a document using a file URL, a base64 encoded string, or a local file path. Run the standard OCR model on that document.
```
forms = Forms(auth)
forms.run_ocr("URL", "FILE_URL_HERE")
forms.run_ocr("BASE64", "BASE_64_STRING_HERE")
forms.run_ocr("FILE_PATH", "FILE_PATH_HERE")
```

Run a custom OCR model. 

```
forms = Forms(auth, "CUSTOM_MODEL_ID_HERE")
forms.run_ocr("URL", "FILE_URL_HERE")
forms.run_ocr("BASE64", "BASE_64_STRING_HERE")
forms.run_ocr("FILE_PATH", "FILE_PATH_HERE")
```

### RikAI
Upload a document using a file URL, a base64 encoded string, or a local file path. Run RikAI on that document.
```
rikai = RikAI(auth)
question = "QUESTION_HERE"
rikai.ask_question("URL", "FILE_URL_HERE", question)
rikai.ask_question("BASE64", "BASE_64_STRING_HERE", question)
rikai.ask_question("FILE_PATH", "FILE_PATH_HERE", question)
```

Run a custom RikAI model on that document.
```
rikai = RikAI(auth, "CUSTOM_MODEL_ID_HERE")
question = "QUESTION_HERE"
rikai.ask_question("URL", "FILE_URL_HERE", question)
rikai.ask_question("BASE64", "BASE_64_STRING_HERE", question)
rikai.ask_question("FILE_PATH", "FILE_PATH_HERE", question)
```

Run the RikAI summarizer on the document.
```
rikai = RikAI(auth, "CUSTOM_MODEL_ID_HERE")
fields = {"document_type": "TYPE_HERE", "summary_description": "DESCRIPTION_HERE"}
rikai.summarize("URL", "FILE_URL_HERE", fields)
rikai.summarize("BASE64", "BASE_64_STRING_HERE", fields)
rikai.summarize("FILE_PATH", "FILE_PATH_HERE", fields)
```
