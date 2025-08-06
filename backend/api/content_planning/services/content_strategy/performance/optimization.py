"""
Optimization Service
Performance optimization and monitoring.
"""

import logging
import time
import asyncio
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import text

logger = logging.getLogger(__name__)

class PerformanceOptimizationService:
    """Service for performance optimization and monitoring."""

    def __init__(self):
        self.performance_metrics = {
            'response_times': {},
            'database_queries': {},
            'memory_usage': {},
            'cache_hit_rates': {}
        }
        
        self.optimization_config = {
            'max_response_time': 2.0,  # seconds
            'max_database_queries': 10,
            'max_memory_usage': 512,  # MB
            'min_cache_hit_rate': 0.8
        }

    async def optimize_response_time(self, operation_name: str, operation_func: Callable, *args, **kwargs) -> Dict[str, Any]:
        """Optimize response time for operations."""
        try:
            start_time = time.time()
            
            # Execute operation
            result = await operation_func(*args, **kwargs)
            
            end_time = time.time()
            response_time = end_time - start_time
            
            # Record performance metrics
            self._record_response_time(operation_name, response_time)
            
            # Check if optimization is needed
            if response_time > self.optimization_config['max_response_time']:
                optimization_suggestions = await self._suggest_response_time_optimizations(operation_name, response_time)
                logger.warning(f"Slow response time for {operation_name}: {response_time:.2f}s")
            else:
                optimization_suggestions = []
            
            return {
                'result': result,
                'response_time': response_time,
                'optimization_suggestions': optimization_suggestions,
                'performance_status': 'optimal' if response_time <= self.optimization_config['max_response_time'] else 'needs_optimization'
            }

        except Exception as e:
            logger.error(f"Error optimizing response time for {operation_name}: {str(e)}")
            return {
                'result': None,
                'response_time': 0.0,
                'optimization_suggestions': ['Error occurred during operation'],
                'performance_status': 'error'
            }

    async def optimize_database_queries(self, db: Session, query_func: Callable, *args, **kwargs) -> Dict[str, Any]:
        """Optimize database queries."""
        try:
            start_time = time.time()
            query_count_before = self._get_query_count(db)
            
            # Execute query function
            result = await query_func(db, *args, **kwargs)
            
            end_time = time.time()
            query_count_after = self._get_query_count(db)
            query_count = query_count_after - query_count_before
            response_time = end_time - start_time
            
            # Record database performance
            self._record_database_performance(query_func.__name__, query_count, response_time)
            
            # Check if optimization is needed
            if query_count > self.optimization_config['max_database_queries']:
                optimization_suggestions = await self._suggest_database_optimizations(query_func.__name__, query_count, response_time)
                logger.warning(f"High query count for {query_func.__name__}: {query_count} queries")
            else:
                optimization_suggestions = []
            
            return {
                'result': result,
                'query_count': query_count,
                'response_time': response_time,
                'optimization_suggestions': optimization_suggestions,
                'performance_status': 'optimal' if query_count <= self.optimization_config['max_database_queries'] else 'needs_optimization'
            }

        except Exception as e:
            logger.error(f"Error optimizing database queries for {query_func.__name__}: {str(e)}")
            return {
                'result': None,
                'query_count': 0,
                'response_time': 0.0,
                'optimization_suggestions': ['Error occurred during database operation'],
                'performance_status': 'error'
            }

    async def optimize_memory_usage(self, operation_name: str, operation_func: Callable, *args, **kwargs) -> Dict[str, Any]:
        """Optimize memory usage for operations."""
        try:
            import psutil
            import os
            
            process = psutil.Process(os.getpid())
            memory_before = process.memory_info().rss / 1024 / 1024  # MB
            
            # Execute operation
            result = await operation_func(*args, **kwargs)
            
            memory_after = process.memory_info().rss / 1024 / 1024  # MB
            memory_used = memory_after - memory_before
            
            # Record memory usage
            self._record_memory_usage(operation_name, memory_used)
            
            # Check if optimization is needed
            if memory_used > self.optimization_config['max_memory_usage']:
                optimization_suggestions = await self._suggest_memory_optimizations(operation_name, memory_used)
                logger.warning(f"High memory usage for {operation_name}: {memory_used:.2f}MB")
            else:
                optimization_suggestions = []
            
            return {
                'result': result,
                'memory_used_mb': memory_used,
                'optimization_suggestions': optimization_suggestions,
                'performance_status': 'optimal' if memory_used <= self.optimization_config['max_memory_usage'] else 'needs_optimization'
            }

        except Exception as e:
            logger.error(f"Error optimizing memory usage for {operation_name}: {str(e)}")
            return {
                'result': None,
                'memory_used_mb': 0.0,
                'optimization_suggestions': ['Error occurred during memory optimization'],
                'performance_status': 'error'
            }

    async def optimize_cache_performance(self, cache_service, operation_name: str) -> Dict[str, Any]:
        """Optimize cache performance."""
        try:
            # Get cache statistics
            cache_stats = await cache_service.get_cache_stats()
            
            # Calculate cache hit rates
            hit_rates = {}
            for cache_type, stats in cache_stats.items():
                if stats.get('entries', 0) > 0:
                    # This is a simplified calculation - in practice, you'd track actual hits/misses
                    hit_rates[cache_type] = 0.8  # Placeholder
            
            # Record cache performance
            self._record_cache_performance(operation_name, hit_rates)
            
            # Check if optimization is needed
            optimization_suggestions = []
            for cache_type, hit_rate in hit_rates.items():
                if hit_rate < self.optimization_config['min_cache_hit_rate']:
                    optimization_suggestions.append(f"Low cache hit rate for {cache_type}: {hit_rate:.2%}")
            
            return {
                'cache_stats': cache_stats,
                'hit_rates': hit_rates,
                'optimization_suggestions': optimization_suggestions,
                'performance_status': 'optimal' if not optimization_suggestions else 'needs_optimization'
            }

        except Exception as e:
            logger.error(f"Error optimizing cache performance: {str(e)}")
            return {
                'cache_stats': {},
                'hit_rates': {},
                'optimization_suggestions': ['Error occurred during cache optimization'],
                'performance_status': 'error'
            }

    def _record_response_time(self, operation_name: str, response_time: float) -> None:
        """Record response time metrics."""
        try:
            if operation_name not in self.performance_metrics['response_times']:
                self.performance_metrics['response_times'][operation_name] = []
            
            self.performance_metrics['response_times'][operation_name].append({
                'response_time': response_time,
                'timestamp': datetime.utcnow().isoformat()
            })
            
            # Keep only last 100 entries
            if len(self.performance_metrics['response_times'][operation_name]) > 100:
                self.performance_metrics['response_times'][operation_name] = self.performance_metrics['response_times'][operation_name][-100:]
                
        except Exception as e:
            logger.error(f"Error recording response time: {str(e)}")

    def _record_database_performance(self, operation_name: str, query_count: int, response_time: float) -> None:
        """Record database performance metrics."""
        try:
            if operation_name not in self.performance_metrics['database_queries']:
                self.performance_metrics['database_queries'][operation_name] = []
            
            self.performance_metrics['database_queries'][operation_name].append({
                'query_count': query_count,
                'response_time': response_time,
                'timestamp': datetime.utcnow().isoformat()
            })
            
            # Keep only last 100 entries
            if len(self.performance_metrics['database_queries'][operation_name]) > 100:
                self.performance_metrics['database_queries'][operation_name] = self.performance_metrics['database_queries'][operation_name][-100:]
                
        except Exception as e:
            logger.error(f"Error recording database performance: {str(e)}")

    def _record_memory_usage(self, operation_name: str, memory_used: float) -> None:
        """Record memory usage metrics."""
        try:
            if operation_name not in self.performance_metrics['memory_usage']:
                self.performance_metrics['memory_usage'][operation_name] = []
            
            self.performance_metrics['memory_usage'][operation_name].append({
                'memory_used_mb': memory_used,
                'timestamp': datetime.utcnow().isoformat()
            })
            
            # Keep only last 100 entries
            if len(self.performance_metrics['memory_usage'][operation_name]) > 100:
                self.performance_metrics['memory_usage'][operation_name] = self.performance_metrics['memory_usage'][operation_name][-100:]
                
        except Exception as e:
            logger.error(f"Error recording memory usage: {str(e)}")

    def _record_cache_performance(self, operation_name: str, hit_rates: Dict[str, float]) -> None:
        """Record cache performance metrics."""
        try:
            if operation_name not in self.performance_metrics['cache_hit_rates']:
                self.performance_metrics['cache_hit_rates'][operation_name] = []
            
            self.performance_metrics['cache_hit_rates'][operation_name].append({
                'hit_rates': hit_rates,
                'timestamp': datetime.utcnow().isoformat()
            })
            
            # Keep only last 100 entries
            if len(self.performance_metrics['cache_hit_rates'][operation_name]) > 100:
                self.performance_metrics['cache_hit_rates'][operation_name] = self.performance_metrics['cache_hit_rates'][operation_name][-100:]
                
        except Exception as e:
            logger.error(f"Error recording cache performance: {str(e)}")

    def _get_query_count(self, db: Session) -> int:
        """Get current query count from database session."""
        try:
            # This is a simplified implementation
            # In practice, you'd use database-specific monitoring tools
            return 0
        except Exception as e:
            logger.error(f"Error getting query count: {str(e)}")
            return 0

    async def _suggest_response_time_optimizations(self, operation_name: str, response_time: float) -> List[str]:
        """Suggest optimizations for slow response times."""
        try:
            suggestions = []
            
            if response_time > 5.0:
                suggestions.append("Consider implementing caching for this operation")
                suggestions.append("Review database query optimization")
                suggestions.append("Consider async processing for heavy operations")
            elif response_time > 2.0:
                suggestions.append("Optimize database queries")
                suggestions.append("Consider adding indexes for frequently accessed data")
                suggestions.append("Review data processing algorithms")
            
            # Add operation-specific suggestions
            if 'ai_analysis' in operation_name.lower():
                suggestions.append("Consider implementing AI response caching")
                suggestions.append("Review AI service integration efficiency")
            elif 'onboarding' in operation_name.lower():
                suggestions.append("Optimize data transformation algorithms")
                suggestions.append("Consider batch processing for large datasets")
            
            return suggestions
            
        except Exception as e:
            logger.error(f"Error suggesting response time optimizations: {str(e)}")
            return ["Unable to generate optimization suggestions"]

    async def _suggest_database_optimizations(self, operation_name: str, query_count: int, response_time: float) -> List[str]:
        """Suggest optimizations for database performance."""
        try:
            suggestions = []
            
            if query_count > 20:
                suggestions.append("Implement query batching to reduce database calls")
                suggestions.append("Review and optimize N+1 query patterns")
                suggestions.append("Consider implementing database connection pooling")
            elif query_count > 10:
                suggestions.append("Optimize database queries with proper indexing")
                suggestions.append("Consider implementing query result caching")
                suggestions.append("Review database schema for optimization opportunities")
            
            if response_time > 1.0:
                suggestions.append("Add database indexes for frequently queried columns")
                suggestions.append("Consider read replicas for heavy read operations")
                suggestions.append("Optimize database connection settings")
            
            # Add operation-specific suggestions
            if 'strategy' in operation_name.lower():
                suggestions.append("Consider implementing strategy data caching")
                suggestions.append("Optimize strategy-related database queries")
            elif 'onboarding' in operation_name.lower():
                suggestions.append("Batch onboarding data processing")
                suggestions.append("Optimize onboarding data retrieval queries")
            
            return suggestions
            
        except Exception as e:
            logger.error(f"Error suggesting database optimizations: {str(e)}")
            return ["Unable to generate database optimization suggestions"]

    async def _suggest_memory_optimizations(self, operation_name: str, memory_used: float) -> List[str]:
        """Suggest optimizations for memory usage."""
        try:
            suggestions = []
            
            if memory_used > 100:
                suggestions.append("Implement data streaming for large datasets")
                suggestions.append("Review memory-intensive data structures")
                suggestions.append("Consider implementing pagination")
            elif memory_used > 50:
                suggestions.append("Optimize data processing algorithms")
                suggestions.append("Review object lifecycle management")
                suggestions.append("Consider implementing lazy loading")
            
            # Add operation-specific suggestions
            if 'ai_analysis' in operation_name.lower():
                suggestions.append("Implement AI response streaming")
                suggestions.append("Optimize AI model memory usage")
            elif 'onboarding' in operation_name.lower():
                suggestions.append("Process onboarding data in smaller chunks")
                suggestions.append("Implement data cleanup after processing")
            
            return suggestions
            
        except Exception as e:
            logger.error(f"Error suggesting memory optimizations: {str(e)}")
            return ["Unable to generate memory optimization suggestions"]

    async def get_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance report."""
        try:
            report = {
                'timestamp': datetime.utcnow().isoformat(),
                'response_times': self._calculate_average_response_times(),
                'database_performance': self._calculate_database_performance(),
                'memory_usage': self._calculate_memory_usage(),
                'cache_performance': self._calculate_cache_performance(),
                'optimization_recommendations': await self._generate_optimization_recommendations()
            }
            
            return report
            
        except Exception as e:
            logger.error(f"Error generating performance report: {str(e)}")
            return {
                'timestamp': datetime.utcnow().isoformat(),
                'error': str(e)
            }

    def _calculate_average_response_times(self) -> Dict[str, float]:
        """Calculate average response times for operations."""
        try:
            averages = {}
            for operation_name, times in self.performance_metrics['response_times'].items():
                if times:
                    avg_time = sum(t['response_time'] for t in times) / len(times)
                    averages[operation_name] = avg_time
            
            return averages
            
        except Exception as e:
            logger.error(f"Error calculating average response times: {str(e)}")
            return {}

    def _calculate_database_performance(self) -> Dict[str, Dict[str, float]]:
        """Calculate database performance metrics."""
        try:
            performance = {}
            for operation_name, queries in self.performance_metrics['database_queries'].items():
                if queries:
                    avg_queries = sum(q['query_count'] for q in queries) / len(queries)
                    avg_time = sum(q['response_time'] for q in queries) / len(queries)
                    performance[operation_name] = {
                        'average_queries': avg_queries,
                        'average_response_time': avg_time
                    }
            
            return performance
            
        except Exception as e:
            logger.error(f"Error calculating database performance: {str(e)}")
            return {}

    def _calculate_memory_usage(self) -> Dict[str, float]:
        """Calculate average memory usage for operations."""
        try:
            averages = {}
            for operation_name, usage in self.performance_metrics['memory_usage'].items():
                if usage:
                    avg_memory = sum(u['memory_used_mb'] for u in usage) / len(usage)
                    averages[operation_name] = avg_memory
            
            return averages
            
        except Exception as e:
            logger.error(f"Error calculating memory usage: {str(e)}")
            return {}

    def _calculate_cache_performance(self) -> Dict[str, float]:
        """Calculate cache performance metrics."""
        try:
            performance = {}
            for operation_name, rates in self.performance_metrics['cache_hit_rates'].items():
                if rates:
                    # Calculate average hit rate across all cache types
                    all_rates = []
                    for rate_data in rates:
                        if rate_data['hit_rates']:
                            avg_rate = sum(rate_data['hit_rates'].values()) / len(rate_data['hit_rates'])
                            all_rates.append(avg_rate)
                    
                    if all_rates:
                        performance[operation_name] = sum(all_rates) / len(all_rates)
            
            return performance
            
        except Exception as e:
            logger.error(f"Error calculating cache performance: {str(e)}")
            return {}

    async def _generate_optimization_recommendations(self) -> List[str]:
        """Generate optimization recommendations based on performance data."""
        try:
            recommendations = []
            
            # Check response times
            avg_response_times = self._calculate_average_response_times()
            for operation, avg_time in avg_response_times.items():
                if avg_time > self.optimization_config['max_response_time']:
                    recommendations.append(f"Optimize response time for {operation} (avg: {avg_time:.2f}s)")
            
            # Check database performance
            db_performance = self._calculate_database_performance()
            for operation, perf in db_performance.items():
                if perf['average_queries'] > self.optimization_config['max_database_queries']:
                    recommendations.append(f"Reduce database queries for {operation} (avg: {perf['average_queries']:.1f} queries)")
            
            # Check memory usage
            memory_usage = self._calculate_memory_usage()
            for operation, memory in memory_usage.items():
                if memory > self.optimization_config['max_memory_usage']:
                    recommendations.append(f"Optimize memory usage for {operation} (avg: {memory:.1f}MB)")
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating optimization recommendations: {str(e)}")
            return ["Unable to generate optimization recommendations"]

    async def cleanup_old_metrics(self, days_to_keep: int = 30) -> Dict[str, int]:
        """Clean up old performance metrics."""
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days_to_keep)
            cleaned_count = 0
            
            for metric_type, operations in self.performance_metrics.items():
                for operation_name, metrics in operations.items():
                    if isinstance(metrics, list):
                        original_count = len(metrics)
                        # Filter out old metrics
                        self.performance_metrics[metric_type][operation_name] = [
                            m for m in metrics 
                            if datetime.fromisoformat(m['timestamp']) > cutoff_date
                        ]
                        cleaned_count += original_count - len(self.performance_metrics[metric_type][operation_name])
            
            logger.info(f"Cleaned up {cleaned_count} old performance metrics")
            return {'cleaned_count': cleaned_count}
            
        except Exception as e:
            logger.error(f"Error cleaning up old metrics: {str(e)}")
            return {'cleaned_count': 0} 