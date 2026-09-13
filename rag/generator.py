import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def build_prompt(question, retrieved_documents):
    context = "\n\n".join(
        result["document"]
        for result in retrieved_documents
    )

    prompt = f"""
You are a UofT Computer Science academic planning assistant.

Use the academic information in the context to help the student
understand UofT Computer Science courses and plan their studies.

RULES:
1. Use only information provided in the context.
2. Never invent prerequisites, exclusions, requirements, or course details.
3. If the context does not contain enough information, clearly say so.
4. Distinguish facts from your recommendations.
5. When recommending courses, explain why they are relevant.
6. When discussing prerequisites, clearly identify the prerequisite
   courses found in the context.
7. If the student asks what they should take next, consider the
   prerequisites and the student's stated interests.
8. Mention the course codes you used as sources.
9. Do not claim that a course is required for a program unless the
   context explicitly says so.

ACADEMIC CONTEXT:
{context}

STUDENT QUESTION:
{question}

Give a clear, concise answer that would be useful to a UofT student.
"""

    return prompt


def generate_answer(question, retrieved_documents):

    prompt = build_prompt(
        question,
        retrieved_documents
    )

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content