import subprocess
from pathlib import Path

BTOR2KW_BINARY = Path(__file__).parent.resolve() / "btor2kwcount/build/bin/kwcount"

KEYWORDS = [
    "add",
    "and",
    "bad",
    "constraint",
    "concat",
    "const",
    "constd",
    "consth",
    "dec",
    "eq",
    "fair",
    "iff",
    "implies",
    "iff",
    "inc",
    "init",
    "input",
    "ite",
    "justice",
    "mul",
    "nand",
    "neq",
    "neg",
    "next",
    "nor",
    "not",
    "one",
    "ones",
    "or",
    "output",
    "read",
    "redand",
    "redor",
    "redxor",
    "rol",
    "ror",
    "saddo",
    "sext",
    "sgt",
    "sgte",
    "sdiv",
    "sdivo",
    "slice",
    "sll",
    "slt",
    "slte",
    "sort",
    "smod",
    "smulo",
    "ssubo",
    "sra",
    "srl",
    "srem",
    "state",
    "sub",
    "uaddo",
    "udiv",
    "uext",
    "ugt",
    "ugte",
    "ult",
    "ulte",
    "umulo",
    "urem",
    "usubo",
    "write",
    "xnor",
    "xor",
    "zero",
]

def parse_kwcount(benchmark_path: str) -> list[int]:
    """
    Parse results from kwcount_binary for a btor2 benchmark (in btor2)
    """
    benchmark_path = Path(benchmark_path)
    if not benchmark_path.is_file():
        raise ValueError(f"The provided benchmark does not exist: {benchmark_path}")
    # check whether kwcount_binary exists
    if not Path(BTOR2KW_BINARY).is_file():
        raise ValueError("The btor2kwcount binary does not exist. Please build it first.")
    btor2kw_output = subprocess.run([BTOR2KW_BINARY, benchmark_path], capture_output=True, text=True)
    if btor2kw_output.returncode != 0:
        raise ValueError(f"Error processing {benchmark_path}: {btor2kw_output.stderr}")
    outputlines = btor2kw_output.stdout.splitlines()
    assert len(outputlines) == 2, f"Unexpected output from {benchmark_path}: {outputlines}"
    # kwcount output is in the format: kw0count kw1count ... kwNcount
    kw_counts = outputlines[0].split()
    kw_counts = [int(count) for count in kw_counts]
    # make sure the number of keywords is correct
    if len(kw_counts) != len(KEYWORDS):
        raise ValueError(f"Unexpected number {len(kw_counts)} of keywords in {benchmark_path} embedding")
    bit_counts = outputlines[1].split()
    bit_counts = [int(count) for count in bit_counts]
    return kw_counts, bit_counts

def get_kwcounts(benchmark_path: str) -> list[int]:
    """
    Get the keyword counts for a btor2 benchmark (in btor2)
    """
    kw_counts, _ = parse_kwcount(benchmark_path)
    return kw_counts