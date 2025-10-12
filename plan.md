<!-- 9fdd0b11-f340-4c54-8047-c7d42ddafc17 bbc46bfa-c4ef-4471-8c2b-f281f3445875 -->
# AI Tool Categorization and Tag Standardization

## Overview

Standardize all AI tool tags to match category file conventions, add Dataview query displays to each category page, and comprehensively re-tag all 135+ AI tools based on their actual capabilities.

## Tag Standardization Scheme

Current inconsistencies need standardization:

- `AI/AudioRelated` → `AI/AudioGeneration`
- `AI/AI_Agents` → `AI/AI_Agents` (keep as is)
- `AI/AI_Benchmarks` → `AI/AI_Benchmarks` (keep as is)
- `AI/AI_WritingTools` → `AI/AI_WritingTools` (keep as is)
- `AI/AI_Prompts` → `AI/AI_Prompts` (keep as is)
- `AI/AI_Indexes` → `AI/AI_Indexes` (keep as is)
- `AI/CodingAIs` → `AI/CodingAIs` (keep as is)
- `AI/Detection` → `AI/Detection` (keep as is)
- `AI/ImageGeneration` → `AI/ImageGeneration` (keep as is)
- `AI/MiscellaneousAI` → `AI/MiscellaneousAI` (keep as is)
- `AI/Productivity` → `AI/Productivity` (keep as is)
- `AI/RoleplayingAIs` → `AI/RoleplayingAIs` (keep as is)
- `AI/SelfHostingTools` → `AI/SelfHostingTools` (keep as is)
- `AI/TextGeneration` → `AI/TextGeneration` (keep as is)
- `AI/VideoGeneration` → `AI/VideoGeneration` (keep as is)

## Category Page Updates

Add Dataview queries to each category file to automatically display tools:

**Example format for Coding AIs.md:**

````markdown
## 🛠️ Tools in this Category

```dataview
LIST
FROM "AI/003_Content (TheAIs)"
WHERE contains(tags, "AI/CodingAIs")
SORT file.name ASC
````

```

Apply this pattern to all 15 category files.

## Tool Evaluation Strategy

For each of the 135+ AI tools, evaluate based on:

1. **Primary Function** - What's the main purpose?
2. **Secondary Capabilities** - What else can it do?
3. **Use Cases** - How is it actually used?
4. **Description Content** - What features are mentioned?

### Example Re-tagging Logic

**Cursor** (currently: `ai-tool`, `AI/CodingAIs`, `AI`):

- Primary: Coding AI → `AI/CodingAIs` ✓
- Has text generation capabilities → `AI/TextGeneration` ✓
- Productivity tool for developers → `AI/Productivity` ✓
- Could be considered an agent → `AI/AI_Agents` ✓

**ChatGPT** (currently: `ai-tool`, `AI/TextGeneration`, `AI`):

- Primary: Text generation → `AI/TextGeneration` ✓
- Coding assistance mentioned → `AI/CodingAIs` ✓
- Productivity use → `AI/Productivity` ✓
- Writing assistance → `AI/AI_WritingTools` ✓
- Agent-like behavior → `AI/AI_Agents` ✓

**Ollama** (currently: `ai-tool`, `AI/SelfHostingTools`, `AI`):

- Primary: Self-hosting → `AI/SelfHostingTools` ✓
- Runs text models → `AI/TextGeneration` ✓
- Can run coding models → `AI/CodingAIs` ✓
- Agent capabilities → `AI/AI_Agents` (if supports agents)

## Implementation Steps

1. Update Audio Generation category tag from `AI/AudioRelated` to `AI/AudioGeneration`
2. Add Dataview queries to all 15 category pages
3. Systematically review all 135+ tools in alphabetical order
4. Update tags based on comprehensive functionality analysis
5. Verify consistency across all files

## Files to Modify

- 15 category files in `AI/002_AI categories/`
- 135+ tool files in `AI/003_Content (TheAIs)/`
- Priority: Tools with obvious missing tags (coding AIs, general chatbots, multi-purpose tools)

### To-dos - Phase 1 (COMPLETED ✅)

- [x] Update AI/AudioRelated tag to AI/AudioGeneration across all files
- [x] Add Dataview query sections to all 15 category files
- [x] Review and re-tag AI tools A-M (approximately 68 tools)
- [x] Review and re-tag AI tools N-Z (approximately 67 tools)
- [x] Final verification of tag consistency and Dataview query functionality

---

## Phase 2: Advanced Enhancements

### Dashboard & Navigation

#### 1. Master Dashboard
Create `AI/001_Tools/AI_Master_Dashboard.md` with:
- Overview statistics (total tools per category using Dataview)
- Recently added/updated tools (sorted by modification date)
- Most popular tags and categories
- Quick links to all 15 categories
- Summary statistics (total tools: 135+)

#### 2. Filter Dashboard
Create `AI/001_Tools/Filter_Dashboard.md` with quick filters:
- Free tools only
- No sign-up required tools
- Tools by rating (4+ stars)
- Tools by pricing tier
- Platform-specific tools (Web/Desktop/Mobile/API)

### Tool Enhancement Features

#### 3. Extended Frontmatter Schema
Add to each tool's frontmatter:
```yaml
# Existing
tags: [...]
summary: "..."

# New additions
rating: 4.5              # User/community rating
last_verified: 2025-10-12
pricing: free/freemium/paid
sign_up_required: yes/no
status: active/deprecated/beta/discontinued
has_api: yes/no
api_type: REST/GraphQL
platforms: [Web, Desktop, Mobile, CLI]
integrations: [VSCode, GitHub, Slack]
aliases: [GPT, ChatGPT, OpenAI Chat]  # For better search
response_time: fast/medium/slow
community_size: large/medium/small
```

#### 4. Cross-Reference System
Add to each tool file:
```markdown
## 🔗 Related Tools
\`\`\`dataview
LIST summary
FROM "AI/003_Content (TheAIs)"
WHERE contains(tags, "AI/CodingAIs") AND file.name != this.file.name
SORT rating DESC
LIMIT 5
\`\`\`
```

#### 5. Usage Examples Section
Add to each tool file:
```markdown
## 💡 Common Use Cases
- Code review and analysis
- Documentation generation
- Bug fixing and debugging
- Learning new programming concepts
```

#### 6. Changelog Section
Add to each tool file:
```markdown
## 📋 Changelog
- 2025-10-12: Added AI/Productivity tag, updated pricing
- 2025-09-15: Tool reached 1M users milestone
- 2025-08-01: Added API access tier
```

### Comparison & Analysis

#### 7. Comparison Tables
Create category-specific comparison pages:
- `AI/004_Comparisons/Coding_AIs_Comparison.md`
- `AI/004_Comparisons/Text_Generation_Comparison.md`
- `AI/004_Comparisons/Image_Generation_Comparison.md`

Format:
```markdown
| Tool | Pricing | Sign-up | Rating | API | Key Features |
|------|---------|---------|--------|-----|--------------|
| ChatGPT | Freemium | Yes | 4.8 | Yes | GPT-5, reasoning |
| Claude | Freemium | Yes | 4.7 | Yes | Safety-focused |
```

### Advanced Organization

#### 8. Tag Hierarchy
Implement sub-tags for granularity:
```yaml
tags:
  - AI/CodingAIs/IDE_Integration
  - AI/CodingAIs/Code_Review
  - AI/TextGeneration/Chat
  - AI/TextGeneration/Content_Creation
  - AI/ImageGeneration/Text_to_Image
  - AI/ImageGeneration/Image_Editing
```

#### 9. New Folder Structure
```
AI/
├── 001_Tools/
│   ├── AI_Dashboard.md (existing)
│   ├── AI_Master_Dashboard.md (NEW)
│   └── Filter_Dashboard.md (NEW)
├── 002_AI categories/ (existing 15 files)
├── 003_Content (TheAIs)/ (existing 135+ tools)
├── 004_Comparisons/ (NEW)
│   ├── Coding_AIs_Comparison.md
│   ├── Text_Generation_Comparison.md
│   ├── Image_Generation_Comparison.md
│   └── Audio_Generation_Comparison.md
├── 005_Guides/ (NEW)
│   ├── Getting_Started_With_AI_Tools.md
│   ├── Choosing_The_Right_Tool.md
│   └── API_Integration_Guide.md
├── 006_Workflows/ (NEW)
│   ├── Content_Creation_Workflow.md
│   ├── Development_Workflow.md
│   └── Research_Workflow.md
└── 007_Archive/ (NEW)
    └── Deprecated_Tools.md
```

### Automation & Maintenance

#### 10. Automation Opportunities
Create utility scripts:
- `scripts/check_urls.py` - Validate all tool URLs are active
- `scripts/update_dates.py` - Auto-update last_verified dates
- `scripts/generate_report.py` - Monthly report of new/updated tools
- `scripts/tag_validator.py` - Ensure tag consistency

### To-dos - Phase 2

- [ ] Create AI_Master_Dashboard.md with statistics and overview
- [ ] Create Filter_Dashboard.md with quick filter queries
- [ ] Create folder structure (004_Comparisons, 005_Guides, 006_Workflows, 007_Archive)
- [ ] Create comparison tables for major categories (Coding, Text Gen, Image Gen, Audio)
- [ ] Add extended frontmatter schema to template file
- [ ] Update 10 sample tools with extended frontmatter as examples
- [ ] Add cross-reference sections to 10 sample tools
- [ ] Add usage examples to 10 sample tools  
- [ ] Create 2-3 workflow guides
- [ ] Create 2-3 getting started guides
- [ ] Create URL validation script
- [ ] Test all Dataview queries in dashboards

