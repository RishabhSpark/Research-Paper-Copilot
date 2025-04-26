import requests

def fetch_pmc_full_paper(pmcid):
    base_url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi'

    params = {
        'db': 'pmc',
        "id": pmcid,
        'retmode': 'text'
    }

    response = requests.get(base_url, params)
    response.raise_for_status()
    return response.text