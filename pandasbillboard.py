from bs4 import BeautifulSoup
import urllib
import re
import musicbrainzngs

def scrape_billboard():
  request_path = "http://www.umdmusic.com/default.asp?Lang=English&Chart=D"
  out_file = "us_billboard.psv"
  log_path = "log.txt"
  f = open(out_file, 'a')
  log_file = open(log_path, 'a')

  while request_path != "":
    print ("Downloading data from: " + request_path)
    response = urllib.urlopen(request_path)
    html = response.read()
    soup = BeautifulSoup(html, 'html5lib')
    chart_date=""

    # Find all tags with href attribute matching the given regex
    previous_link=soup.find_all(href=re.compile("ChDate=\d+&ChMode=P"))
    if len(previous_link) > 0:
        request_path = previous_link[0]['href'] # The href attribute of the first match
        request_path = "http://www.umdmusic.com/" + request_path
        m = re.match(".*ChDate=(\d+).*",request_path)
        chart_date = m.group(1)
        if chart_date[0:4] <> '2017':
          request_path = "" # Only count 2017 entries
    else:
      request_path=""

    main_table=soup.find_all(text=re.compile("Display Chart Table"))[0]
    while main_table.name != "table":
            main_table = main_table.next_element

    for row in main_table.tbody.children:
        if row.name == "tr":
            past_first_cell=False
            for cell in row.children:
                if cell.name == "td":
                    if len(cell.contents) == 1:
                        f.write(cell.string.strip()+"|")
                        past_first_cell=True
                    elif len(cell.contents) == 3:
                        #fix that lets us skip header rows
                        if not(past_first_cell):
                            break
                        f.write(cell.contents[0].string.strip() + "|")
                        f.write(cell.contents[2].string.strip() + "|")
            if past_first_cell:
                f.write(chart_date + "\n")



  f.close()
  log_file.close()


scrape_billboard()
