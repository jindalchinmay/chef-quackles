## Inspiration 💡
In our own households we saw how much food goes to waste just because we don’t know its there and how to use it. Also, all of us are pretty bad at cooking. So, we thought of making a fun solution to this problem.

## What it does 🍳
After saying “Hey Chef” just ask Chef whatever you’d like to do in your kitchen. It will know exactly what’s in your fridge and get context by fetching real recipes from a vector database! Chef Quackles also remembers message history so that you can cook alongside it in real time, asking any questions related to nutrition, steps, or what to do if you put in too many eggs…

There's also a website that connects to Chef Quackles for manual input. 

## How we built it 🛠️
Chef Quackles is built on a software pipeline using 2 separate UX interfaces alongside a Flask server. When the user calls to get ingredients from their fridge, a separate Flask server hosted by a Raspberry Pi is called, taking a photo and remotely uploading it to a Firebase container. Image recognition is done by a multimodal LLM and the ingredients are identified and returned. For the recipe match, a vectorDB was set up using a sentence-to-vector embedding model and a semantic search was performed on ingredients + tags for over 270,000+ recipes!  Additionally due to mean embedding weighting, we utilized rerank-english-v3.0 to rerank the top x recipes for better context. This enables the chef to focus on specific ingredients vs all the ingredients in your fridge. Multimodal LLMs were also used for image generation to create an appealing UI. Additionally, audio-to-text models were used to create an audio chatbot that employed a RAG pipeline of the previous functions, alongside a MongoDB database for context history. The webpage was developed using React in Next.js. The calls to Chef Quackles were parsed using openai whisper and translated into speech using eleven labs. 

## Challenges we ran into 🤔
A big challenge was the setup of 3 separate servers – the webpage, the kitchen photo raspberry pi server and the main backend server.  Additionally Waterloo wifi was not a standard ssid + password network which created challenges with remote SSHing into the pi. Eventually through a delicate process using a team member’s hotspot we were able to set up all 3 servers on the same IP network. 

## Accomplishments that we're proud of 🏆
We are proud to have created a complex network involving frontend, backend, and network programming to seamlessly integrate all components. Additionally, we are extremely proud of how functional the chef is in real-life usage. Designing not one, but two UXs for the user has taught us to think from the user’s perspective and create software that is not only appealing but also highly functional. 

## What we learned 🧠
We learned that making this project required numerous test runs to seamlessly integrate hardware and software—nothing ever works perfectly on the first try…or the eleventh! 

In all seriousness, we learned how to integrate multiple stacks, setting up three databases, building a robust backend, and ensuring seamless communication between components. This taught us a lot about both the technical and design aspects of creating functional and user-friendly software. One of the most significant lessons we learned from integrating the vector database is the importance of efficient data indexing for rapid search results. Initially, we faced challenges with the speed and accuracy of our recipe matching. By fine-tuning the sentence-to-vector embedding model and optimizing the indexing process, we improved the system's ability to quickly retrieve relevant recipes based on the ingredients detected in the fridge. This taught us the critical role of optimized data structures in enhancing performance and user satisfaction.

## What's next for Chef Quackles 🚀
The next steps for Chef Quackles involve expanding its capabilities and enhancing user interactions. We plan to integrate more advanced AI models for personalized recipe recommendations and dietary suggestions tailored to individual preferences and nutritional needs. Additionally, we aim to incorporate real-time voice recognition improvements for more seamless interactions. Furthermore, we're looking to develop a mobile app to allow users to interact with Chef Quackles on the go, ensuring that culinary guidance and assistance are always at their fingertips. Our goal is to make Chef Quackles an indispensable kitchen assistant that continues to evolve and adapt to users' needs.
