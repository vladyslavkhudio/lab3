import socket, threading, time

def encoder(text):
    """This function is using Ceasars ciphre to encode
    messages in our function"""
    text_new = ''
    digit = ''
    step1 = 1

    #Проходимося по кожному символу в тексті
    for a in text:
            #якщо цифра то збираємо в окрему стрінгу DIGIT
            range_ = ord(a)
            if range_ in range(48,58):
                digit = digit + a
                continue
            #якщо вжк не цифра і якщо DIGIT не пустий то зсовуємо його на 1 і запсуємо в результат і чистим DIGIT
            elif digit != "":
                digit = int(digit)
                digit = digit + step1
                digit = str(digit)
                text_new = text_new + digit
                digit = ""

            #якщо буква то
            if range_ in range(97,123) or range_ in range(1072,1104) or range_ in range(65,91) or range_ in range(1040,1072) or range_ == "1168"or"1169"or"1028"or"1108"or"1031"or"1111": ###IMPORTANT NOTE:
                if a == "Z":                                                                                                                                                               ###LAST RANGE DEFINITION IS FOR CHARACTERS
                    a = "A"                                                                                                                                                                   ### WHICH ARE ADDED RECENTLY IN CHARSET SO THEY HAVE
                    text_new = text_new + a                                                                                                                                                      ### CODE NOT IN UKR ALPHABET RANGE
                    continue                                                                                                                                                                           ###WE WILL DEFINE THEM WITH OTHER CHARACTERS
                                                                                                                                                                                                       ### DECODER WILL DECODE THIS CHARACTERS NORMALLY
                elif a == "z":
                    a = "a"
                    text_new = text_new + a
                    continue
                elif a == "Я":
                    a = "А"
                    text_new = text_new + a
                    continue
                elif a == "я":
                    a = "а"
                    text_new = text_new + a
                    continue
                else:
                    code_of_symbol = ord(a)
                    code_of_symbol += step1
                    a = chr(code_of_symbol)
                    text_new = text_new + a
                    continue
    #додаємо все з DIGIT якщо він не пустий в результат
    if digit != "":
        digit = int(digit)
        digit = digit + step1
        digit = str(digit)
        text_new = text_new + digit
    return text_new

def decoder(text):
    """This function is created to decode encrypted
    messages (in this repository is used to decrypt messages encrypted by function "encoder")"""
    text_new = ''
    digit = ''
    step1 = -1


    #Проходимося по кожному символу в тексті
    for a in text:
            #якщо цифра то збираємо в окрему стрінгу DIGIT
            range_ = ord(a)
            if range_ in range(48,58):
                digit = digit + a
                continue
            #якщо вжк не цифра і якщо DIGIT не пустий то зсовуємо його на 1 і запсуємо в результат і чистим DIGIT
            elif digit != "":
                    digit = int(digit)
                    digit = digit + step1
                    digit = str(digit)
                    text_new = text_new + digit
                    digit = ""

            #якщо буква то
            if range_ in range(97,122) or range_ in range(1072,1103) or range_ in range(65,90) or range_ in range(1040,1071) or range_ == "1168"or"1169"or"1028"or"1108"or"1031"or"1111": ###FOR LAST RANGE AND
                if a == "A":                                                                                                                                                              ###DESCIPRION ABOUT IT
                                                                                                                                                                                        ##YOU CAN SEE IN def_encoder.py
                    a = "Z"                                                                                                                                                             ##(also in this repository)
                    text_new = text_new + a
                    continue
                elif a == "a":
                    a = "z"
                    text_new = text_new + a
                    continue
                elif a == "А":
                    a = "Я"
                    text_new = text_new + a
                    continue
                elif a == "а":
                    a = "я"
                    text_new = text_new + a
                    continue
                else:
                    code_of_symbol = ord(a)
                    code_of_symbol += step1
                    a = chr(code_of_symbol)
                    text_new = text_new + a
                    continue
    #додаємо все з DIGIT якщо він не пустий в результат
    if digit != "":
        digit = int(digit)
        digit = digit + step1
        digit = str(digit)
        text_new = text_new + digit
    return text_new



key = 1
shutdown = False
join = False

x = input(' Decrypt messages? y/n: ')
def receving(name, sock):
    while not shutdown:
        try:
            while True:
                data, addr = sock.recvfrom(1024)

                decrypt = " "
                k = False
                if x == "y":
                    for i in data.decode("utf-8"):
                        if i == ":":
                            k = True
                            decrypt += i
                        elif k == False or i == " ":
                            decrypt += i
                        else:
                            decrypt += decoder(i)
                else:
                    for i in data.decode("utf-8"):
                        if i == ":":
                            k = True
                            decrypt += i
                        elif k == False or i == " ":
                            decrypt += i
                        else:
                            decrypt += i

                print(decrypt)


                time.sleep(0.2)
        except:
            pass


host = 192.168.0.106
port = 0

server = ("192.168.0.104", 4040)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(False)

alias = input("Name: ")

rT = threading.Thread(target=receving, args=("RecvThread", s))
rT.start()

while shutdown == False:
    if join == False:

        s.sendto(("[" + alias + "] => join chat ").encode("utf-8"), server)
        join = True
    else:
        try:
            message = input()



            message = encoder(message)


            if message != "":
                s.sendto(("[" + alias + "] :: " + message).encode("utf-8"), server)

            time.sleep(0.2)
        except:
            s.sendto(("[" + alias + "] <= left chat ").encode("utf-8"), server)
            shutdown = True

rT.join()
s.close()
