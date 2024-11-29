#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 21:12:51 2023
@author: Raul Batalha
@email: raul.batalha@hotmail.com
"""

import os
import time

from src.utils.capture_screen import CaptureScreen
from agent.qagent import QAgent
from src.utils.test_screen import ScreenTest
from src.utils.util import *


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def menu():
    while True:
        clear_screen()
        print("====== Screen ======")
        print("1. Screen Train")
        print("2. Screen Test")
        print("3. Exit")
        choice = input("Choose options: ")
        if choice == "1":
            path_file = 'files/uidump.xml'
            WindowDump.dump_window()
            touchable_areas, screen_width, screen_height = TouchArea.parse_dump(path_file)
            capture = CaptureScreen(touchable_areas)
            capture.save_file_txt()
            agent = QAgent()
            agent.run_training()
        elif choice == "2":
            test_agent = ScreenTest('models/training_model.npy')
            num_episodes = 10
            output_file = 'files/goal_positions.txt'
            goal_positions = test_agent.test(num_episodes, output_file)
            print("Goal Positions:", goal_positions)
            test_agent.plot_state_values(test_agent.values)
        elif choice == "3":
            break
        else:
            print("Invalid option. Try again!")
            
if __name__ == "__main__":
    menu()