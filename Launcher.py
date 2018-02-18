"""
Create the database and interface to check the aliments insert in the database
from the OpenFoodFacts API
"""
import argparse
import datetime
from tkinter import Tk
import records
import Database as db
import Interface as inte



def parse_arguments():
    """
    create an argument to force the database to update
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--extension", \
                        help="""Rebuilt the databse and update the informations stored in it""")
    return parser.parse_args()

def check_last_update():
    """
    Compare the date of the last update store in database with
    today's date and return True if the number of days is more than 7
    """
    db = records.Database('mysql+pymysql://rayane:aaaabbbb1234@localhost/offdb')
    last_update = db.query('select * from last_update')
    today = datetime.date.today()
    for update in last_update:
        if ((today - update["date_of_update"]).days) > 7:
            return True

def launch_api_interface(tkinter_class):
    """
    Create a instance of the Interface class to display
    an interface that the user can use to check the datas
    in database
    """
    fenetre = Tk()
    fenetre.title("OpenFoodFacts API")
    fenetre.geometry('2000x500+400+0')
    interface = tkinter_class(fenetre)
    interface.mainloop()

def update_database(tkinter_class):
    """
    Create a new instance of the Database class that
    will desstroy and create again the whole databse
    and fill it with the last data from OpenFoodFacts
    """
    new_database = db.Database()
    new_database.fill_database()
    launch_api_interface(tkinter_class)


if __name__ == "__main__":
    #If the user write update as the extension or the file
    #hasn't been launch in more than a week, the database is updated
    args = parse_arguments()
    if args.extension == "update":
        update_database(inte.Interface)
    elif check_last_update():
        update_database(inte.Interface)
    else:
        launch_api_interface(inte.Interface)
