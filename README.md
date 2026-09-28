# CS6120 HW1 - Advanced DNA/RNA Parser

## How to run the code:

python3 advanced_dna_rna_parser.py <path_to_fasta_file>

*Examples:*

`python3 advanced_dna_rna_parser.py test_files/test_part1_in.fasta`

`python3 advanced_dna_rna_parser.py test_files/test_part2_in.fasta`

`python3 advanced_dna_rna_parser.py test_files/test_part3_in.fasta`

If there's no filepath given then it defaults to test_files/test_part1_in.fasta

## Assumptions I made:

- Lowercase input is accepted. Before any classification, counting and codon matching, the lowercase sequences are converted into uppercase.

**For classification:**

- A sequence is DNA if it has a T and no U.
- A sequence is RNA if it has a U and no T.
- A sequence is Invalid if it contains both T and U, neither of them, or any character other than A, C, G, T, U, and the ambiguous letters N, R, Y.
- I used only N, R, and Y as valid ambiguous nucleotides.


**ORF / codon logic:**

- A codon with an ambiguous letter (ATN) won't match a
  literal start or stop codon string, so it gets treated as non-matching.

- For each start codon found in-frame, the search moves forward in steps of 3.

## Regex Usage

- I used `[ACGTURYN]+` with `fullmatch()` to validate that the sequences contains the allowed characters based off the test files.
- I used `startswith(">")` to detect the header files.
- For part 2's start/stop codon matching, I used direct string slicing and equality checks (`seq[i:i+3] == start_codon`) instead of regex, since codons are fixed-length substrings.

## Files
- `advanced_dna_rna_parser.py` - main script
- `test_files/` - the 3 test FASTA files
- `output_part1.txt`, `output_part2.txt`, `output_part3.txt` - sample output files