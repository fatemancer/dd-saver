import requests,sys,json,rp,codecs,time
import lxml.html as html
from pandas import DataFrame


def read_settings(filename):
	with open(filename,"rb") as f:
		return json.load(f)

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

def get_pages(url,jar):
	# page = requests.get(url, cookies=jar)
	# print page
	with codecs.open("specimen-page.html", encoding="utf-8") as ff:
		page = ff.read()	
	page_parsed_html = html.fromstring(page)
	# getting upper scrollbar
	element = page_parsed_html.xpath("//*[contains(@class,'block page')]/a/@href")
	return element

def parse_article_id(r):
	return r.split(" ")[2].split("_")[1]

settings = read_settings("cookies.json")
jar = requests.cookies.RequestsCookieJar()
jar.set(settings["name"],settings["value"],domain="darkdiary.ru",path="/")
print jar

login = sys.argv[1]
url = "http://darkdiary.ru/users/" + login + "/"
pages = get_pages(url,jar)

ids = []
if query_yes_no("Login is " + login + "\nPages range:\n" + pages[0] + "\n" + pages[-1] + "\n\n Is the data above correct?"):
	begin = int(pages[0].split("=")[1])
	end = int(pages[-1].split("=")[1])
	ids = range(begin,end+1)

pages = []
for i in ids:
	params = dict(page=i)
	p = requests.get(url,params=params,cookies=jar)
	records = html.fromstring(p.text).xpath("//article/@class")
	for r in records:
		print "Parsing page " + str(i) + "..."
		rec_id = parse_article_id(r)
		link = "http://darkdiary.ru/users/" + login + "/" + rec_id + "/comment/"
		rp.parse_record(link,jar)
		print "Parsing " + link + "\nOK, waiting 10 seconds..."
		time.sleep(10)
	print "Parsing page " + str(i) + "\nOK, waiting 15 seconds..."
	time.sleep(15)
