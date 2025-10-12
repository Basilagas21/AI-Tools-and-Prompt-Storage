# 🔍 Filter Dashboard

Advanced filtering and discovery tools for finding the perfect AI tool for your needs.

## 🎯 Quick Filters

### 💰 Pricing Filters

#### Free Tools Only
```dataview
TABLE WITHOUT ID
  file.link as "Tool",
  summary as "Summary",
  pricing as "Pricing"
FROM #ai-tool
WHERE pricing = "free"
SORT file.name ASC
```

#### Freemium Tools
```dataview
TABLE WITHOUT ID
  file.link as "Tool",
  summary as "Summary",
  pricing as "Pricing"
FROM #ai-tool
WHERE pricing = "freemium"
SORT file.name ASC
```

#### Paid Tools Only
```dataview
TABLE WITHOUT ID
  file.link as "Tool",
  summary as "Summary",
  pricing as "Pricing"
FROM #ai-tool
WHERE pricing = "paid"
SORT file.name ASC
```

### 🚀 Access Filters

#### No Sign-up Required
```dataview
TABLE WITHOUT ID
  file.link as "Tool",
  summary as "Summary",
  pricing as "Pricing",
  sign_up_required as "Sign-up Required"
FROM #ai-tool
WHERE sign_up_required = "no"
SORT file.name ASC
```

#### Instant Access Tools
```dataview
TABLE WITHOUT ID
  file.link as "Tool",
  summary as "Summary",
  pricing as "Pricing",
  sign_up_required as "Sign-up Required",
  response_time as "Response Time"
FROM #ai-tool
WHERE sign_up_required = "no" AND pricing = "free"
SORT file.name ASC
```

### ⭐ Quality Filters

#### High-Rated Tools (4+ Stars)
```dataview
TABLE WITHOUT ID
  file.link as "Tool",
  summary as "Summary",
  rating as "Rating",
  pricing as "Pricing"
FROM #ai-tool
WHERE rating >= 4.0
SORT rating DESC
```

#### Top-Tier Tools (4.5+ Stars)
```dataview
TABLE WITHOUT ID
  file.link as "Tool",
  summary as "Summary",
  rating as "Rating",
  pricing as "Pricing",
  community_size as "Community Size"
FROM #ai-tool
WHERE rating >= 4.5
SORT rating DESC
```

### 🏢 Platform Filters

#### Web-Based Tools
```dataview
TABLE WITHOUT ID
  file.link as "Tool",
  summary as "Summary",
  platforms as "Platforms",
  pricing as "Pricing"
FROM #ai-tool
WHERE contains(platforms, "Web")
SORT file.name ASC
```

#### Desktop Applications
```dataview
TABLE WITHOUT ID
  file.link as "Tool",
  summary as "Summary",
  platforms as "Platforms",
  pricing as "Pricing"
FROM #ai-tool
WHERE contains(platforms, "Desktop")
SORT file.name ASC
```

#### Mobile Apps
```dataview
TABLE WITHOUT ID
  file.link as "Tool",
  summary as "Summary",
  platforms as "Platforms",
  pricing as "Pricing"
FROM #ai-tool
WHERE contains(platforms, "Mobile")
SORT file.name ASC
```

#### CLI Tools
```dataview
TABLE WITHOUT ID
  file.link as "Tool",
  summary as "Summary",
  platforms as "Platforms",
  pricing as "Pricing"
FROM #ai-tool
WHERE contains(platforms, "CLI")
SORT file.name ASC
```

### 🔌 Technical Filters

#### API-Enabled Tools
```dataview
TABLE WITHOUT ID
  file.link as "Tool",
  summary as "Summary",
  has_api as "API Available",
  api_type as "API Type",
  pricing as "Pricing"
FROM #ai-tool
WHERE has_api = "yes"
SORT file.name ASC
```

#### REST API Tools
```dataview
TABLE WITHOUT ID
  file.link as "Tool",
  summary as "Summary",
  api_type as "API Type",
  pricing as "Pricing"
FROM #ai-tool
WHERE api_type = "REST"
SORT file.name ASC
```

#### GraphQL API Tools
```dataview
TABLE WITHOUT ID
  file.link as "Tool",
  summary as "Summary",
  api_type as "API Type",
  pricing as "Pricing"
FROM #ai-tool
WHERE api_type = "GraphQL"
SORT file.name ASC
```

### ⚡ Performance Filters

#### Fast Response Tools
```dataview
TABLE WITHOUT ID
  file.link as "Tool",
  summary as "Summary",
  response_time as "Response Time",
  pricing as "Pricing"
FROM #ai-tool
WHERE response_time = "fast"
SORT file.name ASC
```

#### Medium Response Tools
```dataview
TABLE WITHOUT ID
  file.link as "Tool",
  summary as "Summary",
  response_time as "Response Time",
  pricing as "Pricing"
FROM #ai-tool
WHERE response_time = "medium"
SORT file.name ASC
```

### 🏷️ Status Filters

#### Active Tools
```dataview
TABLE WITHOUT ID
  file.link as "Tool",
  summary as "Summary",
  status as "Status",
  last_verified as "Last Verified"
FROM #ai-tool
WHERE status = "active"
SORT last_verified DESC
```

#### Beta Tools
```dataview
TABLE WITHOUT ID
  file.link as "Tool",
  summary as "Summary",
  status as "Status",
  last_verified as "Last Verified"
FROM #ai-tool
WHERE status = "beta"
SORT file.name ASC
```

#### Recently Updated Tools
```dataview
TABLE WITHOUT ID
  file.link as "Tool",
  summary as "Summary",
  last_verified as "Last Verified",
  status as "Status"
FROM #ai-tool
WHERE last_verified >= date(today) - dur(30 days)
SORT last_verified DESC
```

### 🔗 Integration Filters

#### VSCode Integration
```dataview
TABLE WITHOUT ID
  file.link as "Tool",
  summary as "Summary",
  integrations as "Integrations",
  pricing as "Pricing"
FROM #ai-tool
WHERE contains(integrations, "VSCode")
SORT file.name ASC
```

#### GitHub Integration
```dataview
TABLE WITHOUT ID
  file.link as "Tool",
  summary as "Summary",
  integrations as "Integrations",
  pricing as "Pricing"
FROM #ai-tool
WHERE contains(integrations, "GitHub")
SORT file.name ASC
```

#### Slack Integration
```dataview
TABLE WITHOUT ID
  file.link as "Tool",
  summary as "Summary",
  integrations as "Integrations",
  pricing as "Pricing"
FROM #ai-tool
WHERE contains(integrations, "Slack")
SORT file.name ASC
```

## 🎯 Combined Filters

### Free + High-Rated + No Sign-up
```dataview
TABLE WITHOUT ID
  file.link as "Tool",
  summary as "Summary",
  rating as "Rating",
  pricing as "Pricing",
  sign_up_required as "Sign-up Required"
FROM #ai-tool
WHERE pricing = "free" AND rating >= 4.0 AND sign_up_required = "no"
SORT rating DESC
```

### API + Fast Response + Active
```dataview
TABLE WITHOUT ID
  file.link as "Tool",
  summary as "Summary",
  has_api as "API Available",
  response_time as "Response Time",
  status as "Status"
FROM #ai-tool
WHERE has_api = "yes" AND response_time = "fast" AND status = "active"
SORT file.name ASC
```

### Desktop + Paid + High-Rated
```dataview
TABLE WITHOUT ID
  file.link as "Tool",
  summary as "Summary",
  platforms as "Platforms",
  pricing as "Pricing",
  rating as "Rating"
FROM #ai-tool
WHERE contains(platforms, "Desktop") AND pricing = "paid" AND rating >= 4.0
SORT rating DESC
```

## 📊 Filter Statistics

### Pricing Distribution
```dataview
TABLE WITHOUT ID
  length(rows) as "Count",
  pricing as "Pricing Type"
FROM #ai-tool
WHERE pricing
GROUP BY pricing
SORT Count DESC
```

### Platform Distribution
```dataview
TABLE WITHOUT ID
  length(rows) as "Count",
  platform as "Platform"
FROM #ai-tool
FLATTEN platforms as platform
WHERE platform
GROUP BY platform
SORT Count DESC
```

### Status Distribution
```dataview
TABLE WITHOUT ID
  length(rows) as "Count",
  status as "Status"
FROM #ai-tool
WHERE status
GROUP BY status
SORT Count DESC
```

---

## 🔗 Related Dashboards

- [[AI_Master_Dashboard]] - Main dashboard with overview
- [[AI_Dashboard]] - Original dashboard
- [[AI/004_Comparisons]] - Tool comparisons
- [[AI/005_Guides]] - Getting started guides

---

*Use these filters to quickly find tools that match your specific requirements. All filters are automatically updated based on tool metadata.*
