# A13-Q44

def burrows_wheeler_transform(text: str) -> str:
    # Generate all cyclic rotations of text
    rotations = [text[i:] + text[:i] for i in range(len(text))]

    # Sort rotations lexicographically
    rotations_sorted = sorted(rotations)

    # Last column gives the BWT
    last_column = ''.join(rotation[-1] for rotation in rotations_sorted)

    return last_column


if __name__ == "__main__":
    import sys

    # Read input (strip newline)
    text = sys.stdin.read().strip()

    # Compute BWT
    bwt = burrows_wheeler_transform(text)

    # Output
    print(bwt)
