# To Run:

## Setup

After the first clone, make a virtual environment using ```virtualenv treehacks24-venv```

Before pushing:

- Run ```pip freeze >> requirements.txt```

After pulling:

- Run ```pip install -r requirements.txt```

### Example .env configuration

```
TOGETHER_API = "secret"
USER_EMAIL = "pgasawa@berkeley.edu"
HOST = "1.1.1.1"
SERVER_LISTEN_PORT = "12342"
SERVER_SEND_PORT = "12343"
NAME = "Parth"
OPENAI_API_KEY = "secret"
```

You can find your host IP address by running ```ifconfig | grep "inet "```. You will need to generate a Together AI API Key and an OpenAI API Key.

Additionally, create a Google Cloud project with email and calendar scopes. Add the emails of accounts you want to use, and then download credentials.json and put it into the ```client``` folder.

## Run

1. Run ```flask --app main run``` from the ```flask``` folder
2. Run ```npm start``` from the ```frontend``` folder
3. Run ```python server.py``` from the ```server``` folder
3. Run ```python client.py``` from the ```client``` folder
3. Run ```python client_ping.py``` from the ```client``` folder

# Information (from [Devpost](https://devpost.com/software/invisible-me))

## Inspiration

Have you ever wished you had…another you?

This thought has crossed all of our heads countless times as we find ourselves swamped in too many tasks, unable to keep up in meetings as information flies over our head, or wishing we had the feedback of a third perspective.

Our goal was to build an **autonomous agent** that could be that person for you — an AI that learns from your interactions and proactively takes **actions**, provides **answers**, offers advice, and more, to give back your time to you.

## What it does

Ephemeral is an **autonomous AI agent** that interacts with the world primarily through the modality of **voice**. It can sit in on meetings, calls, anywhere you have your computer out.

It’s power is the ability to take what it hears and proactively carry out repetitive actions for you such as be a real-time AI assistant in meetings, draft emails directly in your Google inbox, schedule calendar events and invite attendees, search knowledge corpuses or the web for answers to questions, image generation, and more.

Multiple users (in multiple languages!) can use the technology simultaneously through the server/client architecture that efficiently handles multiprocessing.

## How we built it

![link](https://i.imgur.com/PatcdIi.png)

**Languages**: Python ∙ JavaScript ∙ HTML ∙ CSS

**Frameworks and Tools**: React.js ∙ PyTorch ∙ Flask ∙ LangChain ∙ OpenAI ∙ TogetherAI ∙ Many More

### 1. Audio to Text

We utilized OpenAI’s Whisper model and the python speech_recognition library to convert audio in real-time to text that can be used by downstream functions.

### 2. Client → Server via Socket Connection

We use socket connections between the client and server to pass over the textual query to the server for it to determine a particular action and action parameters. The socket connections enable us to support multiprocessing as multiple clients can connect to the server simultaneously while performing concurrent logic (such as real-time, personalized agentic actions during a meeting).

### 3. Neural Network Action Classifier

We trained a neural network from scratch to handle the multi-class classification problem that is going from text to action (or none at all). Because the agent is constantly listening, we need a way to efficiently and accurately determine if each transcribed chunk necessitates a particular action (if so, which?) or none at all (most commonly). 

We generated data for this task utilizing data augmentation sources such as ChatGPT (web).

### 4. LLM Logic: Query → Function Parameters

We use in-context learning via few-shot prompting and RAG to query the LLM for various agentic tasks. We built a RAG pipeline over the conversation history and past related, relevant meetings for context. The agentic tasks take in function parameters, which are generated by the LLM. 

### 5. Server → Client Parameters via Socket Connection

We pass back the function parameters as a JSON object from the server socket to the client.

### 6. Client Side Handler: API Call

A client side handler receives a JSON object that includes which action (if any) was chosen by the Action Planner in step 3, then passes control to the appropriate handler function which handles authorizations and makes API calls to various services such as Google’s Gmail Client, Calendar API, text-to-speech, and more. 

### 7. Client Action Notifications → File (monitored by Flask REST API)

After the completion of each action, the client server writes the results of the action down to a file which is then read by the React Web App to display ephemeral updates on a UI, in addition to suggestions/answers/discussion questions/advice on a polling basis.

### 8. React Web App and Ephemeral UI

To communicate updates to the user (specifically notifications and suggestions from Ephemeral), we poll the Flask API for any updates and serve it to the user via a React web app. Our app is called Ephemeral because we show information minimally yet expressively to the user, in order to promote focus in meetings.

## Challenges we ran into

We spent a significant amount of our time optimizing for lower latency, which is important for a real-time consumer-facing application. In order to do this, we created sockets to enable 2-way communication between the client(s) and the server. Then, in order to support concurrent and parallel execution, we added support for multithreading on the server-side.
Choosing action spaces that can be precisely articulated enough in text such that a language model can carry out actions was a troublesome task. We went through a lot of experimentation on different tasks to figure out which would have the highest value to humans and also the highest correctness guarantee.

## Accomplishments that we're proud of

Successful integration of numerous OSS and closed source models into a working product, including Llama-70B-Chat, Mistral-7B, Stable Diffusion 2.1, OpenAI TTS, OpenAI Whisper, and more.
Integration of real actions that we can see ourselves directly using was very cool to see go from a hypothetical to a reality. The potential for impact of this general workflow in various domains is not lost on us, as while the general productivity purpose stands, there are many more specific gains to be seen in fields such as digital education, telemedicine, and more!

## What we learned

The possibility of powerful autonomous agents to supplement human workflows signals the shift of a new paradigm where more and more our imprecise language can be taken by these programs and turned into real actions on behalf of us.

## What's next for Ephemeral

An agent is only constrained by the size of the action space you give it. We think that Ephemeral has the potential to grow boundlessly as more powerful actions are integrated into its planning capabilities and it returns more of a user’s time to them.
