# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 10:49:14 2019

@author: Nathan Hoang
"""
import json
import os

def item_value(database, product):
    '''totals per item value'''
    total_value = database.db[product][1] * database.db[product][2]
    return float(total_value)

def total_value(database):
    '''totals value across all items'''
    total_value = 0
    for x in database.db:
        item_value = 0
        item_value += database.db[x][1] * database.db[x][2]
        print(f'ID #: {x} | item: {database.db[x][0]} | \
qty: {database.db[x][2]}  |  price: {database.db[x][1]}  |  \
line value: ${item_value:.2f}')

    for x in database.db:
        total_value += database.db[x][1] * database.db[x][2]
    print(f'\nTotal inventory value: ${total_value:.2f}\n')

class InvDB():
    '''class for database'''
    def __init__(self, location):
        self.location = os.path.expanduser(location)
        self.load(self.location)

    def load(self, location):
        if os.path.exists(location):
            self._load()
        else:
            self.db = {}

    def _load(self):
        self.db = json.load(open(self.location, "r"))

    def dumpdb(self):
        json.dump(self.db, open(self.location, "w+"))

    def set(self, key, value):
        self.db[str(key)] = value
        self.dumpdb()

    def get(self, key):
        return self.db[key]

    def delete(self, key):
        del self.db[key]
        self.dumpdb()

    def resetdb(self):
        self.db = {}
        self.dumpdb()



def file_maintenance(database):
    '''function for file maintenance screen/prompt'''
    while True:
        product_adj = input('\nPlease enter the product ID, enter "S" to \
search product IDs, OR enter "E" to return: ')

        if product_adj == 'E':
            break
        elif product_adj == 'S':
            print('\n'*100)
            while True:
                user_search = input('Enter the name of the item to search or \
enter "A" for a list of ALL. "E" to return: ')

                if user_search == 'E':
                    break
                elif user_search == 'A':
                    print('\n'*100)
                    print('All results listed below:\n\n')
                    for x in database.db:
                        print(f'item: {database.db[x][0]} | ID #: {x}')
                    print(f'\n{len(database.db)} results\n')
                else:
                    print('\n'*100)
                    result_counter = 0
                    for x in database.db:
                        if user_search.lower() in database.db[x][0].lower():
                            result_counter += 1
                            print(f'\nitem name: \
{database.db[x][0]} \
| ID #: {x}\n')

                    print(f'\n{result_counter} results\n')

        else:
            try:
                print(database.db[product_adj][0])
                print('\n'*100)
            except:
                print('\n'*100)
                print('\nInvalid action or Product ID')
            else:
                while True:
                    print(f'\n ---ID: {product_adj}---\n\n\
item: {database.db[product_adj][0]} | \
qty: {database.db[product_adj][2]}  |  \
price: ${database.db[product_adj][1]:.2f}  |  \
value: ${item_value(database, product_adj):.2f}')
                    user_action = input('\n\nEnter "Q" to adjust QTY, "P" \
to adjust price, "N" to adjust name, "D" to delete item, "E" to return: ')
                    if user_action == 'E':
                        print('\n'*100)
                        break
                    elif user_action == 'Q':
                        print('\n'*100)
                        while True:
                            try:
                                print(f'\n\
{database.db[product_adj][0]} | \
current qty: {database.db[product_adj][2]}')
                                adj_qty = int(input('Please enter QTY \
to increase. (Enter a negative value to decrease. E.g. "-1"): '))
                            except:
                                print('Please enter a numerical integer')
                            else:
                                database.db[product_adj][2] += int(adj_qty)
                                database.dumpdb()
                                print('\n'*100)
                                print('\n--Adjusted--\n')
                                break
                    elif user_action == 'P':
                        print('\n'*100)
                        while True:
                            try:
                                print(f'\n\
{database.db[product_adj][0]} | \
current price: ${database.db[product_adj][1]:.2f}')
                                adj_price = float(input('Please enter \
new price: $'))
                            except:
                                print('Please enter a numerical value \
for price')
                            else:
                                database.db[product_adj][1] = \
                                float(adj_price)
                                database.dumpdb()
                                print('\n'*100)
                                print('\n--Adjusted--\n')
                                break
                    elif user_action == 'N':
                        print('\n'*100)
                        while True:
                            print(f'\ncurrent name: \
{database.db[product_adj][0]}')
                            adj_name = input('\nPlease enter new name: ')
                            database.db[product_adj][0] = adj_name
                            database.dumpdb()
                            print('\n'*100)
                            print('\n--Adjusted--\n')
                            break
                    elif user_action == 'D':
                        print('\n'*100)
                        while True:
                            del_decision = input(f'\nAre you sure you \
would like to delete "{database.db[product_adj][0]}" \
from the system?\nSelect "Y" or "N": ')
                            if del_decision == 'Y':
                                database.delete(product_adj)
                                print('\nEntry deleted from the system\n')
                                break
                            if del_decision == 'N':
                                break
                        break
                    else:
                        print('\n'*100)
                        print('\nPlease enter a valid value or \
"E" to return')



def add_product(database):
    '''function for add product screen/prompt'''
    while True:
        decision = input('\nWould you like to add a new product? enter \
"Y" to continue or "E" to return: ')

        if decision == 'E':
            break
        elif decision == 'Y':
            while True:
                new_product_continue = True
                new_product_id = input('Please enter an ID # for new item or \
"E" to return: ')

                if new_product_id == 'E':
                    break
                for id_num in database.db:
                    if id_num == new_product_id:
                        print('\n'*100)
                        print(f'\nID # {id_num} already exists as seen below:\
\n\nitem: {database.db[id_num][0]} | ID #: {id_num}\n\nPlease delete \
existing item or choose another ID.\n')
                        new_product_continue = False
                        break
                if new_product_continue == True:
                    new_product_name = input('\nPlease enter a name for this \
item: ')
                    while True:
                        try:
                            new_product_price = float(input(f'\nPlease enter a\
 price for "{new_product_name}": $'))
                        except:
                            print('\nPlease enter a numerical value for \
price.')
                        else:
                            break
                    while True:
                        try:
                            new_product_qty = int(input(f'\nPlease enter an \
initial qty for "{new_product_name}": '))
                        except:
                            print('\nPlease enter an integer for initial qty.')
                        else:
                            if new_product_qty >= 0:
                                break
                    database.set(new_product_id, [new_product_name, \
                                                  new_product_price, \
                                                  new_product_qty])
                    print('\n'*100)
                    print(f'\n"{new_product_name}" has been added to the \
system.\n')
                    break



def shell(database):
    '''shell to run the program'''
    while True:
        print('\n'*100)
        print('**********************************\n\nWelcome to N.A.T.E. \
Inventory Tracking System\n\n**********************************\n\n\n\n')
        print('"1" to add a new product\n\n"2" for existing file maintenance\
\n\n"3" to see total inventory value\n\n"Q" to QUIT')

        user_selection = input('\nPlease select an option: ')

        if user_selection == 'Q':
            database.dumpdb()
            break

        elif user_selection == '1':
            print('\n'*100)
            add_product(database)

        elif user_selection == '2':
            print('\n'*100)
            file_maintenance(database)

        elif user_selection == '3':
            print('\n'*100)
            print('\nThis will generate a report that will provide total \
inventory value across all products.\n')
            while True:
                full_inv_report = input('Would you like to continue and run \
the report? "Y" to continue: ')
                if full_inv_report == 'Y':
                    print('\n'*100)
                    print('\nReport generated: \n\n')
                    total_value(database)

                else:
                    break
        else:
            print('Not a valid selection.')

my_inv_db = InvDB("./my_database.db")
my_inv_db.load("./my_database.db")
my_inv_db.dumpdb()
my_inv_db._load()

shell(my_inv_db)
