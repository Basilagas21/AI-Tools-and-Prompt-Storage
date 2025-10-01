# 📚 Prompt Storage System

Welcome to your new, scalable prompt storage system in Obsidian! This guide will walk you through setting up and using the system to efficiently store, organize, and retrieve your prompts.

### **System Overview**

This system uses a combination of **folders**, **tags**, and the **Dataview** plugin to automate the organization of your prompts.

- **Folders**: All prompts are stored in a main `Prompts` folder for a clean file structure.
    
- **Tags**: Instead of relying on a rigid folder structure, we use a hierarchical tagging system (e.g., `#prompt/marketing`) for flexible categorization.
    
- **Dataview**: This powerful plugin reads your tags and automatically generates dynamic lists of your prompts on your dashboard.
    

### **How to Use**

Follow these steps to get started:

#### **1. Install the Dataview Plugin**

- Go to **Settings** > **Community plugins**.
    
- Click **"Turn on Community plugins"** (if they are not already on).
    
- Click **"Browse"** and search for "Dataview".
    
- Click **"Install"** and then **"Enable"**.
    

#### **2. Create Your Prompt Files**

- Create a dedicated `Prompts` folder in your vault.
    
- Inside the `Prompts` folder, create a new file for each prompt.
    
- At the top of each file, add a YAML frontmatter section with a `tags` field. This is how Dataview finds your prompts.
    
- Use the `tags` to categorize your prompt. A good practice is to always include a general `#prompt` tag, followed by a more specific category tag. For example:
    

```
---
tags:
  - "#prompt"
  - "#prompt/creative"
---
```

#### **3. View Your Prompts on the Dashboard**

Your `Prompt Dashboard.md` is set up with Dataview queries to automatically pull in your prompts. Each section on the dashboard has a hidden Dataview query that looks for a specific tag.

For example, to list all your creative prompts with their titles, the dashboard uses this query:

```
TABLE file.name as "Title"
FROM "Prompts"
WHERE contains(file.tags, "#prompt/creative")
SORT file.name ASC
```

- To see the list, simply open the `Prompt Dashboard.md` file in your main Obsidian window.
    
- You can edit these queries to customize what's displayed or how it's sorted.
    

### **Tips for Efficiency**

- **Use a Template**: Create a template for new prompts. This ensures every prompt file has the necessary tags and structure.
    
- **Create New Categories**: If you need a new category, just start using a new tag like `#prompt/new-category`. Then, you can add a new section on your dashboard with a Dataview query for that tag.
    
- **Link Between Files**: Use `[[Internal Links]]` to connect related prompts or link to specific notes for context. This creates a flexible, interconnected network of information.