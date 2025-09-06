# src/latest_ai_development/main.py
from .crew import LatestAiDevelopmentCrew # Relative import within the package
import os

def run():
    print("## Welcome to the Content Generation Crew")
    print('-----------------------------------------')

    # Ensure the 'output' directory exists relative to the project root
    # For projects structured with CrewAI, the `crewai run` command
    # usually sets the working directory to the project root.
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    topic = input("Enter the topic for content generation: ")
    content_type = input("Enter the desired content type (e.g., blog_post, linkedin_post, facebook_post): ")

    # Create an instance of your CrewBase class
    crew_instance = LatestAiDevelopmentCrew()

    print(f"\n## Generating a {content_type} about: {topic}")
    print("---------------------------------------------------\n")

    # Kickoff the crew
    # This is the correct pattern for crewai_project with CrewBase
    try:
        # IMPORTANT: Call the .crew() method on the instance to get the Crew object,
        # then call kickoff() on that Crew object.
        result = crew_instance.crew().kickoff(inputs={
            'topic': topic,
            'content_type': content_type
        })

        print("\n\n########################")
        print("## Crew Execution Finished")
        print("########################\n")
        print(result)

        # You can also read the final output file
        final_output_file = os.path.join(output_dir, f'final_content_for_{content_type}.md')
        if os.path.exists(final_output_file):
            with open(final_output_file, 'r', encoding='utf-8') as f:
                final_content = f.read()
            print(f"\n--- Content saved to {final_output_file} ---\n")
            # print(final_content) # Uncomment to print the full file content to console
        else:
            print(f"\n--- Final output file not found: {final_output_file} ---")

    except Exception as e:
        print(f"An error occurred during crew execution: {e}")

# This __main__ block is what 'crewai run' (via uv/run_crew) will execute.
# It calls the `run()` function.
if __name__ == "__main__":
    run()