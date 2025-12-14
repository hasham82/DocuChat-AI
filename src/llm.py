"""
LLM integration and prompt management for RAG chatbot - FREE VERSION with Ollama.
"""
import os
from typing import List, Dict, Any
from langchain.llms import Ollama
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.schema import HumanMessage, AIMessage, SystemMessage
import yaml


class LLMManager:
    """Manages LLM interactions using FREE Ollama."""
    
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize LLM manager with Ollama."""
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        # Initialize FREE Ollama LLM
        model_name = self.config['llm']['model']
        base_url = self.config['llm'].get('base_url', 'http://localhost:11434')
        
        print(f"Connecting to Ollama at {base_url}")
        print(f"Using model: {model_name}")
        
        try:
            self.llm = Ollama(
                model=model_name,
                base_url=base_url,
                temperature=self.config['llm']['temperature'],
            )
            
            # Test connection
            test_response = self.llm("Hi")
            print("✓ Successfully connected to Ollama!")
            
        except Exception as e:
            print(f"❌ Error connecting to Ollama: {str(e)}")
            print("\nMake sure Ollama is running:")
            print("1. Check if Ollama is installed: ollama --version")
            print(f"2. Pull the model: ollama pull {model_name}")
            print("3. Ollama should be running automatically (check system tray)")
            raise
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for RAG."""
        return """You are a helpful AI assistant that answers questions based on the provided context.

Instructions:
1. Answer the question using ONLY the information from the context below
2. If the context doesn't contain enough information, say "I don't have enough information in the provided documents to answer this question."
3. Be concise but comprehensive
4. Cite the source document when possible
5. If asked about something not in the context, politely decline and explain why

Context:
{context}

Remember: Only use information from the context above. Do not use your general knowledge."""
    
    def generate_answer(
        self, 
        question: str, 
        context: str,
        chat_history: List = None
    ) -> str:
        """Generate answer using RAG approach."""
        # Format the system prompt with context
        system_message = self._get_system_prompt().format(context=context)
        
        # Build the full prompt
        full_prompt = f"{system_message}\n\n"
        
        # Add chat history if provided
        if chat_history:
            full_prompt += "Previous conversation:\n"
            for msg in chat_history[-4:]:  # Last 4 messages
                if isinstance(msg, HumanMessage):
                    full_prompt += f"Human: {msg.content}\n"
                elif isinstance(msg, AIMessage):
                    full_prompt += f"Assistant: {msg.content}\n"
            full_prompt += "\n"
        
        # Add current question
        full_prompt += f"Human: {question}\n\nAssistant:"
        
        # Generate response
        try:
            response = self.llm(full_prompt)
            return response.strip()
        except Exception as e:
            return f"Error generating response: {str(e)}\n\nPlease make sure Ollama is running."
    
    def generate_answer_streaming(
        self,
        question: str,
        context: str,
        chat_history: List = None
    ):
        """Generate answer with streaming for real-time display."""
        # Format the system prompt with context
        system_message = self._get_system_prompt().format(context=context)
        
        # Build the full prompt
        full_prompt = f"{system_message}\n\n"
        
        if chat_history:
            full_prompt += "Previous conversation:\n"
            for msg in chat_history[-4:]:
                if isinstance(msg, HumanMessage):
                    full_prompt += f"Human: {msg.content}\n"
                elif isinstance(msg, AIMessage):
                    full_prompt += f"Assistant: {msg.content}\n"
            full_prompt += "\n"
        
        full_prompt += f"Human: {question}\n\nAssistant:"
        
        # Stream response (Ollama doesn't support streaming in LangChain the same way)
        # So we'll return the full response
        try:
            response = self.llm(full_prompt)
            # Simulate streaming by yielding chunks
            words = response.split()
            for i, word in enumerate(words):
                if i < len(words) - 1:
                    yield word + " "
                else:
                    yield word
        except Exception as e:
            yield f"Error: {str(e)}"
    
    def evaluate_answer_quality(
        self,
        question: str,
        answer: str,
        context: str
    ) -> Dict[str, Any]:
        """Evaluate if the answer is grounded in context."""
        eval_prompt = f"""Evaluate if the following answer is properly grounded in the provided context.

Question: {question}

Context: {context}

Answer: {answer}

Provide a brief evaluation:
1. Is the answer based on the context? (Yes/No)
2. Are there any hallucinations or unsupported claims? (Yes/No)
3. Brief explanation (1 sentence)

Format: 
Grounded: Yes/No
Hallucinations: Yes/No
Explanation: <your explanation>"""
        
        try:
            eval_response = self.llm(eval_prompt)
            return {
                "evaluation": eval_response,
                "question": question,
                "answer": answer
            }
        except Exception as e:
            return {
                "evaluation": f"Error: {str(e)}",
                "question": question,
                "answer": answer
            }
    
    def rephrase_question(self, question: str, chat_history: List) -> str:
        """Rephrase question considering chat history for better retrieval."""
        if not chat_history:
            return question
        
        history_text = ""
        for msg in chat_history[-4:]:
            if isinstance(msg, HumanMessage):
                history_text += f"Human: {msg.content}\n"
            elif isinstance(msg, AIMessage):
                history_text += f"Assistant: {msg.content}\n"
        
        rephrase_prompt = f"""Given the conversation history, rephrase the follow-up question to be a standalone question.

Chat History:
{history_text}

Follow-up Question: {question}

Rephrased Standalone Question:"""
        
        try:
            response = self.llm(rephrase_prompt)
            return response.strip()
        except Exception as e:
            print(f"Error rephrasing: {e}")
            return question


if __name__ == "__main__":
    # Test LLM
    print("Testing Ollama LLM connection...\n")
    
    try:
        llm_manager = LLMManager()
        
        # Sample context
        context = """
        Document 1: Python is a high-level programming language known for its simplicity.
        It was created by Guido van Rossum and first released in 1991.
        
        Document 2: Python supports multiple programming paradigms including procedural,
        object-oriented, and functional programming.
        """
        
        # Test answer generation
        question = "Who created Python?"
        print(f"Question: {question}")
        print("Generating answer...\n")
        
        answer = llm_manager.generate_answer(question, context)
        
        print(f"Answer: {answer}")
        
        print("\n" + "="*50)
        print("✓ LLM test successful!")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Install Ollama from https://ollama.ai")
        print("2. Run: ollama pull llama3.1")
        print("3. Make sure Ollama is running")