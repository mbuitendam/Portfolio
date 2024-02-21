from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def genPassword():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8,10))]
    password_symbols = [choice(symbols) for _ in range(randint(2,4))]
    password_numbers = [choice(numbers) for _ in range(randint(2,4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    passwordInput.insert(END, password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def savePassword():
    websiteEntry = website.get()
    usernameEntry = username.get()
    passwordEntry = passwordInput.get()

    #json filing
    new_data = {
        websiteEntry: {
            "email": usernameEntry,
            "password": passwordEntry,
        }
    }

    if len(websiteEntry) != 0 and len(passwordEntry) != 0 and len(usernameEntry) != 0:
        try:    
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)
            with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
        finally:
            website.delete(0,END)
            passwordInput.delete(0,END)
    else:
        messagebox.showinfo(title="Oops", message="You need to fill in the website and Password")

def find_password():
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Something went wrong", message="No data file found")
    except IndexError:
        messagebox.showinfo(title="No password?", message="No details for the website exists")

    else:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
            websiteEntry = website.get()
            info = data.get(websiteEntry)

            messagebox.showinfo(title=f"{websiteEntry}", message=f"{info}")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

# image
canvas = Canvas(width=200, height=200)
myPass_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=myPass_img)
canvas.grid(column=1, row=0)


# form
website_label = Label(text="Website:")
website = Entry(width=20)
search = Button(text="Search", width=15, command=find_password)
website.focus()

website_label.grid(column=0, row=1)
website.grid(column=1, row=1)
search.grid(column=2, row=1)


username_label = Label(text="Email/Username:")
username = Entry(width=40)
username.insert(END, "mathew.buitendam11@gmail.com")

username_label.grid(column=0, row=2)
username.grid(column=1, row=2, columnspan=2)


password_label = Label(text="Password:")
passwordInput = Entry(width=21)
generatePass = Button(text="Generate Password", command=genPassword)

password_label.grid(column=0, row=3)
passwordInput.grid(column=1, row=3)
generatePass.grid(column=2, row=3)


addPass = Button(text="Add", width=36, command=savePassword)
addPass.grid(column=1, row=4, columnspan=2)

window.mainloop()