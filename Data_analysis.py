

# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET

import matplotlib.pyplot as plt

from datetime import datetime

import datetime as dt


SC_temp = []

DateTime = []

Time = []

CC_temp = []

DPG_temp = []


def plot_temperatures(file):

	lines = file.readlines() 

	SC_temp = []

	DateTime = []

	Time = []

	CC_temp = []

	DPG_temp = []


	for line in lines:

		root = ET.fromstring(line) #parsing

		CC_temp.append(float(root.find('CC_T1').text)) #parsing

		SC_temp.append(float(root.find('SC_T1').text)) #parsing

		DPG_temp.append(float(root.find('DPG_T1').text)) #parsing

		DateTime.append(root.find('time').text) #parsing

		Time.append(((datetime.strptime(DateTime[-1], "%Y-%m-%d %H:%M:%S.%f") - datetime.strptime(DateTime[0], "%Y-%m-%d %H:%M:%S.%f")).total_seconds())/60.0) #take time difference from first data point and convert it to minutes

	plt.plot(Time, CC_temp, 'b^', label='Conditioning Chamber Temperature')

	plt.plot(Time, SC_temp, 'ro', label='Sample Chamber Temperature') 

	plt.plot(Time, DPG_temp, 'k-', label='Dew point generator Temperature')

	plt.title(file.name.split('.xml')[0].replace("_", " ")) #Grab file name and convert underscore to space

	plt.legend()

	plt.xlabel('Time (min)')

	plt.ylabel('Temperature (\u2103)')

	plt.savefig(file.name.split('.xml')[0]+'.pdf') #Grab file name to save figure

	plt.show()

file = open('SC_TSet_tracking_bypass_ON.xml', 'r') #Change file name to change plot

plot_temperatures(file)

