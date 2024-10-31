from pepperpy.file import read_json, write_json, read_csv, write_csv

def demonstrate_file_operations():
    # Exemplo com JSON
    data = {
        "nome": "Pepperpy",
        "versão": "1.0.0",
        "configurações": {
            "debug": True,
            "log_level": "INFO"
        }
    }
    
    write_json(data, "config_example.json")
    loaded_json = read_json("config_example.json")
    print("📄 Dados JSON carregados:", loaded_json)
    
    # Exemplo com CSV
    csv_data = [
        ["Nome", "Idade", "Cidade"],
        ["João", "30", "São Paulo"],
        ["Maria", "25", "Rio de Janeiro"]
    ]
    
    write_csv(csv_data, "dados_example.csv")
    loaded_csv = read_csv("dados_example.csv")
    print("📊 Dados CSV carregados:", loaded_csv)

if __name__ == "__main__":
    demonstrate_file_operations() 