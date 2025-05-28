import nltk
import json
import random
import numpy as np
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD
import pickle
import tkinter as tk
from tkinter import scrolledtext, Tk, Frame, Button, Entry, StringVar

# Initialize NLP components
lemmatizer = WordNetLemmatizer()
nltk.download('punkt')
nltk.download('wordnet')

class VirtualTherapist:
    def __init__(self):
        self.words = []
        self.classes = []
        self.documents = []
        self.ignore_chars = ['?', '!', '.', ',']
        self.model = None
        self.intents = self.load_intents()
        self.prepare_data()
        
    def load_intents(self):
        with open('data/intents.json') as file:
            return json.load(file)

    def prepare_data(self):
        for intent in self.intents['intents']:
            for pattern in intent['patterns']:
                tokens = nltk.word_tokenize(pattern)
                self.words.extend(tokens)
                self.documents.append((tokens, intent['tag']))
                if intent['tag'] not in self.classes:
                    self.classes.append(intent['tag'])
                    
        self.words = [lemmatizer.lemmatize(w.lower()) 
                     for w in self.words if w not in self.ignore_chars]
        self.words = sorted(list(set(self.words)))
        self.classes = sorted(list(set(self.classes)))

    def create_training_data(self):
        training = []
        output_empty = [0] * len(self.classes)
        
        for doc in self.documents:
            bag = []
            pattern_words = [lemmatizer.lemmatize(word.lower()) 
                            for word in doc[0]]
            bag = [1 if word in pattern_words else 0 
                  for word in self.words]
            
            output_row = list(output_empty)
            output_row[self.classes.index(doc[1])] = 1
            training.append([bag, output_row])
            
        random.shuffle(training)
        return np.array(training, dtype=object)

    def build_model(self):
        self.model = Sequential()
        self.model.add(Dense(128, input_shape=(len(self.words),), activation='relu'))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(64, activation='relu'))
        self.model.add(Dropout(0.3))
        self.model.add(Dense(len(self.classes), activation='softmax'))
        
        sgd = SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
        self.model.compile(loss='categorical_crossentropy',
                          optimizer=sgd, metrics=['accuracy'])
        
    def train_model(self, epochs=200, batch_size=5):
        training_data = self.create_training_data()
        train_x = list(training_data[:,0])
        train_y = list(training_data[:,1])
        
        hist = self.model.fit(np.array(train_x), np.array(train_y),
                             epochs=epochs, batch_size=batch_size, verbose=1)
        self.model.save('models/therapist_model.h5', hist)
        pickle.dump(self.words, open('models/words.pkl', 'wb'))
        pickle.dump(self.classes, open('models/classes.pkl', 'wb'))

    def load_model(self):
        self.model = load_model('models/therapist_model.h5')
        self.words = pickle.load(open('models/words.pkl', 'rb'))
        self.classes = pickle.load(open('models/classes.pkl', 'rb'))

    def predict_intent(self, sentence):
        tokens = nltk.word_tokenize(sentence)
        tokens = [lemmatizer.lemmatize(word.lower()) for word in tokens]
        bag = [1 if word in tokens else 0 for word in self.words]
        
        res = self.model.predict(np.array([bag]))[0]
        ERROR_THRESHOLD = 0.25
        results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
        results.sort(key=lambda x: x[1], reverse=True)
        
        return_list = []
        for r in results:
            return_list.append({'intent': self.classes[r[0]], 'probability': str(r[1])})
        return return_list

    def get_response(self, intents_list):
        tag = intents_list[0]['intent']
        for intent in self.intents['intents']:
            if intent['tag'] == tag:
                return random.choice(intent['responses'])
        return "Could you please rephrase that?"

class TherapistGUI:
    def __init__(self, master):
        self.master = master
        self.therapist = VirtualTherapist()
        self.therapist.load_model()
        self.setup_ui()
        
    def setup_ui(self):
        self.master.title("AI Virtual Therapist")
        self.master.geometry("600x500")
        self.master.resizable(False, False)
        
        self.chat_history = scrolledtext.ScrolledText(self.master, wrap=tk.WORD)
        self.chat_history.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.chat_history.config(state=tk.DISABLED)
        
        input_frame = Frame(self.master)
        input_frame.pack(padx=10, pady=10, fill=tk.X)
        
        self.user_input = Entry(input_frame, font=('Arial', 12))
        self.user_input.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.user_input.bind("<Return>", self.send_message)
        
        send_btn = Button(input_frame, text="Send", command=self.send_message)
        send_btn.pack(side=tk.RIGHT, padx=5)
        
    def send_message(self, event=None):
        user_msg = self.user_input.get()
        self.user_input.delete(0, tk.END)
        
        if user_msg.lower() in ['quit', 'exit', 'bye']:
            self.master.destroy()
            return
            
        self.update_chat("You: " + user_msg, "blue")
        response = self.therapist.get_response(self.therapist.predict_intent(user_msg))
        self.update_chat("Therapist: " + response, "green")
        
    def update_chat(self, message, color):
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.insert(tk.END, message + '\n\n', color)
        self.chat_history.config(state=tk.DISABLED)
        self.chat_history.see(tk.END)

if __name__ == "__main__":
    root = Tk()
    app = TherapistGUI(root)
    root.mainloop()
