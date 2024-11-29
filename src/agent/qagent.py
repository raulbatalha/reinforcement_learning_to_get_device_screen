#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 21:12:51 2023
@author: Raul Batalha
@email: raul.batalha@hotmail.com
"""

import pickle
import random

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from src.environment.env_screen import EnvScreen
from qlearning import QLearning
from src.utils.util import Grafic


class QAgent:
    """
    QAgent class for training and running Q-learning algorithm.
    """
    
    def __init__(self, gama = 0.9,alpha = 0.5, episodes = 300, number_metrics = 10, actions = ['UP', 'DOWN', 'RIGHT', 'LEFT']):
        """
        Initialize QAgent with specified parameters.

        Args:
            gamma (float): Discount factor for future rewards.
            alpha (float): Learning rate for updating Q-values.
            episodes (int): Number of episodes for training.
            number_metrics (int): Number of metrics to calculate average rewards.
            actions (list): List of possible actions.
        """
        
        self.values = {}
        self. gama = gama
        self.alpha = alpha
        self.episodes = episodes
        self.number_metrics = number_metrics
        self.env = EnvScreen(dimensions=[EnvScreen.width_cols, EnvScreen.height_rows])
        self.actions = actions

    def run_training(self, save_to='models/training_model.npy'):
        """
        Run Q-learning training.

        Args:
        
        save_to (str): File path to save the trained model.
        
        """
        
        self.env.reset()
        rewards_list = []
        steps_list = []
        step = 0
        result_path = []
        for episode in range(self.episodes):
            self.env.reset()
            position, goal_position = QLearning.unique_starts(episode)
            start_position = position
            self.env.position = np.asarray(position)
            self.env.goal_position = np.asarray(goal_position)
            current_state = self.env.compressed_state_rep()
            use_epsilon = 0.1
            if episode > 200:
                use_epsilon = 0.0
            action, action_v = QLearning.policy(self.values, current_state, epsilon=use_epsilon, verbose=(episode == 299))
            total_reward = 0
            deltas = []

            while not self.env.over:
                if episode == 299:
                    print(f'state: \n{current_state}')
                    print(f'action chosen: {(action, action_v)}')
                    result_path.append(action)
                step += 1
                reward = self.env.move(action)
                total_reward += reward
                next_state = self.env.compressed_state_rep()
                next_action, next_action_v = QLearning.policy(self.values, next_state, epsilon=use_epsilon, verbose=(episode == 299))
                if self.env.over:
                    next_action_v = 100
                    total_reward += 100
                delta = next_action_v * self.gama + reward - action_v
                deltas.append(delta)
                new_value = action_v + delta * self.alpha
                QLearning.update(current_state, action, new_value, self.values)
                current_state = next_state
                action = next_action
                action_v = next_action_v
            rewards_list.append(total_reward)
            steps_list.append(step)

            if episode > self.number_metrics:
                print(f'episode: {episode} total_reward: {total_reward} agg: {sum(rewards_list[-self.number_metrics:]) / self.number_metrics} ')
                print(f'original reward: {sum(rewards_list[:self.number_metrics]) / self.number_metrics} ')
                print(f'explored states: {len(self.values.keys())} ')
                print(f'average delta: {sum(deltas) / len(deltas)}')
                print(f'steps: {step}')
                print(f'difference: {start_position} {goal_position}')
                QLearning.state_values(self.values)
                
        print(self.values)
        path_file = './files/steps_by_steps.txt'
        with open(path_file, 'w') as f:
            output = str(steps_list) + '\n' + str(self.values)
            f.write(output)

        self.env.reset()
        position, goal_position = QLearning.unique_starts(episode)
        start_position = position
        self.env.position = np.asarray(position)
        self.env.goal_position = np.asarray(goal_position)
        boards = self.env.path(result_path)
        frames = [Image.fromarray(frame, 'RGB') for frame in boards]
        path_file = 'media/result.gif'
        Grafic.create_gif(frames, path_file)
        
        with open(save_to, 'wb') as handle:
            pickle.dump(self.values, handle, protocol=pickle.HIGHEST_PROTOCOL)
            
    def plot_state_values(values):
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
        state_matrix = np.array(state_matrix)
        
        plt.imshow(state_matrix, cmap='viridis', origin='lower')
        plt.colorbar()
        plt.xlabel('Column')
        plt.ylabel('Row')
        plt.title('State Values')
        plt.show()