import requests
from bs4 import BeautifulSoup as bs
import csv
import re


def extrair_area_numerica(area_texto):
    """Converte área de texto (ex: '300,00 m²') para número."""
    if not area_texto or area_texto == 'N/A':
        return None
    # Remove ' m²' e substitui separadores
    area_num = area_texto.replace(' m²', '').replace('.', '').replace(',', '.')
    try:
        return float(area_num)
    except:
        return None


def extrair_dados_imovel(listing):
    """Extrai dados de um imóvel da listagem HTML."""
    name_tag = listing.find('meta', itemprop='name')
    address_tag = listing.find('span', class_='endereco')
    price_tag = listing.find('meta', itemprop='price')
    area_tag = listing.find('li', title='Área total')
    neighborhood_tag = listing.find('span', class_='bairro')
    url_tag = listing.find('link', itemprop='url')
    
    area_texto = area_tag.text.strip() if area_tag else 'N/A'
    preco = float(price_tag['content']) if price_tag else 0
    area_num = extrair_area_numerica(area_texto)
    
    # Calcular preço médio (preço por m²)
    preco_medio = round(preco / area_num, 2) if area_num and area_num > 0 else None
    
    return {
        'Nome': name_tag['content'] if name_tag else 'N/A',
        'Endereco': address_tag.text.strip() if address_tag else 'N/A',
        'Preco': preco,
        'Area': area_texto,
        'Preco_medio': preco_medio,
        'Bairro': neighborhood_tag.text.strip() if neighborhood_tag else 'N/A',
        'Url': url_tag['href'] if url_tag else 'N/A'
    }


def scrape_imoveis(estado, cidade, bairro=None, max_paginas=5):
    """Scrape de terrenos com parâmetros configuráveis."""
    
    # Construir URL baseado nos parâmetros
    if bairro:
        url_base = f"https://www.infoimoveis.com.br/busca/venda/terreno/{estado}/{cidade}/{bairro}"
    else:
        url_base = f"https://www.infoimoveis.com.br/busca/venda/terreno/{estado}/{cidade}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    all_properties = []
    
    print(f"\n{'='*60}")
    print(f"Iniciando scraping...")
    print(f"Estado: {estado.upper()}")
    print(f"Cidade: {cidade.replace('-', ' ').title()}")
    if bairro:
        print(f"Bairro: {bairro.replace('-', ' ').title()}")
    print(f"Páginas: 1 até {max_paginas}")
    print(f"{'='*60}\n")
    
    for page in range(1, max_paginas + 1):
        print(f"Coletando página {page}...")
        
        url = f"{url_base}?pagina={page}"
        response = requests.get(url, headers=headers)
        soup = bs(response.content, 'html.parser')
        listings = soup.find_all('li', class_='li-item')
        
        if not listings:
            print(f"  → Nenhum imóvel encontrado. Parando.")
            break
        
        for listing in listings:
            all_properties.append(extrair_dados_imovel(listing))
        
        print(f"  → {len(listings)} imóveis encontrados")
    
    print(f"\n{'='*60}")
    print(f"Total: {len(all_properties)} imóveis")
    print(f"{'='*60}\n")
    
    # Salvar em CSV
    if all_properties:
        # Gerar nome do arquivo baseado nos parâmetros
        if bairro:
            filename = f'Scrape_{cidade}_{bairro}.csv'
        else:
            filename = f'Scrape_{cidade}.csv'
            
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['Nome', 'Endereco', 'Preco', 'Area', 'Preco_medio', 'Bairro', 'Url'])
            writer.writeheader()
            writer.writerows(all_properties)
        print(f"Dados salvos em: {filename}")
    else:
        print("Nenhum imóvel encontrado.")
    
    return all_properties


def main():
    """Interface interativa para configurar o scraping."""
    print("\n" + "="*60)
    print("SCRAPER DE IMÓVEIS - INFOIMOVEIS.COM.BR")
    print("="*60 + "\n")
    
    # Input estado
    estado = input("Digite o estado (ex: ms, sp, rj): ").strip().lower()
    
    # Input cidade
    cidade = input("Digite a cidade (ex: campo-grande, sao-paulo): ").strip().lower()
    
    # Input bairro (opcional)
    bairro_input = input("Digite o bairro (deixe vazio para buscar toda a cidade): ").strip().lower()
    bairro = bairro_input if bairro_input else None
    
    # Input número de páginas
    while True:
        try:
            max_paginas = int(input("Digite o número máximo de páginas (ex: 5): ").strip())
            if max_paginas > 0:
                break
            else:
                print("Por favor, digite um número maior que 0.")
        except ValueError:
            print("Por favor, digite um número válido.")
    
    # Executar scraping
    scrape_imoveis(estado, cidade, bairro, max_paginas)


if __name__ == "__main__":
    main()


