import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button

Builder.load_string("""

<MenuScreen>:
    user: User
    password: Password

    FloatLayout:
        
        Label:
            text: 'Login Page'
            size_hint: 0.3, 0.1
            pos_hint: {"x":0.35, "top":1} 
        
        Label:
            text: 'Username'
            size_hint: 0.2, 0.1
            pos_hint: {"left":0, "top":0.8}         
        
        TextInput:
            id:User
            multiline: False
            size_hint: 0.8, 0.3
            pos_hint: {"x":0.20, "top":0.9} 
            
        Label:
            text: 'Password'
            size_hint: 0.2, 0.1
            pos_hint: {"left":0, "top":0.5} 

        TextInput:
            id:Password
            multiline: False
            size_hint: 0.8, 0.3
            pos_hint: {"x":0.20, "top":0.6} 

        
        Button:
            text: 'submit'
            on_press: root.check()
            size_hint: 0.5, 0.3
            pos_hint: {"x":0.5, "bottom":1}
            
        Button:
            text: 'Create'
            on_press: root.create()
            size_hint: 0.5, 0.3
            pos_hint: {"x":0, "bottom":1} 
            
<NotesScreen>
    info: info

    FloatLayout:
      
        Label:
            text: 'Notes'
            size_hint: 0.3, 0.2
            pos_hint: {"x":0.35, "top":1} 
        
        TextInput: 
            id:info
            multiline: True
            text:""     
            size_hint: 1, 0.6
            pos_hint: {"x":0, "top":0.8} 
            
        
        Button:
            text: 'menu'
            size_hint: 1, 0.3
            pos_hint: {"x":0, "bottom":1} 
            on_press: root.menu()
    
<CreateScreen>:
    
    user: CreateUser
    password: CreatePassword

    FloatLayout:
        
        Label:
            text: 'Create Page'
            size_hint: 0.3, 0.1
            pos_hint: {"x":0.35, "top":1} 
        
        Label:
            text: 'Username'
            size_hint: 0.2, 0.1
            pos_hint: {"left":0, "top":0.8}         
        
        TextInput:
            id:CreateUser
            multiline: False
            size_hint: 0.8, 0.3
            pos_hint: {"x":0.20, "top":0.9} 
            
        Label:
            text: 'Password'
            size_hint: 0.2, 0.1
            pos_hint: {"left":0, "top":0.5} 

        TextInput:
            id:CreatePassword
            multiline: False
            size_hint: 0.8, 0.3
            pos_hint: {"x":0.20, "top":0.6}
                 
        Button:
            text: 'Menu'
            on_press: root.menu()
            size_hint: 0.5, 0.3
            pos_hint: {"x":0, "bottom":1}
            
        Button:
            text: 'Create'
            on_press: root.create()
            size_hint: 0.5, 0.3
            pos_hint: {"x":0.5, "bottom":1} 
""")

# Declare the screens
class MenuScreen(Screen):

    user = ObjectProperty(None)
    password = ObjectProperty(None)



    def check(self): #checks if the file is empty

        with open ('accounts.txt','r') as file:
            contents = file.read()
            if contents == '':
                create_acc()

            else:
                MenuScreen.verify(self)

    def verify(self): #verifies input

        user_in = self.user.text
        pass_in = self.password.text
        accounts = {}
        Names = []

        with open("accounts.txt") as file:
            for lines in file:
                (not_notes,notes) = lines.split(';')
                (UserName,PassWord) = not_notes.split(":")
                accounts[UserName] = PassWord

            if user_in in accounts.keys(): #checks valid user

                correct_pass = accounts[user_in]
                correct_pass = correct_pass.replace(';', '')

                for names in accounts.keys():
                    Names.append(names)

                if pass_in == correct_pass: #checks password to the valid user
                    self.x = Names.index(user_in)
                    print(self.x)

                    with open('line.txt', 'w') as file:
                        str(self.x).replace(".0","")
                        print(self.x)
                        file.write(str(self.x))
                        MenuScreen.notes(self)

                else:
                    invalid()

            else:
                invalid()


    def notes(self): #moves to notes screen
        sm.transition.direction = 'left'
        sm.current = 'notes'


    def create(self): #moves to create screen
        sm.transition.direction = 'right'
        sm.current = 'create'

    def on_leave(self): #empties textinput on leave
        self.user.text = ''
        self.password.text = ''

class NotesScreen(Screen):
    info = ObjectProperty(None)


    def on_enter(self, **kwargs): #loads notes when enter the notes screen

        with open('line.txt', 'r') as file: #finds out the line number
            x = file.read()
            x = int(float(x))
            with open('accounts.txt', 'r') as file:
                lines = file.readlines()
                (account, notes) = lines[x].split(";")
                notes = notes.replace("\\n","\n")
                self.info.text = notes

    def menu(self):
        with open('line.txt', 'r') as file: #finds out the line number
            x = file.read()
            x = int(float(x))

        with open('accounts.txt', 'r') as file:
            lines = file.readlines()
            (account, notes) = lines[x].split(";")

        with open('accounts.txt', 'w+') as file:
            lines[x] = "\n"
            self.info.text = self.info.text.replace("\n","\\n")
            lines[x] = account + ';' + self.info.text + "\n"
            file.writelines(lines)

        print(self.info.text)
        sm.transition.direction = 'right'
        sm.current = 'menu'



class CreateScreen(Screen):

    user = ObjectProperty(None)
    password = ObjectProperty(None)

    def menu(self):
        sm.transition.direction = 'left'
        sm.current = 'menu'

    def create(self):
        taken = []
        User = self.user.text
        Password = self.password.text
        if User != '' and Password != '':
            with open('accounts.txt', 'r') as file:
                for line in file:
                    (UserName, other) = line.split(':')
                    taken.append(UserName)

            if User not in taken:
                with open('accounts.txt', 'a+') as file:
                    file.write( User + ':' + Password + ';' + '\n')
            else:
                duplicate_acc()
        else:
            empty_acc()


def duplicate_acc():
    text = 'UserName taken'
    popupWindow = Popup(title="Popup Window", content=Label(text=text), size_hint=(.5, .5),pos_hint={'right': .75, 'top': .8})
    popupWindow.open() # show the popup

def empty_acc():
    text = 'Please don\'t leave it blank'
    popupWindow = Popup(title="Popup Window", content=Label(text=text), size_hint=(.5, .5),pos_hint={'right': .75, 'top': .8})
    popupWindow.open() # show the popup

def invalid():
    text = 'Invalid login'
    popupWindow = Popup(title="Popup Window", content=Label(text=text), size_hint=(.5, .5),pos_hint={'right': .75, 'top': .8})
    popupWindow.open() # show the popup

def create_acc():
    Grid = GridLayout(cols = 1)
    close = Button(text='Create account')
    Grid.add_widget(Label(text='No accounts, Please create one'))
    Grid.add_widget(close)
    popupWindow = Popup(title="Popup Window", content=Grid, size_hint=(.5, .5),pos_hint={'right': .75, 'top': .8},auto_dismiss=False)
    popupWindow.open()  # show the popup
    close.bind(on_press = popupWindow.dismiss)
    close.bind(on_press = create)

def create(btn):
    sm.transition.direction = 'right'
    sm.current = 'create'

# Create the screen manager
sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(NotesScreen(name='notes'))
sm.add_widget(CreateScreen(name='create'))

class MyApp(App):

    def build(self):

        return sm


if __name__ == '__main__':
    MyApp().run()