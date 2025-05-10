from typing import Dict, List, Any, Optional
from enum import Enum
from .daily_planner import AntyAIPlanner
from .activity_planner import AntyAIActivityPlanner
import asyncio
import logging
from datetime import datetime

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
            TaskType.DAILY_PLANNER: AntyAIPlanner(), # create a daily plan for the user based on their preferences
            TaskType.ACTIVITY_PLANNER: AntyAIActivityPlanner(), # create an activity plan for the user based daily plan
            # Add other agents as they are implemented
            # TaskType.EVENT_SEARCH: EventSearchAgent(),
            # TaskType.WEATHER_CHECK: WeatherAgent(),
        }
        
        self.current_step = self._determine_current_step()
        # Initialize completed activities tracking
        self.completed_activities = {
            0: [],  # Morning completed activities
            1: [],  # Afternoon completed activities
            2: []   # Evening completed activities
        }
        
    def _determine_current_step(self) -> int:
        """
        Determine the current step based on time of day:
        0: Morning (5:00 - 11:59)
        1: Afternoon (12:00 - 17:59)
        2: Evening (18:00 - 4:59)
        """
        current_hour = datetime.now().hour
        
        if 5 <= current_hour < 12:
            return 0  # Morning
        elif 12 <= current_hour < 18:
            return 1  # Afternoon
        else:
            return 2  # Evening
            
    def get_current_time_period(self) -> str:
        """Get the current time period as a string."""
        periods = ["Morning", "Afternoon", "Evening"]
        return periods[self.current_step]
        
    def mark_activity_completed(self, activity: str) -> None:
        """Mark an activity as completed for the current step."""
        if activity not in self.completed_activities[self.current_step]:
            self.completed_activities[self.current_step].append(activity)
            logger.info(f"Marked activity as completed for {self.get_current_time_period()}: {activity}")
            
    def get_completed_activities(self, step: Optional[int] = None) -> List[str]:
        """Get completed activities for a specific step or current step if none specified."""
        if step is None:
            step = self.current_step
        return self.completed_activities[step]
        
    def get_remaining_activities(self, daily_plan: Dict) -> List[str]:
        """Get remaining activities for the current step."""
        current_period = self.get_current_time_period()
        all_activities = daily_plan.get(current_period, [])
        completed = self.get_completed_activities()
        return [activity for activity in all_activities if activity not in completed]
        
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
            if task_type == TaskType.DAILY_PLANNER:
                result = await agent.generate_recommendations(kwargs.get('user_preferences', {}))
            elif task_type == TaskType.ACTIVITY_PLANNER:
                result = await agent.generate_recommendations(kwargs.get('activity_description', ''))
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
    
    # Get the current time period
    current_period = orchestrator.get_current_time_period()
    print(f"Current time period: {current_period}")
    
    daily_planner_result = await orchestrator.delegate_task(
        TaskType.DAILY_PLANNER,
        user_preferences=user_preferences
    )
    print("Daily planner result:", daily_planner_result['result'])

    # Get the activity for the current time period
    if isinstance(daily_planner_result['result'], str):
        daily_plan = eval(daily_planner_result['result'])
    else:
        daily_plan = daily_planner_result['result']
        
    # Get remaining activities for current period
    remaining_activities = orchestrator.get_remaining_activities(daily_plan)
    print(f"\nRemaining activities for {current_period}:")
    for i, activity in enumerate(remaining_activities, 1):
        print(f"{i}. {activity}")
    
    if remaining_activities:
        # Plan the first remaining activity
        activity_description = remaining_activities[0]
        activity_planner_result = await orchestrator.delegate_task(
            TaskType.ACTIVITY_PLANNER,
            activity_description=activity_description
        )
        print("\nActivity planner result:", activity_planner_result['result'])
        
        # Mark the activity as completed
        orchestrator.mark_activity_completed(activity_description)
        print(f"\nMarked '{activity_description}' as completed")
        
        # Show updated remaining activities
        updated_remaining = orchestrator.get_remaining_activities(daily_plan)
        print(f"\nUpdated remaining activities for {current_period}:")
        for i, activity in enumerate(updated_remaining, 1):
            print(f"{i}. {activity}")
    else:
        print(f"No remaining activities for {current_period}")

if __name__ == "__main__":
    asyncio.run(main())
