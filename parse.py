import re
import requests
from collections import Counter
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_path):
    text = ''
    with open(pdf_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def extract_keywords(text):
    words = re.findall(r'\b\w+\b', text.lower())
    keyword_counter = Counter(words)
    top_keywords = keyword_counter.most_common(10)
    return [keyword[0] for keyword in top_keywords]

def fetch_text_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Find the <div> element with the specified class and id
    job_post_div = soup.find('div', class_='jobs-box__html-content jobs-description-content__text t-14 t-normal jobs-description-content__text--stretch', id='job-details')
    if job_post_div:
        # Extract text from the div
        job_post_text = job_post_div.get_text(separator='\n')
        return job_post_text
    else:
        print("Job post details not found on the webpage.")
        return None
    return job_post_text

def match_keywords_with_job_post(keywords, job_post):
    matched_keywords = [keyword for keyword in keywords if keyword in job_post.lower()]
    return matched_keywords

if __name__ == "__main__":
    resume_path = 'resume.pdf'
    job_post_url = 'https://www.linkedin.com/jobs/view/3760325640'
    
    # Extract text from resume
    resume_text = extract_text_from_pdf(resume_path)
    resume_keywords = extract_keywords(resume_text)
    
    # Fetch job post text from URL
    job_post_text = fetch_text_from_url(job_post_url)
    
    # Match keywords with job post
    matched_keywords = match_keywords_with_job_post(resume_keywords, job_post_text)
    
    # Display results
    print("Resume Keywords:", resume_keywords)
    print("\nJob Post Text:")
    print(job_post_text)
    print("\nMatched Keywords with Job Post:", matched_keywords)
