# requires pew to be installed with pip (virtual env stuff)
pip install pew
# THIS REQUIRES TENSORFLOW 1.15 (or 1.13.1 if you have a lower-end gpu), CUDA 10.0, AND CUDNN 10.0
pew new --python=3.7 -i discord.py -i tensorflow-gpu==1.15 -i gpt-2-simple ConvoBot