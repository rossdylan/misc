#!/bin/bash
# Author: Ross Delinger
# Simple script to update all packages pip knows about
# Super dumb, just tries to update all packages
trap exittrap INT
packages=`pip freeze | sed -e 's/==.*//' -e 's/\n/ /'`
exittrap()
{
	exit
}
for p in $packages; do
	pip install --upgrade $p
done
