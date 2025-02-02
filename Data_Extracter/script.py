import os
import json

if __name__== '__main__':

    # Read the first JSON file
    with open('data/audio.json', 'r') as f1:
        json1 = json.load(f1)

    # Read the second JSON file
    with open('data/screen.json', 'r') as f2:
        json2 = json.load(f2)

    # Combine them into a list
    combined_json = json1+json2

    # Save the combined JSON to a new file
    with open('data/res.json', 'w') as outfile:
        json.dump(combined_json, outfile, indent=4)

    # Print to verify
    print(combined_json)

    os.system("scp -i ~/HackVM.pem /Users/felixmeng/Desktop/Coinbase_Hackathon/data/res.json ubuntu@ec2-35-89-143-40.us-west-2.compute.amazonaws.com:/home/ubuntu/PrivatePersonalAgent/data.json")



   
