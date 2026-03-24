"""
Chat Routes - AI chatbot endpoints
"""
from fastapi import APIRouter, HTTPException, status
from typing import List, Dict
import os
from openai import OpenAI

router = APIRouter()

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None
model = os.getenv("OPENAI_MODEL", "gpt-4")

# Conversation history storage (in production, use database)
conversation_history = {}

@router.post("/chat")
async def chat_with_advisor(user_id: str, message: str):
    """Chat with AI Financial Advisor"""
    
    try:
        if client is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="OPENAI_API_KEY is not configured. Set it in backend/.env.",
            )

        # Initialize conversation history for user if not exists
        if user_id not in conversation_history:
            conversation_history[user_id] = []
        
        # Add user message to history
        conversation_history[user_id].append({
            "role": "user",
            "content": message
        })
        
        # System prompt for financial advisor
        system_prompt = """You are FinGuru, an AI-powered personal finance mentor for Indians. 
        Your expertise includes:
        - Personal financial planning and budgeting
        - Investment strategies and SIP planning
        - Tax optimization and income tax planning
        - Retirement planning and FIRE goals
        - Insurance needs assessment
        - Debt management
        - Real estate investment guidance
        
        Always provide advice specific to Indian context:
        - Reference Indian investment vehicles (MFs, NPS, ULIP, Insurance, etc.)
        - Consider Indian tax laws and deductions (80C, 80D, etc.)
        - Mention relevant financial instruments available in India
        - Use Indian currency (₹) in examples
        - Consider India-specific life events and financial challenges
        
        Be conversational, encouraging, and practical. Avoid complex jargon unless necessary.
        Always ask clarifying questions to provide better recommendations."""
        
        # Get response from OpenAI
        response = client.chat.completions.create(
            model=model,
            system=system_prompt,
            messages=conversation_history[user_id],
            temperature=0.7,
            max_tokens=500
        )
        
        assistant_message = response.choices[0].message.content
        
        # Add assistant response to history
        conversation_history[user_id].append({
            "role": "assistant",
            "content": assistant_message
        })
        
        return {
            "status": "success",
            "user_id": user_id,
            "user_message": message,
            "assistant_response": assistant_message,
            "history_length": len(conversation_history[user_id])
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat: {str(e)}"
        )

@router.get("/chat-history/{user_id}")
async def get_chat_history(user_id: str):
    """Get chat history for a user"""
    
    if user_id not in conversation_history:
        return {"history": []}
    
    return {
        "user_id": user_id,
        "history": conversation_history[user_id]
    }

@router.delete("/chat-history/{user_id}")
async def clear_chat_history(user_id: str):
    """Clear chat history for a user"""
    
    if user_id in conversation_history:
        del conversation_history[user_id]
    
    return {"message": "Chat history cleared"}

@router.post("/quick-advice")
async def get_quick_advice(topic: str, context: Dict):
    """Get quick financial advice on a specific topic"""
    
    try:
        if client is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="OPENAI_API_KEY is not configured. Set it in backend/.env.",
            )

        prompt = f"""
        Topic: {topic}
        Context: {context}
        
        Provide quick, actionable financial advice in 2-3 sentences.
        Keep it simple and specific to Indian context.
        """
        
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=150
        )
        
        return {
            "status": "success",
            "topic": topic,
            "advice": response.choices[0].message.content
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting advice: {str(e)}"
        )

@router.post("/financial-question")
async def answer_financial_question(question: str):
    """Answer general financial questions"""
    
    try:
        if client is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="OPENAI_API_KEY is not configured. Set it in backend/.env.",
            )

        system_prompt = """You are a helpful financial advisor with expertise in Indian personal finance.
        Provide accurate, practical answers to financial questions.
        Always mention that this is general information and not personalized advice."""
        
        response = client.chat.completions.create(
            model=model,
            system=system_prompt,
            messages=[{"role": "user", "content": question}],
            temperature=0.7,
            max_tokens=300
        )
        
        return {
            "status": "success",
            "question": question,
            "answer": response.choices[0].message.content
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error answering question: {str(e)}"
        )
