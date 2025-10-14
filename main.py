import pandas as pd
import os

def main():
    # Caminho para o arquivo CSV
    csv_path = os.path.join('dataset', 'jewelry.csv')
    
    # Definindo as colunas do CSV
    columns = [
        'Date', 'OrderID', 'ProductID', 'Quantity', 'CategoryID', 
        'JewelleryType', 'BrandID', 'Price', 'UserID', 'Gender', 
        'BoxColour', 'Metal', 'Gem'
    ]
    
    try:
        # Lendo o arquivo CSV com pandas
        df = pd.read_csv(csv_path, names=columns, header=None)
        
        print(f"Arquivo CSV carregado com sucesso!")
        print(f"Número de linhas: {len(df)}")
        print(f"Número de colunas: {len(df.columns)}")
        
        print("\nPrimeiras 5 linhas:")
        print(df.head())
        
        print("\nInformações sobre o dataset:")
        print(df.info())
        
        print("\nEstatísticas descritivas das colunas numéricas:")
        print(df.describe())
        
        print("\nValores únicos por coluna:")
        for column in df.columns:
            unique_count = df[column].nunique()
            print(f"  {column}: {unique_count} valores únicos")
        
        return df
        
    except FileNotFoundError:
        print(f"Erro: Arquivo {csv_path} não encontrado.")
        return None
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        return None

if __name__ == "__main__":
    dataset = main()