from typing import Dict, List, Any, Optional
from enum import Enum
from daily_planner import AntyAIPlanner
import asyncio
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TaskType(Enum):
    DAILY_PLANNER = "daily_planner"
    ACTIVITY_PLANNER = "activity_planner"
    RECOMMENDATIONS = "recommendations"
    ACTIVITY_DETAILS = "activity_details"
    # EVENT_SEARCH = "event_search"
    # WEATHER_CHECK = "weather_check"

class OrchestratorAgent:
    def __init__(self):
        """Initialize the orchestrator with specialized agents."""
        self.agents = {
            TaskType.DAILY_PLANNER: AntyAIPlanner(),
            TaskType.RECOMMENDATIONS: AntyAIPlanner(),  # Using AntyAIPlanner for recommendations
            # Add other agents as they are implemented
            # TaskType.EVENT_SEARCH: EventSearchAgent(),
            # TaskType.WEATHER_CHECK: WeatherAgent(),
        }
        
    async def delegate_task(self, task_type: TaskType, **kwargs) -> Dict[str, Any]:
        """
        Delegate a task to the appropriate agent and return the result.
        
        Args:
            task_type: The type of task to delegate
            **kwargs: Additional arguments needed for the specific task
            
        Returns:
            Dict containing the task results and metadata
        """
        try:
            if task_type not in self.agents:
                raise ValueError(f"No agent available for task type: {task_type}")
            
            agent = self.agents[task_type]
            logger.info(f"Delegating {task_type.value} task to {agent.__class__.__name__}")
            
            # Execute the appropriate method based on task type
            if task_type == TaskType.RECOMMENDATIONS:
                result = await agent.generate_recommendations(kwargs.get('user_preferences', {}))
            elif task_type == TaskType.ACTIVITY_DETAILS:
                result = await agent.get_activity_details(kwargs.get('activity_name', ''))
            else:
                raise NotImplementedError(f"Task type {task_type} not implemented yet")
            
            return {
                "status": "success",
                "task_type": task_type.value,
                "result": result,
                "metadata": {
                    "agent": agent.__class__.__name__,
                    "timestamp": asyncio.get_event_loop().time()
                }
            }
            
        except Exception as e:
            logger.error(f"Error in task delegation: {str(e)}")
            return {
                "status": "error",
                "task_type": task_type.value,
                "error": str(e),
                "metadata": {
                    "timestamp": asyncio.get_event_loop().time()
                }
            }
    
    async def process_complex_task(self, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Process multiple related tasks and combine their results.
        
        Args:
            tasks: List of task configurations, each containing:
                  - task_type: TaskType enum
                  - params: Dict of parameters for the task
                  
        Returns:
            Dict containing combined results and metadata
        """
        results = []
        for task in tasks:
            task_type = TaskType(task['task_type'])
            result = await self.delegate_task(task_type, **task.get('params', {}))
            results.append(result)
            
        return {
            "status": "success",
            "results": results,
            "metadata": {
                "total_tasks": len(tasks),
                "completed_tasks": len([r for r in results if r['status'] == 'success']),
                "timestamp": asyncio.get_event_loop().time()
            }
        }



# Example usage
async def main():
    orchestrator = OrchestratorAgent()
    
    # Example of delegating a single task
    user_preferences = {
        "schedule": {
            "workStartTime": "09:00",
            "workEndTime": "17:00",
            "breakTime": "12:00",
            "breakDuration": 30
        },
        "interests": ["culture", "food", "nature"],
        "preferredStartTime": "10:00",
        "preferredEndTime": "16:00",
        "pace": "moderate"
    }
    
    result = await orchestrator.delegate_task(
        TaskType.RECOMMENDATIONS,
        user_preferences=user_preferences
    )
    print("Single task result:", result['result'])

if __name__ == "__main__":
    asyncio.run(main())
