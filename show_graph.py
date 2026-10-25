
from pathlib import Path

from app.agent.graph import analyst_graph

# Generate the graph image.
image_data = analyst_graph.get_graph().draw_png()

# Save the image in the project folder.
output_path = Path("langgraph_flow.png")
output_path.write_bytes(image_data)

print(f"Flowchart saved to: {output_path.resolve()}")
