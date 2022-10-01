#!/usr/bin/env python

import pygame  # install via pip install pygame
import threading
import queue
import os

pygame.init()
clock = pygame.time.Clock()

joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
joystick_list = []
joyid = "joyid"
joyname = "joyname"

for i in range(pygame.joystick.get_count()):
    jid = {joyid: i, joyname: pygame.joystick.Joystick(i).get_name()}
    print(pygame.joystick.Joystick(i).get_guid())
    joystick_list.append(jid)
mascon_select = next((i for i, item in enumerate(joystick_list) if item["joyname"] == "Nintendo Switch Pro Controller"),
                     None)

if mascon_select is None:
    print("No Nintendo Switch Pro Controller found. Connect the correct controller and restart the script")
    exit()


mascon_counter = 99
pygame.event.clear()  # Clear events to remove wrong inputs.

while 1:
    for event in pygame.event.get():
        if event.type == pygame.JOYAXISMOTION:
            # Lever section
            mascon_axis = (joysticks[mascon_select].get_axis(1))
            mascon_axis = (round(mascon_axis, 2))
            if mascon_axis == 0.8:
                #print("P4")
                qMascon.put(power_max)
                mascon_counter = 1
            if mascon_axis == 0.62:
                if mascon_counter == 3:
                    qMascon.put(power_inc)
                    mascon_counter = 2
                if mascon_counter == 1:
                    qMascon.put(power_dec)
                    mascon_counter = 2
            if mascon_axis == 0.44:
                if mascon_counter == 4:
                    qMascon.put(power_inc)
                    mascon_counter = 3
                if mascon_counter == 2:
                    qMascon.put(power_dec)
                    mascon_counter = 3
            if mascon_axis == 0.25:
                if mascon_counter == 5:
                    qMascon.put(power_inc)
                    mascon_counter = 4
                if mascon_counter == 3:
                    qMascon.put(power_dec)
                    mascon_counter = 4
            if mascon_axis == 0.0:
                qMascon.put(neutral)
                mascon_counter = 5
            if mascon_axis == -0.21:
                if mascon_counter == 5:
                    qMascon.put(brake_inc)
                    mascon_counter = 6
                if mascon_counter == 7:
                    qMascon.put(brake_dec)
                    if notchfix:
                        qMascon.put(brake_dec)
                    mascon_counter = 6
            if mascon_axis == -0.32:
                if mascon_counter == 6:
                    qMascon.put(brake_inc)
                    if notchfix:
                        qMascon.put(brake_inc)
                    mascon_counter = 7
                if mascon_counter == 8:
                    qMascon.put(brake_dec)
                    mascon_counter = 7
            if mascon_axis == -0.43:
                if mascon_counter == 7:
                    qMascon.put(brake_inc)
                    mascon_counter = 8
                if mascon_counter == 9:
                    qMascon.put(brake_dec)
                    if notchfix:
                        qMascon.put(brake_dec)
                    mascon_counter = 8
            if mascon_axis == -0.53:
                if mascon_counter == 8:
                    qMascon.put(brake_inc)
                    if notchfix:
                        qMascon.put(brake_inc)
                    mascon_counter = 9
                if mascon_counter == 10:
                    qMascon.put(brake_dec)
                    mascon_counter = 9
            if mascon_axis == -0.64:
                if mascon_counter == 9:
                    qMascon.put(brake_inc)
                    mascon_counter = 10
                if mascon_counter == 11:
                    qMascon.put(brake_dec)
                    mascon_counter = 10
            if mascon_axis == -0.75:
                if mascon_counter == 10:
                    qMascon.put(brake_inc)
                    if notchfix:
                        qMascon.put(brake_inc)
                    mascon_counter = 11
                if mascon_counter == 12:
                    qMascon.put(brake_dec)
                    mascon_counter = 11
            if mascon_axis == -0.85:
                if mascon_counter == 11:
                    qMascon.put(brake_inc)
                    mascon_counter = 12
                if mascon_counter >= 13:
                    qMascon.put(brake_dec)
                    mascon_counter = 12
            if mascon_axis == -1.00:
                qMascon.put(brake_eb)
                mascon_counter = 14

        # Button section
        if event.type == pygame.JOYBUTTONDOWN and event.button == 0:
            print("A")
        if event.type == pygame.JOYBUTTONDOWN and event.button == 1:
            print("B")
        if event.type == pygame.JOYBUTTONDOWN and event.button == 2:
            print("X")
        if event.type == pygame.JOYBUTTONDOWN and event.button == 3:
            print("Y")
        if event.type == pygame.JOYBUTTONDOWN and event.button == 4:
            print("MINUS")
        if event.type == pygame.JOYBUTTONDOWN and event.button == 6:
            print("PLUS")
        if event.type == pygame.JOYBUTTONDOWN and event.button == 11:
            print("UP")
        if event.type == pygame.JOYBUTTONDOWN and event.button == 12:
            print("DOWN")
        if event.type == pygame.JOYBUTTONDOWN and event.button == 13:
            print("LEFT")
        if event.type == pygame.JOYBUTTONDOWN and event.button == 14:
            print("RIGHT")
