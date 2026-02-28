<p align="center">
  <img src="./img.png" alt="Project Banner" width="100%">
</p>

# [BuildBack] 🎯

## Basic Details

### Team Name: [Nova]

### Team Members
- Member 1: [Nedhya Remesh] - [College of Engineering Thalassery]
- Member 2: [Surabhi Aneesh] - [College of Engineering Thalassery]

### Hosted Project Link
[https://buildback-nova.streamlit.app/]

### Project Description
[BuildBack is an interactive web application designed to help Computer Science students and developers instantly reverse-engineer codebases and documentation into presentation-ready architecture guides. It acts as an automated "study buddy" and mock examiner, transforming raw project files into comprehensive technical breakdowns and interactive Viva Voce (project defense) mock tests.]

### The Problem statement
[Students and developers waste hours manually decoding complex codebases, drawing architecture diagrams from scratch, and guessing what technical questions an examiner might ask during a project defense. The manual documentation process is overwhelming, slow, and stressful..]

### The Solution
[BuildBack completely automates the documentation and defense-prep workflow. By simply pasting a GitHub link or uploading a project file, our system instantly reverse-engineers the code to generate visual architecture diagrams, ready-to-read presentation scripts, and a context-aware, interactive mock Viva test. We turn hours of stressful manual preparation into a seamless, one-click process.]

---

## Technical Details

### Technologies/Components Used

**For Software:**
- Languages used: [Python]
- Frameworks used: [Streamlit]
- Libraries used: [google-generativeai,requests,pypdf,python-pptx,zipfile, os, tempfile, json, re]
- Tools used: [VS Code,Mermaid.js,GitHub REST API]

---

## Features

List the key features of your project:
- Feature 1: [Multi-Source Data Ingestion: Effortlessly import project context by pasting a public GitHub URL or uploading local codebase files and documentation (ZIP, PDF, PPTX).]
- Feature 2: [Automated Architecture Reverse-Engineering: Instantly generates a high-level system summary, an in-depth component breakdown, and visual flowcharts (via Mermaid.js) directly from the raw code]
- Feature 3: [Interactive Mock Defense (Viva Prep): Auto-generates a context-aware, 5-question Multiple Choice test with a gamified UI, progress tracking, and detailed explanations to simulate a technical evaluation.]
- Feature 4: [One-Click Export & Documentation: Download the fully generated architecture guide as a clean Markdown (.md) file, ready to be used as a project README or printed as a handout for evaluators.]

---

## Implementation

### For Software:

#### Installation
```bash
[Installation commands - e.g., npm install, pip install -r requirements.txt]
```

#### Run
```bash
[Run commands - e.g., npm start, python app.py]
```

---

## Project Documentation

### For Software:

#### Screenshots (Add at least 3)

![Screenshot1]
<img width="1916" height="882" alt="Screenshot 2026-02-28 110427" src="https://github.com/user-attachments/assets/befc2fcf-f282-4f7e-8d37-340b1d87ba76" />

Shows the main results dashboard after analysis, featuring the collapsible architecture guide, the report download button, and the start of the interactive mock test.

![Screenshot2]
<img width="1916" height="854" alt="Screenshot 2026-02-28 110437" src="https://github.com/user-attachments/assets/c453ef9c-84d6-4adf-837f-160b40598440" />

Illustrates the 3-tier system architecture diagram (Presentation, Application, and Data layers) of the Narrative Nexus project.

![Screenshot3]
<img width="1916" height="851" alt="Screenshot 2026-02-28 110444" src="https://github.com/user-attachments/assets/27838be9-30b7-4b90-a7e3-5ae0d57f9249" />

Displays the AI-generated system architecture diagram (written in Mermaid code) along with a step-by-step textual walkthrough of the data flow.
![Screenshot4]
<img width="1911" height="864" alt="Screenshot 2026-02-28 110459" src="https://github.com/user-attachments/assets/4468e584-d774-42cb-b0dc-163a29c69f1c" />
Shows the generated 60-second presentation pitch, the report download button, and the interactive defense preparation quiz interface.

#### Diagrams

**System Architecture:**

![Architecture Diagram]<img width="3544" height="5722" alt="Generative AI Pipeline for-2026-02-28-045501" src="https://github.com/user-attachments/assets/a32c0f88-b4a2-41ea-b91c-bc34df2d31fb" />

*Explain your system architecture - components, data flow, tech stack interaction*
Data Ingestion: The user interacts with the Streamlit Frontend. Depending on their input, the system either makes network calls to the GitHub API or uses local Python libraries (pypdf, zipfile) to parse uploaded files.

Noise Filtering: The system automatically strips out useless files (like node_modules or .git) to create a clean, token-efficient context block.

AI Orchestration: This clean context is sent to the AI Engine. We use dual-prompting here: one prompt strictly requests a Markdown architecture report, and the second prompt forces the AI to output a pure JSON array for the quiz.

Stateful Rendering: The generated Markdown is rendered into the dashboard (complete with visual diagrams), and the JSON array is parsed by Streamlit's session state to build the interactive, auto-graded mock test.

**Application Workflow:**

![Workflow]
<img width="4447" height="5939" alt="AI Orchestration for-2026-02-28-050137" src="https://github.com/user-attachments/assets/358d0003-f11b-417a-9d1e-4647d3bcedd3" />

*Add caption explaining your workflow*
Step 1: Context Aggregation
The user provides their project source (a GitHub repository link or a local ZIP/PDF/PPTX file). BuildBack instantly scans the files, identifies the core tech stack (e.g., React, Django), and extracts a truncated summary of the codebase.

Step 2: Reverse-Engineering & Diagramming
The extracted data is processed by the AI engine, which generates a high-level executive summary, a detailed component-by-component breakdown, and a visual flowchart mapping out how data moves through the user's system.

Step 3: The "Pitch" Generation
BuildBack synthesizes the technical data into a conversational, 60-second "Elevator Pitch," giving the student a ready-to-read script for introducing their project to an evaluator.

Step 4: Interactive Mock Viva Defense
Simultaneously, the system generates a 5-question multiple-choice quiz tailored explicitly to the detected frameworks and logic. The user interacts with the quiz, receiving instant grading and detailed "Why?" explanations for every right or wrong answer to reinforce their knowledge.

Step 5: Export & Deploy
Once the review is complete, the user clicks a single button to download the entire generated architecture guide as a clean Markdown (.md) file, ready to be dropped into their repository as a professional README or printed for their defense.
---


---

## Additional Documentation

### For Web Projects with Backend:

#### API Documentation

**Base URL:** `https://api.yourproject.com`

##### Endpoints

**GET /api/endpoint**
- **Description:** [What it does]
- **Parameters:**
  - `param1` (string): [Description]
  - `param2` (integer): [Description]
- **Response:**
```json
{
  "status": "success",
  "data": {}
}
```

**POST /api/endpoint**
- **Description:** [What it does]
- **Request Body:**
```json
{
  "field1": "value1",
  "field2": "value2"
}
```
- **Response:**
```json
{
  "status": "success",
  "message": "Operation completed"
}
```

[Add more endpoints as needed...]

---

---
### For Scripts/CLI Tools:

#### Command Reference

**Basic Usage:**
```bash
python script.py [options] [arguments]
```

**Available Commands:**
- `command1 [args]` - Description of what command1 does
- `command2 [args]` - Description of what command2 does
- `command3 [args]` - Description of what command3 does

**Options:**
- `-h, --help` - Show help message and exit
- `-v, --verbose` - Enable verbose output
- `-o, --output FILE` - Specify output file path
- `-c, --config FILE` - Specify configuration file
- `--version` - Show version information

**Examples:**

```bash
# Example 1: Basic usage
python script.py input.txt

# Example 2: With verbose output
python script.py -v input.txt

# Example 3: Specify output file
python script.py -o output.txt input.txt

# Example 4: Using configuration
python script.py -c config.json --verbose input.txt
```

#### Demo Output

**Example 1: Basic Processing**

**Input:**
```
This is a sample input file
with multiple lines of text
for demonstration purposes
```

**Command:**
```bash
python script.py sample.txt
```

**Output:**
```
Processing: sample.txt
Lines processed: 3
Characters counted: 86
Status: Success
Output saved to: output.txt
```

**Example 2: Advanced Usage**

**Input:**
```json
{
  "name": "test",
  "value": 123
}
```

**Command:**
```bash
python script.py -v --format json data.json
```

**Output:**
```
[VERBOSE] Loading configuration...
[VERBOSE] Parsing JSON input...
[VERBOSE] Processing data...
{
  "status": "success",
  "processed": true,
  "result": {
    "name": "test",
    "value": 123,
    "timestamp": "2024-02-07T10:30:00"
  }
}
[VERBOSE] Operation completed in 0.23s
```

---

## Project Demo

### Video
[Add your demo video link here - YouTube, Google Drive, etc.]

*Explain what the video demonstrates - key features, user flow, technical highlights*

### Additional Demos
[Add any extra demo materials/links - Live site, APK download, online demo, etc.]

---

## AI Tools Used (Optional - For Transparency Bonus)

If you used AI tools during development, document them here for transparency:

**Tool Used:** [Gemini]

**Purpose:** [What you used it for]
- Example: "Generated boilerplate React components"
- Example: "Debugging assistance for async functions"
- Example: "Code review and optimization suggestions"

**Key Prompts Used:**
- "Create a REST API endpoint for user authentication"
- "Debug this async function that's causing race conditions"
- "Optimize this database query for better performance"

**Percentage of AI-generated code:** [Approximately X%]

**Human Contributions:**
- Architecture design and planning
- Custom business logic implementation
- Integration and testing
- UI/UX design decisions

*Note: Proper documentation of AI usage demonstrates transparency and earns bonus points in evaluation!*

---

## Team Contributions

- [Name 1]: [Specific contributions - e.g., Frontend development, API integration, etc.]
- [Name 2]: [Specific contributions - e.g., Backend development, Database design, etc.]
- [Name 3]: [Specific contributions - e.g., UI/UX design, Testing, Documentation, etc.]

---

## License

This project is licensed under the [LICENSE_NAME] License - see the [LICENSE](LICENSE) file for details.

**Common License Options:**
- MIT License (Permissive, widely used)
- Apache 2.0 (Permissive with patent grant)
- GPL v3 (Copyleft, requires derivative works to be open source)

---

Made with ❤️ at TinkerHub
