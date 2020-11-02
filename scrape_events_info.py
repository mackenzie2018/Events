import json
import pandas as pd
import re
from datetime import datetime
from bs4 import BeautifulSoup
from dateutil.parser import parse

# Open up the soup tin
def read_soups(filename):
    with open(filename,'r') as file:
        soups = json.load(file)
    return soups

def parser(string):
    try:
        return parse(string)
    except:
        return "n/a"

soups = read_soups(input("What is the file name?"))
print('Opening soup tin...')

# Start an empty df
output = pd.DataFrame()

# Pick out the events info
## AddGod
soup = BeautifulSoup(soups['Addleshaw Goddard'],'html.parser')
AddGod_root = "https://www.addleshawgoddard.com"

event_titles = [
    title.text.strip() 
    for title 
    in soup.find_all("h5",
                     {"class":"search-result-list-item__heading"}
                    )
]

event_dates = [
    date.text.strip() 
    for date 
    in soup.find_all("p",
                     {"class":"search-result-list-item__date"}
                    )
]

event_descriptions = [
    desc.text.strip() 
    for desc 
    in soup.find_all("div",
                     {'class':'search-result-list-item__content'}
                    )
]

event_urls = [
    AddGod_root+url['href'] 
    for url 
    in soup.find_all("a",href=True) 
    if "/events/" in url['href']
]

AddGod = list(zip(event_titles,
                  event_dates,
                  event_descriptions,
                  event_urls))

AddGod_df = pd.DataFrame(AddGod,
                         columns=["Title","Date","Description","URL"])
AddGod_df['Date'] = AddGod_df['Date'].apply(parser)

output = output.append(AddGod_df,sort=True)

del AddGod, AddGod_root, soup, AddGod_df
del event_titles, event_dates, event_descriptions, event_urls

## BCLP
soup = BeautifulSoup(soups['Berwin Leighton Paisner'],'html.parser')
BCLP_root = "https://www.bclplaw.com"

titles = soup.find_all("div",{'class':'search-results__result-title'})  
dates = soup.find_all("div",{'class':'search-results__result-date type-108'})
event_types = soup.find_all("div",{'class':'search-results__result-type'})
event_urls = soup.find_all("a",{'class':'js-search-results__link'},href=True)
clean_titles = [title.text.strip() for title in titles]
clean_dates = [date.text.strip() for date in dates]
clean_event_types = [event_type.text.strip() for event_type in event_types]
clean_event_urls = [BCLP_root + url['href'] for url in event_urls]
BCLP = list(zip(clean_titles,
                clean_dates,
                clean_event_types,
                clean_event_urls))

BCLP_df = pd.DataFrame(BCLP,columns=["Title","Date","Type","URL"])
BCLP_df['Date'] = BCLP_df['Date'].apply(parser)
output = output.append(BCLP_df,sort=True)

del titles, dates, event_types, event_urls
del clean_titles, clean_dates, clean_event_types, clean_event_urls
del soup, BCLP, BCLP_root, BCLP_df

## CMS
soup = BeautifulSoup(soups["CMS CMNO"],'html.parser')
CMS_root = "https://cms.law"

titles = soup.find_all("div",{'class':"search-result__headline"})
days = soup.find_all("div",{'class':"day"})
months = soup.find_all("div",{'class':"month"})
event_descriptions = soup.find_all("div",{'class':"search-result__excerpt"})
event_urls = soup.find_all("a",{'class':'search-result__link'},href=True)

clean_titles = [title.text.strip() for title in titles]
clean_dates = [day.text.strip()+" "+month.text.strip() 
               for day,month 
               in zip(days,months)]
clean_event_descriptions = [desc.text.strip() for desc in event_descriptions]
clean_event_urls = [CMS_root + url['href'] for url in event_urls]

CMS = list(zip(clean_titles,
               clean_dates,
               clean_event_descriptions,
               clean_event_urls))

CMS_df = pd.DataFrame(CMS,columns=["Title","Date","Description","URL"])

CMS_df['Date'] = CMS_df['Date'].apply(parser)

output = output.append(CMS_df,sort=True)

del soup, CMS, CMS_df, CMS_root
del titles,days,months,event_descriptions,event_urls
del clean_titles, clean_dates, clean_event_descriptions, clean_event_urls

## Fenwick Elliot
soup = BeautifulSoup(soups["Fenwick Elliott"],'html.parser')
FE_root = "https://www.fenwickelliott.com"

title_arg = {'class':"field-item even",'property':"dc:title"}
titles = soup.find_all("div",title_arg)

date_arg = {'class':"field field-name-field-event-displayed-date field-type-text field-label-hidden"}
dates = soup.find_all("div",date_arg)

descriptions = [
    desc for desc 
    in soup.find_all("div",
                     {'class':"field-item even",
                      'property':'content:encoded'}
                    )
]

urls = [
    url for url 
    in soup.find_all("a",href=True) 
    if url['href'].startswith("/events/")
]

clean_titles = [title.text.strip() for title in titles]
clean_dates = [date.text.strip() for date in dates]
clean_descriptions = [desc.p.text for desc in descriptions]
clean_event_urls = [FE_root+url['href'] for url in urls]

FE = list(zip(clean_titles,
              clean_dates,
              clean_descriptions[1:],
              clean_event_urls
             ))

FE_df = pd.DataFrame(FE,columns=["Title","Date","Description","URL"])

FE_df['Date'] = FE_df['Date'].apply(lambda x: parser(" ".join(x.split(" ")[:3])))
                                    
output = output.append(FE_df,sort=True)

del soup, FE_root, title_arg, titles
del date_arg, dates, descriptions, urls
del clean_titles, clean_dates, clean_descriptions, clean_event_urls
del FE, FE_df

## Herbert Smith Freehills
soup = BeautifulSoup(soups["Herbert Smith Freehills"],'html.parser')
HSF_root = "https://www.herbertsmithfreehills.com"

event_titles = [
    title.text.strip() 
    for title 
    in soup.find_all("h3")
]

date_arg = {"class":"field field--name-field-tag-line field--type-text field--label-hidden"}
event_dates_descs = [
    desc.text.strip() 
    for desc 
    in soup.find_all("div",date_arg)
] 

event_urls = [
    HSF_root+url['href'] 
    for url 
    in soup.find_all("a",{'class':'hubPage-linkWrapper'},href=True)
]

HSF = list(zip(event_titles,
               event_dates_descs,
               event_urls))

HSF_df = pd.DataFrame(HSF,columns=["Title","Date","URL"])
HSF_df['Date'] = HSF_df['Date'].apply(parser)
output = output.append(HSF_df,sort=True)

del soup, HSF_root
del event_titles, date_arg, event_dates_descs, event_urls
del HSF, HSF_df

## Hogan Lovells
soup = BeautifulSoup(soups["Hogan Lovells"],'html.parser')
HL_root = "https://www.hoganlovells.com"

event_titles = [
    title.text.strip() 
    for title 
    in soup.find_all("h2")
]

event_dates = [
    date.text.strip() 
    for date 
    in soup.find_all("p",{'class':'article-date'})
]

event_descs = [
    desc.findChildren("p")[-2].text.strip()
    for desc 
    in soup.find_all("div",{'class':'article-text'})
]

event_urls = [
    HL_root+url["href"] 
    for url 
    in soup.find_all("a",
                     {'title':re.compile("This link will redirect to")},
                     href=True)
]

HL = list(zip(event_titles,
              event_dates,
              event_descs,
              event_urls))

HL_df = pd.DataFrame(HL,columns=["Title","Date","Description","URL"])
HL_df['Date'] = HL_df['Date'].apply(parser)
output = output.append(HL_df,sort=True)

del soup, HL_root
del event_titles, event_dates, event_descs, event_urls
del HL, HL_df

## LaLive
soup = BeautifulSoup(soups["Lalive"],'html.parser')
Lalive_root = "https://www.lalive.law"

event_titles = [title.text.strip() 
                for title 
                in soup.find_all("h3",{'class':'title9'})]

event_dates = [date.text.strip() 
               for date 
               in soup.find_all("span",{'class':'date'})]

event_venues = [venue.text.strip() 
               for venue 
               in soup.find_all("h2",{'class':'title3 regular'})]

event_descriptions = [desc.text.strip() 
                      for desc 
                      in soup.find_all("span",{'class':'legend'})]

event_speakers = [speaker.text.strip() 
                  for speaker 
                  in soup.find_all("span",{'class':'speaker'})]

Lalive = list(zip(event_titles,
                  event_dates,
                  event_venues,
                  event_descriptions,
                  event_speakers))

Lalive_columns = ["Title","Date","Venue","Description","Speaker"]
Lalive_df = pd.DataFrame(Lalive[:20],columns=Lalive_columns)
Lalive_df['Date'] = Lalive_df['Date'].apply(parser)
output = output.append(Lalive_df,sort=True)

del soup, Lalive_root
del event_titles, event_dates, event_venues, event_descriptions, event_speakers
del Lalive, Lalive_columns, Lalive_df

## Landmark Chambers
soup = BeautifulSoup(soups["Landmark Chambers"],'html.parser')

event_titles = [
    title.text.strip() 
    for title 
    in soup.find_all("h2",{'class':'list__title'})
]

event_dates = [
    date.text.strip() 
    for date 
    in soup.find_all("div",{'class':'columns small-8 medium-3'})
]

event_locations = [
    location.text.strip() 
    for location 
    in soup.find_all("div",{'class':'columns small-8 medium-4'})
]

event_urls = [
    url['href'] 
    for url 
    in soup.find_all("a",{'class':"list__link"},href=True)
]

LC = list(zip(event_titles,
              event_dates,
              event_locations,
              event_urls))

LC_df = pd.DataFrame(LC,columns=["Title","Date","Venue","URL"])
LC_df['Date'] = LC_df['Date'].apply(parser)
output = output.append(LC_df,sort=True)

del soup
del event_titles, event_dates, event_locations, event_urls
del LC, LC_df

## Mayer Brown
### Come back later

## Pinsent Masons
### Tricky one...

## White & Case
soup = BeautifulSoup(soups["White & Case"],'html.parser')
WC_root = "https://www.whitecase.com"

event_titles = [
    h2.text 
    for h2 
    in soup.find_all("h2",{'class':'title'})
]

date_arg = {'class':'field field--name-field-date field--type-datetime field--label-hidden field--item'}
event_dates = [
    date.time['datetime'] 
    for date 
    in soup.find_all("div",date_arg)
]

event_urls = [
    WC_root + a['href'] 
    for a in soup.find_all("a",
                           {'class':'list-item-link'},
                           href=True)
]

event_types = [
    div.text.strip() 
    for div 
    in soup.find_all("div",
                     {'class':'field field--name-field-publication-type'}
                    )
]

WC = list(zip(event_titles,
              event_dates,
              event_urls,
              event_types))

WC_df = pd.DataFrame(WC,columns=["Title","Date","URL","Type"])
WC_df['Date'] = WC_df['Date'].apply(parser)
output = output.append(WC_df,sort=True)

del soup, WC_root
del event_titles, date_arg, event_urls, event_types
del WC, WC_df

## Baker McKenzie
soup = BeautifulSoup(soups["Baker McKenzie"],'html.parser')
root = "https://www.bakermckenzie.com"

event_titles = [
    div.text
    for div 
    in soup.find_all("div",{"class":"content-headline"})
]

event_urls = [
    root+tag['href']
    for tag 
    in soup.find_all("a",{"class":"promo-content-link"},href=True)
]

event_types = [
    "Event" if "events" in url 
    else "Article"
    for url in event_urls
]

BMac = list(zip(event_titles,
                event_urls,
                event_types))

BMac_df = pd.DataFrame(BMac,columns=["Title","URL","Type"])
# BMac_df['Date'] = BMac_df['Date'].apply(parser)
output = output.append(BMac_df,sort=True)

del soup, root
del event_titles, event_urls, event_types 
del BMac, BMac_df

## Clyde & Co
soup = BeautifulSoup(soups["Clyde & Co"],'html.parser')
Clyde_root = "https://www.clydeco.com"

event_titles = [title.text 
                for title 
                in soup.find_all("p",{'class':'archive__entry__title'})]


event_dates = [date['datetime'] 
              for date 
              in soup.find_all("time",{'class':'archive__day__title'})]

event_urls = [Clyde_root+url['href'] 
              for url 
              in soup.find_all("a",{'class':'archive__entry'},href=True)]

Clyde = list(zip(event_titles,
                 event_dates,
                 event_urls))

Clyde_df = pd.DataFrame(Clyde,columns=["Title","Date","URL"])
Clyde_df['Date'] = Clyde_df['Date'].apply(parser)
output = output.append(Clyde_df,sort=True)

del soup, Clyde_root
del event_titles, event_dates, event_urls
del Clyde, Clyde_df

## Jones Day
soup = BeautifulSoup(soups["Jones Day"],'html.parser')
JD_root = "https://www.jonesday.com"

events_section = [
    section 
    for section 
    in soup.find_all("section",{'aria-label':'Events'})
][0]

event_titles = [
    title.text.strip() 
    for title 
    in events_section.find_all("h3",
                               {'class':re.compile("articleblock__row")})
]

event_dates = [
    date.text.strip() 
    for date 
    in events_section.find_all("span",
                               {'class':'articleblock__meta'})
][0::2]

url_arg = {'class':'articleblock__inner articleblock__inner--img'}
event_urls = [
    JD_root+url['href'] 
    for url 
    in events_section.find_all("a",url_arg,href=True)
]

JonesDay = list(zip(event_titles,event_dates,event_urls))
JonesDay_df = pd.DataFrame(JonesDay,columns=["Title","Date","URL"])
JonesDay_df['Date'] = JonesDay_df['Date'].apply(parser)
output = output.append(JonesDay_df,sort=True)

del soup, JD_root
del events_section
del event_titles, event_dates, url_arg, event_urls
del JonesDay, JonesDay_df

## Mayer Brown

soup = BeautifulSoup(soups["Mayer Brown"],'html.parser')
MB_root = "https://www.mayerbrown.com"

event_titles = [
    title.text.strip() 
    for title 
    in soup.find_all("span",{'class':'link link__underlined'})
]

event_months = [
    month.text.strip() 
    for month 
    in soup.find_all("div",{'class':'newsblock__label newsblock__month'})
]

event_years = [
    year.text.strip() 
    for year 
    in soup.find_all("div",{'class':'newsblock__label newsblock__year'})
]

event_urls = [
    MB_root+url.a['href']
    for url 
    in soup.find_all("div",{'class':'newsblock__col newsblock__col--wide'})
]

event_dates = [
    y+' '+x for x,y in zip(event_years,event_months)
]

MB = list(zip(event_titles,
              event_dates,
              event_urls))

MB_df = pd.DataFrame(MB,columns=["Title","Date","URL"])
MB_df['Date'] = MB_df['Date'].apply(parser)
output = output.append(MB_df,sort=True)

del soup, MB_root
del event_titles, event_months, event_years, event_urls, event_dates
del MB, MB_df

## McGuire Woods
soup = BeautifulSoup(soups["McGuireWoods"],'html.parser')
root = "https://www.mcguirewoods.com"

event_divs = [
    div 
    for div 
    in soup.find_all("div",
                     {"class":"col-md-6 col-xl-3 tile pageResource"})
]

event_titles = [
    div.findChildren("p")[0].text.strip()
    for div 
    in event_divs[-7:]
]

event_dates = [
    div.findChildren("p")[1].text.strip()
    for div 
    in event_divs[-7:]
]

event_urls = [
    root + div.a['href'] 
    for div 
    in event_divs[-7:]
]

# event_descriptions = [
#     div.findChildren("p")[2].text.strip()
#     for div 
#     in event_divs[-7:]
# ]

McGuireWoods = list(zip(event_titles,
                        event_dates,
                        event_urls))

McGuireWoods_df = pd.DataFrame(
    McGuireWoods,
    columns=['Title','Date','URL']
)

McGuireWoods_df['Date'] = McGuireWoods_df['Date'].apply(parser)
output = output.append(McGuireWoods_df,sort=True)

del soup, root
del event_divs, event_titles, event_dates, event_urls
del McGuireWoods, McGuireWoods_df

## Mishcon de Reya

soup = BeautifulSoup(soups['Mishcon de Reya'],'html.parser')
target_class = ("ajax-listing-item post post--event card col-12 " +  
                "col-xs-6 col-sm-6 col-md-4 col-lg-3 ajax-equalize-item")
root = "https://www.mishcon.com"

event_divs = [
    div 
    for div 
    in soup.find_all("div",{"class":target_class})
]

event_titles = [
    div.findChild("div",{"class":"post__body card-body"}).a.text
    for div
    in event_divs
]

event_dates = [
    div.findChild("time",{"class":"post__date"})['datetime']
    for div 
    in event_divs
]

event_urls = [
    root + div.findChild("a",{"class":"post__image-link"},href=True)['href']
    for div 
    in event_divs 
]

Mishcon = list(zip(event_titles,
                   event_dates,
                   event_urls))

Mishcon_df = pd.DataFrame(Mishcon,columns=['Title','Date','URL'])
Mishcon_df['Date'] = Mishcon_df['Date'].apply(parser)
output = output.append(Mishcon_df,sort=True)

del soup, target_class, root
del event_divs, event_titles, event_dates, event_urls
del Mishcon, Mishcon_df

## SCL

soup = BeautifulSoup(soups["SCL"],'html.parser')

SCL_root = "https://www.scl.org.uk"

event_titles = [
    div.span.text 
    for div
    in soup.find_all("div",
                     {'class':'views-field views-field-title'}
                    )
]

event_dates = [
    span['content'] 
    for span 
    in soup.find_all("span",
                     {"class":"date-display-single"}
                    )
]

event_urls = [
    SCL_root + div.span.a['href']
    for div 
    in soup.find_all("div",
                     {"class":"views-field views-field-title"}
                    )
]

event_organisers = [
    organisers.text.replace("Organiser(s):  ","").strip()
    for organisers
    in soup.find_all("div",
                     {"class":"views-field views-field-php"}
                    ) 
]

SCL = list(zip(event_titles,
               event_dates[::2],
               event_urls,
               event_organisers))

SCL_df = pd.DataFrame(SCL,columns=['Title','Date','URL','Organisers'])
SCL_df['Date'] = SCL_df['Date'].apply(parser)
output = output.append(SCL_df,sort=True)

del soup, SCL_root, event_titles, event_dates, event_urls
del event_organisers, SCL, SCL_df

# Spit out events info as an Excel table
output['Date'] = output['Date'].astype(str)
output['Date'] = output['Date'].apply(lambda x: x.split("+")[0] if "+" in x else x)
date_stamp = datetime.now().strftime("%Y%m%d_%H%M")
output.to_excel(f"{date_stamp} events data.xlsx")