import sys
sys.path.insert(0, "C:\\Users\\ite\\Documents\\GitHub\\pet_dash\\model_executables")
from model_executables import set_executables
from bokeh.plotting import figure, curdoc
curdoc().clear()

button_grid = set_executables()
curdoc().add_root(button_grid)
