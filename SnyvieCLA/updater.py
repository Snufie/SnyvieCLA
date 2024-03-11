import os
import requests
import shutil
import zipfile

script_dir = os.path.dirname(os.path.realpath(__file__))  # get the script directory
print(script_dir)

class Updater():
    def __init__(self, version):
        self.version = version
        self.Fversion = version.replace('v', '')
        print(self.Fversion)
        self.update()

    def update(self):
        url = f"https://github.com/Snufie/SnyvieCLA/archive/refs/tags/{self.version}.zip"  # replace with your GitHub repo URL
        response = requests.get(url)
        with open(f'SnyvieCLA-{self.Fversion}.zip', 'wb') as file:
            file.write(response.content)
            print(response.content)

        with zipfile.ZipFile(f'SnyvieCLA-{self.Fversion}.zip', 'r') as zip_ref:
            zip_ref.extractall(f'SnyvieCLA-{self.Fversion}')  # Extract files in the specified directory
            print(zip_ref.namelist())

        script_dir = os.path.dirname(os.path.realpath(__file__))  # get the script directory

        for root, dirs, files in os.walk(f'SnyvieCLA-{self.Fversion}'):  # replace 'repo' with your repo name
            for filename in files:
                if filename != 'updater.py':
                    old_file_path = os.path.join(script_dir, filename)
                    new_file_path = os.path.join(root, filename)
                    if os.path.exists(old_file_path):
                        os.remove(old_file_path)
                    shutil.move(new_file_path, script_dir)

        os.remove(f'SnyvieCLA-{self.Fversion}.zip')
        shutil.rmtree(f'SnyvieCLA-{self.Fversion}')