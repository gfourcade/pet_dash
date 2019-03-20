import pandas as pd
import numpy as np
from pet_perfect.sku import *
from pet_perfect.bin_order import fill_bins
from pet_perfect.cf_order import fill_cf_orders
from pet_perfect.fg_order import fill_fg_orders
from pet_perfect.master_formula import *
from pet_perfect.utils import *
import matplotlib.pyplot as plt
from bokeh.transform import linear_cmap
from bokeh.io import curdoc, output_notebook, show
from bokeh.plotting import figure
from bokeh.layouts import gridplot, widgetbox, layout, column, row
from bokeh.models import ColumnDataSource, Plot, Grid, LinearAxis, Legend, CDSView, BooleanFilter
from bokeh.models import HoverTool
from bokeh.models import CustomJS, Div, Button
from bokeh.models.glyphs import Rect
from bokeh import events
import datetime

def update_mf(mfs, skus, cf_orders, bins, bins_waste):
		for mf in mfs:
			scode = mfs[mf].skus[0]
			for cf in filter(lambda x: x in cf_orders, skus[scode].get_cfs()):
				for order in cf_orders[cf]:
					order.update_mf(mf)
				for b in bins:
					if bins[b].code == cf:
						bins[b].update_mf(mf)
		mfs = []
		for row, val in  out_bins_waste.iterrows():
			if(val["cf code"] != "None"):
				mf = cf_orders[val["cf code"]][0].master_code
				mfs.append(mf)
			else:
				mfs.append("None")
		out_bins_waste["master_code"] = mfs
	
def analyzer():
	# INPUT
	breakout_excel = pd.read_excel("pet_dash/static/model/Breakout.xlsx",sheet_name=None)
	units_pallet = breakout_excel.get("Units per Pallet")
	breakout = breakout_excel.get("Breakout")
	rates_umbra = breakout_excel.get("Umbra")
	rates_thiele = breakout_excel.get("Thiele")
	rates_parsons = breakout_excel.get("Parsons")
	rates_ptech = breakout_excel.get("Premier Tech")

	units_pallet.set_index('Item Number', inplace = True)
	breakout.set_index('Item Number', inplace = True)
	rates_umbra.set_index('UPC', inplace = True)
	rates_ptech.set_index('UPC', inplace = True)
	rates_thiele.set_index('UPC', inplace = True)
	rates_parsons.set_index('UPC', inplace = True)


	demand_excel = pd.read_excel("pet_dash/static/model/Demand.xlsx",sheet_name=None)
	demand = demand_excel.get("Demand")
	demand.set_index('item number', inplace = True)

	# OUTPUT
	excel_source2 = pd.read_excel("pet_dash/static/model/Output.xlsx",sheet_name=None)
	out_cf = excel_source2.get("out_cf")
	#out_cf_orders = excel_source2.get("out_cf_orders")
	out_fg = excel_source2.get("out_fg")
	out_packline = excel_source2.get("out_packline")
	out_bins = excel_source2.get("out_bins")
	out_bins_waste = excel_source2.get("out_bin_wasting")
	print("read the excel files")
	print(out_bins_waste.columns)
	##
	#THIS NEEDS TO BE RE ADDED, WHY WAS IT DELETED?
	##
	#idx_to_drop = out_bins_waste[out_bins_waste["cf code"] == "None"].index
	 
	# Delete these row indexes from dataFrame
	#out_bins_waste.drop(idx_to_drop , inplace=True)

	out_cf.set_index('cf code', inplace = True)
	#out_cf_orders.set_index('code', inplace = True)
	out_fg.set_index('sku', inplace = True)
	#out_packline.set_index('line', inplace = True)
	#out_bins.set_index('bin', inplace = True)#
	print("Re index everything")
	
	      
	big_cf_orders = fill_cf_orders(out_cf)
	big_fg_orders = fill_fg_orders(out_fg, breakout)
	big_skus = fill_skus(big_fg_orders, breakout, demand, rates_umbra,rates_parsons, rates_ptech, rates_thiele)
	big_mfs = fill_mf(big_skus, breakout)
	big_bins = fill_bins(out_bins, out_bins_waste)

	update_mf(big_mfs, big_skus, big_cf_orders, big_bins, out_bins_waste)

	print("Objects are ready")
	occupation_fig = start_occupation_graphics(big_cf_orders, big_bins, big_fg_orders, out_bins_waste)

	equals_demand = get_equals(big_skus, big_mfs,  simple_demand_equality)
	equals = get_equals(big_skus, big_mfs,  simple_equality)
	dic_mf_similarities ={"Simple equality":equals, "Simple equality filter by demand":equals_demand}


	print("ocuppation is ready")
	sim_widget = add_mf_similarities_widgetobox(dic_mf_similarities)
	#curdoc().clear()
	print("similarity widget ready")
	occupation_layout = layout([
	  	[occupation_fig, sim_widget]
	])#, sizing_mode='stretch_both')
	return occupation_layout
	#curdoc().add_root(occupation_layout)

