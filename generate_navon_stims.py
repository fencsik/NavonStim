#!/usr/bin/env python3

import os
import sys
sys.path.append("../")

import string
from PIL import Image, ImageDraw, ImageFont, ImageOps
import numpy as np
import matplotlib.pyplot as plt
import math
import cmath
import random
import pdb

font_path = os.path.join('/System', 'Library', 'Fonts', 'Monaco.ttf')
global_font_index = 0 # 0 is usually regular, 1 bold
local_font_index = 0
global_font_size = 300
local_font_size = 18
local_step_size_factor = [1.15, 1.35] # x, y
image_size = 360
image_bg = (255, 255, 255)
transparent = False
progress_bar = False

def polar_to_cartesian(r, phi):
    x = r * np.cos(phi)
    y = r * np.sin(phi)
    return x, y

def make_dirs(dirs):
    # dirs is a list
    for d in dirs:
        if not os.path.isdir(d):
            os.makedirs(d)

def letter_to_shifted_masks(letter, im_size=image_size, font_size=global_font_size,
                            font_path=font_path):
    image = Image.new("RGB", (im_size, im_size), image_bg)
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype(font_path, font_size, index=global_font_index)
    box = draw.textbbox([0, 0], letter, font=font, anchor='lt')
    w = box[2] - box[0]
    h = box[3] - box[1]
    centered_x, centered_y = ((im_size - w)/2, 0) # really, upper left that will produce a centered letter
    
    masks = []

    r = 0
    phi = np.random.uniform(0, 2*math.pi)
    shift_x, shift_y = map(int, map(round, polar_to_cartesian(r, phi)))
    x, y = centered_x + shift_x, centered_y + shift_y
    image = Image.new("RGB", (im_size, im_size), image_bg)
    draw = ImageDraw.Draw(image)
    draw.text((x, y), letter, font=font, fill="black")
    masks.append(image)

    return masks

def render(mask, fill_letter, savename, savedir, font_size=local_font_size,
           font_path=font_path):
    mask = np.array(mask)
    image = Image.new("RGB", (mask.shape[0], mask.shape[1]), image_bg)
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype(font_path, font_size, index=local_font_index)
    box = draw.textbbox([0, 0], fill_letter, font=font, anchor='lt')
    step_size_x = int(round((box[2] - box[0]) * local_step_size_factor[1]))
    step_size_y = int(round((box[3] - box[1]) * local_step_size_factor[0]))

    for x in np.arange(0, mask.shape[0], step_size_x):
        for y in np.arange(0, mask.shape[1], step_size_y):
            if np.array_equal(mask[x, y, :], [0, 0, 0]):
                draw.text((y, x), fill_letter, font=font, fill="black")

    if transparent:
        transparency = image_bg
    else:
        transparency = None

    image.save(os.path.join(savedir, "{}.png".format(savename)),
                   format='PNG',
                   transparency=transparency)

# Print iterations progress
def printProgressBar (
        iteration, total, prefix = '', suffix = '',
        decimals = 1, length = 100,
        fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()

def make_stims(navon_savedir="navon_stims"):
    make_dirs([navon_savedir])

    # assemble list of upper-case letters and digits
    all_letters = list(string.ascii_uppercase)
    all_letters.extend(list(string.digits))
    # remove the awkward ones
    for letter in ('I', 'Q', '0', '1'):
        all_letters.remove(letter)
    all_letters = ['4', '8', 'H', 'M', 'S', 'X']

    n_steps = len(all_letters)**2
    step = 0

    print('Generating {} images...'.format(n_steps))
    for shape_letter in all_letters:
        masks = letter_to_shifted_masks(shape_letter)
        for fill_letter in all_letters:
            for i, mask in enumerate(masks):
                savename = "{}-{}".format(shape_letter, fill_letter)
                render(mask, fill_letter, savename, navon_savedir)
                step += 1
                if progress_bar:
                    printProgressBar(step, n_steps, length=64)
    if not progress_bar:
        print('done')

if __name__=="__main__":
    make_stims("navon")


