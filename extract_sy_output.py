import os
import glob
import re

def main():
    # Find the most recently dated EnglishOysyesGalkhes_withSY*.txt
    files = glob.glob('EnglishOysyesGalkhes_withSY_*.txt')
    if not files:
        print("No files found.")
        return

    # Sort by modification time to get the latest
    latest_file = max(files, key=os.path.getmtime)

    # Extract timestamp from filename
    match = re.search(r'_withSY_(\d{8}_\d{6})\.txt', latest_file)
    timestamp = match.group(1) if match else "UNKNOWN"
    output_filename = f"SY_output_{timestamp}.txt"

    with open(latest_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split into paragraphs/blocks
    # Blocks are separated by a double newline followed by another block or end of file
    blocks = re.split(r'\n\n+', content.strip())

    extracted_blocks = []
    for block in blocks:
        lines = block.split('\n')
        
        # We expect 5 lines for regular paragraphs:
        # 0: English
        # 1: Oysyes (Yiddish)
        # 2: Sat (IPA) - Drop
        # 3: Sat (YCD) - Drop
        # 4: SY (Final) - Keep
        
        if len(lines) >= 5:
            # Reorder as English, Oysyes, Final SY per your request
            extracted = f"{lines[0]}\n{lines[1]}\n{lines[4]}"
            extracted_blocks.append(extracted)
        elif len(lines) >= 3:
            # Handle the title block or short blocks (English, Oysyes, SY)
            extracted_blocks.append('\n'.join(lines))
        elif block.strip():
            extracted_blocks.append(block.strip())

    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(extracted_blocks) + '\n')

    print(f"Processed {latest_file} -> {output_filename}")

if __name__ == "__main__":
    main()
