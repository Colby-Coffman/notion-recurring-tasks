import datetime
import subprocess
import urllib.request
import time
import os
import pathlib
import sys
import inspect

logfile = '/home/colby_coffman/Code/Workspace/Notion/log.txt'

class Item:
	def __init__(self, name, priority, frequency, next_edit):
		self.should_add = False
		self.name = name
		self.priority = priority
		self.frequency = frequency
		self.next_edit = datetime.datetime.fromisoformat(next_edit)
		self.checkUpdate()

	def checkUpdate(self):
		if datetime.datetime.now() > self.next_edit:
				self.should_add = True
				self.newNE()

	def newNE(self):
		self.next_edit = datetime.datetime.now()
		self.next_edit = self.next_edit.replace(hour=4, minute=0, second=0, microsecond=0)
		if self.frequency[0] == "ED":
			one_day = datetime.timedelta(1)
			self.next_edit = self.next_edit + one_day
		if self.frequency[0] == 'W':
			today_weekday = self.next_edit.weekday()
			days = []
			for char in self.frequency[1]:
				if char == 'M':
					days.append(0)
				elif char == 't':
					days.append(1)
				elif char == 'W':
					days.append(2)
				elif char == 'T':
					days.append(3)
				elif char == 'F':
					days.append(4)
				elif char == 'S':
					days.append(5)
				elif char == 's':
					days.append(6)
			daysuntil = 0
			while True:
				if today_weekday == 7:
					today_weekday = 0
				if today_weekday in days:
					break
				today_weekday += 1
				daysuntil += 1
			if daysuntil == 0:
				if len(days) == 1:
					daysuntil = 7
				else:
					for i in range(len(days)):
						if i == (len(days) - 1):
							daysuntil = days[i] - days[0]
						elif today_weekday == days[i]:
							daysuntil = days[i + 1] - days[i]
							break
							
			self.next_edit = self.next_edit.replace(hour=4, minute=0, second=0, microsecond=0) + datetime.timedelta(daysuntil)
			

	def add(self):
		date = str(datetime.datetime.now().date())
		while not checkInternet():
		#	with open(logfile, "a") as file:
				#file.write("No internet {}\n".format(datetime.datetime.now())) implement again when you can control log file size
			time.sleep(5)
		addItem(self.name, self.priority, date)
		self.should_add = False
		updateNE(self)
		

def getItems():
	items = []
	with open("/home/colby_coffman/Code/Workspace/Notion/Notion Data", "r") as file:
		lines = file.readlines()
		for line in range(2, len(lines)):
			data = list(lines[line])
			data.pop()
			data = ''.join(data).split(';')
			frequency = None
			frequency_data = data[2].split(':')
			if frequency_data[0] == 'ED':
				frequency = ('ED',)
			elif frequency_data[0] == 'W':
				frequency = ('W',frequency_data[1])
			next_edit = None
			next_edit_data = data[3].split(' ')
			today = datetime.datetime.now()
			if len(next_edit_data) == 1:
				if frequency[0] == 'ED':
					next_edit = str(today)
				if frequency[0] == 'W':
					today_weekday = today.weekday()
					days = []
					for char in frequency[1]:
						if char == 'M':
							days.append(0)
						elif char == 't':
							days.append(1)
						elif char == 'W':
							days.append(2)
						elif char == 'T':
							days.append(3)
						elif char == 'F':
							days.append(4)
						elif char == 'S':
							days.append(5)
						elif char == 's':
							days.append(6)
					daysuntil = 0
					while True:
						if today_weekday == 7:
							today_weekday = 0
						if today_weekday in days:
							break
						today_weekday += 1
						daysuntil += 1
					next_edit = str(today.replace(hour=4, minute=0, second=0, microsecond=0) + datetime.timedelta(daysuntil))
					updateNE(Item(data[0], data[1], frequency, next_edit))
			else:
				next_edit = next_edit_data[1] + ' ' +  next_edit_data[2]
			item = Item(data[0], data[1], frequency, next_edit)
			items.append(item)
	return items

def updateNE(item):
	with open("/home/colby_coffman/Code/Workspace/Notion/Notion Data", "r") as file:
		lines = file.readlines()
		line = 0
		char = 0
		for i in range(2, len(lines)):
			data = lines[i].split(';')
			if data[0] == item.name:
				line = i
				break
		temp = list(lines[line])
		temp.pop()
		temp = ''.join(temp).split(';')
		temp_ne = temp[3].split(' ')
		if len(temp_ne) == 1:
			temp_ne.append(str(item.next_edit))
		else:
			temp_ne.pop()
			temp_ne[1] = str(item.next_edit)
		temp.pop()
		temp = ';'.join(temp) + ';' +  ' '.join(temp_ne) + '\n'
		lines[line] = temp
	with open("/home/colby_coffman/Code/Workspace/Notion/Notion Data", "w") as file:
		file.write("".join(lines))

def addItem(name: str, priority: str, date: str):
	curframe = inspect.currentframe()
	calframe = inspect.getouterframes(curframe, 2)
	if checkInternet():
		index = '/home/colby_coffman/Code/Workspace/Notion/index.js'
		node = '/home/colby_coffman/.nvm/versions/node/v16.18.0/bin/node'
		args = [node, index, name, priority, date]
		subprocess.run(args)
		return
	else:
		return

def checkInternet(host='http://google.com'):
	try:
		urllib.request.urlopen(host)
		return True
	except:
		return False
