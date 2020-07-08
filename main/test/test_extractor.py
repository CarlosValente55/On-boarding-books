import unittest
from ..extractor import Extractor
import xml.etree.ElementTree as ET

xml_doc = ET.Element('ONIXmessage')
product = ET.SubElement(xml_doc, 'product')
header = ET.SubElement(xml_doc, 'header')
reference = ET.SubElement(product, 'a001').text = '12345'
publishingdetail = ET.SubElement(product, 'publishingdetail')
salesrights = ET.SubElement(publishingdetail, 'salesrights')
territory = ET.SubElement(salesrights, 'territory')
country_long_tag = ET.SubElement(territory, 'x449').text = 'CA OG IT'


class TestExtractor(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.extractor = Extractor()
        self.extractor.find_countries_path(xml_doc, [])

    @classmethod
    def tearDownClass(self):
        pass

    def test__find_countries_included(self):
        # Tests if path was well extracted
        self.assertEqual(self.extractor.country_path, [
                         'ONIXmessage', 'product', 'publishingdetail', 'salesrights', 'territory', 'x449'])

    def test__find_reference(self):
        # Tests if record reference was well extracted
        self.assertEqual(self.extractor.record_reference, '12345')

    def test__format_countries(self):
        formated_countries = self.extractor._Extractor__format_countries(
            'AX      AL      DZ      AS      AD      AO      AI      AQ      AG')
        expected = ['AX', 'AL', 'DZ', 'AS', 'AD', 'AO', 'AI', 'AQ', 'AG']
        self.assertEqual(formated_countries, expected)
