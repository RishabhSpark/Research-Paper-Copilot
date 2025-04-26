import requests
import xml.etree.ElementTree as ET
from typing import List

def fetch_pmc_papers(query: str, top_k: int = 5) -> List[str]:
    search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    esummary_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

    pmc_ids = []
    total_checked = 0
    retstart = 0
    batch_size = 50

    while len(pmc_ids) < top_k:
        search_params = {
            'db': 'pubmed',
            'term': query,
            'retstart': retstart,
            'retmax': batch_size,
            'retmode': 'xml'
        }
        search_response = requests.get(search_url, params=search_params)
        if search_response.status_code != 200:
            raise Exception(f"Failed to search PubMed: {search_response.status_code}")

        search_root = ET.fromstring(search_response.text)
        id_list = [id_elem.text for id_elem in search_root.findall(".//Id")]

        if not id_list:
            print("No more papers to search.")
            break

        # esummary to get PMC IDs
        for i in range(0, len(id_list), 10): 
            batch_ids = id_list[i:i+10]
            esummary_params = {
                'db': 'pubmed',
                'id': ','.join(batch_ids),
                'retmode': 'xml'
            }
            esummary_response = requests.get(esummary_url, params=esummary_params)
            if esummary_response.status_code != 200:
                raise Exception(f"Failed to fetch esummary: {esummary_response.status_code}")

            summary_root = ET.fromstring(esummary_response.text)

            for docsum in summary_root.findall('.//DocSum'):
                total_checked += 1
                article_ids = docsum.find('.//Item[@Name="ArticleIds"]')
                pmc_id = None
                if article_ids is not None:
                    for item in article_ids.findall('Item'):
                        if item.attrib.get('Name') == 'pmc':
                            pmc_id = item.text
                            break

                if pmc_id:
                    pmc_ids.append(pmc_id)

                if len(pmc_ids) >= top_k:
                    break
            if len(pmc_ids) >= top_k:
                break

        retstart += batch_size

    print(f"Searched {total_checked} papers. Found {len(pmc_ids)} papers with PMC IDs.")
    return pmc_ids