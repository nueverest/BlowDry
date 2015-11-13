from cssutils.css import CSSStyleDeclaration, Property
from xml.dom import SyntaxErr
# Custom
from classpropertyparser import ClassPropertyParser
__author__ = 'chad nelson'
__project__ = 'blow dry css'


class CSSStyleBuilder(object):
    def __init__(self, property_parser=ClassPropertyParser()):
        print('\nCSSStyleBuilder Running:')
        self.property_parser = property_parser
        self.css_properties = set()
        self.css_style_declaration = CSSStyleDeclaration(cssText='')

        invalid_css_classes = []
        reasons = []
        for css_class in self.property_parser.class_set:
            name = self.property_parser.get_property_name(css_class=css_class)

            # 'name' can return an empty string '' if css_class does not match any patterns in the property_dict.
            try:
                encoded_property_value = self.property_parser.get_encoded_property_value(
                    property_name=name,
                    css_class=css_class
                )
            except ValueError:
                invalid_css_classes.append(css_class)
                reasons.append(' (property_name not found in self.property_dict.)')
                continue

            priority = self.property_parser.get_property_priority(css_class=css_class)
            value = self.property_parser.get_property_value(
                property_name=name,
                encoded_property_value=encoded_property_value,
                property_priority=priority      # TODO: Why is priority required???? Validation does not occur anymore.
            )
            # Build CSS Property AND Add to css_properties OR Remove invalid css_class from class_set.
            try:
                css_property = Property(name=name, value=value, priority=priority)
                if css_property.valid:
                    self.css_properties.add(css_property)
                else:
                    invalid_css_classes.append(css_class)
                    reasons.append(' (cssutils invalid property value: ' + value + ')')
                    continue
            except SyntaxErr:
                invalid_css_classes.append(css_class)
                reasons.append(' (cssutils SyntaxErr invalid property value: ' + value + ')')
                continue

        # Clean out invalid CSS Classes.
        for i, invalid_css_class in enumerate(invalid_css_classes):
            self.property_parser.class_set.remove(invalid_css_class)
            self.property_parser.removed_class_set.add(invalid_css_class + reasons[i])

        css_text = self.get_css_text()
        self.css_style_declaration.cssText = css_text

    def get_css_text(self):
        css_text = ''
        for css_property in self.css_properties:
            css_text += css_property.cssText + '; '
        return css_text
