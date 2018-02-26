"""
class Database
"""
import pymysql
import requests
import records

class Database():
    """
    class creating the database, querying the datas from the OpenFoodFacts API
    and filling the databse with them
    """
    def __init__(self):
        self.connection = pymysql.connect(host='localhost',
                                          user='rayane',
                                          password='aaaabbbb1234',
                                          db='offdb',
                                          charset='utf8mb4',
                                          cursorclass=pymysql.cursors.DictCursor)
        #Attribute containing the connection to the database and use to make the pymysql queries
        self.db = records.Database('mysql+pymysql://rayane:aaaabbbb1234@localhost/offdb')
        self.deactivate_fk = """SET FOREIGN_KEY_CHECKS = 0"""
        #Code SQL to disable the foreign keys to be able to drop the tables more easily
        self.empty_database = """DROP TABLE IF EXISTS %s, %s, %s, %s"""%\
                            ("categories", "aliments", "saving", "last_update")
        """
        Code SQL to drop the tables if exists so that the Database is completely updated with
        the new data in OpenFoodFact
        """
        self.reactivate_fk = """SET FOREIGN_KEY_CHECKS = 1"""
        #Code SQL to reactivate the foreign keys
        self.create_categories = """CREATE TABLE IF NOT EXISTS categories (
                                                id int(200) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                                categories_names varchar(40) NOT NULL
                                                ) """
        """
        Code SQL that will be executed to create the table categories to contain the categories
        of aliment that will be searched
        """
        self.create_aliments = """CREATE TABLE IF NOT EXISTS aliments (
                                                id int(50) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                                aliments_names varchar(1000) UNIQUE NOT NULL ,
                                                categories_id int(200) NOT NULL,
                                                aliment_description varchar(2500) NOT NULL,
                                                where_to_buy varchar(2000) NOT NULL,
                                                OpenFoodFact_url varchar(2000) NOT NULL,
                                                nutrition_grade char(1) NOT NULL,
                                                CONSTRAINT fk_category_id
                                                FOREIGN KEY (categories_id) 
                                                REFERENCES categories(id)
                                                )"""
        """
        That code will create the table aliments to contain the aliments.
        The foregin key make sure that when an aliment is added in the table,
        it belongs to a category existing in the categories table
        """
        self.create_substitutes_saved = """CREATE TABLE IF NOT EXISTS saving (
                                                        id int(50) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                                                                        aliments_names varchar(2000) NOT NULL,
                                                                                        name_aliment_substituted varchar(1000) NOT NULL,
                                                                                        aliment_description varchar(2500) NOT NULL,
                                                                                        where_to_buy varchar(2000) NOT NULL,
                                                                                        OpenFoodFact_url varchar(2000) NOT NULL,
                                                                                        nutrition_grade char(1) NOT NULL,
                                                                                        CONSTRAINT fk_aliment_substituted
                                                                                        FOREIGN KEY (name_aliment_substituted) 
                                                                                        REFERENCES aliments(aliments_names)
                                                                                        )"""

        self.create_update = """CREATE TABLE IF NOT EXISTS last_update (
                                                                    id int(50) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                                                    date_of_update DATE NOT NULL 
                                                                    )"""
        """
        Create the table saving that will stock the aliments saved because they are healthier
        alternative to another aliment stocked in the database aliments.
        The foreign key make sure that when the substitute is saved,
        the aliment it replace exist in the aliments table.
        """
        self.insert_categories = """REPLACE INTO `categories` VALUES(1, 'Condiments'),
                                                                (2, 'Produits laitiers'),
                                                                (3, 'Desserts'),
                                                                (4, 'Viandes'),
                                                                (5, 'Sandwichs');"""
        #Insert inside the tables categories the categories chosen to search aliments from
        with self.connection.cursor() as cursor:
            cursor.execute(self.deactivate_fk)
            cursor.execute(self.empty_database)
            cursor.execute(self.reactivate_fk)
            cursor.execute(self.create_categories)
            cursor.execute(self.create_aliments)
            cursor.execute(self.create_substitutes_saved)
            cursor.execute(self.create_update)
            cursor.execute(self.insert_categories)
        #Execute all the SQL instructions previously written
        self.connection.commit()
        #Commmit the change in the database
    def get_products_from_api(self, ctgory, nutri_grade, nmbr_of_reslt, nmbr_almnt_wanted):
        """
        Method to get the product from OpenFoodFact by using the module records.
        It takes for arguments:
        the category and the nutrition grade wanted for the products requested,
        the number of result per page  and the number maximum of aliments to return.
        """
        produt_to_get = \
        {'search_terms':ctgory, 'nutrition_grades':nutri_grade, 'page_size':nmbr_of_reslt, 'json':1}
        #Define the arguments used for the search of the products in OpenFoodFact
        request_api_products = \
        requests.get('https://fr.openfoodfacts.org/cgi/search.pl', params=produt_to_get)
        #Attribute that will contain the data gotten from OpenFoodFact
        json = request_api_products.json()
        aliments = {}
        #Dictionnary that will contain the products
        brand_list = []
        #List of the brand of each product added to the dictionnary aliments
        name_list = []
        #List of the name of each product added to the dictionnary aliments
        for product in json['products']:
            if len(aliments.values()) == nmbr_almnt_wanted:
                #If the maximum nmber of aliments put in argument has been added in the dicitonnary,
                #the loop end and no more product is added to the dictionnary
                break
            elif self.check_exist(product) and self.check_already_added(product, brand_list, name_list):
                #If the product contain all the informations expected and hasn't already
                #been added in the database
                product.update({'category':ctgory})
                #Add the category used to find it in the product
                brand_list.append(product['brands'])
                #Add the brand of the product in the brand list
                name_list.append(product['product_name'])
                #Add the name of the product in the name list
                aliments[product['product_name']] = product
                #Add the product to the dictionnary with is name as the dictionnary key
            else:
                continue
                #If the product doesn't contain the informations expected or has already been
                #added in database, the script move to the next product in json['products']
        return aliments
        #The function return the dictionnary of aliments added

    def check_already_added(self, data, brands, names):
        """
        Method to check if a product has already been added in the dicitonnary by
        comparing the name and brand of each products
        """
        data['product_name'] = str.lower(data['product_name'])
        data['brands'] = str.lower(data['brands'])
        #Transform the brand and the name of the product to lowercase
        if data['brands'] not in brands and data['product_name'] not in names:
            #If the brand name and product name are not already in one of the list containing
            #the brands and names of products that have already been added return true
            return True

    def check_exist(self, data):
        """
        Check that the product contain the keys we are looking for and that
        the keys are not empty
        """
        if 'product_name' in data and 'brands' in data and 'stores' in data and 'url' in data \
        and 'ingredients_text' in data and 'nutrition_grades' in data:
            if data['product_name'] and data['brands'] and data['stores'] and data['url'] \
            and data['ingredients_text'] and data['nutrition_grades']:
                return True

    def insert_into_table(self, data):
        """
        Method to insert the products contained in the aliment dictionnary return by the method
        get_products_from_api
        """
        for product in data.values():
            #data.value() return a lsit of all the values of a dictionnary because the product have
            #been stocked in a dictionnary
            with self.connection.cursor() as cursor:
                get_category = "SELECT `id` FROM `categories` WHERE `categories_names`=%s"
                cursor.execute(get_category, (product['category']))
                category = cursor.fetchone()

                insert_aliments = """REPLACE INTO `aliments`
                (`aliments_names`, `categories_id`, `aliment_description`, `where_to_buy`, `OpenFoodFact_url`, `nutrition_grade`)
                VALUES (%s, %s, %s, %s, %s, %s)"""
                cursor.execute(insert_aliments, (product["product_name"], category['id'],\
                product["ingredients_text"], product["stores"], product["url"], product["nutrition_grades"]))
                self.connection.commit()

    def fill_database(self):
        """
        Fill the databse created with the datas from OpenFoodFacts
        """
        get_category = self.db.query('select * from categories')
        for category in get_category:
            aliments = self.get_products_from_api(category["categories_names"], 'e', 20, 6)
            self.insert_into_table(aliments)
            substitutes = self.get_products_from_api(category["categories_names"], 'a', 20, 3)
            self.insert_into_table(substitutes)
        with self.connection.cursor() as cursor:
            update_database = """INSERT INTO last_update VALUES (1, CURDATE())"""
            cursor.execute(update_database)
            self.connection.commit()

        #Get the products from the api
        #Insert the products inside the database
