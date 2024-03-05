from datetime import datetime, timedelta
import AdvLog as AdvLog
import snyvie as Snyvie
import inspect

date = datetime.today().date()
tomorrow = date + timedelta(days=1)
print(f"date: {date}\ntomorrow: {tomorrow}")

def main():
    instance = Snyvie.AppInit()
    
if __name__ == "__main__":
    main()
    while True:
        action = input("What do you want to do? ").lower()
        funcs = Snyvie.check_functions()
        # print(funcs)
        for cmd, cls in funcs:
            if action == cmd:
                # print(f"{action} - {cls}")
                class_obj = getattr(Snyvie, cls)  # Get the class from the snyvie module
                instance = class_obj()  # Instantiate the class
                sig = inspect.signature(getattr(instance, cmd)) # Get the arguments for the function 'cmd' and store them in a list
                args = []
                for param in sig.parameters.values():
                    arg_type = param.annotation
                    if arg_type is not inspect._empty:
                        args.append((param.name.capitalize(), arg_type))
                params = []
                for arg in args:
                    try:
                        paramI = ''
                        paramI = arg[1](input(f"{arg[0]}: "))
                    except:
                        if paramI == '' or None:
                            paramI = param.default
                    params.append(paramI)
                getattr(instance, cmd)(*params)  # Call the method

        