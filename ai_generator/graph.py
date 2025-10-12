from langchain_ollama import ChatOllama
from pydantic import BaseModel
from langchain_core.prompts import PromptTemplate
from django.contrib.auth.models import User
from typing import Optional, List, Dict
from langgraph.graph import StateGraph, END
from lesson.models import Lesson
from quiz.models import Quiz

llm = ChatOllama(model="llama3")

class GeneratedQuestion(BaseModel):
    enonce: str
    explications: Optional[str] = ""
    choices: Dict[str, bool] 

class GeneratedQuiz(BaseModel):
    questions: List[GeneratedQuestion]

class GeneratorState(BaseModel):
    user_id: int = None
    lesson_id: int = None
    lesson: Lesson = None
    questions: List[GeneratedQuestion] = None
    reply: Optional[str] = ""

    class Config:
        arbitrary_types_allowed = True


def fetch_lesson(state: GeneratorState) -> GeneratorState: 
    try:       
        lesson = Lesson.objects.get(id=state.lesson_id)
        state.lesson = lesson
    except Lesson.DoesNotExist:
        raise ValueError(f"Lesson with id={state.lesson_id} does not exist")
    except Exception as ex:
        raise RuntimeError(f"Unexpected error while fetching the lesson") from ex
    
    return state

generate_quiz_prompt = PromptTemplate.from_template("""
You are a Quiz generator. Generate {amount} questions based on this lesson:

Lesson content:
{lesson}

Return a JSON array where each element is an object with the following fields:

- enonce: the text of the question
- explications: explanation of the answer (can be empty)
- choices: a dictionary of answer options, with True for the correct answer and False for incorrect ones

Return only the JSON array — no extra text, no markdown.
""")



def generate_quiz(state: GeneratorState) -> GeneratorState:
    structured_llm = llm.with_structured_output(GeneratedQuiz)
    chain = generate_quiz_prompt | structured_llm
    result: GeneratedQuiz = chain.invoke({
        "lesson": state.lesson.content,
        "amount": 10
    })

    list_questions = []
    for question in result.questions:
        list_questions.append(question)


    state.questions = list_questions

    return state


def respond_to_user(state: GeneratorState) -> GeneratorState: 
    reply = "Your Quiz has been created, you can now go through it and save it"
    state.reply = reply
    return state


graph = StateGraph(GeneratorState)

graph.add_node("fetch_lesson", fetch_lesson)
graph.add_node("generate_quiz", generate_quiz)
graph.add_node("response_to_user", respond_to_user)


graph.set_entry_point("fetch_lesson")
graph.add_edge("fetch_lesson" , "generate_quiz")
graph.add_edge("generate_quiz", "response_to_user")
graph.add_edge("response_to_user", END)

quiz_generator_graph = graph.compile()