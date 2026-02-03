import requests
from bs4 import BeautifulSoup as bs

def get_sao_francisco_data():
    url = "https://www.infoimoveis.com.br/busca/venda/terreno/ms/campo-grande/sao-francisco?pagina={page}"
    
    # Teste uma pagina
    page = 1
    
    # Header pra simular um navegador
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url.format(page=page), headers=headers)
    print(f"Status Code: {response.status_code}")
    
    soup = bs(response.content, 'html.parser')
    
    # Debug: Verifica container principal
    listagem_div = soup.find('div', id='listagemV2')
    print(f"Achou listagemV2 div: {listagem_div is not None}")
    
    # Acha todas as listagens
    all_listings = soup.find_all('li', class_='li-item')
    print(f"Achou {len(all_listings)} listagens")
    
    
    # Acha primeira listagem
    if all_listings:
        listing = all_listings[0]
    
        # Extrai dados 
        name = listing.find('meta', itemprop='name')['content'] if listing.find('meta', itemprop='name') else 'N/A'
        
        address_tag = listing.find('span', class_='endereco')
        address = address_tag.text.strip() if address_tag else 'N/A'
        
        price_tag = listing.find('meta', itemprop='price')
        price = float(price_tag['content']) if price_tag else 0
        
        area_tag = listing.find('li', title='Área total')
        area = area_tag.text.strip() if area_tag else 'N/A'
        
        neighborhood_tag = listing.find('span', class_='bairro')
        neighborhood = neighborhood_tag.text.strip() if neighborhood_tag else 'N/A'
        
        url_tag = listing.find('link', itemprop='url')
        property_url = url_tag['href'] if url_tag else 'N/A'
        
        # Printa o resultado
        print(f"Nome: {name}")
        print(f"Endereço: {address}")
        print(f"Preço: R$ {price:,.2f}")
        print(f"Área: {area}")
        print(f"Bairro: {neighborhood}")
        print(f"URL: {property_url}")
    else:
        print("No listing found")

if __name__ == "__main__":
    get_sao_francisco_data()


