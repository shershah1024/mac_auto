import requests
import json

def send_email_request(message):
    # ngrok URL
    url = "https://oi-connection-b411b48bdba0.herokuapp.com//send_email"
    
    # Request headers
    headers = {
        "Content-Type": "application/json"
    }
    
    # Request payload
    payload = {
        "message": message
    }
    
    try:
        # Send POST request
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        
        # Check if the request was successful
        response.raise_for_status()
        
        # Print the response
        print("Response status code:", response.status_code)
        print("Response body:", response.json())
    
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)

# Example usage
if __name__ == "__main__":
    test_message = "Please send an email to shahir saying hi from your system"
    send_email_request(test_message)