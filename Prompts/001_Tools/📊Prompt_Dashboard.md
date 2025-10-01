
Welcome to your central hub for managing and navigating your prompts! This dashboard is designed to automatically show you your prompts by category.
You can also refer to [[README.file Prompt Storage |README.md]] for tutorials to use the prompt storage

### **Prompt Categories**

- [[CreateNewPrompts]] : Got new prompt? Start creating one here
    
- [[Creative Prompts]]: For stories, poetry, and artistic ideas.
    
- [[Technical Prompts]]: For code, scripts, and technical tasks.
    
- [[Analytical Prompts]]: For research, reports, and data analysis.
    
- [[General Prompts]]: For everyday tasks and miscellaneous ideas.
    
- [[Marketing Prompts]]: For ad copy, social media, and email campaigns.
    
- [[Educational Prompts]]: For learning, summarizing, and teaching.
    
- [[Productivity Prompts]]: For planning, brainstorming, and task management.
- [[Persona Prompts]] : For getting ez access through a persona
    

### **How to Use This System**

This dashboard is designed to be **dynamic**! To make it work, you'll need the **Dataview** plugin. Once installed, the queries below will automatically list your prompts.

### **Marketing Prompts**

```dataview
TABLE file.name as "Title"
FROM ""
WHERE contains(file.tags, "prompt/marketing")   
SORT file.name ASC
```

### **Educational Prompts**

```dataview
TABLE file.name as "Title"
FROM ""
WHERE contains(file.tags, "#prompt/educational")
SORT file.name ASC
```

### **Creative Prompts**

```dataview
TABLE file.name as "Title"
FROM ""
WHERE contains(file.tags, "#prompt/creative")
SORT file.name ASC
```
### **Technical Prompts**

```dataview
TABLE file.name as "Title"
FROM ""
WHERE contains(file.tags, "#prompt/technical")
SORT file.name ASC
```

### **Analytical Prompts**

```dataview
TABLE file.name as "Title"
FROM ""
WHERE contains(file.tags, "#prompt/analytical")
SORT file.name ASC
```

### **Productivity Prompts**

```dataview
TABLE file.name as "Title"
FROM ""
WHERE contains(file.tags, "#prompt/productivity")
SORT file.name ASC
```

### **General Prompts**

```dataview
TABLE file.name as "Title"
FROM ""
WHERE contains(file.tags, "#prompt/general")
SORT file.name ASC
```