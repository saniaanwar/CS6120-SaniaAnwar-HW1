# Sania Anwar - Natural Langauge Processing
# CS6120 - Homework 1


# Question 1 - Parsing FASTA with Regex

# seq5 is lowercase --> uppercase
# new entries start with >

import re
import sys

valid_letters = re.compile(r"[ACGTURYN]+")

def open_fasta(filepath):
    records = []
    header = None
    current_record = []

    with open(filepath) as f:
        for sequence in f:
            sequence = sequence.strip()
            if not sequence:
                continue #skip any blank spaces
            if sequence.startswith(">"):
                if header is not None:
                    records.append((header, "".join(current_record)))
                header = sequence
                current_record = []
            else:
                current_record.append(sequence)

    # to save the last record 
    if header is not None:
        records.append((header, "".join(current_record)))

    return records

def classify_sequence(seq):
    seq = seq.upper()
    if not valid_letters.fullmatch(seq):
        return "Invalid"

    has_t = "T" in seq
    has_u = "U" in seq

    # DNA uses T but no U (can have ambiguous like N, R, etc)
    # RNA uses U but no T (can have ambigous)
    # If a sequence has both T and U then it's invalid

    if has_t and not has_u:
        return "DNA"
    if has_u and not has_t:
        return "RNA"
    return "Invalid"

# Question 2 - Locating Start/Stop Codons and Open Reading Frames

def locate_open_reading_frame(seq, seq_type):
    seq = seq.upper()

    if seq_type == "DNA":
        start_codon = "ATG"
        stop_codon = ("TAA", "TAG", "TGA")
    else:
        start_codon = "AUG"
        stop_codon = ("UAA", "UAG", "UGA")

    open_reading_frame = []

    # codons start at indices 0, 3, 6 etc
    for i in range(0, len(seq) - 2, 3):
        if seq[i:i+3] != start_codon:
            continue

        # iterating in steps of 3 while looking for a stop codon
        # codons with ambiguous letters don;t equal a start/stop (non-matching)
        for j in range(i+3, len(seq)-2,3):
            if seq[j:j+3] in stop_codon:
                open_reading_frame.append((i, j, seq[i:j + 3]))
                break

    return open_reading_frame


# Question 3 - Nucleotide Frequencies & Summary Report

def counts_nucleotides(seq, seq_type):
    seq = seq.upper()
    unique = "T" if seq_type == "DNA" else "U"

    a = seq.count("A")
    c = seq.count("C")
    g = seq.count("G")
    t_or_u = seq.count(unique)

    # all letters after A, C, G, and T/U are ambiguous
    ambiguous = len(seq) - (a + c + g + t_or_u)

    return a, c, g, t_or_u, ambiguous

def mean_length_validSeq(lengths):
    if len(lengths) == 0:
        return 0
    return sum(lengths) / len(lengths)


def main():
    filepath = sys.argv[1] if len(sys.argv) > 1 else "test_files/test_part1_in.fasta"

    dna_length = []
    rna_length = []
    invalid_counts = 0

    for header, seq in open_fasta(filepath):
        seq = seq.upper()
        seq_type = classify_sequence(seq)

        print(header)
        print(seq)
        print("Type: ",seq_type)

        if seq_type == "DNA":
            dna_length.append(len(seq))
        elif seq_type == "RNA":
            rna_length.append(len(seq))
        else:
            invalid_counts += 1

        if seq_type != "Invalid":

            a, c, g, t_or_u, ambigious = counts_nucleotides(seq, seq_type)
            unique = "T" if seq_type == "DNA" else "U"
            open_reading_frame = locate_open_reading_frame(seq, seq_type)

            print("Length: ", len(seq))
            print(f"Counts: A = {a}, C = {c}, G = {g}, {unique} = {t_or_u}, ambiguous = {ambigious}")
            print("Number of ORFs: ", len(open_reading_frame))
            for start, stop, orf in open_reading_frame:
                print("--> Starts at: ,", start, "Stops at: ,", stop, "Open Reading Frame: ", orf)
        print()
        print()

    # final summary is after all the records are read and classified

    print("--SUMMARY--")
    print("Valid DNA sequences: ", len(dna_length))
    print("Mean DNA length: ", round(mean_length_validSeq(dna_length), 2))
    print("Valid RNA sequences: ", len(rna_length))
    print("Mean RNA length: ", round(mean_length_validSeq(rna_length), 2))
    print("Invalid Sequences: ", invalid_counts)

if __name__ == "__main__":
    main()

