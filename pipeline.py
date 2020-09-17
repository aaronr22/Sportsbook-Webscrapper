import pointsbet_football
import foxbets_football 
import draftkings_football
import fanduel_football 
import aggregator
import williamhill_football
import resorts_football 
import bet365_football

try:
    print("Scrapping PB...")
    pb_lines = pointsbet_football.get_lines()
except:
    pb_lines = {}
    print("Failed to get PB lines")
try:
    print("Scrapping FoxBet...")
    fb_lines = foxbets_football.get_lines()
except:
    fb_lines = {}
    print("Failed to get FB lines")
try:
    print("Scrapping Draftking...")
    dk_lines = draftkings_football.get_lines()
except:
    dk_lines = {}
    print("Failed to get DK lines")
try:
    print("Scrapping Fanduel...")
    fd_lines = fanduel_football.get_lines()
except:
    fd_lines = {}
    print("Failed to get FD lines")
try:
    print('Scrapping William Hill...')
    wh_lines = williamhill_football.run_wh()
except:
    wh_lines = {}
    print("Failed to get WH lines")
try:
    print("Scrapping Resort...")
    r_lines = resorts_football.get_lines()
except:
    r_lines = {}
    print("Failed to get R lines")
try:
    print("Scrapping Bet365...")
    bet365_lines = bet365_football.get_lines()
except:
    bet365_lines = {}
    print("Failed to get Bet365 lines")


try:
    html_output = aggregator.run_aggregator(fd_lines, dk_lines, pb_lines, fb_lines, wh_lines, r_lines, bet365_lines)
except:
    print("Failed to aggregate lines...")

print(html_output)