"""
This module detects the intent of the user prompt to guide optimization strategy.

The intent detector classifies prompts into categories using rule-based keyword matching:
- explanation: For prompts asking to explain or describe concepts
- comparison: For prompts comparing two or more items
- coding: For programming-related prompts
- creative: For creative writing prompts
- analysis: For analytical evaluation prompts
- general: Default category for unclassified prompts
"""


def detect_intent(prompt: str) -> str:
    """
    Detect the primary intent of a user prompt using keyword matching.
    
    Args:
        prompt: The user input prompt to classify.
        
    Returns:
        A string representing the detected intent category.
    """
    intents = detect_intents(prompt)
    return intents[0] if intents else "general"


def detect_intents(prompt: str) -> list:
    """
    Detects all possible user intents instead of only one.
    
    Args:
        prompt: The user input prompt to classify.
        
    Returns:
        A list of detected intent categories sorted by priority.
    """
    # Convert to lowercase for matching
    lower_prompt = prompt.lower()
    
    # Define keyword groups for each intent
    explanation_keywords = [
        "explain", "describe", "what is", "define", "tell me about", "how does", 
        "what does", "clarify", "elaborate", "illustrate", "break down", "walk me through",
        "help me understand", "give an overview", "introduce", "summarize", "outline",
        "can you explain", "please describe", "what are", "what's", "meaning of",
        "definition of", "concept of", "idea behind", "principle of", "theory of",
        "how to understand", "make sense of", "shed light on", "elucidate", "expound",
        "detail", "specify", "characterize", "interpret", "demystify", "unpack",
        "talk about", "discuss", "cover", "go over", "run through", "provide details",
        "give me information", "inform me about", "enlighten me", "teach me", "educate me"
    ]

    comparison_keywords = [
        "compare", "difference between", "vs", "versus", "contrast", "distinguish",
        "compare and contrast", "differentiate", "how does X differ from Y", 
        "what's the difference", "similarities and differences", "better than",
        "worse than", "superior to", "inferior to", "advantages over", "disadvantages of",
        "X or Y", "which is better", "which should I choose", "preferred over",
        "relative to", "in comparison to", "compared to", "as opposed to", "rather than",
        "instead of", "alternative to", "versus each other", "side by side",
        "head to head", "match up", "stack up against", "measure against", "weigh against",
        "parallel between", "correlation between", "relationship between", "likeness",
        "disparity", "distinction", "divergence", "variance", "discrepancy"
    ]

    coding_keywords = [
        "code", "python", "java", "implement", "algorithm", "function", "javascript",
        "c++", "programming", "script", "program", "develop", "build", "create",
        "write code", "debug", "fix bug", "error", "syntax", "compile", "execute",
        "run", "class", "method", "variable", "loop", "array", "list", "dictionary",
        "object", "API", "library", "framework", "module", "package", "import",
        "return", "parameter", "argument", "string", "integer", "boolean", "float",
        "data structure", "recursion", "iteration", "conditional", "if statement",
        "for loop", "while loop", "try catch", "exception", "async", "await",
        "callback", "promise", "regex", "sql", "database", "query", "html", "css",
        "react", "node", "django", "flask", "backend", "frontend", "fullstack",
        "git", "github", "repository", "commit", "push", "pull", "merge", "branch",
        "refactor", "optimize", "test", "unit test", "integration", "deployment",
        "docker", "kubernetes", "CI/CD", "REST API", "GraphQL", "JSON", "XML",
        "OOP", "functional programming", "lambda", "closure", "scope", "inheritance",
        "polymorphism", "encapsulation", "abstraction", "design pattern", "SOLID"
    ]

    creative_keywords = [
        "story", "poem", "imagine", "creative", "fiction", "write a story",
        "tale", "narrative", "plot", "character", "scene", "dialogue", "novel",
        "short story", "fantasy", "sci-fi", "science fiction", "romance", "thriller",
        "mystery", "adventure", "drama", "comedy", "satire", "parody", "fable",
        "legend", "myth", "fairy tale", "bedtime story", "children's story",
        "write a poem", "haiku", "sonnet", "limerick", "verse", "rhyme", "stanza",
        "ballad", "ode", "elegy", "free verse", "acrostic", "epic", "lyric",
        "create a character", "develop a plot", "world-building", "setting",
        "protagonist", "antagonist", "conflict", "climax", "resolution", "twist",
        "creative writing", "fiction writing", "compose", "craft", "invent",
        "dream up", "conjure", "envision", "visualize", "brainstorm ideas",
        "screenplay", "script", "monologue", "soliloquy", "play", "act", "scene",
        "song lyrics", "rap", "metaphor", "simile", "imagery", "symbolism",
        "allegory", "personification", "flashback", "foreshadowing", "narrator",
        "point of view", "first person", "third person", "omniscient", "backstory",
        "arc", "theme", "motif", "tone", "mood", "atmosphere", "genre"
    ]

    analysis_keywords = [
        "analyze", "analysis", "pros and cons", "evaluate", "assess", "examine",
        "review", "critique", "judge", "appraise", "scrutinize", "investigate",
        "study", "inspect", "explore", "dissect", "parse", "deconstruct",
        "advantages and disadvantages", "benefits and drawbacks", "strengths and weaknesses",
        "upsides and downsides", "positive and negative", "merits and demerits",
        "for and against", "arguments for", "arguments against", "case for", "case against",
        "weigh the options", "consider the implications", "assess the impact",
        "evaluate the effectiveness", "determine the value", "measure the success",
        "critical analysis", "in-depth analysis", "detailed examination", "thorough review",
        "comprehensive assessment", "systematic evaluation", "objective analysis",
        "interpret the data", "draw conclusions", "infer", "deduce", "reason",
        "think critically", "question", "challenge", "verify", "validate", "test",
        "evidence for", "evidence against", "support for", "opposition to",
        "feasibility", "viability", "practicality", "effectiveness", "efficiency",
        "performance", "quality", "reliability", "validity", "credibility",
        "trade-offs", "opportunity cost", "risk assessment", "cost-benefit",
        "SWOT analysis", "strengths", "weaknesses", "opportunities", "threats",
        "implications", "ramifications", "consequences", "outcomes", "results",
        "findings", "observations", "insights", "patterns", "trends", "correlations"
    ]
    
    question_keywords = [
        "what", "why", "how", "when", "where", "who", "which", "whose", "whom",
        "can you", "could you", "would you", "will you", "should I", "do you",
        "is it", "are there", "does it", "has it", "have you", "did you",
        "question about", "I'm wondering", "I want to know", "tell me", "show me",
        "help me", "assist me", "guide me", "advise me", "suggest", "recommend"
    ]

    instruction_keywords = [
        "create", "make", "build", "generate", "produce", "develop", "design",
        "construct", "formulate", "devise", "draft", "compose", "prepare",
        "give me", "provide", "show", "display", "present", "demonstrate",
        "list", "enumerate", "outline", "summarize", "condense", "shorten",
        "expand", "elaborate", "extend", "lengthen", "add to", "include",
        "remove", "delete", "exclude", "omit", "filter", "extract", "isolate",
        "convert", "transform", "translate", "adapt", "modify", "change",
        "update", "revise", "edit", "improve", "enhance", "optimize", "refine",
        "simplify", "clarify", "restructure", "reorganize", "reformat", "rewrite"
    ]

    research_keywords = [
        "research", "find information", "look up", "search for", "investigate",
        "gather data", "collect information", "source", "reference", "citation",
        "study on", "report about", "statistics", "data", "facts", "figures",
        "evidence", "documentation", "literature review", "survey", "poll",
        "recent developments", "latest news", "current trends", "up-to-date",
        "scholarly", "academic", "peer-reviewed", "scientific", "empirical",
        "case study", "experiment", "trial", "test results", "findings"
    ]

    problem_solving_keywords = [
        "solve", "fix", "troubleshoot", "resolve", "address", "handle",
        "deal with", "overcome", "work around", "find a solution", "answer",
        "remedy", "correct", "repair", "debug", "diagnose", "identify the issue",
        "problem with", "issue with", "error in", "bug in", "challenge",
        "difficulty", "obstacle", "roadblock", "bottleneck", "how do I fix",
        "how to solve", "what's wrong", "why isn't", "not working", "failing"
    ]

    tutorial_keywords = [
        "tutorial", "guide", "how-to", "step by step", "walkthrough", "instructions",
        "teach me", "show me how", "learn", "training", "course", "lesson",
        "beginner", "for beginners", "getting started", "introduction to",
        "basics of", "fundamentals", "start with", "first steps", "quickstart",
        "best practices", "tips", "tricks", "techniques", "methods", "approaches"
    ]

    summarization_keywords = [
        "summarize", "summary", "brief", "overview", "recap", "synopsis",
        "abstract", "digest", "condensed version", "tldr", "in short", "in brief",
        "key points", "main ideas", "highlights", "essence", "gist", "nutshell",
        "boil down", "distill", "compress", "reduce", "shorten", "abbreviate"
    ]
    
    # Map intent names to their keyword lists
    intent_keywords = {
        "explanation": explanation_keywords,
        "comparison": comparison_keywords,
        "coding": coding_keywords,
        "creative": creative_keywords,
        "analysis": analysis_keywords,
        "question": question_keywords,
        "instruction": instruction_keywords,
        "research": research_keywords,
        "problem_solving": problem_solving_keywords,
        "tutorial": tutorial_keywords,
        "summarization": summarization_keywords
    }
    
    # Priority order for sorting
    priority_order = [
        "comparison", "coding", "analysis", "tutorial", "explanation",
        "research", "summarization", "creative", "instruction", "question",
        "problem_solving", "general"
    ]
    
    # Detect all matching intents
    detected = []
    for intent_name, keywords in intent_keywords.items():
        for keyword in keywords:
            if keyword in lower_prompt:
                if intent_name not in detected:
                    detected.append(intent_name)
                break
    
    # If no intent detected, return general
    if not detected:
        return ["general"]
    
    # Sort by priority order
    detected.sort(key=lambda x: priority_order.index(x) if x in priority_order else len(priority_order))
    
    return detected


if __name__ == "__main__":
    tests = [
        "Explain CNN",
        "Difference between CNN vs RNN and analyze performance",
        "Summarize this article and explain key ideas",
        "Write a story and describe the main character"
    ]
    for t in tests:
        print(t, "→", detect_intents(t))
