import sys
class cli :
    def print_help(args_zero):
        print("Help UC")
        print( args_zero + " --cli --in <path> --pass <password> --out <path>")
        print("Use --out <path> to specify the output file.")
        print("Use --encrypt to use encrypt mode.")
        print("Use --decrypt to use decrypt mode.")
    def pars_args():
        if sys.argv.__len__() == 1:
             return
        if sys.argv.__len__() < 4 or sys.argv.__len__() > 8:
            cli.print_help(sys.argv[0])
            return {"err":True}
        if sys.argv[1] != "--cli":
            cli.print_help(sys.argv[0])
            return {"err":True}
        file_in_name = ""
        file_out_name = ""
        password_in = ""
        is_encrypt_or_encrypt = True
    
        for i in range(1, sys.argv.__len__()-1):
            if sys.argv[i] == "--in":
                file_in_name = str(sys.argv[i+1])
            elif sys.argv[i] == "--out":
                file_out_name = str(sys.argv[i+1])
            elif sys.argv[i] == "--pass":
                password_in = str(sys.argv[i+1])
            elif sys.argv[i] == "--encrypt":
                is_encrypt_or_encrypt = True
            elif sys.argv[i] == "--decrypt":
                is_encrypt_or_encrypt = False
            
        if file_out_name == "":
            file_out_name = file_in_name + ".uc"
        print("file_in_name: " + file_in_name)
        print("file_out_name: " + file_out_name)
        print("password_in: " + password_in)
        return {"file_in_name": file_in_name,"file_out_name": file_out_name, "password_in": password_in,
                "is_encrypt_or_encrypt":is_encrypt_or_encrypt, "err":False}


