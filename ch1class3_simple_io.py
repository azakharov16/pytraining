import os
import pickle

os.chdir('C://Users//andrey.zakharov//PycharmProjects//training//class3')

ratings_moodys = {'Russia': 'Ba1', 'USA': 'Aaa', 'UK': 'Aa2', 'Ukraine': 'Caa2', 'Switzerland': 'Aaa', 'Venezuela': 'Caa3',
'China': 'A1', 'Canada': 'Aaa', 'Netherlands': 'Aaa', 'Brazil': 'Ba2', 'France': 'Aa2', 'India': 'Baa2', 'Pakistan': 'B3'}

aggregation_moodys = {'Aaa': 'Aaa', 'Aa1': 'Aa', 'Aa2': 'Aa', 'Aa3': 'Aa', 'A1': 'A', 'A2': 'A', 'A3': 'A',
'Baa1': 'Baa', 'Baa2': 'Baa', 'Baa3': 'Baa', 'Ba1': 'Ba', 'Ba2': 'Ba', 'Ba3': 'Ba', 'B1': 'B', 'B2': 'B', 'B3': 'B', 
'Caa1': 'Caa-C', 'Caa2': 'Caa-C', 'Caa3': 'Caa-C', 'Ca1': 'Caa-C', 'Ca2': 'Caa-C', 'Ca3': 'Caa-C', 'C': 'Caa-C'}

pit_transitions_moodys = {
'Aaa': {'Aaa': 96.90, 'Aa': 2.94, 'A': 0.04, 'Baa': 0.09, 'Ba': 0.00, 'B': 0.00, 'Caa-C': 0.00, 'WR': 0.04, 'D': 0.00},
'Aa': {'Aaa': 3.46, 'Aa': 92.91, 'A': 2.11, 'Baa': 0.79, 'Ba': 0.12, 'B': 0.00, 'Caa-C': 0.00, 'WR': 0.6, 'D': 0.00},
'A': {'Aaa': 0.00, 'Aa': 4.17, 'A': 91.22, 'Baa': 3.25, 'Ba': 1.29, 'B': 0.07, 'Caa-C': 0.00, 'WR': 0.00, 'D': 0.00},
'Baa': {'Aaa': 0.00, 'Aa': 0.00, 'A': 6.10, 'Baa': 89.10, 'Ba': 4.24, 'B': 0.51, 'Caa-C': 0.04, 'WR': 0.00, 'D': 0.00},
'Ba': {'Aaa': 0.00, 'Aa': 0.00, 'A': 0.00, 'Baa': 8.32, 'Ba': 85.34, 'B': 5.33, 'Caa-C': 0.29, 'WR': 0.13, 'D': 0.58},
'B': {'Aaa': 0.00, 'Aa': 0.00, 'A': 0.00, 'Baa': 0.00, 'Ba': 4.76, 'B': 88.66, 'Caa-C': 3.47, 'WR': 0.41, 'D': 2.71},
'Caa-C': {'Aaa': 0.00, 'Aa': 0.00, 'A': 0.00, 'Baa': 0.00, 'Ba': 0.12, 'B': 17.83, 'Caa-C': 67.58, 'WR': 1.50, 'D': 12.97},
'D': {'Aaa': 0.00, 'Aa': 0.00, 'A': 0.00, 'Baa': 0.00, 'Ba': 0.00, 'B': 0.00, 'Caa-C': 0.00, 'WR': 0.00, 'D': 100.00}
}

f = open('ratings_dict.pkl', 'wb')
pickle.dump(ratings_moodys, f)
f.close()
del ratings_moodys

f = open('ratings_dict.pkl', 'rb')
ratings_moodys = pickle.load(f)
f.close()

with open('all_data.pkl', 'wb') as pkl_file:
	pickle.dump(
		{'d1': ratings_moodys, 'd2': aggregation_moodys, 'd3': pit_transitions_moodys},
		pkl_file
	)
	pkl_file.close()
del ratings_moodys, aggregation_moodys, pit_transitions_moodys

with open('all_data.pkl', 'rb') as pkl_file:
	dicts = pickle.load(pkl_file)
	pkl_file.close()

ratings_moodys = dicts['d1']
aggregation_moodys = dicts['d2']
transition_moodys = dicts['d3']

import json
with open('all_data.json', 'w') as jfile:
	json.dump(
		{'d1': ratings_moodys, 'd2': aggregation_moodys, 'd3': pit_transitions_moodys},
		jfile
	)
	jfile.close()

del ratings_moodys, aggregation_moodys, pit_transitions_moodys

with open('all_data.json', 'r') as jfile:
	dicts = json.load(jfile)
	jfile.close()

ratings_moodys = dicts['d1']
aggregation_moodys = dicts['d2']
pit_transitions_moodys = dicts['d3']
del dicts


def mean(array):
	return sum(array) / len(array)


mean_dict = {}

import zipfile as zf
from pprint import pprint
# Note that this library can read only .zip archives, not the new .7z archives
with zf.ZipFile('shocks.zip') as zfile:
	names = ['Corporate_rate', 'GDP_rate', 'Inflation_rate', 'Mortgage_rate', 'Mosprime6m']
	for name in names:
		with zfile.open('Shocks_' + name + '.txt') as f:
			content = str(f.read(), 'utf-8').replace('\r', '').replace('\n', '\t')
			exec(name + ' = content')
			del content
			mean_dict[name] = mean([float(x) for x in eval(name + ".strip().split('\t')")])
			f.close()
	zfile.close()

pprint(mean_dict)

