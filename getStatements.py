import requests
from bs4 import BeautifulSoup
import re
# import the json file
import json

# load the json file
with open('all_words.json', 'r') as f:
    all_words = json.load(f)

# print the first 10 words



def get_statements(link):
    try:
        response = requests.get(link, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find all paragraphs
        all_ps = soup.find_all('p')
        for idx, p in enumerate(all_ps):
            # Normalize whitespace for searching
            if "last statement" in p.get_text(strip=True).lower():
                # Instead of just the next <p>, get everything from idx+1 to end of containing div
                # Find the div containing the "Last Statement" <p>
                parent_div = None
                current_tag = all_ps[idx]
                while current_tag and current_tag.name != "div":
                    current_tag = current_tag.parent
                parent_div = current_tag

                # If we found a parent div, gather everything after the "Last Statement" <p> to the end of the div
                if parent_div:
                    found = False
                    statement_html_segments = []
                    for tag in parent_div.find_all(['p', 'span', 'i', 'b', 'em'], recursive=True):
                        if not found and tag == all_ps[idx]:
                            found = True
                            continue
                        if found:
                            statement_html_segments.append(str(tag))
                    # Join all segments and strip all html tags
                    combined_html = "\n".join(statement_html_segments)
                    text_content = re.sub(r'<.*?>', '', combined_html)
                    # INSERT_YOUR_CODE
                    # Convert all double quotes to single quotes
                    text_content = text_content.replace('"', "'")
                    print("--------------------------------")
                    print(text_content)
                    print("--------------------------------")
                    return text_content
                else:
                    # fallback: just as before (next_p)
                    if idx + 1 < len(all_ps):
                        next_p = all_ps[idx + 1]
                        html_content = str(next_p)
                        html_content = re.sub(r'<.*?>', '', html_content)
                        print(html_content)
                        return html_content
        # If no "Last Statement" section found
        print("No statement found.")
        return ""
    except Exception as e:
        print(f"Error fetching statement: {e}")
        return ""

count = 0
for index, person in enumerate(all_words):
    print(person['firstName'], person['lastName'])
    # get the link
    link = person['link']
    all_words[index]['statement'] = get_statements(link)
    count += 1
    print(f"Processed {count} of {len(all_words)}")
# save the json file
with open('all_words_with_statements.json', 'w') as f:
    json.dump(all_words, f, indent=4)

# get_statements("https://www.tdcj.texas.gov/death_row/dr_info/ellisedwardlast.html")
# get_statements("https://www.tdcj.texas.gov/death_row/dr_info/noblesjonathanlast.html")