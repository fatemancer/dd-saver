import requests,sys,json

def out_record_name(url):
	return url.rsplit("/")[-3]

def parse_record(url,jar):
	data = requests.get(url,cookies=jar)
	print "Code " + str(data.status_code)
	parsed_out_name = out_record_name(url) + ".html"
	print "Out: " + parsed_out_name
	outfile = open(parsed_out_name, "w")
	outfile.write(data.text.encode('utf-8'))
	outfile.close()

if __name__ == "__main__":
	print "Cannot start as a standalone program"
	raise Exception
