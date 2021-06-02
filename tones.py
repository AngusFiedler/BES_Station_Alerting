# Import the required module for text 
# to speech conversion
from gtts import gTTS
import email_listener
import os, re, config
import webbrowser

def create_voice(voice_text, file_name): 

    # Create the voice object with the given text
    myobj = gTTS(text=voice_text, lang='en', slow=False)

    # Save theb voice object with the given file name
    myobj.save(file_name)

def call_type(email_txt):
    # Store the call type
    call_type_txt = "Unknown Call Type"

    # Water Rescue call type
    if "REWATR" in email_txt:
        call_type_txt = "Water Rescue"
    # Structure Fire call type
    elif "FISTRR" in email_txt:
        call_type_txt = "Structure Fire"
    # Major Accident
    elif "MAACCR" in email_txt:
        call_type_txt = "Major Accident"
    # Injury Accident call type
    elif "INACCR" in email_txt:
        call_type_txt = "Injury Accident"
    # Fire Support call type
    elif "FISUPR" in email_txt:
        call_type_txt = "Fire Support"
    # Fill the box call type
    elif "FTBR" in email_txt:
        call_type_txt = "Fill The Box"
    # Wildland Fire call type
    elif "FIWILR" in email_txt:
        call_type_txt = "Wildland Fire"
    # Technical Rescue call type
    elif "RETECR" in email_txt:
        call_type_txt = "Technical Rescue"
    # Hazmat call type
    elif "HAZFULR" in email_txt:
        call_type_txt = "Hazmat Response"
    # Mutual Aid
    elif "MUAIDR" in email_txt:
        call_type_txt = "Mutual Aid Request"
    # Fire Information
    elif "FIINFR" in email_txt:
        call_type_txt = "Fire Information"
    # Medical
    elif "EMSR" in email_txt:
        call_type_txt = "Medical Response"
    # Missing Person call Type
    elif "RELOSR" in email_txt:
        call_type_txt = "Lost Party"
    # Smoke Report call Type
    elif "FISMOR" in email_txt:
        call_type_txt = "Smoke Report"
    # Bat Chief call Type
    elif "AABACHFR" in email_txt:
        call_type_txt = "Structure Fire"
    # Air Accident Call Type
    elif "AIACCR" in email_txt:
        call_type_txt = "Air Accident"
    

    return call_type_txt

def call_add(email_txt):
    start = 'ADD:'
    end = 'BLD:'
    call_add_txt = email_txt[email_txt.find(start)+len(start):email_txt.rfind(end)]

    print(call_add_txt)
    return call_add_txt

def call_desc(email_txt):
    start = 'INFO:'
    end = 'TIME:'
    call_desc_txt = email_txt[email_txt.find(start)+len(start):email_txt.rfind(end)]

    print(call_desc_txt)
    return call_desc_txt

def interp_message(email_listener, msg_dict):
    # check if a message exists
    if msg_dict:
        first_msg = list(msg_dict.keys())[0]

        # get the plain text from the email
        email_txt = msg_dict[first_msg]['Plain_Text']

        # Print the email for debugging purposes
        print(email_txt)

        # Send the message to the interp 
        email_recieved(email_txt)

    # print(msg_dict['Plain_Text'])

def parse_emails():
    # Set your email, password, what folder you want to listen to, and where to save attachments
    email = config.email_address
    app_password = config.password
    folder = "Inbox"
    attachment_dir = "/attachments"
    el = email_listener.EmailListener(email, app_password, folder, attachment_dir)

    # Log into the IMAP server
    el.login()

   
    timeout = 60
    while (True):
        print("before Timeout")
        el.listen(timeout,process_func=interp_message)
        print("After Timeout")

def email_recieved(email_txt):
    # Start the timer
    filename = "/Timer/index.html"
    webbrowser.open('file://' + os.getcwd() + filename,new=2)

    # Get call type:
    call_type_txt = call_type(email_txt)
    create_voice(call_type_txt, "call_type.mp3")

    # Get call add
    call_add_txt = call_add(email_txt)
    create_voice(call_add_txt, "call_add.mp3")
    
    # Get call Desc
    call_desc_txt = call_desc(email_txt)
    create_voice(call_desc_txt, "call_desc.mp3")

    # Play the full audio
    os.system("mpg321 fire_paging.mp3")
    os.system("mpg321 call_type.mp3")
    os.system("mpg321 call_add.mp3")
    os.system("mpg321 call_desc.mp3")   

def main():
    parse_emails()

if __name__ == "__main__":
    main()