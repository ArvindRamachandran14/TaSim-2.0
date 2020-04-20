

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

		root = ET.fromstring(line)

		CC_temp.append(float(root.find('CC_T1').text))

		SC_temp.append(float(root.find('SC_T1').text))

		DPG_temp.append(float(root.find('DPG_T1').text))

		DateTime.append(root.find('time').text)

		Time.append(((datetime.strptime(DateTime[-1], "%Y-%m-%d %H:%M:%S.%f") - datetime.strptime(DateTime[0], "%Y-%m-%d %H:%M:%S.%f")).total_seconds())/60.0)

	plt.plot(Time, CC_temp, 'b^', label='Conditioning Chamber Temperature')

	plt.plot(Time, SC_temp, 'ro', label='Sample Chamber Temperature')

	plt.plot(Time, DPG_temp, 'k-', label='Dew point generator Temperature')

	plt.title(file.name.split('.xml')[0].replace("_", " "))

	plt.legend()

	plt.xlabel('Time (min)')

	plt.ylabel('Temperature (\u2103)')

	plt.savefig(file.name.split('.xml')[0]+'.pdf')

	plt.show()

file = open('SC_TSet_tracking_bypass_ON.xml', 'r')

plot_temperatures(file)

