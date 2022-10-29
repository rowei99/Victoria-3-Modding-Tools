from tkinter import *
from tkinter import ttk
from tkinter import colorchooser
from tkinter import filedialog
from pathlib import Path
from tkinter import messagebox
import re

class Main:
    def __init__(self, root):
        root.title("Victoria 3 Modding Aid")
        
        countries_template = \
        """COUNTRIES = {{
    c:{} = {{
        effect_starting_technology_tier_{}_tech = yes
        effect_starting_politics_{}= yes
    }}
}}
        """

        #list_of_tech_effects = []
        list_of_named_tech_levels = ["Very High(UK)","High(Bavaria)","Medium(Argentina)","Low(Qing-ish)","Very Low(Decentralized)"]
        current_cultures = StringVar()
        current_colour = StringVar()
        path_to_main_folder = StringVar()
        current_tag = StringVar()
        current_captial = StringVar()
        current_tech_level = StringVar()
        recognition = StringVar()
        radio_tier = StringVar()
        radio_writing_mode = StringVar(root,'a+')
        current_political_situation = StringVar()
        current_fullname = StringVar()

        def choose_color():
            # variable to store hexadecimal code of color
            temp_colour =  str(colorchooser.askcolor(title ="Choose color")[0])
            current_colour.set(re.sub("\W", " ", temp_colour))
            
        def select_folder():
            path_to_main_folder.set(filedialog.askdirectory())

        #Writes to a file under country definitions adding the currently described country
        def write_to_country_definitions():
            Path(path_to_main_folder.get()+"/common/country_definitions").mkdir(parents=True, exist_ok=True)
            with open (path_to_main_folder.get()+"/common/country_definitions/03_countries.txt",radio_writing_mode.get()) as file:
                try:
                    uppercase_tag = current_tag.get().upper()
                except:
                    messagebox.showerror(title="Bozo",message="Invalid tag")
                    return
                file.write(
                    uppercase_tag + " = {\n"+
                        "\tcolor = { "+current_colour.get()+" }"+
                        "\n\n"+
                        "\tcountry_type = "+recognition.get()+
                        "\n\n"+
                        "\ttier = "+radio_tier.get()+
                        "\n\n"+
                        "\tcultures = { "+current_cultures.get()+" }\n"+
                        "\tcapital = STATE_"+current_captial.get()+
                        "\n}\n\n"
                    )

        def create_new_history_country():
            Path(path_to_main_folder.get()+"/common/history/countries").mkdir(parents=True, exist_ok=True)
            with open (path_to_main_folder.get()+"/common/history/countries/"+current_tag.get().lower()+current_fullname.get().lower()+".txt",radio_writing_mode.get()) as file:
                try:
                    uppercase_tag = current_tag.get().upper()
                except:
                    messagebox.showerror(title="Bozo",message="Invalid tag")
                    return
                numeric_tech_value = list_of_named_tech_levels.index(current_tech_level.get())+1
                file.write(countries_template.format(uppercase_tag,str(numeric_tech_value),current_political_situation.get()))
        

        frame = ttk.Frame(root, padding="3 3 12 12")
        frame.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        #Centralization options
        radio_decentralized = ttk.Radiobutton(frame, text="Decentralized", 
        variable=recognition, value="decentralized")
        radio_unrecognized = ttk.Radiobutton(frame, text="Unrecognized", 
        variable=recognition, value="unrecognized")
        radio_recognized = ttk.Radiobutton(frame, text="Recognized", 
        variable=recognition, value="recognized")

        radio_decentralized.grid(column=1, row=0, sticky=W)
        radio_unrecognized.grid(column=1, row=1, sticky=W)
        radio_recognized.grid(column=1, row=2, sticky=W)

        #Country tier
        radio_principality = ttk.Radiobutton(frame, text="Principality", 
        variable=radio_tier, value="principality")
        radio_grand_principality = ttk.Radiobutton(frame, text="Grand Principality", 
        variable=radio_tier, value="grand_principality")
        radio_kingdom = ttk.Radiobutton(frame, text="Kingdom", 
        variable=radio_tier, value="kingdom")
        radio_empire = ttk.Radiobutton(frame, text="Empire",
        variable=radio_tier, value="empire")

        radio_principality.grid(column=2, row=0, sticky=W)
        radio_grand_principality.grid(column=2, row=1, sticky=W)
        radio_kingdom.grid(column=2, row=2, sticky=W)
        radio_empire.grid(column=2, row=3, sticky=W)

        #writing type options
        radio_overwrite = ttk.Radiobutton(frame, text="Overwrite contents", 
        variable=radio_writing_mode, value="w+")
        radio_add = ttk.Radiobutton(frame, text="Add to contents", 
        variable=radio_writing_mode, value="a+")

        radio_overwrite.grid(column=0,row=0)
        radio_add.grid(column=0,row=1)

        #tech and political starts
        tech_level_dropdown = ttk.Combobox(frame,textvariable=current_tech_level,values=["Very Low(Decentralized)","Low(Qing-ish)","Medium(Argentina)","High(Bavaria)","Very High(UK)"],state="readonly")
        tech_level_dropdown.grid(column=6,row=0)
        tech_level_label = ttk.Label(frame, text="Starting tech level:").grid(column=5,row=0)

        political_situation_dropdown = ttk.Combobox(frame,textvariable=current_political_situation,values=["traditional","reactionary","conservative","liberal"],state="readonly")
        political_situation_dropdown.grid(column=6,row=1)
        political_situation_label=ttk.Label(frame, text="Starting politics:").grid(column=5,row=1)

        button = ttk.Button(frame, text="Choose Colour", command=choose_color).grid(column=2, row=4)
        colour_label = ttk.Label(frame, textvariable=current_colour).grid(column=3, row=4)
        
        file_select_button = ttk.Button(frame, text="Select the main directory of your mod", command=select_folder).grid(column=3, row=4, columnspan = 2, sticky=W)
        path_label = ttk.Label(frame, textvariable=path_to_main_folder).grid(column=2, row=5, columnspan = 3, sticky=W)

        tag_entry_label = ttk.Label(frame, text="Three letter tag:").grid(column=3,row=0)
        tag_entry = ttk.Entry(frame, textvariable = current_tag).grid(column=4,row=0)

        cultures_entry_label = ttk.Label(frame, text="Primary cultures:").grid(column=3,row=1)
        cultures_entry = ttk.Entry(frame, textvariable = current_cultures).grid(column=4,row=1)

        capital_entry_label = ttk.Label(frame, text="Captial state: STATE_").grid(column=3,row=2)
        capital_entry = ttk.Entry(frame, textvariable = current_captial).grid(column=4,row=2)

        fullname_entry_label = ttk.Label(frame, text="Full name of country:").grid(column=3,row=3)
        fullname_entry = ttk.Entry(frame, textvariable = current_fullname).grid(column=4,row=3)

        #ttk.Button(frame, text="Quit", command=root.destroy).grid(column=0, row=4)

        write_to_countries_button = ttk.Button(frame, text="Write to countries file", command = write_to_country_definitions).grid(column=1,row=4)
        write_to_history_button = ttk.Button(frame, text="Write to history file", command = create_new_history_country).grid(column=0,row=4)



root = Tk()
Main(root)
root.mainloop()