""" class Interface"""
from tkinter import END, X, BOTH, Button, Frame, Label, Listbox
import functools
import math
import records
import pymysql

class Interface(Frame):
    """
    That class creates the main frame containing all the content used to display and organize the
    data from OpenFoodFact contained in the database created by the class Database.
    The user will have the choice between two buttons, one to select the categories contained in
    the database and get a substituted from the aliments contained in the categories selected,
    the aliment substituted can be saved in the database.
    The second button display the aliments saved in the database.
    """
    def __init__(self, fenetre, **kwargs):
        """
        initialize the widgets and attributes necessary to use the class
        """
        self.db = records.Database('mysql+pymysql://rayane:aaaabbbb1234@localhost/offdb')
        #variable containing the connection to the database with records
        self.connection = pymysql.connect(host='localhost',
                                          user='rayane',
                                          password='aaaabbbb1234',
                                          db='offdb',
                                          charset='utf8mb4',
                                          cursorclass=pymysql.cursors.DictCursor)
        #variable containing the connection the database with pymysql


        Frame.__init__(self, fenetre, width=2000, height=1000, **kwargs)
        self.pack(fill=BOTH)
        #Create the main containing all the other widgets

        self.chose_a_substitute = Button(self, text="1-Quel aliment souhaitez-vous remplacer?",\
                                         command=self.chose_category, width=200, height=17)
        self.chose_a_substitute.pack(fill=X)
        #Button that will display the categories in the db by calling the method chose_category

        self.display_substitutes_saved = Button(self, text="2-Retrouver mes aliment substitués",\
                                        command=self.display_aliments_saved, width=200, height=17)
        self.display_substitutes_saved.pack(fill=X)
        #Button that will display the substitutes saved in the Database by calling
        #the method display_aliments_saved

        self.previous_menu = Button(text="Retour", command=self.move_on_choice_menu)
        #Button that allow the user to comeback on the first menu to chose between the button
        #chose_a_substitute and display_a_substitutes_saved
        self.label = Label(self, text='Choisissez une catégorie à consulter:')
        #Label widget that display a text to make the actions to do clearer

        self.saving_list = Listbox(self, width=200, height=30)
        #Create the list that will contain the substitutes saved in the database
        self.categories_list = Listbox(self, width=200, height=30)
        #Create the list that will contain the categories saved in the database

    def display_aliments_saved(self):
        """
        Method displaying the aliments saved in the database
        """
        new_connection = records.Database('mysql+pymysql://rayane:aaaabbbb1234@localhost/offdb')

        self.chose_a_substitute.pack_forget()
        self.display_substitutes_saved.pack_forget()
        #Hide the buttons chose_a_substitute and display_substitutes_saved

        self.saving_list.pack(side="bottom")
        self.saving_list.delete(0, END)
        #Display the listbox saving_list in the main frame and empty it before
        #getting the aliments saved from the database

        self.label.config(text="Liste des aliments substitués", bg="#D6D6D6")
        self.label.pack(side="top")
        #Change the text displayed in the label and keep it at the top of the main frame

        self.aliments = new_connection.query('select * from saving')
        #Attribute containing all the aliments saved in the database by querying them
        #via records
        self.add_to_list(self.saving_list, self.aliments)
        #Method that add the aliments placed in argument in the list added as argument
        self.colour_list(self.saving_list, 5)
        #Method colouring the elements composing one aliment for every one on two aliments

        self.previous_menu.pack(side="bottom")
        self.previous_menu.config(text="Retour", command=self.move_on_choice_menu)
        #Place the previous_menu button at the bottom of the main frame and make sure
        #that the config of the button bring back on the first menu

    def colour_list(self, listname, number_of_rows_per_aliment):
        """
        Colour the elements in the listbox to make them more visible.It colours 4
        elements every fourr elements because the informations contained on each aliment
        are displayed on 4 elements (name, where_to_buy,url and description)
        """
        for aliment in range(int(listname.size()/number_of_rows_per_aliment)):
            #We divide by 4 the number of elements in the list coloured to know the number of
            #aliments that it contains
            if aliment%2 == 0:
                #The even aliments are not coloured
                continue
            else:
                #If not even we colour the 4 items describing the aliments in the listbox
                for line in range(number_of_rows_per_aliment):
                    #for the 4 next elements
                    listname.itemconfig(line+(number_of_rows_per_aliment*aliment), {'bg':'#CBCBCB'})
                    #(4*item) to know where the first item of the aliment begin in the listbox

    def add_to_list(self, list_name, aliments):
        """
        Add in the list chosen for the list_name argument the description of the aliments
        chosen for the aliments
        """
        for aliment in aliments:
            list_name.insert(END, "Nom du produit: %s " %aliment["aliments_names"])
            list_name.insert(END, "Où l'acheter: %s" %aliment['where_to_buy'])
            list_name.insert(END, "URL: %s" %aliment['OpenFoodFact_url'])
            list_name.insert(END, "Description: %s" %aliment['aliment_description'])
            if list_name == self.saving_list:
                list_name.insert(END, "Nom aliment substitué: %s"\
                                 %aliment['name_aliment_substituted'])

    def move_on_choice_menu(self):
        """
        Method to comeback on the first menu to chose between the button chose_a_substitute
        and display_a_substitutes_saved
        """
        self.label.pack_forget()
        self.categories_list.pack_forget()
        self.previous_menu.pack_forget()
        self.saving_list.pack_forget()
        #Hide the label, the categories_list list, the previous_menu button and the saving_list list
        #because they are the widgets displayed when we want to come back to the first menu
        self.chose_a_substitute.pack(fill=X)
        self.display_substitutes_saved.pack(fill=X)
        #Display the buttons of the first menu : chose_a_substitute and display_substitutes_saved

    def move_on_categories_menu(self):
        """
        Method to comeback on the menu where we can choose from which category we want to
        display the aliments saved in the database
        """
        self.aliments_list.pack_forget()
        #Hide the list displaying the aliments
        self.categories_list.pack(side="bottom")
        self.categories_list.bind('<ButtonRelease-1>',\
                                functools.partial(self.get_aliments, nutrition_grade="e"))
        #Display the list containing the categories and bind to the elements in the listbox
        #the method get_aliments that will get the aliments from the category selected
        #with a nutrition_grade of "e"
        self.label.config(text="Cliquez sur une catégorie pour voir ses aliments:")
        self.previous_menu.config(command=self.move_on_choice_menu)
        #Change the method call by the previous_menu button to move_on_choice_menu because the
        #user will be in the category menu after the call of move_on_categories_menu

    def move_on_results_menu(self):
        """
        Method to move back in the menu where we can choose which aliment we want
        to get a substitute from.
        """
        self.saving_button.pack_forget()
        self.substitute_list.pack_forget()
        #Hide the widgets saving_button and substitute_list
        self.label.config(text="Choisissez l'aliment à substituer avec la souris", bg="#D6D6D6")
        self.aliments_list.pack(side="bottom")
        #Display the list containing the aliments under the label
        self.previous_menu.pack(side="bottom")
        self.previous_menu.config(text="Retour", command=self.move_on_categories_menu)
        #Change the method called when the user click on the button by move_on_categories_menu
        #because once the method move_on_results_menu is called, the menu before that is the one
        #of the category to chose.

    def chose_category(self):
        """
        Display the menu to chose a category by calling the categories contained in the database
        """
        self.chose_a_substitute.pack_forget()
        self.display_substitutes_saved.pack_forget()
        #Hide the buttons of the first menu
        self.label.pack(side="top", fill=X)
        self.label.config(text="Cliquez sur une catégorie pour voir ses aliments:")
        #display the message asking the user to chose a category to see the aliments of
        self.categories_list.delete(0, END)
        self.categories = self.db.query('select * from categories')
        self.categories_list.pack(fill=BOTH)
        for category in self.categories:
            self.categories_list.insert(END, category["categories_names"])
        self.categories_list.bind('<ButtonRelease-1>',\
                                 functools.partial(self.get_aliments, nutrition_grade="e"))
        #Empty the content of the categories_list listbox, then get the categories contained in,
        #the database displayed the listbox, add the categories names as elements of the listbox
        #categories_list and bind the method get_aliments to the elements of the listbox

        self.previous_menu.pack(side="bottom")

    def get_aliments(self, evt, nutrition_grade):
        """
        Method getting the aliments depending of the nutrition_grade chosen in argument
        """
        if nutrition_grade == "e":
            self.category_id = self.categories_list.curselection()[0] + 1
            #curselection()[0] gives the number of the first element selected in the listbox.
            #The first element of a listbox is 0, but in a database the first element begin at one.
            #So the id of the category chosen equal the number of the element chosen plus one.
            self.categories_list.pack_forget()
            #Hide the list containing the categories
            self.aliments_list = Listbox(self, width=200, height=30)
            self.aliments_list.pack(side="bottom")
            #Create an place under the label the list that will contain
            #the aliments of the category chosen
            self.label.config(text="Cliquez sur un aliment pour voir son substitut:",
                              bg="#D6D6D6")
            #Change the text of the label
            self.aliments = self.db.query('select * from aliments where nutrition_grade = "e" \
                                           and categories_id = %s' %(self.category_id))
            self.add_to_list(self.aliments_list, self.aliments)
            self.colour_list(self.aliments_list, 4)
            #Get the aliment with a SQL query on the database via records depending of
            #the id of the category selected previously and with a nutrition_grade of e,
            # then add the aliments to the listbox aliments_list and colour the elements of the list
            self.previous_menu.config(text="Retour", command=self.move_on_categories_menu)
            #Change the method call by clicking on the return button by move_on_categories_menu
            self.aliments_list.bind('<ButtonRelease-1>', \
                                     functools.partial(self.get_aliments, nutrition_grade="a"))
            #Add an event on the element of aliments_list so that the method get_aliments is called
            #with "a" for argument to be able to display an aliment with a better nutrition grade by
            #clicking on one of the aliments in the aliments_list

        if nutrition_grade == "a":
            self.aliment_id = int(math.ceil((self.aliments_list.curselection()[0] + 1)/4))
            #The id of the element selected in the aliments_list equal the place in the list of
            #the first element selected plus one like previously seen for the category id.But this
            #time it is divided by four because each aliment is displayed on four elements of the
            #list and rounded up to get the id.If the user click on one of the four first elements,
            #he would get either 0.25, 0.50, 0.75 or 1 that would be rounded up so that for each
            #elements he would get the number 1 that is the id of the aliment selected.
            self.name_aliment_substituted = self.db.query('select aliments_names from aliments \
                                                           where id = %s ' %(self.aliment_id))
            self.name_aliment_substituted = self.name_aliment_substituted[0]["aliments_names"]
            #Once the id gotten, we query that aliment in the database via the aliment_id and
            #we keep the name of that aliment in an attribute named name_aliment_substituted
            self.label.config(text="Voici un substitut possible:", bg="#D6D6D6")
            self.aliments_list.pack_forget()
            #Change the label text and hide the aliment_list to replace with the substitute_list one
            self.substitute_list = Listbox(self, width=200, height=30)
            self.substitute_list.pack(side="bottom")
            #Create the substitute_list and display it under the label
            self.aliments = self.db.query('select * from aliments where nutrition_grade = "a" \
                                           and categories_id = %s ORDER BY RAND() LIMIT 1' %(self.category_id))
            #Get a random aliment from the databse with a nutrition gra de of a
            self.saving_button = Button(text="Sauvegarder en bdd", command=self.save_in_db)
            self.saving_button.pack(side="left")
            self.add_to_list(self.substitute_list, self.aliments)
            #Create a button displayed in the bottom left called saving_button
            #that will add the substitute displayed in the substitute_list inside
            #a table containing all the substitutes saved by the user
            self.previous_menu.config(command=self.move_on_results_menu)
            self.previous_menu.pack(side="right")
            #Change the method called by the return button and display it in the botom right

    def save_in_db(self):
        """
        Save in the table saving the substituted displayed in substitute_list
        """
        with self.connection.cursor() as cursor:
            insert_aliments = """INSERT INTO `saving`
            (`aliments_names`, `name_aliment_substituted`, `aliment_description`,
             `where_to_buy`, `OpenFoodFact_url`, `nutrition_grade`)
            VALUES (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(insert_aliments,\
                (self.aliments[0]["aliments_names"], self.name_aliment_substituted,\
                 self.aliments[0]["aliment_description"], self.aliments[0]["where_to_buy"],\
                 self.aliments[0]["OpenFoodFact_url"], self.aliments[0]["nutrition_grade"]))
            self.connection.commit()
            #Insert into the table containing the substitutes saved the substitute displayed in substitute_list
        self.label.config(text="L'aliment a bien été sauvegardé", bg="red")
        #Change the label text to inform the user of the insertion in database once it is done
