from subprocess import call
from bokeh.io import curdoc, output_notebook, show
from bokeh.layouts import gridplot, widgetbox, layout, gridplot
from bokeh.models.widgets import Button, Paragraph
from bokeh.plotting import figure, curdoc
from bokeh.models import Div, ColumnDataSource, Range1d
import dashboard

class ButtonHelper(object):

	def run_model(self, bat_name):
		if bat_name:
			call(["dir", "&&","cd", "pet_dash", "&&", "cd", "static", "&&", "cd", "model", "&&", bat_name, "&&", "dir"], shell=True)
		else:
			analyzer_page = dashboard.analyzer()
			print("post analyzer")
			curdoc().clear()
			print("clear")
			curdoc().add_root(analyzer_page)

		#print(call(["dir && cd pet_dash/static/model && dir"], shell=True))

		#print(call(["dir && cd pet_dash/static/model && dir && "+bat_name], shell=True))
		#print(call(["DIR"], shell=True))
		#call([bat_name], shell=True)

	def __init__(self, button_name, description, bat_string, photo_dir):
		self.button = Button(label=button_name, button_type="success")
		self.button.on_click(lambda :  self.run_model(bat_string))

		self.desc = Paragraph(text=description)
		self.photo = figure(plot_width = 300, plot_height = 250, title="", toolbar_location=None)
		sim_src = ColumnDataSource(dict(url = [photo_dir]))
		self.photo.toolbar.logo = None 
		self.photo.toolbar_location = None
		self.photo.x_range=Range1d(start=0, end=1)
		self.photo.y_range=Range1d(start=0, end=1)
		self.photo.xaxis.visible = None
		self.photo.yaxis.visible = None
		self.photo.xgrid.grid_line_color = None
		self.photo.ygrid.grid_line_color = None
		self.photo.image_url(url='url', x=0.05, y = 0.85, h=0.7, w=0.9, source=sim_src)
		self.photo.outline_line_alpha = 0





def set_executables():
	desc_sim = "Run the demand in this enviorment to modify variables or to understand specific behavior."
	name_sim = 'Simulation'
	batch_sim = r'Simulation.bat'
	photo_sim = r'pet_dash/static/Simulation.png'
	
	simulation = ButtonHelper(name_sim, desc_sim, batch_sim, photo_sim)

	desc_opt ="Run the demand in this enviorment to get the model that optimize the production."
	name_opt = "Optimization"
	batch_opt = r'Optimization.bat'
	photo_opt = r'model_executables/static/optimizer.png'

	optimize = ButtonHelper(name_opt, desc_opt, batch_opt, photo_opt)
	
	desc_an = "Analyze the last output of the program, whether it was done via optimizer or simulation."
	name_an = "Analyze"
	batch_an = ''
	photo_an = r'model_executables/static/optimizer.png'
	analyze = ButtonHelper(name_an, desc_an, batch_an, photo_an)

	#curdoc().clear()
	button_grid = gridplot([

		[simulation.photo, optimize.photo, analyze.photo],
	  	[simulation.button, optimize.button, analyze.button],
	  	[simulation.desc, optimize.desc, analyze.desc]
	], toolbar_location=None)
	return button_grid
	#curdoc().add_root(button_grid)