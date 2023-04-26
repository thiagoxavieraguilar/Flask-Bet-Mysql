import httpx
import asyncio
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Get the ODDS API KEY from the .env file
api_key = os.environ.get('ODDS_API_KEY')

# Set the sport keys to soccer leagues in Brazil and UEFA Champions League
sport_key = ['soccer_brazil_campeonato', 'soccer_uefa_champs_league']
# Set the market to Head to Head
market = 'h2h'

# Ssynchronous function that retrieves the odds from the API
async def get_odds():
    async with httpx.AsyncClient() as client:
        matches = []

        # Loop through the sport keys to retrieve odds for each
        for sport in sport_key:
            url = f'https://api.the-odds-api.com/v3/odds/?apiKey={api_key}&sport={sport}&region=uk&mkt={market}'
            try:
                response = await client.get(url)
                print(response)
                if response.status_code == 200:
                    print('request feita')
                    data = response.json()
                    if data['success']:
                        # Loop through the matches in the data
                        for match in data['data']:
                            # Get the home and visiting teams 
                            home_team = match['home_team']
                            visit_team = match['teams'][1]
                            # If the home team and visit team are the same, it is likely that the order is wrong
                            # Therefore, we switch the order of the visit and home team and mark an error in the order of the teams
                            if home_team == visit_team:
                                visit_team = match['teams'][0]   
                                error_ordem_team = True     
                            else:
                                error_ordem_team = False             
                            for site in match['sites']:
                                # Get the  odds from matches 
                                if site['site_key'] == 'betway':
                                    if error_ordem_team == True:
                                        odd_home_team = site['odds']['h2h'][1]
                                        odd_visit_team = site['odds']['h2h'][0]
                                    else:
                                        odd_home_team = site['odds']['h2h'][0]
                                        odd_visit_team = site['odds']['h2h'][1]
                                    odd_empate= site['odds']['h2h'][1]

                                     # Add the match data to the matches list
                                    match_data = {
                                            'home_team': home_team,
                                            'home_team_odds': odd_home_team,
                                            'visit_team': visit_team,
                                            'visit_team_odds': odd_visit_team,
                                            'empate_odds': odd_empate
                                        }
                                    matches.append(match_data)
            except httpx.HTTPError:
                pass
    return matches