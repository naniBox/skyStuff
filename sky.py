#!/usr/bin/env python3.9

import datetime
import astral
from astral.sun import sun
from suntime import Sun, SunTimeException
import os
import glob
from pytz import timezone
from pathlib import Path
import argparse

latitude = 34.6937
longitude = 135.5023
#sun = Sun(latitude, longitude)
OsakaTZ = timezone('Asia/Tokyo')
osaka = astral.LocationInfo(name="Osaka", region="Japan", 
							timezone="Asia/Tokyo", latitude=latitude, 
							longitude=longitude)

dayCamDir = "/mnt/kioku/media/Photos/eye/dayCam/"
dayLightDir = "/mnt/kioku/media/Photos/eye/dayLight01/"

def get_sun(date):
	s = sun(osaka.observer, date, tzinfo=osaka.timezone)
	return s["sunrise"], s["sunset"]

def print_times(day, sunrise, sunset):
	print("{} : Sunrise: {} ->: Sunset: {}".format(day, sunrise, sunset))


def test_days():
	day = datetime.date(2022, 1, 1)
	today = datetime.date.today()

	while day < today:
		sunrise, sunset = get_sun(day)
		print_times(day, sunrise, sunset)
		day += datetime.timedelta(days=1)

def parse_photo(fname):
	#print("opening '{}'".format(fname))
	lines = [l.strip() for l in open(fname,"rt").readlines()]
	#print(lines)
	p1 = Path(lines[0])
	p2 = Path(fname)
	photo = p2.parent / p1.name
	dt = datetime.datetime.strptime(lines[1],"DateTime: %Y%m%d %H:%M:%S")
	dt = dt.replace(tzinfo=OsakaTZ)
	return str(photo),dt

def get_photos_for_day(day_str):
	dname = os.path.join(dayCamDir, day_str)
	print(dname, end="")
	dt = datetime.datetime.strptime(day_str,"%Y%m%d")
	day = datetime.date(dt.year, dt.month, dt.day)
	sunrise, sunset = get_sun(day)
	fnames = sorted(glob.glob("{}/*.txt".format(dname)))
	print_times(day, sunrise, sunset)
	print("  ",fnames[:5])
	photos = []
	for fname in fnames:
		photo,dt = parse_photo(fname)
		if dt > sunrise and dt < sunset:
			photos.append(photo)
		else:
			pass
			print("     Reject:",dt,sunrise,sunset)
	print(": {} : Sunrise: {} ->: Sunset: {} : {}".format(day, sunrise, sunset, len(photos)))
	#print("  ",len(photos), photos[0:5])
	return photos

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("--start_date", help="What date to start on")
	parser.add_argument("--outdir", help="where to do the linking")
	parser.add_argument("--test_days", help="Runs the tests", action="store_true")
	args = parser.parse_args()
	if args.test_days:
		test_days()
		return
	start = None
	if args.start_date:
		start = args.start_date
	if args.outdir:
		OUTDIR = args.outdir
	else:
		OUTDIR = dayLightDir

	days = sorted(os.listdir(dayCamDir))
	all_photos = []

	# if we do not have a specific start, then store all
	do_store = False
	if start is None:
		do_store = True
	else:
		print("We have a start, starting from: '{}'".format(start))
	for day_str in days:
		if start:
			if day_str == start:
				print("  Found the start: '{}'".format(start))
				do_store = True

		if do_store:
			photos = get_photos_for_day(day_str)
			all_photos += photos
	#print(all_photos)
	count = 0
	for photo in all_photos:
		dst_name = Path(OUTDIR) / Path("dayLight {:08d}.jpg".format(count))
		src_name = Path("..").joinpath(*Path(photo).parts[-3:])
		count += 1
		if os.path.exists(dst_name):
			continue
		print(">> {} => {} => {}".format(photo, dst_name, src_name))
		os.symlink(src_name, dst_name)
		
	print(len(all_photos))

if __name__ == '__main__':
	main()
