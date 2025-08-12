from Bio import Align
from Bio.Seq import Seq
import json

# Load the examples JSON
with open("sequence_examples.json") as f:
    EXAMPLES = json.load(f)


def _normalize_nt(s: str) -> str:
    return ''.join(s.split()).upper().replace('U', 'T')

def _gapped_core_from_blocks(query: str, ref: str, alignment):
    """
    Build CORE gapped strings from alignment.aligned blocks.
    - Uses only the aligned region (no leading/trailing soft-clips).
    - Preserves internal indels as '-' on the opposite strand.
    """
    q_blocks = alignment.aligned[0]  # list of [start, end] rows for query
    r_blocks = alignment.aligned[1]  # list of [start, end] rows for ref
    if len(q_blocks) == 0:
        return "", ""

    q_out, r_out = [], []

    # Start with the first aligned block
    q0s, q0e = q_blocks[0]
    r0s, r0e = r_blocks[0]
    q_out.append(query[q0s:q0e])
    r_out.append(ref[r0s:r0e])

    # Handle internal gaps between consecutive blocks
    for i in range(len(q_blocks) - 1):
        q_cur_s, q_cur_e = q_blocks[i]
        r_cur_s, r_cur_e = r_blocks[i]
        q_next_s, q_next_e = q_blocks[i + 1]
        r_next_s, r_next_e = r_blocks[i + 1]

        q_gap = q_next_s - q_cur_e  # insertion in query relative to ref
        r_gap = r_next_s - r_cur_e  # deletion in query (insertion in ref)

        if q_gap > 0 and r_gap == 0:
            # Query has extra bases; ref has a gap
            q_out.append(query[q_cur_e:q_next_s])
            r_out.append("-" * q_gap)
        elif r_gap > 0 and q_gap == 0:
            # Ref has extra bases; query has a gap
            q_out.append("-" * r_gap)
            r_out.append(ref[r_cur_e:r_next_s])
        elif q_gap == 0 and r_gap == 0:
            # Directly adjacent blocks (rare but possible)
            pass
        else:
            # Both advanced -> unexpected for contiguous block model; be safe:
            # align the shorter chunk and gap the remainder
            k = min(q_gap, r_gap)
            if k > 0:
                q_out.append(query[q_cur_e:q_cur_e+k])
                r_out.append(ref[r_cur_e:r_cur_e+k])
            if q_gap > k:
                q_out.append(query[q_cur_e+k:q_next_s])
                r_out.append("-" * (q_gap - k))
            if r_gap > k:
                q_out.append("-" * (r_gap - k))
                r_out.append(ref[r_cur_e+k:r_next_s])

        # Append the next aligned block
        q_out.append(query[q_next_s:q_next_e])
        r_out.append(ref[r_next_s:r_next_e])

    return "".join(q_out), "".join(r_out)

def check_sequence(seq: str, percent_identity=0.7):
    """
    Align 'seq' to known examples (local alignment).
    Returns:
      - best example name (or 'general')
      - list of nt variants (within core alignment only)
      - AA sequence from aligned query (trimmed to full codons)
      - aligned query string (gapped, core only)
      - aligned reference string (gapped, core only)
    """
    seq = _normalize_nt(seq)
    min_score = len(seq) * percent_identity  # minimum score for a decent alignment
    aligner = Align.PairwiseAligner()
    aligner.mode = "local"
    aligner.match_score = 1
    aligner.mismatch_score = -1
    aligner.open_gap_score = -5
    aligner.extend_gap_score = -2

    best_name, best_alignment, best_ref = "general", None, None
    for name, data in EXAMPLES.items():
        ref = _normalize_nt(data["sequence"])
        offset = data["codon_offset"]
        alns = aligner.align(seq, ref)
        if alns[0].score< min_score:
            continue
        if alns and (best_alignment is None or alns[0].score > best_alignment.score):
            best_name, best_alignment, best_ref = name, alns[0], ref

    if best_alignment is None:
        # No decent local alignment; return general + whole-seq translation
        return "general", [],None, None, None, None

    # Build core gapped strings (no soft-clipped ends)
    aln_query, aln_ref = _gapped_core_from_blocks(seq, best_ref, best_alignment)

    # Variant calling within the core region only
    variants = []
    ref_nt_idx = offset*3  # 1-based position within the *reference core alignment*
    for q_nt, r_nt in zip(aln_query, aln_ref):
        if r_nt != "-":
            ref_nt_idx += 1
        if q_nt == r_nt:
            continue
        if q_nt != "-" and r_nt != "-":
            variants.append(f"c.{r_nt}{ref_nt_idx}{q_nt}")          # substitution
        elif q_nt == "-" and r_nt != "-":
            variants.append(f"c.del{r_nt}{ref_nt_idx}")             # deletion vs ref
        elif q_nt != "-" and r_nt == "-":
            variants.append(f"c.ins{q_nt}{ref_nt_idx}")       # insertion vs ref

    # Translate aligned query region (strip gaps; keep whole codons)
    q_nogap = aln_query.replace("-", "")
    #reference sequence is always in frame, we can check the query offset
    ref_start_nt = best_alignment.aligned[1][0][0]  # 0-based index into reference
    print(ref_start_nt)
    shift = ref_start_nt % 3
    if shift:
        q_nogap = q_nogap[3-shift:]  # remove leading soft-clips
    print(q_nogap)

    if len(q_nogap) % 3:
        q_nogap = q_nogap[:len(q_nogap) - (len(q_nogap) % 3)]
    aa_seq = str(Seq(q_nogap).translate())

    return best_name, variants, aa_seq, aln_query, aln_ref, best_alignment

if __name__ == "__main__":
    # Example usage
    seq = "TGGGCTCCGGTGCGTTCGGCACGGTGTATAAGGGACTCTTGATCCCAGAAGGTGAGAAAGTTAAAATTCCCGTCGCTATCAAGGAATTAAGAGAAGCAACA"
    name, variants, aa_seq, aligned_seq, aligned_ref, best_alignment = check_sequence(seq)
    print(f"Best match: {name}")
    if name != "general":
        print(f"Variants: {variants}")
        print(f"Amino acid sequence: {aa_seq}")
        print(f"Aligned sequence: {aligned_seq}")
        print(f"Aligned reference: {aligned_ref}")
        print(f"Best alignment: \n{best_alignment}")
        print(f"Alignment score: {best_alignment.score}")