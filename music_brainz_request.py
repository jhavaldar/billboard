import pandas as pd
import musicbrainzngs

def millisecond_format(num):
  m, s = divmod(num, 1000*60)
  return ("%d:%02d" % (m, s/1000))

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

def search():

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

search()

