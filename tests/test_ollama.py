import requests

url = "http://localhost:11434/api/generate"
payload = {
    "model": "llama2",
    "prompt": "Here is a caption from children's story book page: 'a cartoon of two girls talking to each other'. And here part of the story related to the image ' Once upon atime there lived twin sisters. Their names were Tinky and Pinky. Their mother told that they should not go to a particular pond. But they wanted to know what was there in the pond. So the went to the pond. suddenly friendly monster sprang up.'.Describe it vividly with excitement and emotions as if telling a story to visually impaired child. The story continues in next page so do not add anything that is not there in the prompt",
    "stream": False
}

response = requests.post(url, json=payload)
resp_data = response.json()
print(resp_data["response"])
