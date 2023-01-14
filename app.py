from flask import Flask, render_template, session, redirect
from process_data_tables import ProcessDataTables

app = Flask(__name__)

@app.route('/', methods=("POST", "GET"))
def html_table():
    
    #Load tables from dictionary
    df_dict = ProcessDataTables.get_last_update_as_dataframes()
    curios_df = df_dict["curios"]
    weapon_df = df_dict["weapons"]
    weapon_blessing_traits_df = df_dict["weapon-blessing-traits"]
    modifiers_df = df_dict["modifiers"]

    return render_template('index.html', tables=[curios_df.to_html(classes='data'), weapon_df.to_html(classes='data'), weapon_blessing_traits_df.to_html(classes='data'), modifiers_df.to_html(classes='data')], 
    titles=["Placeholder", "Curios", "Weapons", "Weapon Blessings and Traits", "Modifiers"])

if __name__ == "__main__":
    app.run(debug=True)