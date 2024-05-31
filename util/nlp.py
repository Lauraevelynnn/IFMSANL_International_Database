from transformers import pipeline

def deadline(email_body, deadline_purpose, deadline_model, deadline_question):
    qa_pipeline = pipeline(deadline_purpose, model=deadline_model)
    result = qa_pipeline(question=deadline_question, context=email_body)
    print('NLP deadline: ' + result['answer'])
    return (result['answer'])

def summarize_email(email_body, summarization_purpose, summarization_model):
    summarizer = pipeline(summarization_purpose, model=summarization_model)
    summary = summarizer(email_body, max_length=100, min_length=10, truncation=True)[0]['summary_text']
    return summary.replace("_", "").replace(" .", ".").strip()