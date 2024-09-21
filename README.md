# Lectio Opgave-Kalender Sync

Dette program hjælper dig med at synkronisere dine opgaver fra Lectio til din Google Kalender. Det henter opgaveinformationer fra Lectio og opretter events i din Google Kalender baseret på afleveringsfristerne. På denne måde har du altid styr på dine deadlines!

## Funktioner

- Hent opgaver fra Lectio.
- Opret events i Google Kalender med afleveringsfrister.
- Slet automatisk tidligere opgave-events i kalenderen, så kun de nyeste er til stede.
  
## Krav

Før du kan bruge programmet, skal du sikre dig, at du har følgende:

1. **Python** installeret (version 3.8 eller nyere).
2. **Google Calendar API** opsat med et `client_secret.json`-fil (se instruktionerne nedenfor).
3. **Selenium WebDriver** og Chrome installeret for at logge ind på Lectio.

## Installation

### 1. Klon repository og installer afhængigheder
Klon dette repository til din lokale maskine og installer afhængighederne:

```bash
git clone https://github.com/din-bruger/lectio-opgave-sync.git
cd lectio-opgave-sync
pip install -r requirements.txt
```

### 2. Opsætning af Google Calendar API

For at kunne oprette og slette events i din Google Kalender skal du opsætte **Google Calendar API** og downloade din egen `client_secret.json`-fil.

Følg disse trin:

1. Gå til [Google Cloud Console](https://console.cloud.google.com/).
2. Opret et nyt projekt.
3. Naviger til **APIs & Services > Credentials**.
4. Klik på **Create Credentials** og vælg **OAuth 2.0 Client IDs**.
5. Vælg applikationstypen som **Desktop App**.
6. Download den genererede `client_secret.json`-fil.
7. Flyt denne fil til programmets rodmappe, dvs. samme mappe som `main.py`.

For mere detaljeret vejledning, kan du følge denne guide fra Google: [Guide til opsætning af Google Calendar API](https://developers.google.com/calendar/quickstart/python).

### 3. Konfigurer Selenium WebDriver

Selenium bruges til at logge ind på Lectio og hente opgaver. Du skal have **Chrome** installeret samt **ChromeDriver**, der matcher din Chrome-version.

1. Download **ChromeDriver** her: [ChromeDriver Download](https://chromedriver.chromium.org/downloads).
2. Sørg for, at `chromedriver.exe` er placeret et sted i dit system-`PATH`, eller tilføj stien til programmet i koden, hvis det er nødvendigt.

## Brug af programmet

Når alt er sat op, kan du køre programmet fra terminalen:

```bash
python main.py
```

Følg instruktionerne i terminalen:

1. Indtast dit **Lectio brugernavn** og **kodeord**.
2. Programmet henter opgaverne fra Lectio.
3. Opgaverne bliver automatisk oprettet som events i din Google Kalender.
4. Eventuelle tidligere opgave-events vil blive slettet for at undgå duplikater.

## Token-fil

Efter første godkendelse vil der blive gemt en `token.json`-fil. Denne fil bruges til at gemme dine Google-kalenderoplysninger, så du ikke behøver at godkende adgang hver gang du kører programmet. Hvis du ønsker at logge ind med en anden Google-konto, kan du slette `token.json`.

## Fejlfinding

Hvis du støder på problemer, kan du tjekke følgende:

- Sørg for, at din `client_secret.json` er korrekt placeret og gyldig.
- Sørg for, at **Selenium WebDriver** er opdateret og korrekt installeret.
- Hvis du får en timeout-fejl, kan du prøve at øge Selenium WebDriver's timeout i koden.

## Udviklet af

**Khizar Irshad Chaudhry**
Skriv gerne, hvis der opstår problemer.
---
