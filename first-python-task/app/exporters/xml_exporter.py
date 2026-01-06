import os
from xml.etree.ElementTree import Element, SubElement, ElementTree, tostring
from xml.dom import minidom
from app.exporters.base_exporter import BaseExporter


class XmlExporter(BaseExporter):
    def export(self, data: list[dict], output_path: str):
        root_name = os.path.basename(output_path).replace(".xml", "")
        root = Element(root_name)

        if not data:
            empty_item = SubElement(root, "item")
            note = SubElement(empty_item, "note")
            note.text = "No data"

        for row in data:
            item_el = SubElement(root, "item")
            for key, value in row.items():
                field = SubElement(item_el, key)
                field.text = str(value) if value is not None else ""
                
        rough_string = tostring(root, encoding='utf-8')

        reparsed = minidom.parseString(rough_string)
        pretty_xml = reparsed.toprettyxml(indent="  ", encoding="utf-8").decode("utf-8")

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(pretty_xml)