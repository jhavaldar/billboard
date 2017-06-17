import pandas as pd
import musicbrainzngs
import json

def millisecond_format(num):
  m, s = divmod(num, 1000*60)
  return ("%d:%02d" % (m, s/1000))

# Given an iter index in the loop, track name, and artist, does an API request to musicbrainz, and if 
# that fails, then write the index + info to the log file
def music_brainz_request(index, query_content, artist, log):
  
  musicbrainzngs.set_useragent("Billboard Analysis", "0.3", "http://jhavaldar.github.io/jhavaldar")
  musicbrainzngs.set_rate_limit(limit_or_interval=0.5)
  result = musicbrainzngs.search_recordings(query=query_content, artist=artist, primarytype='single')['recording-list']


  if len(result) > 0:
    result = result[0]
    if 'length' in result:
      duration = int(result['length']);
    else:
      log.write(str(index) + "|" + artist + "|" + query_content)
      log.write("\n")
      return "N/A"
    return millisecond_format(duration)
  else:
    return "N/A"

#For each artist in the Billboard chart file, print out their lengths
def create_Lengths_File():

  fpath = "us_billboard.psv"
  out_file = "us_billboard_lengths.psv"
  log_file = "log.txt"
  log = open(log_file, 'a')
  f = open(out_file, 'a')
  df = pd.read_csv(fpath, sep='|')
  total = df.shape[0]

  f.write("Index|Chart|Weeks|Artist|Track|Date|Length")
  for index, row in df.iterrows():
    chart = str(row['Chart1'])
    weeks = str(row['Chart4'])
    track = row['Track']
    artist = row['Artist'].split(" featuring ")[0]
    date = str(row['Date2'])
    music_brainz = music_brainz_request(index, track, artist, log)
    if music_brainz <> "N/A":
      f.write(str(index) + "|" + chart + "|" + weeks + "|" + artist + "|" + track + "|" + date + "|" + music_brainz)
      f.write("\n")
    print ((index+0.0)/total) * 100

  log.close()
  f.close()

#For each entry in the Billboard track file, create a json of its chart history
def toSerialDict():
  data = {}
  #Chart1 = This week position
  #Date2 = This week's date
  in_file_path = "us_billboard.psv"
  df = pd.read_csv(in_file_path, sep='|')
  total = df.shape[0]

  for index, row in df.iterrows():
    chart = str(row['Chart1']) # This week's position
    date = str(row['Date2']) #This week's date

    track = str(row['Track'])
    artist = str(row['Artist'])
    key = artist+"|"+track

    if key in data.keys():
      arr = data[key] # The array consisting of all the dates and position
      arr[date]=chart
    else:
      data[key] = {date:chart}

    print (index*100.0)/total;

  with open('result.json', 'w') as fp:
    json.dump(data, fp)

def removeDoubles():
  data = {}
  #Chart1 = This week position
  #Date2 = This week's date
  in_file_path = "us_billboard_lengths.psv"
  df = pd.read_csv(in_file_path, sep='|')
  total = df.shape[0]

  for index, row in df.iterrows():
    chart = int(row['Chart']) # This week's position
    track = str(row['Track'])
    artist = str(row['Artist'])
    length = str(row['Length'])
    key = artist+"|"+track

    # Check if the peak chart is less than the previously held one
    if key in data.keys():
      data[key]['Chart'] = min(chart, data[key]['Chart'])
    else:
      data[key] = {'Length': length, 'Chart': chart}

    print (index*100.0)/total;

  with open('lengths_chart.json', 'w') as fp:
    json.dump(data, fp)

def reFormat(filepath):
  with open(filepath) as data_file:    
    data = json.load(data_file)
  newdata = []
  for key in data:
    length = data[key]['Length']
    chart = data[key]['Chart']
    artist, track =key.split("|")
    arr = {'artist': artist, 'track':track, 'length': length, 'chart': chart}
    newdata.append(arr)
  with open('lengths_chart_v2.json', 'w') as fp:
    json.dump(newdata, fp)

removeDoubles()
reFormat('lengths_chart.json')
