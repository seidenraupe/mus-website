# MuS-Website

**Live:** https://seidenraupe.github.io/mus-website/

Neuimplementierung von [museumschaffen.ch](https://www.museumschaffen.ch/) als statische Website: gleiche Informationsarchitektur und das typische Schwarz-Weiss-Raster (grosse Fliessschrift, Ticker, Zeilenraster). Die Originalschrift **Agipo Light** (Radim Peško) ist nur für museumschaffen.ch lizenziert — lokal steht Outfit als geometrischer Ersatz.

## Veranstaltungen (Eventfrog)

Quelle ist derselbe **Coucou-JSON-Export** wie in [prototype-hvw-website](https://github.com/seidenraupe/prototype-hvw-website), gefiltert auf die Eventfrog-Organisation **Museum Schaffen, OrgID `5116588`**.

| Datei | Rolle |
|---|---|
| `data/mus_export.json` | Aktueller Export (Snapshot + tägliches Update) |
| `scripts/fetch-mus-events.mjs` | Node-Fetch für GitHub Actions |
| `cronjobs/eventfrog_to_mus.py` | Gleiches Layout, für Hostpoint-Cron |

Felder wie im HVW-Export: `reference`, `title`, `description`, `description_long`, `description_html`, `image`, `url`, `date`, `time_start`, `time_end`, `category`, Location-Felder.

```bash
EVENTFROG_API_KEY=<key> npm run fetch:events
```

GitHub Action `.github/workflows/update-eventfrog-events.yml` läuft täglich um 05:00 UTC. Secret `EVENTFROG_API_KEY` im Repo hinterlegen (gleicher Public-API-Key wie beim HVW-Prototyp).

Live-Referenz des bestehenden Exports: `https://www.hvwinterthur.ch/mus_export.json`

## Lokal ansehen

```bash
python -m http.server 8080
# → http://localhost:8080
```

## Seiten

- Start (aktuell / Programm / Journal)
- Ausstellungen inkl. Erinnerungstank Haldengut
- Programm + Eventdetail aus JSON
- Besucherinfos, Journal, Über uns, Kontakt, Raummiete, Medien, Unterstützen, Newsletter, Impressum, Datenschutz

## Hinweise

- Bilder der aktuellen Ausstellung und Journal-Teaser stammen von museumschaffen.ch (Museum Schaffen).
- Eventbilder kommen von Eventfrog.
- Cursor-hosted Git (`origin.cursor.com`) ist auf nativem Windows noch nicht unterstützt; GitHub ist die aktive Remote.
