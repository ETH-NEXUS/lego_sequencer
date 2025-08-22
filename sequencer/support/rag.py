from openai import OpenAI
from openai import APIError, RateLimitError, APIConnectionError, BadRequestError, AuthenticationError
from sequencer.support.translations import get_translation, join_list
# set up logging
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)



def generate_reflection(api_key, seq, aln_infos, species, username, max_tokens=512, temperature=0.7, lang='en'):

    reflection_template = compile_reflection_template(seq, aln_infos, species, username, lang)
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

def compile_reflection_template(seq, aln_infos, species, username, lang):
        example, gene, variants, protein_var, domains_hit, json_data = aln_infos
        if example == "general":
            intro=get_translation("reflection_template.intro.general", lang).format(username=username, seq=seq)
            example_text = get_translation("reflection_template.examples.general", lang).format(species=join_list(species, lang))
            role=get_translation("reflection_template.role.general", lang)
        else:
            intro=get_translation("reflection_template.intro.examples", lang).format(username=username, seq=seq)

            example_text = get_translation(f"reflection_template.examples.{example}", lang).format(
                gene=gene,
                domain_phrase=get_translation("reflection_template.domains", lang).format(domains=join_list(domains_hit.keys(), lang)) if domains_hit else ""
            )
            if variants:
                var_list = join_list(variants, lang)
                if protein_var:
                    prot_list = join_list(protein_var, lang)
                    if example == "sars2_rbd":
                        protein_phrase = get_translation("reflection_template.sars_protein_variants", lang).format(variants=prot_list)
                    else:
                        protein_phrase = get_translation("reflection_template.protein_variants", lang).format(variants=prot_list)
                else:
                    protein_phrase = get_translation("reflection_template.no_protein_variants", lang)
                var_phrase = get_translation("reflection_template.variants", lang).format(variants=var_list, protein_phrase=protein_phrase)
            else:
                var_phrase = get_translation("reflection_template.no_variants", lang)
            example_text += "\n\n" + var_phrase    
            role=get_translation("reflection_template.role.examples", lang)
        # If species is a list, join it for the prompt
        reflection_template = f'{intro}\n\n{example_text}\n\n{role}'
        logger.info("Reflection example text: %s", reflection_template)
        return reflection_template
    

if __name__ == "__main__":
    # Example usage

    api_key = "<YOUR_API_KEY>"
    seq = "TGCTGTCAGTAGATCCCAAGCG"
    species = '"Notamacropus eugenii", "Ornithodoros turicata", "Candidatus Spongiihabitans", "Paenibacillus nuruki"'
    username = "Alice"
    lang = "en"
    aln_infos = ("general", "unknown", [], [], {})
    for part in generate_reflection(api_key, aln_infos=aln_infos, species=species, username=username, lang=lang):
        if part is not None:
            print(part, end='', flush=True)