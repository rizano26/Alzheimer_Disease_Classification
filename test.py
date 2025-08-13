import requests

url = "https://dementia-api-277145010791.europe-west1.run.app/predict"
image_path = "26 (69).jpg"  # Sesuaikan dengan file yang ada

with open(image_path, "rb") as f:
    files = {"file": f}
    response = requests.post(url, files=files)

print("Status code:", response.status_code)
print("Response text:")
print(response.text)