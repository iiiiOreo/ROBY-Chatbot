import random
import json
import pickle
import nltk
import math
import re
import time
import customtkinter
import numpy as np
import tkinter as tk
from datetime import date
from PIL import ImageTk, Image
from tkinter import messagebox
from keras.optimizers import SGD
from nltk.stem import PorterStemmer
from keras.models import load_model
from keras.models import Sequential
from keras.layers import Dense, Dropout

stemmer = PorterStemmer()
intents = json.loads(open("S:/Projects/University/ROBY Chatbot project (S4)/Code/intense.json").read())

words = []
classes = []
documents = []
ignore_letters = ["?", "!", ".", ","]

for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        documents.append((word_list, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words = [stemmer.stem(word.lower()) for word in words if word not in ignore_letters]
words = sorted(set(words))

pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

training = []
output_empty = [0] * len(classes)

for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [stemmer.stem(word.lower()) for word in word_patterns]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)

    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append([bag, output_row])

random.shuffle(training)
training = np.array(training)

train_x = list(training[:, 0])
train_y = list(training[:, 1])

model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
hist = model.fit(np.array(train_x), np.array(train_y), epochs=1000, batch_size=8, verbose=2)
model.save("chatbotmodel.h5")

stemmer = PorterStemmer()
intents = json.loads(open("S:/Projects/University/ROBY Chatbot project (S4)/Code/intense.json").read())
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbotmodel.h5')

def clean_up_sentences(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [stemmer.stem(word) for word in sentence_words]
    return sentence_words

def bagw(sentence):
    sentence_words = clean_up_sentences(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bagw(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

def get_response(intents_list, intents_json):
    if intents_list:
        tag = intents_list[0]['intent']
        list_of_intents = intents_json['intents']
        result = ""
        for i in list_of_intents:
            if i['tag'] == tag:
                result = random.choice(i['responses'])
                break
        return result
    else:
        return "I'm sorry, I don't understand."
    
def key_return(event):
    message = entry.get()
    send_message()
    
def send_message():
    message = entry.get()
    entry.delete(0, tk.END)
    if message.strip() != "":
        if re.search("solve",message.lower()):
            text.insert(tk.END, "USER: " + message + "\n\n")
            text.insert(tk.END, "ROBY: Sure! Please enter the mathematical expression you want me to calculate and press calculate.\n")
            text.insert(tk.END, "--------------------------------------\n")
            window.geometry("621x620")
            button_calculate = customtkinter.CTkButton(master=window, corner_radius=10, bg="#3A1078",text="Calculate", width=110, command=calculate_expression)
            button_calculate.pack(pady=10, padx=5, side=tk.LEFT)
            text.see(tk.END)
        elif re.search("time",message.lower()):
            window.geometry("501x620")
            current_time = time.strftime("%H:%M:%S")
            text.insert(tk.END, "USER: " + message + "\n\n")
            text.insert(tk.END, "ROBY: " + "Current Time is " + current_time + "\n")
            text.insert(tk.END, "--------------------------------------\n")
            text.see(tk.END)
        elif re.search("date",message.lower()):
            window.geometry("501x620")
            today = date.today()
            datee = today.strftime("%d/%m/%Y")
            text.insert(tk.END, "USER: " + message + "\n\n")
            text.insert(tk.END, "ROBY: " + "Today's date is " + datee + "\n")
            text.insert(tk.END, "--------------------------------------\n")
            text.see(tk.END)
        else:
            window.geometry("501x620")
            ints = predict_class(message)
            res = get_response(ints, intents)
            text.insert(tk.END, "USER: " + message + "\n\n")
            text.insert(tk.END, "ROBY: " + res + "\n")
            text.insert(tk.END, "--------------------------------------\n")
            text.see(tk.END)

def close_chatbot():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        window.destroy()

def temp_text(e):
    e = e
    entry.delete(0, "end")

def calculate_expression():
    expression = entry.get()
    entry.delete(0, tk.END)
    try:
        if ("sin" in expression):
            x = 0
            result = 0
            for i,item in enumerate(expression):
                if expression[i].isdigit():
                    if not expression[i+1].isdigit():
                        x = int(i)
                    elif expression[i+1].isdigit():
                        x = int(expression[i]+expression[i+1])
                        break
                    elif expression[i+2].isdigit():
                        x = int(expression[i]+expression[i+1]+expression[i+2])
                        break
            g=math.radians(x)
            result = math.sin(g)
        elif ("sqrt" in expression):
            x = 0
            result = 0
            for i,item in enumerate(expression):
                if expression[i].isdigit():
                    if not expression[i+1].isdigit():
                        x = int(i)
                    elif expression[i+1].isdigit():
                        x = int(expression[i]+expression[i+1])
                        break
                    elif expression[i+2].isdigit():
                        x = int(expression[i]+expression[i+1]+expression[i+2])
                        break
            result = math.sqrt(x)
        elif ("cos" in expression):
            x = 0
            result = 0
            for i,item in enumerate(expression):
                if expression[i].isdigit():
                    if not expression[i+1].isdigit():
                        x = int(i)
                    elif expression[i+1].isdigit():
                        x = int(expression[i]+expression[i+1])
                        break
                    elif expression[i+2].isdigit():
                        x = int(expression[i]+expression[i+1]+expression[i+2])
                        break
            g=math.radians(x)
            result = math.cos(g)
        elif ("tan" in expression):
            x = 0
            result = 0
            for i,item in enumerate(expression):
                if expression[i].isdigit():
                    if not expression[i+1].isdigit():
                        x = int(i)
                    elif expression[i+1].isdigit():
                        x = int(expression[i]+expression[i+1])
                        break
                    elif expression[i+2].isdigit():
                        x = int(expression[i]+expression[i+1]+expression[i+2])
                        break
            g=math.radians(x)
            result = math.tan(g)
        elif ("exp" in expression):
            x = 0
            result = 0
            for i,item in enumerate(expression):
                if expression[i].isdigit():
                    if not expression[i+1].isdigit():
                        x = int(i)
                    elif expression[i+1].isdigit():
                        x = int(expression[i]+expression[i+1])
                        break
                    elif expression[i+2].isdigit():
                        x = int(expression[i]+expression[i+1]+expression[i+2])
                        break
            result = math.exp(x)
        elif ("log" in expression):
            x = 0
            result = 0
            for i,item in enumerate(expression):
                if expression[i].isdigit():
                    if not expression[i+1].isdigit():
                        x = int(i)
                    elif expression[i+1].isdigit():
                        x = int(expression[i]+expression[i+1])
                        break
                    elif expression[i+2].isdigit():
                        x = int(expression[i]+expression[i+1]+expression[i+2])
                        break
            result = math.log(x)
        else:    
            result = eval(expression)
        text.insert(tk.END, "USER: " + expression + "\n\n")
        text.insert(tk.END, "ROBY: The result is " + str(result) + "\n")
        text.insert(tk.END, "--------------------------------------\n")
        text.see(tk.END)
    except Exception:
        text.insert(tk.END, "USER: " + expression + "\n\n")
        text.insert(tk.END, "ROBY: Sorry, I couldn't evaluate the expression.\n")
        text.insert(tk.END, "--------------------------------------\n")
        text.see(tk.END)

window = tk.Tk()
window.geometry("501x620")
window.resizable(0, 0)
window.title("ROBY Chatbot")
window.configure(bg='#222831')
Font_tuple = ("cairo", 13, "bold")

pic_frame = tk.LabelFrame(window, highlightthickness=0, bg='#222831', padx=0, pady=0, width=512, height=210)
pic_frame['relief'] = 'flat'
pic_frame.pack(padx=2,pady=2)
background_image = ImageTk.PhotoImage(Image.open("S:/Projects/University/ROBY Chatbot project (S4)/Pic/ROBY.png"))
background_label = tk.Label(pic_frame, bg='#222831', image=background_image)
background_label['relief'] = 'flat'
background_label.place(x=0, y=0)

text_frame= tk.LabelFrame(window, highlightthickness=0, bg='#222831', padx=0, pady=0,  width=512, height=210)
text_frame['relief'] = 'flat'
text_frame.pack(padx=2,pady=2)

text = tk.Text(master=text_frame, wrap=tk.WORD, highlightthickness=0, width=55, height=18, bg='#222831', fg='#d6d8d6')
text['relief'] = 'flat'
text.pack(fill=tk.BOTH, expand=1)
text.configure(font = Font_tuple)

entry = customtkinter.CTkEntry(master=window, width=241, height=32, corner_radius=10)
entry.insert(0, "Enter the text here")
entry.pack(pady=10, padx=10, side=tk.LEFT, expand=True, fill=tk.BOTH)
entry.bind('<FocusIn>', temp_text)

button_send = customtkinter.CTkButton(master=window, corner_radius=10, bg="#3A1078",text="Send", width = 110, command=send_message)
button_send.pack(pady=10, padx=5, side=tk.LEFT)

button_quit = customtkinter.CTkButton(master=window, corner_radius=10, bg="#3A1078",text="Quit", width = 110, command=close_chatbot)
button_quit.pack(pady=10, padx=5, side=tk.LEFT)

window.bind('<Return>', key_return)

window.mainloop()