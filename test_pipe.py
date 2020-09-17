import draftkings_football
import fanduel_football 


try:
    print("Scrapping Draftking...")
    dk_lines = draftkings_football.get_lines()
    print(dk_lines)
except:
    dk_lines = {'Failed':"True"}
    print("Failed to get DK lines")
