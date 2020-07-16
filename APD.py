import sys
import csv
from pfr import scores, get_games
from stats import calculate_apd
from plot import graph_team

# #scrapes data from a pro-football-reference boxscore webpage and accordingly creates a gamelog txt file
# #works under the assumption that the parameter is necessarily a PFR boxcore webpage
# def createdata(src):
#     data = open('data','w+')
#     source = requests.get(src)
#     soup = BeautifulSoup(source.text,"lxml")
#     div = soup.find("div",id="all_team_stats")
#     timesearch= re.search('(?P<mins1>\d\d):(?P<secs1>\d\d).*(?P<mins2>\d\d):(?P<secs2>\d\d)',div.prettify())
#     if timesearch:
#         data.write("Total time: %d\n"%(60*(int)(timesearch.group('mins1'))+(int)(timesearch.group('secs1'))+60*(int)(timesearch.group('mins2'))+(int)(timesearch.group('secs2'))))
    
#     rows = soup.find("table",id="scoring").tbody.find_all("tr")
#     for row in rows:
#         line = ""
#         line+=row.find("th").text+" "
#         for td in row.find_all("td"):
#             line+=td.text+ " "
#         data.write("%s\n"%line.strip())
#     data.close()

# #given a gamelog txt file, reads it and calculates the in-game average point differential
# def apd(logfilename,playoff):
#     fName = open(logfilename,'r')
#     numscores=0
#     scorediff={}
#     time={}
#     scorediff[numscores]=0
#     time[numscores]=0
#     num = 15
#     ottime = 10
#     if(playoff==1):
#         ottime = 15
#     totaltime=3600
#     for line in fName:
#         totaltimesearch = re.search('Total time: (?P<time>\d+)',line)
#         otsearch = re.search('OT(?P<ot>\d*) (?P<mins>\d+):(?P<secs>\d\d).* (?P<away>\d+) (?P<home>\d+)',line)
#         quartersearch = re.search('(?P<quarter>\d) (?P<mins>\d+):(?P<secs>\d\d).* (?P<away>\d+) (?P<home>\d+)',line)
#         scoresearch=re.search('(?P<mins>\d+):(?P<secs>\d\d).* (?P<away>\d+) (?P<home>\d+)',line)
#         if totaltimesearch:
#             totaltime=(int)(totaltimesearch.group('time'))
#         if otsearch:
#             if otsearch.group('ot'):
#                 num = 60+(int)(otsearch.group('ot'))*ottime
#             else:
#                 num = 60+ottime
#             numscores+=1
#             scorediff[numscores]=(int)(otsearch.group('home'))-(int)(otsearch.group('away'))
#             time[numscores]=60*num-60*(int)(otsearch.group('mins'))-(int)(otsearch.group('secs'))
#         elif quartersearch:
#             quarter = (int)(quartersearch.group('quarter'))
#             if(quarter==2):
#                 num=30
#             elif(quarter==3):
#                 num=45
#             elif(quarter == 4):
#                 num=60
#             numscores+=1
#             scorediff[numscores]=(int)(quartersearch.group('home'))-(int)(quartersearch.group('away'))
#             time[numscores]=60*num-60*(int)(quartersearch.group('mins'))-(int)(quartersearch.group('secs'))
#         elif scoresearch:
#             numscores+=1
#             scorediff[numscores]=(int)(scoresearch.group('home'))-(int)(scoresearch.group('away'))
#             time[numscores]=60*num-60*(int)(scoresearch.group('mins'))-(int)(scoresearch.group('secs'))
#     fName.close()
#     totalpd=0.0
#     print(scorediff)
#     for x in range (0, numscores):
#         deltatime = time[x+1]-time[x]
#         totalpd += deltatime*scorediff[x]
#     totalpd+=(totaltime-time[numscores])*scorediff[numscores]
#     apd = totalpd/totaltime
#     return apd

def average(l):
    return sum(l) / len(l)
    
if __name__ == '__main__':
    if sys.argv[1] == "season":
        season = "2019"
        if len(sys.argv) == 3:
            season = int(sys.argv[2])
        weeks = range(1, 22)
        week_by_week = {}
        for week in weeks:
            print(f"week {week}")
            games = get_games(week, season=season)
            for game in games:
                game_stats = scores(game)
                stats = calculate_apd(game_stats)
                for k, v in stats.items():
                    week_by_week[k] = week_by_week.get(k, []) + [v]
        averages = {k: average(v) for k, v in week_by_week.items()}
        with open(f"{season}.csv", "w") as csvfile:
            seasonwriter = csv.writer(csvfile)
            for k, v in week_by_week.items():
                seasonwriter.writerow([k] + v)
            for k, v in averages.items():
                seasonwriter.writerow([k] + [v])
    elif sys.argv[1] == "game":
        url = sys.argv[2]
        game_stats = scores(url)
        stats = calculate_apd(game_stats)
        print(stats)
    elif sys.argv[1] == "saved":
        file_name = sys.argv[2]
        with open(file_name) as csvfile:
            seasonreader = csv.reader(csvfile)
            i = 0
            week_by_week = {}
            averages = {}
            for row in seasonreader:
                if i > 31:
                    team, average = row
                    averages[team] = average
                else:
                    week_by_week[row[0]] = [float(r) for r in row[1:]]
                i += 1
        graph_team("NWE", week_by_week["NWE"])


