import kivy
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.app import App
import Ai_Book_Analytics
import gpt_responce
global_choice = 0

global_temp_ai_book_assistant = ''
global_temp_ai_psychologist = ''
global_temp_ai_personal_assistant = ''
global_book_name =''
Builder.load_file('Build_File/home_screen.kv')
Builder.load_file('Build_File/chat_screen.kv')
Builder.load_file('Build_File/setup_screen.kv')
Builder.load_file('Build_File/book_name.kv')

class BookName(Screen):
    def book_select(self):
        global global_book_name, global_choice
        global_book_name = self.ids.bookname.text
        global_choice = 3
        file_path = 'PDF/' + global_book_name
        print(global_book_name)
        if global_book_name == 'Book Name?(with extension .pdf)':
            self.ids.bookname.text = 'Enter a name first!!!!!??'
        else:
            try:
                with open(file_path, 'r') as file:
                    self.manager.current = 'chat'
            except FileNotFoundError:
                self.ids.bookname.text = f"File '{file_path}' not found. Try Again"
            except IOError:
                print(f"Error reading file '{file_path}'.")
                self.ids.bookname.text = f"Error reading file '{file_path}'. Try Again"

    def backToHome(self):
        global  global_choice
        global_choice = 0
        self.manager.current = 'home'


class SetupScreen(Screen):

    def save_to_txt_file(self,file_path, content):
        try:
            with open(file_path, 'w') as file:
                file.write(content)
            print(f"Content saved to '{file_path}' successfully.")
        except IOError:
            print(f"Error saving content to '{file_path}'.")


    def cancel_openai(self):
        self.ids.openai_api.text = "OpenAi Api Key"

    def cancel_pinecone_api(self):
        self.ids.pinecone_api.text = "Pinecone API Key"

    def cancel_pinecone_env(self):
        self.ids.pinecone_env.text = "Pinecone Env key"

    def cancel_index_name(self):
        self.ids.index_name.text = "Index Name"

    def save_openai(self):
        self.save_to_txt_file('setup_api_and_env/temp.txt', self.ids.openai_api.text)

    def save_pinecone_api(self):
        self.save_to_txt_file('setup_api_and_env/temp.txt', self.ids.pinecone_api.text)

    def save_pinecone_env(self):
        self.save_to_txt_file('setup_api_and_env/temp.txt', self.ids.pinecone_env.text)

    def save_index_name(self):
        self.save_to_txt_file('setup_api_and_env/temp.txt', self.ids.index_name.text)

    def cancel_all(self):
        self.ids.openai_api.text = "OpenAi Api Key"
        self.ids.pinecone_api.text = "Pinecone API Key"
        self.ids.pinecone_env.text = "Pinecone Env key"
        self.ids.index_name.text = "Index Name"

    def save_all(self):
        self.save_to_txt_file('setup_api_and_env/temp.txt', self.ids.openai_api.text)
        self.save_to_txt_file('setup_api_and_env/temp.txt', self.ids.pinecone_api.text)
        self.save_to_txt_file('setup_api_and_env/temp.txt', self.ids.pinecone_env.text)
        self.save_to_txt_file('setup_api_and_env/temp.txt', self.ids.index_name.text)

    def backToHome(self):
        global global_choice
        global_choice = 0
        self.manager.current = 'home'


class HomeScreen(Screen):
    def aiSetup(self):
        global global_choice
        global_choice = -1
        self.manager.current = 'setup'
        #print('Setup Clicked')

    def aiPsychologist(self):
        global global_choice, global_temp_ai_psychologist
        global_choice = 1
        self.manager.current = 'chat'

    def aiPersonalAssistant(self):
        global global_choice, global_temp_ai_personal_assistant
        global_choice = 2
        self.manager.current = 'chat'

    def aiBookAnalyist(self):
        global global_choice, global_temp_ai_book_assistant
        global_choice = 3
        self.manager.current = 'bookname'


class ChatScreen(Screen):

    def backToHome(self):
        global global_choice, global_temp_ai_psychologist, global_temp_ai_personal_assistant, global_temp_ai_book_assistant
        prompt = self.prompt.text
        if global_choice == 1:
            global_temp_ai_psychologist = prompt
            self.manager.current = 'home'
        elif global_choice == 2:
            global_temp_ai_personal_assistant = prompt
            self.manager.current = 'home'
        elif global_choice == 3:
            global_temp_ai_book_assistant = prompt
            self.manager.current = 'bookname'
        global_choice = 0


    def promtSend(self):
        global global_choice
        prompt = self.prompt.text
        print("you choice : " + str(global_choice) + "\n your promt is : " + prompt)
        humanText = self.humanText
        if prompt == '':
            humanText.text = '    '
        else:
            humanText.text = prompt
        humanText.texture_update()
        humanText.height = humanText.texture_size[1]

        if global_choice == 1:
            response = self.AiPsychologist(prompt)
        elif global_choice == 2:
            response = self.AiPersonalAssistant(prompt)
        elif global_choice == 3:
            response =  self.AiBookAnalyist(prompt)

        print('\n '+ response)
        aiText = self.aiText
        aiText.text = response
        aiText.texture_update()
        aiText.height = aiText.texture_size[1]
        self.prompt.text =''

    def AiPsychologist(self, promt):
        response = gpt_responce.get_gtp_responce(promt)[1]
        return response

    def AiPersonalAssistant(self, promt):
        response = 'Here is your ai Personal Assistant responce '
        return response

    def break_string(self, string, line_length):
        broken_string = ""
        for i in range(0, len(string), line_length):
            broken_string += string[i:i + line_length] + "\n"
        return broken_string

    def AiBookAnalyist(self, prompt):

        global  global_book_name
        #PDF/book1_chapter1_1.pdf
        file_path = 'PDF/'+ global_book_name
        response =  Ai_Book_Analytics.load_file(file_path,prompt)
        return self.break_string(response, 50)






class MyApp(App):
    def build(self):
        screen_manager = ScreenManager()
        screen_manager.add_widget(HomeScreen(name='home'))
        screen_manager.add_widget(ChatScreen(name='chat'))
        screen_manager.add_widget(SetupScreen(name='setup'))
        screen_manager.add_widget(BookName(name='bookname'))
        return screen_manager


if __name__ == '__main__':
    MyApp().run()
