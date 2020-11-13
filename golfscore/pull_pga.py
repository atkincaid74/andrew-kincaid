import requests
from bs4 import BeautifulSoup


def get_players(soup, player_col, score_col, thru_col):
    rows = soup.find_all("tr", class_="Table__TR Table__even")
    players = {}

    for row in rows[1:]:
        cols = row.find_all("td")
        # If we get a bad row. For example, during the tournament we there 
        # is a place holder row that represents the cut line
        if len(cols) < 5:
            continue
        player = cols[player_col].text.strip()
        score = cols[score_col].text.strip().upper()        
        thru = cols[thru_col].text.strip() if thru_col else "F" 
        if score == 'CUT':
            players[player] = {'TO PAR': 'CUT', 'THRU': thru}
            continue
        elif score == 'WD':
            players[player] = {'TO PAR': 'WD', 'THRU': thru}
            continue
        elif score == 'DQ':
            players[player] = {'TO PAR': 'DQ', 'THRU': thru}
            continue
        elif score == 'E':
            players[player] = {'TO PAR': 0, 'THRU': thru}
        else:
            try:
                players[player] = {'TO PAR': int(score), 'THRU': thru}
            except ValueError:
                players[player] = {'TO PAR': '?', 'THRU': '?'}
    return players


def get_col_indices(soup):
    header_rows = soup.find_all("tr", class_="Table__TR Table__even")

    # other possible entries for what could show up, add here.
    player_fields = ['PLAYER']
    to_par_fields = ['TO PAR', 'TOPAR', 'TO_PAR']
    thru_fields = ['THRU']

    header_col = header_rows[0].find_all("th")

    player_col = None
    score_col = None
    thru_col = None

    for i in range(len(header_col)):
        col_txt = header_col[i].text.strip().upper()
        if col_txt in player_fields:
            player_col = i
            continue
        if col_txt in to_par_fields:
            score_col = i
            continue
        if col_txt in thru_fields:
            thru_col = i
            continue

    if player_col is None or score_col is None:
        print("Unable to track columns")
        exit()
    
    return player_col, score_col, thru_col


def verify_scrape(players):
    if len(players) < 25:
        print("Less than 25 players, seems suspicious, so exiting")

    bad_entry_count = 0
    for key, value in players.items():
        scr = players[key]['TO PAR']
        if scr == '?':
            bad_entry_count += 1
        if type(scr) is int and (scr > 50 or scr < -50):
            print(f"Bad score entry {scr}")

    if bad_entry_count > 3:
        # arbitrary number here, I figure this is enough
        # bad entries to call it a bad pull
        print("Multiple bad entries, exiting")


def get_tournament_name(soup):
    tournament_name = soup.find_all(
        "h1", class_="headline headline__h1 Leaderboard__Event__Title")[0].text
    return tournament_name


def get_player_data():
    result = requests.get("http://www.espn.com/golf/leaderboard")
    soup = BeautifulSoup(result.text, "html.parser")

    player_col, score_col, thru_col = get_col_indices(soup)
    players = get_players(soup, player_col, score_col, thru_col)
    verify_scrape(players)

    return players


def get_score_data():
    result = requests.get("http://www.espn.com/golf/leaderboard")
    soup = BeautifulSoup(result.text, "html.parser")

    status = soup.find_all("div",
                           class_="status")[0].find_all("span")[0].text.upper()
    active = 'FINAL' not in status

    player_col, score_col, thru_col = get_col_indices(soup)
    players = get_players(soup, player_col, score_col, thru_col)

    verify_scrape(players)

    data = {'Tournament': get_tournament_name(soup),
            'IsActive': active, 'Players': players}

    return data


def get_status():
    result = requests.get("http://www.espn.com/golf/leaderboard")
    soup = BeautifulSoup(result.text, "html.parser")

    status = soup.find_all("div",
                           class_="status")[0].find_all("span")[0].text

    return status
