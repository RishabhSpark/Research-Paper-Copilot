import xml.etree.ElementTree as ET

def get_full_text(element):
    """Recursively extracts all text inside an XML element, including nested tags."""
    text_parts = []
    
    if element.text:
        text_parts.append(element.text)
    
    for child in element:
        text_parts.append(get_full_text(child))
        if child.tail:
            text_parts.append(child.tail)
    
    return ''.join(text_parts)

def extract_text_from_pmc_xml(xml_text):
    """Extracts text from the XML files, and formats it nicely."""
    root = ET.fromstring(xml_text)
    body = root.find('.//body')
    if body is None:
        print("No body found in XML.")
        return ""

    def process_section(section, level=1):
        output = []
        
        title_elem = section.find('title')
        if title_elem is not None:
            title_text = get_full_text(title_elem).strip()
            if title_text:
                if level == 1:
                    output.append(f"\n**{title_text.upper()}**")
                elif level == 2:
                    output.append(f"\n**{title_text}**")
                else:
                    output.append(f"\n**{title_text}**")

        # Extract paragraphs
        for elem in section:
            if elem.tag == 'p':
                para_text = get_full_text(elem).strip()
                if para_text:
                    output.append(f"{para_text}")
            elif elem.tag == 'sec':
                output.append(process_section(elem, level + 1))

        return "\n\n".join(output)

    return process_section(body)