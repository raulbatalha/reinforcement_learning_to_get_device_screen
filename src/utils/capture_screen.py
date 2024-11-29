#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 21:12:51 2023
@author: Raul Batalha
@email: raul.batalha@hotmail.com
"""

import subprocess


class CaptureScreen:
    def __init__(self, touchable_areas):
        self.touchable_areas = touchable_areas
        self.screen_width = 0
        self.screen_height = 0
        self.max_touch_x = 65535
        self.max_touch_y = 65535
        self.get_screen_dimensions()
        
    def get_touch_coordinates(self):
        adb_command = 'adb shell getevent -l'
        process = subprocess.Popen(adb_command, shell=True, stdout=subprocess.PIPE)

        for line in iter(process.stdout.readline, b''):
            line = line.decode('utf-8').strip()
            if 'ABS_MT_POSITION_X' in line:
                x = int(line.split(' ')[-1], 16)
            elif 'ABS_MT_POSITION_Y' in line:
                y = int(line.split(' ')[-1], 16)
                return x, y
        return None

    def get_screen_dimensions(self):
        adb_command = 'adb shell wm size'
        process = subprocess.Popen(adb_command, shell=True, stdout=subprocess.PIPE)
        output = process.stdout.readline().decode('utf-8').strip()
        dimensions = output.split(' ')[-1].split('x')
        self.screen_width = int(dimensions[0])
        self.screen_height = int(dimensions[1])

    def set_touch(self):
        coordinates = self.get_touch_coordinates()
        if coordinates:
            x, y = coordinates
            adjusted_x = x * (self.screen_width - 1) // self.max_touch_x
            adjusted_y = y * (self.screen_height - 1) // self.max_touch_y

            print(f'Touch coordinates: x={adjusted_x} y={adjusted_y}')
            touch_result = self.check_touch_location(adjusted_x, adjusted_y)
            print(f'Touch coordinates valid: {touch_result}')
        else:
            print('No touch coordinates found!')

    def check_touch_location(self, x, y):
        for area in self.touchable_areas:
            if self.within_touchable_area(x, y, area):
                return True
        return False

    def within_touchable_area(self, x, y, area):
        if 'left' in area and 'top' in area and 'right' in area and 'bottom' in area:
            left = area['left']
            top = area['top']
            right = area['right']
            bottom = area['bottom']
            if left <= x <= right and top <= y <= bottom:
                return True
        return False
    
    def save_file_txt(self):
        path = 'files/touch_areas.txt'
        with open(path, "w") as file:
            for touch_area in self.touchable_areas:
                file.write(f"Name: {touch_area['name']}\n")
                file.write(f"Coordinates: ({touch_area['x1']}, {touch_area['y1']}, {touch_area['x2']}, {touch_area['y2']})\n")
                file.write("\n")
        print("Data save in touch_areas.txt")