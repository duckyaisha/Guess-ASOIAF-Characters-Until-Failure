#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 19:43:39 2026

@author: alexmorano
"""

# Guess asoiaf characters until failure
import streamlit as st
import pandas as pd
import time

def clear_input():
    st.session_state.guessbox = ""

asoiafdf = pd.read_csv("CLEANasoiafcsv.csv")

st.title("Guess ASOIAF Characters Until Failure")

if "correctlist" not in st.session_state:
    st.session_state.correctlist = []

if "madeupguys" not in st.session_state:
    st.session_state.madeupguys = []

if "incorrectcounter" not in st.session_state:
    st.session_state.incorrectcounter = 0

if "timer" not in st.session_state:
    st.session_state.timer = 30  # start with 30 seconds

timer_display = st.empty()
timer_display.write(f"Time remaining: {st.session_state.timer} seconds")

if st.session_state.timer <= 0:
    st.error("⏳ TIME'S UP! Game over!")
    st.write(f"Correct guesses ({len(st.session_state.correctlist)}): {st.session_state.correctlist}")
    st.write(f"Fake guesses: {st.session_state.madeupguys}")
    st.stop()  # stop the rest of the app

with st.form("guess_form", clear_on_submit= True):
    character = st.text_input(
        "Guess a character. Aliases accepted (Blackfish, Bloodraven). "
        "Use full names like Eddard Stark."
        "Use married names for married women like Catelyn Stark",

    )
    
    submitted = st.form_submit_button("Submit Guess")
    

if submitted:
    character = character.strip().lower()


    if character == "":
        st.warning("Enter a character name first!")

    elif character in asoiafdf["Character"].values and character not in st.session_state.correctlist:
        st.success(f"Yes, {character} is a legitimate ASOIAF character")
        st.session_state.correctlist.append(character)
        st.session_state.timer += 5
        
    elif character in asoiafdf["Character"].values and character in st.session_state.correctlist:
        st.warning(f"Already said {character}")

    elif character in asoiafdf["Alias"].values:
        row = asoiafdf[asoiafdf["Alias"] == character]
        realname = row.iloc[0]["Character"]
        
        if realname not in st.session_state.correctlist:
            st.success(f"Yes, {realname} (also known as {character}) is a legitimate ASOIAF character")
            st.session_state.correctlist.append(realname)
            st.session_state.timer += 8
            
        else:
            st.warning(f"Already said {realname}")
    
    elif character not in asoiafdf["Alias"].values and character not in asoiafdf['Character'].values:
        parts = character.split()
        
        if len(parts) == 1:
            firstname = parts[0]
        
            match = asoiafdf[
                (asoiafdf["Forename"] == firstname)]
        
            if not match.empty:
                realname = match.iloc[0]["Character"]

                if realname not in st.session_state.correctlist:
                    st.success(f"Yes, {realname} is a legitimate ASOIAF character")
                    st.session_state.correctlist.append(realname)
                    st.session_state.timer += 5
        
        
            if match.empty:
                st.error(f"{character} is not a valid ASOIAF character")
                st.session_state.incorrectcounter += 1
                st.session_state.madeupguys.append(character)

            
        if len(parts) >= 2:
            firstname = parts[0]
            surname = parts[-1]

            match = asoiafdf[
                (asoiafdf["Forename"] == firstname) &
                (
                (asoiafdf["Surname"] == surname) | 
                (asoiafdf["Old Surname"] == surname)
                )
                ]

            if not match.empty:
                realname = match.iloc[0]["Character"]

                if realname not in st.session_state.correctlist:
                    st.success(f"Yes, {realname} is a legitimate ASOIAF character")
                    st.session_state.correctlist.append(realname)
                    st.session_state.timer += 5
        
            if match.empty:
                st.error(f"{character} is not a valid ASOIAF character")
                st.session_state.incorrectcounter += 1
                st.session_state.madeupguys.append(character)

    else:
        st.error(f"{character} is not a valid ASOIAF character")
        st.session_state.incorrectcounter += 1
        st.session_state.madeupguys.append(character)

   
if st.session_state.timer > 0:
    time.sleep(1)
    st.session_state.timer -= 1
    st.rerun()