# Cronjobs Museum Schaffen

`eventfrog_to_mus.py` schreibt `data/mus_export.json` nur für Eventfrog-OrgID **5116588**.

```bash
pip install -r cronjobs/requirements.txt
EVENTFROG_API_KEY=<key> python cronjobs/eventfrog_to_mus.py
```

API-Key: Umgebungsvariable oder Datei `cronjobs/eventfrog_api_key` (Vorlage: `eventfrog_api_key.example`). Nicht committen.
