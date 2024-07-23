import pandas as pd

# Path to the CSV file
file_path = 'CRC_Control113_PRJNA447983_metadata.txt'

# Read the CSV file
df = pd.read_csv(file_path)

# Convert the DataFrame to an HTML table
html_table = df.to_html(index=False)

# Save the HTML table to a file
with open('metagenome_metadata_csv.html', 'w') as f:
    f.write(html_table)

