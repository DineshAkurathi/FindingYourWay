# FindingYourWay

## Introduction

Finding your way is a Python script that employs probabilistic tracking and pathfinding algorithms to locate a drone within a complex grid-based environment. This project aims to efficiently discover the drone's position while adapting to changing probabilities, making it suitable for scenarios where drones may be used in search and rescue missions or surveillance.

## Features

- **Grid-Based Environment:** The script initializes a grid representing the environment in which the drone is operating. It distinguishes between blocked and unblocked cells to define possible drone paths.

- **Random Drone Initialization:** A drone is randomly placed within the environment, considering unblocked cells as potential starting points. This mimics real-world scenarios where the drone's initial location is uncertain.

- **Probability Grid:** A probability grid is created, associating each grid cell with a probability value. This grid reflects the likelihood of the drone's presence in each cell and serves as the basis for decision-making.

- **A star Pathfinding:** The script employs the A* algorithm to find the most probable path to the drone. It calculates heuristic values based on the probability of the drone's presence in neighboring cells, aiming to minimize moves and optimize search.

- **Adaptive Search:** The code continuously updates its search strategy based on changing probabilities. When higher probabilities are detected, the system recalculates paths, allowing the drone to adapt to new information effectively.

- **Termination Criteria:** The script includes termination criteria based on a predefined probability threshold (e.g., 0.89). When this threshold is met, the system identifies the drone's location, counts the number of moves made, and flags the drone as found.

## Getting Started

1. **Environment Setup:** Ensure you have Python installed on your system.

2. **Clone the Repository:** Clone this repository to your local machine.

   ```
   git clone https://github.com/DineshAkurathi/finding_your_way.git
   ```

3. **Run the Script:** Execute the Python script to initiate the drone search within the predefined environment. The script will output information about the drone's location and the number of moves required to find it.

   ```
   python finding_your_way_final.py
   ```

## Contribution

Contributions to this project are welcome! Feel free to submit issues, suggest improvements, or create pull requests.


## Acknowledgments

- The script's pathfinding and search algorithms were inspired by A* algorithm principles and probabilistic tracking techniques.

- Special thanks to the open-source community for providing valuable resources and libraries for Python development.

## Contact

For questions or inquiries about this project, please contact the project maintainer:

- Name: Dinesh Akurathi
- Email: dinesh.akurathi9@gmail.com

Feel free to reach out with any feedback or inquiries.
