# Beaker - CE Note Taker
Capture notes and info

## Run Code Locally
```
pip3 install virtualenv
python3 -m virtualenv .venv
source .venv/bin/activate
pip3 install -r src/requirements.txt
python3 src/main.py
```
Then you can browse the code [locally](http://localhost:8080).<br /><br />
**Deactivate the environment** 
Run the following command
```
deactivate
```

## Config
Config is either via local file [config.json](code/config.json) or recreating with environmental variables:<br />
**EXAMPLE:**
```bash
GCP_PROJECT='beaker-416605'
GCS_BUCKET='beaker-416605-upload'
COLLECTIONID='notes'
```
