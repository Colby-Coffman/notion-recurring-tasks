#!/usr/bin/env python3

import datetime as dt
import notion
import time

logfile = '/home/colby_coffman/Code/Workspace/Notion/log.txt'

items = notion.getItems()
while True:
	for item in items:
		item.checkUpdate()
		if item.should_add:
			item.add()
	time.sleep(60)
