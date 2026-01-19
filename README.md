# 🏛️ House of Consequences – Core Engine

*house-of-consequences-core* on institutionaalinen ydinjärjestelmä, joka tekee päätösten seuraukset näkyviksi, mitattaviksi ja oikeudellisesti jäljitettäviksi — ennen kuin päätökset normalisoituvat vahingoksi.

Tämä ei ole analytiikkatyökalu.
Tämä on *governance-infrastruktuuri*.


## 🔍 Mikä tämä on?

House of Consequences on universaali päätösten elinkaarimoottori, joka:

- mallintaa *päätöksen vaikutuksen, seuraukset, sopeutumisen, kertaantumisen, normalisoitumisen ja oppimisen*,
- lukitsee nämä vaiheet *JSON Schema -rakenteiksi*,
- validoi ne *FastAPI-palvelulla*,
- kirjaa kaikki vaiheet *oikeudellisesti päteviin audit-lokeihin*,
- tuottaa *allekirjoitettuja PDF-raportteja (QES)*,
- ja mahdollistaa *jälkikäteisen vastuun kohdentamisen*.


## 🎯 Miksi tämä on olemassa?

Koska yhteiskunnat eivät kaadu yksittäisiin virheisiin,
vaan siihen, että virheistä tulee *normaali tila*.

Tämä järjestelmä estää:

- haitallisten tilojen normalisoitumisen,
- vastuun hämärtymisen,
- päätösten vaikutusten katoamisen instituutioiden sisään.


## 🧠 Keskeinen periaate

**Yksikään päätös ei ole valmis ennen kuin sen seuraukset on mallinnettu, mitattu ja arkistoitu.**


## 🧱 Arkkitehtuurin ytimet

| Kerros | Kuvaus |
|--------|--------|
| 🧬 Schema Layer | Lukitut JSON-skeemat (päätös, evidence, audit, foresight) |
| ⚙️ Engine Layer | Päätöksen elinkaarimoottori + normalisoitumisen tunnistin |
| 🧾 Audit Layer | Oikeudellinen audit trail + PKI/QES |
| 📊 Foresight Layer | Ennusteet, mittarit, PDCA-loopit |
| 🌐 API Layer | FastAPI-validointi, OpenAPI, integraatiot |


## 📁 Projektirakenne


house-of-consequences-core/
├── api/                  # FastAPI-palvelu
├── schemas/              # Lukitut JSON Schema -määrittelyt
├── audit/                # Audit-logit ja raporttigeneraattorit
├── crypto/               # PKI, QES, allekirjoitukset
├── governance/           # Päätösten elinkaarimoottori
├── foresight/            # Ennustemallit ja mittarit
├── docs/                 # Juridinen ja tekninen dokumentaatio
└── tests/                # Testaus


## 🔐 Turva ja oikeudellinen pätevyys

Järjestelmä tukee:

- *Qualified Electronic Signatures (QES)*,
- *PKI-allekirjoituksia PDF-raporteissa*,
- *aikaleimattuja, muuttumattomia audit-lokeja*,
- yhteensopivuutta EU:n eIDAS-asetuksen kanssa.


## 🚀 Käyttö (kehittäjä)

```bash
git clone https://github.com/<org>/house-of-consequences-core.git
cd house-of-consequences-core
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn api.main:app --reload


API käynnistyy osoitteessa:


http://127.0.0.1:8000/docs


🌍 Julkinen käyttöliittymä

Tämä core-moottori on suunniteltu integroitavaksi:
	•	valtiollisiin päätöksentekojärjestelmiin,
	•	kansalaisyhteiskunnan seurantatyökaluihin.
        (Kansalaisaloite, avoin data jne.)
    •	yritysten governance-palvelut toimivat
        erillisellä kaupallisella lisenssillä.

Julkinen portaali: https://houseofconsequences.org


🏛️ Institutionaalinen asema

House of Consequences ei ole mielipidejärjestelmä.
Se on rakenteellinen vastuun infrastruktuuri.

Se ei sano mitä pitää päättää —
se näyttää mitä tapahtuu, jos päätös hyväksytään.


🧭 Lisenssi ja omistajuus

Tämän järjestelmän ydinarvo on rakenteellinen riippumattomuus.
Käyttöoikeudet, lisenssit ja institutionaalinen hallintamalli määritellään erillisessä GOVERNANCE_MODEL.md-dokumentissa.



✨ Seuraavat vaiheet
	1.	🔒 JSON Schema -lukitukset
	2.	⚙️ FastAPI-validointipalvelu
	3.	🧾 Audit-log middleware
	4.	📄 PDF-raporttigeneraattori + QES
	5.	📘 OpenAPI-sopimus
	6.	🌐 Domain-portaali (houseofconsequences.org)


House of Consequences ei ole järjestelmä päätöksille.
Se on järjestelmä seurauksille.
