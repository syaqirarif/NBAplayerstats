import streamlit as st
import pandas as pd

st.title("2021-2022 NBA Playoffs Player Stats")

csv_file = '2021-2022 NBA Player Stats - Playoffs.csv'
df = pd.read_csv(csv_file, encoding='ISO-8859-1', delimiter=';')

df.columns = [
    'Rank', 'Player', 'Position', 'Age', 'Team', 'Games Played', 'Games Started',
    'Minutes Per Game', 'Field Goals Made', 'Field Goals Attempted', 'Field Goal Percentage',
    '3-Pointers Made', '3-Pointers Attempted', '3-Point Percentage', '2-Pointers Made',
    '2-Pointers Attempted', '2-Point Percentage', 'Effective FG Percentage', 'Free Throws Made',
    'Free Throws Attempted', 'Free Throw Percentage', 'Offensive Rebounds', 'Defensive Rebounds',
    'Total Rebounds', 'Assists', 'Steals', 'Blocks', 'Turnovers', 'Personal Fouls', 'Points'
]

positions = df['Position'].unique()

position_summary = pd.DataFrame({
    'Abbreviation': ['C', 'SG', 'PG', 'PF', 'SF'],
    'Position': ['Center', 'Shooting Guard', 'Point Guard', 'Power Forward', 'Small Forward'],
})

st.write("### Basketball Positions Summary")
st.dataframe(position_summary)

players_by_position = {pos: df[df['Position'] == pos]['Player'].tolist() for pos in positions}

def most_likely_to_succeed(df, position):
    df_pos = df[df['Position'] == position]
    df_pos['Success Score'] = df_pos['Points'] + df_pos['Assists'] + df_pos['Total Rebounds']
    top_player = df_pos.loc[df_pos['Success Score'].idxmax()]
    return top_player

top_players = {}
positions_list = ['C', 'SG', 'PG', 'PF', 'SF']

for pos in positions_list:
    top_players[pos] = most_likely_to_succeed(df, pos)

top_players_df = pd.DataFrame(top_players).T
top_players_df = top_players_df[['Player', 'Team', 'Points', 'Assists', 'Total Rebounds']]

st.write("### Top Player for Each Position")
st.dataframe(top_players_df)

st.write("### Player Statistics Overview")
st.dataframe(df)

st.write("### Basic Statistics")
st.write(df.describe())

st.write("### Advanced Efficiency Analysis")

df['Points per FG Attempt'] = df['Points'] / df['Field Goals Attempted']
df['Assists-to-Turnover Ratio'] = df['Assists'] / df['Turnovers']
df['Efficiency Score'] = (
    df['Points per FG Attempt'] * 0.4 +
    df['Assists-to-Turnover Ratio'] * 0.3 +
    df['Games Played'] * 0.2 +
    df['Minutes Per Game'] * 0.1
)

selected_players = {}
for pos in positions_list:
    selected_player = st.selectbox(f"Select a {position_summary[position_summary['Abbreviation'] == pos]['Position'].values[0]}", players_by_position[pos])
    selected_players[pos] = selected_player

st.write("### Your Dream Team")
dream_team_df = pd.DataFrame({
    'Position': [position_summary[position_summary['Abbreviation'] == pos]['Position'].values[0] for pos in positions_list],
    'Player': [selected_players[pos] for pos in positions_list]
})

st.dataframe(dream_team_df)

custom_team_ids = {
    'C': 3,
    'SG': 68,
    'PG': 58,
    'PF': 67,
    'SF': 185
}

custom_team_players = {}
for pos, player_id in custom_team_ids.items():
    player = df[df['Rank'] == player_id]['Player'].values[0]
    custom_team_players[pos] = player

custom_team_df = pd.DataFrame({
    'Position': [position_summary[position_summary['Abbreviation'] == pos]['Position'].values[0] for pos in custom_team_ids.keys()],
    'Player': [custom_team_players[pos] for pos in custom_team_ids.keys()]
})

st.write("### Team Chosen by Me (Basically the Olympic Team XD)")
st.dataframe(custom_team_df)
