import certifi
import ssl
import urllib.request

# Check if the certifi path is correctly set
print("Certifi path:", certifi.where())

# Test SSL connection with certifi's certificate
url = "https://www.google.com"
context = ssl.create_default_context(cafile=certifi.where())
try:
    with urllib.request.urlopen(url, context=context) as response:
        print("SSL Test Passed:", response.status == 200)
except Exception as e:
    print("SSL Test Failed:", e)
