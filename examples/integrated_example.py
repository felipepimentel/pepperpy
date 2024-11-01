"""Example of integrated Pepperpy usage."""
import asyncio
from pepperpy.core.context import ContextManager
from pepperpy.core.extension import ExtensionManager
from pepperpy.workflow.engine import Workflow
from pepperpy.pipeline.processor import Pipeline

async def demonstrate_integrated():
    # Criar contexto principal
    context_manager = ContextManager()
    root_context = context_manager.create_context()
    
    # Configurar extensões
    extension_manager = ExtensionManager(root_context)
    await extension_manager.initialize_all()
    
    # Criar workflow com contexto
    workflow = Workflow(
        "data_processing",
        context=root_context.create_child(workflow_type="data_processing")
    )
    
    # Adicionar tarefas ao workflow
    workflow.add_task(
        "fetch_data",
        lambda ctx: {"data": [1, 2, 3]},
        retry_count=3
    )
    
    workflow.add_task(
        "process_data",
        lambda ctx: [x * 2 for x in ctx["fetch_data"]["data"]],
        depends_on=["fetch_data"]
    )
    
    # Criar pipeline com contexto
    pipeline = Pipeline(
        "transform_data",
        context=root_context.create_child(pipeline_type="transform")
    )
    
    # Configurar estágios do pipeline
    pipeline.add_stage(
        "normalize",
        lambda x: [i/max(x) for i in x]
    )
    
    pipeline.add_stage(
        "format",
        lambda x: [{"value": i} for i in x]
    )
    
    # Executar workflow e pipeline
    workflow_result = await workflow.execute()
    pipeline_result = await pipeline.process(workflow_result["process_data"])
    
    print(f"Final result: {pipeline_result}")

if __name__ == "__main__":
    asyncio.run(demonstrate_integrated()) 