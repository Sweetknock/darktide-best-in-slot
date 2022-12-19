import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

#Setup for dynamic web pages that need to open web drive to load data
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
options = Options()
options.headless = True
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
driver = webdriver.Chrome(options=options)

class ScrapeGamesLantern:
    def __init__(self):
        pass

    def get_curio_traits(self):    
        # Get Curio perks
        curio_url = 'https://darktide.gameslantern.com/curios'

        response = requests.get(curio_url)
            
        soup = BeautifulSoup(response.text, 'html.parser')

        #Get list of perks
        curio_perk_class = 'list-disc m-auto bg-neutral-900 bg-opacity-80 text-shadow-none shadow-none px-8 py-4 border-2 border-[#4F674E] text-[#ecf1e8]'
        curio_perk_list = soup.find('ul', class_ = curio_perk_class)
        curio_perk_list = curio_perk_list.find_all('li')
        curio_perk_list = [cpl.text for cpl in curio_perk_list]
        
        #Get list of curio blessings
        curio_blessing_class = 'list-disc bg-neutral-900 bg-opacity-80 text-shadow-none shadow-none px-8 py-4 border-2 border-[#4F674E] text-[#ecf1e8]'
        curio_blessing_list = soup.find('ul', class_ = curio_blessing_class)
        curio_blessing_list = curio_blessing_list.find_all('li')
        curio_blessing_list = [cbl.text for cbl in curio_blessing_list]

        #Combine lists together and add column to label blessing vs perk
        curio_catagory_list = ["Blessing"]*len(curio_blessing_list) + ["Perk"]*len(curio_perk_list)
        curio_trait_list  = curio_blessing_list + curio_perk_list
            #replace "+"" with "added" because of google sheet formulas
        curio_trait_list = [ctl.replace("+", "Added ") for ctl in curio_trait_list]

        #Create final dataframe
        curio_df = pd.DataFrame({"Catagory": curio_catagory_list, "Trait": curio_trait_list})
        return curio_df

    def get_weapon_perk(self):
                # Get Curio perks
        curio_url = 'https://darktide.gameslantern.com/weapon-perks'

        response = requests.get(curio_url)
            
        soup = BeautifulSoup(response.text, 'html.parser')

        #Get list of perks
        weapon_perk_class = 'w-full max-w-3xl bg-neutral-900 p-4 border-2 border-[#4F674E] text-[#ecf1e8] m-auto mb-6'
        weapon_perk_class = soup.find('table', class_ = weapon_perk_class)
        weapon_perk_list = weapon_perk_class.find_all('tr')
        weapon_perk_list = [cpl.text for cpl in weapon_perk_list]
        weapon_perk_list = [wpl.replace("\n","").replace("+", "Added ") for wpl in weapon_perk_list]
        weapon_perk_df = pd.DataFrame({"Weapon Perks": weapon_perk_list})
        return weapon_perk_df

    #Get Weapon blessings and perks
    #This web page is dynamically loaded so I need to use selenium
    def get_weapon_blessing(self):

        #Once page is loaded I can scrape
        weapon_blessings_traits_url = 'https://darktide.gameslantern.com/weapon-blessing-traits'
        driver.get(weapon_blessings_traits_url)
        time.sleep(5) 
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        #Get blessing name
        weapon_traits_perk_name_list = soup.find_all('h3', class_ = 'font-teko text-2xl text-[#D7E4CE]')
        weapon_traits_perk_name_list = [pn.text for pn in weapon_traits_perk_name_list]

        #Get blessing description
        weapon_traits_perk_description_list = soup.find_all('p', class_ = "text-[#89A783] leading-5 text-sm")
        weapon_traits_perk_description_list = [d.text for d in weapon_traits_perk_description_list]

        #Get weapons list for each blassing
        weapon_traits_show_weapons_list = soup.find_all('ul', class_ = "list-disc text-xs pl-24 pt-2 text-neutral-200")
        weapon_traits_show_weapons_list = [d.text for d in weapon_traits_show_weapons_list]
        
        #Create final dataframe
        weapon_traits_perk_df = pd.DataFrame({"Name":weapon_traits_perk_name_list, 
                                            "Description":weapon_traits_perk_description_list,
                                            "Associated Weapons":weapon_traits_show_weapons_list})
        return weapon_traits_perk_df

    #Get Weapon Info
    #This web page is dynamically loaded so I need to use selenium
    def get_weapon_info(self):
        #Once page is loaded I can scrape
        weapon_info_url = 'https://darktide.gameslantern.com/weapons'
        driver.get(weapon_info_url)
        time.sleep(5) 
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        #Get list of perks
        weapon_item_class = 'flex flex-col lg:flex-row flex-wrap gap-2 items-center p-2 justify-center'
        weapon_item_class = soup.find('div', class_ = weapon_item_class)
        weapon_item_list = weapon_item_class.find_all('a')
        weapon_item_list = [cpl["href"] for cpl in weapon_item_list]

        weapon_name_list = []
        weapon_bonus_stat_list = []
        weapon_blessing_list = []

        for url in weapon_item_list:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            weapon_name = soup.find('h1')
            weapon_name_list.append(weapon_name.text.replace(" Weapon - Darktide", "").replace("\n", ""))

            weapon_bonus_stat = soup.find_all('h2', class_ = 'text-[#ecf1e8] text-xl font-bold mb-1')
            weapon_bonus_stat = [wbs.text for wbs in weapon_bonus_stat]
            weapon_bonus_stat_list.append(str(weapon_bonus_stat))

            weapon_blessing = soup.find_all('h3', class_ = 'font-bold text-[#ecf1e8] text-xl')
            weapon_blessing = [wb.text for wb in weapon_blessing]
            weapon_blessing_list.append(str(weapon_blessing))

        weapon_info_df = pd.DataFrame({"Name":weapon_name_list,"Bonus Stats":weapon_bonus_stat_list, "Blessings":weapon_blessing_list})
        #weapon_item_df = pd.DataFrame({"Weapon Perks": weapon_item_list})
        return weapon_info_df

def main():
    pass
    dt = ScrapeGamesLantern()

    curio_traits_df = dt.get_curio_traits()
    print(curio_traits_df)

    weapon_blessings_df = dt.get_weapon_blessing()
    print(weapon_blessings_df)

    weapon_perks_df = dt.get_weapon_perk()
    print(weapon_perks_df)

    weapon_info_df = dt.get_weapon_info()
    print(weapon_info_df)

if __name__ == '__main__':
    main()
