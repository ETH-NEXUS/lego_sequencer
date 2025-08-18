from openai import OpenAI
from openai import APIError, RateLimitError, APIConnectionError, BadRequestError, AuthenticationError
from sequencer.support.translations import get_translation



def generate_reflection(api_key, reflection_template, max_tokens=512, temperature=0.7, username=None, lang='en'):

    
    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        stream = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "<YOUR_SITE_URL>",
                "X-Title": "<YOUR_SITE_NAME>",
            },
            model="openai/gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": reflection_template,
                },
            ],
            max_tokens=max_tokens,
            temperature=temperature,
            stream=True
        )
        for chunk in stream:
            if hasattr(chunk.choices[0].delta, "content"):
                yield chunk.choices[0].delta.content
    except RateLimitError:
        yield get_translation("rate_limit", lang)
    except APIConnectionError:
        yield get_translation("connection_error", lang)
    except BadRequestError as e:
        yield get_translation("bad_request", lang).format(error=e)
    except AuthenticationError:
        yield get_translation("auth_error", lang)
    except APIError as e:
        yield get_translation("api_error", lang).format(error=e)
    except Exception as e:
        yield get_translation("unexpected_error", lang).format(error=e)



if __name__ == "__main__":
    # Example usage

    api_key = "<YOUR_API_KEY>"
    seq = "TGCTGTCAGTAGATCCCAAGCG"
    species = '"Notamacropus eugenii", "Ornithodoros turicata", "Candidatus Spongiihabitans", "Paenibacillus nuruki"'

    for part in generate_reflection(api_key, seq, species):
        if part is not None:
            print(part, end='', flush=True)