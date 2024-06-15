import json
from datetime import datetime, timedelta
import os
import inspect
import requests
import updater as Updater

CURRENT_VERSION = "v1.1.8"

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
        date: str,
        repeat: bool,
        repeat_after_days: int,
        saveto: str = "default",
    ):
        date_obj = datetime.strptime(date, "%Y-%m-%d")  # convert string to datetime
        self.entry = {
            "name": name,
            "description": description,
            "date": date_obj.strftime("%Y-%m-%d"),  # use date_obj here
            "repeat": bool(repeat),
            "repeater": repeat_after_days,
        }
        if not os.path.exists(f"SnyvieCLA/data/{saveto}.json"):
            try:
                with open(f"SnyvieCLA/data/savefiles.json", "w+") as f:
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
            with open(f"SnyvieCLA/data/{saveTo}.json", "r+") as f:
                data = json.load(f)
                print(f"{data =}")
                if not data:
                    print(data)
                    data = {"entries": []}
                data["entries"].append(self.entry)
                f.seek(0)
                json.dump(data, f, indent=4)
        except FileNotFoundError:
            with open(f"SnyvieCLA/data/{saveTo}.json", "w") as f:
                data = {"entries": [self.entry]}
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"{e =}")
            
    def remove(self, name: str, savedAt: str = "default"):
        with open(f"SnyvieCLA/data/{savedAt}.json", "r+") as f:
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
            os.remove(f"SnyvieCLA/data/{saveFile}.json")
        elif choice in ["no", "n", ""]:
            print("Aborted")
            
    def formatDate(self, days: int):
        day_ext = month_ext = year_ext = ""
        years = months = 0
        if days >= 30:
            months = days // 30
            days = days % 30
        if months >= 12:
            years = months // 12
            months = months % 12
        time_parts = []
        if years > 0:
            year_ext = "year" if years == 1 else "years"
            time_parts.append(f"{years} {year_ext}")
        if months > 0:
            month_ext = "month" if months == 1 else "months"
            time_parts.append(f"{months} {month_ext}")
        if days > 0:
            day_ext = "day" if days == 1 else "days"
            time_parts.append(f"{days} {day_ext}")
        return ", ".join(time_parts)

    def nearing(self, span: int = 1):
        savefiles = []
        self.silent_passed()
        with open(f"SnyvieCLA/data/savefiles.json", "r+") as f:
            data = json.load(f)
            for i in data["entries"]:
                savefiles.append(i)
            for i in savefiles:
                with open(f"SnyvieCLA/data/{i}", "r+") as f:
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
                            print(i["repeater"])
                            print(f"Due {due}")       
    
    def silent_passed(self):
        savefiles = []
        try:
            with open(f"SnyvieCLA/data/savefiles.json", "r+") as f:
                data = json.load(f)
                for i in data["entries"]:
                    savefiles.append(i)
        except FileNotFoundError:
            with open(f"SnyvieCLA/data/savefiles.json", "w") as f:
                json.dump({"entries": []}, f)
            self.passed()  # call passed method here
            return
        except Exception as e:
            self.passed()  # call passed method here
            return

        for i in savefiles:
            try:
                with open(f"SnyvieCLA/data/{i}", "r+") as f:
                    data = json.load(f)
                    for i in (data["entries"]):
                        entry_date = datetime.strptime(i["date"], "%Y-%m-%d").date()
                        days_passed = (datetime.now().date() - entry_date).days
                        if days_passed > 0:
                            self.repeater(i["repeater"], days_passed, i['name'])
            except FileNotFoundError:
                with open(f"SnyvieClA/data/{i}", "w") as f:
                    json.dump({"entries": []}, f)
                self.passed()  # call passed method here
                return
            except Exception as e:
                self.passed()  # call passed method here
                return
    
    def passed(self):
        savefiles = []
        try:
            with open(f"SnyvieCLA/data/savefiles.json", "r+") as f:
                data = json.load(f)
                for i in data["entries"]:
                    savefiles.append(i)
        except FileNotFoundError:
            print(f"{bcolors.FAIL}Error: data/savefiles.json not found. Creating a new file...{bcolors.ENDC}")
            with open(f"SnyvieCLA/data/savefiles.json", "w") as f:
                json.dump({"entries": []}, f)
            return
        except Exception as e:
            print(f"{bcolors.FAIL}Error: {e}{bcolors.ENDC}")
            return

        for i in savefiles:
            try:
                with open(f"SnyvieClA/data/{i}", "r+") as f:
                    data = json.load(f)
                    for i in (data["entries"]):
                        entry_date = datetime.strptime(i["date"], "%Y-%m-%d").date()
                        days_passed = (datetime.now().date() - entry_date).days
                        if days_passed > 0:
                            passed = self.formatDate(days_passed)
                            repeat = i["repeater"]
                            if days_passed == repeat:
                                rep = self.repeater(i["repeater"],days_passed,i['name'])  # call repeater here
                                if rep == None:
                                    break # if the repeater function returns None, break the loop, if it malfunctioned it would return 404
                                
                            print(f"{bcolors.HEADER}{i["name"]}{bcolors.ENDC}")
                            print(i["description"])
                            print(i["date"])
                            print(i["repeat"])
                            print(i["repeater"])
                            print(f"{bcolors.FAIL}{passed} ago{bcolors.ENDC}")
                            return
                    print(f"{bcolors.OKGREEN}No entries passed{bcolors.ENDC}")
            except FileNotFoundError:
                print(f"{bcolors.FAIL}Error: {i} not found. Creating a new file...{bcolors.ENDC}")
                with open(f"SnyvieCLA/data/{i}", "w") as f:
                    json.dump({"entries": []}, f)
            except Exception as e:
                print(f"{bcolors.FAIL}Error: {e}{bcolors.ENDC}")
                                

    def repeater(self, repeater: int, passed: int, name: str):
        if passed >= 0:
            try:
                with open(f"SnyvieCLA/data/default.json", "r+") as f:
                    data = json.load(f)
                    for i in data["entries"]:
                        print(i["repeat"])
                        if i["name"] == name and bool(i["repeat"])==True:
                            print("passed the check")
                            original_date = datetime.strptime(i["date"], "%Y-%m-%d").date()
                            i["date"] = (original_date + timedelta(days=repeater)).strftime("%Y-%m-%d")
                    f.seek(0)
                    json.dump(data, f, indent=4)
                    f.truncate()
                    print(f"{bcolors.OKGREEN}Entry updated{bcolors.ENDC}")
                    
            except Exception as e:
                print(f"{bcolors.FAIL}Error: {e}{bcolors.ENDC}")
                return 404

        
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
    def initialise(self) -> None:
        self.start()

    def exit(self):
        exit()

    def start(self):
        date = datetime.today().date()
        tomorrow = date + timedelta(days=1)
        print(f"date: {date}\ntomorrow: {tomorrow}")
        try:
            Agenda().passed()
            self.checkUpdates()
        except Exception as e:
            print(f"{bcolors.FAIL}Error: {e}{bcolors.ENDC}")
    

    
    def checkUpdates(self):
        print(f"{bcolors.BOLD}Checking for updates{bcolors.ENDC}")
        print(f"{bcolors.OKCYAN}Current version: {CURRENT_VERSION}{bcolors.ENDC}")
        response = requests.get("https://api.github.com/repos/Snufie/SnyvieCLA/releases/latest", headers={"Accept": "application/vnd.github.v3+json"})
        latest_release = response.json()['tag_name'], response.json()['published_at'], response.json()['body']
        print(latest_release)
        if latest_release[0] != CURRENT_VERSION:
            print(f"{bcolors.WARNING}New version available: {latest_release[0]}{bcolors.ENDC}")
            print(f"{bcolors.OKBLUE}Published at: {latest_release[1]}{bcolors.ENDC}")
            print(f"{bcolors.OKGREEN}Release notes: {latest_release[2]}{bcolors.ENDC}")
            choice = input("Do you want to update? (y/N) ").lower()
            if choice in ["yes", "y"]:
                print("Updating...")
                Updater.Updater(latest_release[0])
                import sys
                sys.exit(0)
            elif choice in ["no", "n", ""]:
                print("Aborted")

class version:
    def version(self):
        print(f"Current version: {CURRENT_VERSION}")

    def help(self):
        print("Available commands:")
        print("  version: Print the current version of the application")
        # Add descriptions for other commands here
