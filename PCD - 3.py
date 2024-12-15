from google.colab import drive
import gdown
import rasterio
import numpy as np

def main():
    
    drive.mount('/content/drive')

    
    url = 'https://drive.google.com/uc?export=download&id=1BrtGByxXu5xqBGOvSBmPWkb_YGZagHav'
    output = 'imagem_satellite.tif'

    
    gdown.download(url, output, quiet=False)

    
    total_pixels, pixels_sem_dados, pixels_soja, pixels_pastagem = processar_imagem(output)

    
    area_soja_ha, area_pastagem_ha = calcular_areas(pixels_soja, pixels_pastagem)

    
    exibir_resultados(total_pixels, pixels_sem_dados, pixels_soja, pixels_pastagem, area_soja_ha, area_pastagem_ha)

def processar_imagem(caminho):
    """Processa a imagem em blocos e retorna as contagens de pixels."""
    total_pixels = pixels_sem_dados = pixels_soja = pixels_pastagem = 0

    with rasterio.open(caminho) as src:
        for _, window in src.block_windows(1):
            dados = src.read(1, window=window)
            total_pixels += dados.size
            pixels_sem_dados += np.sum(dados == 0)
            pixels_soja += np.sum(dados == 39)
            pixels_pastagem += np.sum(dados == 15)

    return total_pixels, pixels_sem_dados, pixels_soja, pixels_pastagem

def calcular_areas(pixels_soja, pixels_pastagem):
    """Calcula áreas em hectares a partir das contagens de pixels."""
    resolucao_pixel_ha = (30 * 30) / 10000  
    area_soja_ha = pixels_soja * resolucao_pixel_ha
    area_pastagem_ha = pixels_pastagem * resolucao_pixel_ha

    return area_soja_ha, area_pastagem_ha

def exibir_resultados(total, sem_dados, soja, pastagem, area_soja, area_pastagem):
    """Exibe os resultados calculados."""
    print(f"Quantidade total de pixels: {total}")
    print(f"Quantidade de pixels sem dados (código 0): {sem_dados}")
    print(f"Quantidade de pixels de plantio de soja (código 39): {soja}")
    print(f"Quantidade de pixels de pastagem (código 15): {pastagem}")
    print(f"\nÁrea de plantio de soja: {area_soja:.2f} hectares, correspondendo a {soja} pixels")
    print(f"Área de cobertura de pastagem: {area_pastagem:.2f} hectares, correspondendo a {pastagem} pixels")


if __name__ == "__main__":
    main()