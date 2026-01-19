# House of Consequences – Governance API

Tämä API tarjoaa oikeudellisesti kelvollisen auditointi- ja governance-rajapinnan House of Consequences -ytimelle. Se vastaa päätösten, toimien ja järjestelmätilojen jäljitettävästä kirjaamisesta, raportoinnista ja todentamisesta.

API on tarkoitettu:
- viranomaisille,
- instituutioille,
- riippumattomille tarkastajille,
- kansalaisinstansseille ja
- tutkimus- ja compliance-käyttöön.

Se ei ole käyttöliittymä eikä päätöksentekojärjestelmä, vaan *audit- ja todentamiskerros*.

---

## 🎯 Tarkoitus

Governance API mahdollistaa:

- tapahtumien append-only audit-lokituksen,
- kryptografisesti ketjutetun lokiketjun ylläpidon,
- oikeudellisesti pätevien raporttien (PDF) tuottamisen,
- Qualified Electronic Signature (QES) -allekirjoituksen raportteihin,
- hallinnollisen ja institutionaalisen valvonnan tukemisen.

API ei:
- tee päätöksiä,
- arvioi politiikkaa,
- tarjoa käyttöliittymää,
- sisällä AI-mallien logiikkaa.

---

## 🧱 Arkkitehtuurirooli

Governance API toimii seuraavasti:

[Päätösjärjestelmät / UI:t]
|
v
Governance API
|
v
Audit-lokit → Hash-ketju → PDF-raportti → QES-allekirjoitus

Kaikki tapahtumat validoidaan JSON Schema -malleilla ennen tallennusta.

---

## 📦 Keskeiset endpointit

### 🧾 Lisää audit-merkintä
*POST* /audit/entry

Lisää uuden tapahtuman audit-ketjuun.

- Syöte validoidaan audit.log.schema.json mukaan.
- Tapahtuma ketjutetaan edelliseen hashilla.
- Tallennus on append-only.

---

### 📜 Hae audit-ketju
*GET* /audit/chain

Palauttaa koko audit-ketjun kronologisessa järjestyksessä.

---

### 📊 Generoi audit-raportti
*POST* /audit/report

Luo PDF-muotoisen raportin audit-ketjusta.

- Raportti allekirjoitetaan Qualified Electronic Signature (QES) -tasolla.
- Palauttaa PDF-tiedoston sekä allekirjoitusmetadataa.

---

### 📡 Governance-tila
*GET* /governance/status

Palauttaa:
- lokiketjun tilan,
- viimeisimmän hashin,
- järjestelmän eheys- ja valmiustilan.

---

## 🔐 Oikeudellinen kelpoisuus

API noudattaa seuraavia periaatteita:

- *Append-only*: lokimerkintöjä ei voi muuttaa tai poistaa.
- *WORM-yhteensopivuus*: Write Once, Read Many.
- *Kryptografinen ketjutus*: jokainen merkintä viittaa edelliseen.
- *Aikaleimat*: ISO-8601, UTC.
- *QES-allekirjoitus*: eIDAS-yhteensopiva sähköinen allekirjoitus.

Tämä mahdollistaa audit-ketjun käytön:
- hallinnollisessa,
- sääntelyllisessä,
- oikeudellisessa ja
- forenssisessa kontekstissa.

---

## 📜 Skeemat ja validointi

API käyttää seuraavia JSON Schema -määrittelyjä:

| Skeema | Tarkoitus |
|--------|------------|
| schemas/audit.log.schema.json | Yksittäinen audit-merkintä |
| schemas/audit.log.storage.schema.json | Audit-ketjun säilytys |
| schemas/audit.report.schema.json | Audit-raportin rakenne |
| schemas/governance.enforcement.schema.json | Governance-valvontatila |

Kaikki POST-syötteet validoidaan näitä vasten ennen käsittelyä.

---

## 🛠 Tekninen toteutus

- *Framework*: FastAPI
- *Kieli*: Python 3.11+
- *Raportointi*: ReportLab
- *Allekirjoitus*: RSA-4096, SHA-256, QES-yhteensopiva
- *Validointi*: JSON Schema draft 2020-12
- *Hashaus*: SHA-256 / BLAKE3

---

## 🧭 Governance-malli

Tämä API toimii osana House of Consequences -governance-mallia:

- Core-protokolla on yhteisön omistuksessa (AGPL-3.0).
- Audit-logit ovat julkisesti todennettavissa.
- Päätöslogiikka on erotettu audit-kerroksesta.
- Muutokset governance-rakenteeseen tehdään dokumentoidusti ja läpinäkyvästi.

Katso: GOVERNANCE_MODEL.md.

---

## ⚠️ Rajaukset

Tämä API ei:
- korvaa viranomaisjärjestelmiä,
- tee päätöksiä,
- tarjoa poliittista arviointia,
- sisällä käyttäjähallintaa tai käyttöliittymää.

Se toimii *todentavana ja jäljitettävänä kerroksena* muiden järjestelmien alla.

---

## 📄 Lisenssi

Core-koodi: *AGPL-3.0*  
Governance-dokumentit: *CC-BY-SA-4.0*

Enterprise-palvelut: erillinen sopimus (katso projektin pää-README).

---

## 📬 Yhteystiedot

Tekniset kysymykset: GitHub Issues  
Governance-keskustelu: GitHub Discussions  
Yhteistyö ja pilotit: contact@houseofconsequences.org
