# 🤖 AI Tools Dashboard

This dashboard is the central hub for discovering and managing AI tools and websites. It's designed to be a flexible and organized system for keeping track of the AI landscape.

## 🚀 How to Use

1.  **Add a New AI Tool**: To add a new AI tool, create a new note in the `003_Content (TheAIs)` folder. Use the [[AI_Tool_Template]] from the `099_Templates` folder to structure your note.
2.  **Tagging**: Each tool should be tagged with `#ai-tool` and at least one category tag (e.g., `#AI/TextGeneration`). This allows the dashboard to automatically list the tool.
3.  **Categories**: The `002_AI categories` folder contains notes for each category. You can add descriptions or other relevant information to these notes.

## 🛠️ All AI Tools

```dataview
TABLE WITHOUT ID
  file.link as "AI",
  summary as "Summary",
  tags as "AICategories"
FROM #ai-tool
SORT file.name ASC
```

---

## 📋 Category-Specific Tools

### 🤖 Text Generation AIs

```dataview
TABLE WITHOUT ID
  file.link as "Tool",
  summary as "Summary"
FROM #ai-tool
WHERE contains(tags, "AI/TextGeneration") OR contains(tags, "category/text-generation")
SORT file.name ASC
```

### 💻 Coding AIs

```dataview
TABLE WITHOUT ID
  file.link as "Tool",
  summary as "Summary"
FROM #ai-tool
WHERE contains(tags, "AI/CodingAIs") OR contains(tags, "category/coding")
SORT file.name ASC
```

### ✍️ AI Writing Tools

```dataview
TABLE WITHOUT ID
  file.link as "Tool",
  summary as "Summary"
FROM #ai-tool
WHERE contains(tags, "AI/AI_WritingTools") OR contains(tags, "category/writing")
SORT file.name ASC
```

### 🎬 Video Generation AIs

```dataview
TABLE WITHOUT ID
  file.link as "Tool",
  summary as "Summary"
FROM #ai-tool
WHERE contains(tags, "AI/VideoGeneration")
SORT file.name ASC
```

### 🎨 Image Generation AIs

```dataview
TABLE WITHOUT ID
  file.link as "Tool",
  summary as "Summary"
FROM #ai-tool
WHERE contains(tags, "AI/ImageGeneration") OR contains(tags, "category/image-generation")
SORT file.name ASC
```

### 🎵 Audio Generation AIs

```dataview
TABLE WITHOUT ID
  file.link as "Tool",
  summary as "Summary"
FROM #ai-tool
WHERE contains(tags, "AI/AudioRelated")
SORT file.name ASC
```

### 📊 AI Benchmarks

```dataview
TABLE WITHOUT ID
  file.link as "Tool",
  summary as "Summary"
FROM #ai-tool
WHERE contains(tags, "AI/AI_Benchmarks")
SORT file.name ASC
```

### 📚 AI Indexes

```dataview
TABLE WITHOUT ID
  file.link as "Tool",
  summary as "Summary"
FROM #ai-tool
WHERE contains(tags, "AI/AI_Indexes")
SORT file.name ASC
```

### 🎭 Roleplaying AIs

```dataview
TABLE WITHOUT ID
  file.link as "Tool",
  summary as "Summary"
FROM #ai-tool
WHERE contains(tags, "AI/RoleplayingAIs")
SORT file.name ASC
```

### 🏠 Self-Hosting Tools

```dataview
TABLE WITHOUT ID
  file.link as "Tool",
  summary as "Summary"
FROM #ai-tool
WHERE contains(tags, "AI/SelfHostingTools")
SORT file.name ASC
```

### 🎯 AI Prompts

```dataview
TABLE WITHOUT ID
  file.link as "Tool",
  summary as "Summary"
FROM #ai-tool
WHERE contains(tags, "AI/AI_Prompts")
SORT file.name ASC
```

### 🤖 AI Agents

```dataview
TABLE WITHOUT ID
  file.link as "Tool",
  summary as "Summary"
FROM #ai-tool
WHERE contains(tags, "AI/AI_Agents") OR contains(tags, "category/ai-agent")
SORT file.name ASC
```

### 🔍 AI Detection

```dataview
TABLE WITHOUT ID
  file.link as "Tool",
  summary as "Summary"
FROM #ai-tool
WHERE contains(tags, "AI/AI_Detection")
SORT file.name ASC
```

### 🛠️ Miscellaneous AIs

```dataview
TABLE WITHOUT ID
  file.link as "Tool",
  summary as "Summary"
FROM #ai-tool
WHERE contains(tags, "AI/Miscellaneous")
SORT file.name ASC
```

### ⚡ Productivity AIs

```dataview
TABLE WITHOUT ID
  file.link as "Tool",
  summary as "Summary"
FROM #ai-tool
WHERE contains(tags, "AI/Productivity") OR contains(tags, "category/productivity")
SORT file.name ASC
```
