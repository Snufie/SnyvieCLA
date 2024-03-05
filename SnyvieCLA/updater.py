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
        self.update()

    def update(self):
        url = f"https://github.com/Snufie/SnyvieCLA/archive/refs/tags/{self.Fversion}.zip"  # replace with your GitHub repo URL
        response = requests.get(url)
        with open(f'SnyvieCLA-{self.Fversion}.zip', 'wb') as file:
            file.write(response.content)

        with zipfile.ZipFile(f'SnyvieCLA-{self.Fversion}.zip', 'r') as zip_ref:
            zip_ref.extractall(f'SnyvieCLA-{self.Fversion}')

        script_dir = os.path.dirname(os.path.realpath(__file__))  # get the script directory

        for filename in os.listdir(f'SnyvieCLA-{self.Fversion}/SnyvieCLA-{self.Fversion}'):  # replace 'repo' with your repo name
            if filename != 'updater.py':
                old_file_path = os.path.join(script_dir, filename)
                if os.path.exists(old_file_path):
                    if os.path.isdir(old_file_path):
                        shutil.rmtree(old_file_path)
                    else:
                        os.remove(old_file_path)
                shutil.move(f'SnyvieCLA-{self.Fversion}/SnyvieCLA-{self.Fversion}/{filename}', old_file_path)

        os.remove(f'SnyvieCLA-{self.Fversion}.zip')
        shutil.rmtree(f'SnyvieCLA-{self.Fversion}')