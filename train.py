import tensorflow as tf
import gpt_2_simple as gpt2
import os
import requests

main_dataset = "complete-data"
chat_dir = "chats"
model_name = "124M"

# downloads gpt-2 124M model if we don't have it currently installed (IT'S FAT AT AROUND 498MB, MAKE SURE YOU HAVE SPACE!)
if not os.path.isdir(os.path.join("models", model_name)):
	print(f"Downloading {model_name} model...")
	gpt2.download_gpt2(model_name=model_name)   # model is saved into current directory under /models/124M/

sess = gpt2.start_tf_sess()

# start train
gpt2.finetune(sess, main_dataset, accumulate_gradients=1, use_memory_saving_gradients=True, model_name=model_name, steps=10000) # steps is max number of training steps

print(gpt2.generate(sess))