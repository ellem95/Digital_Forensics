#import Python's hash, time, and string modules
import hashlib
import time
import string
#flag will increment if a password is cracked, if flag=0 at end then the password was not in the list.
#counter will record the number of passwords attempted
flag=0
counter = 0
#this function encodes and hashes character strings for use in the brute force attack
def myhashfuction():
    encode_guess = guess.encode('utf-8') #this encodes the string of characters as utf-8
    guesshash = hashlib.md5(encode_guess.strip()).hexdigest() #this hashes the encoded character string and returns it in hexadecimal
    if guesshash == password: #compares created hash with input hash
        time4 = time.time() #records time that password is found to calculate total time
        totaltime2 = time4-time3
        flag = 1
        print("Password is: " + guess)
        print("Passwords attempted: " + str(counter))
        print("Time taken: " + str(totaltime2) + " seconds.")
        exit()


attack = input("input attack type (1: dictionary, 2: brute force): ") #prompts user to select attack

#Dictionary attack
if attack == "1":
    wordlist = input("Wordlist: ") #input path to your wordlist file
    password = input("Enter password to crack: ") #input password hash; this input should be the hash and not a file containing the hash.
    try:
        time1 = time.time() #record initial time
        dictionary = open(wordlist, "r") #opens the wordlist file and reads it
        print(dictionary)
    except:
        print("No such file.")
        quit()
    for word in dictionary: #goes through each word in wordlist
        encode_word = word.encode('utf-8') #this encodes each word from the wordlist in utf-8, so it can be properly hashed
        passhash = hashlib.md5(encode_word.strip()).hexdigest()
        counter += 1 #adds 1 to counter so we can keep track of passwords attempted

        if passhash == password:
            time2 = time.time() #records time when matching hash is found
            totaltime = time2-time1 #total time taken to find matching hash
            print("The password is " + word)
            print("Passwords attempted: " + str(counter))
            print("Time taken: " + str(totaltime) + " seconds.")
            flag = 1 #this allows us to confirm that the password is not in the list if the flag is 0 after going through the entire list.
            exit()
    if flag == 0:
        print("Password is not in the list.")
        exit()

#Brute force attack:
#In this attack, I cycle through the characters as a nested for loop and then string together the characters as a "guess."
#I've originally used a set of 94 characters, containing all lowercase, uppercase, digits, and special characters.
#This obviously goes through a lot of possible passwords (94^5+94^4...etc.), so I reduced the number of special characters it goes through for a total of 75 characters (only common special characters).
if attack == "2":
    password = input("Enter password to crack: ") #enter hash, not file containing hash
    time3 = time.time() #start time
    characters = list(string.ascii_letters + string.digits + string.punctuation)[:75] #I originally used 'string.printable'(which contains all the punctuation and starts with digits), but changed it to this so that it would cycle through lower case letters before numbers.

    for char1 in characters:
        for char2 in characters:
            for char3 in characters:
                for char4 in characters:
                    for char5 in characters:
                        guess = (char1+char2+char3+char4+char5)
                        counter += 1 #increment the number of passwords tried
                        myhashfuction() #this function is defined at the beginning of the code
                    guess = (char1+char2+char3+char4)
                    counter += 1
                    myhashfuction()
                guess = (char1+char2+char3)
                counter += 1
                myhashfuction()
            guess = (char1+char2)
            counter += 1
            myhashfuction()
        guess = (char1)
        counter += 1
        myhashfuction()
    if flag == 0:
        time5 = time.time()
        listtime = time5 - time3
        print('Password not found.')
        print('Passwords attempted: ' + str(counter))
        print('Time taken: ' + str(listtime))
        exit()
else:
    print("Input not recognized.") #if you input anything other than 1 or 2 for the attack, it will provide this feedback
    exit()
