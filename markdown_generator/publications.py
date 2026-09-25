import os
import re
import unicodedata

import bibtexparser


BIB_FILE = "publications.bib"
OUTPUT_DIR = "../_publications"

MY_NAME = "Issam Chekakta"


# ============================================================
# Text cleaning
# ============================================================

def clean_latex(text):
    if not text:
        return ""

    text = str(text)

    text = re.sub(r"\\textbf\s*\{([^{}]*)\}", r"\1", text)
    text = re.sub(r"\\textit\s*\{([^{}]*)\}", r"\1", text)
    text = re.sub(r"\\emph\s*\{([^{}]*)\}", r"\1", text)
    text = re.sub(r"\\color\s*\{[^{}]*\}", "", text)

    replacements = {
        r"\'a": "á",
        r"\'e": "é",
        r"\'i": "í",
        r"\'o": "ó",
        r"\'u": "ú",
        r"\`a": "à",
        r"\`e": "è",
        r"\`i": "ì",
        r"\`o": "ò",
        r"\`u": "ù",
        r"\^a": "â",
        r"\^e": "ê",
        r"\^i": "î",
        r"\^o": "ô",
        r"\^u": "û",
        r'\"a': "ä",
        r'\"e': "ë",
        r'\"i': "ï",
        r'\"o': "ö",
        r'\"u': "ü",
        r"\~n": "ñ",
        r"\c{c}": "ç",
        r"\c c": "ç",
        r"{\'e}": "é",
        r"{\`e}": "è",
        r"{\^e}": "ê",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = text.replace("---", "—")
    text = text.replace("--", "–")
    text = text.replace(r"\&", "&")
    text = text.replace(r"\%", "%")
    text = text.replace(r"\_", "_")
    text = text.replace(r"\#", "#")

    text = text.replace("{", "").replace("}", "")
    text = re.sub(r"\s+", " ", text).strip()

    return text


def yaml_escape(text):
    return text.replace("'", "''")


# ============================================================
# Authors
# ============================================================

def format_author(author):
    author = clean_latex(author).strip()

    if "," in author:
        last, first = [x.strip() for x in author.split(",", 1)]
        return f"{first} {last}".strip()

    return author


def format_authors(author_field):
    authors = re.split(r"\s+and\s+", author_field)

    formatted = []

    for author in authors:
        name = format_author(author)

        if name.lower() == MY_NAME.lower():
            name = f"<strong>{name}</strong>"

        formatted.append(name)

    return ", ".join(formatted)


def format_authors_plain(author_field):
    authors = re.split(r"\s+and\s+", author_field)
    return ", ".join(format_author(author) for author in authors)


# ============================================================
# Publication type
# ============================================================

def get_publication_type(entry):

    entry_type = entry.get("ENTRYTYPE", "").lower()

    if entry_type == "article":
        return "journal"

    if entry_type == "inproceedings":
        return "conference"

    if entry_type == "phdthesis":
        return "thesis"

    return "other"

def get_status_label(entry):

    status = entry.get("status", "").lower().strip()

    if status == "accepted":
        return "Accepted"
    elif status == "preprint":
        return "Preprint"
    else:
        return ""
    
def get_publication_label(publication_type):

    labels = {
        "journal": "Journal Article",
        "conference": "Conference Paper",
        "thesis": "PhD Thesis",
        "preprint": "Preprint",
        "accepted": "Accepted",
        "other": "Publication",
    }

    return labels.get(publication_type, "Publication")


# ============================================================
# Venue
# ============================================================

def get_venue(entry):

    entry_type = entry.get("ENTRYTYPE", "").lower()

    if entry_type == "phdthesis":
        school = clean_latex(entry.get("school", ""))
        return f"PhD Thesis, {school}" if school else "PhD Thesis"

    if entry_type == "inproceedings":
        return clean_latex(entry.get("booktitle", ""))

    return clean_latex(entry.get("journal", ""))


# ============================================================
# URL slug
# ============================================================

def make_slug(title):

    title = clean_latex(title)

    normalized = unicodedata.normalize("NFKD", title)
    normalized = normalized.encode("ascii", "ignore").decode("ascii")

    slug = normalized.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = slug.strip("-")

    return slug


# ============================================================
# Citation
# ============================================================

def make_citation(entry):

    authors = format_authors_plain(entry.get("author", ""))
    year = entry.get("year", "")
    title = clean_latex(entry.get("title", ""))

    venue = get_venue(entry)

    if venue:
        return f'{authors} ({year}). "{title}." <i>{venue}</i>.'

    return f'{authors} ({year}). "{title}."'


# ============================================================
# Main
# ============================================================

def main():

    if not os.path.exists(BIB_FILE):
        raise FileNotFoundError(
            f"Could not find {BIB_FILE}. "
            "Run this script from the markdown_generator folder."
        )

    with open(BIB_FILE, encoding="utf-8") as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    generated = 0

    for entry in bib_database.entries:

        title = clean_latex(entry.get("title", "Untitled"))
        year = str(entry.get("year", "")).strip()

        if not year:
            print(f"Skipping entry without year: {entry.get('ID')}")
            continue

        pub_date = f"{year}-01-01"

        slug = make_slug(title)
        filename = f"{pub_date}-{slug}.md"
        filepath = os.path.join(OUTPUT_DIR, filename)

        venue = get_venue(entry)
        citation = make_citation(entry)

        authors = format_authors(entry.get("author", ""))

        publication_type = get_publication_type(entry)
        publication_label = get_publication_label(publication_type)
        status_label = get_status_label(entry)
        doi = entry.get("doi", "").strip()

        if doi:
            paper_url = f"https://doi.org/{doi}"
        else:
            paper_url = ""

        excerpt = f"{publication_label}."

        md = "---\n"
        md += f'title: "{title}"\n'
        md += "collection: publications\n"
        md += f"permalink: /publication/{pub_date}-{slug}\n"
        md += f"excerpt: '{yaml_escape(excerpt)}'\n"
        md += f"date: {pub_date}\n"
        md += f"venue: '{yaml_escape(venue)}'\n"
        md += f"publication_type: '{publication_type}'\n"
        md += f"publication_label: '{publication_label}'\n"
        md += f"authors: '{yaml_escape(authors)}'\n"
        md += f"citation: '{yaml_escape(citation)}'\n"
        md += f"status_label: '{status_label}'\n"
        if paper_url:
            md += f"paperurl: '{paper_url}'\n"

        md += "---\n\n"

        md += f"{authors}\n\n"

        if venue:
            md += f'<span class="publication-venue">{venue}</span>\n\n'

        if paper_url:
            md += f"[View publication]({paper_url})\n\n"

        md += f"**Authors:** {authors}\n"

        with open(filepath, "w", encoding="utf-8") as output_file:
            output_file.write(md)

        generated += 1
        print(f"Generated: {filename}")

    print()
    print(f"Done. Generated {generated} publication files.")


if __name__ == "__main__":
    main()


















# # coding: utf-8

# # # Publications markdown generator for academicpages
# # 
# # Takes a TSV of publications with metadata and converts them for use with [academicpages.github.io](academicpages.github.io). This is an interactive Jupyter notebook, with the core python code in publications.py. Run either from the `markdown_generator` folder after replacing `publications.tsv` with one that fits your format.
# # 
# # TODO: Make this work with BibTex and other databases of citations, rather than Stuart's non-standard TSV format and citation style.
# # 

# # ## Data format
# # 
# # The TSV needs to have the following columns: pub_date, title, venue, excerpt, citation, site_url, and paper_url, with a header at the top. 
# # 
# # - `excerpt` and `paper_url` can be blank, but the others must have values. 
# # - `pub_date` must be formatted as YYYY-MM-DD.
# # - `url_slug` will be the descriptive part of the .md file and the permalink URL for the page about the paper. The .md file will be `YYYY-MM-DD-[url_slug].md` and the permalink will be `https://[yourdomain]/publications/YYYY-MM-DD-[url_slug]`


# # ## Import pandas
# # 
# # We are using the very handy pandas library for dataframes.

# # In[2]:

# import pandas as pd


# # ## Import TSV
# # 
# # Pandas makes this easy with the read_csv function. We are using a TSV, so we specify the separator as a tab, or `\t`.
# # 
# # I found it important to put this data in a tab-separated values format, because there are a lot of commas in this kind of data and comma-separated values can get messed up. However, you can modify the import statement, as pandas also has read_excel(), read_json(), and others.

# # In[3]:

# publications = pd.read_csv("publications.tsv", sep="\t", header=0)
# publications


# # ## Escape special characters
# # 
# # YAML is very picky about how it takes a valid string, so we are replacing single and double quotes (and ampersands) with their HTML encoded equivilents. This makes them look not so readable in raw format, but they are parsed and rendered nicely.

# # In[4]:

# html_escape_table = {
#     "&": "&amp;",
#     '"': "&quot;",
#     "'": "&apos;"
#     }

# def html_escape(text):
#     """Produce entities within text."""
#     return "".join(html_escape_table.get(c,c) for c in text)


# # ## Creating the markdown files
# # 
# # This is where the heavy lifting is done. This loops through all the rows in the TSV dataframe, then starts to concatentate a big string (```md```) that contains the markdown for each type. It does the YAML metadata first, then does the description for the individual page. If you don't want something to appear (like the "Recommended citation")

# # In[5]:

# import os
# for row, item in publications.iterrows():
    
#     md_filename = str(item.pub_date) + "-" + item.url_slug + ".md"
#     html_filename = str(item.pub_date) + "-" + item.url_slug
#     year = item.pub_date[:4]
    
#     ## YAML variables
    
#     md = "---\ntitle: \""   + item.title + '"\n'
    
#     md += """collection: publications"""
    
#     md += """\npermalink: /publication/""" + html_filename
    
#     if len(str(item.excerpt)) > 5:
#         md += "\nexcerpt: '" + html_escape(item.excerpt) + "'"
    
#     md += "\ndate: " + str(item.pub_date) 
    
#     md += "\nvenue: '" + html_escape(item.venue) + "'"
    
#     if len(str(item.paper_url)) > 5:
#         md += "\npaperurl: '" + item.paper_url + "'"
    
#     md += "\ncitation: '" + html_escape(item.citation) + "'"
    
#     md += "\n---"
    
#     ## Markdown description for individual page
    
#     if len(str(item.paper_url)) > 5:
#         md += "\n\n<a href='" + item.paper_url + "'>Download paper here</a>\n" 
        
#     if len(str(item.excerpt)) > 5:
#         md += "\n" + html_escape(item.excerpt) + "\n"
        
#     md += "\nRecommended citation: " + item.citation
    
#     md_filename = os.path.basename(md_filename)
       
#     with open("../_publications/" + md_filename, 'w') as f:
#         f.write(md)


