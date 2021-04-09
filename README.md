# CongressionalTwitterBot
Replies to members of Congress and the Senate with their office's phone number to increase accessibility and accountability

To modify:  
Clone the repository  
```git clone https://github.com/johnbumgardner/CongressionalTwitterBot.git```  
Create a developer account and get API and Access Tokens  
```touch auth.json```  
Fill auth.json with  
```
{
	"api_key": "API_KEY",
	"api_secret_key": "API_SECRET_KEY",
	"access_token": "ACCESS_TOKEN",  
	"access_token_secret": "ACCESS_TOKEN_SECRET",
}
```  
Build the Docker image  
```docker build . -t congress-bot```  
Run the image  
```docker run -it congress-bot```  
