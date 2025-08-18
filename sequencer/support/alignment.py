from Bio import Align
from Bio.Seq import Seq
import json
import math
import os

# Load the examples JSON
EXAMPLES_PATH = os.path.join(os.path.dirname(__file__), "sequence_examples.json")

with open(EXAMPLES_PATH) as f:
    EXAMPLES = json.load(f)


def make_blast_mock_single_hit(
    alignment,name='Homo sapiens'
) -> dict:
    """
    Build a minimal BLAST JSON-like dict with a single hit, keeping only fields you care about.
    - Uses gapped qseq/hseq and a BLAST-style midline.
    - Computes identity, align_len, gaps (count of '-' chars across both strings).
    """
    # Basic sanity checks
    qseq = str(alignment[0])
    hseq = str(alignment[1])
    midline = get_match_line(hseq, qseq)  # midline is the match line
    score = alignment.score
    hit_len = (
        alignment.aligned[1][0][1] - alignment.aligned[1][0][0] + 1
    )  # 1-based length of the hit
    align_len = len(qseq)  # length of the query sequence
    return {
        "BlastOutput2": [
            {
                "report": {
                    "results": {
                        "search": {
                            "hits": [
                                {
                                    "description": [{"sciname": name}],
                                    "hsps": [
                                        {
                                            "score": score,
                                            "query_strand": "Plus",
                                            "hit_strand": "Plus",
                                            "align_len": align_len,
                                            "qseq": qseq,
                                            "midline": midline,
                                            "hseq": hseq,
                                        }
                                    ],
                                }
                            ]
                        }
                    }
                }
            }
        ]

    }


def blast_mock_json(**kwargs) -> str:
    """Convenience wrapper: returns a pretty-printed JSON string."""
    return json.dumps(make_blast_mock_single_hit(**kwargs), indent=2)


def var_string(var):
    """
    Convert a variant tuple to a string representation.
    """
    if var[2] == "sub":
        return f"c.{var[0]}{var[3]}"
    if var[0] != var[1]:
        return f"c.{var[0]}_{var[1]}{var[2]}{var[3]}"
    return f"c.{var[0]}{var[2]}{var[3]}"


def _normalize_nt(s: str) -> str:
    return "".join(s.split()).upper().replace("U", "T")


def get_aa(seq):
    return str(Seq(seq).translate())


def minmax(x):
    if not x:
        return None, None
    return min(x), max(x)


def find_best_match(seq: str, percent_identity=0.7):
    """
    Align 'seq' to known examples (local alignment).
    Returns:
      - best example name (or 'general')
      - list of nt variants (within core alignment only)
      - AA sequence from aligned query (trimmed to full codons)
      - AA sequence from query (aligned part)
      - AA offset in query
    """
    seq = _normalize_nt(seq)
    min_score = len(seq) * percent_identity  # minimum score for a decent alignment
    aligner = Align.PairwiseAligner()
    aligner.mode = "local"
    aligner.match_score = 1
    aligner.mismatch_score = -2
    aligner.open_gap_score = -3
    aligner.extend_gap_score = -2

    best_name, best_alignment = "general", None
    for name, data in EXAMPLES.items():
        ref = _normalize_nt(data["sequence"])
        offset = data["codon_offset"]
        alns = aligner.align(seq, ref)
        if alns[0].score < min_score:
            continue
        if alns and (best_alignment is None or alns[0].score > best_alignment.score):
            best_name, best_alignment, example, gene = name, alns[0], data.get("example"), data.get("gene")

    if best_alignment is None:
        # No decent local alignment; return general + whole-seq translation
        return "general", [], None, None, None, None, None, None, None

    # Build core gapped strings (no soft-clipped ends)
    aln_query, aln_ref = best_alignment[0], best_alignment[1]

    # Variant calling within the core region only
    variants = []  # list of variant tuples: (start, end, type, seq)
    ref_nt_idx = offset * 3  # 1-based position within the *reference core alignment*

    for i, (q_nt, r_nt) in enumerate(zip(aln_query, aln_ref)):
        if r_nt != "-":
            ref_nt_idx += 1
        if q_nt == r_nt:
            continue
        if q_nt != "-" and r_nt != "-":
            variants.append(
                (ref_nt_idx, ref_nt_idx, "sub", f"{r_nt}>{q_nt}", [i])
            )  # substitution
        elif q_nt == "-":
            variants.append(
                (ref_nt_idx, ref_nt_idx, "del", r_nt, [i])
            )  # deletion vs ref
        elif r_nt == "-":
            variants.append(
                (ref_nt_idx, ref_nt_idx, "ins", q_nt, [i])
            )  # insertion vs ref
    indel = None
    variants_joined = []
    for var in variants:
        if indel is not None and var[2] == indel[2] and indel[1] + 1 == var[0]:
            # join indels together
            indel = (
                indel[0],
                var[0],
                indel[2],
                indel[3] + var[3],
                indel[4] + var[4],
            )  # extend the indel
        elif var[2] != "sub":
            if indel is not None:
                variants_joined.append(indel)
            indel = var
        else:
            if indel:
                variants_joined.append(indel)
                indel = None
            variants_joined.append(var)
    if indel:
        variants_joined.append(indel)

    q_nogap = aln_query.replace("-", "")
    r_nogap = aln_ref.replace("-", "")
    # reference sequence is always in frame, we can check the query offset
    ref_start_nt = best_alignment.aligned[1][0][0]  # 0-based index into reference
    shift = 3 - ref_start_nt % 3
    if shift:
        q_nogap = q_nogap[shift:]  # remove leading soft-clips
        r_nogap = r_nogap[shift:]  # remove leading soft-clips
    if len(q_nogap) % 3:
        q_nogap = q_nogap[: len(q_nogap) - (len(q_nogap) % 3)]
    if len(r_nogap) % 3:
        r_nogap = r_nogap[: len(r_nogap) - (len(r_nogap) % 3)]
    aa_seq_q = get_aa(q_nogap)
    aa_seq_r = get_aa(r_nogap)
    aa_offset = math.ceil(ref_start_nt / 3) + offset  # 1-based AA offset in query
    return (
        best_name,
        [var_string(v) for v in variants_joined],
        aa_seq_q,
        aa_seq_r,
        aa_offset,
        offset * 3,
        best_alignment, 
        example, 
        gene,
    )


def get_match_line(ref, query):
    line = []
    for r, q in zip(ref, query):
        if r == q:
            line.append("|")
        elif r == "-" or q == "-":
            line.append("-")
        else:
            line.append(".")
    return "".join(line)


def format_alignment(aln, offset=0):
    """
    Format the alignment for display.
    Returns a tuple of (reference, match line, query).
    """
    ref = aln[1]
    query = aln[0]
    offset_ref = str(offset + aln.aligned[1][0][0])
    offset_query = str(aln.aligned[0][0][0])
    space = max(len(offset_ref), len(offset_query))
    offset_ref = offset_ref.rjust(space)  # right-align offset
    offset_query = offset_query.rjust(space)  # right-align offset

    match_line = (" " * (space + 2)) + get_match_line(ref, query)

    return f"{offset_ref}: {ref}\n{match_line}\n{offset_query}: {query}"


if __name__ == "__main__":
    # Example usage
    seq = "TGGGCTCCTTTGCGTTCACGGTGTATAAGGGACTCTTGATCCCAGAAGGAGTTAAAATTCCCGTCGCTATCAAGGAATTAAGAGAAGCAACA"
    (
        name,
        variants,
        aa_seq_q,
        aa_seq_r,
        aa_offset,
        nt_offset,
        aln,
        example,
        gene
        
    ) = find_best_match(seq, percent_identity=0.5)

    print(f"Best match: {name}")
    if name != "general":
        print(f'seq={seq}'),
        print((f'matched_example={name}')),
        print(f'username="Matthias Lienhard"'),
        print(f'variants={", ".join(variants)}'),
        print(f'aln=\n{format_alignment(aln, offset=nt_offset)}'),
        print(f'aa_seq_q={aa_seq_q}'),
        print(f'aa_seq_r={aa_seq_r}'),
        print(f'aa_offset={aa_offset}'),
        

