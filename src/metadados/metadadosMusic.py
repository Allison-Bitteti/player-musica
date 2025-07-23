import os
from mutagen import File
from mutagen.id3 import ID3, APIC

def get_capaAlbum(music_path: str) -> str:
    try:
        audio = File(music_path)
        if audio is None:
            raise Exception("Arquivo inválido")

        if audio.tags is not None and isinstance(audio.tags, ID3):
            for tag in audio.tags.values():
                if isinstance(tag, APIC):
                    # Salva a capa extraída como imagem temporária
                    capa_path = os.path.join("temp_capa.jpg")
                    with open(capa_path, "wb") as f:
                        f.write(tag.data)
                    return capa_path

    except Exception as e:
        print(f"Erro ao obter capa de {music_path}: {e}")
    
    # Caminho da imagem padrão (use o caminho correto no seu projeto)
    return r"assets\default_album.png"
