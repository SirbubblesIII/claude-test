"""
Scratchpad Phase: Evidence gathering and memory management.

Formulates search queries, executes tool calls with timestamps,
and manages memory with explicit lifecycle metadata.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Callable, TYPE_CHECKING
from enum import Enum
from datetime import datetime, timedelta
import uuid
import json

if TYPE_CHECKING:
    from .reasoning import Hypothesis


class EvidenceSourceType(Enum):
    """Types of evidence sources."""
    WEB_SEARCH = "web_search"
    CODEBASE_SEARCH = "codebase_search"
    FILE_READ = "file_read"
    TOOL_EXECUTION = "tool_execution"
    MEMORY_QUERY = "memory_query"
    USER_INPUT = "user_input"


class MemoryOperationType(Enum):
    """Types of memory operations."""
    WRITE = "write"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    QUERY = "query"


@dataclass
class EvidenceSource:
    """
    A source of evidence with timestamp and attribution.
    """
    
    source_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    source_type: EvidenceSourceType = EvidenceSourceType.WEB_SEARCH
    query: str = ""
    result: Any = None
    timestamp: datetime = field(default_factory=datetime.now)
    attribution: str = ""
    reliability_score: float = 0.5  # 0.0 to 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize evidence source to dictionary."""
        return {
            "source_id": self.source_id,
            "source_type": self.source_type.value,
            "query": self.query,
            "result": str(self.result)[:500] if self.result else None,  # Truncate for serialization
            "timestamp": self.timestamp.isoformat(),
            "attribution": self.attribution,
            "reliability_score": self.reliability_score,
            "metadata": self.metadata,
        }


@dataclass
class MemoryEntry:
    """
    A memory entry with lifecycle metadata.
    """
    
    entry_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    key: str = ""
    value: Any = None
    value_score: float = 0.5  # Quality/relevance score
    provenance: List[str] = field(default_factory=list)  # Source IDs
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def is_expired(self) -> bool:
        """Check if memory entry has expired."""
        if self.expires_at is None:
            return False
        return datetime.now() > self.expires_at
    
    def update(self, new_value: Any, value_score: float, 
              provenance: List[str]) -> None:
        """Update memory entry."""
        self.value = new_value
        self.value_score = value_score
        self.provenance.extend(provenance)
        self.updated_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize memory entry to dictionary."""
        return {
            "entry_id": self.entry_id,
            "key": self.key,
            "value": str(self.value)[:500] if self.value else None,
            "value_score": self.value_score,
            "provenance": self.provenance,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "tags": self.tags,
            "metadata": self.metadata,
        }


@dataclass
class MemoryOperation:
    """
    A memory operation with explicit lifecycle metadata.
    """
    
    operation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    operation_type: MemoryOperationType = MemoryOperationType.WRITE
    entry_id: Optional[str] = None
    key: Optional[str] = None
    value: Any = None
    value_score: float = 0.5
    provenance: List[str] = field(default_factory=list)
    expiry_duration: Optional[timedelta] = None
    tags: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize memory operation to dictionary."""
        return {
            "operation_id": self.operation_id,
            "operation_type": self.operation_type.value,
            "entry_id": self.entry_id,
            "key": self.key,
            "value": str(self.value)[:500] if self.value else None,
            "value_score": self.value_score,
            "provenance": self.provenance,
            "expiry_duration": str(self.expiry_duration) if self.expiry_duration else None,
            "tags": self.tags,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
        }


class MemoryStore:
    """
    Manages memory entries with lifecycle tracking.
    """
    
    def __init__(self):
        self.entries: Dict[str, MemoryEntry] = {}
        self.operations: List[MemoryOperation] = []
    
    def write(self, operation: MemoryOperation) -> MemoryEntry:
        """
        Write a memory entry.
        
        Args:
            operation: Memory operation specifying what to write
            
        Returns:
            Created or updated memory entry
        """
        if operation.key is None:
            raise ValueError("Memory write operation requires a key")
        
        # Calculate expiry
        expires_at = None
        if operation.expiry_duration:
            expires_at = datetime.now() + operation.expiry_duration
        
        # Create or update entry
        if operation.entry_id and operation.entry_id in self.entries:
            entry = self.entries[operation.entry_id]
            entry.update(operation.value, operation.value_score, 
                        operation.provenance)
            if expires_at:
                entry.expires_at = expires_at
            if operation.tags:
                entry.tags.extend(operation.tags)
        else:
            entry = MemoryEntry(
                entry_id=operation.entry_id or str(uuid.uuid4()),
                key=operation.key,
                value=operation.value,
                value_score=operation.value_score,
                provenance=operation.provenance.copy(),
                expires_at=expires_at,
                tags=operation.tags.copy(),
                metadata=operation.metadata.copy(),
            )
            self.entries[entry.entry_id] = entry
        
        # Record operation
        operation.entry_id = entry.entry_id
        self.operations.append(operation)
        
        return entry
    
    def read(self, key: str) -> Optional[MemoryEntry]:
        """Read a memory entry by key."""
        for entry in self.entries.values():
            if entry.key == key and not entry.is_expired():
                return entry
        return None
    
    def query(self, tags: List[str] = None, 
             min_score: float = 0.0) -> List[MemoryEntry]:
        """
        Query memory entries by tags and minimum score.
        
        Args:
            tags: Tags to filter by (entries must have all tags)
            min_score: Minimum value score
            
        Returns:
            List of matching memory entries
        """
        results = []
        for entry in self.entries.values():
            if entry.is_expired():
                continue
            if entry.value_score < min_score:
                continue
            if tags:
                if not all(tag in entry.tags for tag in tags):
                    continue
            results.append(entry)
        return results
    
    def cleanup_expired(self) -> int:
        """Remove expired entries. Returns count of removed entries."""
        expired_keys = [
            entry_id for entry_id, entry in self.entries.items()
            if entry.is_expired()
        ]
        for key in expired_keys:
            del self.entries[key]
        return len(expired_keys)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary of memory store."""
        return {
            "total_entries": len(self.entries),
            "total_operations": len(self.operations),
            "expired_entries": sum(1 for e in self.entries.values() if e.is_expired()),
        }


@dataclass
class ScratchpadPhase:
    """
    Scratchpad Phase: Evidence gathering and memory management.
    """
    
    task_id: str = ""
    evidence_sources: List[EvidenceSource] = field(default_factory=list)
    memory_store: MemoryStore = field(default_factory=MemoryStore)
    timestamp: datetime = field(default_factory=datetime.now)
    
    def formulate_search_query(self, hypothesis: Any, 
                              context: Dict[str, Any]) -> str:
        """
        Formulate a search query for external evidence.
        
        Args:
            hypothesis: The hypothesis to gather evidence for
            context: Additional context for query formulation
            
        Returns:
            Search query string
        """
        # Construct query from hypothesis statement and key terms
        query_parts = [hypothesis.statement]
        if context.get("key_terms"):
            query_parts.extend(context["key_terms"])
        
        query = " ".join(query_parts)
        return query
    
    def execute_tool_call(self, tool_name: str, query: str, 
                         tool_func: Optional[Callable] = None,
                         **kwargs) -> EvidenceSource:
        """
        Execute a tool call with timestamp and attribution.
        
        Args:
            tool_name: Name of the tool
            query: Query or input for the tool
            tool_func: Optional function to execute (for testing)
            **kwargs: Additional arguments for tool
            
        Returns:
            EvidenceSource with results
        """
        source_type_map = {
            "web_search": EvidenceSourceType.WEB_SEARCH,
            "codebase_search": EvidenceSourceType.CODEBASE_SEARCH,
            "file_read": EvidenceSourceType.FILE_READ,
        }
        
        source_type = source_type_map.get(tool_name, EvidenceSourceType.TOOL_EXECUTION)
        
        # Execute tool function with error handling and result validation
        result = None
        reliability_score = 0.5  # Default reliability
        
        if tool_func:
            try:
                result = tool_func(query, **kwargs)
                
                # Assess reliability based on result quality
                if result:
                    result_str = str(result)
                    
                    # Higher reliability for structured results (JSON)
                    if isinstance(result, dict) or (isinstance(result, str) and 
                        (result_str.startswith('{') or result_str.startswith('['))):
                        reliability_score = 0.8
                    
                    # Check for error indicators
                    error_indicators = ['error', 'failed', 'exception', 'traceback']
                    if any(indicator in result_str.lower() for indicator in error_indicators):
                        reliability_score = 0.3
                    
                    # Higher reliability for longer, more detailed results
                    if len(result_str) > 100:
                        reliability_score = min(1.0, reliability_score + 0.1)
                    elif len(result_str) < 20:
                        reliability_score = max(0.2, reliability_score - 0.2)
                else:
                    reliability_score = 0.2  # Empty result is less reliable
                    
            except Exception as e:
                result = json.dumps({
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "query": query,
                    "tool": tool_name
                })
                reliability_score = 0.1  # Errors have very low reliability
        
        evidence_source = EvidenceSource(
            source_type=source_type,
            query=query,
            result=result,
            attribution=f"{tool_name} at {datetime.now().isoformat()}",
            reliability_score=reliability_score,
            metadata={
                "tool_name": tool_name,
                "query_length": len(query),
                "result_length": len(str(result)) if result else 0,
                **kwargs
            },
        )
        
        self.evidence_sources.append(evidence_source)
        return evidence_source
    
    def decide_memory_write(self, evidence: EvidenceSource, 
                           hypothesis_id: str,
                           value_score: float,
                           tags: List[str],
                           expiry_duration: Optional[timedelta] = None) -> MemoryOperation:
        """
        Decide and create a memory write operation.
        
        Args:
            evidence: Evidence source to store
            hypothesis_id: Associated hypothesis ID
            value_score: Quality/relevance score
            tags: Tags for categorization
            expiry_duration: How long to keep in memory
            
        Returns:
            MemoryOperation for writing to memory
        """
        operation = MemoryOperation(
            operation_type=MemoryOperationType.WRITE,
            key=f"evidence_{evidence.source_id}",
            value=evidence.result,
            value_score=value_score,
            provenance=[evidence.source_id, hypothesis_id],
            expiry_duration=expiry_duration or timedelta(days=7),
            tags=tags + [evidence.source_type.value, hypothesis_id],
            metadata={
                "evidence_query": evidence.query,
                "reliability_score": evidence.reliability_score,
            },
        )
        
        # Execute the write
        self.memory_store.write(operation)
        
        return operation
    
    def get_scratchpad_summary(self) -> Dict[str, Any]:
        """Get a summary of the scratchpad phase."""
        return {
            "task_id": self.task_id,
            "evidence_count": len(self.evidence_sources),
            "memory_summary": self.memory_store.get_summary(),
            "timestamp": self.timestamp.isoformat(),
        }

