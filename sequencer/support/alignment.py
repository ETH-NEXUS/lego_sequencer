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
    alignment,gene='Gene'
) -> dict:
    """
    Build a minimal BLAST JSON-like dict with a single hit, keeping only fields you care about.
    - Uses gapped qseq/hseq and a BLAST-style midline.
    - Computes identity, align_len, gaps (count of '-' chars across both strings).
    """
    # Basic sanity checks
    qseq, midline, hseq, start_gaps, end_gaps = format_alignment(alignment, gene)
    score = alignment.score
    hit_len = (
        alignment.aligned[1][0][1] - alignment.aligned[1][0][0] + 1
    )  # 1-based length of the hit
    align_len = len([c for c in qseq if c != "-"])  # length of the query sequence
    return {
        "BlastOutput2": [
            {
                "report": {
                    "results": {
                        "search": {
                            "hits": [
                                {
                                    "description": [{"sciname": gene}],
                                    "hsps": [
                                        {
                                            "score": score,
                                            "query_strand": "Plus",
                                            "hit_strand": "Plus",
                                            "align_len": align_len,
                                            "aln_start" : start_gaps +1,
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
    aligner.mode = "global"
    aligner.match_score = 1
    aligner.mismatch_score = -1
    aligner.open_gap_score = -3
    aligner.extend_gap_score = -.5
    aligner.target_end_gap_score = 0        # no penalty at ref ends



    best_name, best_alignment = "general", None
    for name, data in EXAMPLES.items():
        ref = _normalize_nt(data["sequence"])
        alns = aligner.align(seq, ref)
        if alns[0].score < min_score:
            continue
        if alns and (best_alignment is None or alns[0].score > best_alignment.score):
            best_name, best_alignment = name, alns[0]

    return best_name, best_alignment


def resolve_variant(var, aln_ref, aln_query):
    if len(var) == 1:
        return var[0]
    rna_pos= min([v[0][0] for v in var]), max([v[0][1] for v in var])
    idx=min([v[1][0] for v in var]), max([v[1][1] for v in var])
    codons=min([v[2][0] for v in var]), max([v[2][1] for v in var])
    if all (v[3] == "ins" for v in var) or all (v[3] == "del" for v in var):
        alt= "".join(v[4] for v in var)
        vartype= var[0][3]
    else:
        vartype = 'delins'
        r= "".join(aln_ref[i] for i in range(idx[0], idx[1]+1) if aln_ref[i] != "-")
        a= "".join(aln_query[i] for i in range(idx[0], idx[1]+1) if aln_query[i] != "-")
        alt = f"{r}>{a}" 
    #print(f"Resolving variant: {var} to {rna_pos}, {idx}, {codons}, {vartype}, {alt}")
    return (rna_pos, idx, codons,vartype, alt )

def get_idx(idx,n, aln_ref, aln_query):
    # go n nt in aln_query and return the index in aln_query
    
    step = 1 if n<0 else -1
    i=n
    pos=idx
    while i != 0:
        if aln_ref[pos] != "-":
            i += step
        pos +=- step
        if pos < 0:
            return get_idx(idx, n+3, aln_ref, aln_query)
        if pos >= len(aln_ref):
            return get_idx(idx, n-3, aln_ref, aln_query)
    print(f'{n} steps from {idx} -> {pos}')
    return pos


def get_protein_variants(variants, aln_ref, aln_query, cds_start):
    """
    Convert nucleotide variants to protein variants.
    Returns a list of tuples: (codon, aa_ref, aa_alt, type, description)
    """
    protein_variants = []
    pre=[]
    codons_set= set()  # set of codons that have variants
    for i in range(len(variants)):
        codons= variants[i][2]
        if i+1 < len(variants) and codons[1] >= variants[i+1][2][0]:
            pre.append(variants[i])
            continue
        var = resolve_variant(pre+[variants[i]], aln_ref, aln_query)
        pre = []
        inframe_start = var[2][0] * 3 + cds_start
        inframe_end = var[2][1] * 3 + 3 + cds_start 
        #print(f"{inframe_start} - {var[0][0]}, {var[0][1]} - {inframe_end}")
        start_n = inframe_start - var[0][0]
        end_n = inframe_end - var[0][1] 
        start_idx = get_idx(var[1][0],start_n, aln_ref, aln_query)
        end_idx = get_idx(var[1][1],end_n, aln_ref, aln_query)
        #print(f"start_idx={start_idx}, end_idx={end_idx}")
        r= "".join(aln_ref[i] for i in range(start_idx, end_idx) if aln_ref[i] != "-")
        q= "".join(aln_query[i] for i in range(start_idx, end_idx) if aln_query[i] != "-")
        
        aa_r= get_aa(r)
        if len(q) % 3 != 0:
            protein_variants.append(f"p.{aa_r}{var[2][0]+1}fs")  # premature stop codon
            codons_set.add(var[2][0]+1)
            continue
        aa_q= get_aa(q)
        if aa_r == aa_q:
            #protein_variants.append('synonymous')
            continue
            
        elif aa_r and aa_q:
            if len(aa_r) == len(aa_q) == 1:
                #substitution
                protein_variants.append(f'p.{aa_r}{var[2][0]+1}{aa_q}')
            else:
                #delins
                if var[2][0]== var[2][1]:
                    protein_variants.append(f'p.{aa_r}{var[2][0]+1}delins{aa_q}')
                else:
                    protein_variants.append(f'p.{aa_r[0]}{var[2][0]+1}_{aa_r[-1]}{var[2][1]+1}delins{aa_q}')
        elif aa_r:
            #deletion
            if var[2][0]== var[2][1]:
                protein_variants.append(f'p.{aa_r}{var[2][0]+1}del')
            else:
                protein_variants.append(f'p.{aa_r[0]}{var[2][0]+1}_{aa_r[-1]}{var[2][1]+1}del')
        elif aa_q:
            #insertion
            protein_variants.append(f'p.{var[2][0]+1}ins{aa_q}')
        codons_set.add(var[2][0]+1)

    return protein_variants

def get_variants(alignment, name):
    cds_start= EXAMPLES[name].get("cds_start", 0)

    aln_ref, aln_query, start_gaps, end_gaps = _format_alignment(alignment)
    # Variant calling within the core region only
    ref_idx=start_gaps
    variants = []  # list of variant tuples: (start, end, type, seq)
    current_var=[]
    for i, (q_nt, r_nt) in enumerate(zip(aln_query, aln_ref)):
        if r_nt != "-":
            ref_idx += 1
        if q_nt == r_nt:
            if current_var:
                variants.append(resolve_variant(current_var, aln_ref, aln_query))
                current_var = []
            continue
        codon= (ref_idx - cds_start) // 3
        if q_nt != "-" and r_nt != "-":
            current_var.append(
                ((ref_idx, ref_idx), (i, i),(codon,codon), "sub", f"{r_nt}>{q_nt}")
            )  # substitution
        elif q_nt == "-":
            current_var.append(
                ((ref_idx, ref_idx), (i, i), (codon, codon), "del", r_nt)
            )  # deletion vs ref
        elif r_nt == "-":
            current_var.append(
                ((ref_idx, ref_idx), (i, i), (codon, codon), "ins", q_nt)
            )  # insertion vs ref
    if current_var:
        variants.append(resolve_variant(current_var))
    print('\n'.join(f"Variant: {v}" for v in variants))

    return variants, get_protein_variants(variants, aln_ref, aln_query, cds_start=cds_start)

def format_nt_variant(var):
    '''format a variant tuple into a HGVS string representation'''
    pos, vartype, bases= var[0][0], var[3], var[4]
    if vartype == "sub":
        vartype = ""
    elif vartype == "ins":
        pos = f'{pos}_{pos+1}'
    else:
        if var[0][0] != var[0][1]:
            pos = f'{var[0][0]}_{var[0][1]}'
        if vartype == "del":
            bases = ""
    return f'r.{pos}{vartype}{bases}'

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

def _format_alignment(aln): 
    ref = aln[1]
    query = aln[0]
    start_gaps= query.find(next(ch for ch in query if ch != '-'))
    end_gaps = len(query)-query.rfind(next(ch for ch in query[::-1] if ch != '-')) - 1
    ref=ref[start_gaps:-end_gaps]
    query=query[start_gaps:-end_gaps]
    return ref, query, start_gaps, end_gaps

def format_alignment(aln,  seq=''):
    """
    Format the alignment for display.
    Returns a tuple of (reference, match line, query).
    """
    ref, query, start_gaps, end_gaps = _format_alignment(aln)
    offset_ref = f'{seq} {start_gaps+1}'
    #offset_query = str(aln.aligned[0][0][0])
    offset_query = "read"
    space = max(len(offset_ref), len(offset_query))
    offset_ref = offset_ref.rjust(space)  # right-align offset
    offset_query = offset_query.rjust(space)  # right-align offset
    match_line = (" " * (space + 2)) + get_match_line(ref, query)
    return (f'{offset_ref}: {ref}', match_line, f'{offset_query}: {query}', start_gaps, end_gaps)


def query_sequence(seq):
    name, aln = find_best_match(seq, percent_identity=0.5)
    if name != "general":
        domains = EXAMPLES[name].get("features", {})
        gene = EXAMPLES[name].get("gene", "unknown")
        cds_start= EXAMPLES[name].get("cds_start", 0)
        example = EXAMPLES[name]["example"]
        json_data = make_blast_mock_single_hit(
            alignment=aln,
            gene=gene
        )
        aln_infos = json_data["BlastOutput2"][0]["report"]["results"]["search"]["hits"][0]["hsps"][0]
        aln_start_codon= (aln_infos["aln_start"]- cds_start)//3
        aln_end_codon= (aln_infos["aln_start"]- cds_start + aln_infos["align_len"] -1)//3
        domains_hit = {k:v for k,v in domains.items() if overlap((v["start_codon"], v["end_codon"]), (aln_start_codon, aln_end_codon))}
        var, protein_var=get_variants(aln, name)
        return example, gene, [format_nt_variant(v) for v in var], protein_var, domains_hit, json_data
    return "general", "unknown", [], [], {}, {}

def overlap(interval1, interval2):
    return interval1[0] <= interval2[1] and interval2[0] <= interval1[1]

if __name__ == "__main__":
    # Example usage
    seqL = [
        "GGTCAACGAGCAAGAATTTCTTTAGCAAGAGCA",
        "GATCAATGAGCAAGAATTTCTTTAGCAAGAGCA",
    
        "CTGGGCTCCGGTGCGTTCGGCACGGTG",
        "CTGAGCTCCGGTGCGTTCGGCACGGTG",
        "CCCGTCGCTATCAAGGAATTAAGAGAAGCAACATCTCCGAAAGCCAAC",
        "CCCGTCGCTATCAAGACATCTCCGAAAGCCAAC",

        "GCCGGTAGCACACCTTGTAATGGTGTTGAAGGT",
        "GCCGGTGGCACACCTTGTAATGGTGTTGAAGGT",
        "GCCGGTAACACACCTTGTAATGGTGTTGAAGGT",
        "GCCGGTAGCACACCTTGTAATGGTGTTCAAGGT",

        "CACGTGAAGGCGGCGCGCGCCCGGGACC",
        "CACTTGAAGGCGGCGCGCGCCCGGGACC",

        "GTCCAGAGATACATTGACCTTCTCCCCA",
        "GTCCAGAGATACCTTGAGCTTCTCCCCA",
        ]

    for seq in seqL:

        # name, aln = find_best_match(seq, percent_identity=0.5)
        # gene= EXAMPLES.get(name, {}).get("gene", "unknown")

        name, gene, var, protein_var, domains, json_data = query_sequence(seq)
        print(f"===================\nBest match: {name}")
        if name != "general":
            # var, (protein_var, domains)=get_variants(aln, name)
            aln = json_data["BlastOutput2"][0]["report"]["results"]["search"]["hits"][0]["hsps"][0]
            print(f'seq={seq}'),
            print((f'matched_example={name}')),
            print(f'variants={", ".join(var)}')
            print(f'protein variants={", ".join(protein_var)}'),
            print(f'domains={domains}')
            print('aln=\n'+'\n'.join([aln['qseq'], aln['midline'], aln['hseq']])),

        #print(f'aa_seq_q={aa_seq_q}'),
        #print(f'aa_seq_r={aa_seq_r}'),
        #print(f'aa_offset={aa_offset}'),
        

