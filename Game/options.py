import customtkinter
from board import openView as openGame
from PIL import Image

def openView():
    global app, nTextEntry, labelP, botButton, swapped, isBot, switchVar
    customtkinter.set_appearance_mode('dark')
    customtkinter.set_default_color_theme('dark-blue')

    swapped = True
    isBot = True

    app = customtkinter.CTk()
    app.title('Atoll')
    app.geometry('400x320')
    app.minsize(400, 320)
    app.maxsize(400, 320)
    app.resizable(False, False)
    app.grid_columnconfigure(0, weight=1)
    app.grid_rowconfigure(1, weight=1)

    header = customtkinter.CTkFrame(app, fg_color="transparent")
    header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10)
    header.grid_columnconfigure(0, weight=1)
    header.grid_columnconfigure(1, weight=0)

    gameNameLabel = customtkinter.CTkLabel(header, text='Atoll', fg_color='transparent', font=('', 25, 'bold'))
    gameNameLabel.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    theme_icon = customtkinter.CTkImage(
        light_image=Image.open("./assets/light_theme.png"),
        dark_image=Image.open("./assets/dark_theme.png"),
        size=(40, 40)
    )

    button = customtkinter.CTkButton(
        header,
        text="",
        width=40,
        height=40,
        hover=False,
        fg_color="transparent",
        image=theme_icon,
        command=changeTheme
    )
    button.grid(row=0, column=1, padx=10, pady=10, sticky="e")

    frame = customtkinter.CTkFrame(app)
    frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky='nwes')
    frame.grid_columnconfigure(0, weight=1)

    nInputFrame = customtkinter.CTkFrame(frame, fg_color='transparent')
    nInputFrame.grid(row = 0, column = 0, padx=10, pady=(10, 20), sticky='ew', columnspan=2)
    nInputFrame.grid_columnconfigure(0, weight=1)

    nInputLabel = customtkinter.CTkLabel(nInputFrame, text='Duzina stranice:')
    nInputLabel.grid(row = 0, column = 0, sticky='w')

    nTextEntry = customtkinter.CTkEntry(nInputFrame, height=10, placeholder_text='5, 7, 9...')
    nTextEntry.grid(row = 1, column = 0, sticky='we')

    playerFrame = customtkinter.CTkFrame(frame, fg_color='transparent')
    playerFrame.grid(row = 1, column = 0, padx = 10, pady = 10, sticky = 'ew', columnspan=2)
    playerFrame.grid_columnconfigure((0, 1, 2), weight=1)

    labelX = customtkinter.CTkLabel(playerFrame, text='X')
    labelX.grid(row = 0, column = 0)

    labelO = customtkinter.CTkLabel(playerFrame, text='O')
    labelO.grid(row = 0, column = 2)

    labelP = customtkinter.CTkLabel(playerFrame, text='Player 1', width=40)
    labelP.grid(row = 1, column = 0, padx = 10)

    swapImage = customtkinter.CTkImage(Image.open('./assets/swap.png'), size=(20, 20))

    swapButton = customtkinter.CTkButton(playerFrame, text='', image=swapImage, width=40, command=swapPlayerClick)
    swapButton.grid(row=1, column=1, padx = 10)

    botButton = customtkinter.CTkButton(playerFrame, text='Bot', width=40, command=addPlayerClick)
    botButton.grid(row=1, column=2, padx = 10)

    buttonsFrame = customtkinter.CTkFrame(frame, fg_color='transparent')
    buttonsFrame.grid(row = 2, column=0, sticky='ew', columnspan=2)
    buttonsFrame.grid_rowconfigure(0, weight=1)
    buttonsFrame.grid_columnconfigure(0, weight=1)
    buttonsFrame.grid_columnconfigure(1, weight=1)

    switchVar = customtkinter.StringVar(value = 'off')
    switchEl = customtkinter.CTkSwitch(buttonsFrame, text='Hide confirm/undo buttons', variable=switchVar, onvalue='on', offvalue='off')
    switchEl.grid(row = 0, column = 0, padx=10, columnspan=2, sticky='w')

    startButton = customtkinter.CTkButton(buttonsFrame, text='Start', command=startButtonClick)
    startButton.grid(row=1, column=0, padx=10, pady=10, sticky='ew')

    exitButton = customtkinter.CTkButton(buttonsFrame, text='Exit', command=exitButtonClick)
    exitButton.grid(row=1, column=1, padx=10, pady=10, sticky='ew')
    app.mainloop()

def startButtonClick():
    notNum = False
    n = int(nTextEntry.get())
    hideButtons = switchVar.get() == 'on'

    try:
        n = int(n)
    except:
        notNum = True

    
    if(notNum or n < 3 or n > 9 or n % 2 == 0):
        infoBox = customtkinter.CTkToplevel()
        infoBox.geometry('300x100')
        infoBox.grid_rowconfigure(0, weight=1)
        infoBox.grid_columnconfigure(0, weight=1)
        infoBox.title('Notification')

        label = customtkinter.CTkLabel(infoBox, text='N mora biti neparan broj izmedju 3 i 9')

        label.grid(row = 0, column = 0, sticky='nsew')
        infoBox.grab_set()
        return

    app.withdraw()
    openGame(n, isBot, swapped, app, customtkinter.get_appearance_mode().lower(), hideButtons)

def exitButtonClick():
    app.quit()

def swapPlayerClick():
    global swapped
    swapped = not swapped
    labelP.grid(row = 1, column = 0 if swapped else 2)
    botButton.grid(row = 1, column = 2 if swapped else 0)

def addPlayerClick():
    global isBot
    isBot = not isBot
    botButton.configure(text = 'Bot' if isBot else 'Player 2')

def changeTheme():
    customtkinter.set_appearance_mode("dark" if customtkinter.get_appearance_mode().lower() == "light" else "light")