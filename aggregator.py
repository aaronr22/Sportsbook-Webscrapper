from fuzzywuzzy import fuzz

def similar_key(search_key, list_keys):
    max_key = (0, '')
    for key in list_keys:
        if(fuzz.token_set_ratio(search_key, key) > max_key[0]):
            max_key = (fuzz.token_set_ratio(search_key, key), key)
    return max_key

def run_aggregator(fd_lines, dk_lines, pb_lines, fb_lines, wh_lines, r_lines, bet365_lines):
    out_dict = {}
    for date in fd_lines.keys():
        fd_to_dk = {}
        out_dict[date] = {}
        #convert fd to draftkings name dict
        for fd_team in fd_lines[date].keys():
            try:
                fd_to_dk[fd_team] = similar_key(fd_team, dk_lines[date].keys())[1]
            except Exception as e:
                print(e)
            if(date in dk_lines.keys()):
                try:
                    dk_val = dk_lines[date][fd_to_dk[fd_team]]
                except:
                    dk_val = 0
            else:
                dk_val = 0
            if(date in pb_lines.keys()):
                try:
                    pb_val = pb_lines[date][fd_team]
                except:
                    pb_val = 0
            else:
                pb_val = 0
            if(date in fb_lines.keys()):
                try:
                    fb_val = fb_lines[date][fd_team]
                except:
                    fb_val = 0
            else:
                fb_val = 0
            if(date in wh_lines.keys()):
                try:
                    wh_val = wh_lines[date][fd_team]
                except: 
                    wh_val = 0
            else:
                wh_val = 0
            if(date in r_lines.keys()):
                try:
                    r_val = r_lines[date][fd_team]
                except Exception as e: 
                    print(e)
                    r_val = 0
            else:
                r_val = 0     
            if(date in bet365_lines.keys()):
                try:
                    b365_val = bet365_lines[date][fd_team]
                except: 
                    b365_val = 0
            else:
                b365_val = 0                  
            out_dict[date][fd_team] = (fd_lines[date][fd_team], dk_val, pb_val, fb_val, wh_val, r_val, b365_val)
    final_dict = {}
    for date in out_dict.keys():
        final_dict[date] = {}
        for team in out_dict[date]:
            final_dict[date][team] = {}
            match = out_dict[date][team]
            tmp_list1 = [[match[0][0][1], match[0][0][2], match[0][0][3]]]
            tmp_list2 = [[match[0][1][1], match[0][1][2], match[0][1][3]]]
            if(match[1] == 0):
                tmp_list1.append(0)
                tmp_list2.append(0)
            else:
                tmp_list1.append([match[1][0][1],match[1][0][3],match[1][0][2]])
                tmp_list2.append([match[1][1][1],match[1][1][3],match[1][1][2]])
            if(match[2] == 0):
                tmp_list1.append(0)
                tmp_list2.append(0)
            else:
                tmp_list1.append([match[2][0][1],match[2][0][3],match[2][0][2]])
                tmp_list2.append([match[2][1][1],match[2][1][3],match[2][1][2]])
            if(match[3] == 0):
                tmp_list1.append(0)
                tmp_list2.append(0)
            else:
                tmp_list1.append([match[3][0][1],match[3][0][2],match[3][0][3]])
                tmp_list2.append([match[3][1][1],match[3][1][2],match[3][1][3]])
            if(match[4] == 0):
                tmp_list1.append(0)
                tmp_list2.append(0)
            else:
                tmp_list1.append([match[4][0][1],match[4][0][2],match[4][0][3]])
                tmp_list2.append([match[4][1][1],match[4][1][2],match[4][1][3]])
            if(match[5] == 0):
                tmp_list1.append(0)
                tmp_list2.append(0)
            else:
                tmp_list1.append([match[5][0][1],match[5][0][2],match[5][0][3]])
                tmp_list2.append([match[5][1][1],match[5][1][2],match[5][1][3]]) 
            if(match[6] == 0):
                tmp_list1.append('0')
                tmp_list2.append('0')
            else:
                tmp_list1.append([match[6][0][1],match[6][0][2],match[6][0][3]])
                tmp_list2.append([match[6][1][1],match[6][1][2],match[6][1][3]]) 
            final_dict[date][team][match[0][0][0]] = tmp_list1
            final_dict[date][team][match[0][1][0]] = tmp_list2

    tmp_str = "<table><tr><th>Date</th><th>Game</th><th>Team</th><th>Fanudel</th><th>Draftkings</th><th>Pointsbet</th><th>Foxbets</th><th>William Hill</th><th>Resorts</th><th>Bet365</th></tr>"
    for date in final_dict.keys():
        data = final_dict[date]
        for key in data.keys():
            tmp_str = tmp_str + "<tr><th>"+date+"</th><th>" + key + "</th></tr>"
            for team in data[key].keys():
                if(data[key][team][0] != 0):
                    str1 = ' '.join([str(elem)+' | ' for elem in data[key][team][0]])
                else: 
                    str1 = '--'
                if(data[key][team][1] != 0):
                    str2 = ' '.join([str(elem)+' |' for elem in data[key][team][1]])
                else: 
                    str2 = '--'
                if(data[key][team][2] != 0):
                    str3 = ' '.join([str(elem)+' | ' for elem in data[key][team][2]])
                else: 
                    str3 = '--'
                if(data[key][team][3] != 0):
                    str4 = ' '.join([str(elem)+' | ' for elem in data[key][team][3]])
                else: 
                    str4 = '--'
                if(data[key][team][4] != 0):
                    str5 = ' '.join([str(elem)+' | ' for elem in data[key][team][4]])
                else: 
                    str5 = '--'
                if(data[key][team][5] != 0):
                    str6 = ' '.join([str(elem)+' | ' for elem in data[key][team][5]])
                else: 
                    str6 = '--' 
                if(data[key][team][6] != 0):
                    str7 = ' '.join([str(elem)+' | ' for elem in data[key][team][6]])
                else: 
                    str7 = '--'                     
                tmp_str = tmp_str + "<tr><td></td><td></td><td>" + team +"</td><td>" + str1 +"</td><td>" + str2 +"</td><td>" + str3 +"</td><td>" + str4 +"</td><td>" + str5 +"</td><td>" + str6 +"</td><td>" + str7 +"</td></tr>"
    print(final_dict)
    tmp_str = tmp_str + "</table>"
    return tmp_str + "</table>"