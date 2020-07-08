import click
from main.extractor import Extractor
from model.db import Country


@click.command()
@click.option('--book', '-b', default=['all'], multiple=True, help="Select the name of the file you want to extract countrys from.\n Eg: --book=1.xml       f")
@click.option('--log-info', '-lf', default=True, type=bool, help='Turn on or off the info logging. Eg: --log-info=true')
@click.option('--delete-table', '-dt', help='Select the name of the tables you want to delete. Eg: --delete-table=sales_rights')
def export_sales_information(book, log_info, delete_table):
    

    # If the cli captured a table to delete
    if delete_table:
        Country().delete_sales_rights_table(delete_table)
    Country().create_sales_rights_table()
    extractor = Extractor(book)
    extractor.export_sales_information(log_info)


if __name__ == '__main__':
    export_sales_information()
