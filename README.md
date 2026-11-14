# Sito ruggierorusso.com

Sito statico del fotografo Ruggiero Russo (ERRE studio, Barletta). Ospitato gratis su Netlify,
dominio e posta su Aruba.

## Come è fatto
- `site/` – il sito pubblicato (Netlify pubblica questa cartella, nessun comando di build).
- `build.py` – rigenera tutte le pagine (IT + EN) da `catalogo.json`, dalle foto in `site/img/`.
- `catalogo.json` – i 37 progetti: titolo, categoria (FASHION / STILL-LIFE / ADVERTISING), crediti, foto.
- `tools/check.js` – controllo link e screenshot (Playwright).


## Netlify
Collegare il progetto Netlify esistente (ruggierorussophotography) a questo repository:
Project configuration → Build & deploy → Link repository → GitHub → `sito-ruggierorusso`,
branch `main`, publish directory `site`, build command vuoto.

## Aggiornare a mano
```
python3 build.py          # rigenera le pagine
```

## Nota
Il collegamento automatico con Instagram (sezione Diario) è stato rimosso il 14/11/2026 su richiesta del titolare.
