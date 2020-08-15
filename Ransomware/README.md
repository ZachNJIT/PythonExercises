THIS IS JUST A PROOF OF CONCEPT FOR STUDENTS. Use of ransomware for
nefarious purposes is illegal in most jurisdictions. This project 
was conceived an in-class demonstration of effective and ineffective
mitigation strategies against ransomware, and it should be used to that end.

Configuration of ransomware Python script.

The script is currently set to encrypt all .txt and .docx files in
the /home directory, create a decrypt key, and leave one copy on
the system while sending one to a remote email address. The following
parameters should be adjusted in main.py before execution:

Line 17: File types can be added or removed as needed (now .txt,.docx)
	In practice, documents and media are often targeted, i.e.
	files such as .pdf,.rtf,.jpg,.png,.wav,.mov,.mp3,etc

Line 66: Specifies the local root of the encryption process. Here, we
	have chosed /home for a more realistic ransomware simulation.
	For simply verify the program behavior, however, this can be
	changed to '.' to target only the active directory.

Line 85: The 'from' address of the SMTP email. The SMTP server must
	be configured to use this address
Line 86: The 'to' address of the SMTP email. The SMTP server must be
	configured to use this address

Line 97: The address of the SMTP server should be replaced with that
	of the attacker. Almost all SMTP servers are compatible with
	can use port 587, so it is unlikely that this will need to be
	modified. If port 587 is unsuccessful, ports 588, 2525, 465,
	25, and 80 can be tried, in that order.
Line 98: The user and pass login credentials of the SMTP sever. Here,
	Mailjet accepts hashed versions of these credentials. Other
	SMTP servers such as Dreamhost require the actual user and 
	pass here
	
Line 100: The Bitcoin wallet address should be that of the attacker's

Running the ransomware Python script

First, Python3 and PyCrypto must be installed. In Ubuntu, this can be
done with

sudo pip install pycrypto

Then, with the program folder as the active directory, use the terminal
command

python3 main.py --create encrypt

to encrypt user personal files. Python3 must be used for the SMTP server
to work. The encryption leaves a decoder in the program folder. To decrypt,
move the decoder to the decrypt directory and use the terminal command

python3 main.py --create decrypt --decoder ./decrypt/decoder

This script is intended to be run on Linux, but it is possible it may run
on Mac or Windows with the appropriate modification to Line 66 to fit
the needed directory stle.

Antivirus software

While too long to detail here, installation directions for ClamAV and
Sophos antivirus can be found at their respective sites.

ClamAV: https://www.clamav.net/
Sophos: https://www.sophos.com/en-us/free-tools/sophos-antivirus-for-linux.aspx

It should also be possible to install ClamAV with the following command
in terminal:

apt-get install clamav clamav-daemon clamav-freshclam

Once ClamAV is installed, to scan the main.py file, use the following
command in terminal with the project folder as the active directory:

clamscan main.py

To activate ClamAV scanning daemon, with root permission edit the conf
/etc/clamav/clamd.conf to change the following line

LocalSocketGroup root
User root

Then start the clamav-daemon with the terminal command

systemctl start clamav-daemon


To enable Sophos scanning and Live protection, use the following commands in
terminal:

sudo /opt/sophos-av/bin/savdctl enable
sudo /opt/sophos-av/bin/savconfig LiveProtection true



