# Navon dataset from "The Origins and Prevalence of Texture Bias in Convolutional Neural Networks"
	
This repository was forked from code use to develop the Navon dataset used in the paper ["The Origins and Prevalence of Texture Bias in Convolutional Neural Networks"](https://arxiv.org/abs/1911.09071) by Katherine Hermann, Ting Chen, and Simon Kornblith. See the original repository for more information.

I modified the code to create entirely upright stimuli, make the font, size, and spacing more centralized, and enable image files with a transparent background. I also updated some code because ImageDraw.Draw no longer has a textsize method, at least in the Pillow fork of PIL.
	
`generate_navon_stims.py` is the script used to generate the stimuli. It will create a directory and store image files in them.
