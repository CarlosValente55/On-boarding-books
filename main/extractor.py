import os
import xml.etree.ElementTree as ET
from model.db import Country, Db
import re
from main.utils import database_log


class Extractor():
    def __init__(self, list_of_books=["all"]):
        self.list_of_books = list_of_books
        self.file_path = os.path.abspath(os.getcwd()+'/data')
        self.country_path = None
        self.record_reference = None
        self.fetch_tags = ['CountriesIncluded', 'x449']

    def export_sales_information(self, infoLogging=True):
        # Iterates over the books selected
        for book_path in self.extract_selected_files():
            root = ET.parse(book_path).getroot()
            # Calculate the path until the Countries Tags
            self.find_countries_path(root, [])
            # If a path to Countries Tags was found
            if self.country_path is not None:
                # Loop through xml elements using the path calculated
                for element in self.country_path[1::]:
                    root = root.find(element)

                self.__extract_countries(infoLogging, root, book_path)
                self.country_path = None

    def extract_selected_files(self):
        # If cli command is set up to extract from all books
        if self.list_of_books[0] == 'all':
            for file in os.listdir(self.file_path):
                yield(self.file_path+'/'+file)
        # If cli command is set up to extract from certain book(s)
        else:
            for book in self.list_of_books:
                yield(self.file_path+'/'+book)

    def __extract_countries(self, infoLogging, root, book_path):
        # Iterate through the list of Countries of this book
        for i, country in enumerate(self.__format_countries(root.text)):
            # Creates a Country Instance to be stored
            self.country = Country(self.record_reference, country)
            self.country.store(self.country)
            # Saves the new Book to be stored in the db
            response = self.country.close_and_save()
            # If infoLogging was selected in the CLI
            if infoLogging:
                database_log(response, country, self.record_reference, book_path.split(
                    '/')[-1], i+1, len(self.__format_countries(root.text)))

    def __format_countries(self, countries):
        if countries:
            countries = re.sub('\s', ' ', countries)
            return countries.split()

    def find_countries_path(self, root, onix_path):
        """ Recursive Depth First Search Function to calculate the path to Countries and also the record_reference
            Args:
                1- Root- Is the xml element that is being iterated.
                2- Onix_path- Is the list of elements to reach country tags
        """
        # If the xml element is one of the country tags(short or long)
        if root.tag in self.fetch_tags:
            onix_path.append(root.tag)
            self.country_path = list(onix_path)
        if root.tag == 'a001':
            self.record_reference = root.text
        if list(root):
            onix_path.append(root.tag)
            self.find_countries_path(list(root)[0], onix_path)
            for i in range(1, len(list(root))):
                self.find_countries_path(list(root)[i], onix_path)
            del onix_path[-1]
        else:
            return onix_path
