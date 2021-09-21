"""Change default NCS/NSO settings."""
import xml.etree.ElementTree as ET

print("⚙️⚙️⚙️ Tunning 'ncs.conf'")

ns = {"xmlns": "http://tail-f.com/yang/tailf-ncs-config"}

parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True))
tree = ET.parse("ncs.conf", parser=parser)
root = tree.getroot()
ET.register_namespace("xmlns", "http://tail-f.com/yang/tailf-ncs-config")

# turn off PAM authentication
pam_enabled = root.find("./xmlns:aaa/xmlns:pam/xmlns:enabled", ns)
if pam_enabled is not None:
    print(f"Old settings: {pam_enabled.text.lower()=}")
pam_enabled.text = "false"

# change CLI to cisco style
style = root.find("./xmlns:cli/xmlns:style", ns)
if style is not None:
    print(f"Old settings: {style.text.lower()=}")
else:
    print("'./xmlns:cli/xmlns:style' node doesn't exist, adding...")
    cli = root.find("./xmlns:cli", ns)
    style = ET.SubElement(cli, "xmlns:style")
style.text = "c"

print(f"New settings: {pam_enabled.text=}")
print(f"New settings: {style.text=}")

tree.write(
    file_or_filename="ncs.conf",
    xml_declaration=None,
    method="xml",
    short_empty_elements=False,
    default_namespace=None,
)
