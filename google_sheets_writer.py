import gspread
from scrape_gameslantern import ScrapeGamesLantern
import re

def main():
    gc = gspread.oauth()
    workbook = gc.open('40k_Darktide_Weapons_and_Curios')


    worksheet_list = workbook.worksheets()
    worksheet_list = [re.findall(r'\'.*?\'', str(wsl))[0] for wsl in worksheet_list]
    worksheet_list = [wsl.replace("'","" ) for wsl in worksheet_list]
    sheet_titles = ['Weapon Blessings', 'Weapon Perks', 'Weapon Info', 'Curios']

    for title in sheet_titles:
        if title not in worksheet_list:
            workbook.add_worksheet(title=title, rows=200, cols=20)

    dt = ScrapeGamesLantern()

    worksheet = workbook.worksheet("Weapon Blessings")
    weapon_blessings_df = dt.get_weapon_blessing()
    weapon_blessings_df["Tier"] = worksheet.col_values(1)[1:]
    weapon_blessings_df = weapon_blessings_df[ ['Tier'] + [ col for col in weapon_blessings_df.columns if col != 'Tier' ] ]
    worksheet.update([weapon_blessings_df.columns.values.tolist()] + weapon_blessings_df.values.tolist())
    
    worksheet = workbook.worksheet("Weapon Perks")
    weapon_perks_df = dt.get_weapon_perk()
    weapon_perks_df["Tier"] = worksheet.col_values(1)[1:]
    weapon_perks_df = weapon_perks_df[ ['Tier'] + [ col for col in weapon_perks_df.columns if col != 'Tier' ] ]
    worksheet.update([weapon_perks_df.columns.values.tolist()] + weapon_perks_df.values.tolist())

    worksheet = workbook.worksheet("Weapon Info")
    weapon_info_df = dt.get_weapon_info()
    #weapon_info_df["Tier"] = worksheet.col_values(1)[1:]
    weapon_info_df["Tier"] = ["NR"]*len(weapon_info_df)
    weapon_info_df = weapon_info_df[ ['Tier'] + [ col for col in weapon_info_df.columns if col != 'Tier' ] ]
    worksheet.update([weapon_info_df.columns.values.tolist()] + weapon_info_df.values.tolist())

    worksheet = workbook.worksheet("Curios")
    curio_traits_df = dt.get_curio_traits()
    curio_traits_df["Tier"] = worksheet.col_values(1)[1:]
    curio_traits_df = curio_traits_df[ ['Tier'] + [ col for col in curio_traits_df.columns if col != 'Tier' ] ]
    worksheet.update([curio_traits_df.columns.values.tolist()] + curio_traits_df.values.tolist())

if __name__ == '__main__':
    main()