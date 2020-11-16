import rasa , os , shutil
   
rasapath = rasa.__file__[:-11] + "nlu/utils/hugging_face/"

dir_path = os.path.dirname(os.path.realpath(__file__)) + "/hugging_face/"
shutil.rmtree(rasapath)
shutil.copytree(dir_path,rasapath)
print("Done!")


