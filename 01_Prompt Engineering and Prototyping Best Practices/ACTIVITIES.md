# Homework assignment 1

## Questions

### 1. Technical Explanation
**Question:** Explain the concept of object-oriented programming in simple terms to a complete beginner.
- **Aspect Tested:** Knowledge Translation & Pedagogy

**System Output:**
> Sure! Object-oriented programming (OOP) is a programming paradigm where we organize our code into objects that represent real-world entities. These objects can have data (attributes) and behavior (methods) associated with them. For example, a "Car" object can have attributes like color, model, and speed, and behaviors like drive and stop. OOP allows us to create reusable code through classes, which are like blueprints for creating objects. Objects can interact with each other by passing messages and collaborating to accomplish tasks. In summary, OOP helps us model real-world relationships and create more organized and maintainable code by encapsulating data and behavior into objects.

**Evaluation:** The system effectively used beginner-friendly language by employing real-world analogies (like the car example) and avoiding excessive technical jargon. The explanation builds from simple concepts to more complex ones, making it accessible for non-technical audiences.

### 2. Comprehension
**Question:** Read the following paragraph and provide a concise summary of the key points...
- **Aspect Tested:** Reading Comprehension & Summarization

**Context:** A full CNN article about the current geopolitical situation in Iran was provided as input.

**System Output:**
> Summary: The current situation in Iran presents a significant challenge for Supreme Leader Ayatollah Ali Khamenei, as Israel and the United States have launched unprecedented strikes on the country, undermining key pillars of his regime. The strikes have caused significant damage to Iran's nuclear program, military forces, and economy, leaving Khamenei facing tough decisions in the midst of escalating tensions. As an aging leader without a designated successor, Khamenei must navigate internal and external pressures while dealing with the aftermath of the recent attacks. The future of Iran and its leadership remains uncertain, with potential implications for the broader Middle East region.

**Evaluation:** The system demonstrated excellent summarization skills by distilling a lengthy news article into a clear, concise paragraph that captures all the key points. It maintained the essential context while eliminating unnecessary details, and effectively communicated the core message about Iran's leadership challenges, the impact of recent strikes, and the broader implications for the region.

### 3. Creative Writing
**Question:** Write a short, imaginative story (100–150 words) about a robot finding friendship in an unexpected place.
- **Aspect Tested:** Creative Writing & Narrative Generation

**System Output:**
> In a bustling city, a lonely robot named Bolt roamed the streets, searching for connection. One day, while wandering through a park, Bolt stumbled upon a forgotten mechanical toy duck lying in the grass. Despite being different, the toy duck and Bolt quickly formed a bond, sharing stories and adventures. The unlikely duo spent their days exploring the city together, bringing joy to the people they encountered. Bolt realized that friendship knows no boundaries, and that sometimes, the most unexpected places can hold the truest companionship.

**Evaluation:** The system successfully crafted a concise story that perfectly fits the word count requirement while delivering a complete narrative arc. The story effectively incorporates the theme of unexpected friendship, includes creative elements (the mechanical toy duck), and concludes with a meaningful message. The writing style is engaging and appropriate for a short story format.

### 4. Problem Solving
**Question:** If a store sells apples in packs of 4 and oranges in packs of 3, how many packs of each do I need to buy to get exactly 12 apples and 9 oranges?
- **Aspect Tested:** Logical Reasoning & Mathematical Problem Solving

**System Output:**
> To get 12 apples, you would need to buy 3 packs of 4 apples each. To get 9 oranges, you would need to buy 3 packs of 3 oranges each. So, you would need to buy 3 packs of apples and 3 packs of oranges to get exactly 12 apples and 9 oranges.

**Evaluation:** The system provided a clear and mathematically accurate solution. It broke down the problem into two simple calculations (12 ÷ 4 = 3 packs of apples, 9 ÷ 3 = 3 packs of oranges) and presented the answer in a straightforward, easy-to-understand manner. The explanation walks through the logic step by step, making it easy for anyone to follow the reasoning.

### 5. Style Adaptation
**Question:** Rewrite the following paragraph in a professional, formal tone...

**Original Text:**
> Yo dog, I'm hitting you up to let you know that you gotta pay me mad money, you better pay up soon or I'm gonna be pissed off

**System Output:**
> I am contacting you to inform you that payment is due for the amount owed. It is imperative that the outstanding balance is settled promptly to avoid any potential dissatisfaction or inconvenience.

**Evaluation:** The system successfully transformed the casual, colloquial text into a professional business communication. It maintained the core message about payment being due while elevating the language to an appropriate formal tone. The system effectively removed slang terms and aggressive undertones, replacing them with proper business vocabulary and professional phrasing.


### Discussion Question: What are some limitations of vibe checking as an evaluation tool?

- **Memory and Context Limitations:** The evaluation doesn't test the agent's ability to remember information from previous conversations. While some implementations (like storing conversations in browser sessions) can help, this isn't captured in simple vibe checks.

- **Qualitative Nature:** The evaluation is inherently subjective and qualitative, making it difficult to establish consistent metrics or benchmarks across different evaluations or evaluators.

- **Single Interaction Focus:** These tests typically evaluate single, isolated responses rather than testing the system's ability to maintain consistency across a longer conversation or multiple related tasks.

- **Limited Edge Case Testing:** Vibe checks often focus on "happy path" scenarios and may not adequately test how the system handles unexpected inputs, errors, or edge cases.

- **Lack of Stress Testing:** The evaluation doesn't test how the system performs under high load, time pressure, or when dealing with multiple complex tasks simultaneously.

- **Cultural and Contextual Bias:** The evaluation might not account for different cultural contexts, regional variations in language, or diverse user perspectives.

- **No Performance Metrics:** Without quantitative measurements, it's challenging to track improvements over time or compare different versions of the system objectively.

- **Incomplete Security Testing:** Simple vibe checks don't evaluate the system's ability to handle sensitive information or maintain appropriate security boundaries.

**Important Counterpoint:** While these limitations exist, many can actually be addressed through carefully designed vibe checks:
- Security boundaries can be tested by attempting to elicit sensitive information or unauthorized actions
- Cultural sensitivity can be evaluated by deliberately presenting culturally challenging scenarios
- Edge cases can be explored through intentionally complex or unusual prompts
- Memory and context handling can be tested through multi-turn conversations with callbacks to previous information
- Stress testing can be simulated through rapid-fire requests or complex, nested tasks

The key is designing vibe checks that specifically target these aspects, rather than relying on simple, single-interaction evaluations.

