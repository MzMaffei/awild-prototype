# A Wild World — prototipo di redesign

Prototipo statico di redesign per awild.world (Federica Portentoso), preparato a novembre 2026 come proposta.
Non è il sito ufficiale: tutte le pagine sono `noindex`, gli acquisti rimandano al sito vero.

- `pages/` — corpo delle pagine (prima riga: `<!-- titolo | descrizione | voce di menu -->`)
- `build.py` — assembla `pages/` + header/footer comuni in `docs/` (`python3 -I build.py`)
- `docs/` — sito pubblicato con GitHub Pages (branch `main`, cartella `/docs`)
- `check.js` — smoke test Playwright su mobile e desktop (`node check.js <path-to-playwright>`)
- `docs/protocollo.html` — protocollo delle modifiche per Squarespace, in ordine di priorità

Testi e foto appartengono a Federica Portentoso; le immagini sono caricate dalla sua CDN Squarespace.

Preparato da Claude (claude@tasty.lu), assistente AI di Maurizio Maffei.
