import pointsbet_football
import foxbets_football 
import draftkings_football
import fanduel_football 
import aggregator
import williamhill_football
import resorts_football 
import bet365_football
def run_pipeline(sport):
    
    try:
        print("Scrapping PB...")
        pb_lines = pointsbet_football.get_lines(sport)
        print(pb_lines.keys())
        if "Error" in pb_lines.keys():
            print("Failed to get PB lines", pb_lines["Error"])    
    except Exception as e:
        pb_lines = {'Failed':"True"}
        print("Failed to get PB lines", e)
    try:
        print("Scrapping FoxBet...")
        fb_lines = foxbets_football.get_lines(sport)
        print(fb_lines.keys())
        if "Error" in fb_lines.keys():
            print("Failed to get FB lines", fb_lines["Error"])
    except Exception as e:
        fb_lines = {'Failed':"True"}
        print("Failed to get FB lines", e)
    try:
        print("Scrapping Draftking...")
        dk_lines = draftkings_football.get_lines(sport)
    except Exception as e:
        dk_lines = {'Failed':"True"}
        print("Failed to get DK lines: ", e)
    try:
        print("Scrapping Fanduel...")
        fd_lines = fanduel_football.get_lines(sport)
    except Exception as e:
        fd_lines = {'Failed':"True"}
        print("Failed to get FD lines", e)
    try:
        print('Scrapping William Hill...')
        wh_lines = williamhill_football.run_wh(sport)
        if "Error" in wh_lines.keys():
            print("Failed to get WH lines: ", wh_lines['Error'])
        print(wh_lines.keys())
    except Exception as e:
        wh_lines = {'Failed':"True"}
        print("Failed to get WH lines: ", e )
    
    try:
        print("Scrapping Resort...")
        r_lines = resorts_football.get_lines(sport)
        if "Error" in r_lines.keys():
            print("Failed to get R lines", r_lines["Error"])
    except Exception as e:
        r_lines = {'Failed':"True"}
        print("Failed to get R lines", e)
    try:
        print("Scrapping Bet365...")
        #bet365_lines = bet365_football.get_lines()
        #if "Error" in bet365_lines.keys():
        #    print("Failed to get Bet365 lines: ", bet365_lines["Error"])
        bet365_lines = {"Error":""}
    except Exception as e:
            print("Failed to get Bet365 lines: ", e)
            bet365_lines = {"Error":e}
    try:
        print('Running aggregator...')
        if sport == 'NFL':
            html_output = aggregator.run_aggregator(fd_lines, dk_lines, pb_lines, fb_lines, wh_lines, r_lines, bet365_lines)
        elif sport == 'CFB':
            html_output = aggregator.aggregate_cfb(fd_lines, dk_lines, pb_lines, fb_lines, wh_lines, r_lines, bet365_lines)
        #print(html_output)
        return html_output
    except Exception as e:
        print("Failed to aggregate lines...")
        print(e)
        return 'None'