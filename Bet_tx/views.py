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

#Set locale to Pt-br
locale.setlocale(locale.LC_ALL, 'pt_BR.utf-8')

# Fuso horário do Brasil
tz = pytz.timezone('America/Sao_Paulo')


def update_matches():
    global matches
    matches = asyncio.run(get_odds())
    print('Odds e partidas atualizadas.')

schedule.every(1).minutes.do(update_matches)

def schedule_thread():
    while True:
        schedule.run_pending()
        time.sleep(1)



@views.route("/")
@views.route("/home",  methods=['GET', 'POST'])
@login_required
def home():
    global matches
    if matches is None:
        matches = asyncio.run(get_odds())
    print(matches)
    return render_template('home.html', matches=matches, user=current_user)




@views.route('/show_results',  methods=['GET', 'POST'])
@login_required
def show_results():
    if request.method == 'POST':
        form_data = dict(request.form)
        name = current_user.username 
        value_bet = form_data['valor']
        del form_data['valor']
        try:
            value_bet = float(value_bet)
        except:    
            flash('Por favor, insira um valor para a aposta!')
            return redirect(url_for('home'))
        
        matches_bet= []
        odds = []
        
        for team, value in form_data.items():
            odds_str, outcome = value.split(',')
            try:
                odds_float = float(odds_str)
            except ValueError:
                flash(f'Valor inválido de cotação para {team}!')
                return redirect(url_for('home'))
            matches_bet.append((team,outcome,odds_float))
            odds.append(odds_float)

        if not matches_bet:
            flash('Selecione os times para fazer a aposta.')
            return redirect(url_for('home'))
        
        odd_final = math.prod(odds)
        odd_final_text = f'{odd_final:_.2f}'
        value_bet_not_format = value_bet
        value_return_bet = odd_final * value_bet
        return_bet = locale.currency(value_return_bet, grouping=True)
        value_bet = locale.currency(value_bet, grouping=True)

        message_body = f"Apostas feitas:\n"
        for match in matches_bet:
            message_body += f"- {match[0]} x {match[1]} ({match[2]})\n"

        now_time = datetime.datetime.now(tz)
        now_time = now_time.strftime("%H:%M")
        message_body += f"\nODDS: *{odd_final_text}*\nValor Apostado: *{value_bet}*\nPossível Retorno: {return_bet}.\nHorário: {now_time}.\n Nome apostado: {name}"    
        
        matches_bet_str = '|'.join([','.join(map(str, match)) for match in matches_bet])


        new_bet = Bet(matches_bet=matches_bet_str, odd_final=odd_final, value_bet=value_bet_not_format, return_bet=value_return_bet,author=current_user.id)
        db.session.add(new_bet)
        db.session.commit()
        send_message(message_body)            
        session.clear()
        return render_template('result.html',matches_bet=matches_bet, odd_final=odd_final_text,value_bet = value_bet, return_bet=return_bet)
    
    return redirect(url_for("home"))

