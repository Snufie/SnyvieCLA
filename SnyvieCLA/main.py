from datetime import datetime, timedelta
import AdvLog as AdvLog
import snyvie as Snyvie
import inspect

date = datetime.today().date()
tomorrow = date + timedelta(days=1)
print(f"date: {date}\ntomorrow: {tomorrow}")

def main():
    instance = Snyvie.Agenda()
    instance.passed()
    
if __name__ == "__main__":
    main()
    while True:
        action = input("What do you want to do? ").lower()
        funcs = Snyvie.check_functions()
        print(funcs)
        for cmd, cls in funcs:
            if action == cmd:
                print(f"{action} - {cls}")
                class_obj = getattr(Snyvie, cls)  # Get the class from the snyvie module
                instance = class_obj()  # Instantiate the class
                sig = inspect.signature(getattr(instance, cmd)) # Get the arguments for the function 'cmd' and store them in a list
                args = []
                for param in sig.parameters.values():
                    arg_type = param.annotation
                    if arg_type is not inspect._empty:
                        arg = arg_type
                        args.append(arg)
                params = []
                for arg in args:
                    print(arg)
                    param = arg(input(f"{arg}: "))
                    params.append(param)
                getattr(instance, cmd)(*params)  # Call the method


class test():
    def __init__(self):
        pass 
    def cook(self):
        print("cooking")
        
        # action = input("What do you want to do? ").lower()
        # if action == "exit":
        #     break
        # elif action == "view":
        #     span = int(input("Span: "))
        #     snyvie.Agenda().view(span)
        # elif action == "nearing":
        #     span = int(input("Span: "))
        #     snyvie.Agenda().nearing(span)
        # elif action == "passed":
        #     snyvie.Agenda().passed()
        # elif action == "help":
        #     print("Commands: view, nearing, passed, create, remove, removeAll, exit")
        # elif action == "create":
        #     name = input("Name: ")
        #     description = input("Description: ")
        #     date = input("Date (yyyy-mm-dd): ")
        #     repeat = input("Repeat (True/False): ")
        #     saveto = input("Save to (default): ")
        #     if saveto == "":
        #         saveto = "default"
        #     snyvie.Agenda().create(name, description, date, repeat, saveto)
        # elif action == "remove":
        #     name = input("Name: ")
        #     savedAt = input("Saved at (default): ")
        #     if savedAt == "":
        #         savedAt = "default"
        #     snyvie.Agenda().remove(name, savedAt)
        # elif action == "removeall":
        #     savedAt = input("Saved at (default): ")
        #     if savedAt == "":
        #         savedAt = "default"
        #     snyvie.Agenda().removeAll(savedAt)
        # else:
        #     print("Invalid action")
        