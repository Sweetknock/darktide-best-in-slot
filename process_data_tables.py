from scrape_gameslantern import ScrapeGamesLantern
import pandas as pd
import json

class ProcessDataTables():
    def __init__():
        pass

    def check_games_lantern_and_update(request_instructions):
        with open(request_instructions) as f:
            gameslantern_html_request_instructions = json.load(f)

        gameslantern_request_dict = {}
        
        #gameslantern_lists = ["weapons", "modifiers", "curios", "weapon-blessing-traits"]
        gameslantern_keys = gameslantern_html_request_instructions.keys()
        for key in gameslantern_keys:
            dt = ScrapeGamesLantern(gameslantern_html_request_instructions[key])
            gameslantern_request_dict[key] = dt.get_html_data_from_request_json()

        with open('backup.json', 'w') as f:
            json.dump(gameslantern_request_dict, f, indent=1)

    def get_last_update_as_dataframes():
        try:
            with open("/var/www/html/darktide-best-in-slot/backup.json") as json_file:
                gameslantern_request_dict = json.load(json_file)
        except:    
            with open("backup.json") as json_file:
                gameslantern_request_dict = json.load(json_file)

        gameslantern_df_dict = {}    
        gameslantern_df_dict["weapons"] = pd.DataFrame(gameslantern_request_dict["weapons"])
        gameslantern_df_dict["modifiers"] = pd.DataFrame(gameslantern_request_dict["modifiers"])
        gameslantern_df_dict["weapon-blessing-traits"] = pd.DataFrame(gameslantern_request_dict["weapon-blessing-traits"])

        curio_trait = []
        curio_catagory = []
        for key in ['Blessing', 'Perk']:
            curio_trait += (gameslantern_request_dict["curios"][key])
            curio_catagory += ([key]*len(gameslantern_request_dict["curios"][key]))
        gameslantern_df_dict["curios"] = pd.DataFrame({"catagory":curio_catagory, "trait":curio_trait})

        return gameslantern_df_dict
