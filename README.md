# Lectio Opgave Kalender Synnc

## Introduktion

Dette program scraper opgaver fra Lectio og tilføjer dem automatisk som events i din Google Kalender. Programmet logger ind på Lectio, henter opgaverne, og konverterer dem til kalenderbegivenheder ved hjælp af Google Calendar API.

---

## Funktioner

- Automatisk login på Lectio og scraping af opgaver.
- Omdanner opgaver til kalenderbegivenheder med afleveringsdatoer.
- Sletter gamle opgave-events fra Google Kalender.
- Understøtter Lectio-elever på alle skoler ved blot at ændre skoleID.

---

## Opsætning

Følg nedenstående trin for at konfigurere programmet og få det til at køre:

### 1. Klon repository'et

```bash
git clone https://github.com/KhizarIrshadChaudhry/Lectio-Opgave-Kalender-Sync.git
cd Lectio-Opgave-Kalender-Sync
```
### 2. Installer nødvendige Python-pakker

Sørg for, at du har Python installeret. Installer derefter de nødvendige pakker ved at køre:

```bash
pip install -r requirements.txt
```

### 3. Opret et Google Calendar API-projekt

For at programmet kan oprette events i din Google Kalender, skal du opsætte Google Calendar API:

1. Gå til Google Developers Console: [Google Developer Console](https://console.developers.google.com/).
2. Opret et nyt projekt.
3. Aktivér "Google Calendar API" for dit projekt.
4. Opret et OAuth 2.0-klient-id under "Credentials".
5. Download `client_secret.json` og placer det i samme mappe som dit program.
6. Sørg for at ændre stien til filen i koden, hvis det er nødvendigt.

**Flere detaljer om opsætning af Google Calendar API:**  
[Google Calendar API - Python Quickstart](https://developers.google.com/calendar/quickstart/python)

### 4. Skift skoleID til dit eget

For at få adgang til opgaverne fra din egen skole, skal du skifte `skoleID` i koden. Som standard er skoleID sat til **NEXT Sukkertoppen HTX** (skoleID = "518"). Du kan finde skoleID for din skole ved at gå til din Lectio-startside og se på URL'en, der ser sådan her ud:

```
https://www.lectio.dk/lectio/{SKOLE_ID}/forside.aspx
```

Her skal du erstatte `{SKOLE_ID}` med tallet i URL'en for din skole.

I koden skal du ændre linjen (linje 175):
```python
skoleID = "518"  # Ændre til dit eget skoleID
```

### 5. Kør programmet

For at køre programmet, skal du blot starte det i terminalen:

```bash
python main.py
```

Programmet vil bede om dit Lectio-brugernavn og adgangskode og tilføje dine opgaver til Google Kalender.

---

## Kontakt

Programmet er udviklet af **Khizar Irshad Chaudhry**.  
Hvis du har spørgsmål eller forslag, er du velkommen til at kontakte mig.

---

Med denne README-fil er det nu klart, hvordan man sætter både Google API’et og skoleID korrekt op for at bruge programmet med deres egen skole.
