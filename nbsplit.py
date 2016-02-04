#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import click

@click.argument('filename')
@click.option('-n', '--cellnum', default=-1)
@click.option('-p', '--prefix', default=None, type=str)
@click.command()
def split(filename, prefix=None, cellnum=-1):
	"""Split a Jupyter notebook to two notebooks.

	filename (str): filename of notebook to split.
	
	prefix (str): if given, the notebook will be split at the first cell that starts with prefix.
	
	cellnum (int): the cell number to split on; used only if prefix is not given.
	"""
	print("Splitting", filename)
	with open(filename, 'rt', encoding='utf8') as f:
		notebook = json.load(f)
	nbformat = notebook['nbformat']
	if int(nbformat) != 4:
		raise ValueError("I can only work with nbformat 4")
	cells = notebook['cells']
	if prefix is not None:
		print("Searching for a cell that starts with: {}".format(prefix))
		for i, cell in enumerate(cells):
			if cell['source']:
				if cell['source'][0].startswith(prefix):
					cellnum = i
					break
	if cellnum >= 0:
		print("Splitting at cell {}: {}...".format(cellnum, cells[cellnum]['source'][0][:20]))
		cells1 = cells[:cellnum]
		cells2 = cells[cellnum:]	 
	else:
		raise ValueError("Must have a non-negative cell number: {}".format(cellnum))
	notebook1 = notebook.copy()
	notebook2 = notebook.copy()
	notebook1['cells'] = cells1
	notebook2['cells'] = cells2
	filename1, ext1 = os.path.splitext(filename)
	filename2, ext2 = os.path.splitext(filename)
	filename1 += '_1'
	filename2 += '_2'
	with open(filename1 + ext1, 'wt') as f:
		json.dump(notebook1, f)
	print("Wrote head notebook to {}".format(filename1 + ext1))
	with open(filename2 + ext2, 'wt') as f:
		json.dump(notebook2, f)
	print("Wrote tail notebook to {}".format(filename2 + ext2))


if __name__ == '__main__':
	split()