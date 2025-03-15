import shutil
import os

folders_to_delete = ['build', 'dist']
egg_info_dirs = [d for d in os.listdir() if d.endswith('.egg-info')]

for folder in folders_to_delete + egg_info_dirs:
    if os.path.exists(folder):
        print(f"Deleting {folder}...")
        shutil.rmtree(folder)
