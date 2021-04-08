import re
import requests
import pandas as pd
from bs4 import BeautifulSoup


def to_int(potential_int):
    try:
        return int(potential_int)
    except ValueError:
        return potential_int


def get_players(soup):
    (player_col, score_col, thru_col, position_col, today_col,
     total_col, round_cols, tee_time_col) = get_col_indices(soup)
    rows = soup.find_all("tr", class_="Table__TR Table__even")
    players = {}

    for row in rows[1:]:
        cols = row.find_all("td")
        # # If we get a bad row. For example, during the tournament we there
        # #  is a place holder row that represents the cut line
        # if len(cols) < 5:
        #     continue
        player = cols[player_col].text.strip()
        out_dict = {}

        if score_col is not None:
            score = cols[score_col].text.strip().upper()
            if score in ('CUT', 'WD', 'DQ', 'E'):
                out_dict['TO PAR'] = score
            else:
                try:
                    out_dict['TO PAR'] = int(score)
                except ValueError:
                    out_dict['TO PAR'] = '?'

        if today_col:
            today = cols[today_col].text.strip()
            out_dict['TODAY'] = to_int(today)

        if thru_col:
            out_dict['THRU'] = cols[thru_col].text.strip() if thru_col else "F"

        if round_cols[1] is not None:
            out_dict['R1'] = to_int(cols[round_cols[1]].text.strip())
        if round_cols[2] is not None:
            out_dict['R2'] = to_int(cols[round_cols[2]].text.strip())
        if round_cols[3] is not None:
            out_dict['R3'] = to_int(cols[round_cols[3]].text.strip())
        if round_cols[4] is not None:
            out_dict['R4'] = to_int(cols[round_cols[4]].text.strip())

        if total_col is not None:
            out_dict['TOTAL'] = to_int(cols[total_col].text.strip())
        if position_col is not None:
            out_dict['POSITION'] = cols[position_col].text.strip()
        if tee_time_col is not None:
            out_dict['TEE TIME'] = cols[tee_time_col].text.strip()

        players[player] = out_dict

    score_df = pd.DataFrame.from_dict(players, orient='index')

    if 'TO PAR' in score_df.columns:
        score_df.loc[score_df['TO PAR'] == 'WD'] = score_df.loc[
            score_df['TO PAR'] == 'WD'].apply(fix_withdrew, axis=1)
        score_df.loc[score_df['TO PAR'] == 'CUT'] = score_df.loc[
            score_df['TO PAR'] == 'CUT'].apply(fix_cut, axis=1)

    return score_df


def fix_withdrew(s):
    s.loc[s.index.str.match(r'R\d') &
          ((~s.astype(str).str.isnumeric()) |
           (pd.to_numeric(s, errors='coerce') < 60))] = 80
    s.POSITION = 'WD'
    s['TO PAR'] = s.loc[s.index.str.match(r'R\d')].sub(72).sum()
    s['TOTAL'] = s.loc[s.index.str.match(r'R\d')].sum()

    return s


def fix_cut(s):
    s.loc[['R3', 'R4']] = 80
    s.POSITION = 'CUT'
    s['TO PAR'] = s.loc[s.index.str.match(r'R\d')].sub(72).sum()
    s['TOTAL'] = s.loc[s.index.str.match(r'R\d')].sum()

    return s


def get_col_indices(soup):
    header_rows = soup.find_all("tr", class_="Table__TR Table__even")

    # other possible entries for what could show up, add here.
    player_fields = ['PLAYER']
    to_par_fields = ['TO PAR', 'TOPAR', 'TO_PAR']
    thru_fields = ['THRU']
    position_fields = ['POS', 'POSITION']
    today_fields = ['TODAY']
    total_fields = ['TOT', 'TOTAL']
    tee_time_fields = ['TEE TIME']

    header_col = header_rows[0].find_all("th")

    player_col = None
    score_col = None
    thru_col = None
    position_col = None
    today_col = None
    total_col = None
    round_cols = {i: None for i in range(1, 5)}
    tee_time_col = None

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
        if col_txt in position_fields:
            position_col = i
            continue
        if col_txt in today_fields:
            today_col = i
            continue
        if col_txt in total_fields:
            total_col = i
            continue
        if re.match(r'R\d', col_txt):
            rnd = int(re.findall(r'\d', col_txt)[0])
            round_cols[rnd] = i
            continue
        if col_txt in tee_time_fields:
            tee_time_col = i
            continue

    if player_col is None:
        print("Unable to track columns")
    
    return (player_col, score_col, thru_col, position_col, today_col,
            total_col, round_cols, tee_time_col)


def verify_scrape(players):
    if len(players) < 25:
        print("Less than 25 players, seems suspicious, so exiting")

    bad_entry_count = 0
    for key, value in players.items():
        scr = value['TO PAR']
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


def get_projected_cut(soup=None):
    if soup is None:
        result = requests.get("http://www.espn.com/golf/leaderboard")
        soup = BeautifulSoup(result.text, "html.parser")

    try:
        projected_cut = soup.find(
            "tr", class_="cutline Table__TR Table__even"
        ).find("td").find("span").text.strip()
    except Exception as e:
        print(e)
        projected_cut = None

    return projected_cut


def get_player_data(soup=None):
    if soup is None:
        result = requests.get("http://www.espn.com/golf/leaderboard")
        soup = BeautifulSoup(result.text, "html.parser")

    players = get_players(soup)
    # verify_scrape(players)

    return players


def get_score_data():
    result = requests.get("http://www.espn.com/golf/leaderboard")
    soup = BeautifulSoup(result.text, "html.parser")

    status = soup.find_all("div",
                           class_="status")[0].find_all("span")[0].text.upper()
    active = 'FINAL' not in status

    players = get_players(soup)

    verify_scrape(players)

    data = {'Tournament': get_tournament_name(soup),
            'IsActive': active, 'Players': players}

    return data


def get_status(soup=None):
    if soup is None:
        result = requests.get("http://www.espn.com/golf/leaderboard")
        soup = BeautifulSoup(result.text, "html.parser")

    status = soup.find_all("div",
                           class_="status")[0].find_all("span")[0].text

    return status


def get_soup():
    result = requests.get("http://www.espn.com/golf/leaderboard")
    soup = BeautifulSoup(result.text, "html.parser")

    return soup
