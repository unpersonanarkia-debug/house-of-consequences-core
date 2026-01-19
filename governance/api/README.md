# House of Consequences Governance API

Tämä API tarjoaa auditointiin ja governance-enforcementiin liittyvät REST-rajapinnat seuraavasti:

## 🎯 Tavoite

API mahdollistaa:
- audit-loki-tapahtumien keräämisen
- audit-ketjun rakentamisen (append-only, cryptographically chained)
- oikeudellisesti validoitavien raporttien generoinnin (PDF + QES)
- hallinnollisen governance-tilan seurannan

Se ei sisällä UI-logiikkaa tai casebook-mallinnuksia — nämä hoidetaan erillisissä komponenteissa.

## 📦 Endpoints

### 🧾 Audit entries
POST /audit/entry  
Lisää uusi audit-tapahtuma ketjuun.

### 📜 Audit chain
GET /audit/chain  
Palauttaa koko audit-ketjun järjestyksessä.

### 📊 Audit report
POST /audit/report  
Generoi PDF-muotoinen audit-raportti ja QES-allekirjoituksen.

### 📡 Governance status
GET /governance/status  
Yhteenveto audit-ketjusta ja tilasta.

## 🔐 Oikeudellisuus ja validointi

Tämä API toimii JSON-skeemojen mukaisesti ja validointia tehdään:

- schemas/audit.log.schema.json  
- schemas/audit.log.storage.schema.json  
- schemas/audit.report.schema.json  
- schemas/governance.enforcement.schema.json

Validointi varmistaa, että kaikki data noudattaa sovittuja normeja ja on oikeudellisesti kelvollista tallennettavaksi.

## 🛠 Tekninen stack

- Python (FastAPI)
- JSON Schema (2020-12)
- Cryptographic chaining (SHA-256 / BLAKE3)
- PDF generation (ReportLab)
- QES signing (RSA 4096, PSS + SHA-256)
