# Sito ruggierorusso.com

Sito statico del fotografo Ruggiero Russo (ERRE studio, Barletta). Ospitato gratis su Netlify,
dominio e posta su Aruba.

## Come è fatto
- `site/` – il sito pubblicato (Netlify pubblica questa cartella, nessun comando di build).
- `build.py` – rigenera tutte le pagine (IT + EN) da `catalogo.json`, dalle foto in `site/img/` e da `instagram.json`.
- `catalogo.json` – i 37 progetti: titolo, categoria (FASHION / STILL-LIFE / ADVERTISING), crediti, foto.
- `instagram_sync.py` – scarica gli ultimi post Instagram in `site/img/ig/` e scrive `instagram.json`.
- `.github/workflows/instagram.yml` – ogni giorno: rinnova il token, scarica i post, rigenera il sito, pubblica.
- `tools/check.js` – controllo link e screenshot (Playwright).

## Instagram
- Ogni post appare nella sezione **Diario** della home (ultimi 12).
- Se la didascalia contiene **#portfolio**, il post diventa anche una pagina progetto:
  prima riga = titolo; righe `BRAND: ...`, `MODEL: ...` ecc. = crediti;
  categoria con **#fashion**, **#stilllife** oppure (default) advertising.

## Secrets del repository (Settings → Secrets and variables → Actions)
- `IG_TOKEN` – token a lunga durata dell'Instagram API with Instagram Login (permesso `instagram_business_basic`).
- `GH_PAT` – (facoltativo) token GitHub fine-grained con permesso *Secrets: read and write* su questo repository,
  serve al workflow per salvare il token Instagram rinnovato. Senza, il token Instagram va rinnovato a mano ogni 60 giorni.

## Netlify
Collegare il progetto Netlify esistente (ruggierorussophotography) a questo repository:
Project configuration → Build & deploy → Link repository → GitHub → `sito-ruggierorusso`,
branch `main`, publish directory `site`, build command vuoto.

## Aggiornare a mano
```
python3 build.py          # rigenera le pagine
```
