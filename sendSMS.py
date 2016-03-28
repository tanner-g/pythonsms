import requests, secrets
from csh import cshldap

def send(num, mssg):
	message = {
                "number": num,
                "message": mssg
        }
	r = requests.post('http://textbelt.com/text', message)
        print r.json()


def main():
	names = ['tnrglantz', 'smirabito']

	ldap = cshldap.LDAP("tnrglantz", secrets.ldappass)
	for name in names:
		member = ldap.member(name)
		number = "".join(_ for _ in member['mobile'][0] if _ in "1234567890")
		send(int(number), "Hi "+member['cn'][0])

if __name__ == '__main__':
	main()
