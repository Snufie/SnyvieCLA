import json
from datetime import datetime, timedelta
import os
import inspect
import requests

CURRENT_VERSION = "v1.0.3"

class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

class Agenda:
    def __init__(self) -> None:
        pass

    def create(
        self,
        name: str,
        description: str,
        date: datetime,
        repeat: bool,
        saveto: str = "default",
    ):
        self.entry = {
            "name": name,
            "description": description,
            "date": date,
            "repeat": repeat,
        }
        if not os.path.exists(f"SnyvieCLA/{saveto}.json"):
            try:
                with open(f"SnyvieCLA/savefiles.json", "w+") as f:
                    data = json.load(f)
                    data["entries"].append(saveto)
                    f.seek(0)
                    json.dump(data, f, indent=4)
            except Exception as e:
                print(e)
        self.save(saveto)

    def save(self, saveTo):
        print(saveTo)
        try:
            with open(f"SnyvieCLA/{saveTo}.json", "r+") as f:
                data = json.load(f)
                print("data:", data)
                if not data:
                    data = {"entries": []}
                data["entries"].append(self.entry)
                f.seek(0)
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"error: {e}")

    def remove(self, name: str, savedAt: str = "default"):
        with open(f"SnyvieCLA/{savedAt}.json", "r+") as f:
            data = json.load(f)
            for i in data["entries"]:
                if i["name"] == name:
                    data["entries"].remove(i)
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

    def removeAll(self, saveFile: str = "default"):
        choice = input("Are you sure you want to delete all entries? (y/N) ").lower()
        if choice in ["yes", "y"]:
            os.remove(f"SnyvieCLA/{saveFile}.json")
        elif choice in ["no", "n", ""]:
            print("Aborted")
            
    def formatDate(self, days: int):
        if days >= 30:
            months = days // 30
            remainder = int((months*30)-days)
            if months == 1:
                ext = ""
            else:
                ext = "s"
            if remainder == 1:
                ext2 = ""
            elif remainder == 0:
                return f"{months} month{ext}"
            else:
                ext2 = "s"
            return f"{months} month{ext} and {remainder} day{ext2}"
        else:
            return

    def nearing(self, span: int = 1):
        savefiles = []
        with open(f"SnyvieCLA/savefiles.json", "r+") as f:
            data = json.load(f)
            for i in data["entries"]:
                savefiles.append(i)
            for i in savefiles:
                with open(f"SnyvieCLA/{i}", "r+") as f:
                    data = json.load(f)
                    for i in (data["entries"]):
                        entry_date = datetime.strptime(i["date"], "%Y-%m-%d").date()
                        days_left = (entry_date - datetime.now().date()).days
                        if 0 <= days_left <= span:
                            if days_left == 0:
                                due = "today"
                            elif days_left == 1:
                                due = "tomorrow"
                            else:
                                due = f"in {days_left} days"
                            print(f"{bcolors.HEADER}{i["name"]}{bcolors.ENDC}")
                            print(i["description"])
                            print(i["date"])
                            print(i["repeat"])
                            print(f"Due {due}")       
    
    def passed(self):
        savefiles = []
        with open(f"SnyvieCLA/savefiles.json", "r+") as f:
            data = json.load(f)
            for i in data["entries"]:
                savefiles.append(i)
            try:
                for i in savefiles:
                    with open(f"SnyvieCLA/{i}", "r+") as f:
                        data = json.load(f)
                        for i in (data["entries"]):
                            entry_date = datetime.strptime(i["date"], "%Y-%m-%d").date()
                            days_passed = (datetime.now().date() - entry_date).days
                            if days_passed > 0:
                                passed = self.formatDate(days_passed)
                                if passed == None:
                                    passed = f"{days_passed} days"
                                print(f"{bcolors.HEADER}{i["name"]}{bcolors.ENDC}")
                                print(i["description"])
                                print(i["date"])
                                print(i["repeat"])
                                print(f"{bcolors.FAIL}{passed} ago{bcolors.ENDC}")
            except Exception as e:
                if savefiles == []:
                    print("No entries found")
                else:
                    print(e)
                    with open(f"SnyvieCLA/default.json", "w") as f:
                        f.write('{"entries": []}')
                    print("Save files are corrupted. Default save file has been created")

class PyCLI():
    def __init__(self) -> None:
        pass
    
    def createPy(self):
        code = input("")
        with open("snyPy.py", "w") as f:
            f.write(code)
        print("File created")
        try:
            import snyPy as snoopy
            snyPy()
        except Exception as e:
            print(e)

        
def check_functions():
    functions = []
    class_names = [name for name, obj in globals().items() if isinstance(obj, type)]
    classes = []
    for name in class_names:
        obj = globals()[name]
        module = inspect.getmodule(obj)
        if module is not None:
            module_name = module.__name__
            if module_name == "snyvie":
                classes.append((name, module_name))
    for class_name, module_name in classes:
        class_obj = globals()[class_name]
        class_functions = inspect.getmembers(class_obj, predicate=inspect.isfunction)
        for function_name, _ in class_functions:
            if function_name != "__init__":
                functions.append((function_name, class_name))
    return functions

class AppInit():
    def __init__(self) -> None:
        self.start()
        checkUpdates()
        return

    def start(self):
        date = datetime.today().date()
        tomorrow = date + timedelta(days=1)
        print(f"date: {date}\ntomorrow: {tomorrow}")
    
    def exit(self):
        exit()

   
def checkUpdates():
        print("Checking for updates")
        response = requests.get("https://api.github.com/repos/Snufie/SnyvieCLA/releases/latest", headers={"Accept": "application/vnd.github.v3+json"})
        latest_release = response.json()['tag_name'], response.json()['published_at'], response.json()['body']
        print(latest_release)


