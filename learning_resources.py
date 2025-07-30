"""Learning resources storage using JSON files."""

import json
import os
from pathlib import Path
from typing import List, Dict, Optional, Any, Tuple
from datetime import datetime, timezone
from dataclasses import dataclass, asdict
from enum import Enum
import logging

logger = logging.getLogger("laravel-learning-resources")


class ResourceType(Enum):
    """Type of learning resource."""
    ARTICLE = "article"
    TUTORIAL = "tutorial"
    VIDEO = "video"
    DOCUMENTATION = "documentation"
    COURSE = "course"
    PODCAST = "podcast"
    PACKAGE = "package"


class DifficultyLevel(Enum):
    """Difficulty level of resource."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class ResourceSource(Enum):
    """Source of the learning resource."""
    LARAVEL_NEWS = "laravel-news"
    SPATIE_BLOG = "spatie-blog"
    LARACASTS = "laracasts"
    LARAVEL_BOOTCAMP = "laravel-bootcamp"
    CONFERENCE_TALK = "conference-talk"
    COMMUNITY = "community"
    OFFICIAL_DOCS = "official-docs"


@dataclass
class ResourceMetadata:
    """Metadata for a learning resource."""
    id: Optional[int]
    type: ResourceType
    title: str
    description: Optional[str]
    url: str
    source: ResourceSource
    difficulty_level: Optional[DifficultyLevel]
    published_date: Optional[datetime]
    last_updated: datetime
    tags: List[str]
    metadata: Dict[str, Any]  # Additional source-specific metadata


class LearningResourceDatabase:
    """JSON-based storage for learning resources."""
    
    def __init__(self, data_dir: Path):
        """Initialize the database with the data directory."""
        self.data_dir = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Ensure subdirectories exist
        for subdir in ['articles', 'tutorials', 'videos', 'package_combinations', 'use_cases']:
            (self.data_dir / subdir).mkdir(exist_ok=True)
        
        # Cache for loaded data
        self._resources_cache: Optional[List[ResourceMetadata]] = None
        self._last_cache_time: Optional[datetime] = None
        self._cache_ttl = 300  # 5 minutes
        
        logger.info(f"Initialized LearningResourceDatabase with data at {self.data_dir}")
    
    def _serialize_resource(self, resource: ResourceMetadata) -> Dict[str, Any]:
        """Convert a resource to a JSON-serializable dict."""
        data = asdict(resource)
        # Convert enums to values
        data['type'] = resource.type.value if resource.type else None
        data['source'] = resource.source.value if resource.source else None
        data['difficulty_level'] = resource.difficulty_level.value if resource.difficulty_level else None
        # Convert datetime to ISO format
        if resource.published_date:
            data['published_date'] = resource.published_date.isoformat()
        data['last_updated'] = resource.last_updated.isoformat()
        return data
    
    def _deserialize_resource(self, data: Dict[str, Any]) -> ResourceMetadata:
        """Convert a dict to a ResourceMetadata object."""
        # Convert string values back to enums
        if data.get('type'):
            data['type'] = ResourceType(data['type'])
        if data.get('source'):
            data['source'] = ResourceSource(data['source'])
        if data.get('difficulty_level'):
            data['difficulty_level'] = DifficultyLevel(data['difficulty_level'])
        # Convert ISO strings back to datetime
        if data.get('published_date'):
            data['published_date'] = datetime.fromisoformat(data['published_date'])
        if data.get('last_updated'):
            data['last_updated'] = datetime.fromisoformat(data['last_updated'])
        else:
            data['last_updated'] = datetime.now(timezone.utc)
        
        # Ensure tags is a list
        if not isinstance(data.get('tags'), list):
            data['tags'] = []
        
        # Ensure metadata is a dict
        if not isinstance(data.get('metadata'), dict):
            data['metadata'] = {}
        
        return ResourceMetadata(**data)
    
    def _load_all_resources(self) -> List[ResourceMetadata]:
        """Load all resources from JSON files."""
        # Check cache
        if self._resources_cache is not None and self._last_cache_time:
            if (datetime.now() - self._last_cache_time).total_seconds() < self._cache_ttl:
                return self._resources_cache
        
        resources = []
        
        # Load articles
        articles_dir = self.data_dir / 'articles'
        for file_path in articles_dir.glob('*.json'):
            try:
                with open(file_path, 'r') as f:
                    items = json.load(f)
                    for item in items:
                        resources.append(self._deserialize_resource(item))
            except Exception as e:
                logger.error(f"Error loading {file_path}: {e}")
        
        # Load tutorials
        tutorials_dir = self.data_dir / 'tutorials'
        for file_path in tutorials_dir.glob('*.json'):
            try:
                with open(file_path, 'r') as f:
                    items = json.load(f)
                    for item in items:
                        resources.append(self._deserialize_resource(item))
            except Exception as e:
                logger.error(f"Error loading {file_path}: {e}")
        
        # Load videos
        videos_dir = self.data_dir / 'videos'
        for file_path in videos_dir.glob('*.json'):
            try:
                with open(file_path, 'r') as f:
                    items = json.load(f)
                    for item in items:
                        resources.append(self._deserialize_resource(item))
            except Exception as e:
                logger.error(f"Error loading {file_path}: {e}")
        
        # Update cache
        self._resources_cache = resources
        self._last_cache_time = datetime.now()
        
        return resources
    
    def _save_resource_to_file(self, resource: ResourceMetadata) -> None:
        """Save a resource to the appropriate JSON file."""
        # Determine file path based on type and source
        if resource.type == ResourceType.ARTICLE:
            subdir = 'articles'
        elif resource.type == ResourceType.TUTORIAL:
            subdir = 'tutorials'
        elif resource.type == ResourceType.VIDEO:
            subdir = 'videos'
        else:
            subdir = 'articles'  # Default fallback
        
        filename = f"{resource.source.value.replace('-', '_')}.json"
        file_path = self.data_dir / subdir / filename
        
        # Load existing resources from file
        existing_resources = []
        if file_path.exists():
            try:
                with open(file_path, 'r') as f:
                    items = json.load(f)
                    existing_resources = [self._deserialize_resource(item) for item in items]
            except Exception as e:
                logger.error(f"Error loading existing resources from {file_path}: {e}")
        
        # Add or update resource
        found = False
        for i, existing in enumerate(existing_resources):
            if existing.url == resource.url:
                existing_resources[i] = resource
                found = True
                break
        
        if not found:
            existing_resources.append(resource)
        
        # Save back to file
        with open(file_path, 'w') as f:
            serialized = [self._serialize_resource(r) for r in existing_resources]
            json.dump(serialized, f, indent=2)
        
        # Invalidate cache
        self._resources_cache = None
    
    def add_resource(self, resource: ResourceMetadata) -> int:
        """Add a new resource and return its ID."""
        # Generate ID based on existing resources
        all_resources = self._load_all_resources()
        max_id = max([r.id for r in all_resources if r.id is not None], default=0)
        resource.id = max_id + 1
        
        # Save to file
        self._save_resource_to_file(resource)
        
        return resource.id
    
    def get_resource(self, resource_id: int) -> Optional[ResourceMetadata]:
        """Get a resource by ID."""
        resources = self._load_all_resources()
        for resource in resources:
            if resource.id == resource_id:
                return resource
        return None
    
    def search_resources(
        self,
        query: Optional[str] = None,
        resource_type: Optional[ResourceType] = None,
        source: Optional[ResourceSource] = None,
        difficulty: Optional[DifficultyLevel] = None,
        tags: Optional[List[str]] = None,
        limit: int = 50
    ) -> List[ResourceMetadata]:
        """Search for resources matching criteria."""
        resources = self._load_all_resources()
        results = []
        
        for resource in resources:
            # Type filter
            if resource_type and resource.type != resource_type:
                continue
            
            # Source filter
            if source and resource.source != source:
                continue
            
            # Difficulty filter
            if difficulty and resource.difficulty_level != difficulty:
                continue
            
            # Tag filter
            if tags:
                if not any(tag in resource.tags for tag in tags):
                    continue
            
            # Query filter (search in title and description)
            if query:
                query_lower = query.lower()
                if not (
                    query_lower in resource.title.lower() or
                    (resource.description and query_lower in resource.description.lower()) or
                    any(query_lower in tag.lower() for tag in resource.tags)
                ):
                    continue
            
            results.append(resource)
        
        # Sort by last_updated descending
        results.sort(key=lambda r: r.last_updated, reverse=True)
        
        return results[:limit]
    
    def get_resources_for_use_case(self, use_case: str) -> List[Tuple[ResourceMetadata, float]]:
        """Get resources for a specific use case with relevance scores."""
        # Load use case patterns
        patterns_file = self.data_dir / 'use_cases' / 'patterns.json'
        if not patterns_file.exists():
            return []
        
        try:
            with open(patterns_file, 'r') as f:
                patterns = json.load(f)
        except Exception as e:
            logger.error(f"Error loading use case patterns: {e}")
            return []
        
        if use_case not in patterns:
            return []
        
        pattern = patterns[use_case]
        keywords = pattern.get('keywords', [])
        related_packages = pattern.get('packages', [])
        
        # Search for relevant resources
        resources = self._load_all_resources()
        scored_resources = []
        
        for resource in resources:
            score = 0.0
            
            # Check keywords in title/description
            for keyword in keywords:
                if keyword.lower() in resource.title.lower():
                    score += 0.3
                if resource.description and keyword.lower() in resource.description.lower():
                    score += 0.2
            
            # Check tags
            for tag in resource.tags:
                if tag.lower() in keywords:
                    score += 0.2
                if tag.lower() in related_packages:
                    score += 0.3
            
            if score > 0:
                scored_resources.append((resource, score))
        
        # Sort by score descending
        scored_resources.sort(key=lambda x: x[1], reverse=True)
        
        return scored_resources
    
    def get_package_combination(self, packages: List[str]) -> Optional[Dict[str, Any]]:
        """Get guide for a package combination."""
        # Normalize package list
        packages_set = set(p.lower() for p in packages)
        
        # Load predefined combinations
        predefined_file = self.data_dir / 'package_combinations' / 'predefined.json'
        if predefined_file.exists():
            try:
                with open(predefined_file, 'r') as f:
                    combinations = json.load(f)
                    
                for combo in combinations:
                    combo_packages = set(p.lower() for p in combo.get('packages', []))
                    if combo_packages == packages_set:
                        return combo
            except Exception as e:
                logger.error(f"Error loading package combinations: {e}")
        
        return None
    
    def add_package_combination(
        self,
        packages: List[str],
        use_case: str,
        guide_content: str,
        compatibility_notes: str
    ) -> int:
        """Add a new package combination guide."""
        # This would append to a combinations.json file
        # For now, just log that it would be added
        logger.info(f"Would add package combination: {packages}")
        return 1  # Mock ID


class LearningResourceFetcher:
    """Fetches and manages learning resources."""
    
    def __init__(self, data_dir: Optional[Path] = None):
        """Initialize the fetcher with data directory."""
        if data_dir is None:
            # Use the project's data directory
            project_root = Path(__file__).parent
            data_dir = project_root / "data" / "learning_resources"
        
        self.db = LearningResourceDatabase(data_dir)
        logger.info(f"Initialized LearningResourceFetcher with data at {data_dir}")
    
    def add_resource(
        self,
        title: str,
        url: str,
        resource_type: ResourceType,
        source: ResourceSource,
        description: Optional[str] = None,
        difficulty: Optional[DifficultyLevel] = None,
        published_date: Optional[datetime] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> int:
        """Add a new learning resource."""
        resource = ResourceMetadata(
            id=None,
            type=resource_type,
            title=title,
            description=description,
            url=url,
            source=source,
            difficulty_level=difficulty,
            published_date=published_date,
            last_updated=datetime.now(timezone.utc),
            tags=tags or [],
            metadata=metadata or {}
        )
        
        return self.db.add_resource(resource)
    
    def search(
        self,
        query: str = "",
        resource_type: Optional[str] = None,
        difficulty: Optional[str] = None,
        source: Optional[str] = None,
        tags: Optional[List[str]] = None,
        limit: int = 50
    ) -> List[ResourceMetadata]:
        """Search for learning resources."""
        # Convert string parameters to enums
        type_enum = ResourceType(resource_type) if resource_type else None
        diff_enum = DifficultyLevel(difficulty) if difficulty else None
        source_enum = ResourceSource(source) if source else None
        
        return self.db.search_resources(
            query=query if query else None,
            resource_type=type_enum,
            difficulty=diff_enum,
            source=source_enum,
            tags=tags,
            limit=limit
        )
    
    def get_by_use_case(self, use_case: str, limit: int = 20) -> List[ResourceMetadata]:
        """Get resources relevant to a use case."""
        scored_resources = self.db.get_resources_for_use_case(use_case)
        return [r[0] for r in scored_resources[:limit]]
    
    def get_package_combination_guide(self, packages: List[str]) -> Optional[Dict[str, Any]]:
        """Get guide for combining packages."""
        return self.db.get_package_combination(packages)