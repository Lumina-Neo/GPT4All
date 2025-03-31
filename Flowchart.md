flowchart TD
    A[User Prompt to Local Model] --> B[Check Model Parameters]
    B --> C{Token Limit Set?}
    C -->|Yes, Low (e.g. 200-512)| D[Short / Cut-Off Response]
    C -->|No or High (1024+)| E[Extended / Full Response]

    D --> F[Fix in GPT4All GUI (Set to 2048)]
    D --> G[Fix in Python Wrapper (max_tokens=2048)]
    G --> H[main_memory_reader.py Updated]
    F --> H

    E --> I[Long Monad Dialogue Enabled]
    H --> I

    style D fill="#ffcccc"
    style G fill="#ccffcc"
    style H fill="#ccffcc"
    style I fill="#d0f0ff"
