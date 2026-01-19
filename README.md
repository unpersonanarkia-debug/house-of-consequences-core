# House of Consequences – Core

House of Consequences on avoin, oikeudellisesti todennettava ja yhteiskunnallisesti vastuullinen järjestelmä päätösten, toimien ja seurausten dokumentointiin, auditointiin ja jäljitettävyyteen.

Tämä repository sisältää järjestelmän ytimen: protokollan, skeemat, governance-rajapinnat ja todentamismallit. Se ei ole poliittinen ohjelma, eikä päätöksentekojärjestelmä, vaan *todennettavan vastuun infrastruktuuri*.

---

## 🎯 Tarkoitus

House of Consequences -järjestelmän tarkoitus on:

- estää haitallisten seurausten normalisoituminen päätöksenteossa,
- tehdä päätöksenteon vaikutukset näkyviksi ja jäljitettäviksi,
- mahdollistaa oikeudellisesti pätevän auditoinnin,
- tarjota avoin ja vastuullinen infrastruktuuri yhteiskunnalliseen valvontaan.

Järjestelmä ei:
- tee päätöksiä,
- arvioi moraalia,
- ohjaa politiikkaa,
- tarjoa käyttöliittymää.

Se tarjoaa *todentamisen, jäljitettävyyden ja vastuun rakenteen*.

---

## 🧱 Arkkitehtuurin kokonaiskuva

Päätöksenteko- ja toimeenpanojärjestelmät]
|
v
Governance API (auditointi)
|
v
Audit-lokit → Hash-ketjut → Raportit → QES-allekirjoitus
|
v
Avoin tarkastus / viranomaisvalvonta / tutkimus

Core-repo sisältää:
- skeemat (JSON Schema),
- governance-API:n,
- raportointi- ja allekirjoituskerroksen,
- governance-dokumentaation,
- valvontamallit.

---

## 🗂 Repository-rakenne

house-of-consequences-core/
├── governance/
│   ├── api/                  # Auditointi- ja governance-rajapinta
│   ├── schemas/              # JSON Schema -määrittelyt
│   ├── reports/              # Raporttimallit ja -muodot
│   └── enforcement/          # Governance-valvonta ja sanktiomallit
├── protocols/                # Protokollamäärittelyt ja ketjurakenteet
├── compliance/               # Lainsäädäntö- ja standardiviittaukset
├── docs/                     # Arkkitehtuuri, käyttö, governance
├── examples/                 # Esimerkkidata ja käyttötapaukset
├── tests/                    # Testaus ja validointi
└── README.md                 # Tämä tiedosto

---

## 📜 Skeemat ja protokollat

Core nojaa seuraaviin periaatteisiin:

- *Append-only audit-lokit*
- *Kryptografinen ketjutus*
- *Aikaleimat*
- *WORM-yhteensopivuus*
- *QES-allekirjoitus (eIDAS)*

Kaikki tapahtumat validoidaan JSON Schema draft 2020-12 -skeemoilla ennen tallennusta.

Keskeiset skeemat:

| Skeema | Tarkoitus |
|--------|------------|
| audit.log.schema.json | Yksittäinen audit-merkintä |
| audit.log.storage.schema.json | Audit-ketjun säilytys |
| audit.report.schema.json | Raportin rakenne |
| governance.enforcement.schema.json | Governance-valvonta |

---

## 🔐 Oikeudellinen kelpoisuus

House of Consequences on suunniteltu täyttämään:

- eIDAS-vaatimukset (QES),
- GDPR:n jäljitettävyys- ja tilivelvollisuusperiaatteet,
- ISO 27001 / 27701,
- NIS2,
- SOC2.

Tämä mahdollistaa järjestelmän käytön:

- hallinnollisissa prosesseissa,
- sääntelyvalvonnassa,
- oikeudellisissa riidoissa,
- forenssisissa tutkimuksissa.

---

## 🧭 Governance-malli

Järjestelmä noudattaa seuraavia periaatteita:

- Avoin lähdekoodi (AGPL-3.0).
- Avoimet skeemat ja dokumentaatio.
- Päätöksenteko erotettu audit-kerroksesta.
- Muutokset protokollaan dokumentoidaan ja versioidaan.
- Yhteisöllinen valvonta ja tarkastettavuus.

Katso: docs/GOVERNANCE_MODEL.md.

---

## 🛠 Tekninen perusta

- *Kieli*: Python 3.11+
- *API*: FastAPI
- *Validointi*: JSON Schema 2020-12
- *Raportointi*: ReportLab
- *Allekirjoitus*: RSA-4096, SHA-256, QES-yhteensopiva
- *Hashaus*: SHA-256, BLAKE3

---

## ⚠️ Rajaukset

Tämä projekti ei:
- ole poliittinen ohjelma,
- tee päätöksiä,
- tarjoa käyttöliittymää,
- kerää henkilötietoja oletusarvoisesti.

Se on *vastuun ja seurausten todentamisen infrastruktuuri*.

---

## 📄 Lisenssi

Ydinkoodi: *AGPL-3.0*  
Dokumentaatio: *CC-BY-SA-4.0*

Enterprise-käyttö: erillinen sopimus.

---

## 📬 Yhteystiedot

Tekninen tuki: GitHub Issues  
Governance-keskustelu: GitHub Discussions  
Yhteistyö ja pilotit: contact@houseofconsequences.org
