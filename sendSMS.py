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

def startUpPrompt():
	global userName
	print "\tTo exit program type: exit\n\n"
	userName = raw_input("What is your CSH username: ")
	if userName == "exit" or userName == "Exit":
		print "Terminating program..."
	else:
		print "\nYou typed: "+userName+"\n"
		verify = raw_input("Is that correct. yes/no?  ")
		if verify == "exit" or verify == "Exit":
			print "Terminating program..."
		elif verify == "yes" or verify == "Yes" or verify == "y" or verify == "Y":
			main(userName)
		elif verify == "no" or verify == "No" or verify == "n" or verify == "N":
			startUpPrompt()
		else:
			print "Error: Not a valid input."
			startUpPrompt()
def send(num, mssg):
	message = {
                "number": num,
                "message": mssg
        }
	r = requests.post('http://textbelt.com/text', message)
        print r.json()


def collect(input):
	global ldap, phoneNumber, commonName, joinedDate, housingPoints, homeDir
	
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
def getCSHPhoneNum():
	#sends a message to all of the numbers stored in ldap for user specified
        for number in member['mobile']:
                for digit in number:
                        #only numbers stored in the phone number field are added to clean_number
                        if digit in "1234567890":
                                 phoneNumber += digit
def printStats():
	memberStats = "\n\n"+commonName+":\n"+"\nMember Since: "+joinedDate+"\nHome Directory: "+homeDir+"\nHousing Points: "+housingPoints
        print memberStats


def sendNonCSHText(phoneNum, mssg):
	send(int(phoneNum),commonName+" is sending you a message:\n"+ mssg)
def sendCSHText(cshUID, mssg):
	global phoneNumber
	if cshUID == userName:	
		send(int(phoneNumber),"Note to self:\t"+mssg)
		startUpPrompt()
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
def main(input):
	collect(input)
	printStats()
	print "\nCSH Texting Service: \n" 
	input = raw_input("Send to nonCSH/CSH:  ")
	if input == "nonCSH":
		phoneNums = raw_input("Enter the cell phone number: ")
		message = raw_input("Enter your message here. Press ENTER to send. : ")
		sendNonCSHText(phoneNums, message)	
	elif input == "CSH":
		newUsername = raw_input( "Enter CSHer username you wish to message: ")
		inputMessage = raw_input("Enter your message here. Press ENTER to send. : ")
		sendCSHText(newUsername,inputMessage)
if __name__ == '__main__':
	print "\nHello CSHer!\n"
	startUpPrompt()
	#main()
