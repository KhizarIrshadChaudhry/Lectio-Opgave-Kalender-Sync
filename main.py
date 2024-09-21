import os
import json
import datetime
import warnings
#google api osv osv
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
#selenium ting ting osv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

warnings.filterwarnings("ignore")
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'



options = webdriver.ChromeOptions()
#options.add_experimental_option('detach', True) 
options.add_argument('--log-level=3') #reducere unødvendig logs
options.add_experimental_option('excludeSwitches', ['enable-logging'])
service = Service()
service.log_path = os.devnull

options.add_argument("--disable-search-engine-choice-screen")
options.add_argument("headless")
driver = webdriver.Chrome(options=options)

SCOPES = ['https://www.googleapis.com/auth/calendar']
CREDENTIALS_FILE = 'client_secret.json'

def hentOpgaver(brugernavn, kode, skoleID):
    opgaver = []

    driver.get("https://www.lectio.dk/lectio/{}/OpgaverElev.aspx".format(skoleID))

    #LOGIN PÅ LECTIO
    Brugernavn = driver.find_element(By.ID, "username")
    Brugernavn.send_keys(brugernavn)
    Kode = driver.find_element(By.ID, "password")
    Kode.send_keys(kode)
    Kode.send_keys(Keys.ENTER)
    print("login successfuldt")
    #AFHENTE DATA
    Table = driver.find_element(By.XPATH, '//tbody')
    Rows = Table.find_elements(By.TAG_NAME, 'tr')
    #print(Rows)
    print("Gemmer opgaverne...")
    #OMDANNE DATA SOM .JSON FIL
    for row in Rows:
        Cells = row.find_elements(By.TAG_NAME, 'td')
        #ta alt data og gem i py dictionary her
        if len(Cells) > 0 and Cells[5].text.strip()=="Venter" and Cells[0].text.strip()!="Uge":  #tilføj "and Cells[4].text.strip()!="0.00"" hvis ik du vil ha opgaver med elevtimer med
            assignment = {
                "uge": Cells[0].text.strip(),
                "hold": Cells[1].text.strip(),
                "title": Cells[2].text.strip(),
                "frist": Cells[3].text.strip(),
                "elev_tid": Cells[4].text.strip(),
                "status": Cells[5].text.strip(),
                "fravær": Cells[6].text.strip(),
                "afventer": Cells[7].text.strip(),
                "lærer_note": Cells[8].text.strip(),
                "karakter": Cells[9].text.strip(),
                "elev_note": Cells[10].text.strip(),
            }
            opgaver.append(assignment)
            print(f"{Cells[2].text.strip()} gemt i DB successfuldt")
    opgaver_json = json.dumps(opgaver, indent=4, ensure_ascii=False)
    #print(assignments_json)
    #GEM .JSON FILEN
    with open('assignments.json', 'w', encoding='utf-8') as f:
        f.write(opgaver_json)
    print("Alle opgaver gemt!")
    return opgaver



# Setup af google api
def hentCalenderService():
    creds = None
    #token.json findes??
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # Hvis ingen token ik findes så sppærge om godkendelse
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # gem token til brug igen
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Opret Google Calendar API service
    service = build('calendar', 'v3', credentials=creds)
    print("Google logined succesfuldt")
    return service


def lavCalenderEvent(service, opgave):
    # Konverter afleveringsdato til ISO 8601
    frist_dato = opgave['frist'] 
    dato_object = datetime.datetime.strptime(frist_dato, "%d/%m-%Y %H:%M")
    iso_frist_dato = datetime.datetime.strptime(frist_dato, "%d/%m-%Y %H:%M").isoformat()
    
    event = {
        'summary': f"Aflevering: {opgave['title']} ({opgave['hold']})",
        'description': f"{opgave['elev_tid']} timers elevtid. \nOpgave Beskrivelse:\n{opgave['lærer_note']}",
        'start': {
            'dateTime': iso_frist_dato,
            'timeZone': 'Europe/Copenhagen',
        },
        'end': {
            # varieghed er gjort til 1 time rn
            'dateTime': (dato_object + datetime.timedelta(hours=1)).isoformat(),
            'timeZone': 'Europe/Copenhagen',
        },
    }

    event_resultat = service.events().insert(calendarId='primary', body=event).execute()
    print(f"Event lavet: {event_resultat['summary']}")


def sletOpgaveEvents(service):
    # Søg efter "Aflevering" i titlen
    events_result = service.events().list(calendarId='primary', q="Aflevering").execute()
    events = events_result.get('items', [])

    if not events:
        print("Ingen opgave events fundet.")
        return

    # check alle events og slet
    for event in events:
        print(f"Sletter event: {event['summary']}")
        service.events().delete(calendarId='primary', eventId=event['id']).execute()

    print("Alle opgave events er slettet.")

def start_text():
    intro = """
    ***************************************************
    *                                                 *
    *          Lectio Opgave-Kalender Sync            *
    *                                                 *
    *    Dette program hjælper dig med at hente dine  *
    *    opgaver fra Lectio og synkronisere dem med   *
    *    din Google Kalender.                         *
    *                                                 *
    *                  Lavet af:                      *
    *         Khizar Irshad Chaudhry                  *
    *                                                 *
    ***************************************************
    \n\n\n
    """
    print(intro)


def main():
    #ta' lectio creds
    #skift dette til brugernavn og pass hhv til ="brugernavn" ="pass" hvis du ikke vil gi brugernavn hele tiden
    start_text()
    brugernavn = input("Lectio Brugernavn: ") 
    kode = input("Lectio Kodeord: ") 
    bekræft = input("Tryk Enter for at fortsætte eller CTRL+C for at annullere...") #fjern denne linje hvis du sætter lectio creds som en variable istedet for input

    skoleID = "518" #STG's skole ID er 518

    opgaver = hentOpgaver(brugernavn, kode, skoleID)

    service = hentCalenderService()

    sletOpgaveEvents(service)
    for opgave in opgaver:
        lavCalenderEvent(service, opgave)
    print("Alle opgaver gemt i kalenderen.")

if __name__ == '__main__':
    print("Program startet")
    main()