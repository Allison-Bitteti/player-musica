import json

def carregar_configuracoes(caminho="config.json"):
    try:
        with open(caminho, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "pasta_padrao": "",
        }
        
def salvar_configuracoes(config, caminho="config.json"):
    with open(caminho, "w") as f:
        json.dump(config, f, indent=4)