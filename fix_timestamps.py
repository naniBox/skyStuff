import os
import glob
import datetime
import pprint

class Info(object):
	def __init__(self):
		super(Info, self).__init__()

def ex(s):
	return s.split(":",1)[1].strip()

def parse_photo(fname):
	fname = fname[:-3]+"txt"
	lines = [l.strip() for l in open(fname,"rt").readlines()]
	#print(lines)
	i = Info()
	i.path          = lines[0]
	i.datetime      = ex(lines[1])
	i.exposure_time = ex(lines[2])
	i.gain          = ex(lines[3])
	i.pixel_format  = ex(lines[4])
	i.balance_ratio = ex(lines[5])
	i.convergance   = ex(lines[6]).split(",")[-2:]
	#pprint.pprint(vars(i))
	return i

def write_info(fname, info):
	fname = fname[:-3]+"txt"
	ss = []
	ss.append(info.path)
	ss.append("  DateTime: {}".format(info.datetime))
	ss.append("  Exposure Time: {}".format(info.exposure_time))
	ss.append("  Gain: {}".format(info.gain))
	ss.append("  PixelFormat: {}".format(info.pixel_format))
	ss.append("  Balance Ratio: {}".format(info.balance_ratio))
	ss.append("  Convergance: {}\n".format(",".join(info.convergance)))
	open(fname,"wt").write("\n".join(ss))

def main():
	for fname in sorted(glob.glob("*.jpg")):
		st = os.stat(fname)
		info = parse_photo(fname)
		info.datetime = datetime.datetime.fromtimestamp(st.st_mtime).strftime("%Y%m%d %H:%M:%S")
		print(fname, info.datetime)
		#pprint.pprint(vars(info))
		write_info(fname, info)

if __name__ == '__main__':
	main()