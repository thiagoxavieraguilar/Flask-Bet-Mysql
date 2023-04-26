from flask import Flask,render_template, request,session,redirect, url_for, flash, Blueprint
from flask_login import login_required, current_user
from Bet_tx import db
from .models import User,Bet
from Bet_tx.functions import get_odds
from Bet_tx.whatsapp_twilio import send_message
import asyncio
import math
import locale
import datetime
import schedule
import time
import pytz


matches = None

views = Blueprint("views", __name__)

# Set locale to Pt-br
locale.setlocale(locale.LC_ALL, 'pt_BR.utf-8')

# Fuso horário do Brasil
tz = pytz.timezone('America/Sao_Paulo')


# Function to update matches
def update_matches():
    """
    Updates the matches variable by calling the get_odds function and 
    assigning the result to the global variable matches.
    """
    global matches
    matches = asyncio.run(get_odds())
    print('Odds e partidas atualizadas.')

schedule.every(1).minutes.do(update_matches)

def schedule_thread():
    """
    Runs the schedule module to periodically update the matches variable.
    """
    while True:
        schedule.run_pending()
        time.sleep(1)



@views.route("/")
@views.route("/home",  methods=['GET', 'POST'])
@login_required
def home():
    """
    Renders the home page and passes the matches and current_user objects to the template.

    Matches is a list of dictionaries containing odds data for soccer matches. If matches is None, calls the 
    get_odds function asynchronously and stores the result in matches. If matches is empty, displays an error 
    message. Otherwise, renders the home template with the matches and current_user objects.
    """
    global matches
    if matches is None:
        matches = asyncio.run(get_odds())
    
    if len(matches) == 0:
        flash('Error com a Api.')
        return render_template('home.html', matches=matches, user=current_user)
    return render_template('home.html', matches=matches, user=current_user)




@views.route('/show_results',  methods=['GET', 'POST'])
@login_required
def show_results():
    """
    Processes the form data from the home page and creates a new Bet object with the data.
    """
    if request.method == 'POST':
        try:
            form_data = dict(request.form)
            name = current_user.username 
            value_bet = form_data['valor']
            # Checking if the bet value is valid
            if value_bet is not None:
                del form_data['valor']
                try:
                    value_bet = float(value_bet)
                except:    
                    flash('Por favor, insira um valor válido para a aposta!')
                    return redirect(url_for('views.home'))
            else:
                flash('Por favor, insira um valor para a aposta!')
                return redirect(url_for('views.home'))
            matches_bet= []
            odds = []

            # Creating a list of matches and their odds
            for team, value in form_data.items():
                odds_str, outcome = value.split(',')
                try:
                    odds_float = float(odds_str)
                except ValueError:
                    flash(f'Valor inválido de cotação para {team}!')
                    return render_template('home')
                matches_bet.append((team,outcome,odds_float))
                odds.append(odds_float)

            # Checking if at least one match is selected
            if not matches_bet:
                flash('Selecione os times para fazer a aposta.')
                return render_template('home')
            
            # Calculating the final odds and the possible return value
            odd_final = math.prod(odds)
            odd_final_text = f'{odd_final:_.2f}'
            value_bet_not_format = value_bet
            value_return_bet = odd_final * value_bet
            return_bet = locale.currency(value_return_bet, grouping=True)
            value_bet = locale.currency(value_bet, grouping=True)

            # Creating a message to send via WhatsApp with twilio
            message_body = f"Apostas feitas:\n"
            for match in matches_bet:
                message_body += f"- {match[0]} x {match[1]} ({match[2]})\n"

            now_time = datetime.datetime.now(tz)
            now_time = now_time.strftime("%H:%M")
            message_body += f"\nODDS: *{odd_final_text}*\nValor Apostado: *{value_bet}*\nPossível Retorno: {return_bet}.\nHorário: {now_time}.\n Nome apostado: {name}"    
            
            matches_bet_str = '|'.join([','.join(map(str, match)) for match in matches_bet])

            # Create a new instance of the Bet class with the given parameters
            new_bet = Bet(matches_bet=matches_bet_str, odd_final=odd_final, value_bet=value_bet_not_format, return_bet=value_return_bet,author=current_user.id)
            # Add the new_bet object to the database session and commit
            db.session.add(new_bet)
            db.session.commit()
            # Call the function to send message with twilio 
            send_message(message_body)            
            session.clear()
            return render_template('result.html',matches_bet=matches_bet, odd_final=odd_final_text,value_bet = value_bet, return_bet=return_bet)
        except:
            return redirect(url_for('views.home'))
    return redirect(url_for('views.home'))
