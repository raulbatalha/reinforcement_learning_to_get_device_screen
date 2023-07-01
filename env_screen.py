#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 21:12:51 2023
@author: Raul Batalha
@email: raul.batalha@hotmail.com
"""

import numpy as np

from util import Grafic


class EnvScreen:
	height_rows=15
	width_cols=10
	goal=[9, 4]
 
	def __init__(self,  goal_position=np.asarray([0, 0]), initial_position=np.asarray([3, 3]),dimensions=[64, 64], blocked=[]):
		self.goal_position = goal_position
		self.initial_position = initial_position
		self.width = dimensions[0]
		self.height = dimensions[1]
		self.position = initial_position
		self.blocked = blocked
		self.blocked_map = {str(k): True for k in blocked}
		self.total_reward = 0
		self.over = False
		self.rewards = []
		self.grafic = Grafic()
		self.visible_mask = np.zeros(shape=[self.height, self.width, 3], dtype=np.uint8)
		i, j = self.position
		for h in range(i - 1, i + 2):
			for w in range(j - 1, j + 2):
				if self.bound_check([h, w]):
					self.visible_mask[h][w] = [1, 1, 1]

	def reset(self):
		self.goal_position = np.random.randint(0, self.width, [2], dtype=np.int32)
		self.goal_position %= [self.height, self.width]
		self.position = np.random.randint(0, self.width, [2], dtype=np.uint8)
		self.rewards = []
		self.total_reward = 0
		self.over = False
		self.visible_mask = np.zeros(shape=[self.height, self.width, 3], dtype=np.uint8)
		i, j = self.position
		for h in range(i - 1, i + 2):
			for w in range(j - 1, j + 2):
				if self.bound_check([h, w]):
					self.visible_mask[h][w] = [1, 1, 1]
	
	def underlying_scene(self):
		underlying_scene = np.ones(shape=[self.height, self.width, 3], dtype=np.uint8) * 255
		if self.bound_check(self.position):
			underlying_scene[self.position[0] % self.height][self.position[1] % self.width] = self.grafic.PLAYER_COLOR

		# if len(self.goal_position.shape) > 1:
		# 	goal_x = self.goal_position[0, 0] % self.height_rows
		# 	goal_y = self.goal_position[0, 1] % self.width_cols
		# else:
			goal_x = self.goal_position[0] % self.height_rows
			goal_y = self.goal_position[1] % self.width_cols

		if goal_x < self.height and goal_y < self.width:
			underlying_scene[goal_x][goal_y] = self.grafic.GOAL_COLOR
		for blocked_square in self.blocked:
			underlying_scene[blocked_square[0]][blocked_square[1]] = self.grafic.BLOCKED_COLOR
		return underlying_scene

	def visible_scene(self):
		underlying_scene = self.underlying_scene()
		return underlying_scene * self.visible_mask

	def picture(self, fog = False):
		IMG_SCALE_FACTOR = 16
		scene = self.visible_scene() if fog else self.underlying_scene()
		scene = scene.repeat(IMG_SCALE_FACTOR, axis=0).repeat(IMG_SCALE_FACTOR, axis=1)
		return scene

	def move(self, direction):
		assert direction in ['UP','DOWN','RIGHT','LEFT']
		new_position = self.position + self.grafic.direction_to_vector[direction]
		reward = 0
		old_position = self.position

		if self.bound_check(new_position) and (not self.bump(new_position)):
			self.position = new_position
		else:
			reward = -1
		if (self.position[0] == self.goal_position[0]) and (self.position[1] == self.goal_position[1]):
			reward = 10
			self.over = True
		self.rewards.append(reward)
		self.total_reward += reward

		i, j = self.position
		for h in range(i-1, i+2):
			for w in range(j-1, j+2):
				if self.bound_check([h,w]):
					self.visible_mask[h][w] = [1,1,1]
		return reward*1.0

	def bump(self, coordinates):
		x, y = coordinates
		return self.blocked_map.get(str([x, y]), False)

	def venture(self, direction):
		assert direction in ['UP','DOWN','RIGHT','LEFT']
		new_position = self.position + self.grafic.direction_to_vector[direction]
		next_state_string = ''
		print(self.position)
		print('moves to')
		print(new_position)
		if self.bound_check(new_position):
			new_scene = self.visible_scene()
			new_scene[self.position[0]][self.position[1]] = self.grafic.EMPTY_COLOR
			print(new_scene[new_position[0]][new_position[1]])
			print(new_scene[self.position[0]][self.position[1]])
			i, j = new_position
			for h in range(i-1, i+2):
				for w in range(j-1, j+2):
					if self.bound_check([h,w]):
						new_scene[h][w] = self.grafic.EMPTY_COLOR
						if self.goal_position[0] == h and self.goal_position[1] == w:
							new_scene[h][w] = self.grafic.GOAL_COLOR
			new_scene[new_position[0]][new_position[1]] = self.grafic.PLAYER_COLOR
			print('scene:')
			print(new_scene)
			next_state_string = self.state_string(new_scene)
		else:
			next_state_string = self.state_string(self.visible_scene())
		return next_state_string

	def state_string(self, visible_scene):
		string_representation = ''
		for i in range(self.height):
			for j in range(self.width):
				string_representation += self.grafic.color_to_char(visible_scene[i][j])
			string_representation+='\n'
		return string_representation

	def current_state_string(self):
		visible_scene = self.underlying_scene()
		string_representation = ''
		EnvScreen.height_rows, EnvScreen.width_cols, _ = visible_scene.shape

		for i in range(EnvScreen.height_rows):
			for j in range(EnvScreen.width_cols):
				if i < EnvScreen.height_rows and j < EnvScreen.width_cols:
					string_representation += self.grafic.color_to_char(visible_scene[i][j])
			string_representation += '\n'
		return string_representation

	def compressed_state_rep(self):
		string_rep = self.current_state_string()
		return string_rep

	def path(self, steps):
		pictures = [self.picture()]
		for step in steps:
			self.move(step)
			pictures.append(self.picture())
		return pictures

	def bound_check(self, coordinates):
		x, y = coordinates
		return (x >= 0 and x < self.height) and (y >= 0 and y < self.width)