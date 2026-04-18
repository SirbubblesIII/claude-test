"""
Basic usage example for Sage-Conformant Intelligence reasoning module.
"""

import os
from pathlib import Path
from typing import List, Optional
from urllib.parse import quote_plus
import json

from sage_reasoning import ReasoningPipeline


def web_search_tool(query: str, max_results: int = 5, **kwargs) -> str:
    """
    Real web search tool using DuckDuckGo search API.
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return
        **kwargs: Additional search parameters
        
    Returns:
        JSON string with search results including titles, URLs, and snippets
    """
    try:
        # Try to use duckduckgo-search if available
        try:
            from duckduckgo_search import DDGS
            
            results = []
            with DDGS() as ddgs:
                search_results = ddgs.text(
                    query,
                    max_results=max_results,
                    safesearch='moderate'
                )
                
                for result in search_results:
                    results.append({
                        "title": result.get("title", ""),
                        "url": result.get("href", ""),
                        "snippet": result.get("body", ""),
                    })
            
            if results:
                return json.dumps({
                    "query": query,
                    "results": results,
                    "count": len(results),
                    "source": "duckduckgo_search"
                }, indent=2)
            else:
                return json.dumps({
                    "query": query,
                    "results": [],
                    "count": 0,
                    "message": "No results found",
                    "source": "duckduckgo_search"
                })
                
        except ImportError:
            # Fallback: Use requests to scrape DuckDuckGo HTML (no API key needed)
            try:
                import requests
                from html import unescape
                
                url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                }
                
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                
                # Simple HTML parsing for results
                from html.parser import HTMLParser
                
                class ResultParser(HTMLParser):
                    def __init__(self):
                        super().__init__()
                        self.results = []
                        self.current_result = {}
                        self.in_result = False
                        self.in_title = False
                        self.in_snippet = False
                        self.current_text = ""
                        
                    def handle_starttag(self, tag, attrs):
                        attrs_dict = dict(attrs)
                        if tag == "a" and "result__a" in attrs_dict.get("class", ""):
                            self.in_title = True
                            self.in_result = True
                            self.current_result = {"url": attrs_dict.get("href", "")}
                        elif tag == "a" and self.in_result:
                            self.in_snippet = True
                            
                    def handle_endtag(self, tag):
                        if tag == "a" and self.in_title:
                            self.in_title = False
                            self.current_result["title"] = self.current_text.strip()
                            self.current_text = ""
                        elif tag == "a" and self.in_snippet:
                            self.in_snippet = False
                            self.current_result["snippet"] = self.current_text.strip()
                            if len(self.results) < max_results:
                                self.results.append(self.current_result.copy())
                            self.current_result = {}
                            self.in_result = False
                            self.current_text = ""
                            
                    def handle_data(self, data):
                        if self.in_title or self.in_snippet:
                            self.current_text += data
                
                parser = ResultParser()
                parser.feed(response.text)
                
                results = parser.results[:max_results]
                
                return json.dumps({
                    "query": query,
                    "results": results,
                    "count": len(results),
                    "source": "duckduckgo_html"
                }, indent=2)
                
            except ImportError:
                # Final fallback: Return structured mock data with instructions
                return json.dumps({
                    "query": query,
                    "results": [
                        {
                            "title": f"Search results for: {query}",
                            "url": "https://example.com",
                            "snippet": f"To enable real web search, install: pip install duckduckgo-search or pip install requests"
                        }
                    ],
                    "count": 1,
                    "source": "fallback",
                    "note": "Install duckduckgo-search for real search results"
                })
                
    except Exception as e:
        return json.dumps({
            "query": query,
            "error": str(e),
            "error_type": type(e).__name__,
            "results": []
        })


def codebase_search_tool(query: str, root_dir: Optional[str] = None, 
                        file_extensions: Optional[List[str]] = None,
                        max_results: int = 10, **kwargs) -> str:
    """
    Real codebase search tool using semantic file content search.
    
    Searches through code files for relevant content matching the query.
    
    Args:
        query: Search query string
        root_dir: Root directory to search (defaults to current working directory)
        file_extensions: List of file extensions to search (defaults to common code files)
        max_results: Maximum number of matching files to return
        **kwargs: Additional search parameters
        
    Returns:
        JSON string with matching file paths, line numbers, and snippets
    """
    if root_dir is None:
        root_dir = os.getcwd()
    
    if file_extensions is None:
        file_extensions = ['.py', '.js', '.ts', '.java', '.cpp', '.c', '.h', 
                          '.go', '.rs', '.rb', '.php', '.swift', '.kt', '.md']
    
    root_path = Path(root_dir)
    if not root_path.exists():
        return json.dumps({
            "query": query,
            "error": f"Root directory does not exist: {root_dir}",
            "results": []
        })
    
    # Normalize query for search
    query_lower = query.lower()
    query_terms = query_lower.split()
    
    results = []
    files_searched = 0
    
    # Walk through directory tree
    for ext in file_extensions:
        for file_path in root_path.rglob(f"*{ext}"):
            # Skip common ignore patterns
            if any(ignore in str(file_path) for ignore in [
                '__pycache__', '.git', 'node_modules', '.venv', 'venv',
                'dist', 'build', '.pytest_cache', '.mypy_cache'
            ]):
                continue
            
            try:
                files_searched += 1
                if files_searched > 1000:  # Limit total files searched
                    break
                    
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    content_lower = content.lower()
                    
                    # Calculate relevance score
                    score = 0
                    matches = []
                    
                    for term in query_terms:
                        if term in content_lower:
                            # Count occurrences
                            count = content_lower.count(term)
                            score += count
                            
                            # Find line numbers
                            for i, line in enumerate(content.split('\n'), 1):
                                if term in line.lower():
                                    matches.append({
                                        "line": i,
                                        "content": line.strip()[:200]  # Truncate long lines
                                    })
                    
                    if score > 0:
                        # Calculate relative path
                        try:
                            rel_path = str(file_path.relative_to(root_path))
                        except ValueError:
                            rel_path = str(file_path)
                        
                        results.append({
                            "file": rel_path,
                            "absolute_path": str(file_path),
                            "score": score,
                            "matches": matches[:5],  # Limit matches per file
                            "file_size": len(content)
                        })
                        
            except (PermissionError, UnicodeDecodeError, OSError):
                # Skip files we can't read
                continue
            
            if len(results) >= max_results:
                break
        
        if len(results) >= max_results:
            break
    
    # Sort by relevance score
    results.sort(key=lambda x: x["score"], reverse=True)
    results = results[:max_results]
    
    return json.dumps({
        "query": query,
        "results": results,
        "count": len(results),
        "files_searched": files_searched,
        "source": "codebase_search"
    }, indent=2)


def file_read_tool(query: str, **kwargs) -> str:
    """
    Real file reading tool that reads and returns file contents.
    
    Args:
        query: File path to read (can be relative or absolute)
        **kwargs: Additional parameters (encoding, max_lines, etc.)
        
    Returns:
        JSON string with file contents and metadata
    """
    file_path = query.strip()
    encoding = kwargs.get("encoding", "utf-8")
    max_lines = kwargs.get("max_lines", None)
    
    try:
        path = Path(file_path)
        
        # If relative path, try to resolve it
        if not path.is_absolute():
            # Try current directory first
            if not path.exists():
                # Try parent directories
                current = Path.cwd()
                for parent in [current] + list(current.parents):
                    candidate = parent / path
                    if candidate.exists() and candidate.is_file():
                        path = candidate
                        break
        
        if not path.exists():
            return json.dumps({
                "query": query,
                "error": f"File not found: {file_path}",
                "results": []
            })
        
        if not path.is_file():
            return json.dumps({
                "query": query,
                "error": f"Path is not a file: {file_path}",
                "results": []
            })
        
        # Check file size (don't read huge files)
        file_size = path.stat().st_size
        if file_size > 10 * 1024 * 1024:  # 10MB limit
            return json.dumps({
                "query": query,
                "error": f"File too large: {file_size} bytes (max 10MB)",
                "file_size": file_size,
                "results": []
            })
        
        # Read file
        with open(path, 'r', encoding=encoding, errors='replace') as f:
            if max_lines:
                lines = []
                for i, line in enumerate(f):
                    if i >= max_lines:
                        lines.append(f"... (truncated, showing first {max_lines} lines)")
                        break
                    lines.append(line.rstrip('\n\r'))
                content = '\n'.join(lines)
            else:
                content = f.read()
        
        return json.dumps({
            "query": query,
            "file_path": str(path),
            "file_size": file_size,
            "encoding": encoding,
            "line_count": len(content.splitlines()),
            "content": content,
            "source": "file_read"
        }, indent=2)
        
    except Exception as e:
        return json.dumps({
            "query": query,
            "error": str(e),
            "error_type": type(e).__name__,
            "results": []
        })


def main():
    """Run a basic reasoning example."""
    
    # Initialize pipeline
    pipeline = ReasoningPipeline()
    
    # Register real tools for evidence gathering
    pipeline.register_tool("web_search", web_search_tool)
    pipeline.register_tool("codebase_search", codebase_search_tool)
    pipeline.register_tool("file_read", file_read_tool)
    
    # Define task
    task = "How should we design a scalable authentication system?"
    
    # Provide context
    context = {
        "min_hypotheses": 2,
        "preserve_dissent": True,
        "include_actionable_steps": True,
        "hypotheses": [
            {
                "statement": "Use OAuth 2.0 with JWT tokens for stateless authentication",
                "rationale": "Industry standard, stateless, scalable",
                "confidence": 0.7,
            },
            {
                "statement": "Use session-based authentication with Redis for state management",
                "rationale": "More control, easier revocation, Redis provides scalability",
                "confidence": 0.6,
            },
        ],
        "edge_cases": [
            "Token expiration and refresh handling",
            "Cross-domain authentication",
            "Rate limiting and brute force protection",
        ],
        "assumptions": [
            "System must support millions of concurrent users",
            "Security is a primary concern",
        ],
        "analogies": [
            {
                "domain": "Physical Security",
                "analogy": "Like a keycard system: tokens grant access, can be revoked",
            },
        ],
        "metaphors": [
            {
                "metaphor": "Authentication is the bouncer at the club door",
                "source": "Security Architecture",
            },
        ],
    }
    
    # Execute reasoning
    print("Executing reasoning pipeline...")
    trace = pipeline.execute(task, context)
    
    # Display results
    print("\n" + "="*80)
    print("REASONING OUTPUT")
    print("="*80)
    print(trace.final_output)
    
    print("\n" + "="*80)
    print("REASONING TRACE SUMMARY")
    print("="*80)
    print(f"Trace ID: {trace.trace_id}")
    print(f"Task: {trace.task_description}")
    print(f"Hypotheses: {len(trace.reasoning_phase.hypotheses)}")
    print(f"Evidence Sources: {len(trace.scratchpad_phase.evidence_sources)}")
    print(f"Memory Entries: {trace.scratchpad_phase.memory_store.get_summary()['total_entries']}")
    
    # Export trace
    trace_path = f"trace_{trace.trace_id[:8]}.json"
    pipeline.export_trace(trace.trace_id, trace_path)
    print(f"\nTrace exported to: {trace_path}")


if __name__ == "__main__":
    main()

