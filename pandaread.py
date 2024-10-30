import pandas as pd

# Function to read the file and process lines
file_path = r'C:\Users\44779\OneDrive\Desktop\biblical hebrew\Tanach.txt\TextFiles\Genesis.txt'


# r'C:\Users\44779\OneDrive\Desktop\biblical hebrew\Tanach.txt\TextFiles\Amos.txt'
def read_hebrew_bible(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    data = []
    chapter = None

    for line in lines:
        line = line.strip()
        if line and not any(char.isdigit() for char in line):  # Non-Hebrew lines
            continue
        if line.startswith('1:'):  # New chapter
            chapter = line
        else:
            data.append({'Chapter': chapter, 'Verse': line})

    return pd.DataFrame(data)


# Function to extract words from verses
def extract_words(df):
    words = []
    for verse in df['Verse']:
        words.extend(verse.split())  # Split verse into words
    return pd.DataFrame(words, columns=['Word'])


# Read and process the file
df_verses = read_hebrew_bible(file_path)

# Extract words and save to a new DataFrame
df_words = extract_words(df_verses)

# Display the DataFrame with words
print(df_words)

# Save the DataFrame to a CSV file (optional)
df_words.to_csv('Genesis_hebwor.csv', index=False)
