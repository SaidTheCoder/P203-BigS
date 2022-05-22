import socket
from threading import Thread
import random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000

server.bind((ip_address, port))
server.listen()

list_of_clients = []
nicknames = []

questions = [
     " Entomology is the science that studies \n A.Insects\n B.Formation of Rocks\n C.Behaviour of human beings\n D.Living Organisms",
     " At what temperature do the Fahrenheit and Celsius scales give the same reading ? \n A.32° \n B.0° \n C.-40° \n D.212°",
     " Which of the following is not an Ed Sheeran Album? \n A.+ \n B.- \n C.= \n D.÷",
     " Who is the author of the Sherlock Holmes Series? \n A.Agatha Christie \n B.Edgar Allen Poe\n C.Arthur Conan Doyle\n D.Mark Twain",
     " Which continent has the most countries? \n A.Africa\n B.Asia \n C.Europe\n D.North America",
     " What is the first element on the periodic table? \n A.He\n b.C \n C.O\n D.H",
     " Which team won the IPL 2021? \n A.Mumbai Indians \n B.Chennai Super Kings\n C.Sunrisers Hyderabad\n D.Royal Challengers Bangalore",
     " Who is Hades according to Greek Mythology? \n A.God of Sky\n B.God of Seas\n C.God of War\n D.God of Death",
]

answers = ['A', 'C', 'B', 'C', 'A', 'D', 'B', 'D']

print("Server has started...")

def get_random_question_answer(conn):
    random_index = random.randint(0,len(questions) - 1)
    random_question = questions[random_index]
    random_answer = answers[random_index]
    conn.send(random_question.encode('utf-8'))
    return random_index, random_question, random_answer

def remove_question(index):
    questions.pop(index)
    answers.pop(index)

def clientthread(conn, nickname):
    score = 0
    conn.send("Welcome to this quiz game!".encode('utf-8'))
    conn.send("You will receive a question. The answer to that question should be one of A, B, C or D!\n".encode('utf-8'))
    conn.send("Good Luck!\n\n".encode('utf-8'))
    index, question, answer = get_random_question_answer(conn)
    print(answer)
    while True:
        try:
            message = conn.recv(2048).decode('utf-8')
            if message:
                if message.split(": ")[-1] == answer:
                    score += 1
                    conn.send(f"Bravo! Your score is {score}\n\n".encode('utf-8'))
                else:
                    conn.send("Incorrect answer! Better luck next time!\n\n".encode('utf-8'))
                remove_question(index)
                index, question, answer = get_random_question_answer(conn)
                print(answer)
            else:
                remove(conn)
                remove_nickname(nickname)
        except Exception as e:
            print(str(e))
            continue

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

def remove_nickname(nickname):
    if nickname in nicknames:
        nicknames.remove(nickname)

while True:
    conn, addr = server.accept()
    conn.send('NICKNAME'.encode('utf-8'))
    nickname = conn.recv(2048).decode('utf-8')
    list_of_clients.append(conn)
    nicknames.append(nickname)
    print (nickname + " connected!")
    new_thread = Thread(target= clientthread,args=(conn,nickname))
    new_thread.start()