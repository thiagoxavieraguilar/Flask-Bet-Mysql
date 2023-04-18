import httpx
import asyncio
import os
from dotenv import load_dotenv


load_dotenv()
api_key = os.environ.get('ODDS_API_KEY')
sport_key = ['soccer_brazil_campeonato', 'soccer_uefa_champs_league']
market = 'h2h'

async def get_odds():
    async with httpx.AsyncClient() as client:
        matches = []

        for sport in sport_key:
            url = f'https://api.the-odds-api.com/v3/odds/?apiKey={api_key}&sport={sport}&region=uk&mkt={market}'
            try:
                response = await client.get(url)
                print(response)
                if response.status_code == 200:
                    print('request feita')
                    data = response.json()
                    if data['success']:
                        for match in data['data']:
                            home_team = match['home_team']
                            visit_team = match['teams'][1]
                            if home_team == visit_team:
                                visit_team = match['teams'][0]   
                                error_ordem_team = True     
                            else:
                                error_ordem_team = False
                                
                            for site in match['sites']:
                                if site['site_key'] == 'betway':
                                    if error_ordem_team == True:
                                        odd_home_team = site['odds']['h2h'][1]
                                        odd_visit_team = site['odds']['h2h'][0]
                                    else:
                                        odd_home_team = site['odds']['h2h'][0]
                                        odd_visit_team = site['odds']['h2h'][1]
                                    odd_empate= site['odds']['h2h'][1]

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