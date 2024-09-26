import requests

url = "http://localhost:5000/chat"

while True:
    user_message = input("You: ")
    if user_message.lower() in ['quit', 'exit']:
        break
    
    response = requests.post(url, json={"message": user_message})
    bot_response = response.json()["response"]
    print("Bot:", bot_response)

print("Chat ended.")

