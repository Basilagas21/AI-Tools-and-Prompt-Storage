# AI & Prompt Knowledge Base

Welcome to a comprehensive, professionally-organized digital brain for AI exploration, built with [Obsidian](https://obsidian.md/). This repository serves as an advanced knowledge management (PKM) system to catalog AI tools, craft high-quality prompts, and provide intelligent workflows for AI-powered productivity.

Whether you're an AI enthusiast, a developer, or a creative professional, this system provides a scalable framework to harness the power of artificial intelligence with advanced dashboards, comparison tools, workflow guides, and automation scripts.

## 🚀 **What's New in Phase 2**

- **📊 Advanced Dashboards** - Master dashboard with statistics and filter dashboard with 20+ filtering options
- **📈 Comparison Tables** - Detailed side-by-side comparisons for major AI tool categories
- **🛠️ Enhanced Metadata** - Extended frontmatter with ratings, pricing, platforms, and more
- **📚 Comprehensive Guides** - Getting started guides, tool selection frameworks, and API integration help
- **🔄 Workflow Templates** - Complete workflows for content creation, development, and research
- **🔧 Automation Scripts** - URL validation, metadata updates, and tag consistency tools
- **🎯 Cross-References** - Dynamic related tools and intelligent recommendations

---

## The Philosophy

In the rapidly evolving landscape of AI, staying organized is key. This vault is built on the principle of a flexible, interconnected web of knowledge. Instead of rigid hierarchies, it uses a combination of structured directories and dynamic linking, allowing information to be both organized and discoverable in multiple contexts.

## Core Components

This vault is split into two primary domains:

1.  **`/AI/`**: A comprehensive encyclopedia of AI tools and technologies.
2.  **`/Prompts/`**: A powerful and scalable system for developing, storing, and managing AI prompts.

---

## `/AI/` — The AI Encyclopedia

This directory is your comprehensive atlas of the AI world, featuring advanced dashboards, detailed comparisons, and intelligent workflows. It's designed to systematically document and explore the capabilities of various AI tools, from well-known platforms to niche applications.

### 🎯 **Core Structure**

-   **`001_Tools/`**: **Advanced Dashboards & Tools**
    - `AI_Master_Dashboard.md` - Central hub with statistics and overview
    - `Filter_Dashboard.md` - Advanced filtering with 20+ options
    - `AI_Dashboard.md` - Enhanced original dashboard
    - `Phase_2_Implementation_Summary.md` - Complete implementation overview

-   **`002_AI categories/`**: **Standardized Taxonomy System**
    - 15 standardized categories (Text Generation, Coding AIs, Image Generation, etc.)
    - Each category includes Dataview queries for automatic tool listing
    - Consistent tag structure across all tools

-   **`003_Content (TheAIs)/`**: **Enhanced Tool Profiles**
    - 135+ detailed AI tool profiles with extended metadata
    - Cross-reference sections with related tools
    - Usage examples and changelog tracking
    - Standardized frontmatter with ratings, pricing, platforms

-   **`004_Comparisons/`**: **Detailed Tool Comparisons**
    - `Coding_AIs_Comparison.md` - Development tools analysis
    - `Text_Generation_Comparison.md` - Chat and writing tools
    - `Image_Generation_Comparison.md` - Visual content tools
    - `Audio_Generation_Comparison.md` - Voice and music tools

-   **`005_Guides/`**: **Comprehensive Learning Resources**
    - `Getting_Started_With_AI_Tools.md` - Beginner's guide
    - `Choosing_The_Right_Tool.md` - Tool selection framework
    - `API_Integration_Guide.md` - Developer integration help

-   **`006_Workflows/`**: **Complete Process Templates**
    - `Content_Creation_Workflow.md` - End-to-end content process
    - `Development_Workflow.md` - AI-assisted development
    - `Research_Workflow.md` - Research using AI tools

-   **`007_Archive/`**: **Future Archive** - For deprecated tools and historical data

-   **`099_Templates/`**: **Enhanced Templates**
    - `AI_Tool_Template.md` - Extended frontmatter schema
    - Standardized structure for consistency

-   **`100_Reference/`**: **Learning Hub** - Articles, research, and tutorials

---

## `/Prompts/` — The Prompt Engineering Lab

This is more than just a folder of text files; it's a sophisticated system for prompt management. Leveraging the power of Obsidian and the Dataview plugin, it transforms a simple collection of prompts into a dynamic, queryable database.

### How It Works

This system is designed for flexibility and power, allowing you to find the perfect prompt when you need it.

-   **`001_Tools/`**: Notes on tools that assist in prompt engineering, such as prompt builders or optimizers.
-   **`002_Prompt Categories/`**: Similar to the AI directory, this provides a high-level organization of prompt types (e.g., "Creative Writing," "Code Generation," "Marketing Copy").
-   **`003_Content (ThePrompts)/`**: The central repository for all your prompts. Each prompt is a separate note, tagged for easy retrieval.
-   **`004_SampleOfPrompts/`**: A portfolio of your best work. This folder links prompts to their generated outputs, creating a valuable feedback loop for refining your prompt engineering skills.
-   **`099_Templates/`**: Contains templates for structuring new prompts, ensuring they include necessary metadata like tags, parameters, and target AI models.
-   **`100_Reference/`**: Stores guides, articles, and best practices on the art and science of prompt engineering.

> **A Note on a Smarter Workflow**
> The true power of this system is detailed in `Prompts/README.file Prompt Storage.md`. It explains how to use Obsidian's tagging system and the **Dataview plugin** to create dynamic dashboards that automatically organize and display your prompts based on their categories, making your collection instantly searchable and browsable without ever having to move a file.

## 🚀 **Quick Start Guide**

### **1. Setup & Installation**
1. **Clone the Repository**: Download this repository to your local machine
2. **Open as an Obsidian Vault**: Open Obsidian and select "Open folder as vault"
3. **Install Required Plugins**: 
   - [Dataview plugin](https://blacksmithgu.github.io/obsidian-dataview/) - Essential for dynamic queries
   - [Templater plugin](https://github.com/SilentVoid13/Templater) - For template automation
4. **Install Python Dependencies** (for automation scripts):
   ```bash
   pip install requests pyyaml cryptography
   ```

### **2. Explore the Dashboards**
- **Start with `AI/001_Tools/AI_Master_Dashboard.md`** - Your central hub
- **Try `AI/001_Tools/Filter_Dashboard.md`** - Advanced filtering options
- **Check `AI/004_Comparisons/`** - Detailed tool comparisons

### **3. Use the Guides**
- **Beginners**: Start with `AI/005_Guides/Getting_Started_With_AI_Tools.md`
- **Tool Selection**: Use `AI/005_Guides/Choosing_The_Right_Tool.md`
- **Developers**: Check `AI/005_Guides/API_Integration_Guide.md`

### **4. Follow Workflows**
- **Content Creation**: Use `AI/006_Workflows/Content_Creation_Workflow.md`
- **Development**: Follow `AI/006_Workflows/Development_Workflow.md`
- **Research**: Apply `AI/006_Workflows/Research_Workflow.md`

## 🔧 **Automation & Maintenance**

### **Available Scripts**
Located in the `scripts/` directory:

- **`check_urls.py`** - Validates all tool URLs (154 URLs tested)
- **`update_metadata.py`** - Updates tool metadata and dates
- **`tag_validator.py`** - Ensures tag consistency across tools
- **`test_dataview_queries.py`** - Validates all Dataview queries (60 queries tested)

### **Running Scripts**
```bash
# Validate URLs
python scripts/check_urls.py --path "AI/003_Content (TheAIs)" --verbose

# Update metadata
python scripts/update_metadata.py --update-dates --verbose

# Validate tags
python scripts/tag_validator.py --path "AI/003_Content (TheAIs)" --verbose

# Test Dataview queries
python scripts/test_dataview_queries.py --path "AI/001_Tools" --verbose
```

## 📊 **System Statistics**

- **135+ AI Tools** - Comprehensive collection with detailed profiles
- **15 Standard Categories** - Consistent taxonomy and organization
- **60 Dataview Queries** - All validated and working
- **154 URLs** - All validated and accessible
- **4 Comparison Tables** - Detailed analysis of major categories
- **3 Workflow Guides** - Complete process templates
- **3 Getting Started Guides** - From beginner to advanced
- **4 Automation Scripts** - Maintenance and validation tools

## 🎯 **Key Features**

### **Advanced Dashboards**
- **Real-time Statistics** - Tool counts, ratings, pricing distribution
- **Smart Filtering** - 20+ filter options (free tools, API access, ratings, etc.)
- **Dynamic Queries** - Automatically updated tool listings
- **Cross-References** - Intelligent related tool suggestions

### **Enhanced Tool Profiles**
- **Extended Metadata** - Ratings, pricing, platforms, integrations, aliases
- **Usage Examples** - Common use cases for each tool
- **Changelog Tracking** - Version history and updates
- **Related Tools** - Dynamic suggestions based on categories

### **Comprehensive Comparisons**
- **Side-by-Side Analysis** - Detailed feature comparisons
- **Use Case Recommendations** - Best tools for specific needs
- **Performance Metrics** - Speed, quality, and technical specs
- **Pricing Breakdown** - Free, freemium, and paid options

## 🔄 **Customization & Growth**

This system is designed to grow with you:

- **Customize Categories** - Add new AI tool categories as they emerge
- **Refine Templates** - Update templates based on your specific needs
- **Add Workflows** - Create new workflow guides for your use cases
- **Extend Automation** - Build additional scripts for your requirements
- **Community Contribution** - Share improvements and new tools

## 🏆 **Success Metrics**

- ✅ **100% Phase 2 Completion** - All planned features implemented
- ✅ **60 Dataview Queries** - All validated and functional
- ✅ **154 URLs** - All tested and accessible
- ✅ **10 Enhanced Tools** - Extended metadata examples
- ✅ **Professional Structure** - Ready for advanced features and community contributions

---

**This system provides a professional-grade foundation for AI tool discovery, comparison, and workflow optimization. Start with the dashboards, explore the comparisons, follow the workflows, and build your ultimate AI knowledge base!**