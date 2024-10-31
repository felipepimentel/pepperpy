from pepperpy.llm import get_llm
from pepperpy.llm.agents import Agent, MultiAgentSystem
from pepperpy.llm.templates import PromptTemplate, QuickCommand
from pepperpy.llm.metrics import Budget

def demonstrate_advanced_features():
    # Setup budget
    budget = Budget(max_cost=10.0, max_tokens=1000)
    
    # Setup LLMs with different configurations
    code_llm = get_llm("stackspot", budget=budget)
    review_llm = get_llm("openrouter", budget=budget)
    
    # Create templates
    code_template = PromptTemplate(
        template="Write a Python function to ${task}",
        input_variables=["task"]
    )
    
    review_template = PromptTemplate(
        template="Review this code:\n${code}\n\nProvide feedback on:",
        input_variables=["code"]
    )
    
    # Create agents
    coder = Agent(
        name="coder",
        description="Writes Python code",
        llm=code_llm,
        system_prompt="You are an expert Python programmer.",
        templates={"write_code": code_template}
    )
    
    reviewer = Agent(
        name="reviewer",
        description="Reviews code",
        llm=review_llm,
        system_prompt="You are a code review expert.",
        templates={"review": review_template}
    )
    
    # Setup multi-agent system
    mas = MultiAgentSystem()
    mas.register_agent(coder)
    mas.register_agent(reviewer)
    
    # Define workflow
    def process_code_output(response, current_input):
        return {"code": response.content}
    
    mas.register_workflow("code_review", [
        {
            "agent": "coder",
            "template": "write_code",
            "output_processor": process_code_output
        },
        {
            "agent": "reviewer",
            "template": "review"
        }
    ])
    
    # Execute workflow
    results = mas.execute_workflow("code_review", {
        "task": "calculate fibonacci sequence"
    })
    
    # Print results
    print("Code Generation:")
    print(results[0].content)
    print("\nCode Review:")
    print(results[1].content)
    
    # Print metrics
    print(f"\nTotal cost: ${code_llm.total_cost + review_llm.total_cost:.4f}")
    print(f"Total tokens: {code_llm.total_tokens + review_llm.total_tokens}")

if __name__ == "__main__":
    demonstrate_advanced_features() 