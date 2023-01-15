from flask import Flask, render_template, session, redirect
from process_data_tables import ProcessDataTables

app = Flask(__name__)

@app.route('/', methods=("POST", "GET"))
def html_table():
    
    #Load tables from dictionary
    df_dict = ProcessDataTables.get_last_update_as_dataframes()
    curios_df = df_dict["curios"]
    
    weapon_df = df_dict["weapons"]
    weapon_df["Weapon Blessings"] = [','.join([a +' - '+ b for (a,b) in zip(wb,wbd)]) for (wb, wbd) in zip(weapon_df["Weapon Blessings"].to_list(), weapon_df["Weapon Blessing Description"].to_list())]
    weapon_df = weapon_df.drop("Weapon Blessing Description", axis=1)
    #weapon_blessing_traits_df = df_dict["weapon-blessing-traits"]
    #modifiers_df = df_dict["modifiers"]

    return render_template('index.html', tables=[curios_df.to_html(classes='table-bordered', index=False), weapon_df.to_html(classes='table-bordered', index=False)], 
    titles=["Placeholder", "Curios", "Weapons"])

if __name__ == "__main__":
    app.run()