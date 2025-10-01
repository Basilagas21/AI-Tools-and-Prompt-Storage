# 🤖 AI Tools Dashboard

This dashboard is the central hub for discovering and managing AI tools and websites. It's designed to be a flexible and organized system for keeping track of the AI landscape.

## 🚀 How to Use

1.  **Add a New AI Tool**: To add a new AI tool, create a new note in the `003_Content (TheAIs)` folder. Use the [[AI_Tool_Template]] from the `099_Templates` folder to structure your note.
2.  **Tagging**: Each tool should be tagged with `#ai-tool` and at least one category tag (e.g., `#category/text-generation`). This allows the dashboard to automatically list the tool.
3.  **Categories**: The `002_AI categories` folder contains notes for each category. You can add descriptions or other relevant information to these notes.

## 📂 Categories

```dataview
TABLE WITHOUT ID
  file.link as "AICategory"
FROM "002_AI categories"
SORT file.name ASC
```



## 🛠️ All AI Tools

```dataview
TABLE WITHOUT ID
  file.link as "AI",
  summary as "Summary",
  tags as "AICategories"
FROM #ai-tool
SORT file.name ASC
```
