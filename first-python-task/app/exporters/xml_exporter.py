from xml.etree.ElementTree import Element, SubElement, ElementTree
from app.exporters.base_exporter import BaseExporter

class XmlExporter(BaseExporter):
    def export(self, data: dict, output_path: str):
        root = Element("results")

        for section, rows in data.items():
            section_el = SubElement(root, section)

            for row in rows:
                item_el = SubElement(section_el, "item")
                for key, value in row.items():
                    field = SubElement(item_el, key)
                    field.text = str(value)

        tree = ElementTree(root)
        tree.write(output_path, encoding="utf-8", xml_declaration=True)