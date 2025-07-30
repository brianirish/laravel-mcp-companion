# Conference Talk Aggregator Documentation

The ConferenceTalkAggregator fetches Laravel conference talks from YouTube, supporting both API-based and web scraping approaches.

## Features

- **Dual Mode Operation**: Works with or without YouTube API key
- **Multiple Sources**: Fetches from official Laravel channels, Laracon EU, PHP UK Conference
- **Smart Filtering**: Automatically identifies Laravel conference talks vs tutorials
- **Rich Metadata**: Extracts speaker names, conference info, duration, and technology tags
- **Curated Content**: Includes hand-picked recent high-quality talks

## Usage

### Without YouTube API (Default)

```python
from content_aggregators import ConferenceTalkAggregator, LearningResourceFetcher
from pathlib import Path

# Initialize
fetcher = LearningResourceFetcher(Path("learning_resources.db"))
aggregator = ConferenceTalkAggregator(fetcher)

# Fetch conference talks (uses web scraping)
resource_ids = aggregator.fetch_conference_talks(max_videos=50)
```

### With YouTube API

```python
# Set API key via environment variable
export YOUTUBE_API_KEY="your-api-key-here"

# Or pass directly
aggregator = ConferenceTalkAggregator(fetcher, youtube_api_key="your-api-key")

# Fetch using API
resource_ids = aggregator.fetch_conference_talks(use_api=True, max_videos=100)
```

### Backward Compatibility

```python
# Legacy method still works
resource_ids = aggregator.add_known_talks()  # Returns 20 curated talks
```

## Known Channels and Playlists

### Laravel Official
- Channel: [@LaravelPHP](https://www.youtube.com/@LaravelPHP)
- Playlists:
  - Laracon US 2023
  - Laracon Online 2022
  - Laracon EU 2019
  - Laracon US 2019

### Laracon EU
- Channel: [@LaraconEU](https://www.youtube.com/@LaraconEU)

### PHP UK Conference
- Channel: [@phpukconference](https://www.youtube.com/@phpukconference)

## Extracted Metadata

Each conference talk includes:

- **Title**: Full talk title
- **URL**: YouTube video URL
- **Description**: Video description (truncated to 500 chars)
- **Speaker**: Extracted from title or metadata
- **Conference**: Conference name and year
- **Duration**: Video length
- **Tags**: Technology tags, conference tags, year, speaker
- **Difficulty**: Estimated based on content analysis
- **Thumbnail**: Video thumbnail URL (when using API)

## Technology Tags

The aggregator automatically identifies and tags talks about:

- Frameworks: Laravel, Livewire, Inertia, Alpine, Vue, React
- Testing: Pest, PHPUnit
- Tools: Forge, Vapor, Horizon, Telescope, Pulse, Folio, Volt
- Concepts: API, GraphQL, WebSockets, Broadcasting, Queues, Events
- DevOps: Docker, Sail, Deployment

## Filtering Logic

Videos are identified as conference talks if they:
1. Contain Laravel-related keywords
2. Mention conferences or presentations
3. Don't contain tutorial/course indicators

## Rate Limiting

- API mode: 1 second between playlist fetches
- Scraping mode: 2 seconds between requests
- Respects YouTube's rate limits

## Error Handling

- Gracefully handles missing API keys
- Continues on individual video failures
- Logs all errors for debugging