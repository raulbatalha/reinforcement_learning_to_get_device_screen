#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 21:12:51 2023
@author: Raul Batalha
@email: raul.batalha@hotmail.com
"""

import matplotlib.pyplot as plt
import numpy as np

from src.environment.env_screen import EnvScreen
from agent.qlearning import QLearning


class ScreenTest:
    def __init__(self, model_path):
        self.values = np.load(model_path, allow_pickle=True)
        self.env = EnvScreen(dimensions=[EnvScreen.width_cols, EnvScreen.height_rows])

    def test(self, num_episodes, output_file):
        goal_positions = []
        with open(output_file, 'w') as file:
            for episode in range(num_episodes):
                self.env.reset()
                position, goal_position = QLearning.unique_starts(episode)
                self.env.position = np.asarray(position)
                self.env.goal_position = np.asarray(goal_position)
                current_state = self.env.compressed_state_rep()
                while not self.env.over:
                    action, _ = QLearning.policy(self.values, current_state, epsilon=0)
                    self.env.move(action)
                    current_state = self.env.compressed_state_rep()
                goal_positions.append(self.env.goal_position.tolist())
                goal_str = f"Episode {episode+1}: Goal position found! Goal: {self.env.goal_position.tolist()}\n"
                file.write(goal_str)
                print(goal_str)
        return goal_positions
    
    @staticmethod
    def plot_state_values(values):
        state_matrix = [[0 for _ in range(EnvScreen.width_cols)] for _ in range(EnvScreen.height_rows)]
        for i in range(EnvScreen.height_rows):
            for j in range(EnvScreen.width_cols):
                mock_env = EnvScreen(dimensions=[EnvScreen.width_cols, EnvScreen.height_rows])
                mock_env.position = np.asarray([i, j])
                mock_env.goal_position = np.asarray(EnvScreen.goal)
                best_action = None
                state = mock_env.compressed_state_rep()
                best_value = float('-inf')
                allowed = QLearning.allowed_actions(state)
                for action in allowed:
                    if QLearning.learnQ(state, action, values) > best_value:
                        best_value = QLearning.learnQ(state, action, values)
                        best_action = action
                state_matrix[i][j] = round(best_value, 1)

        state_matrix = np.array(state_matrix)
        plt.imshow(state_matrix, cmap='viridis', origin='lower')
        plt.colorbar()
        plt.xlabel('Column')
        plt.ylabel('Row')
        plt.title('State Values')
        plt.show()
