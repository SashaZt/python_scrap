import openai

API_KEY = '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'
openai.api_key = API_KEY


def general_response(text):
    response = openai.Completion.create(
        prompt=text,
        engine='text-davinci-003',
        max_tokens=500,
        temperature=0.7,
        n=1,
        stop=None,
        timeout=15

    )
    if response and response.choices:
        return response.choices[0].text.strip()
    else:
        return None
text = """Bogotto Tokyo perforated Motorcycle Shoes

The Bogotto Tokyo motorcycle shoes have a short shaft, knitted upper with microfiber elements and are perforated.
The flat entry at the back of the shoe, allows easy entry and prevents pressure points arise.

"""
try:
    res = general_response(f'я тебе дам текст, {text} переведи его и сделай пожалуйста рерайт на украинском языке')
    print(res)
except openai.error.RateLimitError:
    print("Превышен квотный лимит API. Пожалуйста, подождите и попробуйте снова позже.")
