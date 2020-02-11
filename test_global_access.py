import globals as g

from test_class import test_class

import json


with open(g.cfgFile, 'r') as fCfg :
	config = json.loads(fCfg.read())        # Read config file
	g.initialize(config)              # Initialize the globals



testclass = test_class()