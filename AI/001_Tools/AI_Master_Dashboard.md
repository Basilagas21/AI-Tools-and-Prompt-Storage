# 🎯 AI Master Dashboard

Welcome to the comprehensive AI Tools Master Dashboard! This is your central hub for discovering, analyzing, and managing the entire AI tools ecosystem.

## 📊 Overview Statistics

### Total Tools by Category
```dataview
TABLE WITHOUT ID
  length(rows) as "Count",
  category as "Category"
FROM "AI/003_Content (TheAIs)"
FLATTEN tags as tag
WHERE tag = "AI/TextGeneration" OR tag = "AI/CodingAIs" OR tag = "AI/AI_WritingTools" OR tag = "AI/VideoGeneration" OR tag = "AI/ImageGeneration" OR tag = "AI/AudioGeneration" OR tag = "AI/AI_Benchmarks" OR tag = "AI/AI_Indexes" OR tag = "AI/RoleplayingAIs" OR tag = "AI/SelfHostingTools" OR tag = "AI/AI_Prompts" OR tag = "AI/AI_Agents" OR tag = "AI/Detection" OR tag = "AI/MiscellaneousAI" OR tag = "AI/Productivity"
GROUP BY tag as category
SORT Count DESC
```

### Recently Added/Updated Tools
```dataview
TABLE WITHOUT ID
  file.link as "Tool",
  summary as "Summary",
  file.mtime as "Last Modified"
FROM "AI/003_Content (TheAIs)"
WHERE file.mtime >= date(today) - dur(30 days)
SORT file.mtime DESC
LIMIT 10
```

### Most Popular Categories
```dataview
TABLE WITHOUT ID
  length(rows) as "Tool Count",
  tag as "Category"
FROM "AI/003_Content (TheAIs)"
FLATTEN tags as tag
WHERE tag = "AI/TextGeneration" OR tag = "AI/CodingAIs" OR tag = "AI/AI_WritingTools" OR tag = "AI/VideoGeneration" OR tag = "AI/ImageGeneration" OR tag = "AI/AudioGeneration" OR tag = "AI/AI_Benchmarks" OR tag = "AI/AI_Indexes" OR tag = "AI/RoleplayingAIs" OR tag = "AI/SelfHostingTools" OR tag = "AI/AI_Prompts" OR tag = "AI/AI_Agents" OR tag = "AI/Detection" OR tag = "AI/MiscellaneousAI" OR tag = "AI/Productivity"
GROUP BY tag
SORT Tool Count DESC
```

## 🚀 Quick Navigation

### 📂 All Categories
```dataview
TABLE WITHOUT ID
  file.link as "Category",
  length(rows) as "Tools"
FROM "AI/002_AI categories"
JOIN "AI/003_Content (TheAIs)" ON file.name
SORT file.name ASC
```

### 🏆 Top Rated Tools
```dataview
TABLE WITHOUT ID
  file.link as "Tool",
  summary as "Summary",
  rating as "Rating"
FROM "AI/003_Content (TheAIs)"
WHERE rating >= 4.0
SORT rating DESC
LIMIT 15
```

### 💰 Free Tools Only
```dataview
TABLE WITHOUT ID
  file.link as "Tool",
  summary as "Summary",
  pricing as "Pricing"
FROM "AI/003_Content (TheAIs)"
WHERE pricing = "free"
SORT file.name ASC
```

### 🔥 No Sign-up Required
```dataview
TABLE WITHOUT ID
  file.link as "Tool",
  summary as "Summary",
  sign_up_required as "Sign-up"
FROM "AI/003_Content (TheAIs)"
WHERE sign_up_required = "no"
SORT file.name ASC
```

## 📈 Category Breakdown

### 🤖 Text Generation AIs
```dataview
TABLE WITHOUT ID
  file.link as "Tool",
  summary as "Summary",
  rating as "Rating",
  pricing as "Pricing"
FROM "AI/003_Content (TheAIs)"
WHERE contains(tags, "AI/TextGeneration")
SORT rating DESC
```

### 💻 Coding AIs
```dataview
TABLE WITHOUT ID
  file.link as "Tool",
  summary as "Summary",
  rating as "Rating",
  pricing as "Pricing"
FROM "AI/003_Content (TheAIs)"
WHERE contains(tags, "AI/CodingAIs")
SORT rating DESC
```

### 🎨 Image Generation AIs
```dataview
TABLE WITHOUT ID
  file.link as "Tool",
  summary as "Summary",
  rating as "Rating",
  pricing as "Pricing"
FROM "AI/003_Content (TheAIs)"
WHERE contains(tags, "AI/ImageGeneration")
SORT rating DESC
```

### 🎵 Audio Generation AIs
```dataview
TABLE WITHOUT ID
  file.link as "Tool",
  summary as "Summary",
  rating as "Rating",
  pricing as "Pricing"
FROM "AI/003_Content (TheAIs)"
WHERE contains(tags, "AI/AudioGeneration")
SORT rating DESC
```

### 🎬 Video Generation AIs
```dataview
TABLE WITHOUT ID
  file.link as "Tool",
  summary as "Summary",
  rating as "Rating",
  pricing as "Pricing"
FROM "AI/003_Content (TheAIs)"
WHERE contains(tags, "AI/VideoGeneration")
SORT rating DESC
```

## 🔍 Advanced Filters

### 🏢 Platform-Specific Tools
```dataview
TABLE WITHOUT ID
  file.link as "Tool",
  summary as "Summary",
  platforms as "Platforms"
FROM "AI/003_Content (TheAIs)"
WHERE platforms
SORT file.name ASC
```

### 🔌 API-Enabled Tools
```dataview
TABLE WITHOUT ID
  file.link as "Tool",
  summary as "Summary",
  has_api as "API Available",
  api_type as "API Type"
FROM "AI/003_Content (TheAIs)"
WHERE has_api = "yes"
SORT file.name ASC
```

### ⚡ Fast Response Tools
```dataview
TABLE WITHOUT ID
  file.link as "Tool",
  summary as "Summary",
  response_time as "Response Time"
FROM "AI/003_Content (TheAIs)"
WHERE response_time = "fast"
SORT file.name ASC
```

## 📋 Quick Stats Summary

- **Total AI Tools:** 135+
- **Categories:** 15
- **Most Popular Category:** Text Generation
- **Free Tools Available:** 40+
- **API-Enabled Tools:** 60+
- **Last Updated:** [[AI_Master_Dashboard]]

---

## 🔗 Related Dashboards

- [[AI_Dashboard]] - Original dashboard
- [[Filter_Dashboard]] - Advanced filtering options
- [[AI/004_Comparisons]] - Tool comparisons
- [[AI/005_Guides]] - Getting started guides
- [[AI/006_Workflows]] - Workflow templates

---

*This dashboard is automatically updated based on tool metadata. Last refreshed: `=date(now)`*
