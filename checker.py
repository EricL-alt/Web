import subprocess
import requests
from twilio.rest import Client
import sys

account_sid = 'ACf49334f0ea0f6c89efa5405c5b7a40f5'
auth_token = "0aa66c20970c9c83ffddd179a59cf177"
twilio_phone_number = '+18887261654'
client = Client(account_sid, auth_token)

applescript_code = '''
tell application "Safari"
    set tabList to {}
    -- Iterate over all windows
    repeat with w in windows
        -- Iterate over all tabs in the current window
        repeat with t in tabs of w
            set end of tabList to URL of t
        end repeat
    end repeat
end tell

-- Return the list of URLs
return tabList
'''

def run_applescript(script):
    try:
        result = subprocess.run(
            ['osascript', '-e', script],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip().split(', ')
    except subprocess.CalledProcessError as e:
        print(f"Error running AppleScript: {e}")
        return []


def classify(text):
    key = "59047a90-68c0-11ef-a82e-ebdea7ffdecdbbda1bd5-b065-4a72-8778-fba8038a95c4"
    url = "https://machinelearningforkids.co.uk/api/scratch/"+ key + "/classify"

    response = requests.get(url, params={ "data" : text })

    if response.ok:
        responseData = response.json()
        topMatch = responseData[0]
        return topMatch
    else:
        response.raise_for_status()

urls = run_applescript(applescript_code)
for url in urls:
    print(url)
    demo = classify(url)
    label = demo["class_name"]
    confidence = demo["confidence"]
    print ("result: '%s' with %d%% confidence" % (label, confidence))

    parameter = sys.argv[1]
    if label=='bad':
        for phone_number in parameter.split(","):
            to_phone_number = phone_number    #'8142808979'
            message_body = 'This is a message from Procrastination Pulverize, I would suggest closing the tab ' + url + ' because it could be a distraction.'

            message = client.messages.create(
                    body=message_body,
                    from_=twilio_phone_number,
                    to=to_phone_number
            )
            print(f'Message sent with SID: {message.sid}')