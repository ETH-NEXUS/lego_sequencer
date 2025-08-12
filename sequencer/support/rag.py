from openai import OpenAI
from openai import APIError, RateLimitError, APIConnectionError, BadRequestError, AuthenticationError
from sequencer.support.translations import get_translation



def generate_reflection(api_key, seq, species, max_tokens=512, temperature=0.7, username=None, lang='en'):
    if not isinstance(seq, str):
        yield get_translation("not_a_sequence", lang).format(seq=seq)
        return
    if username is None:
        username = "a guest of the anniversary party"
    example=check_sequence(seq)
    reflection_template = get_translation("reflection_template", lang)[example]

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
                    "content": reflection_template.format(seq=seq, species=species, username=username),
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

def check_sequence(seq):
    """
    Align the sequence with a set of known examples to determine the type of reflection to generate.
    Allow for missmatches and gaps. 
    The examples are fragments but in frame. 
    Return the example name that matches best, the variants with respect to that example, and the amino acid sequence.
    return 'general' if no match is found.
    """



if __name__ == "__main__":
    # Example usage

    api_key = "<YOUR_API_KEY>"
    seq = "TGCTGTCAGTAGATCCCAAGCG"
    species = '"Notamacropus eugenii", "Ornithodoros turicata", "Candidatus Spongiihabitans", "Paenibacillus nuruki"'

    for part in generate_reflection(api_key, seq, species):
        if part is not None:
            print(part, end='', flush=True)