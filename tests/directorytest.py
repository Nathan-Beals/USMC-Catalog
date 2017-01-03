import os

this_dir = os.path.dirname(os.path.abspath(__file__))
vehicles_dir = this_dir + "/vehicles/"

print(os.listdir('../vehicles'))

print str(vehicles_dir)