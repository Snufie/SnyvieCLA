from datetime import datetime, timedelta
import components.snyvie as Snyvie
import inspect



def main():
    Snyvie.AppInit().initialise()
    
    
if __name__ == "__main__":
    main()
    while True:
        action = input("What do you want to do? ").lower()
        funcs = Snyvie.check_functions()
        # print(f"{funcs =}")
        for cmd, cls in funcs:
            if action == cmd:
                class_obj = getattr(Snyvie, cls)  # Get the class from the snyvie module
                instance = class_obj()  # Instantiate the class
                sig = inspect.signature(getattr(instance, cmd)) # Get the arguments for the function 'cmd' and store them in a list
                args = []
                for param in sig.parameters.values():
                    arg_type = param.annotation
                    if arg_type is not inspect._empty:
                        args.append((param.name.capitalize(), arg_type))
                params = []

                # Get the actual parameters from the user
                for arg in args:
                    param = input(f"Enter {arg[0]}: ")
                    if arg[1] == int:
                        param = int(param)
                    elif arg[1] == float:
                        param = float(param)
                    # Add more elif statements here if there are other types of parameters
                    params.append(param)

                getattr(instance, cmd)(*params)  # Call the method
