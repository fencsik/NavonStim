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

font_path="/System/Library/Fonts/Supplemental/Arial Bold.ttf"
global_font_size = 200
local_font_size = 8
image_size = 224

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
    image = Image.new("RGB", (im_size, im_size), "white")
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype(font_path, font_size)
    box = draw.textbbox([0, 0], letter, font=font, anchor='lt')
    w = box[2] - box[0]
    h = box[3] - box[1]
    centered_x, centered_y = ((im_size - w)/2, 0) # really, upper left that will produce a centered letter
    
    masks = []

    r = 0
    phi = np.random.uniform(0, 2*math.pi)
    shift_x, shift_y = map(int, map(round, polar_to_cartesian(r, phi)))
    print("r = {}, shift = ({}, {})".format(r, shift_x, shift_y))
    x, y = centered_x + shift_x, centered_y + shift_y
    image = Image.new("RGB", (im_size, im_size), "white")
    draw = ImageDraw.Draw(image)
    draw.text((x, y), letter, font=font, fill="black")
    masks.append(image)

    return masks

def render(mask, fill_letter, savename, savedir, font_size=local_font_size,
           font_path=font_path):
    mask = np.array(mask)
    image = Image.new("RGB", (mask.shape[0], mask.shape[1]), "white")
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype(font_path, font_size)
    box = draw.textbbox([0, 0], fill_letter, font=font, anchor='lt')
    step_size  = max([box[2] - box[0], box[3] - box[1]])

    for x in np.arange(0, mask.shape[0], step_size):
        for y in np.arange(0, mask.shape[1], step_size):
            if np.array_equal(mask[x, y, :], [0, 0, 0]):
                draw.text((y, x), fill_letter, font=font, fill="black")

    # fix to no rotation
    rotation_deg = 0

    image = image.rotate(rotation_deg, fillcolor="white", resample=Image.BILINEAR)    
    image.save(os.path.join(savedir, "{}.png".format(savename)))

def make_stims(navon_savedir="navon_stims"):
    make_dirs([navon_savedir])

    #all_letters = list(string.ascii_uppercase)
    all_letters = ['A', '3']

    make_dirs([os.path.join(navon_savedir, shape_letter) 
                     for shape_letter in all_letters])

    for fill_letter in all_letters:
        for shape_letter in all_letters:
            masks = letter_to_shifted_masks(shape_letter)
            for i, mask in enumerate(masks):
                savename = "{}_{}-{}".format(shape_letter, i, fill_letter)
                render(mask, fill_letter, savename, 
                       os.path.join(navon_savedir, shape_letter))


if __name__=="__main__":
    make_stims("navon")


