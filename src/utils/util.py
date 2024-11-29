#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 21:12:51 2023
@author: Raul Batalha
@email: raul.batalha@hotmail.com
"""

import subprocess
import xml.etree.ElementTree as ET

import matplotlib.pyplot as plt


class Grafic:
    GOAL_COLOR = [255, 0, 0]
    PLAYER_COLOR = [0, 0, 255]
    UNKNOWN_COLOR = [255, 0, 255]
    EMPTY_COLOR = [255, 255, 255]
    BLOCKED_COLOR = [1, 1, 1]
    direction_to_vector = {
        'UP': [-1, 0],
        'DOWN': [1, 0],
        'RIGHT': [0, 1],
        'LEFT': [0, -1]
    }

    @staticmethod
    def color_to_char(color):
        color = list(color)
        if color == Grafic.GOAL_COLOR:
            return 'G'
        if color == Grafic.PLAYER_COLOR:
            return 'P'
        if color == Grafic.UNKNOWN_COLOR:
            return 'U'
        if color == Grafic.EMPTY_COLOR:
            return 'W'
        if color == Grafic.BLOCKED_COLOR:
            return 'B'
        else:
            print('dead color found')
            return 'W'

    @staticmethod
    def create_gif(frames, path):
        frame_one = frames[0]
        frame_one.save(path, format="GIF", append_images=frames,save_all=True, duration=500, loop=0)
            
    @staticmethod
    def save_figure(state_matrix, save_path):
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.imshow(state_matrix, cmap='viridis', origin='lower')
        ax.set_xticks([])
        ax.set_yticks([])
        plt.savefig(save_path, bbox_inches='tight')
        plt.close(fig)

class WindowDump:
    @staticmethod
    def dump_window():
        path_file = 'files/uidump.xml'
        subprocess.run(["adb", "shell", "uiautomator", "dump", "/sdcard/uidump.xml"])
        subprocess.run(["adb", "pull", "/sdcard/uidump.xml", path_file])

    @staticmethod
    def parse_dump():
        tree = ET.parse('uidump.xml')
        root = tree.getroot()
        touchable_areas = []
        for node in root.iter():
            if 'class' in node.attrib and 'bounds' in node.attrib:
                class_name = node.attrib['class']
                bounds = node.attrib['bounds']
                bounds_parts = bounds.split('][')
                left, top = map(int, bounds_parts[0].strip('[').split(','))
                right, bottom = map(int, bounds_parts[1].strip(']').split(','))

                if class_name in ['Button', 'EditText', 'ImageView']:
                    touchable_areas.append({
                        'left': left,
                        'top': top,
                        'right': right,
                        'bottom': bottom
                    })
                return touchable_areas
        return touchable_areas
    
class TouchArea:
    @staticmethod
    def parse_bounds(bounds):
        values = bounds.replace("[", "").replace("]", ",").split(",")
        values = [int(value) for value in values if value.isdigit()]

        if len(values) == 4:
            return values
        elif len(values) == 2:
            x, y = values
            return [x, y, x, y]
        else:
            return None

    @staticmethod
    def parse_dump(file_path):
        tree = ET.parse(file_path)
        root = tree.getroot()

        touch_areas = []
        screen_width = 0
        screen_height = 0

        for node in root.iter("node"):
            if node.attrib.get("class") in ["android.widget.Button", "android.widget.EditText", "android.widget.ImageView"]:
                bounds = node.attrib.get("bounds")
                coordinates = TouchArea.parse_bounds(bounds)

                if coordinates:
                    x1, y1, x2, y2 = coordinates
                    touch_area = {
                        "name": node.attrib.get("text"),
                        "x1": x1,
                        "y1": y1,
                        "x2": x2,
                        "y2": y2
                    }
                    touch_areas.append(touch_area)

        dimensions_node = root.find('device')
        if dimensions_node is not None:
            dimensions = dimensions_node.attrib.get('display')
            if dimensions:
                screen_width, screen_height = map(int, dimensions.split('x'))
        return touch_areas, screen_width, screen_height