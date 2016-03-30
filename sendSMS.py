import requests, secrets
from csh import cshldap
#ldap has the username and password needed to authenticate with ldap
ldap = cshldap.LDAP(secrets.ldapusername, secrets.ldappass)
"""
userName	~the username associated with the CSHer logging into the program
phoneNuber	~the phoneNumber retrieved from ldap for the CSHer logging in
commonName	~the common name stored for the CSHer in ldap
joinedDate	~the date the CSHer had an account created in ldap
housingPoints	~the number of housing points the user has recorded in ldap
homeDir		~the home directory for the CSHer in ldap
"""
userName = ""
phoneNumber = ""
commonName = ""
joinedDate = ""
housingPoints = ""
homeDir = ""
"""
Prompts the CSHer for their username. After verfifying the userName, it then calls the main method in order to
	prompt the user for how and who they want to send a message to. 
"""
def startUpPrompt():
	global userName
	print "\tTo exit program type: exit\n\n"		#EXIT PROGRAM PROMPT
	userName = raw_input("What is your CSH username: ")
	if userName == "exit" or userName == "Exit":
		print "Terminating CSH Texting Service..."	#EXITING PROGRAM PROMPT
	else:
		print "\nYou typed: "+userName+"\n"		#verify the username entered
		verify = raw_input("Is that correct. yes/no?  ")
		if verify == "exit" or verify == "Exit":
			print "Terminating CSH Texting Service..."
		elif verify == "yes" or verify == "Yes" or verify == "y" or verify == "Y":	#calls the main function to continue
			main(userName)
		elif verify == "no" or verify == "No" or verify == "n" or verify == "N":	#reprompts if an error is found
			startUpPrompt()
		else:
			print "Error: Not a valid input."					#prompts that the user input was invalid
			startUpPrompt()
"""
Sends the text message to the number specified.
"""
def send(num, mssg):
	message = {
                "number": num,
                "message": mssg
        }
	r = requests.post('http://textbelt.com/text', message)
	print "MESSAGE STATUS: \n"
        print r.json()						#prints the status of the sent message

"""
Collects information about the CSHer logging into the program. It will retreieve their phone number, their housing point count,
	homeDir address, as well as the date they joined CSH. It then prints out that information to the terminal.
"""
def collect(input):
	global ldap, phoneNumber, commonName, joinedDate, housingPoints, homeDir
	#stores the information gathered from ldap
	member = ldap.member(input)
	clean_number =  ""
	memberDate = ""
	housingPoints = ""
	
	#sends a message to all of the numbers stored in ldap for user specified
	for number in member['mobile']:
		for digit in number:
			#only numbers stored in the phone number field are added to clean_number
			if digit in "1234567890":
				 phoneNumber += digit
			commonName = member['cn'][0]
			inputDate = member['memberSince'][0]
			#joinedDate is the date formatted String MM/DD/YYYY
			joinedDate = inputDate[4:6] +"/"+ inputDate[6:8]+"/"+inputDate[0:4]
			housingPoints = member['housingPoints'][0]
			homeDir = member['homeDirectory'][0]
"""
Retrieves the phoneNumber of the CSHer from ldap. If the user did enter a number into Profiles, it will appear in ldap.
"""
def getCSHPhoneNum():
	#sends a message to all of the numbers stored in ldap for user specified
        for number in member['mobile']:
                for digit in number:
                        #only numbers stored in the phone number field are added to clean_number
                        if digit in "1234567890":
                                 phoneNumber += digit
"""
printStats creates a summary of the information gathered about the CSHer logged into the program. This information is 
	called and printed to the screen. 
"""
def printStats():
	memberStats = "\n\n"+commonName+":\n"+"\nMember Since: "+joinedDate+"\nHome Directory: "+homeDir+"\nHousing Points: "+housingPoints
        print memberStats

"""
sendNonCSHText is called when a user specifies they want to send a text message to a member either not yet entered their number into ldap
	or is not a member at all. They will provide a phone number followed by a message.
"""
def sendNonCSHText(phoneNum, mssg):
	send(int(phoneNum),commonName+" is sending you a message:\n"+ mssg)
"""
sendCSHText is called when a user wants to send a message internally to another CSHer. The user must know the other CSHer's username and then
	provide a message to send to that user.
"""
def sendCSHText(cshUID, mssg):
	global phoneNumber
	#if the user is sending a message to themselves, then it adds a header "Note to self:"
	if cshUID == userName:	
		send(int(phoneNumber),"Note to self:\t"+mssg)
		startUpPrompt()
	#if it is no the user logging in, it then sends a message with no header
	else:
		newMember = ldap.member(cshUID)
		phoneNums = newMember['mobile'][0]			
		formattedNum = ""
		#sends a message to all of the numbers stored in ldap for user specified
        	for number in newMember['mobile']:
                	for digit in number:
                        	#only numbers stored in the phone number field are added to clean_number
                        	if digit in "1234567890":
                                	formattedNum += digit
		send(int(formattedNum),mssg)
		startUpPrompt()
"""
main method is called after a user has succesfully entered there username and verified. This will then prompt them how and who they want
	to send a message to.
"""
def main(input):
	#collects the stats on the user logging into the program
	collect(input)
	#prints the collected stats to the terminal
	printStats()
	print "\nWelcome to the CSH Texting Service: \n" 
	#prompts the user if the message is for a CSHer with a logged phone number or not
	input = raw_input("Send to (manual/CSH phone) CSH phone is only for members with phone numbers already in ldap :  ")
	if input == "manual":
		phoneNums = raw_input("Enter the cell phone number: ")
		message = raw_input("Enter your message here. Press ENTER to send. : ")
		sendNonCSHText(phoneNums, message)	
	elif input == "CSH phone":
		newUsername = raw_input( "Enter CSHer username to SEND message to: ")
		inputMessage = raw_input("Enter your message here. Press ENTER to send   : ")
		sendCSHText(newUsername,inputMessage)
if __name__ == '__main__':
	#prints the welcome screen
	print "\nHello CSHer!\n"
	startUpPrompt()
	
