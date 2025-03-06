# %%
import streamlit as st
import pandas as pd 
import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt 

# %%
import requests
import streamlit as st

API_KEY = "703e38c5af704ea2b71e33878e34d5c4"
url = 'https://api.football-data.org/v4/competitions/PL/teams'
headers = {
   'X-Auth-Token': API_KEY
}

@st.cache_data
def fetch_teams():
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        for team in data['teams']:
            print(team['name'])
    else:
        print(f'Fout: {response.status_code}, {response.text}')

fetch_teams()


# %% [markdown]
# Laten we de data opschonen door:
# 
# 1. Missende waarden (NaN) te verwijderen
# 
# 2. Duplicaten te controleren en te verwijderen
# 
# 3. Overbodige informatie te filteren

# %% [markdown]
# Wat dit script doet:
# 
# 1. Haalt teamgegevens op
# 
# 2. Slaat alleen relevante velden op
# 
# 3. Verwijdert missende waarden
# 
# 4. Verwijdert duplicaten
# 
# 5. Geeft een overzicht van de opgeschoonde dataset

# %%
import requests
import pandas as pd
import streamlit as st

# API-instellingen
API_KEY = "703e38c5af704ea2b71e33878e34d5c4"
url = "https://api.football-data.org/v4/competitions/PL/teams"

headers = {
    "X-Auth-Token": API_KEY
}

@st.cache_data
def fetch_teams_data():
    # Data ophalen
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()

        # Lijst maken van relevante gegevens
        teams_data = []
        for team in data.get('teams', []):  # Veilig ophalen van teams-lijst
            teams_data.append({
                "id": team.get("id"),
                "name": team.get("name"),
                "shortName": team.get("shortName"),
                "tla": team.get("tla"),
                "founded": team.get("founded"),
                "venue": team.get("venue"),
            })

        # Data omzetten naar DataFrame
        df = pd.DataFrame(teams_data)

        # Stap 1: Missende waarden verwijderen
        df.dropna(inplace=True)

        # Stap 2: Duplicaten verwijderen
        df.drop_duplicates(inplace=True)

        # Stap 3: Resultaten bekijken
        print(df.head())

    else:
        print(f'Fout: {response.status_code}, {response.text}')

fetch_teams_data()


# %% [markdown]
# Punten per maand te berekenen

# %% [markdown]
# Wat dit script doet 🚀
# ✅ Wedstrijddata ophalen via de API
# ✅ Datum omzetten naar een maandformaat (YYYY-MM)
# ✅ Punten berekenen per wedstrijd:
# 
# Winst → 3 punten
# Gelijkspel → 1 punt
# Verlies → 0 punten
# ✅ Punten per maand per team optellen
# ✅ Netjes weergeven in een DataFrame

# %%
import requests
import pandas as pd
import streamlit as st

# API-instellingen
API_KEY = "703e38c5af704ea2b71e33878e34d5c4"
url = "https://api.football-data.org/v4/competitions/PL/matches"

headers = {
    "X-Auth-Token": API_KEY
}

# Functie om data op te halen, met cache
@st.cache_data
def fetch_data(url, headers):
    response = requests.get(url, headers=headers)
    return response

# Data ophalen via de gecachete functie
response = fetch_data(url, headers)

if response.status_code == 200:
    data = response.json()

    # Lijst maken van relevante wedstrijdgegevens
    matches_data = []
    for match in data.get('matches', []):  
        if match.get("status") == "FINISHED":  # Alleen gespeelde wedstrijden
            matches_data.append({
                "date": match.get("utcDate"),
                "home_team": match["homeTeam"]["name"],
                "away_team": match["awayTeam"]["name"],
                "home_score": match["score"]["fullTime"]["home"],
                "away_score": match["score"]["fullTime"]["away"]
            })

    # Data omzetten naar DataFrame
    df = pd.DataFrame(matches_data)

    # Stap 1: Datum omzetten naar datetime en maand toevoegen
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.to_period("M")  # Maand als YYYY-MM

    # Stap 2: Punten berekenen per wedstrijd
    def calculate_points(row):
        if row["home_score"] > row["away_score"]:
            return (row["home_team"], 3), (row["away_team"], 0)
        elif row["home_score"] < row["away_score"]:
            return (row["home_team"], 0), (row["away_team"], 3)
        else:
            return (row["home_team"], 1), (row["away_team"], 1)

    points = []
    for _, row in df.iterrows():
        home_points, away_points = calculate_points(row)
        points.append({"team": home_points[0], "points": home_points[1], "month": row["month"]})
        points.append({"team": away_points[0], "points": away_points[1], "month": row["month"]})

    # Stap 3: DataFrame maken en per team per maand optellen
    points_df = pd.DataFrame(points)
    points_per_month = points_df.groupby(["team", "month"])["points"].sum().reset_index()

    # Stap 4: Resultaat tonen
    print(points_per_month)

else:
    print(f'Fout: {response.status_code}, {response.text}')


# %% [markdown]
# stand per team per maand toont

# %% [markdown]
# Wat dit script doet:
# 
# 1. Wedstrijddata ophalen van de Premier League.
# 
# 2. Punten per wedstrijd berekenen (3 voor winst, 1 voor gelijkspel, 0 voor verlies).
# 
# 3. Punten per maand groeperen voor elk team.
# 
# 4. Totale punten per team berekenen door alle maanden op te tellen.
# 
# 5. Ranglijst opstellen door de teams te sorteren op het totaal aantal punten.
# 
# 6. Resultaat tonen als de uiteindelijke stand van de Premier League

# %%
import requests
import pandas as pd
import streamlit as st

# API-instellingen
API_KEY = "703e38c5af704ea2b71e33878e34d5c4"
url = "https://api.football-data.org/v4/competitions/PL/matches"

headers = {
    "X-Auth-Token": API_KEY
}

# Functie om data op te halen, met cache
@st.cache_data
def fetch_data(url, headers):
    response = requests.get(url, headers=headers)
    return response

# Data ophalen via de gecachete functie
response = fetch_data(url, headers)

if response.status_code == 200:
    data = response.json()

    # Lijst maken van relevante wedstrijdgegevens
    matches_data = []
    for match in data.get('matches', []):  
        if match.get("status") == "FINISHED":  # Alleen gespeelde wedstrijden
            matches_data.append({
                "date": match.get("utcDate"),
                "home_team": match["homeTeam"]["name"],
                "away_team": match["awayTeam"]["name"],
                "home_score": match["score"]["fullTime"]["home"],
                "away_score": match["score"]["fullTime"]["away"]
            })

    # Data omzetten naar DataFrame
    df = pd.DataFrame(matches_data)

    # Stap 1: Datum omzetten naar datetime en maand toevoegen
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.to_period("M")  # Maand als YYYY-MM

    # Stap 2: Punten berekenen per wedstrijd
    def calculate_points(row):
        if row["home_score"] > row["away_score"]:
            return (row["home_team"], 3), (row["away_team"], 0)
        elif row["home_score"] < row["away_score"]:
            return (row["home_team"], 0), (row["away_team"], 3)
        else:
            return (row["home_team"], 1), (row["away_team"], 1)

    points = []
    for _, row in df.iterrows():
        home_points, away_points = calculate_points(row)
        points.append({"team": home_points[0], "points": home_points[1], "month": row["month"]})
        points.append({"team": away_points[0], "points": away_points[1], "month": row["month"]})

    # Stap 3: DataFrame maken en per team per maand optellen
    points_df = pd.DataFrame(points)
    points_per_month = points_df.groupby(["team", "month"])["points"].sum().reset_index()

    # Stap 4: Totale punten per team berekenen
    total_points = points_per_month.groupby("team")["points"].sum().reset_index()

    # Stap 5: Ranglijst maken op basis van punten
    total_points = total_points.sort_values(by="points", ascending=False).reset_index(drop=True)

    # Stap 6: Resultaat tonen
    print("Premier League Stand:")
    print(total_points)

else:
    print(f'Fout: {response.status_code}, {response.text}')



# %%
import requests
import pandas as pd
from datetime import datetime
import streamlit as st

# Maak een GET-aanroep naar de API
url = "https://api.football-data.org/v4/competitions/PL/matches"
headers = {"X-Auth-Token": "703e38c5af704ea2b71e33878e34d5c4"}  # Vervang door je eigen API-sleutel

# Functie om data op te halen met cache
@st.cache_data
def fetch_data(url, headers):
    response = requests.get(url, headers=headers)
    return response

# Data ophalen via de gecachete functie
response = fetch_data(url, headers)

# Controleer of de aanvraag succesvol was
if response.status_code == 200:
    data = response.json()
else:
    print("Er is iets mis gegaan met het ophalen van de data.")
    exit()

# Verkrijg alle wedstrijden
matches = data['matches']

# Filter wedstrijden per maand (augustus 2024 t/m februari 2025)
filtered_matches = {
    "Augustus": [],
    "September": [],
    "Oktober": [],
    "November": [],
    "December": [],
    "Januari": [],
    "Februari": []
}

for match in matches:
    match_date = datetime.strptime(match['utcDate'], '%Y-%m-%dT%H:%M:%SZ')
    if match_date.year == 2024:
        if match_date.month == 8:
            filtered_matches["Augustus"].append(match)
        elif match_date.month == 9:
            filtered_matches["September"].append(match)
        elif match_date.month == 10:
            filtered_matches["Oktober"].append(match)
        elif match_date.month == 11:
            filtered_matches["November"].append(match)
        elif match_date.month == 12:
            filtered_matches["December"].append(match)
    elif match_date.year == 2025:
        if match_date.month == 1:
            filtered_matches["Januari"].append(match)
        elif match_date.month == 2:
            filtered_matches["Februari"].append(match)

# Lijst van Premier League-teams
teams = [
    "Arsenal FC", "Chelsea FC", "Liverpool FC", "Tottenham Hotspur FC", "Manchester City FC", 
    "Manchester United FC", "Leicester City FC", "Everton FC", "West Ham United FC", 
    "Aston Villa FC", "Newcastle United FC", "Brighton & Hove Albion FC", "Brentford FC", 
    "Crystal Palace FC", "Wolverhampton Wanderers FC", "Southampton FC", "AFC Bournemouth", 
    "Nottingham Forest FC", "Fulham FC", "Ipswich Town FC"
]

# Maak een dictionary om de punten bij te houden per maand
team_stats = {team: {"Augustus": 0, "September": 0, "Oktober": 0, "November": 0, "December": 0, "Januari": 0, "Februari": 0, "Totaal": 0} for team in teams}

# Functie om punten toe te voegen aan de statistieken
def update_points(matches, maand):
    for match in matches:
        home_team = match['homeTeam']['name']
        away_team = match['awayTeam']['name']
        home_score = match['score']['fullTime']['home']
        away_score = match['score']['fullTime']['away']

        # Controleer of de score beschikbaar is
        if home_score is not None and away_score is not None:
            if home_score > away_score:
                team_stats[home_team][maand] += 3
            elif away_score > home_score:
                team_stats[away_team][maand] += 3
            else:
                team_stats[home_team][maand] += 1
                team_stats[away_team][maand] += 1

# Update de statistieken voor elke maand
for maand, matches in filtered_matches.items():
    update_points(matches, maand)

# Bereken het totaal aantal punten per team
for team in teams:
    team_stats[team]["Totaal"] = sum(team_stats[team][maand] for maand in filtered_matches.keys())

# Zet de data om in een DataFrame
stand_data = []
for team, stats in team_stats.items():
    stand_data.append({
        "Team": team,
        "Augustus": stats["Augustus"],
        "September": stats["September"],
        "Oktober": stats["Oktober"],
        "November": stats["November"],
        "December": stats["December"],
        "Januari": stats["Januari"],
        "Februari": stats["Februari"],
        "Totaal": stats["Totaal"]
    })

stand_df = pd.DataFrame(stand_data)

# Sorteer de stand op basis van het totaal aantal punten
stand_df = stand_df.sort_values(by="Totaal", ascending=False).reset_index(drop=True)

# Bekijk de huidige stand
print(stand_df)

# Opslaan van de stand in een CSV-bestand
stand_df.to_csv("premier_league_stand_aug-feb_2024_2025.csv", index=False)


# %%
import requests
import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime

# API-instellingen
API_KEY = "703e38c5af704ea2b71e33878e34d5c4"
url = "https://api.football-data.org/v4/competitions/PL/matches"
headers = {"X-Auth-Token": API_KEY}

# Haal de data op via de API
@st.cache_data
def fetch_data():
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Er is iets mis gegaan met het ophalen van de data.")
        return None

data = fetch_data()

# Verkrijg de lijst van wedstrijden
matches = data['matches'] if data else []

# Verkrijg de teams uit de competitie en verwijder " FC"
teams = set()
for match in matches:
    teams.add(match['homeTeam']['name'].replace(" FC", ""))
    teams.add(match['awayTeam']['name'].replace(" FC", ""))

# Filter de wedstrijden per maand
filtered_matches = {maand: [] for maand in ["Augustus", "September", "Oktober", "November", "December", "Januari", "Februari"]}

# Voeg de wedstrijden toe aan de juiste maand
for match in matches:
    match_date = datetime.strptime(match['utcDate'], '%Y-%m-%dT%H:%M:%SZ')
    maand_namen = ["Augustus", "September", "Oktober", "November", "December", "Januari", "Februari"]
    if 8 <= match_date.month <= 12 and match_date.year == 2024:
        filtered_matches[maand_namen[match_date.month - 8]].append(match)
    elif 1 <= match_date.month <= 2 and match_date.year == 2025:
        filtered_matches[maand_namen[match_date.month + 4]].append(match)

# Initieer team-statistieken
team_stats = {team: {maand: 0 for maand in filtered_matches.keys()} for team in teams}
for team in teams:
    team_stats[team]["Totaal"] = 0

# Functie om punten toe te voegen aan de statistieken
def update_points(matches, maand):
    for match in matches:
        home_team = match['homeTeam']['name'].replace(" FC", "")
        away_team = match['awayTeam']['name'].replace(" FC", "")
        home_score = match['score']['fullTime']['home']
        away_score = match['score']['fullTime']['away']
        if home_score is not None and away_score is not None:
            if home_score > away_score:
                team_stats[home_team][maand] += 3
            elif away_score > home_score:
                team_stats[away_team][maand] += 3
            else:
                team_stats[home_team][maand] += 1
                team_stats[away_team][maand] += 1

# Filteren op basis van het geselecteerde type wedstrijd (Thuis, Uit of Alle)
def filter_matches_by_type(matches, match_type, selected_team):
    if match_type == "Alle wedstrijden":
        return matches  # Geen filter, alle wedstrijden
    elif match_type == "Thuiswedstrijden":
        return [match for match in matches if match['homeTeam']['name'].replace(" FC", "") == selected_team]
    elif match_type == "Uitwedstrijden":
        return [match for match in matches if match['awayTeam']['name'].replace(" FC", "") == selected_team]
    return matches

# Streamlit Widgets in een kolomlay-out
st.title("Premier League Statistieken 2024 - 2025")

# Maak gebruik van de sidebar voor de dropdowns, checkboxen en match-type keuzelijst
with st.sidebar:
    # Dropdowns en Checkboxen in de zijbalk
    selected_month = st.selectbox("Kies een maand", ["All"] + list(filtered_matches.keys()))
    selected_team = st.selectbox("Kies een team", ["Alle teams"] + list(teams))
    match_type = st.selectbox("Kies type wedstrijd", ["Alle wedstrijden", "Thuiswedstrijden", "Uitwedstrijden"])
    
    # Checkboxen
    show_lowest_5 = st.checkbox("Toon top 5 teams met de minste punten")
    show_highest_5 = st.checkbox("Toon top 5 teams met de meeste punten")
    
# Slider boven de barplot
points_filter = st.slider("Minimum aantal punten", 0, 67, 0)

# Filter de wedstrijden op basis van het geselecteerde type wedstrijd
filtered_matches_for_team = filter_matches_by_type(matches, match_type, selected_team)

# Filter de wedstrijden per maand voor het geselecteerde type
filtered_matches_by_month = {maand: [] for maand in filtered_matches.keys()}

# Voeg de gefilterde wedstrijden toe aan de juiste maand
for match in filtered_matches_for_team:
    match_date = datetime.strptime(match['utcDate'], '%Y-%m-%dT%H:%M:%SZ')
    maand_namen = ["Augustus", "September", "Oktober", "November", "December", "Januari", "Februari"]
    if 8 <= match_date.month <= 12 and match_date.year == 2024:
        filtered_matches_by_month[maand_namen[match_date.month - 8]].append(match)
    elif 1 <= match_date.month <= 2 and match_date.year == 2025:
        filtered_matches_by_month[maand_namen[match_date.month + 4]].append(match)

# Reset team_stats om opnieuw te berekenen op basis van de gefilterde wedstrijden
team_stats = {team: {maand: 0 for maand in filtered_matches.keys()} for team in teams}
for team in teams:
    team_stats[team]["Totaal"] = 0

# Update de statistieken voor elke maand op basis van de gefilterde wedstrijden
for maand, matches in filtered_matches_by_month.items():
    update_points(matches, maand)

# Bereken het totaal aantal punten per team
for team in teams:
    team_stats[team]["Totaal"] = sum(team_stats[team][maand] for maand in filtered_matches.keys())

# Zet de data om in een DataFrame
stand_df = pd.DataFrame.from_dict(team_stats, orient="index").reset_index().rename(columns={"index": "Team"})

# Filteren op maand
filtered_df = stand_df.copy()

# Als een maand is geselecteerd, filteren we de DataFrame op de geselecteerde maand
if selected_month != "All":
    filtered_df = filtered_df[filtered_df[selected_month] > 0]  # Alleen teams met punten in de geselecteerde maand

# Filteren op team
if selected_team != "Alle teams":
    filtered_df = filtered_df[filtered_df["Team"] == selected_team]

# Filteren op punten
filtered_df = filtered_df[filtered_df[selected_month if selected_month != "All" else "Totaal"] >= points_filter]

# Sorteren voor de checkboxes
if show_lowest_5:
    filtered_df = filtered_df.nsmallest(5, selected_month if selected_month != "All" else "Totaal")
elif show_highest_5:
    filtered_df = filtered_df.nlargest(5, selected_month if selected_month != "All" else "Totaal")

# Als er geen teams zijn na de filter, toon dan een bericht en laat de grafiek niet zien
if filtered_df.empty:
    st.write("Er zijn geen teams die voldoen aan de geselecteerde criteria.")
else:
    # Visualisatie maken
    fig = px.bar(filtered_df, x="Team", y=selected_month if selected_month != "All" else "Totaal", 
                 title=f"Premier League Stand: {selected_month} (Totaal)", 
                 labels={selected_month if selected_month != "All" else "Totaal": "Punten", "Team": "Team"}, 
                 color="Team", color_discrete_map={team: px.colors.qualitative.Set1[i % len(px.colors.qualitative.Set1)] for i, team in enumerate(filtered_df["Team"].unique())})

    # Dynamische layout aanpassen
    max_y_value = filtered_df[selected_month if selected_month != "All" else "Totaal"].max()
    fig.update_layout(
        yaxis=dict(range=[0, max_y_value + 5]),
        width=1000,
        height=600,
        bargap=0.5,
        margin=dict(l=50, r=50, t=50, b=50)
    )

    # Legenda toevoegen
    fig.update_layout(
        legend_title="Teams",
        showlegend=True
    )
    
    st.plotly_chart(fig)





