import google.generativeai as genai

# Put your actual API key here
genai.configure(api_key="AIzaSyCZm2ZXvui73wT8aUiZorb44A1xeCj002A")

print("Available Models for generateContent:")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(f" - {m.name}")