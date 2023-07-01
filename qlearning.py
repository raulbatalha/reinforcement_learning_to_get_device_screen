#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 21:12:51 2023
@author: Raul Batalha
@email: raul.batalha@hotmail.com
"""

import random

import matplotlib.pyplot as plt
import numpy as np

from env_screen import EnvScreen


class QLearning():
    def __init__(self):
        self.env = EnvScreen(dimensions=[EnvScreen.width_cols, EnvScreen.height_rows])
    
    @staticmethod
    def learnQ(state, action, value_dict):
        result = value_dict.get(state, {}).get(action, 10)
        return result

    @staticmethod
    def update(state, action, value, value_dict):
        state_values = value_dict.get(state, None)
        if state_values:
            state_values[action] = value
        else:
            value_dict[state] = {}
            value_dict[state][action] = value

    @staticmethod
    def allowed_actions(input_state):
        state = input_state
        allowed = ['UP', 'DOWN', 'RIGHT', 'LEFT']
        last_line = state.split('\n')[-1]
        if last_line:
            for c in last_line:
                if c == 'P':
                    allowed.remove('DOWN')
        first_line = state.split('\n')[0]
        if first_line:
            for c in first_line:
                if c == 'P':
                    allowed.remove('UP')
        line_length = EnvScreen.width_cols + 1
        for i in range(EnvScreen.height_rows):
            if len(state) > line_length * i:
                if state[line_length * i] == 'P':
                    allowed.remove('LEFT')
            if len(state) > line_length * i + line_length - 1:
                if state[line_length * i + line_length - 1] == 'P':
                    allowed.remove('RIGHT')
        return allowed

    @staticmethod
    def policy(values, state, epsilon=0.1, verbose=False):
        best_action = None
        best_value = float('-inf')
        allowed = QLearning.allowed_actions(state)
        random.shuffle(allowed)
        for action in allowed:
            if verbose:
                print(f'action: {action} value: {QLearning.learnQ(state, action, values)} vs best_value: {best_value}')
            if QLearning.learnQ(state, action, values) > best_value:
                best_value = QLearning.learnQ(state, action, values)
                if verbose:
                    print(f'new best action: {action}')
                best_action = action
        r_var = random.random()
        if verbose:
            print(f'{r_var} vs {epsilon}')
        if r_var < epsilon:
            if verbose:
                print('choosing random')
            best_action = random.choice(allowed)
            best_value = QLearning.learnQ(state, best_action, values)
        if verbose:
            print(f'chose: {best_action}')
        return best_action, best_value

    @staticmethod
    def state_values(values):
        state_matrix = [[0 for _ in range(EnvScreen.width_cols)] for _ in range(EnvScreen.height_rows)]
        for i in range(EnvScreen.height_rows):
            for j in range(EnvScreen.width_cols):
                mock_env = EnvScreen(dimensions=[EnvScreen.width_cols, EnvScreen.height_rows])
                mock_env.position = np.asarray([i, j])
                mock_env.goal_position = np.asarray(EnvScreen.goal)
                state = mock_env.compressed_state_rep()
                best_value = float('-inf')
                allowed = QLearning.allowed_actions(state)
                for action in allowed:
                    if QLearning.learnQ(state, action, values) > best_value:
                        best_value = QLearning.learnQ(state, action, values)
                state_matrix[i][j] = round(best_value, 1)
        for row in state_matrix:
            print(row)
        return state_matrix
    
    @staticmethod
    def unique_starts(i):
        position = [14, 4]
        goal_position = EnvScreen.goal
        return position, goal_position
