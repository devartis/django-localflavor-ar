from __future__ import unicode_literals

from django_localflavor_ar.forms import (ARProvinceSelect,
    ARPostalCodeField, ARDNIField, ARCUITField)

from django.test import SimpleTestCase
from django_localflavor_ar.forms import ARPhoneNumberField


class ARLocalFlavorTests(SimpleTestCase):
    def test_ARProvinceSelect(self):
        f = ARProvinceSelect()
        out = '''<select name="provincias">
<option value="B">Buenos Aires</option>
<option value="K">Catamarca</option>
<option value="H">Chaco</option>
<option value="U">Chubut</option>
<option value="C">Ciudad Aut\xf3noma de Buenos Aires</option>
<option value="X">C\xf3rdoba</option>
<option value="W">Corrientes</option>
<option value="E">Entre R\xedos</option>
<option value="P">Formosa</option>
<option value="Y">Jujuy</option>
<option value="L">La Pampa</option>
<option value="F">La Rioja</option>
<option value="M">Mendoza</option>
<option value="N">Misiones</option>
<option value="Q">Neuqu\xe9n</option>
<option value="R">R\xedo Negro</option>
<option value="A" selected="selected">Salta</option>
<option value="J">San Juan</option>
<option value="D">San Luis</option>
<option value="Z">Santa Cruz</option>
<option value="S">Santa Fe</option>
<option value="G">Santiago del Estero</option>
<option value="V">Tierra del Fuego, Ant\xe1rtida e Islas del Atl\xe1ntico Sur</option>
<option value="T">Tucum\xe1n</option>
</select>'''
        self.assertHTMLEqual(f.render('provincias', 'A'), out)

    def test_ARPostalCodeField(self):
        error_format = ['Enter a postal code in the format NNNN or ANNNNAAA.']
        error_atmost = ['Ensure this value has at most 8 characters (it has 9).']
        error_atleast = ['Ensure this value has at least 4 characters (it has 3).']
        valid = {
            '5000': '5000',
            'C1064AAB': 'C1064AAB',
            'c1064AAB': 'C1064AAB',
            'C1064aab': 'C1064AAB',
            '4400': '4400',
            'C1064AAB': 'C1064AAB',
        }
        invalid = {
            'C1064AABB': error_atmost + error_format,
            'C1064AA': error_format,
            'C1064AB': error_format,
            '106AAB': error_format,
            '500': error_atleast + error_format,
            '5PPP': error_format,
        }
        self.assertFieldOutput(ARPostalCodeField, valid, invalid)

    def test_ARDNIField(self):
        error_length = ['This field requires 7 or 8 digits.']
        error_digitsonly = ['This field requires only numbers.']
        valid = {
            '20123456': '20123456',
            '20.123.456': '20123456',
            '20123456': '20123456',
            '20.123.456': '20123456',
            '20.123456': '20123456',
            '9123456': '9123456',
            '9.123.456': '9123456',
        }
        invalid = {
            '101234566': error_length,
            'W0123456': error_digitsonly,
            '10,123,456': error_digitsonly,
        }
        self.assertFieldOutput(ARDNIField, valid, invalid)

    def test_ARCUITField(self):
        error_format = ['Enter a valid CUIT in XX-XXXXXXXX-X or XXXXXXXXXXXX format.']
        error_invalid = ['Invalid CUIT.']
        error_legal_type = ['Invalid legal type. Type must be 27, 20, 23 or 30.']
        valid = {
            '20-10123456-9': '20-10123456-9',
            '20-10123456-9': '20-10123456-9',
            '27-10345678-4': '27-10345678-4',
            '20101234569': '20-10123456-9',
            '27103456784': '27-10345678-4',
            '30011111110': '30-01111111-0',
        }
        invalid = {
            '2-10123456-9': error_format,
            '210123456-9': error_format,
            '20-10123456': error_format,
            '20-10123456-': error_format,
            '20-10123456-5': error_invalid,
            '27-10345678-1': error_invalid,
            '27-10345678-1': error_invalid,
            '11211111110': error_legal_type,
        }
        self.assertFieldOutput(ARCUITField, valid, invalid)

    def test_ARPhoneNumberField(self):
        error_invalid = ['Invalid format. Phone format must be XXxx-XXxx-XXXX (lowercase digits are optional numbers).']

        valid = {
            '011-4899-5666': '011-4899-5666',
            '11-6898-1111': '11-6898-1111',
            '22-55-6546': '22-55-6546',
            '2266-55-6546': '2266-55-6546',
            '2266-5566-6546': '2266-5566-6546',
            '111-656-6489': '111-656-6489',
        }

        invalid = {
            '2-1012-3456': error_invalid,
            '21-0146-119': error_invalid,
            '11-01234567': error_invalid,
            '92-4444-': error_invalid,
            '99984-10-65': error_invalid,
            '-1034-5551': error_invalid,
            '27-1-1555': error_invalid,
            '255-499-99999': error_invalid,
        }

        self.assertFieldOutput(ARPhoneNumberField, valid, invalid)

