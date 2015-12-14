from unittest import TestCase, main
# custom 
from unitparser import UnitParser
__author__ = 'chad nelson'
__project__ = 'blow dry css'


class TestUnitParser(TestCase):
    def test_add_units_multi_value_conversion_True_invalid_pass_through(self):
        # Handles cases input like: '1a2', '-35mx 15mx', '1px 2 m11 2', '22.5px 10 22.5px 10'
        # Outputs: '1a2', '-35mx 15mx', '0.0625em 0.125em m11 0.125em', '22.5px 0.625em 22.5px 0.625em'
        property_name = 'padding'
        property_values = ['1a2', '-35mx 15mx', '1px 2 m11 2', '22.5px 10 22.5px 10']
        expected_values = ['1a2', '-35mx 15mx', '0.0625em 0.125em m11 0.125em', '1.4062em 0.625em 1.4062em 0.625em']
        unit_parser = UnitParser(property_name=property_name, px_to_em=True)

        for i, value in enumerate(property_values):
            new_value = unit_parser.add_units(property_value=value)
            self.assertEqual(new_value, expected_values[i], msg=i)

    def test_add_units_multi_value_conversion_True(self):
        # Handles cases input like: '12.5', '-35 15', '1 2 1 2', '20% 20%', '5em 6em 5em 6em'
        # Outputs: '0.75em', '-35px 15px', '1px 2px 1px 2px', '20% 20%', '5em 6em 5em 6em'
        property_name = 'padding'
        property_values = ['12', '-35 15', '1 2 1 2', '20% 20%', '5em 6em 5em 6em']
        expected_values = [
            '0.75em', '-2.1875em 0.9375em', '0.0625em 0.125em 0.0625em 0.125em', '20% 20%', '5em 6em 5em 6em'
        ]
        unit_parser = UnitParser(property_name=property_name, px_to_em=True)

        for i, value in enumerate(property_values):
            new_value = unit_parser.add_units(property_value=value)
            self.assertEqual(new_value, expected_values[i], msg=i)

    def test_add_units_margin_top_conversion_True(self):
        property_name = 'margin-top'
        property_values = ['1', '-20.0', '15px', '60rem']
        expected_values = ['0.0625em', '-1.25em', '0.9375em', '60rem']
        unit_parser = UnitParser(property_name=property_name, px_to_em=True)

        for i, value in enumerate(property_values):
            new_value = unit_parser.add_units(property_value=value)
            self.assertEqual(new_value, expected_values[i], msg=i)

    def test_add_units_multi_value_no_conversion(self):
        # Handles cases input like: '12', '-35 15', '1 2 1 2'
        # Outputs: '12px', '-35px 15px', '1px 2px 1px 2px'
        property_name = 'padding'
        property_values = ['12', '-35 15', '1 2 1 2', '20% 20%', '5em 6em 5em 6em']
        expected_values = ['12px', '-35px 15px', '1px 2px 1px 2px', '20% 20%', '5em 6em 5em 6em']
        unit_parser = UnitParser(property_name=property_name, px_to_em=False)

        for i, value in enumerate(property_values):
            new_value = unit_parser.add_units(property_value=value)
            self.assertEqual(new_value, expected_values[i], msg=i)

    def test_add_units_multi_value_conversion_True_strange_input(self):
        # Note that the cm, rem, and em cases are not handled intuitively causing the units to be mixed.
        # This still produces valid CSS.
        property_name = 'padding'
        property_values = ['-35rem 15', '3 4px 3px 5', '5em 6 5em 6', '1em 100 4cm 9rem']
        expected_values = [
            '-35rem 0.9375em', '0.1875em 0.25em 0.1875em 0.3125em', '5em 0.375em 5em 0.375em', '1em 6.25em 4cm 9rem'
        ]
        unit_parser = UnitParser(property_name=property_name, px_to_em=True)

        for i, value in enumerate(property_values):
            new_value = unit_parser.add_units(property_value=value)
            self.assertEqual(new_value, expected_values[i], msg=i)

    def test_add_units_multi_value_no_conversion_strange_input(self):
        # Note that the cm, rem and em cases are not handled intuitively causing the units to be mixed.
        # This still produces valid CSS.
        property_name = 'padding'
        property_values = ['-35rem 15', '3 4px 3px 5', '5em 6 5em 6', '1em 100 4cm 9rem']
        expected_values = ['-35rem 15px', '3px 4px 3px 5px', '5em 6px 5em 6px', '1em 100px 4cm 9rem']
        unit_parser = UnitParser(property_name=property_name, px_to_em=False)

        for i, value in enumerate(property_values):
            new_value = unit_parser.add_units(property_value=value)
            self.assertEqual(new_value, expected_values[i], msg=i)

    def test_add_units_margin_top_no_conversion(self):
        property_name = 'margin-top'
        property_values = ['1', '-20.0', '15px', '60rem']
        expected_values = ['1px', '-20.0px', '15px', '60rem']
        unit_parser = UnitParser(property_name=property_name, px_to_em=False)

        for i, value in enumerate(property_values):
            new_value = unit_parser.add_units(property_value=value)
            self.assertEqual(new_value, expected_values[i], msg=i)

    def test_add_units_margin_top_no_conversion_invalid_units(self):
        # Expect the values to pass through unchanged.
        property_name = 'margin-top'
        property_values = ['1um', '-20.0no', '15txt', '60st']
        unit_parser = UnitParser(property_name=property_name, px_to_em=False)

        for value in property_values:
            new_value = unit_parser.add_units(property_value=value)
            self.assertEqual(new_value, value, msg=value)

    def test_add_units_margin_top_conversion_True_invalid_units(self):
        # Expect the values to pass through unchanged.
        property_name = 'margin-top'
        property_values = ['12aou', '-35oeu 15ou', '1ou 2oeu 1ou 2ou', '20i 20u*', '5e 6m 5e 6m']
        unit_parser = UnitParser(property_name=property_name, px_to_em=True)

        for value in property_values:
            new_value = unit_parser.add_units(property_value=value)
            self.assertEqual(new_value, value, msg=value)

    def test_add_units_multi_value_no_conversion_invalid_units(self):
        # Expect the values to pass through unchanged.
        property_name = 'padding'
        property_values = ['12aou', '-35oeu 15ou', '1ou 2oeu 1ou 2ou', '20i 20u*', '5e 6m 5e 6m']
        unit_parser = UnitParser(property_name=property_name, px_to_em=False)

        for value in property_values:
            new_value = unit_parser.add_units(property_value=value)
            self.assertEqual(new_value, value, msg=value)

    def test_add_units_multi_value_conversion_True_invalid_units(self):
        # Expect the values to pass through unchanged.
        property_name = 'padding'
        property_values = ['1um', '-20.0no', '15txt', '60st']
        unit_parser = UnitParser(property_name=property_name, px_to_em=True)

        for value in property_values:
            new_value = unit_parser.add_units(property_value=value)
            self.assertEqual(new_value, value, msg=value)
    
    def test_px_to_em_typecast_string_input(self):
        unit_parser = UnitParser(base=16)
        for pixels in range(-1000, 1001):
            expected = round(pixels / unit_parser.base, 4)
            expected = str(expected) + 'em'
            actual = unit_parser.convert_px_to_em(pixels=str(pixels))       # typecast to string str()
            self.assertEqual(actual, str(expected), msg=pixels)


    def test_px_to_em_int_input(self):
        unit_parser = UnitParser(base=16)
        for pixels in range(-1000, 1001):
            expected = round(pixels / unit_parser.base, 4)
            expected = str(expected) + 'em'
            actual = unit_parser.convert_px_to_em(pixels=pixels)
            self.assertEqual(actual, str(expected), msg=pixels)

    def test_px_to_em_float_input(self):
        unit_parser = UnitParser(base=16)
        # Thank you: http://stackoverflow.com/questions/477486/python-decimal-range-step-value#answer-477506
        for pixels in range(-11, 11, 1):
            pixels /= 10.0
            expected = round(pixels / unit_parser.base, 4)
            expected = str(expected) + 'em'
            actual = unit_parser.convert_px_to_em(pixels=pixels)
            self.assertEqual(actual, str(expected), msg=pixels)

    def test_px_to_em_invalid_input(self):
        # Expect the value to pass through unchanged.
        unit_parser = UnitParser(base=16)
        invalid_inputs = ['cat', '11px', ' 234.8', 'n2_4p', '25deg', '16kHz', ]
        for invalid in invalid_inputs:
            expected = invalid
            actual = unit_parser.convert_px_to_em(pixels=invalid)
            self.assertEqual(actual, expected, msg=invalid)

    def test_px_to_em_change_base(self):
        unit_parser = UnitParser(base=48)
        for pixels in range(-1000, 1001):
            expected = round(pixels / unit_parser.base, 4)
            expected = str(expected) + 'em'
            actual = unit_parser.convert_px_to_em(pixels=pixels)
            self.assertEqual(actual, str(expected), msg=pixels)

    def test_px_to_em_string_base(self):
        unit_parser = UnitParser(base='480')
        for pixels in range(-1000, 1001):
            expected = round(pixels / unit_parser.base, 4)
            expected = str(expected) + 'em'
            actual = unit_parser.convert_px_to_em(pixels=pixels)
            self.assertEqual(actual, str(expected), msg=pixels)

    def test_px_to_em_Wrong_base(self):
        self.assertRaises(ValueError, UnitParser, base='wrong')


if __name__ == '__main__':
    main()


