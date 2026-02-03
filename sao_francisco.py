import requests
from bs4 import BeautifulSoup as bs
import csv


def extrair_dados_imovel(listing):
    """Extrai dados de um imóvel da listagem HTML."""
    name_tag = listing.find('meta', itemprop='name')
    address_tag = listing.find('span', class_='endereco')
    price_tag = listing.find('meta', itemprop='price')
    area_tag = listing.find('li', title='Área total')
    neighborhood_tag = listing.find('span', class_='bairro')
    url_tag = listing.find('link', itemprop='url')
    
    return {
        'Nome': name_tag['content'] if name_tag else 'N/A',
        'Endereco': address_tag.text.strip() if address_tag else 'N/A',
        'Preco': float(price_tag['content']) if price_tag else 0,
        'Area': area_tag.text.strip() if area_tag else 'N/A',
        'Bairro': neighborhood_tag.text.strip() if neighborhood_tag else 'N/A',
        'Url': url_tag['href'] if url_tag else 'N/A'
    }


def get_sao_francisco_data():
    """Scrape de terrenos do bairro São Francisco."""
    url = "https://www.infoimoveis.com.br/busca/venda/terreno/ms/campo-grande/sao-francisco?pagina={page}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    all_properties = []
    
    for page in range(1, 5):
        print(f"Coletando página {page}...")
        
        response = requests.get(url.format(page=page), headers=headers)
        soup = bs(response.content, 'html.parser')
        listings = soup.find_all('li', class_='li-item')
        
        for listing in listings:
            all_properties.append(extrair_dados_imovel(listing))
        
        print(f"  → {len(listings)} imóveis encontrados")
    
    print(f"\nTotal: {len(all_properties)} imóveis")
    
    # Salvar em CSV
    if all_properties:
        filename = 'Scrape.csv'
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['Nome', 'Endereco', 'Preco', 'Area', 'Bairro', 'Url'])
            writer.writeheader()
            writer.writerows(all_properties)
        print(f"Dados salvos em: {filename}")
    else:
        print("Nenhum imóvel encontrado.")
    
    return all_properties

if __name__ == "__main__":
    get_sao_francisco_data()


