import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from googletrans import Translator, LANGUAGES
from kivy.core.text import LabelBase

# Register fonts for various languages
LabelBase.register(name="NotoSans", fn_regular="fonts/NotoSans-Regular.ttf")                # Overall
LabelBase.register(name="NotoSansArabic", fn_regular="fonts/NotoSansArabic-Regular.ttf")    # Arabic
LabelBase.register(name="NotoSansTC", fn_regular="fonts/NotoSansTC-VariableFont_wght.ttf")  # Traditional Chinese
LabelBase.register(name="NotoSansKR", fn_regular="fonts/NotoSansKR-VariableFont_wght.ttf")  # Korean

class TranslatorApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Input text field
        self.input_text = TextInput(hint_text='Enter text for Translation', font_name="NotoSans",
                                    size_hint=(1, 0.3), multiline=True)
        self.layout.add_widget(self.input_text)

        # Language selection spinner
        capitalized_languages = [lang.capitalize() for lang in LANGUAGES.values()]
        self.language_spinner = Spinner(
            text='Choose the Language',
            values=capitalized_languages,
            size_hint=(1, 0.1)
        )
        self.layout.add_widget(self.language_spinner)

        # Translate button
        self.translate_button = Button(text='Translate', size_hint=(1, 0.1), background_color=(0, 1, 0, 1))
        self.translate_button.bind(on_press=self.translate_text)
        self.layout.add_widget(self.translate_button)

        # Output label, initially set to use the universal font
        self.output_text = Label(
            text='Translation appears here',
            font_name="NotoSans",  # Default to the universal font
            size_hint=(1, 0.5),
            halign='center',
            valign='middle'
        )
        self.output_text.bind(size=self.output_text.setter('text_size'))
        self.layout.add_widget(self.output_text)

        # Translator instance
        self.translator = Translator()

        return self.layout

    def translate_text(self, instance):
        input_text = self.input_text.text
        selected_language = self.language_spinner.text.lower()

        # Check for empty input and language selection
        if input_text.strip() and selected_language != 'choose the language':
            try:
                # Find the target language code
                target_language = list(LANGUAGES.keys())[list(LANGUAGES.values()).index(selected_language)]

                # Determine which font to use based on the target language
                if target_language == 'ar':  # Arabic
                    self.output_text.font_name = "NotoSansArabic"
                elif target_language == 'zh-tw':  # Traditional Chinese
                    self.output_text.font_name = "NotoSansTC"
                elif target_language == 'ko':  # Korean
                    self.output_text.font_name = "NotoSansKR"
                else:
                    self.output_text.font_name = "NotoSans"  # Default for Latin and other scripts

                # Perform translation
                translated_text = self.translate(input_text, target_language)
                self.output_text.text = translated_text

            except ValueError:
                self.output_text.text = "Error: Selected language is not supported."
        elif not input_text.strip():
            self.output_text.text = "Input text is empty, please enter text for translation."
        else:
            self.output_text.text = "Please select a target language."

    def translate(self, text, target_language='en'):
        try:
            translated = self.translator.translate(text, dest=target_language)
            return translated.text
        except Exception as e:
            return f"Translation error: {e}"

if __name__ == '__main__':
    TranslatorApp().run()
