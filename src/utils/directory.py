def get_musics(path):
    import os
    
    extensions = (".mp3", "m4a")
    musics = []
    
    if not os.path.exists(path):
        return []
    
    for root, dir, files in os.walk(path):
        for file in files:
            if file.lower().endswith(extensions):
                musics.append(os.path.join(root, file))
    return musics